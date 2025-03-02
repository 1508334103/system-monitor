<template>
  <q-layout view="hHh lpR fFf">
      <q-header elevated class="bg-primary text-white">
          <q-toolbar>
              <q-toolbar-title>
                  系统资源监控平台
              </q-toolbar-title>
          </q-toolbar>
      </q-header>
      <q-page-container>
          <div class="q-pa-md">
              <!-- 数据展示 -->
              <div class="column q-col-gutter-md full-width">
                  <div class="col-12 full-width">
                      <CpuChart />
                  </div>
                  <div class="col-12 full-width">
                      <MemoryChart />
                  </div>
                  <div class="col-12 full-width">
                      <DiskChart />
                  </div>
                  <div class="col-12 full-width">
                      <NetworkChart />
                  </div>
              </div>
          </div>
      </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import CpuChart from './components/CpuChart.vue'
import MemoryChart from './components/memoryChart.vue'
import DiskChart from './components/diskChart.vue'
import NetworkChart from './components/networkChart.vue'
</script>