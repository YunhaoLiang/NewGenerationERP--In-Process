from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentResponse

class PlanningAgent(BaseAgent):
    """生产计划Agent"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化PlanningAgent
        
        Args:
            agent_id: Agent唯一标识，如果不提供则自动生成
            agent_type: Agent类型，如果不提供则使用类名的小写形式
        """
        super().__init__(agent_id, agent_type)
        self.production_capacity = 100  # 每日产能
        self.working_days = 5  # 每周工作日
        
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理生产计划任务
        
        Args:
            parameters: 任务参数，包含产品信息
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.status = "processing"
            print(f"PlanningAgent {self.agent_id} 开始处理生产计划...")
            
            # 验证输入参数
            if "product_info" not in parameters:
                return AgentResponse(
                    status="error",
                    error="缺少产品信息参数"
                )
                
            product_info = parameters["product_info"]
            deadline = parameters.get("deadline")
            
            # 创建主生产计划
            mps = self._create_master_production_schedule(product_info, deadline)
            
            # 创建作业计划
            jss = self._create_job_schedule(mps)
            
            # 构建计划详情
            plan_details = {
                "plan_id": f"PLN_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "product_info": product_info,
                "mps": mps,
                "jss": jss,
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
            self.status = "completed"
            print(f"PlanningAgent {self.agent_id} 生产计划处理完成")
            
            return AgentResponse(
                status="success",
                data=plan_details
            )
            
        except Exception as e:
            self.status = "error"
            print(f"PlanningAgent {self.agent_id} 处理生产计划时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练PlanningAgent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        try:
            self.status = "training"
            print(f"PlanningAgent {self.agent_id} 开始训练...")
            
            # 这里可以添加实际的训练逻辑
            # 目前只是模拟训练过程
            
            self.status = "idle"
            print(f"PlanningAgent {self.agent_id} 训练完成")
            
            return AgentResponse(
                status="success",
                data={"message": "训练完成"}
            )
            
        except Exception as e:
            self.status = "error"
            print(f"PlanningAgent {self.agent_id} 训练时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    def _create_master_production_schedule(self, product_info: Dict[str, Any], deadline: str = None) -> Dict[str, Any]:
        """创建主生产计划
        
        Args:
            product_info: 产品信息
            deadline: 截止日期
            
        Returns:
            Dict[str, Any]: 主生产计划
        """
        total_quantity = product_info["quantity"]
        
        # 计算生产周期
        production_cycles = self._calculate_production_cycles(total_quantity)
        
        # 计算每日产能
        daily_capacity = self._calculate_daily_capacity(total_quantity, production_cycles)
        
        # 确定开始和结束日期
        start_date = datetime.now()
        if deadline:
            end_date = datetime.fromisoformat(deadline)
            # 调整生产周期以满足截止日期
            available_days = (end_date - start_date).days
            if available_days < production_cycles:
                # 如果可用天数不足，增加每日产能
                daily_capacity = (total_quantity + available_days - 1) // available_days
                production_cycles = available_days
        else:
            end_date = start_date + timedelta(days=production_cycles)
        
        return {
            "total_quantity": total_quantity,
            "production_cycles": production_cycles,
            "daily_capacity": daily_capacity,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "specifications": {
                "cpu": product_info.get("cpu", ""),
                "memory": product_info.get("memory", ""),
                "storage": product_info.get("storage", ""),
                "gpu": product_info.get("gpu", "")
            }
        }
        
    def _create_job_schedule(self, mps: Dict[str, Any]) -> List[Dict[str, Any]]:
        """创建作业计划
        
        Args:
            mps: 主生产计划
            
        Returns:
            List[Dict[str, Any]]: 作业计划列表
        """
        job_schedule = []
        start_date = datetime.fromisoformat(mps["start_date"])
        
        for day in range(mps["production_cycles"]):
            current_date = start_date + timedelta(days=day)
            # 跳过周末
            while current_date.weekday() >= self.working_days:
                current_date += timedelta(days=1)
                
            job_schedule.append({
                "job_id": f"JOB_{current_date.strftime('%Y%m%d')}_{day + 1}",
                "day": day + 1,
                "date": current_date.isoformat(),
                "planned_quantity": mps["daily_capacity"],
                "specifications": mps["specifications"],
                "status": "planned"
            })
            
        return job_schedule
        
    def _calculate_production_cycles(self, total_quantity: int) -> int:
        """计算生产周期
        
        Args:
            total_quantity: 总数量
            
        Returns:
            int: 生产周期（天数）
        """
        base_cycles = (total_quantity + self.production_capacity - 1) // self.production_capacity
        # 考虑周末，增加所需的额外天数
        extra_days = (base_cycles // self.working_days) * 2
        return base_cycles + extra_days
        
    def _calculate_daily_capacity(self, total_quantity: int, production_cycles: int) -> int:
        """计算每日产能
        
        Args:
            total_quantity: 总数量
            production_cycles: 生产周期
            
        Returns:
            int: 每日产能
        """
        return min(
            (total_quantity + production_cycles - 1) // production_cycles,
            self.production_capacity
        ) 