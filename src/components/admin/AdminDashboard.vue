<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminSettings from './AdminSettings.vue'
import AdminInventory from './AdminInventory.vue'
import AdminGOMS from './AdminGOMS.vue' 

const router = useRouter()
const activeModule = ref('dashboard') 

// --- ESTADO DE MÉTRICAS REALES ---
const stats = ref({
  totalProductos: 0,
  stockTotal: 0,
  totalVentas: 0,
  ingresosTotales: 0,
  logs: []
})
const isLoadingStats = ref(true)

// --- OBTENER DATOS REALES DEL BACKEND ---
const fetchDashboardStats = async () => {
  try {
    // 1. OBTENEMOS TUS PRODUCTOS REALES
    // Usamos la misma ruta que usa tu Home.vue para calcular el inventario exacto
    const resProducts = await fetch('http://127.0.0.1:8000/api/v1/products/')
    if (resProducts.ok) {
      const products = await resProducts.json()
      
      // Calculamos las métricas reales
      stats.value.totalProductos = products.length // Cuántos modelos distintos hay
      stats.value.stockTotal = products.reduce((acc, p) => acc + (p.stock || 0), 0) // Suma de todas las unidades
    }

    // 2. OBTENEMOS LAS VENTAS (Ruta futura)
    const resVentas = await fetch('http://127.0.0.1:8000/api/v1/ventas/stats')
    if (resVentas.ok) {
      const dataVentas = await resVentas.json()
      stats.value.totalVentas = dataVentas.total_ordenes
      stats.value.ingresosTotales = dataVentas.ingresos_totales
    } else {
      cargarVentasSimuladas() // Si no existe la ruta de ventas aún, simulamos
    }

  } catch (error) {
    console.error("Error conectando con la base de datos:", error)
    cargarVentasSimuladas()
  } finally {
    isLoadingStats.value = false
  }
}

// Simulador temporal solo para las ventas y logs
const cargarVentasSimuladas = () => {
  stats.value.totalVentas = 14
  stats.value.ingresosTotales = 24500
  stats.value.logs = [
    { hora: '14:02', mensaje: 'Nueva orden registrada: Threadripper Beast', usuario: 'Usuario_849', tipo: 'success' },
    { hora: '13:45', mensaje: 'Actualización de inventario global.', usuario: 'ROOT_Admin', tipo: 'danger' },
    { hora: '11:30', mensaje: 'Nuevo cliente autenticado en AUTH_GATEWAY.', usuario: 'System', tipo: 'info' }
  ]
}

onMounted(() => {
  const role = localStorage.getItem('techricci_role')
  if (role !== 'admin') {
    router.push('/store')
  } else {
    fetchDashboardStats() // Ejecutamos el cálculo al entrar
  }
})
</script>

