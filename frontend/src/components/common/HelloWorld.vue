<script setup lang="ts">
import { ref } from 'vue'

defineProps<{ msg: string }>()

const count = ref(0)
</script>

<template>
  <div class="u-p-6 u-max-w-md u-mx-auto">
    <el-card class="u-shadow-md">
      <template #header>
        <h1 class="u-text-2xl u-font-bold u-text-center u-text-primary">{{ msg }}</h1>
      </template>

      <div class="u-space-y-4">
        <el-card class="u-bg-gray-50">
          <el-button type="primary" @click="count++"> count is {{ count }} </el-button>
          <p class="u-mt-2 u-text-sm u-text-gray-600">
            Edit
            <el-tag size="small" type="info">components/HelloWorld.vue</el-tag>
            to test HMR
          </p>
        </el-card>

        <div class="u-space-y-2">
          <p class="u-text-sm">
            Check out
            <el-link href="https://vuejs.org/guide/quick-start.html#local" target="_blank" type="primary"> create-vue </el-link>
            , the official Vue + Vite starter
          </p>
          <p class="u-text-sm">
            Install
            <el-link href="https://github.com/johnsoncodehk/volar" target="_blank" type="primary"> Volar </el-link>
            in your IDE for a better DX
          </p>
          <p class="u-text-xs u-text-gray-500 u-text-center">Click on the Vite and Vue logos to learn more</p>
        </div>
      </div>
    </el-card>
  </div>
</template>
