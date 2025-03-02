<template>
    <q-card class="cpu-chart">
        <q-card-section>
            <div class="text-h6">CPU 使用率</div>
            <!-- 加载状态 -->
            <div v-if="cpuStore.loading" class="flex flex-center" style="height: 300px">
                <q-spinner-dots size="40px" color="primary" />
                <span class="q-ml-sm">加载中...</span>
            </div>
            
            <!-- 错误状态 -->
            <div v-else-if="cpuStore.error" class="flex flex-center" style="height: 300px">
                <q-banner class="bg-negative text-white">
                    {{ cpuStore.error }}
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
import { useCpuStore } from '../stores/hardwareStores'

const cpuStore = useCpuStore()

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
    if (!chartRef.value || !cpuStore.cpuInfo) return
    
    chart = echarts.init(chartRef.value)
    
    // 准备雷达图数据
    const cpuData = cpuStore.cpuInfo.cpu_per_core || []
    
    const option = {
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            data: cpuData.map((_, index) => `核心 ${index}`)
        },
        yAxis: {
            type: 'value',
            max: 100,
            name: '使用率 (%)'
        },
        series: [{
            data: cpuData,
            type: 'bar',
            name: 'CPU使用率'
        }]
    }
    
    chart.setOption(option)
}

// 监听数据变化
watch(() => cpuStore.cpuInfo, (newData) => {
    if (!chart) {
        initChart()
        return
    }
    
    if (newData) {
        const cpuData = newData.cpu_per_core || []
        chart.setOption({
            xAxis: {
                data: cpuData.map((_, index) => `核心 ${index}`)
            },
            series: [{
                data: cpuData
            }]
        })
    }
}, { deep: true })

// 生命周期钩子
onMounted(() => {
    cpuStore.startAutoUpdate(3000)
    initChart()
    // 监听窗口大小变化
    window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
    cpuStore.stopAutoUpdate()
    chart?.dispose()
    window.removeEventListener('resize', () => chart?.resize())
})
</script>

<style scoped>
.cpu-chart {
    width: 100%;
    margin-bottom: 1rem;
}
</style>