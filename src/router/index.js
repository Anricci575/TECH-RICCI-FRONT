import { createRouter, createWebHistory } from 'vue-router'
// Ajustamos la ruta para que busque en la carpeta components
import Auth from '../components/Auth.vue'
import Home from '../components/Home.vue'
// Importamos el nuevo panel de administrador táctico
import AdminDashboard from '../components/admin/AdminDashboard.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Auth',
      component: Auth 
    },
    {
      path: '/store',
      name: 'Store',
      component: Home 
    },
    {
      path: '/admin',
      name: 'Admin',
      component: AdminDashboard,
      // SEGURIDAD: Guardia de navegación para bloquear intrusos
      beforeEnter: (to, from, next) => {
        const role = localStorage.getItem('techricci_role')
        if (role === 'admin') {
          next() // Credenciales válidas: permite el acceso
        } else {
          console.warn('[SECURITY] Acceso denegado. Se requiere nivel ROOT.')
          next('/store') // Redirige a los usuarios normales a la tienda
        }
      }
    }
  ]
})

export default router