<template>
  <div class="min-h-screen bg-[var(--color-main-bg)] text-[var(--color-main-text)] transition-colors duration-500 flex flex-col md:flex-row">
    
    <aside class="w-full md:w-64 md:border-r border-b md:border-b-0 border-[var(--color-glass-border)] bg-[var(--color-main-bg)]/80 backdrop-blur-xl flex flex-col justify-between p-6 z-20 md:h-screen md:sticky top-0 shadow-2xl">
      <div>
        <div class="mb-12">
          <h1 class="text-2xl font-light tracking-tighter uppercase leading-none group cursor-default">
            <span class="font-serif italic text-red-500 group-hover:text-red-400 transition-colors">Sistema</span><br>Anulación
          </h1>
          <p class="font-mono text-[9px] opacity-70 tracking-[0.2em] mt-2 text-red-500 flex items-center gap-2">
            <span class="w-1.5 h-1.5 bg-red-500 rounded-full animate-pulse"></span> Nivel de Acceso: ROOT
          </p>
        </div>

        <nav class="flex flex-col gap-3 font-mono text-xs uppercase tracking-widest">
          <button 
            @click="activeModule = 'dashboard'"
            class="text-left px-4 py-3.5 rounded-xl transition-all duration-300 flex items-center gap-3 relative overflow-hidden group"
            :class="activeModule === 'dashboard' ? 'bg-red-500/10 text-red-500 border border-red-500/30 shadow-[0_0_20px_rgba(255,0,0,0.15)]' : 'opacity-60 hover:opacity-100 hover:bg-[var(--color-glass)] border border-transparent'"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-red-500/0 via-red-500/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
            <span class="w-1.5 h-1.5 rounded-full" :class="activeModule === 'dashboard' ? 'bg-red-500 animate-pulse' : 'bg-transparent'"></span>
            📊 Centro de Mando
          </button>

          <button 
            @click="activeModule = 'inventory'"
            class="text-left px-4 py-3.5 rounded-xl transition-all duration-300 flex items-center gap-3 relative overflow-hidden group"
            :class="activeModule === 'inventory' ? 'bg-red-500/10 text-red-500 border border-red-500/30 shadow-[0_0_20px_rgba(255,0,0,0.15)]' : 'opacity-60 hover:opacity-100 hover:bg-[var(--color-glass)] border border-transparent'"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-red-500/0 via-red-500/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
            <span class="w-1.5 h-1.5 rounded-full" :class="activeModule === 'inventory' ? 'bg-red-500 animate-pulse' : 'bg-transparent'"></span>
            📦 Data Warehouse
          </button>
          
          <button 
            @click="activeModule = 'settings'"
            class="text-left px-4 py-3.5 rounded-xl transition-all duration-300 flex items-center gap-3 relative overflow-hidden group"
            :class="activeModule === 'settings' ? 'bg-red-500/10 text-red-500 border border-red-500/30 shadow-[0_0_20px_rgba(255,0,0,0.15)]' : 'opacity-60 hover:opacity-100 hover:bg-[var(--color-glass)] border border-transparent'"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-red-500/0 via-red-500/5 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"></div>
            <span class="w-1.5 h-1.5 rounded-full" :class="activeModule === 'settings' ? 'bg-red-500 animate-pulse' : 'bg-transparent'"></span>
            ⚙️ Apariencia
          </button>
        </nav>
      </div>

      <button @click="router.push('/store')" class="mt-8 text-[10px] font-mono border border-[var(--color-glass-border)] px-4 py-3 rounded-xl hover:border-red-500 hover:text-red-500 hover:bg-red-500/5 transition-all uppercase tracking-widest opacity-70 hover:opacity-100 text-left flex items-center justify-between group">
        <span>Volver a la Tienda</span>
        <span class="group-hover:-translate-x-1 transition-transform">←</span>
      </button>
    </aside>

    <main class="flex-1 p-4 md:p-8 w-full overflow-y-auto relative h-screen">
      <div class="max-w-[1400px] mx-auto w-full pb-20">
        
        <div v-if="activeModule === 'dashboard'" class="flex flex-col gap-8 animate-fade-in w-full">
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-6 rounded-[2rem] hover:border-red-500/30 hover:shadow-[0_10px_30px_rgba(255,0,0,0.05)] transition-all relative overflow-hidden group">
              <div class="absolute -right-4 -top-4 w-24 h-24 bg-blue-500/10 blur-2xl group-hover:bg-blue-500/20 transition-colors"></div>
              <span class="text-[10px] font-mono uppercase tracking-widest opacity-50 block mb-2">Productos Registrados</span>
              <h3 class="text-4xl font-light tracking-tighter text-white">
                <span v-if="isLoadingStats" class="animate-pulse opacity-50">--</span>
                <span v-else>{{ stats.totalProductos }}<span class="text-xl text-zinc-500"> mods.</span></span>
              </h3>
              <p class="text-[10px] text-blue-400 font-mono mt-4 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path></svg>
                Modelos únicos en Base de Datos
              </p>
            </div>
            
            <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-6 rounded-[2rem] hover:border-red-500/30 hover:shadow-[0_10px_30px_rgba(255,0,0,0.05)] transition-all relative overflow-hidden group">
              <div class="absolute right-0 top-0 w-32 h-32 bg-red-500/10 blur-2xl group-hover:bg-red-500/20 transition-colors"></div>
              <span class="text-[10px] font-mono uppercase tracking-widest opacity-50 block mb-2">Unidades en Stock</span>
              <h3 class="text-4xl font-light tracking-tighter text-white">
                <span v-if="isLoadingStats" class="animate-pulse opacity-50">--</span>
                <span v-else>{{ stats.stockTotal }}<span class="text-red-500 text-2xl font-medium"> u.</span></span>
              </h3>
              <p class="text-[10px] text-red-400 font-mono mt-4 flex items-center gap-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                Piezas físicas disponibles
              </p>
            </div>

            <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-6 rounded-[2rem] hover:border-red-500/30 hover:shadow-[0_10px_30px_rgba(255,0,0,0.05)] transition-all relative overflow-hidden group">
              <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-green-500/10 blur-2xl group-hover:bg-green-500/20 transition-colors"></div>
              <span class="text-[10px] font-mono uppercase tracking-widest opacity-50 block mb-2">Órdenes Procesadas</span>
              <h3 class="text-4xl font-light tracking-tighter text-white">
                <span v-if="isLoadingStats" class="animate-pulse opacity-50">--</span>
                <span v-else>{{ stats.totalVentas }}<span class="text-xl text-zinc-500"> ventas</span></span>
              </h3>
              <p class="text-[10px] text-green-500 font-mono mt-4 flex items-center gap-2 font-bold">
                <span class="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.8)]"></span>
                Ingresos: ${{ stats.ingresosTotales.toLocaleString() }}
              </p>
            </div>
          </div>

          <div class="w-full">
            <AdminGOMS />
          </div>

          <div class="glass-card bg-[var(--color-glass)] border border-[var(--color-glass-border)] p-8 rounded-[2rem] w-full mt-2">
            <div class="flex justify-between items-center mb-8 border-b border-[var(--color-glass-border)] pb-4">
              <h3 class="text-xs font-mono uppercase tracking-widest opacity-80">> Registro de Eventos del Sistema</h3>
              <span class="text-[9px] px-2 py-1 bg-red-500/10 text-red-500 rounded border border-red-500/20 font-mono flex items-center gap-2">
                <span class="w-1 h-1 bg-red-500 rounded-full animate-ping"></span> LIVE_FEED
              </span>
            </div>

            <ul class="space-y-4 font-mono text-xs">
              <li v-if="isLoadingStats" class="animate-pulse opacity-50 text-center py-4">Sincronizando logs...</li>
              <li v-else-if="stats.logs.length === 0" class="opacity-50 text-center py-4">No hay eventos recientes.</li>
              
              <li 
                v-for="(log, index) in stats.logs" 
                :key="index"
                class="flex items-center justify-between opacity-80 pl-4 py-2 rounded-r-lg transition-colors border-l-2"
                :class="{
                  'border-green-500 bg-gradient-to-r from-green-500/5 to-transparent': log.tipo === 'success',
                  'border-red-500 bg-gradient-to-r from-red-500/5 to-transparent': log.tipo === 'danger',
                  'border-white/20 hover:bg-white/5': log.tipo === 'info' || !log.tipo
                }"
              >
                <div class="flex items-center gap-4">
                  <span class="opacity-40 w-12 shrink-0">{{ log.hora }}</span>
                  <span v-html="log.mensaje"></span>
                </div>
                <span class="opacity-50 shrink-0">{{ log.usuario }}</span>
              </li>
            </ul>

            <button class="w-full mt-8 py-3 border border-dashed border-[var(--color-glass-border)] rounded-xl text-[9px] font-mono uppercase tracking-widest opacity-50 hover:opacity-100 hover:border-red-500 hover:text-red-400 hover:bg-red-500/5 transition-all">
              Cargar registros anteriores...
            </button>
          </div>
        </div>

        <div v-if="activeModule === 'inventory'" class="animate-fade-in h-full">
          <AdminInventory />
        </div>

        <div v-if="activeModule === 'settings'" class="max-w-4xl animate-fade-in mx-auto">
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
  animation: fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

main::-webkit-scrollbar {
  width: 6px;
}
main::-webkit-scrollbar-track {
  background: transparent;
}
main::-webkit-scrollbar-thumb {
  background-color: rgba(255, 0, 0, 0.2);
  border-radius: 20px;
}
main:hover::-webkit-scrollbar-thumb {
  background-color: rgba(255, 0, 0, 0.4);
}
</style>