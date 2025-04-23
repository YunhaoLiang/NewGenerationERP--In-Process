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

def determine_request_type(text: str) -> str:
    """根据输入文本确定请求类型"""
    # 基于关键词匹配来确定请求类型
    if re.search(r'(订购|订单|购买|买|订购)', text) and re.search(r'(\d+)台', text):
        return "order_processing"
    elif re.search(r'(查询|检索|显示|查看|看).*?订单', text):
        return "order_query"
    elif re.search(r'(生成|创建|制作|出).*?(报表|报告|统计)', text):
        return "report_generation"
    elif re.search(r'(分析|评估|比较|预测)', text):
        return "data_analysis"
    elif re.search(r'(库存|盘点)', text):
        return "inventory_management"
    elif re.search(r'(供应商|供货商)', text):
        return "supplier_management"
    else:
        return "general_inquiry"

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
        "gpu": re.search(r'(NVIDIA\s+RTX\s+\d+|AMD\s+Radeon\s+\w+|RTX\d+)', text)
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

def generate_content_based_on_type(request_type: str, info: Dict[str, Any]) -> str:
    """根据请求类型生成相应的内容"""
    if request_type == "order_processing":
        return f"已完成订单处理：{info['quantity']}台电脑订单已创建，预计交付日期 {info['delivery_date']}"
    elif request_type == "order_query":
        return "已查询订单信息，共找到3条相关记录"
    elif request_type == "report_generation":
        return "已生成销售报表，报表周期：本月，包含销售总额、订单数量和客户分布等信息"
    elif request_type == "data_analysis":
        return "已完成数据分析，分析结果包含趋势预测和异常检测"
    elif request_type == "inventory_management":
        return "已完成库存管理操作，当前库存状态已更新"
    elif request_type == "supplier_management":
        return "已完成供应商管理操作，相关信息已更新"
    else:
        return "已处理您的请求，但未能匹配到具体业务类型"

@router.post("/process")
async def process(request: NLPRequest):
    try:
        logger.info(f"收到处理请求: {request.text}")
        
        # 确定请求类型
        request_type = determine_request_type(request.text)
        
        # 提取订单信息
        order_info = extract_order_info(request.text)
        
        # 根据请求类型生成相应内容
        response_content = generate_content_based_on_type(request_type, order_info)
        
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
                "type": request_type,  # 动态设置请求类型
                "content": response_content,  # 动态生成内容
                "details": {
                    "order_info": order_info,
                    "request_type": request_type,  # 额外添加请求类型信息
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