<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isDark = ref(true)
const isMenuOpen = ref(false)
const currentCbMode = ref('none') // 'none', 'protan', 'tritan', 'achroma'

// Cierra el menú si se hace clic afuera
const closeMenu = (e) => {
  if (!e.target.closest('.accessibility-container')) {
    isMenuOpen.value = false
  }
}

onMounted(() => {
  const htmlElement = document.documentElement
  document.addEventListener('click', closeMenu)

  // 1. Restaurar Tema (Claro/Oscuro)
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'light') {
    isDark.value = false
    htmlElement.classList.remove('dark')
  } else {
    htmlElement.classList.add('dark')
  }

  // 2. Restaurar Modo de Daltonismo
  const savedCbMode = localStorage.getItem('techricci_cb_mode')
  if (savedCbMode && savedCbMode !== 'none') {
    setCbMode(savedCbMode)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', closeMenu)
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  const htmlElement = document.documentElement
  
  if (isDark.value) {
    htmlElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    htmlElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const setCbMode = (mode) => {
  const htmlElement = document.documentElement
  currentCbMode.value = mode
  
  // Limpiar clases anteriores
  htmlElement.classList.remove('cb-protan', 'cb-tritan', 'cb-achroma')
  
  if (mode !== 'none') {
    htmlElement.classList.add(`cb-${mode}`)
  }
  
  localStorage.setItem('techricci_cb_mode', mode)
  isMenuOpen.value = false // Cerrar menú al seleccionar
}
</script>

<template>
  <div class="flex items-center gap-3 accessibility-container relative">
    
    <button 
      @click="toggleTheme" 
      class="relative w-12 h-6 rounded-full bg-zinc-200 dark:bg-zinc-800 border border-black/10 dark:border-white/10 transition-colors duration-500"
      title="Alternar Tema"
    >
      <div 
        class="absolute top-1 left-1 w-4 h-4 rounded-full bg-red-600 transition-transform duration-500 shadow-[0_0_10px_rgba(220,38,38,0.5)]"
        :class="{ 'translate-x-6': isDark }"
      ></div>
    </button>

    <div class="w-px h-4 bg-black/10 dark:bg-white/10"></div>

    <div class="relative">
      <button
        @click="isMenuOpen = !isMenuOpen"
        class="relative w-7 h-7 rounded-full flex items-center justify-center transition-all duration-300 border"
        :class="currentCbMode !== 'none' ? 'bg-blue-500/10 border-blue-500/50 text-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.2)]' : 'bg-transparent border-black/10 dark:border-white/10 text-black/40 dark:text-white/40 hover:text-black dark:hover:text-white'"
        title="Opciones de Accesibilidad"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        <span v-if="currentCbMode !== 'none'" class="absolute top-0 right-0 w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></span>
      </button>

      <div 
        v-if="isMenuOpen" 
        class="absolute right-0 top-10 w-48 bg-white dark:bg-[#0a0a0a] border border-black/10 dark:border-white/10 rounded-xl shadow-2xl overflow-hidden flex flex-col z-50 animate-fade-in"
      >
        <div class="px-3 py-2 bg-black/5 dark:bg-white/5 border-b border-black/5 dark:border-white/5">
          <span class="text-[9px] font-mono uppercase tracking-widest text-black/50 dark:text-white/50">Filtros Visuales</span>
        </div>
        
        <button 
          @click="setCbMode('none')" 
          class="px-3 py-2 text-left text-[10px] font-mono uppercase tracking-wider hover:bg-black/5 dark:hover:bg-white/5 transition-colors flex items-center gap-2" 
          :class="currentCbMode === 'none' ? 'text-red-500 font-bold' : 'text-black/70 dark:text-white/70'"
        >
          👁️ Estándar
        </button>

        <button 
          @click="setCbMode('protan')" 
          class="px-3 py-2 text-left text-[10px] font-mono uppercase tracking-wider hover:bg-black/5 dark:hover:bg-white/5 transition-colors flex items-center gap-2" 
          :class="currentCbMode === 'protan' ? 'text-blue-500 font-bold' : 'text-black/70 dark:text-white/70'"
        >
          🔴 Protanopia
        </button>

        <button 
          @click="setCbMode('tritan')" 
          class="px-3 py-2 text-left text-[10px] font-mono uppercase tracking-wider hover:bg-black/5 dark:hover:bg-white/5 transition-colors flex items-center gap-2" 
          :class="currentCbMode === 'tritan' ? 'text-blue-500 font-bold' : 'text-black/70 dark:text-white/70'"
        >
          🔵 Tritanopia
        </button>

        <button 
          @click="setCbMode('achroma')" 
          class="px-3 py-2 text-left text-[10px] font-mono uppercase tracking-wider hover:bg-black/5 dark:hover:bg-white/5 transition-colors flex items-center gap-2" 
          :class="currentCbMode === 'achroma' ? 'text-blue-500 font-bold' : 'text-black/70 dark:text-white/70'"
        >
          ⚫ Acromatopsia
        </button>
      </div>
    </div>

  </div>
</template>

<style>
/* 1. Protanopia / Deuteranopia (Rojo-Verde) -> Convierte Rojos a Azules */
html.cb-protan { filter: hue-rotate(220deg); }
html.cb-protan img, html.cb-protan video { filter: hue-rotate(-220deg); }

/* 2. Tritanopia (Azul-Amarillo) -> Desplaza el espectro para mayor claridad sin azul */
html.cb-tritan { filter: sepia(30%) hue-rotate(-45deg); }
html.cb-tritan img, html.cb-tritan video { filter: hue-rotate(45deg) sepia(0%); }

/* 3. Acromatopsia (Monocromo) -> Escala de grises con contraste alto */
html.cb-achroma { filter: grayscale(100%) contrast(110%); }
/* Nota: En acromatopsia pura, todo es gris, incluidas las fotos, por lo que no revertimos las imágenes */

@keyframes animate-fade-in {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: animate-fade-in 0.2s ease-out forwards;
}
</style>