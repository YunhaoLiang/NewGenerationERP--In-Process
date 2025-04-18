import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.core.orchestrator import LLMOrchestrator
from src.agents.order_agent import OrderAgent
from src.agents.planning_agent import PlanningAgent
from src.agents.base_agent import BaseAgent
from fastapi.responses import RedirectResponse

app = FastAPI(title="New Generation ERP")

# 添加根路径路由
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# 初始化组件
orchestrator = LLMOrchestrator()
order_agent = OrderAgent()
planning_agent = PlanningAgent()

class Instruction(BaseModel):
    """业务指令模型"""
    text: str
    parameters: Dict[str, Any] = {}

@app.post("/process_instruction")
async def process_instruction(instruction: Instruction):
    """处理业务指令
    
    Args:
        instruction: 业务指令
        
    Returns:
        Dict: 处理结果
    """
    try:
        print("\n=== 收到新的指令 ===")
        print(f"指令内容: {instruction.text}")
        print(f"指令参数: {instruction.parameters}")
        
        # 使用编排器处理指令
        task = await orchestrator.process_instruction(instruction.text, instruction.parameters)
        print(f"\n=== 任务创建结果 ===")
        print(f"任务ID: {task.task_id}")
        print(f"任务类型: {task.task_type}")
        print(f"任务参数: {task.parameters}")
        
        # 根据任务类型调用相应的Agent
        if task.task_type == "order":
            result = await order_agent.process(task.parameters)
            print(f"\n=== 订单处理结果 ===")
            print(f"处理状态: {result.status}")
            print(f"订单数据: {result.data}")
            return result.dict()
        elif task.task_type == "planning":
            result = await planning_agent.process(task.parameters)
            print(f"\n=== 计划处理结果 ===")
            print(f"处理状态: {result.status}")
            print(f"计划数据: {result.data}")
            return result.dict()
        else:
            raise HTTPException(status_code=400, detail="Unsupported task type")
            
    except Exception as e:
        print(f"\n=== 处理出错 ===")
        print(f"错误信息: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agent_status/{agent_id}")
async def get_agent_status(agent_id: str):
    """获取Agent状态
    
    Args:
        agent_id: Agent ID
        
    Returns:
        Dict: Agent状态
    """
    if agent_id == order_agent.agent_id:
        return order_agent.get_status()
    elif agent_id == planning_agent.agent_id:
        return planning_agent.get_status()
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080) 


## 在项目根目录下运行
# cd C:\Users\Louis\Desktop\NewGenerationERP--In-Process
# python -m src.api.main