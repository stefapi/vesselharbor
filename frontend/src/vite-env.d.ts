/// <reference types="vite/client" />
declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
/// <reference types="@histoire/plugin-vue/components" />
/// <reference types="unplugin-vue-router/client" />
