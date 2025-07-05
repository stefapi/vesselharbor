<!-- src/views/NotFound.vue -->
<template>
  <el-container class="u-min-h-screen u-flex u-flex-col u-items-center u-justify-center u-bg-gray-100 u-p-4">
    <el-card class="u-text-center u-max-w-md u-w-full">
      <h1 class="u-text-4xl u-font-bold u-mb-4">404 - Page non trouvée</h1>
      <p class="u-mb-6">La page que vous cherchez n'existe pas.</p>
      <router-link to="/">
        <el-button type="primary" plain>
          Retourner à l'accueil
        </el-button>
      </router-link>
    </el-card>
  </el-container>
</template>

<script lang="ts" setup>
defineOptions({ name: 'NotFound' });
</script>
