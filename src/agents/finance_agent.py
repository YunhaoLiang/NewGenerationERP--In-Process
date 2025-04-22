from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentResponse

class FinanceAgent(BaseAgent):
    """财务Agent"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化FinanceAgent
        
        Args:
            agent_id: Agent唯一标识，如果不提供则自动生成
            agent_type: Agent类型，如果不提供则使用类名的小写形式
        """
        super().__init__(agent_id, agent_type)
        self.budget_categories = ["材料", "人工", "设备", "其他"]
        self.payment_statuses = ["待支付", "已支付", "已取消"]
        self.invoice_statuses = ["待开票", "已开票", "已作废"]
        
    async def _process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理财务任务
        
        Args:
            parameters: 任务参数，包含财务操作类型和相关信息
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.status = "processing"
            print(f"FinanceAgent {self.agent_id} 开始处理财务任务...")
            
            # 验证输入参数
            if "operation_type" not in parameters:
                return AgentResponse(
                    status="error",
                    error="缺少操作类型参数"
                )
                
            operation_type = parameters["operation_type"]
            
            # 根据操作类型选择相应的处理方法
            if operation_type == "budget":
                result = self._handle_budget(parameters)
            elif operation_type == "payment":
                result = self._handle_payment(parameters)
            elif operation_type == "invoice":
                result = self._handle_invoice(parameters)
            elif operation_type == "report":
                result = self._generate_report(parameters)
            else:
                return AgentResponse(
                    status="error",
                    error=f"不支持的操作类型: {operation_type}"
                )
            
            self.status = "completed"
            print(f"FinanceAgent {self.agent_id} 财务任务处理完成")
            
            return AgentResponse(
                status="success",
                data=result
            )
            
        except Exception as e:
            self.status = "error"
            print(f"FinanceAgent {self.agent_id} 处理财务任务时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练FinanceAgent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        try:
            self.status = "training"
            print(f"FinanceAgent {self.agent_id} 开始训练...")
            
            # 这里可以添加实际的训练逻辑
            # 目前只是模拟训练过程
            
            self.status = "idle"
            print(f"FinanceAgent {self.agent_id} 训练完成")
            
            return AgentResponse(
                status="success",
                data={"message": "训练完成"}
            )
            
        except Exception as e:
            self.status = "error"
            print(f"FinanceAgent {self.agent_id} 训练时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    def _handle_budget(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """处理预算相关操作
        
        Args:
            parameters: 预算参数
            
        Returns:
            Dict[str, Any]: 预算处理结果
        """
        budget_id = f"BGT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        budget_items = []
        total_amount = 0.0
        
        for category in self.budget_categories:
            amount = parameters.get(f"{category}_amount", 0.0)
            budget_items.append({
                "category": category,
                "amount": float(amount),
                "description": parameters.get(f"{category}_description", "")
            })
            total_amount += amount
            
        return {
            "budget_id": budget_id,
            "total_amount": float(total_amount),
            "items": budget_items,
            "status": "created",
            "created_at": datetime.now().isoformat()
        }
        
    def _handle_payment(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """处理支付相关操作
        
        Args:
            parameters: 支付参数
            
        Returns:
            Dict[str, Any]: 支付处理结果
        """
        payment_id = f"PAY_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        amount = float(parameters.get("amount", 0.0))
        status = parameters.get("status", "待支付")
        
        if status not in self.payment_statuses:
            status = "待支付"
            
        return {
            "payment_id": payment_id,
            "amount": amount,
            "status": status,
            "payee": parameters.get("payee", ""),
            "payment_date": parameters.get("payment_date", datetime.now().isoformat()),
            "description": parameters.get("description", "")
        }
        
    def _handle_invoice(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """处理发票相关操作
        
        Args:
            parameters: 发票参数
            
        Returns:
            Dict[str, Any]: 发票处理结果
        """
        invoice_id = f"INV_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        amount = float(parameters.get("amount", 0.0))
        status = parameters.get("status", "待开票")
        
        if status not in self.invoice_statuses:
            status = "待开票"
            
        return {
            "invoice_id": invoice_id,
            "amount": amount,
            "status": status,
            "customer": parameters.get("customer", ""),
            "issue_date": parameters.get("issue_date", datetime.now().isoformat()),
            "description": parameters.get("description", "")
        }
        
    def _generate_report(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """生成财务报告
        
        Args:
            parameters: 报告参数
            
        Returns:
            Dict[str, Any]: 报告内容
        """
        report_id = f"RPT_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        report_type = parameters.get("report_type", "summary")
        start_date = parameters.get("start_date", (datetime.now() - timedelta(days=30)).isoformat())
        end_date = parameters.get("end_date", datetime.now().isoformat())
        
        # 这里可以添加实际的报告生成逻辑
        # 目前只是返回一个示例报告
        
        return {
            "report_id": report_id,
            "report_type": report_type,
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "summary": {
                "total_income": 100000.0,
                "total_expense": 80000.0,
                "net_profit": 20000.0
            },
            "details": {
                "income": [
                    {"category": "销售", "amount": 80000.0},
                    {"category": "服务", "amount": 20000.0}
                ],
                "expense": [
                    {"category": "材料", "amount": 40000.0},
                    {"category": "人工", "amount": 30000.0},
                    {"category": "其他", "amount": 10000.0}
                ]
            }
        } 