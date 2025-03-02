import psutil
import time
from typing import Dict, Any, List

class SystemMonitor:
    """
    系统监控类：用于收集和监控系统的各项性能指标
    包括：CPU使用率、内存使用情况、磁盘使用状况和网络流量等
    """
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """
        获取CPU相关信息
        
        Returns:
            Dict[str, Any]: 包含以下CPU信息的字典：
                - cpu_per_core: 每个CPU核心的使用率列表
                - cpu_freq_current: 当前CPU频率
                - cpu_freq_min: CPU最小频率
                - cpu_freq_max: CPU最大频率
                - cpu_count: CPU核心数量
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            return {
                "cpu_per_core": cpu_percent,
                "cpu_freq_current": round(cpu_freq.current, 2),
                "cpu_freq_min": round(cpu_freq.min, 2),
                "cpu_freq_max": round(cpu_freq.max, 2),
                "cpu_count": cpu_count
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """
        获取系统内存和交换空间使用情况
        
        Returns:
            Dict[str, Any]: 包含以下内存信息的字典：
                - memory_total: 总物理内存大小
                - memory_available: 可用物理内存大小
                - memory_used: 已使用的物理内存大小
                - memory_percent: 内存使用率
                - swap_total: 交换空间总大小
                - swap_used: 已使用的交换空间大小
                - swap_free: 可用交换空间大小
                - swap_percent: 交换空间使用率
        """
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "memory_total": memory.total,
                "memory_available": memory.available,
                "memory_used": memory.used,
                "memory_percent": memory.percent,
                "swap_total": swap.total,
                "swap_used": swap.used,
                "swap_free": swap.free,
                "swap_percent": swap.percent
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_disk_info() -> Dict[str, List[Dict[str, Any]]]:
        """
        获取系统所有磁盘分区的使用情况
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: 包含所有磁盘分区信息的字典列表：
                - device: 设备名称
                - mountpoint: 挂载点
                - fstype: 文件系统类型
                - total: 分区总大小
                - used: 已使用空间大小
                - free: 可用空间大小
                - percent: 使用率
        """
        try:
            partitions = psutil.disk_partitions()
            disk_info = []
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": usage.percent
                    })
                except Exception:
                    # 某些分区可能无法访问（如CD-ROM），跳过这些分区
                    continue
                    
            return {"disks": disk_info}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_network_info() -> Dict[str, int]:
        """
        获取网络接口的数据传输统计信息
        
        Returns:
            Dict[str, int]: 包含以下网络统计信息的字典：
                - bytes_sent: 发送的字节数
                - bytes_recv: 接收的字节数
                - packets_sent: 发送的数据包数量
                - packets_recv: 接收的数据包数量
        """
        try:
            network_io = psutil.net_io_counters()
            
            return {
                "bytes_sent": network_io.bytes_sent,
                "bytes_recv": network_io.bytes_recv,
                "packets_sent": network_io.packets_sent,
                "packets_recv": network_io.packets_recv
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_all_info() -> Dict[str, Any]:
        """
        获取系统所有监控指标的汇总信息
        
        Returns:
            Dict[str, Any]: 包含以下信息的字典：
                - timestamp: 数据采集时间戳
                - cpu: CPU使用情况
                - memory: 内存使用情况
                - disk: 磁盘使用情况
                - network: 网络传输统计
        """
        return {
            "timestamp": time.time(),
            "cpu": SystemMonitor.get_cpu_info(),
            "memory": SystemMonitor.get_memory_info(),
            "disk": SystemMonitor.get_disk_info(),
            "network": SystemMonitor.get_network_info()
        }