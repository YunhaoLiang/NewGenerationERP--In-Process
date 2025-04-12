from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.core.orchestrator import LLMOrchestrator
from src.agents.order_agent import OrderAgent
from src.agents.production_agent import ProductionAgent
from src.agents.base_agent import BaseAgent

app = FastAPI(title="New Generation ERP")

# 初始化组件
orchestrator = LLMOrchestrator()
order_agent = OrderAgent()
production_agent = ProductionAgent()

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
        elif task.task_type == "production":
            result = await production_agent.process(task.parameters)
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
    elif agent_id == production_agent.agent_id:
        return production_agent.get_status()
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 