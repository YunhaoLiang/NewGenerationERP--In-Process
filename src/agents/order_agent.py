from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentResponse
from transformers import pipeline
import re
from datetime import datetime

class OrderAgent(BaseAgent):
    """订单处理Agent"""
    
    def __init__(self, agent_id: str = "order_agent_1"):
        """初始化订单Agent
        
        Args:
            agent_id: Agent唯一标识
        """
        super().__init__(agent_id, "order")
        # 初始化NLP模型用于订单解析
        self.nlp = pipeline("text-classification", model="bert-base-chinese")
        
    def _validate_customer_id(self, customer_id: Optional[str]) -> bool:
        """验证客户ID的有效性
        
        Args:
            customer_id: 客户ID
            
        Returns:
            bool: 是否有效
        """
        print(f"\n=== 验证客户ID ===")
        print(f"收到的客户ID: {customer_id}")
        print(f"客户ID类型: {type(customer_id)}")
        
        if not customer_id:
            print("客户ID为空")
            return False
            
        # 验证客户ID格式（假设格式为：CUS_开头加8位数字）
        if not re.match(r'^CUS_\d{8}$', customer_id):
            print(f"客户ID格式不正确: {customer_id}")
            return False
            
        print("客户ID验证通过")
        return True
        
    async def process(self, task: Dict[str, Any]) -> AgentResponse:
        """处理订单任务
        
        Args:
            task: 订单数据
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            print("\n=== OrderAgent开始处理 ===")
            self.status = "processing"
            print(f"当前状态: {self.status}")
            
            # 验证客户ID
            customer_id = task.get("customer_id")
            if not self._validate_customer_id(customer_id):
                raise ValueError("无效的客户ID，格式应为：CUS_开头加8位数字")
            
            # 构建订单信息
            order_info = {
                "order_id": f"ORD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "customer_id": customer_id,
                "product": {
                    "id": task.get("product_id"),
                    "quantity": task.get("quantity", 0)
                },
                "priority": task.get("priority", "normal"),
                "delivery_date": task.get("delivery_date"),
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
            print("\n=== 订单信息 ===")
            print(f"订单号: {order_info['order_id']}")
            print(f"客户ID: {order_info['customer_id']}")
            print(f"产品ID: {order_info['product']['id']}")
            print(f"数量: {order_info['product']['quantity']}")
            print(f"优先级: {order_info['priority']}")
            print(f"交付日期: {order_info['delivery_date']}")
            print(f"状态: {order_info['status']}")
            print(f"创建时间: {order_info['created_at']}")
            
            # TODO: 记录操作日志
            
            self.status = "idle"
            print(f"\n当前状态: {self.status}")
            
            return AgentResponse(
                status="success",
                data=order_info
            )
            
        except Exception as e:
            self.status = "error"
            print(f"\n=== 处理出错 ===")
            print(f"错误信息: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
    
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练订单Agent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        # TODO: 实现训练逻辑
        return AgentResponse(
            status="success",
            data={"message": "Training completed"}
        )
    
    def _extract_products(self, text: str) -> list:
        """从订单文本中提取产品信息
        
        Args:
            text: 订单文本
            
        Returns:
            list: 产品列表
        """
        # TODO: 实现产品信息提取逻辑
        return []
    
    def _determine_priority(self, analysis: list) -> str:
        """确定订单优先级
        
        Args:
            analysis: NLP分析结果
            
        Returns:
            str: 优先级
        """
        # TODO: 实现优先级判断逻辑
        return "normal" 