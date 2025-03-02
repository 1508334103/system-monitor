from fastapi import APIRouter
from app.core.system_monitor import SystemMonitor
from app.schemas.system_info import SystemInfo

router = APIRouter()
system_monitor = SystemMonitor()

@router.get("/info", response_model=SystemInfo)
async def get_system_info():
    """
    获取系统所有监控指标的汇总信息
    
    Returns:
        SystemInfo: 包含以下系统信息的对象：
            - timestamp: 数据采集时间戳
            - cpu: CPU使用率、频率等信息
            - memory: 内存和交换空间使用情况
            - disk: 各分区的存储使用情况
            - network: 网络接口的数据传输统计
            
    示例响应:
        {
            "timestamp": 1648456789.123,
            "cpu": {
                "cpu_per_core": [40.1, 50.3, ...],
                ...
            },
            "memory": {
                "memory_total": 16777216,
                "memory_used": 8388608,
                ...
            },
            ...
        }
    """
    return system_monitor.get_all_info()

@router.get("/cpu")
async def get_cpu_info():
    """
    获取CPU相关监控指标
    
    Returns:
        Dict: 包含以下CPU信息的字典：
            - cpu_per_core: 每个CPU核心的使用率列表
            - cpu_freq_current: 当前CPU频率（MHz）
            - cpu_freq_min: CPU最小频率（MHz）
            - cpu_freq_max: CPU最大频率（MHz）
            - cpu_count: CPU核心数量
            
    示例响应:
        {
            "cpu_per_core": [40.1, 50.3, 45.6, 44.8],
            "cpu_freq_current": 2500.0,
            "cpu_freq_min": 800.0,
            "cpu_freq_max": 3200.0,
            "cpu_count": 4
        }
    """
    return system_monitor.get_cpu_info()

@router.get("/memory")
async def get_memory_info():
    """
    获取内存和交换空间使用情况
    
    Returns:
        Dict: 包含以下内存信息的字典：
            - memory_total: 总物理内存大小（字节）
            - memory_available: 可用物理内存大小（字节）
            - memory_used: 已使用的物理内存大小（字节）
            - memory_percent: 内存使用率（百分比）
            - swap_total: 交换空间总大小（字节）
            - swap_used: 已使用的交换空间大小（字节）
            - swap_free: 可用交换空间大小（字节）
            - swap_percent: 交换空间使用率（百分比）
            
    示例响应:
        {
            "memory_total": 16777216,
            "memory_available": 8388608,
            "memory_used": 8388608,
            "memory_percent": 50.0,
            "swap_total": 4194304,
            "swap_used": 1048576,
            "swap_free": 3145728,
            "swap_percent": 25.0
        }
    """
    return system_monitor.get_memory_info()

@router.get("/disk")
async def get_disk_info():
    """
    获取系统所有磁盘分区的使用情况
    
    Returns:
        Dict: 包含磁盘分区信息列表的字典：
            disks: 分区信息列表，每个分区包含：
                - device: 设备名称
                - mountpoint: 挂载点
                - fstype: 文件系统类型
                - total: 分区总大小（字节）
                - used: 已使用空间大小（字节）
                - free: 可用空间大小（字节）
                - percent: 使用率（百分比）
                
    示例响应:
        {
            "disks": [
                {
                    "device": "/dev/sda1",
                    "mountpoint": "/",
                    "fstype": "ext4",
                    "total": 250790436864,
                    "used": 168732672000,
                    "free": 82057764864,
                    "percent": 67.3
                },
                ...
            ]
        }
    """
    return system_monitor.get_disk_info()

@router.get("/network")
async def get_network_info():
    """
    获取网络接口的数据传输统计信息
    
    Returns:
        Dict: 包含以下网络统计信息的字典：
            - bytes_sent: 发送的总字节数
            - bytes_recv: 接收的总字节数
            - packets_sent: 发送的数据包总数
            - packets_recv: 接收的数据包总数
            
    示例响应:
        {
            "bytes_sent": 1048576,
            "bytes_recv": 2097152,
            "packets_sent": 1000,
            "packets_recv": 2000
        }
    """
    return system_monitor.get_network_info()