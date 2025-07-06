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
import { getUsersService, createUserService, updateUserService, deleteUserService } from '@/services'
import type { User, CreateUserInput, UpdateUserInput } from '@/types'

export function useUsers() {
  const users = ref<User[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const { execute: fetchUsers, isLoading: isFetching } = useAsyncState(
    async () => {
      const response = await getUsersService()
      users.value = response.data
      return response.data
    },
    [],
    { immediate: false }
  )

  const createUser = async (userData: CreateUserInput) => {
    loading.value = true
    try {
      const response = await createUserService(userData)
      users.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la création'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (id: number, userData: UpdateUserInput) => {
    loading.value = true
    try {
      const response = await updateUserService(id, userData)
      const index = users.value.findIndex(u => u.id === id)
      if (index !== -1) {
        users.value[index] = response.data
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
      await deleteUserService(id)
      users.value = users.value.filter(u => u.id !== id)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Erreur lors de la suppression'
      throw err
    } finally {
      loading.value = false
    }
  }

  const activeUsers = computed(() => users.value.filter(u => u.isActive))
  const userCount = computed(() => users.value.length)

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
