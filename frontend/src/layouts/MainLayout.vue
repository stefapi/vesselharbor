<!-- src/layouts/MainLayout.vue -->
<script src="../../vite.config.ts"></script>
<template>
  <VaLayout style="height: 500px">
    <template #top>
      <VaNavbar v-if="isAuthenticated" color="background-primary" >
        <template #left>
          <VaButton class="mr-5" :icon="showSidebar ? 'menu_open' : 'menu'" @click="showSidebar = !showSidebar" />
          <VaNavbarItem  class=" text-xl font-semibold"> Mon Application </VaNavbarItem>
        </template>
        <template #center>
          <VaNavbarItem class="font-bold text-lg"> LOGO </VaNavbarItem>
        </template>
        <template #right>
      <VaDropdown>
        <template #anchor>
          <VaButton preset="secondary">
            <VaIcon name="account_circle" class="mr-2" />
          </VaButton>
        </template>

        <VaDropdownContent class="p-2 min-w-400px overflow-visible">
          <div v-for="(item, index) in menuItems" :key="index">
            <VaButton
              v-if="!item.action"
              preset="secundary"
               size="small"
              color="backgroundSecondary"
              :to="item.path"
              class="px-4 py-2 whitespace-nowrap gap-2"
            >
              <VaIcon :name="item.icon" class="mr-2" />
              {{ item.name }}
            </VaButton>

            <VaButton
              v-else
              preset="secundary"
               size="small"
              color="backgroundSecondary"
              class="px-4 py-2 whitespace-nowrap"
              @click="item.action"
            >
              <VaIcon :name="item.icon" class="mr-2" />
              {{ item.name }}
            </VaButton>
          </div>
        </VaDropdownContent>
      </VaDropdown>
        </template>
      </VaNavbar>
    </template>
    <template #left >
      <VaSidebar v-if="isAuthenticated"  :hoverable="!showSidebar" >
        <VaSidebarItem v-for="(route, index) in filteredRoutes" :key="index" :to="route.path" active-class="bg-primary-dark">
          <VaSidebarItemContent class="gap-3">
            <VaIcon :name="route.icon" />
            <VaSidebarItemTitle class="whitespace-nowrap">
              {{ route.name }}
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
      </VaSidebar>
    </template>
    <template #content  >
      <router-view />
    </template>
  </VaLayout>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const router = useRouter()

const showSidebar = ref(false)

const logout = () => {
  authStore.logout()
  router.push({ name: 'Login' })
}

const routes = [
  { path: '/', name: 'Dashboard', icon: 'dashboard' },
  { path: '/environments', name: 'Environnements', icon: 'landscape' },
  { path: '/groups', name: 'Groupes & Utilisateurs', icon: 'people' },
  { path: '/elements', name: 'Éléments', icon: 'widgets' },
  {
    path: '/audit-logs',
    name: 'Audit Logs',
    icon: 'assignment',
    requiresSuperadmin: true,
  },
]

const menuItems = ref([
  { name: 'Utilisateurs', icon: 'people', path: '/users' },
  { name: 'Groupes', icon: 'group', path: '/groups' },
  { name: 'Policy', icon: 'policy', path: '/policy' },
  { name: 'Clés API', icon: 'vpn_key', path: '/api-keys' },
  { name: 'Clés SSH', icon: 'key', path: '/ssh-keys' },
  { name: 'Ressources matériel', icon: 'computer', path: '/hardware' },
  { name: 'Déconnexion', icon: 'power_settings_new', action: logout }
])

const isAuthenticated = computed(() => authStore.isAuthenticated)
const isSuperadmin = computed(() => authStore.user?.is_superadmin)

const filteredRoutes = computed(() => routes.filter((route) => !route.requiresSuperadmin || (route.requiresSuperadmin && isSuperadmin.value)))

</script>
