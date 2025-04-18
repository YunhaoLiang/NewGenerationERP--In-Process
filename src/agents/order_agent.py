from typing import Dict, Any, Optional, List
from transformers import pipeline
from .base_agent import BaseAgent, AgentResponse
import re
from datetime import datetime

class OrderAgent(BaseAgent):
    """订单处理Agent"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化OrderAgent
        
        Args:
            agent_id: Agent唯一标识，如果不提供则自动生成
            agent_type: Agent类型，如果不提供则使用类名的小写形式
        """
        super().__init__(agent_id, agent_type)
        self.nlp = pipeline("text-classification", model="distilbert-base-uncased")
        
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理订单任务
        
        Args:
            parameters: 任务参数，包含产品信息
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.status = "processing"
            print(f"OrderAgent {self.agent_id} 开始处理订单...")
            
            # 验证输入参数
            if "product_info" not in parameters:
                return AgentResponse(
                    status="error",
                    error="缺少产品信息参数"
                )
                
            product_info = parameters["product_info"]
            task_type = parameters.get("task_type", "order_processing")
            priority = parameters.get("priority", "normal")
            
            # 构建订单详情
            order_details = {
                "order_id": f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "task_type": task_type,
                "customer_info": {
                    "delivery_address": product_info.get("delivery_address", ""),
                    "delivery_date": product_info.get("delivery_date", "")
                },
                "product_info": {
                    "quantity": product_info["quantity"],
                    "specifications": {
                        "cpu": product_info.get("cpu", ""),
                        "memory": product_info.get("memory", ""),
                        "storage": product_info.get("storage", ""),
                        "gpu": product_info.get("gpu", "")
                    }
                },
                "priority": priority,
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
            self.status = "completed"
            print(f"OrderAgent {self.agent_id} 订单处理完成")
            
            return AgentResponse(
                status="success",
                data=order_details
            )
            
        except Exception as e:
            self.status = "error"
            print(f"OrderAgent {self.agent_id} 处理订单时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练OrderAgent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        try:
            self.status = "training"
            print(f"OrderAgent {self.agent_id} 开始训练...")
            
            # 这里可以添加实际的训练逻辑
            # 目前只是模拟训练过程
            
            self.status = "idle"
            print(f"OrderAgent {self.agent_id} 训练完成")
            
            return AgentResponse(
                status="success",
                data={"message": "训练完成"}
            )
            
        except Exception as e:
            self.status = "error"
            print(f"OrderAgent {self.agent_id} 训练时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    def _extract_customer_id(self, text: str) -> str:
        """从文本中提取客户ID
        
        Args:
            text: 订单文本
            
        Returns:
            str: 客户ID
        """
        # 这里使用简单的正则表达式提取客户ID
        # 实际应用中可能需要更复杂的NLP处理
        match = re.search(r"customer[_-]?id:?\s*(\w+)", text, re.IGNORECASE)
        return match.group(1) if match else "unknown"
        
    def _extract_products(self, text: str) -> List[Dict[str, Any]]:
        """从文本中提取产品信息
        
        Args:
            text: 订单文本
            
        Returns:
            List[Dict[str, Any]]: 产品列表
        """
        products = []
        # 这里使用简单的正则表达式提取产品信息
        # 实际应用中可能需要更复杂的NLP处理
        matches = re.finditer(r"(\d+)\s*x\s*([\w\s]+)", text, re.IGNORECASE)
        for match in matches:
            quantity = int(match.group(1))
            name = match.group(2).strip()
            products.append({
                "name": name,
                "quantity": quantity,
                "unit_price": 0.0  # 实际应用中应该从数据库或API获取
            })
        return products
        
    def _determine_priority(self, text: str) -> str:
        """确定订单优先级
        
        Args:
            text: 订单文本
            
        Returns:
            str: 优先级（high/medium/low）
        """
        # 这里使用简单的规则确定优先级
        # 实际应用中可能需要更复杂的NLP处理
        if re.search(r"urgent|asap|immediate", text, re.IGNORECASE):
            return "high"
        elif re.search(r"rush|priority", text, re.IGNORECASE):
            return "medium"
        else:
            return "low" 