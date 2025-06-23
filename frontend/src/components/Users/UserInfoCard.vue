<template>
  <el-card class="u-mb-4">
    <template #header>
      <div class="u-flex u-items-center u-justify-between">
        <h2 class="u-text-lg u-font-bold">Informations utilisateur</h2>
      </div>
    </template>
    <div v-if="user">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ user.id }}</el-descriptions-item>
        <el-descriptions-item label="Email">{{ user.email }}</el-descriptions-item>
        <el-descriptions-item label="Superadmin">
          <el-tag :type="user.is_superadmin ? 'success' : 'info'">
            {{ user.is_superadmin ? 'Oui' : 'Non' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    <div v-else class="u-text-center u-py-4">
      <el-skeleton :rows="3" animated />
    </div>
  </el-card>
</template>

<script setup lang="ts">
defineProps<{
  user: any | null
}>()
</script>
