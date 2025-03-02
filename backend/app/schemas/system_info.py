from pydantic import BaseModel
from typing import List, Dict, Any

class SystemInfo(BaseModel):
    """
    系统信息数据模型
    
    用于序列化和验证系统监控数据的Pydantic模型，对应SystemMonitor.get_all_info()的返回格式
    
    Attributes:
        timestamp (float): 数据采集时间戳
        cpu (Dict[str, Any]): CPU相关信息，包含:
            - cpu_percent: CPU总体使用率
            - cpu_per_core: 每个核心的使用率
            - cpu_freq_current: 当前频率
            - cpu_freq_min: 最小频率
            - cpu_freq_max: 最大频率
            - cpu_count: CPU核心数
        
        memory (Dict[str, Any]): 内存使用信息，包含:
            - memory_total: 总内存
            - memory_available: 可用内存
            - memory_used: 已用内存
            - memory_percent: 内存使用率
            - swap_total: 交换空间总量
            - swap_used: 已用交换空间
            - swap_free: 可用交换空间
            - swap_percent: 交换空间使用率
        
        disk (Dict[str, Any]): 磁盘使用信息，包含:
            - disks: 磁盘分区列表，每个分区包含设备名、挂载点、
                    文件系统类型、容量和使用率等信息
        
        network (Dict[str, Any]): 网络传输统计信息，包含:
            - bytes_sent: 发送字节数
            - bytes_recv: 接收字节数
            - packets_sent: 发送包数
            - packets_recv: 接收包数
    """
    timestamp: float
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    disk: Dict[str, Any]
    network: Dict[str, Any]