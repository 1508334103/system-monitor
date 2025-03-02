import { defineStore } from 'pinia'
import { systemApi } from '../api/system.ts'
import { ref } from 'vue'
import type { CpuInfo, MemoryInfo, DiskInfo, NetworkInfo, SystemInfo } from './schema'

// CPU Store
export const useCpuStore = defineStore('cpu', () => {
    const cpuInfo = ref<CpuInfo | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)
    let intervalId: number | null = null

    async function fetchCpuInfo() {
        try {
            if (error.value) error.value = null
            const response = await systemApi.getCpuInfo()
            cpuInfo.value = response.data
        } catch (e: unknown) {
            if ((e as Error).message === 'Request cancelled') return
            error.value = e instanceof Error ? e.message : 'Unknown error'
        } finally {
            loading.value = false
        }
    }

    function startAutoUpdate(interval = 3000) {
        if (intervalId) return
        fetchCpuInfo() // 立即获取一次数据
        intervalId = window.setInterval(fetchCpuInfo, interval)
    }

    function stopAutoUpdate() {
        if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
        }
    }

    return {
        cpuInfo,
        loading,
        error,
        fetchCpuInfo,
        startAutoUpdate,
        stopAutoUpdate
    }
})

// Memory Store
export const useMemoryStore = defineStore('memory', () => {
    const memoryInfo = ref<MemoryInfo | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)
    let intervalId: number | null = null

    async function fetchMemoryInfo() {
        try {
            if (error.value) error.value = null
            const response = await systemApi.getMemoryInfo()
            memoryInfo.value = response.data
        } catch (e: unknown) {
            if ((e as Error).message === 'Request cancelled') return
            error.value = e instanceof Error ? e.message : 'Unknown error'
        } finally {
            loading.value = false
        }
    }

    function startAutoUpdate(interval = 3000) {
        if (intervalId) return
        fetchMemoryInfo()
        intervalId = window.setInterval(fetchMemoryInfo, interval)
    }

    function stopAutoUpdate() {
        if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
        }
    }

    return {
        memoryInfo,
        loading,
        error,
        fetchMemoryInfo,
        startAutoUpdate,
        stopAutoUpdate
    }
})

// Disk Store
export const useDiskStore = defineStore('disk', () => {
    const diskInfo = ref<DiskInfo | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)
    let intervalId: number | null = null

    async function fetchDiskInfo() {
        try {
            if (error.value) error.value = null
            const response = await systemApi.getDiskInfo()
            diskInfo.value = response.data
        } catch (e: unknown) {
            if ((e as Error).message === 'Request cancelled') return
            error.value = e instanceof Error ? e.message : 'Unknown error'
        } finally {
            loading.value = false
        }
    }

    function startAutoUpdate(interval = 10000) { // 磁盘信息可以更新得慢一些
        if (intervalId) return
        fetchDiskInfo()
        intervalId = window.setInterval(fetchDiskInfo, interval)
    }

    function stopAutoUpdate() {
        if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
        }
    }

    return {
        diskInfo,
        loading,
        error,
        fetchDiskInfo,
        startAutoUpdate,
        stopAutoUpdate
    }
})

// Network Store
export const useNetworkStore = defineStore('network', () => {
    const networkInfo = ref<NetworkInfo | null>(null)
    const loading = ref(true)
    const error = ref<string | null>(null)  
    let intervalId: number | null = null

    async function fetchNetworkInfo() {
        try {
            if (error.value) error.value = null
            const response = await systemApi.getNetworkInfo()
            networkInfo.value = response.data
        } catch (e: unknown) {
            if ((e as Error).message === 'Request cancelled') return
            error.value = e instanceof Error ? e.message : 'Unknown error'
        } finally {
            loading.value = false
        }
    }

    function startAutoUpdate(interval = 2000) { // 网络信息可以更新得更频繁
        if (intervalId) return
        fetchNetworkInfo()
        intervalId = window.setInterval(fetchNetworkInfo, interval)
    }

    function stopAutoUpdate() {
        if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
        }
    }

    return {
        networkInfo,
        loading,
        error,
        fetchNetworkInfo,
        startAutoUpdate,
        stopAutoUpdate
    }
}) 



export const useSystemStore = defineStore('system', () => {
    // 状态
    const systemInfo = ref<SystemInfo | null>(null)
    const initialLoading = ref(true)  // 新增：初始加载状态
    const error = ref<string | null>(null)

    // actions
    async function fetchSystemInfo() {
        try {
            if (error.value) error.value = null
            const response = await systemApi.getSystemInfo()
            systemInfo.value = response.data
        } catch (e: unknown) {
            // 忽略取消的请求错误
            if ((e as Error).message === 'Request cancelled') {
                return
            }
            error.value = e instanceof Error ? e.message : 'Unknown error'
        } finally {
            if (initialLoading.value) initialLoading.value = false
        }
    }

    // 定时更新数据
    let intervalId: number | null = null

    function startAutoUpdate(interval: number = 3000) {
        if (intervalId) return
        fetchSystemInfo() // 立即获取一次数据
        intervalId = window.setInterval(fetchSystemInfo, interval)
    }

    function stopAutoUpdate() {
        if (intervalId) {
            clearInterval(intervalId)
            intervalId = null
        }
    }

    return {
        systemInfo,
        initialLoading,  // 导出初始加载状态
        error,
        fetchSystemInfo,
        startAutoUpdate,
        stopAutoUpdate
    }
})