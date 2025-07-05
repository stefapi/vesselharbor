<template>
  <el-dialog :model-value="modelValue" title="Ajouter un groupe" width="500px" @update:model-value="emit('update:modelValue', $event)">
    <el-form>
      <el-form-item label="Groupe">
        <el-select v-model="selectedGroupLocal" placeholder="Sélectionner un groupe" style="width: 100%" clearable>
          <el-option v-for="group in availableGroups" :key="group.id" :label="group.name + (group.environment_name ? ` (${group.environment_name})` : ' (Global)')" :value="group.id" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog">Annuler</el-button>
        <el-button type="primary" @click="addGroup" :disabled="!selectedGroupLocal"> Ajouter </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: boolean
  availableGroups: any[]
  selectedGroup: number | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
  (e: 'update:selectedGroup', value: number | null): void
  (e: 'addGroup'): void
}>()

const selectedGroupLocal = ref<number | undefined>(props.selectedGroup || undefined)

// Watch for changes in the selectedGroup prop
watch(
  () => props.selectedGroup,
  (newValue) => {
    selectedGroupLocal.value = newValue || undefined
  }
)

// Watch for changes in the local selectedGroup and emit update
watch(selectedGroupLocal, (newValue) => {
  emit('update:selectedGroup', newValue || null)
})

const closeDialog = () => {
  emit('update:modelValue', false)
}

const addGroup = () => {
  emit('addGroup')
}
</script>
