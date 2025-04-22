from typing import Dict, Any, List, Optional, Tuple
from transformers import BertTokenizer, BertModel, BertForSequenceClassification
import json
from datetime import datetime
import re
import torch
import os
import asyncio
import logging
from collections import defaultdict
import psutil
import time
import openai
from openai import AsyncOpenAI
from src.database.history_dao import HistoryDAO
import uuid
from sqlalchemy.orm import Session

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Task:
    """任务类"""
    def __init__(self, task_id: str, task_type: str, parameters: Dict[str, Any]):
        self.task_id = task_id
        self.task_type = task_type
        self.parameters = parameters
        self.status = "pending"
        self.result = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.priority = parameters.get("priority", "normal")
        self.dependencies = parameters.get("dependencies", [])
        self.retry_count = 0
        self.max_retries = 3
        self.error = None

class PerformanceMonitor:
    """性能监控器"""
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "error_rates": {},
            "resource_usage": {},
            "model_latency": {}
        }
    
    async def __aenter__(self):
        self.start_time = time.time()
        self.resource_start = psutil.Process().memory_info().rss
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        resource_end = psutil.Process().memory_info().rss
        
        # 记录性能指标
        self.metrics["response_times"].append(end_time - self.start_time)
        self.metrics["resource_usage"][id(self)] = resource_end - self.resource_start

class TaskScheduler:
    """任务调度器"""
    def __init__(self, orchestrator):
        self.task_queue = asyncio.PriorityQueue()
        self.resource_pool = ResourcePool()
        self._lock = asyncio.Lock()
        self.orchestrator = orchestrator  # 保存对 orchestrator 的引用
    
    async def schedule_task(self, task: Task):
        async with self._lock:
            # 评估任务优先级
            priority = self._evaluate_priority(task)
            
            # 检查资源可用性
            required_resources = self._estimate_resources(task)
            
            if self.resource_pool.can_allocate(required_resources):
                await self._execute_task(task)
            else:
                # 加入等待队列
                await self.task_queue.put((priority, task))
    
    async def _execute_task(self, task: Task):
        """执行任务
        
        Args:
            task: 要执行的任务
        """
        try:
            # 分配资源
            self.resource_pool.allocate(task.task_id, self._estimate_resources(task))
            
            # 更新任务状态
            task.status = "running"
            task.updated_at = datetime.now()
            
            # 获取对应的 agent
            agent = self.orchestrator.agents.get(task.task_type)
            if not agent:
                raise ValueError(f"未找到对应的 Agent: {task.task_type}")
            
            # 调用 agent 处理任务
            result = await agent.process(task.parameters)
            
            # 更新任务状态和结果
            task.status = "completed"
            task.result = result
            task.updated_at = datetime.now()
            
        except Exception as e:
            # 更新任务状态
            task.status = "failed"
            task.error = str(e)
            task.updated_at = datetime.now()
            raise e
            
        finally:
            # 释放资源
            self.resource_pool.release(task.task_id)
    
    def _evaluate_priority(self, task: Task) -> int:
        priority_map = {"high": 1, "normal": 2, "low": 3}
        return priority_map.get(task.priority, 2)
    
    def _estimate_resources(self, task: Task) -> Dict[str, Any]:
        # 根据任务类型估算所需资源
        resource_estimates = {
            "order": {"cpu": 0.1, "memory": 100},
            "planning": {"cpu": 0.2, "memory": 200},
            "prediction": {"cpu": 0.3, "memory": 300},
            "finance": {"cpu": 0.1, "memory": 150}
        }
        return resource_estimates.get(task.task_type, {"cpu": 0.1, "memory": 100})

class ResourcePool:
    """资源池"""
    def __init__(self):
        self.available_resources = {
            "cpu": psutil.cpu_count(),
            "memory": psutil.virtual_memory().available
        }
        self.allocated_resources = defaultdict(lambda: {"cpu": 0, "memory": 0})
    
    def can_allocate(self, resources: Dict[str, Any]) -> bool:
        return (self.available_resources["cpu"] >= resources["cpu"] and
                self.available_resources["memory"] >= resources["memory"])
    
    def allocate(self, task_id: str, resources: Dict[str, Any]):
        self.available_resources["cpu"] -= resources["cpu"]
        self.available_resources["memory"] -= resources["memory"]
        self.allocated_resources[task_id] = resources
    
    def release(self, task_id: str):
        resources = self.allocated_resources[task_id]
        self.available_resources["cpu"] += resources["cpu"]
        self.available_resources["memory"] += resources["memory"]
        del self.allocated_resources[task_id]

