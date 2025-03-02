from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import system

# 创建FastAPI应用实例
app = FastAPI(
    title="System Monitor API",
    description="...",
    version="1.0.0",
    docs_url="/api/docs",    # 自定义API文档路径
    redoc_url="/api/redoc"   # 自定义ReDoc文档路径
)

# 配置CORS（跨源资源共享）中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # 前端开发服务器地址
    ],
    allow_credentials=True,      # 允许携带凭证
    allow_methods=["*"],        # 允许所有HTTP方法
    allow_headers=["*"],        # 允许所有HTTP头
)

# 注册系统监控相关路由
app.include_router(
    system.router,
    prefix="/api/system",    # 路由前缀
    tags=["system"]         # API文档分类标签
)

@app.get("/")
async def root():
    """
    API根路径，返回服务基本信息
    
    Returns:
        Dict: 包含API服务信息的字典
    
    示例响应:
        {
            "message": "System Monitor API"
        }
    """
    return {"message": "System Monitor API"}