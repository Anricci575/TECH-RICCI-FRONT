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
  customFontBase64: '', // Guardará la fuente subida
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

const activeTab = ref('dark') // 'light' o 'dark'
const uploadError = ref('') // Manejo de errores de carga

// Cargar desde la base de datos local al iniciar
onMounted(() => {
  const savedTheme = localStorage.getItem('techricci_theme_config')
  if (savedTheme) {
    Object.assign(theme, JSON.parse(savedTheme))
  }
  applySettings()
  
  // Observar si el usuario cambia el switch del Navbar
  const observer = new MutationObserver(() => applySettings())
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
})

// FUNCIÓN PARA LEER ARCHIVOS DE FUENTE LOCALES
const handleFontUpload = (event) => {
  uploadError.value = ''
  const file = event.target.files[0]
  if (!file) return

  // Validar tamaño (máximo 2MB para evitar desbordar el localStorage)
  if (file.size > 2 * 1024 * 1024) {
    uploadError.value = 'Archivo muy pesado. Máx 2MB.'
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      // Extraemos el nombre limpio (sin extensión ni caracteres raros)
      const cleanName = file.name.split('.')[0].replace(/[^a-zA-Z0-9]/g, '')
      theme.customFontName = `Custom_${cleanName}`
      theme.customFontBase64 = e.target.result // La fuente en Base64
      theme.font = `"${theme.customFontName}", sans-serif` // Seleccionamos la nueva fuente automáticamente
      
      applySettings()
    } catch (error) {
      uploadError.value = 'Error procesando la fuente.'
    }
  }
  reader.readAsDataURL(file) // Lee el archivo como Data URL
}

// INYECCIÓN PROFESIONAL DE CSS
const applySettings = () => {
  const root = document.documentElement
  const isDark = root.classList.contains('dark')
  const currentMode = isDark ? theme.dark : theme.light

  // 1. Inyectamos las variables de color exactamente como las usa tu tienda
  root.style.setProperty('--color-main-bg', currentMode.bg)
  root.style.setProperty('--color-main-text', currentMode.text)
  root.style.setProperty('--color-glass', currentMode.glass)

  // 2. Fuerza Bruta para la Tipografía (Sobrescribe Tailwind)
  let styleTag = document.getElementById('admin-dynamic-styles')
  if (!styleTag) {
    styleTag = document.createElement('style')
    styleTag.id = 'admin-dynamic-styles'
    document.head.appendChild(styleTag)
  }
  
  // Si hay una fuente personalizada cargada, creamos la regla @font-face
  let customFontFaceRule = ''
  if (theme.customFontBase64 && theme.font.includes(theme.customFontName)) {
    customFontFaceRule = `
      @font-face {
        font-family: '${theme.customFontName}';
        src: url('${theme.customFontBase64}');
      }
    `
  }

  // Esto obliga a que absolutamente todos los textos usen la fuente elegida
  styleTag.innerHTML = `
    ${customFontFaceRule}
    body, h1, h2, h3, h4, h5, p, span, a, button, input, select {
      font-family: ${theme.font} !important;
    }
  `

  // 3. Guardamos el estado para que no se pierda al recargar
  try {
    localStorage.setItem('techricci_theme_config', JSON.stringify(theme))
  } catch (e) {
    console.warn("No se pudo guardar la configuración. Posible exceso de cuota por fuente pesada.")
  }
}

// Escuchar cambios en tiempo real sin tener que darle a "Guardar"
watch(theme, () => {
  applySettings()
}, { deep: true })

// NUEVO RESET ABSOLUTO DE FÁBRICA
const resetDefaults = () => {
  // 1. Restauramos el estado reactivo a los valores originales
  theme.font = fonts[0].value
  theme.customFontName = ''
  theme.customFontBase64 = ''
  theme.light = { bg: '#f4f4f5', text: '#09090b', glass: 'rgba(255, 255, 255, 0.7)' }
  theme.dark = { bg: '#030303', text: '#ffffff', glass: 'rgba(255, 255, 255, 0.05)' }
  
  // 2. Limpiamos la memoria local
  localStorage.removeItem('techricci_theme_config')
  
  // 3. Destruimos la etiqueta de inyección CSS para que Tailwind recupere el control
  const styleTag = document.getElementById('admin-dynamic-styles')
  if (styleTag) {
    styleTag.remove()
  }

  // 4. Forzamos la recarga de las variables originales
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
      
    </div>

    <button @click="resetDefaults" class="w-full py-4 border border-red-500/20 text-red-500 font-mono text-[10px] uppercase tracking-[0.2em] rounded-xl hover:bg-red-500 hover:text-white hover:border-red-500 transition-all">
      Restablecer Parámetros Originales
    </button>

  </div>
</template>