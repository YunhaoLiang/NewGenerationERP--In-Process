import sys
import os
import asyncio
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.order_agent import OrderAgent

async def test_order_agent():
    try:
        print("开始测试OrderAgent...")
        agent = OrderAgent()
        
        # 测试创建订单
        order_data = {
            "用户ID": 1,  # admin用户
            "产品ID": 1,  # ThinkPad X1
            "数量": 1
        }
        
        print(f"\n尝试创建订单：{order_data}")
        
        # 创建订单
        result = await agent.process_order(order_data)
        print("\n创建订单结果：")
        print(result)
        
        if result["success"]:
            # 查询订单状态
            order_status = await agent.get_order_status(result["data"]["订单ID"])
            print("\n订单状态：")
            print(order_status)
        else:
            print(f"\n创建订单失败：{result['message']}")
            
    except Exception as e:
        print(f"\n测试过程中出错：{str(e)}")
    finally:
        if 'agent' in locals():
            del agent
        print("\n测试完成")

if __name__ == "__main__":
    asyncio.run(test_order_agent()) 