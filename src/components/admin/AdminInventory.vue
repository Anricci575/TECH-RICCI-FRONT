<script setup>
import { ref, reactive, onMounted } from 'vue'

const inventario = ref([])
const isModalOpen = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

const categorias = ['PC_ENSAMBLADA', 'WORKSTATION', 'LAPTOP', 'COMPONENTE', 'PERIFERICO']

const formData = reactive({
  nombre: '',
  descripcion: '',
  precio: '',
  categoria: categorias[0],
  stock: 1
})

// 1. OBTENER PRODUCTOS (GET)
const fetchInventory = async () => {
  try {
    // Añadimos un parámetro 't' para evitar el caché del navegador
    const response = await fetch(`http://127.0.0.1:8000/api/v1/products/?t=${Date.now()}`)
    
    if (response.ok) {
      const data = await response.json()
      console.log("LOG_SISTEMA: Datos crudos recibidos ->", data)
      
      // Si recibimos un array, lo asignamos directamente
      if (Array.isArray(data)) {
        inventario.value = data
      }
    } else {
      console.error("LOG_SISTEMA: Error en respuesta del servidor")
      loadMockData()
    }
  } catch (error) {
    console.warn("LOG_SISTEMA: Backend desconectado. Usando modo offline.")
    loadMockData()
  }
}

// 2. CREAR PRODUCTO (POST)
const submitProduct = async () => {
  if (!formData.nombre || !formData.precio || !formData.descripcion) {
    errorMessage.value = "Faltan datos críticos para el registro."
    return
  }

  isSubmitting.value = true
  errorMessage.value = ''

  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/products/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        nombre: formData.nombre,
        descripcion: formData.descripcion,
        precio: parseFloat(formData.precio),
        categoria: formData.categoria,
        stock: parseInt(formData.stock)
      })
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.detail || 'Fallo en la comunicación con MySQL')
    }

    // Refrescamos toda la lista desde la DB para asegurar sincronización
    await fetchInventory()
    closeModal()

  } catch (error) {
    console.error("DEBUG_ERROR:", error)
    errorMessage.value = `Error: ${error.message}`
  } finally {
    isSubmitting.value = false
  }
}

const openModal = () => { isModalOpen.value = true }

const closeModal = () => {
  isModalOpen.value = false
  errorMessage.value = ''
  formData.nombre = ''
  formData.descripcion = ''
  formData.precio = ''
  formData.categoria = categorias[0]
  formData.stock = 1
}

const loadMockData = () => {
  // Solo cargamos esto si realmente no hay nada en la DB
  if(inventario.value.length === 0) {
    inventario.value = [
      { id: 'OFF-1', nombre: 'Threadripper Beast', categoria: 'WORKSTATION', precio: '4500.00', stock: 2, status: 'MODO_OFFLINE' },
      { id: 'OFF-2', nombre: 'Dev Studio Laptop', categoria: 'LAPTOP', precio: '2100.00', stock: 5, status: 'MODO_OFFLINE' }
    ]
  }
}

onMounted(fetchInventory)
</script>

<template>
  <div class="glass-card bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] p-6 md:p-8 rounded-[2rem] shadow-2xl w-full text-[var(--color-main-text)] flex flex-col h-full relative">
    
    <div class="mb-4 p-2 bg-black/80 rounded-lg border border-red-500/30 font-mono text-[9px] text-red-400 overflow-hidden">
      <span class="text-white opacity-50 uppercase tracking-tighter">System Debug [DataCount: {{ inventario.length }}]</span>
      <div class="truncate opacity-80 mt-1">> Status: {{ inventario.length > 0 ? 'DATOS_CARGADOS' : 'ESPERANDO_DB' }}</div>
    </div>

    <div class="flex items-center justify-between mb-8 border-b border-[var(--color-glass-border)] pb-4">
      <div class="flex items-center gap-3">
        <div class="w-2 h-2 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,1)]"></div>
        <h2 class="text-xl font-bold uppercase tracking-widest">Data Warehouse</h2>
      </div>
      <button @click="openModal" class="text-[10px] font-mono border border-red-500/50 bg-red-500/10 text-red-500 px-4 py-2 rounded-xl hover:bg-red-500 hover:text-white transition-all uppercase tracking-widest flex items-center gap-2">
        <span class="text-lg leading-none">+</span> Inyectar Equipo
      </button>
    </div>

    <div class="overflow-x-auto flex-1">
      <table class="w-full text-left font-mono text-xs text-[var(--color-main-text)]">
        <thead class="text-[9px] uppercase tracking-widest opacity-50 border-b border-[var(--color-glass-border)]">
          <tr>
            <th class="pb-3 px-2">ID</th>
            <th class="pb-3 px-2">Hardware</th>
            <th class="pb-3 px-2">Categoría</th>
            <th class="pb-3 px-2">Precio (USD)</th>
            <th class="pb-3 px-2 text-right">Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in inventario" :key="item.id || index" class="border-b border-[var(--color-glass-border)] hover:bg-red-500/5 transition-colors">
            <td class="py-4 px-2 opacity-50">#{{ item.id }}</td>
            <td class="py-4 px-2 font-bold">{{ item.nombre }}</td>
            <td class="py-4 px-2 opacity-70">{{ item.categoria }}</td>
            <td class="py-4 px-2 text-red-500 font-bold">${{ item.precio }}</td>
            <td class="py-4 px-2 text-right">
              <span class="px-2 py-1 rounded text-[8px] tracking-widest" :class="item.stock > 0 ? 'bg-green-500/10 text-green-500 border border-green-500/20' : 'bg-red-500/10 text-red-500 border border-red-500/20'">
                {{ item.stock > 0 ? 'ONLINE' : 'SOLD_OUT' }}
              </span>
            </td>
          </tr>
          <tr v-if="inventario.length === 0">
            <td colspan="5" class="py-10 text-center opacity-30 italic">Esperando señal de la base de datos...</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="closeModal"></div>
      <div class="relative w-full max-w-lg bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] p-8 rounded-3xl shadow-2xl animate-fade-in text-[var(--color-main-text)]">
        <h3 class="text-lg font-bold uppercase tracking-widest text-red-500 mb-6">> Nuevo Registro Hardware</h3>
        
        <form @submit.prevent="submitProduct" class="space-y-4 font-mono">
          <div>
            <label class="block text-[10px] opacity-50 mb-1">DESIGNACIÓN</label>
            <input v-model="formData.nombre" type="text" class="w-full bg-black/20 border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm focus:border-red-500 outline-none" required>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[10px] opacity-50 mb-1">PRECIO ($)</label>
              <input v-model="formData.precio" type="number" step="0.01" class="w-full bg-black/20 border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm focus:border-red-500 outline-none" required>
            </div>
            <div>
              <label class="block text-[10px] opacity-50 mb-1">CATEGORÍA</label>
              <select v-model="formData.categoria" class="w-full bg-black/20 border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm outline-none">
                <option v-for="cat in categorias" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-[10px] opacity-50 mb-1">DESCRIPCIÓN TÉCNICA</label>
            <textarea v-model="formData.descripcion" rows="3" class="w-full bg-black/20 border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm focus:border-red-500 outline-none resize-none" required></textarea>
          </div>
          <button type="submit" :disabled="isSubmitting" class="w-full py-4 bg-red-600 hover:bg-red-700 text-white font-bold uppercase tracking-widest rounded-xl transition-all disabled:opacity-50">
            {{ isSubmitting ? 'SINCRONIZANDO...' : 'REGISTRAR EN DB' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>