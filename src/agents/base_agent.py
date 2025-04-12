from typing import Dict, Any, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod

class AgentResponse(BaseModel):
    """Agent响应模型"""
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class BaseAgent(ABC):
    """基础Agent类，所有具体Agent都继承自此类"""
    
    def __init__(self, agent_id: str, agent_type: str):
        """初始化Agent
        
        Args:
            agent_id: Agent唯一标识
            agent_type: Agent类型
        """
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.status = "idle"
        
    @abstractmethod
    async def process(self, task: Dict[str, Any]) -> AgentResponse:
        """处理任务
        
        Args:
            task: 任务数据
            
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