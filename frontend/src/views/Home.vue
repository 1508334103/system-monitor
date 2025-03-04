<template>
  <div class="q-pa-md">
    <BreadcrumbNav />
    <div class="row q-col-gutter-md">
      <div class="col-12 col-sm-6 col-md-3" v-for="item in menuItems" :key="item.path">
        <q-card
          class="menu-card cursor-pointer"
          v-ripple
          @click="router.push(item.path)"
        >
          <q-card-section class="text-center">
            <q-icon :name="item.icon" size="4rem" :color="item.color" />
            <div class="text-h6 q-mt-sm">{{ item.title }}</div>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import BreadcrumbNav from '../components/BreadcrumbNav.vue'

const router = useRouter()

const menuItems = [
  { path: '/cpu', title: 'CPU Monitor', icon: 'mdi-cpu-64-bit', color: 'primary' },
  { path: '/memory', title: 'Memory Monitor', icon: 'mdi-memory', color: 'secondary' },
  { path: '/disk', title: 'Disk Monitor', icon: 'mdi-harddisk', color: 'accent' },
  { path: '/network', title: 'Network Monitor', icon: 'mdi-network', color: 'info' }
]
</script>

<style scoped>
.menu-card {
  transition: transform 0.2s;
}

.menu-card:hover {
  transform: translateY(-5px);
}
</style> 