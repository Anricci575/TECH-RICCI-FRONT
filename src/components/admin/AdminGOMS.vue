<script setup>
import { ref, computed } from 'vue'

// Tiempos del modelo KLM según la literatura (en segundos)
const klmConstants = {
  K: 0.2,  // Tecla
  P: 1.1,  // Apuntar (Mouse)
  H: 0.4,  // Mover mano (Teclado <-> Mouse)
  M: 1.2,  // Pensar / Preparación mental
  B: 0.1   // Clic de Mouse
}

// Datos de la evaluación del formulario "NUEVO REGISTRO"
const tasks = [
  { name: 'Subir Imagen (Elegir Archivo, Clic)', k: 0, p: 1, h: 0, m: 1, b: 1 },
  { name: 'Designación (Apuntar, Clic, "pc")', k: 2, p: 1, h: 1, m: 1, b: 1 },
  { name: 'Valor Unidad (Apuntar, Clic, "20")', k: 2, p: 1, h: 1, m: 1, b: 1 },
  { name: 'Categoría (Abrir drop, Elegir "LAPTOP")', k: 0, p: 2, h: 1, m: 1, b: 2 },
  { name: 'Condición (Abrir drop, Elegir "Nuevo")', k: 0, p: 2, h: 0, m: 1, b: 2 },
  { name: 'Protocolo (Apuntar "Hardware", Clic)', k: 0, p: 1, h: 0, m: 1, b: 1 },
  { name: 'Detalles (Apuntar, Clic, "qwedqwdq")', k: 8, p: 1, h: 1, m: 1, b: 1 },
  { name: 'Finalizar (Apuntar "Registrar", Clic)', k: 0, p: 1, h: 1, m: 1, b: 1 }
]

const totals = computed(() => {
  return tasks.reduce((acc, task) => {
    acc.K += task.k; acc.P += task.p; acc.H += task.h; acc.M += task.m; acc.B += task.b;
    return acc
  }, { K: 0, P: 0, H: 0, M: 0, B: 0 })
})

const totalTime = computed(() => {
  return (totals.value.K * klmConstants.K) +
         (totals.value.P * klmConstants.P) +
         (totals.value.H * klmConstants.H) +
         (totals.value.M * klmConstants.M) +
         (totals.value.B * klmConstants.B)
})

const showOptimization = ref(false)
</script>

