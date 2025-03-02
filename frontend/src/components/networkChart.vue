<template>
    <q-card class="network-chart">
        <q-card-section>
            <div class="text-h6">网络流量</div>
            <!-- 加载状态 -->
            <div v-if="networkStore.loading" class="flex flex-center" style="height: 300px">
                <q-spinner-dots size="40px" color="primary" />
                <span class="q-ml-sm">加载中...</span>
            </div>
            
            <!-- 错误状态 -->
            <div v-else-if="networkStore.error" class="flex flex-center" style="height: 300px">
                <q-banner class="bg-negative text-white">
                    {{ networkStore.error }}
                </q-banner>
            </div>
            <!-- 图表 -->
            <div v-else ref="chartRef" style="height: 300px"></div>
        </q-card-section>
    </q-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, reactive } from 'vue'
import * as echarts from 'echarts'
import { useNetworkStore } from '../stores/hardwareStores'

const networkStore = useNetworkStore()

const chartRef = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

// 保存历史数据
const historyData = reactive({
    timestamps: [] as number[],
    sent: [] as number[],
    received: [] as number[],
    lastSent: 0,
    lastReceived: 0
})

// 最大保存的数据点数量
const MAX_DATA_POINTS = 20

// 格式化网络流量
const formatNetworkTraffic = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B/s';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB/s';
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB/s';
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB/s';
}

// 初始化图表
const initChart = () => {
    if (!chartRef.value) return
    
    chart = echarts.init(chartRef.value)
    
    const option = {
        tooltip: {
            trigger: 'axis',
            formatter: function(params: any) {
                let result = params[0].axisValue + '<br/>';
                params.forEach((param: any) => {
                    result += param.marker + param.seriesName + ': ' + 
                              formatNetworkTraffic(param.value) + '<br/>';
                });
                return result;
            }
        },
        legend: {
            data: ['发送', '接收']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: historyData.timestamps.map((t: number) => new Date(t).toLocaleTimeString())
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: function(value: number) {
                    return formatNetworkTraffic(value);
                }
            }
        },
        series: [
            {
                name: '发送',
                type: 'line',
                data: historyData.sent,
                areaStyle: {
                    opacity: 0.3
                },
                lineStyle: {
                    width: 2
                },
                symbol: 'none'
            },
            {
                name: '接收',
                type: 'line',
                data: historyData.received,
                areaStyle: {
                    opacity: 0.3
                },
                lineStyle: {
                    width: 2
                },
                symbol: 'none'
            }
        ]
    }
    
    chart.setOption(option)
}

// 更新历史数据
const updateHistoryData = (newData: any) => {
    if (!newData) return;
    
    const now = Date.now();
    
    // 计算速率（字节/秒）
    let sentRate = 0;
    let receivedRate = 0;
    
    if (historyData.lastSent > 0 && historyData.timestamps.length > 0) {
        const timeDiff = (now - historyData.timestamps[historyData.timestamps.length - 1]) / 1000;
        sentRate = (newData.bytes_sent - historyData.lastSent) / timeDiff;
        receivedRate = (newData.bytes_recv - historyData.lastReceived) / timeDiff;
    }
    
    // 只有当有上一次数据时才添加新数据点
    if (historyData.lastSent > 0) {
        historyData.timestamps.push(now);
        historyData.sent.push(sentRate);
        historyData.received.push(receivedRate);
        
        // 限制数据点数量
        if (historyData.timestamps.length > MAX_DATA_POINTS) {
            historyData.timestamps.shift();
            historyData.sent.shift();
            historyData.received.shift();
        }
    }
    
    // 更新最后的值
    historyData.lastSent = newData.bytes_sent;
    historyData.lastReceived = newData.bytes_recv;
}

// 监听数据变化
watch(() => networkStore.networkInfo, (newData) => {
    if (newData) {
        updateHistoryData(newData);
    }
    
    if (!chart) {
        initChart();
        return;
    }
    
    chart.setOption({
        xAxis: {
            data: historyData.timestamps.map((t: number) => new Date(t).toLocaleTimeString())
        },
        series: [
            {
                data: historyData.sent
            },
            {
                data: historyData.received
            }
        ]
    });
}, { deep: true })

// 生命周期钩子
onMounted(() => {
    networkStore.startAutoUpdate(2000) // 启动自动更新，网络信息可以更新得更频繁
    initChart()
    // 监听窗口大小变化
    window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
    networkStore.stopAutoUpdate() // 停止自动更新
    chart?.dispose()
    window.removeEventListener('resize', () => chart?.resize())
})
</script>

<style scoped>
.network-chart {
    width: 100%;
    margin-bottom: 1rem;
}
</style> 