from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class NLPRequest(BaseModel):
    text: str
    requireAgents: bool = False

class NLPResponse(BaseModel):
    status: str
    result: Dict[str, Any]
    message: str
    timestamp: str

def extract_order_info(text: str) -> Dict[str, Any]:
    """从文本中提取订单信息"""
    info = {
        "customer": None,
        "quantity": 0,
        "specs": {},
        "delivery_date": None,
        "address": None
    }
    
    # 提取客户名称
    customer_match = re.search(r'客户(\w+)', text)
    if customer_match:
        info["customer"] = customer_match.group(1)
    
    # 提取数量
    quantity_match = re.search(r'(\d+)台', text)
    if quantity_match:
        info["quantity"] = int(quantity_match.group(1))
    
    # 提取配置信息
    specs = {
        "cpu": re.search(r'(Intel\s+i\d+|AMD\s+Ryzen\s+\d+)', text),
        "memory": re.search(r'(\d+)GB', text),
        "storage": re.search(r'(\d+)TB', text),
        "gpu": re.search(r'(NVIDIA\s+RTX\s+\d+|AMD\s+Radeon\s+\w+)', text)
    }
    
    info["specs"] = {
        key: match.group(1) if match else None
        for key, match in specs.items()
    }
    
    # 提取日期
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    if date_match:
        info["delivery_date"] = date_match.group(1)
    
    # 提取地址
    address_match = re.search(r'地址是(.*?)[。\n]', text)
    if address_match:
        info["address"] = address_match.group(1).strip()
    
    return info

@router.post("/process")
async def process(request: NLPRequest):
    try:
        logger.info(f"收到处理请求: {request.text}")
        
        # 提取订单信息
        order_info = extract_order_info(request.text)
        
        # 模拟各个 Agent 的处理过程
        agents_process = {
            "order_agent": {
                "action": "创建订单",
                "details": {
                    "order_no": "ORD" + datetime.now().strftime("%Y%m%d%H%M%S"),
                    "customer": order_info["customer"],
                    "quantity": order_info["quantity"],
                    "delivery_date": order_info["delivery_date"],
                    "shipping_address": order_info["address"]
                }
            },
            "planning_agent": {
                "action": "生成生产计划",
                "details": {
                    "production_phases": [
                        {
                            "phase": "组装",
                            "start_date": "2024-06-01",
                            "end_date": "2024-06-15",
                            "quantity": order_info["quantity"]
                        },
                        {
                            "phase": "测试",
                            "start_date": "2024-06-16",
                            "end_date": "2024-06-25",
                            "quantity": order_info["quantity"]
                        }
                    ]
                }
            },
            "supply_chain_agent": {
                "action": "生成采购计划",
                "details": {
                    "required_components": [
                        {
                            "item": "CPU " + (order_info["specs"].get("cpu") or ""),
                            "quantity": order_info["quantity"],
                            "estimated_cost": 2500
                        },
                        {
                            "item": "内存 " + (order_info["specs"].get("memory") or ""),
                            "quantity": order_info["quantity"],
                            "estimated_cost": 800
                        },
                        {
                            "item": "固态硬盘 " + (order_info["specs"].get("storage") or ""),
                            "quantity": order_info["quantity"],
                            "estimated_cost": 600
                        },
                        {
                            "item": "显卡 " + (order_info["specs"].get("gpu") or ""),
                            "quantity": order_info["quantity"],
                            "estimated_cost": 5000
                        }
                    ]
                }
            },
            "finance_agent": {
                "action": "生成财务预算",
                "details": {
                    "cost_estimation": {
                        "materials": order_info["quantity"] * 8900,  # 材料成本
                        "labor": order_info["quantity"] * 500,      # 人工成本
                        "overhead": order_info["quantity"] * 300     # 管理费用
                    },
                    "total_cost": order_info["quantity"] * 9700,
                    "suggested_price": order_info["quantity"] * 12000,
                    "estimated_profit": order_info["quantity"] * 2300
                }
            }
        }
        
        # 构建响应
        result = {
            "status": "success",
            "result": {
                "type": "order_processing",
                "content": f"已完成订单处理：{order_info['quantity']}台电脑订单已创建，"
                          f"预计交付日期 {order_info['delivery_date']}",
                "details": {
                    "order_info": order_info,
                    "agents_process": agents_process,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            },
            "message": "处理完成",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"处理成功: {result}")
        return result
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"处理失败: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        ) 