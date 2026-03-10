<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from './ThemeToggle.vue'

const router = useRouter()
const userName = ref('Guest')
const userRole = ref('user')

// Extraemos la info de la sesión al montar el componente
onMounted(() => {
  const session = localStorage.getItem('techricci_session')
  const role = localStorage.getItem('techricci_role')
  
  if (session) {
    userName.value = localStorage.getItem('techricci_username') || 'Andrés'
    userRole.value = role || 'user'
  }
})

const handleLogout = () => {
  localStorage.removeItem('techricci_session')
  localStorage.removeItem('techricci_role')
  localStorage.removeItem('techricci_username')
  router.push('/')
}
</script>

<template>
  <div class="fixed top-6 w-full flex justify-center z-50 px-4 transition-all duration-500">
    <nav class="w-full max-w-[1400px] bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] rounded-full px-6 py-3 flex justify-between items-center shadow-lg text-[var(--color-main-text)]">
      
      <div class="flex items-center gap-2 text-xl font-bold tracking-tighter">
        <div class="w-2.5 h-2.5 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,0.8)]"></div>
        TECH<span class="font-light">RICCI</span>
      </div>

      <div class="hidden md:flex space-x-8 text-[11px] font-mono tracking-widest uppercase opacity-60">
        <a href="#tienda" class="hover:text-red-500 hover:opacity-100 transition-colors cursor-pointer">Inventario</a>
        <a href="#servicios" class="hover:text-red-500 hover:opacity-100 transition-colors cursor-pointer">Servicios</a>
      </div>

      <div class="flex items-center gap-4 md:gap-6">
        
        <div class="hidden lg:flex flex-col items-end font-mono leading-none mr-2">
          <span class="text-[9px] text-red-500 uppercase tracking-tighter mb-1 font-bold">
            {{ userRole === 'admin' ? 'ADMINISTRACIÓN' : 'USUARIO' }}
          </span>
          <span class="text-[11px] font-bold tracking-tight opacity-90">{{ userName }}</span>
        </div>

        <button 
          v-if="userRole === 'admin'"
          @click="router.push('/admin')"
          class="flex items-center gap-2 bg-red-500/10 border border-red-500/50 hover:bg-red-500 hover:text-white text-red-500 px-4 py-1.5 rounded-full text-[10px] font-mono uppercase tracking-widest transition-all duration-300 shadow-[0_0_10px_rgba(255,0,0,0.2)]"
          title="Abrir Panel de Control"
        >
          <span>⚙️ Panel</span>
        </button>

        <ThemeToggle />

        <button 
          @click="handleLogout" 
          class="group flex items-center gap-2 border border-[var(--color-glass-border)] hover:border-red-500 hover:bg-red-500/10 px-5 py-2 rounded-full text-[10px] font-mono uppercase tracking-widest transition-all duration-300 opacity-80 hover:opacity-100 hover:text-red-500"
        >
          <span class="w-1.5 h-1.5 rounded-full bg-red-500 group-hover:bg-red-400 transition-colors"></span>
          Cerrar Sesión
        </button>
      </div>

    </nav>
  </div>
</template>