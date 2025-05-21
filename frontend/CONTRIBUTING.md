# Contributing to the Frontend

Thank you for your interest in contributing to the frontend of our FastAPI Vue Template project! This document provides guidelines specifically for the Vue.js frontend.

## Development Setup

1. Ensure you have the required prerequisites:
   - Node.js ≥ 20
   - pnpm ≥ 9
   - An IDE with TypeScript support (VS Code recommended)

2. Install dependencies:
   ```bash
   cd frontend
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

## Code Style and Standards

We use a combination of ESLint, Prettier, and Stylelint to maintain code quality:

- **ESLint**: For JavaScript/TypeScript linting
- **Prettier**: For code formatting
- **Stylelint**: For CSS/SCSS linting

Run linting:
```bash
pnpm lint
```

Format code:
```bash
pnpm format
```

## Component Guidelines

- Use the Composition API with `<script setup>` for new components
- Follow the [Vue.js Style Guide](https://vuejs.org/style-guide/)
- Use TypeScript for type safety
- Use UnoCSS for styling
- Keep components small and focused on a single responsibility
- Use props and events for component communication

Example component:
```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  title: string
  items: string[]
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'select', item: string): void
}>()

const selectedIndex = ref(-1)

const isSelected = computed(() => selectedIndex.value !== -1)

function selectItem(index: number) {
  selectedIndex.value = index
  emit('select', props.items[index])
}
</script>

<template>
  <div class="component">
    <h2>{{ title }}</h2>
    <ul>
      <li
        v-for="(item, index) in items"
        :key="index"
        :class="{ 'selected': index === selectedIndex }"
        @click="selectItem(index)"
      >
        {{ item }}
      </li>
    </ul>
  </div>
</template>
```

## Testing

We use Vitest for unit tests and Playwright for end-to-end tests.

### Unit Tests

Run unit tests:
```bash
pnpm test
```

Run unit tests in CI mode:
```bash
pnpm test:ci
```

Write tests in the `tests` directory with the `.spec.ts` or `.test.ts` extension.

Example test:
```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MyComponent from '../src/components/MyComponent.vue'

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: {
        title: 'Hello',
        items: ['Item 1', 'Item 2']
      }
    })
    expect(wrapper.text()).toContain('Hello')
    expect(wrapper.findAll('li')).toHaveLength(2)
  })
})
```

### End-to-End Tests

Run e2e tests:
```bash
pnpm test:e2e
```

Run e2e tests in development mode:
```bash
pnpm test:e2e:dev
```

Run e2e tests with UI:
```bash
pnpm test:eui:dev
```

Record new tests:
```bash
pnpm test:record:dev
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

Before submitting, ensure:
- All tests pass
- Code is properly formatted
- New features include tests
- Documentation is updated if necessary

## Additional Resources

- [Vue.js Documentation](https://vuejs.org/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [UnoCSS Documentation](https://unocss.dev/)
- [Vite Documentation](https://vitejs.dev/)

Thank you for contributing to our frontend!
