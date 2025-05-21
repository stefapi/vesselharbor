<template>
  <el-table :data="users" stripe border class="u-rounded-xl u-shadow-sm" style="width: 100%">
    <el-table-column prop="id" label="ID" width="80" />
    <el-table-column prop="email" label="Email">
      <template #default="{ row }">
        <router-link :to="`/users/${row.id}`" class="u-text-blue-500 hover:u-underline">
          {{ row.email }}
        </router-link>
      </template>
    </el-table-column>

    <!-- Nombre de groupes -->
    <el-table-column label="Groupes" width="100" align="center">
      <template #default="{ row }">
        <el-tag type="info" v-if="row.user_assignments && row.user_assignments.length">
          {{ row.user_assignments.length }}
        </el-tag>
        <span v-else>-</span>
      </template>
    </el-table-column>

    <!-- Date de création (si disponible) -->
    <el-table-column label="Créé le" width="150" v-if="hasCreatedDate">
      <template #default="{ row }">
        {{ row.created_at ? new Date(row.created_at).toLocaleDateString() : '-' }}
      </template>
    </el-table-column>

    <!-- Superadmin : visible seulement si l'utilisateur courant est superadmin -->
    <el-table-column
      v-if="isSuperadmin"
      prop="is_superadmin"
      label="Superadmin"
      width="120"
    >
      <template #default="{ row }">
        <el-tag :type="row.is_superadmin ? 'success' : 'info'">
          {{ row.is_superadmin ? 'Oui' : 'Non' }}
        </el-tag>
      </template>
    </el-table-column>

    <el-table-column label="Actions" width="80" align="center">
      <template #default="{ row }">
        <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, row)">
          <el-button text icon>
            <i-mdi-dots-vertical class="u-text-xl" />
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="edit">
                <i-mdi-pencil class="u-mr-1" /> Modifier
              </el-dropdown-item>

              <!-- Supprimer : visible uniquement pour superadmin -->
              <el-dropdown-item
                v-if="isSuperadmin"
                command="delete"
              >
                <i-mdi-delete class="u-mr-1" /> Supprimer
              </el-dropdown-item>

              <el-dropdown-item command="groups">
                <i-mdi-account-group class="u-mr-1" /> Groupes
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const isSuperadmin = computed(() => authStore.user?.is_superadmin === true)
const hasCreatedDate = computed(() => props.users.some(user => user.created_at))

const props = defineProps<{
  users: Array<{
    id: number
    email: string
    is_superadmin: boolean
    created_at?: string
    user_assignments?: Array<any>
  }>
}>()

const emit = defineEmits<{
  (e: 'edit', user: typeof props.users[number]): void
  (e: 'delete', id: number): void
  (e: 'manage-groups', user: typeof props.users[number]): void
}>()

function handleCommand(command: string, row: typeof props.users[number]) {
  if (command === 'edit') emit('edit', row)
  if (command === 'delete') emit('delete', row.id)
  if (command === 'groups') emit('manage-groups', row)
}
</script>
