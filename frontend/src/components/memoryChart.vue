<template>
    <q-card class="memory-chart">
        <q-card-section>
            <div class="text-h6">内存使用率</div>
            <!-- 加载状态 -->
            <div v-if="memoryStore.loading" class="flex flex-center" style="height: 300px">
                <q-spinner-dots size="40px" color="primary" />
                <span class="q-ml-sm">加载中...</span>
            </div>
            
            <!-- 错误状态 -->
            <div v-else-if="memoryStore.error" class="flex flex-center" style="height: 300px">
                <q-banner class="bg-negative text-white">
                    {{ memoryStore.error }}
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
import { useMemoryStore } from '../stores/hardwareStores'

const memoryStore = useMemoryStore()

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
    if (!chartRef.value || !memoryStore.memoryInfo) return
    
    chart = echarts.init(chartRef.value)
    
    // 创建内存使用率饼图
    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,
            data: ['已使用', '可用']
        },
        series: [
            {
                name: '内存状态',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '18',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: [
                    { value: memoryStore.memoryInfo.memory_percent, name: '已使用' },
                    { value: 100 - memoryStore.memoryInfo.memory_percent, name: '可用' }
                ]
            }
        ]
    }
    
    chart.setOption(option)
}

// 监听数据变化
watch(() => memoryStore.memoryInfo, (newData) => {
    if (!chart) {
        initChart()
        return
    }
    
    if (newData) {
        chart.setOption({
            series: [
                {
                    data: [
                        { value: newData.memory_percent, name: '已使用' },
                        { value: 100 - newData.memory_percent, name: '可用' }
                    ]
                }
            ]
        })
    }
}, { deep: true })

// 生命周期钩子
onMounted(() => {
    memoryStore.startAutoUpdate(3000) // 启动自动更新
    // 监听窗口大小变化
    window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
    memoryStore.stopAutoUpdate() // 停止自动更新
    chart?.dispose()
    window.removeEventListener('resize', () => chart?.resize())
})
</script>

<style scoped>
.memory-chart {
    width: 100%;
    margin-bottom: 1rem;
}
</style>