from typing import Dict, Any, Optional, List
from transformers import pipeline
from .base_agent import BaseAgent, AgentResponse
import re
from datetime import datetime
from src.config.database import SessionLocal
from src.models.models import Order, Product, User, Inventory
from sqlalchemy.orm import Session

class OrderAgent(BaseAgent):
    """订单处理代理"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化订单代理"""
        super().__init__(agent_id=agent_id, agent_type=agent_type)
        print("初始化OrderAgent...")
        self.db = None
    
    def __del__(self):
        """清理资源"""
        if self.db is not None:
            try:
                print("关闭OrderAgent数据库连接...")
                self.db.close()
            except Exception as e:
                print(f"关闭数据库连接时出错：{str(e)}")
    
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理订单请求
        
        Args:
            parameters: 包含订单信息的参数字典
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.db = SessionLocal()
            result = await self.process_order(parameters)
            return AgentResponse(
                status="success" if result["success"] else "error",
                data=result["data"] if result["success"] else None,
                error=result["message"] if not result["success"] else None
            )
        except Exception as e:
            return AgentResponse(
                status="error",
                error=str(e)
            )
        finally:
            if self.db is not None:
                self.db.close()
                self.db = None
    
    async def process_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理订单
        :param order_data: 订单数据，包含：用户ID，产品ID，数量
        :return: 处理结果
        """
        try:
            print(f"\n开始处理订单：{order_data}")
            
            # 检查用户是否存在
            user = self.db.query(User).filter(User.用户ID == order_data['用户ID']).first()
            if not user:
                print("用户不存在")
                return {"success": False, "message": "用户不存在"}
            print(f"找到用户：{user.用户名}")
            
            # 检查产品是否存在
            product = self.db.query(Product).filter(Product.产品ID == order_data['产品ID']).first()
            if not product:
                print("产品不存在")
                return {"success": False, "message": "产品不存在"}
            print(f"找到产品：{product.产品名称}")
            
            # 检查库存
            inventory = self.db.query(Inventory).filter(Inventory.产品ID == order_data['产品ID']).first()
            if not inventory or inventory.数量 < order_data.get('数量', 1):
                print(f"库存不足，当前库存：{inventory.数量 if inventory else 0}")
                return {"success": False, "message": "库存不足"}
            print(f"当前库存：{inventory.数量}")
            
            # 计算订单金额
            quantity = order_data.get('数量', 1)
            total_amount = product.单价 * quantity
            print(f"订单金额：{float(total_amount)}")
            
            # 创建订单
            new_order = Order(
                用户ID=order_data['用户ID'],
                产品ID=order_data['产品ID'],
                数量=quantity,
                总金额=total_amount,
                订单状态='已创建',
                下单时间=datetime.now()
            )
            
            # 更新库存
            inventory.数量 -= quantity
            print(f"更新后库存：{inventory.数量}")
            
            # 保存到数据库
            self.db.add(new_order)
            self.db.commit()
            print("订单创建成功")
            
            return {
                "success": True,
                "message": "订单创建成功",
                "data": {
                    "订单ID": new_order.订单ID,
                    "用户名": user.用户名,
                    "产品名称": product.产品名称,
                    "数量": quantity,
                    "总金额": float(total_amount),
                    "订单状态": new_order.订单状态
                }
            }
            
        except Exception as e:
            print(f"订单处理失败：{str(e)}")
            self.db.rollback()
            return {"success": False, "message": f"订单处理失败: {str(e)}"}
            
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

    async def get_order_status(self, order_id: int) -> Dict[str, Any]:
        """
        获取订单状态
        :param order_id: 订单ID
        :return: 订单状态信息
        """
        try:
            print(f"\n查询订单状态：{order_id}")
            order = self.db.query(Order)\
                .join(User)\
                .join(Product)\
                .filter(Order.订单ID == order_id)\
                .first()
                
            if not order:
                print("订单不存在")
                return {"success": False, "message": "订单不存在"}
            
            print(f"找到订单：{order.订单ID}")    
            return {
                "success": True,
                "data": {
                    "订单ID": order.订单ID,
                    "用户名": order.user.用户名,
                    "产品名称": order.product.产品名称,
                    "总金额": float(order.总金额),
                    "订单状态": order.订单状态,
                    "下单时间": order.下单时间.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
            
        except Exception as e:
            print(f"查询订单状态失败：{str(e)}")
            return {"success": False, "message": f"获取订单状态失败: {str(e)}"} 