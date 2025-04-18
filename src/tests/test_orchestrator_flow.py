import asyncio
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.core.orchestrator import LLMOrchestrator
from src.agents.order_agent import OrderAgent
from src.agents.planning_agent import PlanningAgent
from src.agents.supply_chain_agent import SupplyChainAgent
from src.agents.prediction_agent import PredictionAgent
from src.agents.finance_agent import FinanceAgent

async def test_orchestrator_flow():
    """测试Orchestrator通过自然语言协调各个Agent的完整流程"""
    print("\n=== 开始测试Orchestrator流程 ===")
    
    # 初始化Orchestrator和所有Agent
    orchestrator = LLMOrchestrator()
    
    # 注册所有Agent
    order_agent = OrderAgent(agent_type="order")
    planning_agent = PlanningAgent(agent_type="planning")
    supply_chain_agent = SupplyChainAgent(agent_type="supply_chain")
    prediction_agent = PredictionAgent(agent_type="prediction")
    finance_agent = FinanceAgent(agent_type="finance")
    
    orchestrator.register_agent(order_agent)
    orchestrator.register_agent(planning_agent)
    orchestrator.register_agent(supply_chain_agent)
    orchestrator.register_agent(prediction_agent)
    orchestrator.register_agent(finance_agent)
    
    # 测试用例1：处理500台电脑订单
    print("\n=== 测试用例1：处理500台电脑订单 ===")
    instruction = "客户需要订购500台高性能电脑，配置要求：Intel i9处理器，32GB内存，1TB SSD，NVIDIA RTX 4080显卡。交货日期为2024-07-01，地址是上海市浦东新区张江高科技园区。请处理这个订单并生成相应的生产计划、采购计划和财务预算。"
    
    # 使用Orchestrator处理指令
    result = await orchestrator.process_instruction(instruction)
    print("\n=== 处理完成 ===")
    print(f"最终结果: {result}")

if __name__ == "__main__":
    asyncio.run(test_orchestrator_flow()) 