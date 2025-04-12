// src/main.ts
import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router/index.js';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css' // ou SCSS si personnalisé
import 'virtual:uno.css'
import 'nprogress/nprogress.css'
import NProgress from 'nprogress'
import 'material-icons/iconfont/material-icons.css'

const app = createApp(App);

router.beforeEach((to, from, next) => {
  NProgress.start()
  next()
})

router.afterEach(() => {
  NProgress.done()
})

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia);
app.use(router);
app.use(ElementPlus)

app.mount('#app');

