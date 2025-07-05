<template>
  <el-card>
    <template #header>
      <div class="u-flex u-items-center u-justify-between">
        <h2 class="u-text-lg u-font-bold">Groupes</h2>
        <el-button type="primary" size="small" @click="$emit('showAddGroupDialog')"> Ajouter un groupe </el-button>
      </div>
    </template>
    <div v-if="userGroups.length > 0">
      <el-table :data="userGroups" style="width: 100%">
        <el-table-column prop="name" label="Nom du groupe" />
        <el-table-column prop="environment_name" label="Environnement">
          <template #default="{ row }">
            {{ row.environment_name || 'Global' }}
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="100" align="center">
          <template #default="{ row }">
            <el-button type="danger" size="small" @click="$emit('removeGroup', row.id)">
              <i-mdi-delete />
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div v-else class="u-text-center u-py-4">
      <p>Aucun groupe assigné à cet utilisateur.</p>
    </div>
  </el-card>
</template>

<script setup lang="ts">
defineProps<{
  userGroups: any[]
}>()

defineEmits<{
  (e: 'showAddGroupDialog'): void
  (e: 'removeGroup', groupId: number): void
}>()
</script>