class LLMOrchestrator:
    """LLM编排器"""
    
    def __init__(self, db_session, openai_api_key: Optional[str] = None, agents: Optional[List[Any]] = None):
        """初始化编排器
        
        Args:
            db_session: 数据库会话
            openai_api_key: OpenAI API 密钥，如果不提供则从环境变量获取
            agents: 要注册的 agent 列表
        """
        self.agents = {}
        self.tasks = {}
        self.performance_monitor = PerformanceMonitor()
        self.task_scheduler = TaskScheduler(self)
        self._cache = {}
        self._lock = asyncio.Lock()
        self.history = []  # 添加历史记录列表
        self.db_session = db_session
        self.history_dao = HistoryDAO(db_session)
        
        # 初始化 OpenAI 客户端
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("未提供 OpenAI API 密钥，请设置 OPENAI_API_KEY 环境变量或通过参数传入")
        self.openai_client = AsyncOpenAI(api_key=api_key)
        
        logger.info("正在加载模型...")
        try:
            # 加载BERT分类器
            self.tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
            self.model = BertForSequenceClassification.from_pretrained("bert-base-chinese", num_labels=5)  # 5个任务类型
            
            # 将模型移到GPU（如果可用）
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self.model.to(self.device)
            self.model.eval()
            
            logger.info("模型加载完成")
            
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            raise e
            
        # 注册 agents
        if agents:
            for agent in agents:
                self.register_agent(agent)
    
    def register_agent(self, agent):
        """注册Agent"""
        self.agents[agent.agent_type] = agent
        logger.info(f"Agent {agent.agent_id} ({agent.agent_type}) 已注册")
    
    async def process_instruction(self, text: str, db: Session) -> Dict:
        """处理指令
        
        Args:
            text: 输入文本指令
            db: 数据库会话
            
        Returns:
            处理结果字典
        """
        start_time = time.time()
        task_id = str(uuid.uuid4())
        result = {}
        status = "failed"
        agents_involved = []
        task_type = "unknown"
        
        try:
            # 分析指令
            task_info = await self._analyze_instruction(text)
            task_type = task_info["main_task"]
            agents_involved = task_info["required_agents"]
            
            # 执行任务
            result = await self._execute_task(task_info)
            status = "completed"
            
            # 保存历史记录
            history_entry = {
                'timestamp': datetime.now(),
                'task_id': task_id,
                'task_type': task_type,
                'input_text': text,
                'result': result,
                'status': status,
                'execution_time': time.time() - start_time,
                'agents_involved': agents_involved
            }
            await self.history_dao.add_history(db, history_entry)
            
            return result
            
        except Exception as e:
            logger.error(f"处理指令失败: {str(e)}")
            result = {"error": str(e)}
            status = "failed"
            
            # 保存错误记录
            history_entry = {
                'timestamp': datetime.now(),
                'task_id': task_id,
                'task_type': task_type,
                'input_text': text,
                'result': result,
                'status': status,
                'execution_time': time.time() - start_time,
                'agents_involved': agents_involved,
                'error': str(e)
            }
            await self.history_dao.add_history(db, history_entry)
            
            raise e
    
    async def _execute_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """执行任务
        
        Args:
            task_info: 任务信息，包含main_task、required_agents等
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        results = {}
        task_sequence = self._generate_task_sequence(task_info)
        
        for task in task_sequence:
            agent_type = task["type"]
            agent = self.agents.get(agent_type)
            if not agent:
                raise ValueError(f"未找到对应的Agent: {agent_type}")
            
            try:
                # 调用agent处理任务
                task_result = await agent.process(task["parameters"])
                results[agent_type] = task_result.to_dict() if hasattr(task_result, 'to_dict') else task_result
            except Exception as e:
                logger.error(f"Agent {agent_type} 处理任务失败: {str(e)}")
                results[agent_type] = {"error": str(e)}
        
        return self._generate_final_result(results)
    
    async def _analyze_instruction(self, text: str) -> Dict[str, Any]:
        """分析指令"""
        # 使用OpenAI分析任务
        analysis = await self._analyze_with_llm(text, self._extract_info_from_text(text))
        
        # 确定优先级
        priority = self._determine_priority(analysis["extracted_info"])
        analysis["priority"] = priority
        
        return analysis
    
    async def _analyze_with_llm(self, text: str, extracted_info: Dict[str, Any]) -> Dict[str, Any]:
        """使用大模型分析任务和依赖关系"""
        prompt = f"""请分析以下订单需求，并确定需要哪些 agent 参与处理，以及它们之间的依赖关系：

订单内容：{text}

已提取的信息：
{json.dumps(extracted_info, ensure_ascii=False, indent=2)}

