
export interface CpuInfo {
    cpu_per_core: number[]
    cpu_freq_current: number
    cpu_freq_min: number
    cpu_freq_max: number
    cpu_count: number
}

export interface MemoryInfo {
    memory_total: number
    memory_available: number
    memory_used: number
    memory_percent: number
    swap_total: number
    swap_used: number
    swap_free: number
    swap_percent: number
}

export interface DiskInfo {
    disks: Array<{
        device: string
        mountpoint: string
        fstype: string
        total: number
        used: number
        free: number
        percent: number
    }>
}

export interface NetworkInfo {
    bytes_sent: number
    bytes_recv: number
    packets_sent: number
    packets_recv: number
}   


// 定义接口类型
export interface SystemInfo {
    timestamp: number
    cpu: {
        cpu_per_core: number[]
        cpu_freq_current: number
        cpu_freq_min: number
        cpu_freq_max: number
        cpu_count: number
    }
    memory: {
        memory_total: number
        memory_available: number
        memory_used: number
        memory_percent: number
        swap_total: number
        swap_used: number
        swap_free: number
        swap_percent: number
    }
    disk: {
        disks: Array<{
            device: string
            mountpoint: string
            fstype: string
            total: number
            used: number
            free: number
            percent: number
        }>
    }
    network: {
        bytes_sent: number
        bytes_recv: number
        packets_sent: number
        packets_recv: number
    }
}