from typing import Dict, List, Optional
from pydantic import BaseModel
from transformers import pipeline
import torch
import re

class Task(BaseModel):
    """表示一个业务任务"""
    task_id: str
    task_type: str
    parameters: Dict
    status: str = "pending"
    result: Optional[Dict] = None

class LLMOrchestrator:
    def __init__(self):
        """初始化LLM编排器"""
        self.nlp = pipeline("text-classification", model="bert-base-chinese")
        self.tasks: Dict[str, Task] = {}
        
    async def process_instruction(self, instruction: str, parameters: Dict = None) -> Task:
        """处理业务指令
        
        Args:
            instruction: 自然语言形式的业务指令
            parameters: 额外的参数
            
        Returns:
            Task: 解析后的任务对象
        """
        # 使用NLP模型分析指令
        analysis = self.nlp(instruction)
        
        # 提取参数
        extracted_params = self._extract_parameters(instruction)
        
        # 如果有额外的参数，合并它们
        if parameters:
            extracted_params.update(parameters)
        
        # 确定任务类型
        task_type = self._determine_task_type(instruction)
        
        # 创建任务
        task = Task(
            task_id=f"task_{len(self.tasks)}",
            task_type=task_type,
            parameters=extracted_params
        )
        
        self.tasks[task.task_id] = task
        return task
    
    def _determine_task_type(self, instruction: str) -> str:
        """确定任务类型"""
        # 简单的关键词匹配
        print("\n=== 任务类型识别 ===")
        # 订单相关关键词
        if any(keyword in instruction for keyword in ["订购", "下单", "购买", "订单"]):
            print("识别为: 订单任务")
            return "order"
        # 生产相关关键词
        elif any(keyword in instruction for keyword in ["生产", "制造", "加工"]):
            print("识别为: 生产任务")
            return "production"
        # 采购相关关键词
        elif any(keyword in instruction for keyword in ["采购", "进货", "购入"]):
            print("识别为: 采购任务")
            return "procurement"
        else:
            print("识别为: 默认任务")
            return "default"
    
    def _extract_parameters(self, instruction: str) -> Dict:
        """提取任务参数"""
        print("\n=== 参数提取 ===")
        params = {
            "instruction": instruction,
            "timestamp": "2024-04-01T12:00:00Z"
        }
        
        # 提取客户ID
        customer_id_match = re.search(r'客户编号(CUS_\d{8})', instruction)
        if customer_id_match:
            params["customer_id"] = customer_id_match.group(1)
            print(f"提取客户ID: {params['customer_id']}")
        
        # 提取产品信息
        products = []
        # 匹配数量和产品名称
        product_matches = re.finditer(r'(\d+)台([\w\s]+?)(?=和|。|，|$)', instruction)
        for match in product_matches:
            quantity = int(match.group(1))
            product_name = match.group(2).strip()
            product = {
                "name": product_name,
                "quantity": quantity
            }
            products.append(product)
            print(f"提取产品: {quantity}台 {product_name}")
        
        if products:
            params["products"] = products
            
        # 提取日期
        date_match = re.search(r'(\d+)月(\d+)日', instruction)
        if date_match:
            month, day = date_match.groups()
            params["delivery_date"] = f"2024-{int(month):02d}-{int(day):02d}"
            print(f"提取日期: {params['delivery_date']}")
            
        # 提取地址
        address_match = re.search(r'送到(.*?)(?=。|$)', instruction)
        if address_match:
            params["shipping_address"] = address_match.group(1).strip()
            print(f"提取地址: {params['shipping_address']}")
            
        # 提取优先级
        if "VIP" in instruction.upper() or "优先" in instruction:
            params["priority"] = "high"
            print("提取优先级: high")
        else:
            params["priority"] = "normal"
            print("提取优先级: normal")
            
        # 提取特殊要求
        requirements_match = re.search(r'需要(.*?)(?=。|$)', instruction)
        if requirements_match:
            params["special_requirements"] = requirements_match.group(1).strip()
            print(f"提取特殊要求: {params['special_requirements']}")
            
        return params
    
    async def execute_task(self, task_id: str) -> Dict:
        """执行任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            Dict: 执行结果
        """
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
            
        # TODO: 实现任务执行逻辑
        task.status = "completed"
        task.result = {"status": "success"}
        return task.result 