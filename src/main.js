import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // <-- Importamos el router que creaste

const app = createApp(App)

app.use(router) // <-- Le inyectamos el sistema de rutas a Vue
app.mount('#app')