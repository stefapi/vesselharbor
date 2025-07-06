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
  <div class="vh-form-field" :class="fieldClasses">
    <label v-if="label" :for="fieldId" class="vh-form-field__label">
      {{ label }}
      <span v-if="required" class="vh-form-field__required">*</span>
    </label>

    <div class="vh-form-field__input-wrapper">
      <slot :fieldId="fieldId" :hasError="hasError" />
    </div>

    <div v-if="hasError" class="vh-form-field__error">
      {{ error }}
    </div>

    <div v-else-if="hint" class="vh-form-field__hint">
      {{ hint }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, useId } from 'vue'

interface Props {
  label?: string
  error?: string
  hint?: string
  required?: boolean
  disabled?: boolean
  size?: 'small' | 'default' | 'large'
}

const props = withDefaults(defineProps<Props>(), {
  required: false,
  disabled: false,
  size: 'default'
})

const fieldId = useId()

const hasError = computed(() => Boolean(props.error))

const fieldClasses = computed(() => [
  `vh-form-field--${props.size}`,
  {
    'vh-form-field--error': hasError.value,
    'vh-form-field--disabled': props.disabled,
    'vh-form-field--required': props.required
  }
])
</script>

<style scoped>
.vh-form-field {
  @apply mb-4;
}

.vh-form-field__label {
  @apply block text-sm font-medium text-gray-700 mb-1;
}

.vh-form-field__required {
  @apply text-red-500 ml-1;
}

.vh-form-field__input-wrapper {
  @apply relative;
}

.vh-form-field__error {
  @apply mt-1 text-sm text-red-600;
}

.vh-form-field__hint {
  @apply mt-1 text-sm text-gray-500;
}

.vh-form-field--small .vh-form-field__label {
  @apply text-xs;
}

.vh-form-field--large .vh-form-field__label {
  @apply text-base;
}

.vh-form-field--error .vh-form-field__label {
  @apply text-red-700;
}

.vh-form-field--disabled {
  @apply opacity-50 pointer-events-none;
}
</style>
