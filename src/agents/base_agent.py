from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from abc import ABC, abstractmethod
import uuid
import asyncio
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentResponse(BaseModel):
    """Agent响应模型"""
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式
        
        Returns:
            Dict[str, Any]: 字典格式的响应数据
        """
        return {
            "status": self.status,
            "data": self.data,
            "error": self.error,
            "execution_time": self.execution_time,
            "metrics": self.metrics
        }

class AgentError(Exception):
    """Agent错误基类"""
    def __init__(self, message: str, is_recoverable: bool = True):
        self.message = message
        self.is_recoverable = is_recoverable
        super().__init__(message)

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
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "last_error": None
        }
        self._lock = asyncio.Lock()
        
    async def process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """处理任务
        
        Args:
            parameters: 任务参数
            
        Returns:
            AgentResponse: 处理结果
        """
        start_time = datetime.now()
        self.status = "processing"
        self.metrics["total_requests"] += 1
        
        try:
            async with self._lock:
                result = await self._process_with_retry(parameters)
                self.metrics["successful_requests"] += 1
                return result
        except AgentError as e:
            self.metrics["failed_requests"] += 1
            self.metrics["last_error"] = str(e)
            logger.error(f"Agent {self.agent_id} 处理失败: {str(e)}")
            return AgentResponse(
                status="error",
                error=str(e),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
        except Exception as e:
            self.metrics["failed_requests"] += 1
            self.metrics["last_error"] = str(e)
            logger.error(f"Agent {self.agent_id} 发生未预期的错误: {str(e)}")
            return AgentResponse(
                status="error",
                error=f"未预期的错误: {str(e)}",
                execution_time=(datetime.now() - start_time).total_seconds()
            )
        finally:
            self.status = "idle"
            self._update_metrics(start_time)
    
    async def _process_with_retry(self, parameters: Dict[str, Any], max_retries: int = 3) -> AgentResponse:
        """带重试机制的处理方法
        
        Args:
            parameters: 任务参数
            max_retries: 最大重试次数
            
        Returns:
            AgentResponse: 处理结果
        """
        for attempt in range(max_retries):
            try:
                return await self._process(parameters)
            except AgentError as e:
                if not e.is_recoverable or attempt == max_retries - 1:
                    raise
                logger.warning(f"Agent {self.agent_id} 第{attempt + 1}次重试")
                await asyncio.sleep(1 * (attempt + 1))  # 指数退避
    
    @abstractmethod
    async def _process(self, parameters: Dict[str, Any]) -> AgentResponse:
        """具体的处理逻辑，由子类实现"""
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
    
    def get_status(self) -> Dict[str, Any]:
        """获取Agent状态
        
        Returns:
            Dict[str, Any]: 状态信息
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "status": self.status,
            "metrics": self.metrics
        }
    
    def _update_metrics(self, start_time: datetime):
        """更新性能指标
        
        Args:
            start_time: 开始时间
        """
        execution_time = (datetime.now() - start_time).total_seconds()
        self.metrics["average_response_time"] = (
            self.metrics["average_response_time"] * (self.metrics["total_requests"] - 1) + execution_time
        ) / self.metrics["total_requests"]
    
    async def reset(self):
        """重置Agent状态"""
        self.status = "idle"
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "last_error": None
        } 