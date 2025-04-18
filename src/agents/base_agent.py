from typing import Dict, Any, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
import uuid

class AgentResponse(BaseModel):
    """Agent响应模型"""
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class BaseAgent(ABC):
    """基础Agent类，所有具体Agent都继承自此类"""
    
    def __init__(self, agent_id: Optional[str] = None, agent_type: Optional[str] = None):
        """初始化Agent
        
        Args:
            agent_id: Agent唯一标识，如果不提供则自动生成
            agent_type: Agent类型，如果不提供则使用类名的小写形式
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.agent_type = agent_type or self.__class__.__name__.lower()
        self.status = "idle"
        
    @abstractmethod
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理任务
        
        Args:
            parameters: 任务参数
            
        Returns:
            AgentResponse: 处理结果
        """
        pass
    
    @abstractmethod
    async def train(self, data: Dict[str, Any]) -> AgentResponse:
        """训练Agent
        
        Args:
            data: 训练数据
            
        Returns:
            AgentResponse: 训练结果
        """
        pass
    
    def get_status(self) -> Dict[str, str]:
        """获取Agent状态
        
        Returns:
            Dict[str, str]: 状态信息
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status
        } 