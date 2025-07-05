// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
// @ts-ignore
import { routes as autoRoutes } from 'vue-router/auto-routes'
import type { RouteRecordRaw } from 'vue-router'
import LoginView from '@/views/Auth/LoginView.vue'
import ForgotPasswordView from '@/views/Auth/ForgotPasswordView.vue'
import ResetPasswordView from '@/views/Auth/ResetPasswordView.vue'
import DashboardView from '@/views/Dashboard/DashboardView.vue'
import AccountView from '@/views/Users/AccountView.vue'
import EnvironmentElementsView from '@/views/Environments/EnvironmentElementsView.vue'
import EnvironmentManagementView from '@/views/Environments/EnvironmentManagementView.vue'
import EnvironmentUsersView from '@/views/Users/EnvironmentUsersView.vue'
import UsersView from '@/views/Users/UsersView.vue'
import UserView from '@/views/Users/UserView.vue'
import { useAuthStore } from '@/store/auth.ts'
import NProgress from 'nprogress'

const manualRoutes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: LoginView, meta: { layout: 'auth' } },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPasswordView, meta: { layout: 'auth' } },
  { path: '/reset-password', name: 'ResetPassword', component: ResetPasswordView, meta: { layout: 'auth' } },
  { path: '/', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  { path: '/account', name: 'Account', component: AccountView, meta: { requiresAuth: true, requiredRole: 'self' } },
  { path: '/environment/:envId/elements', name: 'EnvironmentElements', component: EnvironmentElementsView, meta: { requiresAuth: true } },
  { path: '/environment/:envId/manage', name: 'EnvironmentManagement', component: EnvironmentManagementView, meta: { requiresAuth: true, requiredRole: 'envAdmin' } },
  { path: '/environment/:envId/users', name: 'EnvironmentUsers', component: EnvironmentUsersView, meta: { requiresAuth: true, requiredRole: 'envAdmin' } },
  { path: '/users', name: 'Users', component: UsersView, meta: { requiresAuth: true, requiredRole: 'superadmin' } },
  { path: '/users/:id', name: 'UserView', component: UserView, meta: { requiresAuth: true, requiredRole: 'superadmin' } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') },
]

// Fusion des routes manuelles et auto
const routes: RouteRecordRaw[] = [
  ...manualRoutes,
  ...autoRoutes, // routes définies dans src/pages
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const publicPages = ['Login', 'ForgotPassword', 'ResetPassword', '?uno']
  const loginPages = ['Login', 'ForgotPassword', 'ResetPassword']
  NProgress.start()
  function proceed() {
    if (authStore.isAuthenticated && loginPages.includes(to.name as string)) {
      return next({ name: 'Dashboard' })
    }
    if (!authStore.isAuthenticated && !publicPages.includes(to.name as string)) {
      return next({ name: 'Login' })
    } else if (to.meta.requiredRole) {
      const role = to.meta.requiredRole
      if (role === 'superadmin' && !authStore.user?.is_superadmin) {
        return next({ name: 'Account' })
      } else if (role === 'envAdmin') {
        const envId = Number(to.params.envId)
        if (!authStore.isEnvironmentAdmin(envId)) {
          return next({ name: 'Account' })
        }
      }
    }

    next()
  }
  // Attendre l'initialisation complète du store
  if (!authStore.isInitialized) {
    authStore
      .initialize()
      .then(() => {
        // Une fois initialisé, vérifiez l'authentification et les rôles
        proceed()
      })
      .catch(() => {
        // En cas d'erreur lors de l'initialisation, rediriger vers Login
        authStore.logout()
        next({ name: 'Login' })
      })
  } else {
    // Définition des routes publiques qui ne nécessitent pas d'être authentifié
    proceed()
  }
})

router.afterEach(() => {
  NProgress.done()
})
export default router
