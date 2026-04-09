<script setup>
import { ref, reactive, onMounted, watch } from 'vue'

// Opciones Tipográficas Profesionales
const fonts = [
  { name: 'Inter (UI Moderna)', value: "'Inter', sans-serif" },
  { name: 'Space Mono (Terminal)', value: "'Space Mono', monospace" },
  { name: 'Syncopate (Agresiva/Ancha)', value: "'Syncopate', sans-serif" },
  { name: 'Playfair Display (Elegante)', value: "'Playfair Display', serif" }
]

// Estado Reactivo Centralizado
const theme = reactive({
  font: fonts[0].value,
  customFontName: '',
  customFontBase64: '', 
  light: {
    bg: '#f4f4f5',
    text: '#09090b',
    glass: 'rgba(255, 255, 255, 0.7)'
  },
  dark: {
    bg: '#030303',
    text: '#ffffff',
    glass: 'rgba(255, 255, 255, 0.05)'
  }
})

const activeTab = ref('dark') 
const uploadError = ref('') 

// --- NUEVO: SISTEMA DE PALETAS ---
const paletasGuardadas = ref([])

// Cargar desde la base de datos local al iniciar
onMounted(() => {
  const savedTheme = localStorage.getItem('techricci_theme_config')
  if (savedTheme) {
    Object.assign(theme, JSON.parse(savedTheme))
  }
  applySettings()
  
  // Cargar Paletas Guardadas
  const savedPalettes = localStorage.getItem('techricci_palettes')
  if (savedPalettes) {
    paletasGuardadas.value = JSON.parse(savedPalettes)
  } else {
    // Paletas por defecto de inspiración Tech
    paletasGuardadas.value = [
      { id: 1, bg: '#030303', text: '#ffffff', name: 'Dark Default' },
      { id: 2, bg: '#0A0F1A', text: '#60A5FA', name: 'Deep Blue' },
      { id: 3, bg: '#18181B', text: '#A1A1AA', name: 'Terminal' }
    ]
  }
  
  const observer = new MutationObserver(() => applySettings())
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
})

// --- NUEVAS FUNCIONES DE PALETAS ---
const guardarPaletaActual = () => {
  const currentBg = theme[activeTab.value].bg
  const currentText = theme[activeTab.value].text

  // Evitar duplicados exactos
  const existe = paletasGuardadas.value.find(p => p.bg === currentBg && p.text === currentText)
  if (existe) return 

  const nuevaPaleta = {
    id: Date.now(),
    bg: currentBg,
    text: currentText,
    name: `Custom ${paletasGuardadas.value.length + 1}`
  }
  
  paletasGuardadas.value.push(nuevaPaleta)
  localStorage.setItem('techricci_palettes', JSON.stringify(paletasGuardadas.value))
}

const aplicarPaleta = (paleta) => {
  // Aplica la paleta a la pestaña que esté activa (Light o Dark)
  theme[activeTab.value].bg = paleta.bg
  theme[activeTab.value].text = paleta.text
  // El watch(theme) se encargará de inyectar el CSS automáticamente
}

const borrarPaleta = (id) => {
  paletasGuardadas.value = paletasGuardadas.value.filter(p => p.id !== id)
  localStorage.setItem('techricci_palettes', JSON.stringify(paletasGuardadas.value))
}
// ------------------------------------

const handleFontUpload = (event) => {
  uploadError.value = ''
  const file = event.target.files[0]
  if (!file) return

  if (file.size > 2 * 1024 * 1024) {
    uploadError.value = 'Archivo muy pesado. Máx 2MB.'
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const cleanName = file.name.split('.')[0].replace(/[^a-zA-Z0-9]/g, '')
      theme.customFontName = `Custom_${cleanName}`
      theme.customFontBase64 = e.target.result 
      theme.font = `"${theme.customFontName}", sans-serif` 
      
      applySettings()
    } catch (error) {
      uploadError.value = 'Error procesando la fuente.'
    }
  }
  reader.readAsDataURL(file) 
}

