<template>
  <div class="u-w-full u-flex u-flex-wrap u-items-center u-justify-between u-gap-4 u-mb-4">
    <!-- Champ de recherche -->
    <el-input v-model="model" placeholder="Rechercher par email" clearable class="u-flex-1 u-min-w-[220px]" @input="emit('filter', model)">
      <template #prefix>
        <i-mdi-magnify class="u-text-xl u-text-gray-500" />
      </template>
    </el-input>

    <!-- Bouton -->
    <el-button type="primary" @click="emit('toggle-form')" class="u-whitespace-nowrap">
      <i-mdi-plus class="u-text-xl u-mr-1" />
      {{ isFormOpen ? 'Annuler' : 'Créer un utilisateur' }}
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  filterEmail: string
  isFormOpen: boolean
}>()

const emit = defineEmits<{
  (e: 'filter', value: string): void
  (e: 'toggle-form'): void
}>()

const model = ref(props.filterEmail)

watch(
  () => props.filterEmail,
  (v) => {
    model.value = v
  }
)
</script>
