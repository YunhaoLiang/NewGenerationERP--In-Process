import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.orchestrator import LLMOrchestrator

async def test_orchestrator():
    # 初始化编排器
    orchestrator = LLMOrchestrator()
    
    # 测试用例1：订单处理
    print("\n=== 测试1：订单处理 ===")
    instruction1 = "客户编号CUS_12345678订购5台电脑，3台打印机，需要5月20日送到北京市海淀区，这是VIP订单"
    task1 = await orchestrator.process_instruction(instruction1)
    result1 = await orchestrator.execute_task(task1.task_id)
    print(f"订单处理结果: {result1}")
    
    # 测试用例2：生产任务
    print("\n=== 测试2：生产任务 ===")
    instruction2 = "需要生产10台服务器，预计6月1日完成"
    task2 = await orchestrator.process_instruction(instruction2)
    result2 = await orchestrator.execute_task(task2.task_id)
    print(f"生产任务结果: {result2}")
    
    # 测试用例3：采购任务
    print("\n=== 测试3：采购任务 ===")
    instruction3 = "采购20个CPU，15个内存条，需要6月5日到货"
    task3 = await orchestrator.process_instruction(instruction3)
    result3 = await orchestrator.execute_task(task3.task_id)
    print(f"采购任务结果: {result3}")
    
    # 测试用例4：错误处理
    print("\n=== 测试4：错误处理 ===")
    try:
        # 尝试执行不存在的任务
        await orchestrator.execute_task("nonexistent_task")
    except Exception as e:
        print(f"预期错误: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_orchestrator()) 