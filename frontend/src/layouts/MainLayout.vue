<template>
  <el-container class="u-bg-white dark:u-bg-gray-900 u-flex u-flex-col">
    <!-- NAVBAR -->
    <el-header v-if="isAuthenticated" class="u-bg-primary u-text-white u-h-16 u-px-4 u-flex u-items-center u-justify-between">
      <div class="u-flex u-items-center">
        <el-button @click="toggleSidebar" circle link class="u-flex u-items-center u-justify-center">
          <template v-if="isSidebarCollapsed">
            <i-material-symbols-menu class="u-text-2xl u-text-white" />
          </template>
          <template v-else>
            <i-material-symbols-menu-open class="u-text-2xl u-text-white" />
          </template>
        </el-button>
        <span class="u-text-lg u-font-semibold u-ml-2">Mon App</span>
      </div>

      <el-dropdown>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item v-for="(item, index) in menuItems" :key="index" @click="item.action ? item.action() : $router.push(item.path)">
              <Icon :icon="item.icon.replace(/^i-/, '')" class="u-mr-2" />
              {{ item.name }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
        <el-button link>
          <i-material-symbols-account-circle class="u-text-xl u-text-white" />
        </el-button>
      </el-dropdown>
    </el-header>

    <!-- BODY -->
    <el-container class="u-flex">
      <!-- SIDEBAR -->
      <el-aside
        v-if="isAuthenticated"
        :width="sidebarWidth"
        class="u-transition-all u-duration-300 u-bg-gray-300 dark:u-bg-gray-800 u-border-r u-border-gray-300 dark:u-border-gray-700"
        @mouseenter="onSidebarEnter"
        @mouseleave="onSidebarLeave"
      >
        <el-menu :default-active="$route.path" class="u-h-full">
          <el-menu-item v-for="(route, index) in filteredRoutes" :key="index" :index="route.path" @click="$router.push(route.path)">
            <Icon :icon="route.icon.replace(/^i-/, '')" class="u-text-xl u-mr-1" />
            <template v-if="!isSidebarCollapsed || isSidebarHovered">
              {{ route.name }}
            </template>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- CONTENT -->
      <el-main class="">
        <div class="u-w-full u-max-w-4xl u-mx-auto">
          <slot />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { Icon } from '@iconify/vue'
import { useWindowSize } from '@vueuse/core'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const isSuperadmin = computed(() => authStore.user?.is_superadmin)

const logout = () => {
  authStore.logout()
  router.push({ name: 'Login' })
}

const routes = [
  { path: '/', name: 'Dashboard', icon: 'i-material-symbols:dashboard' },
  { path: '/environments', name: 'Environnements', icon: 'i-mdi:earth' },
  { path: '/groups', name: 'Groupes & Utilisateurs', icon: 'i-mdi:account-group' },
  { path: '/elements', name: 'Éléments', icon: 'i-mdi:cube-outline' },
  { path: '/dns', name: 'DNS', icon: 'i-carbon:network-3' },
  { path: '/domains', name: 'Domaines', icon: 'i-mdi:domain' },
  { path: '/emails', name: 'Mails', icon: 'i-carbon:email' },
  { path: '/databases', name: 'Bases de données', icon: 'i-mdi:database' },
  { path: '/virtual-machines', name: 'Machines virtuelles', icon: 'i-carbon:virtual-machine' },
  {
    path: '/audit-logs',
    name: 'Audit Logs',
    icon: 'i-mdi:file-document-outline',
    requiresSuperadmin: true,
  },
]

const menuItems = ref([
  { name: 'Utilisateurs', icon: 'i-mdi:account', path: '/users' },
  { name: 'Groupes', icon: 'i-mdi:account-group-outline', path: '/groups' },
  { name: 'Policy', icon: 'i-mdi:shield-lock-outline', path: '/policy' },
  { name: 'Clés API', icon: 'i-mdi:key-outline', path: '/api-keys' },
  { name: 'Clés SSH', icon: 'i-mdi:lock-outline', path: '/ssh-keys' },
  { name: 'Ressources matériel', icon: 'i-mdi:monitor', path: '/hardware' },
  { name: 'Déconnexion', icon: 'i-mdi:logout', action: logout },
])

const filteredRoutes = computed(() => routes.filter((route) => !route.requiresSuperadmin || isSuperadmin.value))

// 👇 Responsive state
const { width } = useWindowSize()
const userCollapsed = ref(false)
const isSidebarHovered = ref(false)

const isSidebarCollapsed = ref(false)
watchEffect(() => {
  isSidebarCollapsed.value = width.value < 768 ? true : userCollapsed.value
})

// 👇 Width of the sidebar
const sidebarWidth = computed(() => {
  if (!isAuthenticated.value) return '0'
  if (isSidebarCollapsed.value && !isSidebarHovered.value) return '64px'
  return '200px'
})

// 👇 Manual toggle via button
const toggleSidebar = () => {
  userCollapsed.value = !userCollapsed.value
  isSidebarCollapsed.value = userCollapsed.value
}

// 👇 Hover behavior
const onSidebarEnter = () => {
  if (isSidebarCollapsed.value) isSidebarHovered.value = true
}
const onSidebarLeave = () => {
  if (isSidebarCollapsed.value) isSidebarHovered.value = false
}
</script>
