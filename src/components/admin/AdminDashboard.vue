<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminSettings from './AdminSettings.vue'
import AdminInventory from './AdminInventory.vue' // Importamos el nuevo módulo de inventario

const router = useRouter()
const activeModule = ref('dashboard') // Por defecto, mostramos las métricas al entrar

onMounted(() => {
  const role = localStorage.getItem('techricci_role')
  if (role !== 'admin') {
    router.push('/store')
  }
})
</script>

<template>
  <div class="min-h-screen bg-[var(--color-main-bg)] text-[var(--color-main-text)] transition-colors duration-500 flex flex-col md:flex-row">
    
    <aside class="w-full md:w-64 border-b md:border-b-0 md:border-r border-[var(--color-glass-border)] bg-[var(--color-main-bg)]/50 backdrop-blur-md flex flex-col justify-between p-6 z-20 md:h-screen md:sticky top-0">
      <div>
        <div class="mb-12">
          <h1 class="text-2xl font-light tracking-tighter uppercase leading-none">
            <span class="font-serif italic text-red-500">Sistema</span><br>Anulación
          </h1>
          <p class="font-mono text-[9px] opacity-50 tracking-[0.2em] mt-2 text-red-500">Nivel de Acceso: ROOT</p>
        </div>

        <nav class="flex flex-col gap-2 font-mono text-xs uppercase tracking-widest">
          <button 
            @click="activeModule = 'dashboard'"
            class="text-left px-4 py-3 rounded-xl transition-all flex items-center gap-3"
            :class="activeModule === 'dashboard' ? 'bg-red-500/10 text-red-500 border border-red-500/20 shadow-[0_0_15px_rgba(255,0,0,0.1)]' : 'opacity-50 hover:opacity-100 hover:bg-[var(--color-glass)]'"
          >
            <span class="w-1.5 h-1.5 rounded-full" :class="activeModule === 'dashboard' ? 'bg-red-500 animate-pulse' : 'bg-transparent'"></span>
            📊 Centro de Mando
          </button>

          <button 
            @click="activeModule = 'inventory'"
            class="text-left px-4 py-3 rounded-xl transition-all flex items-center gap-3"
            :class="activeModule === 'inventory' ? 'bg-red-500/10 text-red-500 border border-red-500/20 shadow-[0_0_15px_rgba(255,0,0,0.1)]' : 'opacity-50 hover:opacity-100 hover:bg-[var(--color-glass)]'"
          >
            <span class="w-1.5 h-1.5 rounded-full" :class="activeModule === 'inventory' ? 'bg-red-500 animate-pulse' : 'bg-transparent'"></span>
            📦 Data Warehouse
          </button>
          
          <button 
            @click="activeModule = 'settings'"
            class="text-left px-4 py-3 rounded-xl transition-all flex items-center gap-3"
            :class="activeModule === 'settings' ? 'bg-red-500/10 text-red-500 border border-red-500/20 shadow-[0_0_15px_rgba(255,0,0,0.1)]' : 'opacity-50 hover:opacity-100 hover:bg-[var(--color-glass)]'"
          >
            <span class="w-1.5 h-1.5 rounded-full" :class="activeModule === 'settings' ? 'bg-red-500 animate-pulse' : 'bg-transparent'"></span>
            ⚙️ Apariencia
          </button>
        </nav>
      </div>

      <button @click="router.push('/store')" class="mt-8 text-[10px] font-mono border border-[var(--color-glass-border)] px-4 py-3 rounded-xl hover:border-red-500 transition-colors uppercase tracking-widest opacity-70 hover:opacity-100 text-left">
        ← Volver a la Tienda
      </button>
    </aside>

    <main class="flex-1 p-4 md:p-8 w-full overflow-hidden relative">
      <div class="max-w-[1400px] mx-auto w-full h-full">
        
        <div v-if="activeModule === 'dashboard'" class="flex flex-col gap-6 animate-fade-in w-full">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-6 rounded-[2rem] hover:border-red-500/30 transition-all">
              <span class="text-[10px] font-mono uppercase tracking-widest opacity-50">Ingresos Mensuales</span>
              <h3 class="text-4xl font-light tracking-tighter mt-2">$24,500</h3>
              <p class="text-[10px] text-green-500 font-mono mt-4">+12.5% vs Mes Anterior</p>
            </div>
            
            <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-6 rounded-[2rem] hover:border-red-500/30 transition-all relative overflow-hidden">
              <div class="absolute right-0 top-0 w-32 h-32 bg-red-500/10 blur-2xl"></div>
              <span class="text-[10px] font-mono uppercase tracking-widest opacity-50">Órdenes Activas</span>
              <h3 class="text-4xl font-light tracking-tighter mt-2">14<span class="text-red-500 text-2xl"> u.</span></h3>
              <p class="text-[10px] text-red-500 font-mono mt-4">3 En ensamblaje táctico</p>
            </div>

            <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-6 rounded-[2rem] hover:border-red-500/30 transition-all">
              <span class="text-[10px] font-mono uppercase tracking-widest opacity-50">Salud de Red</span>
              <h3 class="text-4xl font-light tracking-tighter mt-2">99.8<span class="text-xl">%</span></h3>
              <p class="text-[10px] text-green-500 font-mono mt-4 flex items-center gap-2">
                <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span> Nodos Estables
              </p>
            </div>
          </div>

          <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-8 rounded-[2rem] flex-1">
            <div class="flex justify-between items-center mb-8 border-b border-[var(--color-glass-border)] pb-4">
              <h3 class="text-xs font-mono uppercase tracking-widest opacity-70">> Registro de Eventos del Sistema</h3>
              <span class="text-[9px] px-2 py-1 bg-red-500/10 text-red-500 rounded border border-red-500/20 font-mono">LIVE_FEED</span>
            </div>

            <ul class="space-y-4 font-mono text-xs">
              <li class="flex items-center justify-between opacity-80 border-l-2 border-green-500 pl-4 py-1">
                <div class="flex items-center gap-4">
                  <span class="opacity-40 w-12">14:02</span>
                  <span>Nueva orden registrada: <strong class="text-red-500 font-normal">Threadripper Beast</strong></span>
                </div>
                <span class="opacity-50">Usuario_849</span>
              </li>
              <li class="flex items-center justify-between opacity-80 border-l-2 border-red-500 pl-4 py-1">
                <div class="flex items-center gap-4">
                  <span class="opacity-40 w-12">13:45</span>
                  <span>Actualización de inventario global.</span>
                </div>
                <span class="opacity-50">ROOT_Admin</span>
              </li>
              <li class="flex items-center justify-between opacity-80 border-l-2 border-white/20 pl-4 py-1">
                <div class="flex items-center gap-4">
                  <span class="opacity-40 w-12">11:30</span>
                  <span>Nuevo cliente autenticado en AUTH_GATEWAY.</span>
                </div>
                <span class="opacity-50">System</span>
              </li>
              <li class="flex items-center justify-between opacity-80 border-l-2 border-white/20 pl-4 py-1">
                <div class="flex items-center gap-4">
                  <span class="opacity-40 w-12">09:15</span>
                  <span>Respaldo de base de datos completado.</span>
                </div>
                <span class="opacity-50">Cron_Job</span>
              </li>
            </ul>

            <button class="w-full mt-8 py-3 border border-dashed border-[var(--color-glass-border)] text-[9px] font-mono uppercase tracking-widest opacity-50 hover:opacity-100 hover:border-red-500 transition-colors">
              Cargar registros anteriores...
            </button>
          </div>
        </div>

        <div v-if="activeModule === 'inventory'" class="animate-fade-in h-full">
          <AdminInventory />
        </div>

        <div v-if="activeModule === 'settings'" class="max-w-4xl animate-fade-in">
          <AdminSettings />
        </div>

      </div>
    </main>

  </div>
</template>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out forwards;
}
</style>