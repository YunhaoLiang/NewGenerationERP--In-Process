from typing import Dict, Any
from datetime import datetime
import uuid

class AgentResponse:
    """Agent响应类"""
    def __init__(self, status: str, data: Dict[str, Any] = None, message: str = None):
        self.status = status
        self.data = data or {}
        self.message = message
        self.timestamp = datetime.now().isoformat()
        
    def dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "status": self.status,
            "data": self.data,
            "message": self.message,
            "timestamp": self.timestamp
        }

class BaseAgent:
    """Agent基类"""
    
    def __init__(self):
        """初始化Agent"""
        self.agent_id = str(uuid.uuid4())
        self.agent_type = self.__class__.__name__.lower().replace("agent", "")
        self.status = "idle"
        self.last_activity = datetime.now()
        self.error_count = 0
        
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理任务
        
        Args:
            parameters: 任务参数
            
        Returns:
            AgentResponse: 处理结果
        """
        try:
            self.status = "processing"
            self.last_activity = datetime.now()
            
            # 调用具体的处理逻辑
            result = await self._process(parameters)
            
            self.status = "idle"
            self.error_count = 0
            return result
            
        except Exception as e:
            self.status = "error"
            self.error_count += 1
            return AgentResponse(
                status="error",
                message=str(e)
            )
            
    async def _process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """具体的处理逻辑，由子类实现
        
        Args:
            parameters: 任务参数
            
        Returns:
            AgentResponse: 处理结果
        """
        raise NotImplementedError("子类必须实现_process方法")
        
    def get_status(self) -> Dict[str, Any]:
        """获取Agent状态
        
        Returns:
            Dict: Agent状态
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "last_activity": self.last_activity.isoformat(),
            "error_count": self.error_count
        }
        
    def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练Agent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        return AgentResponse(
            status="success",
            message="训练功能待实现"
        ) 