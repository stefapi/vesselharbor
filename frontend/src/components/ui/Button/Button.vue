<!--
  - Copyright (c) 2025.  VesselHarbor
  -
  - ____   ____                          .__    ___ ___             ___.
  - \   \ /   /____   ______ ______ ____ |  |  /   |   \_____ ______\_ |__   ___________
  -  \   Y   // __ \ /  ___//  ___// __ \|  | /    ~    \__  \\_  __ \ __ \ /  _ \_  __ \
  -   \     /\  ___/ \___ \ \___ \\  ___/|  |_\    Y    // __ \|  | \/ \_\ (  <_> )  | \/
  -    \___/  \___  >____  >____  >\___  >____/\___|_  /(____  /__|  |___  /\____/|__|
  -               \/     \/     \/     \/            \/      \/          \/
  -
  -
  - MIT License
  -
  - Permission is hereby granted, free of charge, to any person obtaining a copy
  - of this software and associated documentation files (the "Software"), to deal
  - in the Software without restriction, including without limitation the rights
  - to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  - copies of the Software, and to permit persons to whom the Software is
  - furnished to do so, subject to the following conditions:
  -
  - The above copyright notice and this permission notice shall be included in all
  - copies or substantial portions of the Software.
  -
  - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  - IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  - FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  - AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  - LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  - OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  - SOFTWARE.
  -
  -->

<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    :type="type"
    @click="handleClick"
  >
    <el-icon v-if="loading" class="is-loading">
      <Loading />
    </el-icon>
    <el-icon v-else-if="icon && iconPosition === 'left'">
      <component :is="icon" />
    </el-icon>

    <span v-if="$slots.default" :class="{ 'u-ml-2': icon && iconPosition === 'left', 'u-mr-2': icon && iconPosition === 'right' }">
      <slot />
    </span>

    <el-icon v-if="icon && iconPosition === 'right'">
      <component :is="icon" />
    </el-icon>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Loading } from '@element-plus/icons-vue'

interface Props {
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info'
  size?: 'small' | 'default' | 'large'
  disabled?: boolean
  loading?: boolean
  icon?: any
  iconPosition?: 'left' | 'right'
  block?: boolean
  round?: boolean
  circle?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'primary',
  size: 'default',
  disabled: false,
  loading: false,
  iconPosition: 'left',
  block: false,
  round: false,
  circle: false
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const buttonClasses = computed(() => [
  'vh-button',
  `vh-button--${props.variant}`,
  `vh-button--${props.size}`,
  {
    'vh-button--disabled': props.disabled,
    'vh-button--loading': props.loading,
    'vh-button--block': props.block,
    'vh-button--round': props.round,
    'vh-button--circle': props.circle,
  }
])

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<style scoped>
.vh-button {
  @apply inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md border transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.vh-button--primary {
  @apply bg-blue-600 border-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500;
}

.vh-button--secondary {
  @apply bg-gray-600 border-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500;
}

.vh-button--success {
  @apply bg-green-600 border-green-600 text-white hover:bg-green-700 focus:ring-green-500;
}

.vh-button--warning {
  @apply bg-yellow-600 border-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500;
}

.vh-button--danger {
  @apply bg-red-600 border-red-600 text-white hover:bg-red-700 focus:ring-red-500;
}

.vh-button--info {
  @apply bg-blue-500 border-blue-500 text-white hover:bg-blue-600 focus:ring-blue-400;
}

.vh-button--small {
  @apply px-3 py-1.5 text-xs;
}

.vh-button--large {
  @apply px-6 py-3 text-base;
}

.vh-button--disabled {
  @apply opacity-50 cursor-not-allowed;
}

.vh-button--loading {
  @apply cursor-wait;
}

.vh-button--block {
  @apply w-full;
}

.vh-button--round {
  @apply rounded-full;
}

.vh-button--circle {
  @apply rounded-full w-10 h-10 p-0;
}

.is-loading {
  @apply animate-spin;
}
</style>
