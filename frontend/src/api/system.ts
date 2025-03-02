import axios from 'axios'
import type { CpuInfo, MemoryInfo, DiskInfo, NetworkInfo, SystemInfo } from '../stores/schema'

// 创建 axios 实例
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 5000
})

// API 方法
export const systemApi = {
    // 获取所有系统信息
    getSystemInfo: () => api.get<SystemInfo>('/system/info'),
    
    // 获取 CPU 信息
    getCpuInfo: () => api.get<CpuInfo>('/system/cpu'),
    
    // 获取内存信息
    getMemoryInfo: () => api.get<MemoryInfo>('/system/memory'),
    
    // 获取磁盘信息
    getDiskInfo: () => api.get<DiskInfo>('/system/disk'),
    
    // 获取网络信息
    getNetworkInfo: () => api.get<NetworkInfo>('/system/network')
}