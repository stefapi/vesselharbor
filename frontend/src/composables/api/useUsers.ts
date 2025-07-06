/*
 * Copyright (c) 2025.  VesselHarbor
 *
 * ____   ____                          .__    ___ ___             ___.
 * \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
 *  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
 *   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
 *    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
 *               \/     \/     \/     \/            \/      \/          \/
 *
 *
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

import { ref, computed, readonly } from 'vue'
import { useAsyncState } from '@vueuse/core'
import { listusers, createauser, createauserinfreemode, updateuserinformation, deleteauser } from '@/api'
import type { User, UserCreate, UserUpdate } from '@/api/types'

export function useUsers() {
  const users = ref<User[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { execute: fetchUsers, isLoading: isFetching } = useAsyncState(
    async () => {
      const response = await listusers()
      users.value = Array.isArray(response.data) ? response.data : []
      return users.value
    },
    [],
    { immediate: false }
  )

  const createUser = async (userData: UserCreate, organizationId?: number) => {
    loading.value = true
    try {
      const response = organizationId
        ? await createauser(organizationId, userData)
        : await createauserinfreemode(userData)
      const usersList = Array.isArray(users.value) ? users.value : []
      usersList.push(response.data)
      users.value = usersList
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la création'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (id: number, userData: UserUpdate) => {
    loading.value = true
    try {
      const response = await updateuserinformation(id, userData)
      const usersList = Array.isArray(users.value) ? users.value : []
      const index = usersList.findIndex(u => u.id === id)
      if (index !== -1) {
        usersList[index] = response.data
        users.value = usersList
      }
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la mise à jour'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteUser = async (id: number) => {
    loading.value = true
    try {
      await deleteauser(id)
      const usersList = Array.isArray(users.value) ? users.value : []
      users.value = usersList.filter(u => u.id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression'
      throw err
    } finally {
      loading.value = false
    }
  }

  const activeUsers = computed(() => {
    const usersList = Array.isArray(users.value) ? users.value : []
    return usersList.filter(u => u.isActive)
  })
  const userCount = computed(() => {
    const usersList = Array.isArray(users.value) ? users.value : []
    return usersList.length
  })

  return {
    // State
    users: readonly(users),
    loading: readonly(loading),
    error: readonly(error),
    isFetching,

    // Computed
    activeUsers,
    userCount,

    // Actions
    fetchUsers,
    createUser,
    updateUser,
    deleteUser,

    // Utils
    clearError: () => { error.value = null }
  }
}
