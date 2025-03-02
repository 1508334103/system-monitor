import psutil
import time
import os
import re
from typing import Dict, Any, List

# 检查是否在容器内运行
HOST_PROC = '/host/proc' if os.path.exists('/host/proc') else '/proc'
HOST_SYS = '/host/sys' if os.path.exists('/host/sys') else '/sys'

class SystemMonitor:
    """
    系统监控类：用于收集和监控系统的各项性能指标
    包括：CPU使用率、内存使用情况、磁盘使用状况和网络流量等
    """
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """获取CPU相关信息"""
        # 检查是否在容器中且有宿主机挂载
        if os.path.exists('/host/proc'):
            try:
                return SystemMonitor._get_host_cpu_info()
            except Exception as e:
                print(f"Error reading host CPU info: {e}")
                # 失败时回退到容器内监控
                return SystemMonitor._get_container_cpu_info()
        else:
            return SystemMonitor._get_container_cpu_info()
    
    @staticmethod
    def _get_host_cpu_info() -> Dict[str, Any]:
        """从宿主机/proc目录获取CPU信息"""
        # 读取CPU使用率
        cpu_percent = []
        
        # 读取/proc/stat获取CPU使用情况
        with open(f"{HOST_PROC}/stat", "r") as f:
            cpu_lines = [line for line in f if line.startswith('cpu')]
        
        # 第一行是总体CPU，后面的是每个核心
        per_cpu_lines = cpu_lines[1:]
        
        # 计算每个核心的使用率
        for line in per_cpu_lines:
            values = line.split()[1:8]
            values = [int(val) for val in values]
            user, nice, system, idle, iowait, irq, softirq = values
            
            # 简单计算使用率 (非空闲时间/总时间)
            non_idle = user + nice + system + irq + softirq
            total = non_idle + idle + iowait
            percent = (non_idle / total) * 100 if total > 0 else 0
            cpu_percent.append(round(percent, 1))
        
        # 获取CPU频率
        cpu_freq = {"current": 0, "min": 0, "max": 0}
        try:
            # 尝试读取当前频率
            freq_files = os.listdir(f"{HOST_SYS}/devices/system/cpu/cpu0/cpufreq/")
            if "scaling_cur_freq" in freq_files:
                with open(f"{HOST_SYS}/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
                    cpu_freq["current"] = round(int(f.read().strip()) / 1000, 2)  # 转换为MHz
            
            if "scaling_min_freq" in freq_files:
                with open(f"{HOST_SYS}/devices/system/cpu/cpu0/cpufreq/scaling_min_freq", "r") as f:
                    cpu_freq["min"] = round(int(f.read().strip()) / 1000, 2)
            
            if "scaling_max_freq" in freq_files:
                with open(f"{HOST_SYS}/devices/system/cpu/cpu0/cpufreq/scaling_max_freq", "r") as f:
                    cpu_freq["max"] = round(int(f.read().strip()) / 1000, 2)
        except Exception as e:
            print(f"Error reading CPU frequency: {e}")
        
        # 获取CPU核心数
        cpu_count = len(per_cpu_lines)
        
        return {
            "cpu_per_core": cpu_percent,
            "cpu_freq_current": cpu_freq["current"],
            "cpu_freq_min": cpu_freq["min"],
            "cpu_freq_max": cpu_freq["max"],
            "cpu_count": cpu_count
        }
    
    @staticmethod
    def _get_container_cpu_info() -> Dict[str, Any]:
        """获取容器内CPU信息（原方法）"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        cpu_count = psutil.cpu_count()
        
        return {
            "cpu_per_core": cpu_percent,
            "cpu_freq_current": round(cpu_freq.current, 2) if cpu_freq else 0,
            "cpu_freq_min": round(cpu_freq.min, 2) if cpu_freq and cpu_freq.min else 0,
            "cpu_freq_max": round(cpu_freq.max, 2) if cpu_freq and cpu_freq.max else 0,
            "cpu_count": cpu_count
        }

    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """获取系统内存和交换空间使用情况"""
        if os.path.exists('/host/proc'):
            try:
                return SystemMonitor._get_host_memory_info()
            except Exception as e:
                print(f"Error reading host memory info: {e}")
                return SystemMonitor._get_container_memory_info()
        else:
            return SystemMonitor._get_container_memory_info()
    
    @staticmethod
    def _get_host_memory_info() -> Dict[str, Any]:
        """从宿主机/proc目录获取内存信息"""
        # 读取/proc/meminfo获取内存信息
        mem_info = {}
        with open(f"{HOST_PROC}/meminfo", "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    value = value.strip()
                    if value.endswith("kB"):
                        value = int(value.split()[0]) * 1024  # 转换为字节
                    mem_info[key.strip()] = value
        
        # 计算内存使用情况
        total = int(mem_info.get("MemTotal", 0))
        free = int(mem_info.get("MemFree", 0))
        buffers = int(mem_info.get("Buffers", 0))
        cached = int(mem_info.get("Cached", 0))
        
        available = free + buffers + cached
        used = total - available
        percent = (used / total) * 100 if total > 0 else 0
        
        # 计算交换空间使用情况
        swap_total = int(mem_info.get("SwapTotal", 0))
        swap_free = int(mem_info.get("SwapFree", 0))
        swap_used = swap_total - swap_free
        swap_percent = (swap_used / swap_total) * 100 if swap_total > 0 else 0
        
        return {
            "memory_total": total,
            "memory_available": available,
            "memory_used": used,
            "memory_percent": round(percent, 1),
            "swap_total": swap_total,
            "swap_used": swap_used,
            "swap_free": swap_free,
            "swap_percent": round(swap_percent, 1)
        }
    
    @staticmethod
    def _get_container_memory_info() -> Dict[str, Any]:
        """获取容器内存信息（原方法）"""
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

    @staticmethod
    def get_disk_info() -> Dict[str, List[Dict[str, Any]]]:
        """获取系统所有磁盘分区的使用情况"""
        if os.path.exists('/host/proc'):
            try:
                return SystemMonitor._get_host_disk_info()
            except Exception as e:
                print(f"Error reading host disk info: {e}")
                return SystemMonitor._get_container_disk_info()
        else:
            return SystemMonitor._get_container_disk_info()
    
    @staticmethod
    def _get_host_disk_info() -> Dict[str, List[Dict[str, Any]]]:
        """从宿主机获取磁盘信息"""
        disks = []
        
        # 读取/proc/mounts获取挂载点信息
        with open(f"{HOST_PROC}/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 6:
                    device, mountpoint, fstype = parts[0], parts[1], parts[2]
                    
                    # 跳过虚拟文件系统
                    if fstype in ('proc', 'sysfs', 'devtmpfs', 'devpts', 'tmpfs', 'cgroup', 'cgroup2'):
                        continue
                    
                    # 获取磁盘使用情况
                    try:
                        # 尝试使用os.statvfs获取磁盘使用情况
                        # 注意：这可能不会获取宿主机的真实信息，因为我们无法直接访问宿主机的文件系统
                        # 这是一个限制，可能需要更复杂的解决方案
                        stat = os.statvfs(mountpoint)
                        total = stat.f_blocks * stat.f_frsize
                        free = stat.f_bfree * stat.f_frsize
                        used = total - free
                        percent = (used / total) * 100 if total > 0 else 0
                        
                        disks.append({
                            "device": device,
                            "mountpoint": mountpoint,
                            "fstype": fstype,
                            "total": total,
                            "used": used,
                            "free": free,
                            "percent": round(percent, 1)
                        })
                    except Exception as e:
                        print(f"Error getting disk stats for {mountpoint}: {e}")
        
        return {"disks": disks}
    
    @staticmethod
    def _get_container_disk_info() -> Dict[str, List[Dict[str, Any]]]:
        """获取容器内磁盘信息（原方法）"""
        disks_info = []
        for partition in psutil.disk_partitions(all=False):
            if partition.fstype:
                usage = psutil.disk_usage(partition.mountpoint)
                disks_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                })
        
        return {"disks": disks_info}

    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        """获取网络接口的数据传输统计信息"""
        if os.path.exists('/host/proc'):
            try:
                return SystemMonitor._get_host_network_info()
            except Exception as e:
                print(f"Error reading host network info: {e}")
                return SystemMonitor._get_container_network_info()
        else:
            return SystemMonitor._get_container_network_info()
    
    @staticmethod
    def _get_host_network_info() -> Dict[str, Any]:
        """从宿主机获取网络信息"""
        # 读取/proc/net/dev获取网络接口统计信息
        bytes_sent = 0
        bytes_recv = 0
        packets_sent = 0
        packets_recv = 0
        
        with open(f"{HOST_PROC}/net/dev", "r") as f:
            lines = f.readlines()
            
        # 跳过前两行（标题行）
        for line in lines[2:]:
            parts = line.split(":")
            if len(parts) >= 2:
                interface = parts[0].strip()
                
                # 跳过loopback和容器接口
                if interface == "lo" or interface.startswith("docker") or interface.startswith("veth"):
                    continue
                
                values = parts[1].strip().split()
                if len(values) >= 10:
                    # 接收字节数在第1列，发送字节数在第9列
                    bytes_recv += int(values[0])
                    packets_recv += int(values[1])
                    bytes_sent += int(values[8])
                    packets_sent += int(values[9])
        
        return {
            "bytes_sent": bytes_sent,
            "bytes_recv": bytes_recv,
            "packets_sent": packets_sent,
            "packets_recv": packets_recv
        }
    
    @staticmethod
    def _get_container_network_info() -> Dict[str, Any]:
        """获取容器内网络信息（原方法）"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_recv": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv
        }

    @staticmethod
    def get_all_info() -> Dict[str, Any]:
        """
        获取所有系统监控指标
        
        Returns:
            Dict[str, Any]: 包含以下系统信息的字典：
                - timestamp: 数据采集时间戳
                - cpu: CPU使用率、频率等信息
                - memory: 内存和交换空间使用情况
                - disk: 各分区的存储使用情况
                - network: 网络接口的数据传输统计
        """
        return {
            "timestamp": time.time(),
            "cpu": SystemMonitor.get_cpu_info(),
            "memory": SystemMonitor.get_memory_info(),
            "disk": SystemMonitor.get_disk_info(),
            "network": SystemMonitor.get_network_info()
        }