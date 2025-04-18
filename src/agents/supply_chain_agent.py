from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent, AgentResponse
from datetime import datetime, timedelta

class SupplyChainAgent(BaseAgent):
    """供应链Agent"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化SupplyChainAgent
        
        Args:
            agent_id: Agent唯一标识，如果不提供则自动生成
            agent_type: Agent类型，如果不提供则使用类名的小写形式
        """
        super().__init__(agent_id, agent_type)
        self.safety_stock_factor = 1.2  # 安全库存系数
        self.lead_time_factor = 1.5  # 提前期系数
        
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理供应链任务
        
        Args:
            parameters: 任务参数，包含生产计划信息
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.status = "processing"
            print(f"SupplyChainAgent {self.agent_id} 开始处理供应链任务...")
            
            # 验证输入参数
            if "plan_details" not in parameters:
                return AgentResponse(
                    status="error",
                    error="缺少计划详情参数"
                )
                
            plan_details = parameters["plan_details"]
            
            # 创建采购计划
            procurement_plan = self._create_procurement_plan(plan_details)
            
            # 创建库存计划
            inventory_plan = self._create_inventory_plan(procurement_plan)
            
            # 创建物流计划
            logistics_plan = self._create_logistics_plan(procurement_plan)
            
            # 构建供应链详情
            supply_chain_details = {
                "procurement": procurement_plan,
                "inventory": inventory_plan,
                "logistics": logistics_plan,
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
            self.status = "completed"
            print(f"SupplyChainAgent {self.agent_id} 供应链任务处理完成")
            
            return AgentResponse(
                status="success",
                data=supply_chain_details
            )
            
        except Exception as e:
            self.status = "error"
            print(f"SupplyChainAgent {self.agent_id} 处理供应链任务时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练SupplyChainAgent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        try:
            self.status = "training"
            print(f"SupplyChainAgent {self.agent_id} 开始训练...")
            
            # 这里可以添加实际的训练逻辑
            # 目前只是模拟训练过程
            
            self.status = "idle"
            print(f"SupplyChainAgent {self.agent_id} 训练完成")
            
            return AgentResponse(
                status="success",
                data={"message": "训练完成"}
            )
            
        except Exception as e:
            self.status = "error"
            print(f"SupplyChainAgent {self.agent_id} 训练时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    def _create_procurement_plan(self, plan_details: Dict[str, Any]) -> Dict[str, Any]:
        """创建采购计划
        
        Args:
            plan_details: 计划详情
            
        Returns:
            Dict[str, Any]: 采购计划
        """
        mps = plan_details["mps"]
        total_quantity = mps["total_quantity"]
        
        # 计算采购周期
        procurement_cycle = self._calculate_procurement_cycle(total_quantity)
        
        # 计算采购数量
        procurement_quantity = self._calculate_procurement_quantity(total_quantity)
        
        return {
            "total_quantity": total_quantity,
            "procurement_cycle": procurement_cycle,
            "procurement_quantity": procurement_quantity,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=procurement_cycle)).isoformat()
        }
        
    def _create_inventory_plan(self, procurement_plan: Dict[str, Any]) -> Dict[str, Any]:
        """创建库存计划
        
        Args:
            procurement_plan: 采购计划
            
        Returns:
            Dict[str, Any]: 库存计划
        """
        # 计算安全库存
        safety_stock = self._calculate_safety_stock(procurement_plan["procurement_quantity"])
        
        # 计算再订货点
        reorder_point = self._calculate_reorder_point(procurement_plan["procurement_quantity"], safety_stock)
        
        return {
            "safety_stock": safety_stock,
            "reorder_point": reorder_point,
            "current_stock": 0,  # 实际应用中应该从数据库获取
            "status": "planned"
        }
        
    def _create_logistics_plan(self, procurement_plan: Dict[str, Any]) -> Dict[str, Any]:
        """创建物流计划
        
        Args:
            procurement_plan: 采购计划
            
        Returns:
            Dict[str, Any]: 物流计划
        """
        # 计算运输方式
        transport_mode = self._determine_transport_mode(procurement_plan["procurement_quantity"])
        
        # 计算运输时间
        transport_time = self._calculate_transport_time(transport_mode)
        
        return {
            "transport_mode": transport_mode,
            "transport_time": transport_time,
            "start_date": procurement_plan["start_date"],
            "end_date": (datetime.fromisoformat(procurement_plan["start_date"]) + 
                        timedelta(days=transport_time)).isoformat(),
            "status": "planned"
        }
        
    def _calculate_procurement_cycle(self, total_quantity: int) -> int:
        """计算采购周期
        
        Args:
            total_quantity: 总数量
            
        Returns:
            int: 采购周期（天数）
        """
        return int(total_quantity * 0.1)  # 简单计算：采购周期为总量的10%
        
    def _calculate_procurement_quantity(self, total_quantity: int) -> int:
        """计算采购数量
        
        Args:
            total_quantity: 总数量
            
        Returns:
            int: 采购数量
        """
        return int(total_quantity * self.safety_stock_factor)
        
    def _calculate_safety_stock(self, procurement_quantity: int) -> int:
        """计算安全库存
        
        Args:
            procurement_quantity: 采购数量
            
        Returns:
            int: 安全库存
        """
        return int(procurement_quantity * 0.2)  # 安全库存为采购数量的20%
        
    def _calculate_reorder_point(self, procurement_quantity: int, safety_stock: int) -> int:
        """计算再订货点
        
        Args:
            procurement_quantity: 采购数量
            safety_stock: 安全库存
            
        Returns:
            int: 再订货点
        """
        return int(procurement_quantity * 0.3 + safety_stock)  # 再订货点为采购数量的30%加上安全库存
        
    def _determine_transport_mode(self, quantity: int) -> str:
        """确定运输方式
        
        Args:
            quantity: 数量
            
        Returns:
            str: 运输方式
        """
        if quantity > 1000:
            return "海运"
        elif quantity > 100:
            return "陆运"
        else:
            return "空运"
            
    def _calculate_transport_time(self, transport_mode: str) -> int:
        """计算运输时间
        
        Args:
            transport_mode: 运输方式
            
        Returns:
            int: 运输时间（天数）
        """
        if transport_mode == "海运":
            return 30
        elif transport_mode == "陆运":
            return 7
        else:
            return 3 