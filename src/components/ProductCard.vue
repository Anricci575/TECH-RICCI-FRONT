<script setup>
// Props limpios para recibir datos de MySQL
const props = defineProps(['nombre', 'precio', 'descripcion', 'categoria', 'specs'])

// Función para poner el emoji correcto sin romper el compilador
const getHardwareEmoji = (cat) => {
  if (cat === 'LAPTOP') return '💻'
  if (cat === 'PC_ENSAMBLADA' || cat === 'WORKSTATION') return '🖥️'
  if (cat === 'COMPONENTE') return '🔌'
  return '🖱️'
}
</script>

<template>
  <div class="glass-card group p-2 rounded-[2rem] transition-all duration-500 bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] hover:-translate-y-3 hover:border-red-500/40 hover:shadow-[0_20px_40px_-15px_rgba(255,0,0,0.3)] relative overflow-hidden flex flex-col h-full text-[var(--color-main-text)]">

    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-[1px] bg-gradient-to-r from-transparent via-red-500/0 to-transparent group-hover:via-red-500/70 transition-colors duration-700 z-20"></div>

    <div class="relative aspect-square bg-[var(--color-glass)] rounded-[1.8rem] overflow-hidden flex items-center justify-center border border-[var(--color-glass-border)]">
      
      <div v-if="categoria" class="absolute top-4 left-4 z-30 px-3 py-1 bg-red-600/10 border border-red-500/20 rounded-lg text-[8px] font-mono text-red-500 uppercase tracking-[0.2em] backdrop-blur-md">
        {{ categoria }}
      </div>

      <div class="absolute inset-0 bg-grid-tech opacity-40 group-hover:opacity-100 transition-all duration-700 z-0"></div>
      <div class="absolute inset-0 bg-red-500/0 group-hover:bg-red-500/10 transition-colors duration-700 blur-xl z-0"></div>

      <span class="text-7xl group-hover:scale-125 transition-all duration-700 relative z-20">
        {{ getHardwareEmoji(categoria) }}
      </span>
      
      <div class="absolute top-4 right-4 px-4 py-2 bg-[var(--color-main-bg)] backdrop-blur-md border border-[var(--color-glass-border)] rounded-full text-sm font-bold group-hover:border-red-500/50 group-hover:text-red-500 transition-all duration-300 z-30 shadow-md">
        ${{ precio }}
      </div>
    </div>
    
    <div class="p-6 flex flex-col flex-grow relative z-20">
      <div class="flex items-center gap-2 mb-3">
        <span class="relative flex h-1.5 w-1.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-red-600"></span>
        </span>
        <span class="text-[9px] font-mono opacity-50 uppercase tracking-[0.2em] group-hover:text-red-500 transition-colors">SISTEMA_ACTIVO</span>
      </div>

      <h3 class="text-xl font-bold tracking-tight mb-2 group-hover:text-red-500 transition-all duration-300 capitalize">
        {{ nombre }}
      </h3>
      
      <div class="flex items-start gap-3 flex-grow mb-6">
        <div class="w-0.5 h-4 bg-red-500 mt-1"></div>
        <p class="opacity-60 text-sm font-mono text-[11px] tracking-wide">
          {{ descripcion || specs }}
        </p>
      </div>
      
      <button class="relative w-full py-3 bg-[var(--color-main-text)] border border-[var(--color-main-text)] text-[var(--color-main-bg)] font-bold rounded-xl overflow-hidden group/btn transition-all duration-300 hover:border-red-500 hover:shadow-[0_0_20px_rgba(255,0,0,0.3)] mt-auto">
        <span class="relative z-10 uppercase text-xs">Build Now</span>
        <div class="absolute inset-0 bg-gradient-to-r from-red-700 to-red-500 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 z-0"></div>
      </button>
    </div>
  </div>
</template>