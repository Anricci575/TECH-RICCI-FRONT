<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from './Navbar.vue'
import Hero from './Hero.vue'
import ProductCard from './ProductCard.vue'

const router = useRouter()
const carouselRef = ref(null)

// --- ESTADO REAL DEL INVENTARIO ---
const pcs = ref([]) // Inicialmente vacío para que no haya datos ficticios
const loading = ref(true)

// --- OBTENER PRODUCTOS DE MYSQL ---
const fetchHardware = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/products/')
    if (response.ok) {
      pcs.value = await response.json()
    }
  } catch (error) {
    console.error("Error conectando con la base de datos:", error)
  } finally {
    loading.value = false
  }
}

// --- SEGURIDAD: Navigation Guard ---
onMounted(() => {
  const session = localStorage.getItem('techricci_session')
  if (!session) {
    router.push('/')
  } else {
    // Si hay sesión, procedemos a cargar los productos reales
    fetchHardware()
  }
})

const scrollCarousel = (direction) => {
  if (carouselRef.value) {
    const scrollAmount = 420;
    carouselRef.value.scrollBy({
      left: direction === 'left' ? -scrollAmount : scrollAmount,
      behavior: 'smooth'
    })
  }
}

const servicios = [
  { id: '01', titulo: 'Hardware & Ensamblaje', desc: 'Armado a medida y gestión de cables premium.' },
  { id: '02', titulo: 'Optimización de OS', desc: 'Ajuste de sistemas y despliegue de entornos ligeros.' },
  { id: '03', titulo: 'Diagnóstico a nivel placa', desc: 'Micro-soldadura y reparación de componentes.' }
]
</script>

<template>
  <div class="min-h-screen transition-colors duration-500 bg-[var(--color-main-bg)] text-[var(--color-main-text)] font-sans selection:bg-red-500/30 selection:text-red-600 dark:selection:text-red-200 bg-grid-tech">
    
    <Navbar />
    <Hero />
    
    <section id="tienda" class="max-w-[1400px] mx-auto px-6 py-20 relative z-10 text-[var(--color-main-text)]">
      
      <div class="flex flex-col md:flex-row justify-between items-end mb-12 gap-6 slide-up" style="animation-delay: 0.2s;">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--color-glass-border)] bg-[var(--color-glass)] text-[10px] font-mono uppercase tracking-widest mb-4 opacity-70">
            <span class="text-red-500">✦</span> Ready to ship
          </div>
          <h2 class="text-5xl md:text-6xl font-normal tracking-tighter">
            HARDWARE <span class="font-serif italic opacity-50">SELECTION</span>
          </h2>
        </div>
        
        <div class="flex items-center gap-4">
          <div class="text-[10px] font-mono uppercase tracking-[0.3em] hidden md:block mr-4 opacity-40">
            Desliza para explorar — (01)
          </div>
          <button @click="scrollCarousel('left')" class="w-12 h-12 rounded-full border border-[var(--color-glass-border)] flex items-center justify-center hover:bg-[var(--color-glass)] hover:border-red-500/50 transition-all opacity-50 hover:opacity-100 hover:text-red-500 group">
            <span class="group-hover:-translate-x-1 transition-transform">←</span>
          </button>
          <button @click="scrollCarousel('right')" class="w-12 h-12 rounded-full border border-[var(--color-glass-border)] flex items-center justify-center hover:bg-[var(--color-glass)] hover:border-red-500/50 transition-all opacity-50 hover:opacity-100 hover:text-red-500 group">
            <span class="group-hover:translate-x-1 transition-transform">→</span>
          </button>
        </div>
      </div>

      <div 
        ref="carouselRef" 
        class="flex overflow-x-auto gap-6 pb-8 snap-x snap-mandatory hide-scrollbar slide-up [mask-image:linear-gradient(to_right,transparent,black_5%,black_95%,transparent)] dark:[mask-image:linear-gradient(to_right,transparent,white_5%,white_95%,transparent)]" 
        style="animation-delay: 0.4s;"
      >
        <div v-if="pcs.length === 0 && !loading" class="w-full text-center py-20 border border-dashed border-[var(--color-glass-border)] rounded-[2rem] opacity-30 font-mono uppercase text-xs tracking-widest">
          Esperando inyección de hardware...
        </div>

        <div 
          v-for="pc in pcs" 
          :key="pc.id" 
          class="snap-start shrink-0 w-[85vw] md:w-[400px] transition-transform duration-300 hover:-translate-y-2"
        >
          <ProductCard 
            :nombre="pc.nombre" 
            :precio="pc.precio" 
            :descripcion="pc.descripcion" 
            :categoria="pc.categoria" 
          />
        </div>
      </div>
    </section>

    <section id="servicios" class="max-w-7xl mx-auto px-6 py-32 border-t border-[var(--color-glass-border)] mt-10 relative z-10 text-[var(--color-main-text)]">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div>
          <h2 class="text-5xl md:text-6xl font-normal tracking-tighter leading-tight mb-6">
            End-to-End <br>
            <span class="font-serif italic text-red-600 dark:text-red-500">Tech Services.</span>
          </h2>
          <p class="opacity-60 text-sm leading-relaxed mb-10 max-w-md">
            No solo vendemos equipos; mantenemos tu infraestructura tecnológica funcionando al máximo rendimiento.
          </p>
          <button class="px-8 py-3.5 border border-[var(--color-glass-border)] font-medium rounded-full hover:bg-[var(--color-glass)] transition-all text-sm opacity-90 hover:opacity-100">
            Agendar Diagnóstico
          </button>
        </div>

        <div class="flex flex-col gap-4">
          <div v-for="servicio in servicios" :key="servicio.id" 
               class="glass-card p-6 rounded-3xl flex justify-between items-center group cursor-pointer hover:border-red-500/30 hover:bg-[var(--color-glass)] transition-all shadow-sm">
            <div>
              <h3 class="text-xl font-medium mb-1 group-hover:text-red-500 transition-colors">
                {{ servicio.titulo }}
              </h3>
              <p class="text-xs opacity-60">{{ servicio.desc }}</p>
            </div>
            <span class="font-mono opacity-40 group-hover:opacity-100 group-hover:text-red-500 transition-colors">
              ({{ servicio.id }})
            </span>
          </div>
        </div>
      </div>
    </section>

    <footer class="border-t border-[var(--color-glass-border)] py-10 text-center relative z-10 text-[var(--color-main-text)]">
      <div class="flex items-center justify-center gap-2 text-xl font-bold tracking-tighter mb-4">
        <div class="w-2 h-2 bg-red-600 rounded-full animate-pulse"></div>
        TECH<span class="font-light">RICCI</span>
      </div>
      <p class="text-[10px] font-mono uppercase tracking-widest opacity-40">
        © 2026 — Proyecto Universitario.
      </p>
    </footer>

  </div>
</template>