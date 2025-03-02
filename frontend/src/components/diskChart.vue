<template>
    <q-card class="disk-chart">
        <q-card-section>
            <div class="text-h6">磁盘使用率</div>
            <!-- 加载状态 -->
            <div v-if="diskStore.loading" class="flex flex-center" style="height: 300px">
                <q-spinner-dots size="40px" color="primary" />
                <span class="q-ml-sm">加载中...</span>
            </div>
            
            <!-- 错误状态 -->
            <div v-else-if="diskStore.error" class="flex flex-center" style="height: 300px">
                <q-banner class="bg-negative text-white">
                    {{ diskStore.error }}
                </q-banner>
            </div>
            <!-- 图表 -->
            <div v-else ref="chartRef" style="height: 300px"></div>
        </q-card-section>
    </q-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { useDiskStore } from '../stores/hardwareStores'

const diskStore = useDiskStore()

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
    if (!chartRef.value || !diskStore.diskInfo) return
    
    chart = echarts.init(chartRef.value)
    
    // 准备数据
    const diskData = diskStore.diskInfo.disks.map(disk => ({
        name: disk.mountpoint,
        value: disk.percent,
        total: formatSize(disk.total),
        used: formatSize(disk.used),
        free: formatSize(disk.free)
    }))
    
    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: function(params: any) {
                const disk = params[0];
                return `<div>
                    <p><strong>${disk.name}</strong></p>
                    <p>使用率: ${disk.value}%</p>
                    <p>总容量: ${disk.data.total}</p>
                    <p>已使用: ${disk.data.used}</p>
                    <p>可用: ${disk.data.free}</p>
                </div>`;
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            max: 100,
            name: '使用率 (%)'
        },
        yAxis: {
            type: 'category',
            data: diskData.map(item => item.name),
            axisLabel: {
                formatter: function(value: string) {
                    // 如果路径太长，截断显示
                    return value.length > 15 ? value.substring(0, 12) + '...' : value;
                }
            }
        },
        series: [
            {
                name: '磁盘使用率',
                type: 'bar',
                data: diskData
            }
        ]
    }
    
    chart.setOption(option)
}

// 格式化文件大小
const formatSize = (bytes: number) => {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 监听数据变化
watch(() => diskStore.diskInfo, (newData) => {
    if (!chart) {
        initChart()
        return
    }
    
    if (newData) {
        const diskData = newData.disks.map((disk: any) => ({
            name: disk.mountpoint,
            value: disk.percent,
            total: formatSize(disk.total),
            used: formatSize(disk.used),
            free: formatSize(disk.free)
        }))
        
        chart.setOption({
            yAxis: {
                data: diskData.map((item: any) => item.name)
            },
            series: [
                {
                    data: diskData
                }
            ]
        })
    }
}, { deep: true })

// 生命周期钩子
onMounted(() => {
    diskStore.startAutoUpdate(10000) // 启动自动更新，磁盘信息可以更新得慢一些
    // 监听窗口大小变化
    window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
    diskStore.stopAutoUpdate() // 停止自动更新
    chart?.dispose()
    window.removeEventListener('resize', () => chart?.resize())
})
</script>

<style scoped>
.disk-chart {
    width: 100%;
    margin-bottom: 1rem;
}
</style> 