<template>
  <div class="glass-card bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] p-6 md:p-8 rounded-[2rem] shadow-2xl w-full text-[var(--color-main-text)]">
    
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 border-b border-[var(--color-glass-border)] pb-4 gap-4">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-2.5 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,1)]"></div>
        <div>
          <h2 class="text-xl font-bold uppercase tracking-widest leading-none">Métricas de Usabilidad</h2>
          <p class="text-[10px] font-mono opacity-50 uppercase tracking-[0.2em] mt-1">Evaluación GOMS-KLM Activa</p>
        </div>
      </div>
      
      <button 
        @click="showOptimization = !showOptimization" 
        class="border border-red-500/50 hover:bg-red-500/10 text-red-400 px-4 py-2 rounded-lg text-[10px] font-mono uppercase tracking-widest transition-all"
      >
        {{ showOptimization ? 'Ver Modo Normal' : 'Simular Optimización TAB' }}
      </button>
    </div>

    <div class="overflow-x-auto mb-6">
      <table class="w-full text-left text-sm">
        <thead class="text-[10px] font-mono uppercase tracking-widest opacity-60 border-b border-[var(--color-glass-border)]">
          <tr>
            <th class="pb-3 pl-2">Operación / Tarea</th>
            <th class="pb-3 text-center w-12 text-zinc-300" title="Teclas (K)">K</th>
            <th class="pb-3 text-center w-12 text-blue-400" title="Apuntar (P)">P</th>
            <th class="pb-3 text-center w-12 text-purple-400" title="Mover Mano (H)">H</th>
            <th class="pb-3 text-center w-12 text-yellow-400" title="Pensar (M)">M</th>
            <th class="pb-3 text-center w-12 text-green-400" title="Clic (B)">B</th>
          </tr>
        </thead>
        <tbody class="font-mono text-[11px] divide-y divide-[var(--color-glass-border)]">
          <tr v-for="(task, index) in tasks" :key="index" class="hover:bg-red-500/5 transition-colors">
            <td class="py-3 pl-2 text-zinc-300">{{ task.name }}</td>
            <td class="py-3 text-center">{{ task.k || '-' }}</td>
            <td class="py-3 text-center opacity-80" :class="{ 'line-through text-red-500 opacity-30': showOptimization && task.p > 0 && index !== 0 && index !== 7 }">{{ task.p || '-' }}</td>
            <td class="py-3 text-center opacity-80" :class="{ 'line-through text-red-500 opacity-30': showOptimization && task.h > 0 && index !== 0 && index !== 7 }">{{ task.h || '-' }}</td>
            <td class="py-3 text-center">{{ task.m || '-' }}</td>
            <td class="py-3 text-center">{{ task.b || '-' }}</td>
          </tr>
          <tr class="bg-black/20 font-bold border-t-2 border-zinc-800 text-[12px]">
            <td class="py-4 pl-2 text-red-400 uppercase tracking-widest">TOTALES DEL SISTEMA</td>
            <td class="py-4 text-center">{{ totals.K }}</td>
            <td class="py-4 text-center" :class="{ 'text-red-500': showOptimization }">{{ showOptimization ? 2 : totals.P }}</td>
            <td class="py-4 text-center" :class="{ 'text-red-500': showOptimization }">{{ showOptimization ? 1 : totals.H }}</td>
            <td class="py-4 text-center">{{ totals.M }}</td>
            <td class="py-4 text-center">{{ totals.B }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <div class="bg-black/30 border border-[var(--color-glass-border)] rounded-xl p-4">
        <h4 class="text-[10px] font-mono text-zinc-500 uppercase tracking-widest mb-3 border-b border-zinc-800 pb-2">Constantes (Seg)</h4>
        <ul class="text-[10px] font-mono space-y-1.5 opacity-80">
          <li>[K] Teclado: <span class="float-right font-bold text-white">0.2s</span></li>
          <li>[P] Apuntar: <span class="float-right font-bold text-white">1.1s</span></li>
          <li>[H] Mover mano: <span class="float-right font-bold text-white">0.4s</span></li>
          <li>[M] Prep. Mental: <span class="float-right font-bold text-white">1.2s</span></li>
          <li>[B] Clic Mouse: <span class="float-right font-bold text-white">0.1s</span></li>
        </ul>
      </div>

      <div class="bg-black/30 border border-[var(--color-glass-border)] rounded-xl p-4 flex flex-col justify-center">
        <div v-if="!showOptimization">
          <span class="text-[10px] font-bold text-red-500 uppercase tracking-widest block mb-1">Evaluación Estándar</span>
          <p class="text-xs text-zinc-400 leading-relaxed font-mono">El usuario utiliza el mouse para hacer clic en cada campo individualmente, aumentando drásticamente los operadores (P) y (H).</p>
        </div>
        <div v-else>
          <span class="text-[10px] font-bold text-green-500 uppercase tracking-widest block mb-1">Mejora de Interfaz (TAB)</span>
          <p class="text-xs text-zinc-400 leading-relaxed font-mono">Al permitir navegación por teclado (TAB), eliminamos 8 movimientos de mouse y 4 cambios de mano, reduciendo la fricción cognitiva.</p>
        </div>
      </div>

      <div class="bg-red-950/20 border border-red-500/30 rounded-xl p-6 flex flex-col items-center justify-center relative overflow-hidden group">
        <div class="absolute inset-0 bg-red-500/5 group-hover:bg-red-500/10 transition-colors"></div>
        <span class="text-[10px] font-mono text-red-400 uppercase tracking-widest relative z-10 mb-2">Tiempo Estimado de Registro</span>
        
        <div class="flex items-baseline gap-1 relative z-10">
          <span class="text-5xl font-black tracking-tighter" :class="showOptimization ? 'text-green-500' : 'text-white'">
            {{ showOptimization ? (totalTime - 10.4).toFixed(1) : totalTime.toFixed(1) }}
          </span>
          <span class="text-sm font-mono text-zinc-400">seg</span>
        </div>
      </div>

    </div>
  </div>
</template>