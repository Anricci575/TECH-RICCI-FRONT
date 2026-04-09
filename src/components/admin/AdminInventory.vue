<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

const inventario = ref([])
const isModalOpen = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

// --- NUEVO: Variables para Edición ---
const isEditing = ref(false)
const currentEditId = ref(null)

// Para manejar la previsualización de la imagen
const imagePreview = ref(null)
const fileInputRef = ref(null)

// Control para crear categorías dinámicas
const isCreatingCategory = ref(false)

const categoriasBase = ['PC_ENSAMBLADA', 'LAPTOP', 'COMPONENTE', 'PERIFERICO', 'ROPA_OVERSIZE', 'SERVICIO_TECNICO']
const categorias = ref([...categoriasBase])

const estados = ['🔥 Nuevo', '🛠️ Reacondicionado', '📦 En Espera']
const tiposReparacion = ['No aplica (Solo Venta)', 'Reparación de Hardware', 'Reparación de Software']

const formData = reactive({
  nombre: '',
  descripcion: '',
  precio: '',
  categoria: categorias.value[0],
  estado: estados[0], 
  tipo_reparacion: tiposReparacion[0],
  stock: 1,
  imagen_archivo: null 
})

// --- NUEVO: Buscador y Filtros ---
const searchQuery = ref('')
const selectedCategoryFilter = ref('TODAS')

// Esta es la lista que realmente se muestra en la tabla (filtrada)
const filteredInventario = computed(() => {
  return inventario.value.filter(item => {
    const matchName = item.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchCat = selectedCategoryFilter.value === 'TODAS' || item.categoria === selectedCategoryFilter.value
    return matchName && matchCat
  })
})

// Extraemos las categorías únicas de los productos existentes para el filtro
const availableCategories = computed(() => {
  const cats = new Set(inventario.value.map(i => i.categoria))
  return ['TODAS', ...Array.from(cats)]
})
// ---------------------------------

const fetchInventory = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/products/?t=${Date.now()}`)
    if (response.ok) {
      const data = await response.json()
      if (Array.isArray(data)) {
        inventario.value = data
      }
    } else {
      loadMockData()
    }
  } catch (error) {
    loadMockData()
  }
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    formData.imagen_archivo = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

const triggerFileInput = () => {
  if (fileInputRef.value) fileInputRef.value.click()
}

const toggleCategoryMode = () => {
  isCreatingCategory.value = !isCreatingCategory.value
  if (!isCreatingCategory.value) {
    formData.categoria = categorias.value[0]
  } else {
    formData.categoria = ''
  }
}

// --- NUEVO: Lógica de Edición ---
const openEditModal = (item) => {
  isEditing.value = true
  currentEditId.value = item.id
  errorMessage.value = ''
  isCreatingCategory.value = false

  // Cargar datos básicos
  formData.nombre = item.nombre
  formData.precio = item.precio
  formData.categoria = item.categoria
  formData.stock = item.stock

  // Añadir categoría a la lista si no existe
  if (!categorias.value.includes(item.categoria)) {
    categorias.value.push(item.categoria)
  }

  // Ingeniería Inversa: Separar la descripción empaquetada
  // "[🔥 Nuevo] [Reparación de Hardware] | Pantalla rota..."
  let rawDesc = item.descripcion || ''
  if (rawDesc.includes('|')) {
    const parts = rawDesc.split('|')
    const tagsStr = parts[0]
    formData.descripcion = parts.slice(1).join('|').trim()
    
    const tags = tagsStr.match(/\[(.*?)\]/g)?.map(t => t.replace(/\[|\]/g, '').trim()) || []
    if (tags.length >= 1) formData.estado = tags[0]
    if (tags.length >= 2) formData.tipo_reparacion = tags[1]
  } else {
    formData.descripcion = rawDesc
  }

  // Cargar imagen
  if (item.imagen) {
    imagePreview.value = `http://127.0.0.1:8000/${item.imagen}`
  } else {
    imagePreview.value = null
  }
  formData.imagen_archivo = null // Se queda null a menos que el usuario suba una nueva

  isModalOpen.value = true
}

