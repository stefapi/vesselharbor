<template>
  <el-drawer
    :model-value="visible"
    :title="editingUser ? 'Modifier l\'utilisateur' : 'Créer un utilisateur'"
    size="50%"
    @close="emit('close')"
  >
    <UserForm
      :mode="editingUser ? 'edit' : 'create'"
      :initialData="editingUser"
      @success="emit('success')"
    />
  </el-drawer>
</template>

<script setup lang="ts">
import UserForm from '@/components/UserForm.vue';
defineProps<{ visible: boolean; editingUser: any | null }>();
const emit = defineEmits(['close', 'success']);
</script>
