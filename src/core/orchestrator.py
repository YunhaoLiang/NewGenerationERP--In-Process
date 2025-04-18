from typing import Dict, Any, List
from transformers import BertTokenizer, BertModel
import json
from datetime import datetime
import re
import torch
import os

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

class LLMOrchestrator:
    """LLM编排器"""
    
    def __init__(self):
        """初始化编排器"""
        self.agents = {}
        self.tasks = {}
        
        print("正在加载模型...")
        try:
            # 直接从在线加载模型
            self.tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
            self.model = BertModel.from_pretrained("bert-base-chinese")
            
            # 将模型移到GPU（如果可用）
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self.model.to(self.device)
            self.model.eval()
            
            print("模型加载完成")
            
        except Exception as e:
            print(f"模型加载失败: {str(e)}")
            raise e
        
    def register_agent(self, agent):
        """注册Agent
        
        Args:
            agent: Agent实例
        """
        self.agents[agent.agent_type] = agent
        print(f"Agent {agent.agent_id} ({agent.agent_type}) 已注册")
        
    async def process_instruction(self, text: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理指令
        
        Args:
            text: 自然语言指令
            parameters: 额外参数
            
        Returns:
            Dict: 处理结果
        """
        try:
            print("\n=== 开始处理指令 ===")
            print(f"指令内容: {text}")
            
            # 1. 分析指令类型和需求
            task_analysis = self._analyze_instruction(text)
            print(f"\n指令分析结果: {json.dumps(task_analysis, ensure_ascii=False, indent=2)}")
            
            # 2. 生成任务序列
            task_sequence = self._generate_task_sequence(task_analysis, parameters)
            print(f"\n生成的任务序列: {json.dumps(task_sequence, ensure_ascii=False, indent=2)}")
            
            # 3. 执行任务序列
            results = {}
            for task_info in task_sequence:
                task = Task(
                    task_id=f"TASK_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    task_type=task_info["type"],
                    parameters=task_info["parameters"]
                )
                
                # 执行任务
                agent = self.agents.get(task.task_type)
                if agent:
                    print(f"\n=== 执行任务: {task.task_type} ===")
                    print(f"任务参数: {json.dumps(task.parameters, ensure_ascii=False, indent=2)}")
                    
                    # 更新任务状态
                    task.status = "processing"
                    task.updated_at = datetime.now()
                    
                    # 执行任务
                    result = await agent.process(task.parameters)
                    task.result = result
                    task.status = "completed"
                    task.updated_at = datetime.now()
                    
                    # 保存结果
                    results[task.task_type] = result.data if hasattr(result, 'data') else result
                    
                    print(f"任务完成: {task.task_type}")
                    print(f"执行结果: {json.dumps(results[task.task_type], ensure_ascii=False, indent=2)}")
                else:
                    print(f"未找到对应的Agent: {task.task_type}")
            
            # 4. 生成最终结果
            final_result = self._generate_final_result(results)
            print(f"\n=== 最终结果 ===")
            print(json.dumps(final_result, ensure_ascii=False, indent=2))
            
            return final_result
            
        except Exception as e:
            print(f"\n=== 处理出错 ===")
            print(f"错误信息: {str(e)}")
            raise e
    
    def _analyze_instruction(self, text: str) -> Dict[str, Any]:
        """分析指令
        
        Args:
            text: 自然语言指令
            
        Returns:
            Dict: 分析结果
        """
        # 使用BERT提取特征
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1)
        
        # 基于特征和规则确定任务类型
        extracted_info = self._extract_info_from_text(text)
        
        # 确定任务类型
        task_type = "order"
        if "生产" in text or "制造" in text:
            task_type = "planning"
        elif "采购" in text or "供应" in text:
            task_type = "supply_chain"
        elif "预算" in text or "财务" in text:
            task_type = "finance"
        elif "预测" in text or "分析" in text:
            task_type = "prediction"
            
        # 确定优先级
        priority = "high" if extracted_info.get("quantity", 0) > 100 else "normal"
        
        # 确定子任务
        sub_tasks = ["order"]
        if task_type != "order":
            sub_tasks.append(task_type)
            
        # 确定依赖关系
        dependencies = {
            "planning": ["order"],
            "supply_chain": ["planning"],
            "prediction": ["order"],
            "finance": ["order", "planning", "supply_chain"]
        }
        
        analysis = {
            "main_task": task_type,
            "sub_tasks": sub_tasks,
            "priority": priority,
            "deadline": extracted_info.get("delivery_date"),
            "constraints": [],
            "dependencies": dependencies,
            "extracted_info": extracted_info
        }
        
        return analysis
    
    def _extract_info_from_text(self, text: str) -> Dict[str, Any]:
        """从文本中提取关键信息
        
        Args:
            text: 自然语言文本
            
        Returns:
            Dict: 提取的信息
        """
        info = {
            "quantity": 0,
            "cpu": None,
            "memory": None,
            "storage": None,
            "gpu": None,
            "delivery_date": None,
            "delivery_address": None
        }
        
        # 提取数量
        quantity_match = re.search(r'(\d+)\s*台', text)
        if quantity_match:
            info["quantity"] = int(quantity_match.group(1))
            
        # 提取CPU信息
        if "i9" in text.lower():
            info["cpu"] = "Intel i9"
            
        # 提取内存信息
        memory_match = re.search(r'(\d+)GB', text)
        if memory_match:
            info["memory"] = f"{memory_match.group(1)}GB"
            
        # 提取存储信息
        storage_match = re.search(r'(\d+)TB', text)
        if storage_match:
            info["storage"] = f"{storage_match.group(1)}TB"
            
        # 提取显卡信息
        if "rtx" in text.lower():
            gpu_match = re.search(r'RTX\s*(\d+)', text, re.IGNORECASE)
            if gpu_match:
                info["gpu"] = f"NVIDIA RTX {gpu_match.group(1)}"
                
        # 提取交货日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        if date_match:
            info["delivery_date"] = date_match.group(1)
            
        # 提取地址
        address_match = re.search(r'地址是(.*?)[。\n]', text)
        if address_match:
            info["delivery_address"] = address_match.group(1).strip()
            
        return info
    
    def _generate_task_sequence(self, analysis: Dict[str, Any], parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """生成任务序列
        
        Args:
            analysis: 指令分析结果
            parameters: 额外参数
            
        Returns:
            List[Dict[str, Any]]: 任务序列
        """
        task_sequence = []
        
        # 1. 订单处理任务
        task_sequence.append({
            "type": "order",
            "parameters": {
                "task_type": "order_processing",
                "product_info": analysis["extracted_info"],
                "priority": analysis["priority"]
            }
        })
        
        # 2. 生产计划任务
        task_sequence.append({
            "type": "planning",
            "parameters": {
                "task_type": "production_planning",
                "product_info": analysis["extracted_info"],
                "deadline": analysis["deadline"]
            }
        })
        
        # 3. 供应链任务
        task_sequence.append({
            "type": "supply_chain",
            "parameters": {
                "task_type": "supply_chain_planning",
                "plan_details": {
                    "mps": {
                        "total_quantity": analysis["extracted_info"]["quantity"],
                        "deadline": analysis["deadline"]
                    }
                }
            }
        })
        
        # 4. 预测任务
        task_sequence.append({
            "type": "prediction",
            "parameters": {
                "task_type": "demand_prediction",
                "product_info": analysis["extracted_info"]
            }
        })
        
        # 5. 财务任务
        task_sequence.append({
            "type": "finance",
            "parameters": {
                "operation_type": "budget",
                "材料_amount": analysis["extracted_info"]["quantity"] * 5000,  # 假设每台电脑材料成本5000
                "人工_amount": analysis["extracted_info"]["quantity"] * 1000,  # 假设每台电脑人工成本1000
                "设备_amount": 100000,  # 固定设备成本
                "其他_amount": analysis["extracted_info"]["quantity"] * 500   # 其他成本
            }
        })
        
        return task_sequence
    
    def _generate_final_result(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终结果
        
        Args:
            results: 各个任务的结果
            
        Returns:
            Dict: 最终结果
        """
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "results": results
        } 