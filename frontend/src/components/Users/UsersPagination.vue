<!-- src/components/Users/UsersPagination.vue -->
<template>
  <el-pagination
    :total="totalNum"
    :page-size="perPageNum"
    :current-page="currentPageNum"
    layout="prev, pager, next"
    @update:current-page="emit('page-change', $event)"
    class="u-my-4 u-flex u-justify-center"
  >
    <template #prev>
      <i-mdi-chevron-left class="u-text-lg" />
    </template>
    <template #next>
      <i-mdi-chevron-right class="u-text-lg" />
    </template>
  </el-pagination>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  total: number
  perPage: number
  currentPage: number
}>()

const emit = defineEmits<{
  (e: 'page-change', page: number): void
}>()

// Sécurisation numérique
const totalNum = computed(() => Number(props.total) || 0)
const perPageNum = computed(() => Number(props.perPage) || 10)
const currentPageNum = computed(() => Number(props.currentPage) || 1)
</script>
