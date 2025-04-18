# 新一代ERP系统

基于LLM、智能Agent和联邦学习的新一代ERP系统。

## 功能特点

- 基于LLM的智能编排器，支持自然语言指令处理
- 模块化的智能Agent架构
- 支持联邦学习的数据处理
- 基于MCP协议的通信机制
- 端到端的自动化流程

## 系统要求

- Python 3.8+
- CUDA支持的GPU（推荐）

## 安装

1. 克隆仓库：
```bash
git clone [repository_url]
cd newERP
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

1. 启动API服务：
```bash
python src/api/main.py
```

2. 访问API文档：
```
http://localhost:8000/docs
```

## 项目结构

```
src/
├── agents/          # 智能Agent实现
├── core/            # 核心组件
├── models/          # 机器学习模型
├── utils/           # 工具函数
├── api/             # API接口
└── database/        # 数据库相关
```

## 开发计划

1. 第一阶段：基础架构搭建
   - [x] LLM编排器
   - [x] 基础Agent框架
   - [ ] MCP协议实现

2. 第二阶段：核心功能实现
   - [ ] 订单处理Agent
   - [ ] 生产计划Agent
   - [ ] 采购Agent
   - [ ] 库存Agent

3. 第三阶段：高级功能
   - [ ] 联邦学习支持
   - [ ] 预测分析
   - [ ] 自动化决策

## 贡献指南

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License 