可用的 agent 类型：
1. order: 处理订单基本信息
2. planning: 制定生产计划
3. supply_chain: 处理采购和供应链
4. finance: 处理财务相关
5. prediction: 进行预测分析

请按照以下格式返回分析结果：
{{
    "main_task": "主要任务类型",
    "required_agents": ["需要的 agent 列表"],
    "dependencies": {{
        "agent1": ["依赖的 agent 列表"],
        "agent2": ["依赖的 agent 列表"]
    }},
    "constraints": ["约束条件列表"],
    "reasoning": "推理过程说明",
    "extracted_info": {json.dumps(extracted_info, ensure_ascii=False)}
}}"""
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的 ERP 系统分析员，擅长分析订单需求并确定处理流程。请以JSON格式返回分析结果。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            logger.error(f"调用 OpenAI API 失败: {str(e)}")
            # 使用默认值
            return {
                "main_task": "order",
                "required_agents": ["order"],
                "dependencies": {},
                "constraints": [],
                "reasoning": "分析失败，使用默认值",
                "extracted_info": extracted_info
            }
    
    def _extract_info_from_text(self, text: str) -> Dict[str, Any]:
        """从文本中提取关键信息"""
        info = {
            "quantity": 0,
            "product_specs": {},
            "delivery_date": None,
            "delivery_address": None
        }
        
        # 提取数量
        quantity_match = re.search(r'(\d+)\s*台', text)
        if quantity_match:
            info["quantity"] = int(quantity_match.group(1))
        
        # 提取配置信息
        specs = {
            "cpu": re.search(r'(Intel\s+i\d+|AMD\s+Ryzen\s+\d+)', text),
            "memory": re.search(r'(\d+)GB', text),
            "storage": re.search(r'(\d+)TB', text),
            "gpu": re.search(r'(NVIDIA\s+RTX\s+\d+|AMD\s+Radeon\s+\w+)', text)
        }
        
        info["product_specs"] = {
            key: match.group(1) if match else None
            for key, match in specs.items()
        }
        
        # 提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        if date_match:
            info["delivery_date"] = date_match.group(1)
        
        # 提取地址
        address_match = re.search(r'地址是(.*?)[。\n]', text)
        if address_match:
            info["delivery_address"] = address_match.group(1).strip()
        
        return info
    
    def _determine_priority(self, extracted_info: Dict[str, Any]) -> str:
        """确定优先级"""
        quantity = int(extracted_info.get("quantity", 0))
        if quantity > 1000:
            return "high"
        elif quantity > 100:
            return "normal"
        else:
            return "low"
    
    def _generate_task_sequence(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成任务序列"""
        task_sequence = []
        required_agents = analysis["required_agents"]
        dependencies = analysis["dependencies"]
        
        # 创建依赖图
        processed = set()
        
        def can_process(agent):
            return all(dep in processed for dep in dependencies.get(agent, []))
        
        # 按依赖顺序添加任务
        while len(processed) < len(required_agents):
            for agent in required_agents:
                if agent not in processed and can_process(agent):
                    task_sequence.append({
                        "type": agent,
                        "parameters": self._create_task_parameters(agent, analysis)
                    })
                    processed.add(agent)
        
        return task_sequence
    
    def _create_task_parameters(self, agent_type: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """创建任务参数"""
        extracted_info = analysis["extracted_info"]
        base_params = {
            "priority": analysis["priority"],
            "constraints": analysis["constraints"],
            "product_info": extracted_info
        }
        
        if agent_type == "order":
            base_params.update({
                "order_type": "computer_assembly",
                "quantity": extracted_info["quantity"],
                "delivery_info": {
                    "date": extracted_info["delivery_date"],
                    "address": extracted_info["delivery_address"]
                }
            })
        
        elif agent_type == "planning":
            base_params.update({
                "production_type": "assembly",
                "deadline": extracted_info["delivery_date"],
                "quantity": extracted_info["quantity"]
            })
        
        elif agent_type == "supply_chain":
            base_params.update({
                "required_components": extracted_info["product_specs"],
                "quantity": extracted_info["quantity"],
                "deadline": extracted_info["delivery_date"]
            })
        
        elif agent_type == "finance":
            # 简单的成本估算
            quantity = extracted_info["quantity"]
            base_params.update({
                "cost_estimation": {
                    "materials": quantity * 5000,  # 材料成本
                    "labor": quantity * 1000,      # 人工成本
                    "overhead": quantity * 500      # 管理费用
                }
            })
        
        elif agent_type == "prediction":
            base_params.update({
                "prediction_type": "demand",
                "product_type": "high_performance_computer",
                "market_segment": "enterprise"
            })
        
        return base_params
    
    def _generate_final_result(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终结果"""
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "results": results
        } 