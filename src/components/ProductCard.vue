<script setup>
import { computed } from 'vue'
import { addToCart } from '../store/cart' // <-- Importamos la función del carrito

// Agregamos 'id' a los props para poder identificar el producto en el carrito
const props = defineProps(['id', 'nombre', 'precio', 'descripcion', 'categoria', 'specs', 'imagen'])

const getHardwareEmoji = (cat) => {
  if (cat === 'LAPTOP') return '💻'
  if (cat === 'PC_ENSAMBLADA' || cat === 'WORKSTATION') return '🖥️'
  if (cat === 'COMPONENTE') return '🔌'
  if (cat === 'ROPA_OVERSIZE') return '👕'
  if (cat === 'SERVICIO_TECNICO') return '🛠️'
  return '🖱️'
}

const getImageUrl = (path) => {
  if (!path) return null
  return `http://127.0.0.1:8000/${path}`
}

// 🧠 INGENIERÍA: Separar las etiquetas [Nuevo] de la descripción real
const parsedData = computed(() => {
  const rawDesc = props.descripcion || props.specs || ''
  
  if (rawDesc.includes('|')) {
    const parts = rawDesc.split('|')
    const tagsRaw = parts[0] 
    const textInfo = parts.slice(1).join('|').trim() 
    
    const extractedTags = tagsRaw.match(/\[(.*?)\]/g)?.map(t => t.replace(/\[|\]/g, '').trim()) || []
    
    return { info: textInfo, tags: extractedTags }
  }
  
  return { info: rawDesc, tags: [] }
})

// 🔗 COMPARTIR: Usa la API nativa o copia al portapapeles
const shareProduct = async () => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: `Richi Tech - ${props.nombre}`,
        text: `Mira este equipo en Richi Tech: ${props.nombre} por $${props.precio}`,
        url: window.location.href,
      })
    } catch (err) {
      console.log('Error compartiendo', err)
    }
  } else {
    navigator.clipboard.writeText(window.location.href)
    alert('¡Enlace copiado al portapapeles!')
  }
}

// --- NUEVO: FUNCIÓN PARA AGREGAR AL CARRITO ---
const handleAddToCart = () => {
  addToCart({
    id: props.id,
    nombre: props.nombre,
    precio: props.precio,
    imagen: props.imagen
  })
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

      <div v-if="imagen" class="absolute inset-0 z-20 flex items-center justify-center p-6">
        <img 
          :src="getImageUrl(imagen)" 
          :alt="nombre"
          @error="$event.target.style.display='none'" 
          class="max-w-full max-h-full object-contain group-hover:scale-110 transition-transform duration-700 drop-shadow-[0_0_15px_rgba(255,0,0,0.2)]"
        />
      </div>
      <span v-else class="text-7xl group-hover:scale-125 transition-all duration-700 relative z-20">
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

      <div class="flex justify-between items-start mb-2 gap-2">
        <h3 class="text-xl font-bold tracking-tight group-hover:text-red-500 transition-all duration-300 capitalize">
          {{ nombre }}
        </h3>
        <button @click="shareProduct" class="shrink-0 p-2 rounded-full border border-[var(--color-glass-border)] hover:bg-red-600 hover:border-red-500 hover:text-white text-[var(--color-main-text)] opacity-50 hover:opacity-100 transition-all shadow-md relative z-30" title="Compartir">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path></svg>
        </button>
      </div>
      
      <div class="flex flex-col gap-3 flex-grow mb-6 mt-1">
        
        <div v-if="parsedData.tags.length > 0" class="flex flex-wrap gap-2">
          <span v-for="(tag, index) in parsedData.tags" :key="index" class="px-2 py-0.5 bg-red-500/10 border border-red-500/20 text-red-500 text-[9px] font-mono rounded uppercase tracking-widest">
            {{ tag }}
          </span>
        </div>

        <div class="flex items-start gap-3">
          <div class="w-0.5 h-4 bg-red-500 mt-1 shrink-0"></div>
          <p class="opacity-60 text-sm font-mono text-[11px] tracking-wide line-clamp-2">
            {{ parsedData.info || 'Sin detalles' }}
          </p>
        </div>
      </div>
      
      <button @click="handleAddToCart" class="relative w-full py-3 bg-[var(--color-main-text)] border border-[var(--color-main-text)] text-[var(--color-main-bg)] font-bold rounded-xl overflow-hidden group/btn transition-all duration-300 hover:border-red-500 hover:shadow-[0_0_20px_rgba(255,0,0,0.3)] mt-auto">
        <span class="relative z-10 uppercase text-xs">Build Now</span>
        <div class="absolute inset-0 bg-gradient-to-r from-red-700 to-red-500 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 z-0"></div>
      </button>
    </div>
  </div>
</template>