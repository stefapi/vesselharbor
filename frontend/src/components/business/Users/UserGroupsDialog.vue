<!-- src/components/Users/UserGroupsDialog.vue -->
<template>
  <el-dialog :model-value="visible" :title="dialogTitle" width="600px" @update:model-value="onDialogUpdate">
    <UserGroupsManager :userId="user?.id" :environmentId="null" />
  </el-dialog>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import UserGroupsManager from '@/components/business/Users/UserGroupsManager.vue'

const props = defineProps<{
  visible: boolean // ← reste en lecture seule
  user: any | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const dialogTitle = computed(() => (props.user ? `Gestion des Groupes pour ${props.user.email}` : 'Gestion des Groupes'))

/** Lorsque l’utilisateur ferme la boîte : on relaie vers le parent */
function onDialogUpdate(val: boolean) {
  if (!val) emit('close')
}
</script>