const applySettings = () => {
  const root = document.documentElement
  const isDark = root.classList.contains('dark')
  const currentMode = isDark ? theme.dark : theme.light

  root.style.setProperty('--color-main-bg', currentMode.bg)
  root.style.setProperty('--color-main-text', currentMode.text)
  root.style.setProperty('--color-glass', currentMode.glass)

  let styleTag = document.getElementById('admin-dynamic-styles')
  if (!styleTag) {
    styleTag = document.createElement('style')
    styleTag.id = 'admin-dynamic-styles'
    document.head.appendChild(styleTag)
  }
  
  let customFontFaceRule = ''
  if (theme.customFontBase64 && theme.font.includes(theme.customFontName)) {
    customFontFaceRule = `
      @font-face {
        font-family: '${theme.customFontName}';
        src: url('${theme.customFontBase64}');
      }
    `
  }

  styleTag.innerHTML = `
    ${customFontFaceRule}
    body, h1, h2, h3, h4, h5, p, span, a, button, input, select {
      font-family: ${theme.font} !important;
    }
  `

  try {
    localStorage.setItem('techricci_theme_config', JSON.stringify(theme))
  } catch (e) {
    console.warn("No se pudo guardar la configuración. Posible exceso de cuota por fuente pesada.")
  }
}

watch(theme, () => {
  applySettings()
}, { deep: true })

const resetDefaults = () => {
  theme.font = fonts[0].value
  theme.customFontName = ''
  theme.customFontBase64 = ''
  theme.light = { bg: '#f4f4f5', text: '#09090b', glass: 'rgba(255, 255, 255, 0.7)' }
  theme.dark = { bg: '#030303', text: '#ffffff', glass: 'rgba(255, 255, 255, 0.05)' }
  
  localStorage.removeItem('techricci_theme_config')
  
  const styleTag = document.getElementById('admin-dynamic-styles')
  if (styleTag) {
    styleTag.remove()
  }

  applySettings()
}
</script>

