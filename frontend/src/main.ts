import { createApp } from 'vue'
import router from './router/Router'
import './style.css'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'
import App from './App.vue'

createApp(App)
    .use(router)
    .mount('#app')
