// src/main.ts
import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router/index.js';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// @ts-ignore
import { createVuestic } from 'vuestic-ui';
import 'vuestic-ui/css'
import 'vuestic-ui/styles/essential.css'
import 'vuestic-ui/styles/typography.css'
import 'virtual:uno.css'
import 'nprogress/nprogress.css'
import NProgress from 'nprogress'
//import '@/styles/nprogress.css' // ou ton chemin
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
app.use(createVuestic({
  components: {
    VaToast: {
      position: 'top-right',
      closeable: true,
      duration: 5000
    }
  }
}));

app.mount('#app');

