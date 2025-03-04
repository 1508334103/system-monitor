import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import CpuView from '../views/CpuView.vue'
import MemoryView from '../views/MemoryView.vue'
import DiskView from '../views/DiskView.vue'
import NetworkView from '../views/NetworkView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/cpu',
      name: 'cpu',
      component: CpuView
    },
    {
      path: '/memory',
      name: 'memory',
      component: MemoryView
    },
    {
      path: '/disk',
      name: 'disk',
      component: DiskView
    },
    {
      path: '/network',
      name: 'network',
      component: NetworkView
    }
  ]
})

export default router 