// --- NUEVO: Lógica de Eliminación ---
const deleteProduct = async (id) => {
  if (!confirm('⚠️ ALERTA DE SISTEMA: ¿Estás seguro de eliminar este activo? Esta acción es irreversible.')) return
  
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/v1/products/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) throw new Error('Fallo al purgar el registro')
    await fetchInventory()
  } catch (error) {
    console.error(error)
    alert("Error: No se pudo eliminar el activo.")
  }
}

const submitProduct = async () => {
  if (!formData.nombre || !formData.precio || !formData.descripcion || !formData.categoria) {
    errorMessage.value = "Faltan datos críticos para el registro."
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  const descripcionCompleta = `[${formData.estado}] [${formData.tipo_reparacion}] | ${formData.descripcion}`

  const dataToSend = new FormData()
  dataToSend.append('nombre', formData.nombre)
  dataToSend.append('descripcion', descripcionCompleta)
  dataToSend.append('precio', parseFloat(formData.precio))
  dataToSend.append('categoria', formData.categoria)
  dataToSend.append('stock', parseInt(formData.stock))
  
  if (formData.imagen_archivo) {
    dataToSend.append('file', formData.imagen_archivo)
  }

  try {
    // Si es edición, usamos PUT y el ID, sino POST normal
    const url = isEditing.value 
      ? `http://127.0.0.1:8000/api/v1/products/${currentEditId.value}`
      : 'http://127.0.0.1:8000/api/v1/products/'
    
    const method = isEditing.value ? 'PUT' : 'POST'

    const response = await fetch(url, {
      method: method,
      headers: { 'Accept': 'application/json' },
      body: dataToSend
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'Fallo en la sincronización de datos')
    }

    if (isCreatingCategory.value && !categorias.value.includes(formData.categoria)) {
      categorias.value.push(formData.categoria)
    }

    await fetchInventory()
    closeModal()

  } catch (error) {
    console.error("DEBUG_ERROR:", error)
    errorMessage.value = `Error: ${error.message}`
  } finally {
    isSubmitting.value = false
  }
}

const openModal = () => { 
  isEditing.value = false // Modo Creación
  isModalOpen.value = true 
}

const closeModal = () => {
  isModalOpen.value = false
  errorMessage.value = ''
  isCreatingCategory.value = false
  isEditing.value = false
  currentEditId.value = null
  
  formData.nombre = ''
  formData.descripcion = ''
  formData.precio = ''
  formData.categoria = categorias.value[0]
  formData.estado = estados[0]
  formData.tipo_reparacion = tiposReparacion[0]
  formData.stock = 1
  formData.imagen_archivo = null
  imagePreview.value = null
  if (fileInputRef.value) fileInputRef.value.value = ''
}

const loadMockData = () => {
  if(inventario.value.length === 0) {
    inventario.value = [
      { id: 'OFF-1', nombre: 'Mock: Playera Over', categoria: 'ROPA_OVERSIZE', precio: '35.00', stock: 10, descripcion: '[🔥 Nuevo] [No aplica (Solo Venta)] | Tela de algodón', status: 'MODO_OFFLINE', imagen: null },
      { id: 'OFF-2', nombre: 'Mock: Servicio Técnico', categoria: 'SERVICIO_TECNICO', precio: '120.00', stock: 1, descripcion: '[🛠️ Reacondicionado] [Reparación de Hardware] | Cambio de placa', status: 'MODO_OFFLINE', imagen: null }
    ]
  }
}

onMounted(fetchInventory)
</script>

<template>
  <div class="glass-card bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] p-6 md:p-8 rounded-[2rem] shadow-2xl w-full text-[var(--color-main-text)] flex flex-col h-full relative">
    
    <div class="mb-4 p-2 bg-black/80 rounded-lg border border-red-500/30 font-mono text-[9px] text-red-400 overflow-hidden flex justify-between items-center">
      <div>
        <span class="text-white opacity-50 uppercase tracking-tighter">System Debug [DataCount: {{ inventario.length }}]</span>
        <div class="truncate opacity-80 mt-1">> Status: {{ inventario.length > 0 ? 'DATOS_CARGADOS' : 'ESPERANDO_DB' }}</div>
      </div>
      <span v-if="searchQuery || selectedCategoryFilter !== 'TODAS'" class="bg-red-500/20 px-2 py-1 rounded text-red-300">
        FILTRANDO: {{ filteredInventario.length }} coincidencia(s)
      </span>
    </div>

    <div class="flex items-center justify-between mb-8 border-b border-[var(--color-glass-border)] pb-4">
      <div class="flex items-center gap-3">
        <div class="w-2 h-2 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,1)]"></div>
        <h2 class="text-xl font-bold uppercase tracking-widest">Data Warehouse</h2>
      </div>
      <button @click="openModal" class="text-[10px] font-mono border border-red-500/50 bg-red-500/10 text-red-500 px-4 py-2 rounded-xl hover:bg-red-500 hover:text-white transition-all uppercase tracking-widest flex items-center gap-2 shadow-[0_0_10px_rgba(255,0,0,0.2)]">
        <span class="text-lg leading-none">+</span> Inyectar Registro
      </button>
    </div>

    <div class="mb-6 flex flex-col md:flex-row gap-4 items-center">
      <div class="relative w-full md:w-2/3">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 opacity-50">🔍</span>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Buscar por designación..." 
          class="w-full bg-black/40 border border-zinc-800 rounded-xl pl-10 pr-4 py-2.5 text-xs font-mono text-white focus:outline-none focus:border-red-500/50 transition-all placeholder:text-zinc-600"
        >
      </div>
      <div class="w-full md:w-1/3 relative">
        <select 
          v-model="selectedCategoryFilter"
          class="w-full bg-black/40 border border-zinc-800 rounded-xl px-4 py-2.5 text-xs font-mono text-white focus:outline-none focus:border-red-500/50 transition-all appearance-none cursor-pointer"
        >
          <option v-for="cat in availableCategories" :key="cat" :value="cat" class="bg-zinc-900">{{ cat }}</option>
        </select>
        <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-zinc-500 text-xs">▼</div>
      </div>
    </div>

    <div class="overflow-x-auto flex-1">
      <table class="w-full text-left font-mono text-xs text-[var(--color-main-text)]">
        <thead class="text-[9px] uppercase tracking-widest opacity-50 border-b border-[var(--color-glass-border)]">
          <tr>
            <th class="pb-3 px-2">IMG</th> 
            <th class="pb-3 px-2">Designación</th>
            <th class="pb-3 px-2">Categoría</th>
            <th class="pb-3 px-2">Monto (USD)</th>
            <th class="pb-3 px-2">Estado</th>
            <th class="pb-3 px-2 text-right">Acciones</th> </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredInventario" :key="item.id" class="border-b border-[var(--color-glass-border)] hover:bg-red-500/5 transition-colors group">
            <td class="py-2 px-2">
              <div class="w-10 h-10 rounded-lg bg-black/50 border border-[var(--color-glass-border)] overflow-hidden flex items-center justify-center">
                <img v-if="item.imagen" :src="`http://127.0.0.1:8000/${item.imagen}`" class="w-full h-full object-cover" />
                <span v-else class="opacity-30 text-[10px]">N/A</span>
              </div>
            </td>
            <td class="py-4 px-2 font-bold">{{ item.nombre }}</td>
            <td class="py-4 px-2 opacity-70">{{ item.categoria }}</td>
            <td class="py-4 px-2 text-red-500 font-bold">${{ item.precio }}</td>
            <td class="py-4 px-2">
              <span class="px-2 py-1 rounded text-[8px] tracking-widest" :class="item.stock > 0 ? 'bg-green-500/10 text-green-500 border border-green-500/20' : 'bg-red-500/10 text-red-500 border border-red-500/20'">
                {{ item.stock > 0 ? 'ONLINE' : 'SOLD_OUT' }}
              </span>
            </td>
            <td class="py-4 px-2 text-right">
              <div class="flex items-center justify-end gap-2 opacity-30 group-hover:opacity-100 transition-opacity">
                <button @click="openEditModal(item)" class="p-1.5 rounded hover:bg-blue-500/20 text-zinc-400 hover:text-blue-400 transition-colors" title="Modificar Activo">
                  ✏️
                </button>
                <button @click="deleteProduct(item.id)" class="p-1.5 rounded hover:bg-red-500/20 text-zinc-400 hover:text-red-500 transition-colors" title="Purgar Activo">
                  🗑️
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="filteredInventario.length === 0">
            <td colspan="6" class="py-10 text-center opacity-30 italic">
              {{ inventario.length === 0 ? 'Esperando señal de la base de datos...' : 'No hay resultados para la búsqueda.' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 grid place-items-center p-4 min-h-screen">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="closeModal"></div>

      <div class="relative w-full max-w-2xl bg-[#0a0a0a] border border-zinc-800 rounded-2xl shadow-[0_0_50px_rgba(255,0,0,0.1)] overflow-hidden flex flex-col max-h-[90vh] animate-fade-in text-[var(--color-main-text)]">
        
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r" :class="isEditing ? 'from-blue-900 via-blue-500 to-blue-900' : 'from-red-900 via-red-500 to-red-900'"></div>

        <div class="p-6 border-b border-zinc-800/80 flex justify-between items-center bg-black/50 z-10 sticky top-0 shrink-0">
          <div>
            <h3 class="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <span :class="isEditing ? 'text-blue-500' : 'text-red-500'">></span> 
              {{ isEditing ? 'Modificación de Activo' : 'Inyección de Activo' }}
            </h3>
            <p class="text-[9px] font-mono text-zinc-500 tracking-[0.2em] mt-1">SISTEMA DE REGISTRO V2.2</p>
          </div>
          <button @click="closeModal" class="text-zinc-500 hover:text-red-500 transition-colors w-8 h-8 flex items-center justify-center rounded-full hover:bg-zinc-900">✕</button>
        </div>

        <div class="p-6 overflow-y-auto flex-grow space-y-6 custom-scrollbar">
          
          <div v-if="errorMessage" class="p-3 border border-red-500/30 bg-red-500/10 text-red-500 text-[9px] font-mono rounded-xl">
            [ERROR SYSTEM] {{ errorMessage }}
          </div>

          <form id="productForm" @submit.prevent="submitProduct" class="space-y-6 font-mono">
            
            <div>
              <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2">Identidad Visual (Imagen)</label>
              <div @click="triggerFileInput" class="w-full h-32 border-2 border-dashed border-zinc-700 hover:border-red-500/50 rounded-xl bg-black/30 flex flex-col items-center justify-center cursor-pointer transition-all group relative overflow-hidden">
                <img v-if="imagePreview" :src="imagePreview" class="absolute inset-0 w-full h-full object-contain p-2 opacity-80 group-hover:opacity-40 transition-opacity" />
                <div class="flex flex-col items-center justify-center z-10" :class="{ 'opacity-0 group-hover:opacity-100': imagePreview }">
                  <svg class="w-6 h-6 text-zinc-500 group-hover:text-red-500 mb-2 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                  <span class="text-[10px] font-mono text-zinc-500 group-hover:text-white uppercase tracking-widest transition-colors">
                    {{ imagePreview ? 'Cambiar Archivo' : 'Clic para seleccionar archivo' }}
                  </span>
                </div>
                <input type="file" ref="fileInputRef" class="hidden" accept="image/*" @change="onFileChange">
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2">Nombre del Producto / Equipo a Reparar</label>
                <input v-model="formData.nombre" type="text" placeholder="Ej: iPhone 13 Pantalla / Playera Oversize" class="w-full bg-black/50 border border-zinc-800 rounded-xl p-3.5 text-xs text-white focus:outline-none focus:border-red-500/50 transition-all placeholder:text-zinc-700" required>
              </div>
              <div>
                <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2">Valor Unidad ($)</label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500 font-mono text-xs">$</span>
                  <input v-model="formData.precio" type="number" step="0.01" placeholder="0.00" class="w-full bg-black/50 border border-zinc-800 rounded-xl p-3.5 pl-7 text-xs text-white focus:outline-none focus:border-red-500/50 transition-all placeholder:text-zinc-700" required>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2">Categoría</label>
                <div class="flex gap-2">
                  <div class="relative flex-grow">
                    <input 
                      v-if="isCreatingCategory" 
                      v-model="formData.categoria" 
                      type="text" 
                      placeholder="Escribe la categoría..." 
                      class="w-full bg-black/50 border border-zinc-800 rounded-xl p-3.5 text-xs text-white focus:outline-none focus:border-red-500/50 transition-all" 
                      required
                    >
                    <select 
                      v-else 
                      v-model="formData.categoria" 
                      class="w-full bg-black/50 border border-zinc-800 rounded-xl p-3.5 text-xs text-white focus:outline-none focus:border-red-500/50 transition-all appearance-none cursor-pointer"
                    >
                      <option v-for="cat in categorias" :key="cat" :value="cat" class="bg-zinc-900">{{ cat }}</option>
                    </select>
                    <div v-if="!isCreatingCategory" class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-zinc-500">▼</div>
                  </div>
                  <button 
                    type="button" 
                    @click="toggleCategoryMode" 
                    class="shrink-0 w-11 bg-black/50 border border-zinc-800 rounded-xl flex items-center justify-center text-zinc-400 hover:text-red-500 hover:border-red-500 transition-colors" 
                    :title="isCreatingCategory ? 'Cancelar' : 'Crear Nueva Categoría'"
                  >
                    {{ isCreatingCategory ? '✕' : '➕' }}
                  </button>
                </div>
              </div>

              <div>
                <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2">Estado</label>
                <div class="relative">
                  <select v-model="formData.estado" class="w-full bg-black/50 border border-zinc-800 rounded-xl p-3.5 text-xs text-red-400 focus:outline-none focus:border-red-500/50 transition-all appearance-none cursor-pointer">
                    <option v-for="est in estados" :key="est" :value="est" class="bg-zinc-900">{{ est }}</option>
                  </select>
                  <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-zinc-500">▼</div>
                </div>
              </div>
            </div>

            <div>
              <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2 text-center">Tipo de Reparación (Selecciona si aplica)</label>
              <div class="flex flex-col sm:flex-row gap-2 bg-black/40 p-1.5 rounded-xl border border-zinc-800/80">
                <button 
                  type="button"
                  v-for="(tipo, index) in tiposReparacion" 
                  :key="index"
                  @click="formData.tipo_reparacion = tipo"
                  class="flex-1 py-2.5 rounded-lg text-[9px] font-mono uppercase tracking-widest transition-all duration-300 flex items-center justify-center gap-1.5"
                  :class="formData.tipo_reparacion === tipo ? 'bg-red-500/10 text-red-500 border border-red-500/30 shadow-[0_0_10px_rgba(255,0,0,0.1)]' : 'text-zinc-500 hover:text-zinc-300 border border-transparent'"
                >
                  <span v-if="tipo.includes('Venta')">🚫</span>
                  <span v-if="tipo.includes('Hardware')">⚙️</span>
                  <span v-if="tipo.includes('Software')">💻</span>
                  {{ tipo }}
                </button>
              </div>
            </div>

            <div>
              <label class="block text-[9px] uppercase text-zinc-400 tracking-widest mb-2">Detalles / Síntomas Técnicos</label>
              <textarea v-model="formData.descripcion" rows="2" placeholder="Ej: Pantalla rota, incluye cargador, falla al iniciar..." class="w-full bg-black/50 border border-zinc-800 rounded-xl p-3.5 text-xs text-white focus:outline-none focus:border-red-500/50 transition-all placeholder:text-zinc-700 resize-none" required></textarea>
            </div>

          </form>
        </div>

        <div class="p-6 border-t border-zinc-800/80 bg-black/50 shrink-0">
          <button form="productForm" type="submit" :disabled="isSubmitting" class="relative w-full py-4 text-white font-bold rounded-xl overflow-hidden group/btn transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed" :class="isEditing ? 'bg-blue-600 hover:bg-blue-500 shadow-[0_0_20px_rgba(37,99,235,0.3)]' : 'bg-red-600 hover:bg-red-500 shadow-[0_0_20px_rgba(220,38,38,0.3)]'">
            <span class="relative z-10 uppercase text-xs tracking-widest flex items-center justify-center gap-2">
              <svg v-if="!isSubmitting" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span v-if="isSubmitting" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              {{ isSubmitting ? 'SINCRONIZANDO...' : (isEditing ? 'ACTUALIZAR REGISTRO' : 'REGISTRAR OPERACIÓN') }}
            </span>
            <div class="absolute inset-0 bg-gradient-to-r translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 z-0" :class="isEditing ? 'from-blue-500 to-blue-400' : 'from-red-500 to-red-400'"></div>
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
.animate-fade-in {
  animation: fade-in 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: #3f3f46; border-radius: 10px; }
.custom-scrollbar:hover::-webkit-scrollbar-thumb { background-color: #ef4444; }

.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>