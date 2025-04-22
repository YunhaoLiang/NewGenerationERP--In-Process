from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentResponse
import math
import uuid
import logging

logger = logging.getLogger(__name__)

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
        
    async def _process(self, parameters: Dict[str, Any]) -> AgentResponse:
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
            jss = self._generate_job_scheduling_system(mps)
            
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
            # 如果截止日期早于开始日期，调整为从当前日期开始的合理周期
            if end_date < start_date:
                end_date = start_date + timedelta(days=production_cycles)
            else:
                # 调整生产周期以满足截止日期
                available_days = max(1, (end_date - start_date).days)
                daily_capacity = min(
                    (total_quantity + available_days - 1) // available_days,
                    self.production_capacity
                )
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
        
    def _generate_job_scheduling_system(self, mps_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        根据主生产计划生成作业调度系统
        """
        try:
            total_quantity = mps_data.get("total_quantity", 0)
            start_date = datetime.fromisoformat(mps_data.get("start_date"))
            end_date = datetime.fromisoformat(mps_data.get("end_date"))
            daily_capacity = mps_data.get("daily_capacity", 0)
            
            if total_quantity <= 0 or daily_capacity <= 0:
                return []
                
            # 确保开始日期不晚于结束日期
            if start_date > end_date:
                start_date, end_date = end_date, start_date
                
            # 计算最小所需天数
            min_days_needed = math.ceil(total_quantity / daily_capacity)
            
            # 调整结束日期以确保有足够的生产时间
            date_diff = (end_date - start_date).days
            if date_diff < min_days_needed:
                end_date = start_date + timedelta(days=min_days_needed)
            
            # 生成作业调度
            jss = []
            remaining_quantity = total_quantity
            current_date = start_date
            
            while remaining_quantity > 0 and current_date <= end_date:
                daily_production = min(daily_capacity, remaining_quantity)
                
                job = {
                    "job_id": str(uuid.uuid4()),
                    "date": current_date.isoformat(),
                    "planned_quantity": daily_production,
                    "status": "scheduled",
                    "priority": "normal"
                }
                
                if (end_date - current_date).days < min_days_needed / 2:
                    job["priority"] = "high"  # 临近截止日期时提高优先级
                    
                jss.append(job)
                remaining_quantity -= daily_production
                current_date += timedelta(days=1)
            
            return jss
            
        except Exception as e:
            logger.error(f"生成作业调度系统时出错: {str(e)}")
            return []
        
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