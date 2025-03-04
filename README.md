
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
├── index.html                # 入口HTML文件
├── package.json              # 项目配置和依赖
├── public/                   # 公共资源
│   └── vite.svg             # 网站图标
├── src/                      # 源代码目录
│   ├── api/                  # API请求
│   │   └── system.ts        # 系统监控API
│   ├── assets/              # 静态资源
│   │   └── vue.svg         
│   ├── components/          # 组件
│   │   ├── BreadcrumbNav.vue  # 面包屑导航
│   │   ├── CpuChart.vue      # CPU图表
│   │   ├── diskChart.vue     # 磁盘图表
│   │   ├── memoryChart.vue   # 内存图表
│   │   └── networkChart.vue  # 网络图表
│   ├── router/              # 路由
│   │   └── index.ts        # 路由配置
│   ├── stores/              # 状态管理
│   │   ├── hardwareStores.ts # 硬件状态管理
│   │   └── schema.ts        # 类型定义
│   ├── styles/              # 样式
│   │   └── quasar-variables.scss # Quasar主题变量
│   ├── views/               # 页面视图
│   │   ├── CpuView.vue     # CPU页面
│   │   ├── DiskView.vue    # 磁盘页面
│   │   ├── Home.vue        # 主页
│   │   ├── MemoryView.vue  # 内存页面
│   │   └── NetworkView.vue # 网络页面
│   ├── App.vue             # 根组件
│   ├── config.ts           # 配置文件
│   ├── main.ts             # 入口文件
│   ├── style.css          # 全局样式
│   └── vite-env.d.ts      # Vite类型声明
├── tsconfig.json           # TypeScript配置
└── vite.config.ts         # Vite配置