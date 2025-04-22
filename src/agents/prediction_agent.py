from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from .base_agent import BaseAgent, AgentResponse

class PredictionAgent(BaseAgent):
    """预测Agent"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化PredictionAgent
        
        Args:
            agent_id: Agent唯一标识，如果不提供则自动生成
            agent_type: Agent类型，如果不提供则使用类名的小写形式
        """
        super().__init__(agent_id, agent_type)
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.prediction_horizon = 30  # 预测时间范围（天）
        
        # 添加基本的训练数据
        self._initialize_model()
        
    def _initialize_model(self):
        # 生成示例训练数据
        np.random.seed(42)
        X = np.random.rand(100, 5)  # 5个特征：月份、季节、历史销量、价格、库存
        y = 2 * X[:, 0] + 3 * X[:, 1] - 1.5 * X[:, 2] + X[:, 3] - 0.5 * X[:, 4] + np.random.normal(0, 0.1, 100)
        
        # 标准化数据
        X_scaled = self.scaler.fit_transform(X)
        
        # 训练模型
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
    async def _process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理预测任务
        
        Args:
            parameters: 任务参数，包含产品信息
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.status = "processing"
            print(f"PredictionAgent {self.agent_id} 开始处理预测任务...")
            
            # 验证输入参数
            if "product_info" not in parameters:
                return AgentResponse(
                    status="error",
                    error="缺少产品信息参数"
                )
                
            product_info = parameters["product_info"]
            task_type = parameters.get("task_type", "demand_prediction")
            
            # 根据任务类型选择预测方法
            if task_type == "demand_prediction":
                result = self._predict_demand(product_info)
            elif task_type == "price_prediction":
                result = self._predict_price(product_info)
            elif task_type == "inventory_prediction":
                result = self._predict_inventory(product_info)
            else:
                return AgentResponse(
                    status="error",
                    error=f"不支持的预测类型: {task_type}"
                )
            
            # 构建预测结果
            prediction_details = {
                "prediction_id": f"PRD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "task_type": task_type,
                "product_info": {
                    "quantity": product_info["quantity"],
                    "specifications": {
                        "cpu": product_info.get("cpu", ""),
                        "memory": product_info.get("memory", ""),
                        "storage": product_info.get("storage", ""),
                        "gpu": product_info.get("gpu", "")
                    }
                },
                "predictions": result,
                "status": "completed",
                "created_at": datetime.now().isoformat()
            }
            
            self.status = "completed"
            print(f"PredictionAgent {self.agent_id} 预测任务处理完成")
            
            return AgentResponse(
                status="success",
                data=prediction_details
            )
            
        except Exception as e:
            self.status = "error"
            print(f"PredictionAgent {self.agent_id} 处理预测任务时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练PredictionAgent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        try:
            self.status = "training"
            print(f"PredictionAgent {self.agent_id} 开始训练...")
            
            # 这里可以添加实际的训练逻辑
            # 目前只是模拟训练过程
            
            self.status = "idle"
            print(f"PredictionAgent {self.agent_id} 训练完成")
            
            return AgentResponse(
                status="success",
                data={"message": "训练完成"}
            )
            
        except Exception as e:
            self.status = "error"
            print(f"PredictionAgent {self.agent_id} 训练时出错: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e)
            )
            
    def _predict_demand(self, product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """预测需求
        
        Args:
            product_info: 产品信息
            
        Returns:
            List[Dict[str, Any]]: 预测结果列表
        """
        # 生成未来30天的预测数据
        predictions = []
        base_demand = product_info["quantity"]
        
        for i in range(30):
            date = datetime.now() + timedelta(days=i)
            # 简单的需求预测逻辑
            if date.weekday() < 5:  # 工作日
                predicted_demand = int(base_demand * (1 + 0.1 * (i % 5 - 2)))  # 波动范围：-20% 到 +20%
            else:  # 周末
                predicted_demand = int(base_demand * 0.7)  # 周末需求降低30%
                
            predictions.append({
                "date": date.isoformat(),
                "predicted_demand": predicted_demand,
                "confidence": 0.8 - 0.01 * i  # 随时间推移，置信度降低
            })
            
        return predictions
        
    def _predict_price(self, product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """预测价格
        
        Args:
            product_info: 产品信息
            
        Returns:
            List[Dict[str, Any]]: 预测结果列表
        """
        # 基础价格计算
        base_price = 5000.0  # 基础价格
        if product_info.get("cpu", "").lower().find("i9") != -1:
            base_price += 1000.0
        if product_info.get("memory", "").startswith("32"):
            base_price += 500.0
        if product_info.get("storage", "").startswith("1"):
            base_price += 300.0
        if product_info.get("gpu", "").lower().find("rtx") != -1:
            base_price += 2000.0
            
        # 生成未来30天的价格预测
        predictions = []
        for i in range(30):
            date = datetime.now() + timedelta(days=i)
            # 简单的价格预测逻辑
            predicted_price = base_price * (1 + 0.05 * (i % 3 - 1))  # 波动范围：-5% 到 +5%
            
            predictions.append({
                "date": date.isoformat(),
                "predicted_price": round(predicted_price, 2),
                "confidence": 0.9 - 0.01 * i  # 随时间推移，置信度降低
            })
            
        return predictions
        
    def _predict_inventory(self, product_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """预测库存
        
        Args:
            product_info: 产品信息
            
        Returns:
            List[Dict[str, Any]]: 预测结果列表
        """
        # 初始库存设置
        initial_inventory = product_info["quantity"] // 2  # 假设初始库存为订单量的一半
        daily_production = product_info["quantity"] // 30  # 假设30天内平均生产
        
        # 生成未来30天的库存预测
        predictions = []
        current_inventory = initial_inventory
        
        for i in range(30):
            date = datetime.now() + timedelta(days=i)
            # 简单的库存预测逻辑
            if date.weekday() < 5:  # 工作日
                production = daily_production
                consumption = int(daily_production * 0.9)  # 假设90%的产量被消耗
            else:  # 周末
                production = 0
                consumption = int(daily_production * 0.3)  # 周末消耗降低
                
            current_inventory += production - consumption
            
            predictions.append({
                "date": date.isoformat(),
                "predicted_inventory": max(0, current_inventory),
                "production": production,
                "consumption": consumption,
                "confidence": 0.85 - 0.01 * i  # 随时间推移，置信度降低
            })
            
        return predictions
        
    def _prepare_data(self, historical_data: List[Dict[str, Any]]) -> tuple:
        """准备数据
        
        Args:
            historical_data: 历史数据
            
        Returns:
            tuple: (特征矩阵, 目标变量)
        """
        X = []
        y = []
        
        for data in historical_data:
            X.append([data.get("timestamp", 0)])
            y.append(data.get("value", 0))
            
        return np.array(X), np.array(y)
        
    def _generate_future_dates(self) -> np.ndarray:
        """生成未来日期
        
        Returns:
            np.ndarray: 未来日期数组
        """
        current_date = datetime.now()
        future_dates = [
            current_date + timedelta(days=i)
            for i in range(1, self.prediction_horizon + 1)
        ]
        return np.array([[date.timestamp()] for date in future_dates])
        
    def _calculate_confidence(self, predictions: np.ndarray) -> float:
        """计算置信度
        
        Args:
            predictions: 预测值
            
        Returns:
            float: 置信度
        """
        # 简单实现：使用预测值的标准差作为置信度指标
        return 1.0 / (1.0 + np.std(predictions))
        
    def _check_inventory_alerts(self, predictions: np.ndarray) -> List[Dict[str, Any]]:
        """检查库存预警
        
        Args:
            predictions: 预测值
            
        Returns:
            List[Dict[str, Any]]: 预警列表
        """
        alerts = []
        min_threshold = 100  # 最小库存阈值
        max_threshold = 1000  # 最大库存阈值
        
        for i, value in enumerate(predictions):
            if value < min_threshold:
                alerts.append({
                    "type": "low",
                    "date": (datetime.now() + timedelta(days=i+1)).isoformat(),
                    "value": float(value),
                    "threshold": min_threshold
                })
            elif value > max_threshold:
                alerts.append({
                    "type": "high",
                    "date": (datetime.now() + timedelta(days=i+1)).isoformat(),
                    "value": float(value),
                    "threshold": max_threshold
                })
                
        return alerts 