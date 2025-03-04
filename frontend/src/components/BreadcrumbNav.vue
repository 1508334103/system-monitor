<template>
  <q-breadcrumbs class="q-mb-md">
    <q-breadcrumbs-el icon="home" to="/" />
    <q-breadcrumbs-el v-if="currentPath" :label="currentPath" />
  </q-breadcrumbs>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentPath = computed(() => {
  const path = route.path.slice(1) // 移除开头的 /
  return path.charAt(0).toUpperCase() + path.slice(1) // 首字母大写
})
</script> 