<template>
  <div class="glass-card bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] p-6 md:p-8 rounded-[2rem] shadow-2xl w-full text-[var(--color-main-text)]">
    
    <div class="flex items-center justify-between mb-8 border-b border-[var(--color-glass-border)] pb-4">
      <div class="flex items-center gap-3">
        <div class="w-2 h-2 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,1)]"></div>
        <h2 class="text-xl font-bold uppercase tracking-widest">Global Appearance</h2>
      </div>
      <span class="text-[9px] font-mono opacity-50 border border-[var(--color-glass-border)] px-2 py-1 rounded">LIVE SYNC</span>
    </div>

    <div class="mb-10">
      <label class="block text-[10px] font-mono opacity-60 uppercase tracking-widest mb-3">
        > Tipografía Maestra
      </label>
      
      <div class="relative group mb-4">
        <select v-model="theme.font" class="w-full bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-xl px-4 py-4 text-sm font-bold text-[var(--color-main-text)] focus:outline-none focus:border-red-500/50 transition-all appearance-none cursor-pointer group-hover:border-[var(--color-main-text)]/30">
          <option v-for="font in fonts" :key="font.value" :value="font.value">{{ font.name }}</option>
          <option v-if="theme.customFontName" :value="`'${theme.customFontName}', sans-serif`">
            [ PERSONALIZADA ] {{ theme.customFontName }}
          </option>
        </select>
        <div class="absolute inset-y-0 right-5 flex items-center pointer-events-none text-red-500">▼</div>
      </div>

      <div class="relative mt-4">
        <input type="file" accept=".ttf,.woff,.woff2,.otf" @change="handleFontUpload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10">
        <div class="w-full py-3 border border-dashed border-[var(--color-glass-border)] rounded-xl flex items-center justify-center gap-2 hover:border-red-500/50 transition-colors bg-[var(--color-main-bg)]/50 group">
          <span class="text-xs font-mono uppercase tracking-widest opacity-60 group-hover:text-red-500 transition-colors group-hover:opacity-100">Subir fuente externa (.ttf, .woff)</span>
        </div>
      </div>
      <p v-if="uploadError" class="text-[9px] text-red-500 font-mono mt-2 tracking-widest">{{ uploadError }}</p>
    </div>

    <div class="flex gap-2 mb-6 bg-[var(--color-main-bg)] p-1 rounded-xl border border-[var(--color-glass-border)]">
      <button 
        @click="activeTab = 'dark'" 
        :class="activeTab === 'dark' ? 'bg-[var(--color-glass)] border border-red-500/30 text-red-500 shadow-md' : 'opacity-50 hover:opacity-100'"
        class="flex-1 py-2 text-xs font-mono uppercase tracking-widest rounded-lg transition-all"
      >
        Dark Mode
      </button>
      <button 
        @click="activeTab = 'light'" 
        :class="activeTab === 'light' ? 'bg-[var(--color-glass)] border border-red-500/30 text-red-500 shadow-md' : 'opacity-50 hover:opacity-100'"
        class="flex-1 py-2 text-xs font-mono uppercase tracking-widest rounded-lg transition-all"
      >
        Light Mode
      </button>
    </div>

    <div class="space-y-6 mb-10 p-6 border border-[var(--color-glass-border)] rounded-2xl bg-[var(--color-main-bg)]/30">
      
      <div class="flex items-center justify-between">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-wider mb-1">Color de Fondo</label>
          <p class="text-[9px] font-mono opacity-50">Main Background (bg)</p>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-xs font-mono opacity-60 uppercase w-16 text-right">{{ theme[activeTab].bg }}</span>
          <div class="relative w-10 h-10 rounded-full overflow-hidden border-2 border-[var(--color-glass-border)] shadow-inner cursor-pointer hover:scale-105 transition-transform">
            <input type="color" v-model="theme[activeTab].bg" class="absolute top-[-50%] left-[-50%] w-[200%] h-[200%] cursor-pointer">
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between border-t border-[var(--color-glass-border)] pt-6">
        <div>
          <label class="block text-[11px] font-bold uppercase tracking-wider mb-1">Color de Texto</label>
          <p class="text-[9px] font-mono opacity-50">Main Text Color (letras)</p>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-xs font-mono opacity-60 uppercase w-16 text-right">{{ theme[activeTab].text }}</span>
          <div class="relative w-10 h-10 rounded-full overflow-hidden border-2 border-[var(--color-glass-border)] shadow-inner cursor-pointer hover:scale-105 transition-transform">
            <input type="color" v-model="theme[activeTab].text" class="absolute top-[-50%] left-[-50%] w-[200%] h-[200%] cursor-pointer">
          </div>
        </div>
      </div>
      
      <div class="border-t border-[var(--color-glass-border)] pt-6 mt-6">
        <div class="flex justify-between items-center mb-4">
          <div>
            <label class="block text-[11px] font-bold uppercase tracking-wider mb-1">Paletas Guardadas</label>
            <p class="text-[9px] font-mono opacity-50">Presets Rápidos</p>
          </div>
          <button @click="guardarPaletaActual" class="text-[9px] font-mono flex items-center gap-2 text-red-500 hover:text-white border border-red-500/30 hover:border-red-500/80 hover:bg-red-500/20 px-3 py-1.5 rounded-lg transition-all uppercase tracking-widest">
            <span>+</span> Guardar
          </button>
        </div>

        <div class="flex gap-3 overflow-x-auto pb-2 hide-scrollbar">
          
          <div 
            v-for="paleta in paletasGuardadas" 
            :key="paleta.id"
            class="group relative shrink-0 flex items-center border-2 border-[var(--color-glass-border)] hover:border-red-500/50 rounded-xl p-1 cursor-pointer transition-all hover:scale-105"
            @click="aplicarPaleta(paleta)"
            title="Clic para aplicar"
          >
            <div class="w-10 h-10 rounded-lg overflow-hidden flex shadow-inner border border-black/50">
              <div class="w-1/2 h-full" :style="{ backgroundColor: paleta.bg }"></div>
              <div class="w-1/2 h-full relative" :style="{ backgroundColor: paleta.text }">
                 <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold opacity-90" :style="{ color: paleta.bg }">A</span>
              </div>
            </div>
            
            <button 
              @click.stop="borrarPaleta(paleta.id)" 
              class="absolute -top-2 -right-2 bg-[var(--color-main-bg)] border border-red-500 text-red-500 hover:bg-red-500 hover:text-white w-5 h-5 rounded-full flex items-center justify-center text-[10px] opacity-0 group-hover:opacity-100 transition-all shadow-lg z-10"
              title="Borrar Paleta"
            >
              ✕
            </button>
          </div>

          <p v-if="paletasGuardadas.length === 0" class="text-[10px] font-mono opacity-50 italic my-2 w-full py-2">
            Sin paletas guardadas.
          </p>
        </div>
      </div>
      </div>

    <button @click="resetDefaults" class="w-full py-4 border border-red-500/20 text-red-500 font-mono text-[10px] uppercase tracking-[0.2em] rounded-xl hover:bg-red-500 hover:text-white hover:border-red-500 transition-all">
      Restablecer Parámetros Originales
    </button>

  </div>
</template>

<style scoped>
/* Ocultar barra de scroll para el slider de paletas */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>