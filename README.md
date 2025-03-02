
5. 添加 README.md：
```markdown:README.md
# System Monitor

一个基于 FastAPI 和 Vue3 的系统监控工具。

## 功能特性

- CPU 使用率监控
- 内存使用情况
- 磁盘使用状态
- 实时数据更新

## 技术栈

### 后端
- FastAPI
- psutil
- uvicorn

### 前端
- Vue 3
- Quasar
- ECharts
- Pinia

## 快速开始

### 后端启动

cd backend
python -m venv venv
source venv/bin/activate # 在 Windows 上使用 venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

### 前端启动

cd frontend
npm install
npm run dev
```

## 项目结构

backend/
├── main.py # FastAPI 主文件
├── requirements.txt # 依赖列表
└── utils/ # 工具函数

frontend/
├── public/ # 静态文件
└── src/ # 源码