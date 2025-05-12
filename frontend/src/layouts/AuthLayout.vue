<!-- src/layouts/AuthLayout.vue -->
<template>
  <!-- conteneur plein écran qui centre son contenu -->
  <el-container
    class=" u-flex u-items-center u-justify-center u-bg-white dark:u-bg-gray-900 u-w-full  u-mx-auto"
  >
    <!-- le contenu de la vue s’affiche ici -->
    <slot />
  </el-container>
</template>

<script setup lang="ts">
/* aucun script nécessaire pour l’instant */
</script>
