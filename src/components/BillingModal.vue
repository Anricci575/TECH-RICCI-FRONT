<script setup>
import { ref } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  total: Number
})

const emit = defineEmits(['close', 'paymentSuccess'])

const step = ref(1) // 1: Formulario, 2: Procesando, 3: Factura
const formData = ref({
  nombre: '',
  documento: '',
  metodo: 'pago_movil'
})

const simularPago = () => {
  step.value = 2
  // Simulamos un tiempo de conexión con el banco
  setTimeout(() => {
    step.value = 3
  }, 2500)
}

const cerrar = () => {
  step.value = 1
  formData.value = { nombre: '', documento: '', metodo: 'pago_movil' }
  emit('close')
}

const finalizar = () => {
  emit('paymentSuccess')
  cerrar()
}
</script>

<template>
  <div v-if="isOpen" class="fixed inset-0 z-[200] flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-black/80 backdrop-blur-md" @click="cerrar"></div>

    <div class="glass-card relative w-full max-w-md bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-2xl shadow-2xl overflow-hidden text-[var(--color-main-text)]">
      
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-800 to-red-500"></div>
      <div class="absolute inset-0 bg-grid-tech opacity-10 pointer-events-none"></div>

      <div class="p-6 relative z-10">
        
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-lg font-bold tracking-widest uppercase">Módulo de Facturación</h2>
            <p class="text-[10px] font-mono text-zinc-500">SIMULACIÓN DE ENTORNO SEGURO</p>
          </div>
          <button v-if="step !== 2" @click="cerrar" class="text-zinc-500 hover:text-red-500 transition-colors">✕</button>
        </div>

        <div v-if="step === 1" class="space-y-4">
          <div>
            <label class="block text-[10px] font-mono uppercase text-zinc-400 mb-1">Razón Social / Nombre</label>
            <input v-model="formData.nombre" type="text" class="w-full bg-black/50 border border-zinc-800 rounded-lg p-3 text-sm focus:outline-none focus:border-red-500/50 transition-colors" placeholder="Ej. Inversiones Tech C.A.">
          </div>
          
          <div>
            <label class="block text-[10px] font-mono uppercase text-zinc-400 mb-1">Cédula / RIF</label>
            <input v-model="formData.documento" type="text" class="w-full bg-black/50 border border-zinc-800 rounded-lg p-3 text-sm focus:outline-none focus:border-red-500/50 transition-colors" placeholder="Ej. J-12345678-9">
          </div>

          <div>
            <label class="block text-[10px] font-mono uppercase text-zinc-400 mb-1">Método de Pago</label>
            <select v-model="formData.metodo" class="w-full bg-black/50 border border-zinc-800 rounded-lg p-3 text-sm focus:outline-none focus:border-red-500/50 transition-colors appearance-none cursor-pointer">
              <option value="pago_movil">Pago Móvil</option>
              <option value="transferencia">Transferencia Bancaria</option>
              <option value="binance">Binance Pay (USDT)</option>
              <option value="zelle">Zelle</option>
            </select>
          </div>

          <div class="mt-6 pt-4 border-t border-zinc-800/50 flex justify-between items-center">
            <span class="text-xs font-mono text-zinc-400 uppercase tracking-widest">Total a Pagar</span>
            <span class="text-xl font-bold text-red-500">${{ total.toFixed(2) }}</span>
          </div>

          <button @click="simularPago" :disabled="!formData.nombre || !formData.documento" class="w-full mt-4 py-3 bg-white text-black hover:bg-zinc-200 disabled:opacity-50 disabled:cursor-not-allowed font-bold rounded-xl uppercase tracking-widest text-xs transition-all flex justify-center items-center gap-2">
            Procesar Transacción
          </button>
        </div>

        <div v-if="step === 2" class="py-10 flex flex-col items-center justify-center space-y-4">
          <div class="w-12 h-12 border-4 border-zinc-800 border-t-red-500 rounded-full animate-spin"></div>
          <p class="text-xs font-mono uppercase tracking-widest text-zinc-400 animate-pulse">Contactando pasarela bancaria...</p>
        </div>

        <div v-if="step === 3" class="py-6 flex flex-col items-center text-center space-y-4">
          <div class="w-16 h-16 bg-green-500/10 border border-green-500/30 rounded-full flex items-center justify-center text-green-500 mb-2 shadow-[0_0_20px_rgba(34,197,94,0.2)]">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
          </div>
          <h3 class="text-xl font-bold text-white uppercase tracking-widest">Pago Aprobado</h3>
          
          <div class="w-full bg-black/40 border border-zinc-800 rounded-lg p-4 text-left font-mono text-xs space-y-2">
            <p class="flex justify-between"><span class="text-zinc-500">Nº Factura:</span> <span>#TR-{{ Math.floor(Math.random() * 90000) + 10000 }}</span></p>
            <p class="flex justify-between"><span class="text-zinc-500">Cliente:</span> <span>{{ formData.nombre }}</span></p>
            <p class="flex justify-between"><span class="text-zinc-500">RIF/CI:</span> <span>{{ formData.documento }}</span></p>
            <p class="flex justify-between"><span class="text-zinc-500">Monto:</span> <span class="text-red-400 font-bold">${{ total.toFixed(2) }}</span></p>
            <p class="flex justify-between border-t border-zinc-800 pt-2 mt-2"><span class="text-zinc-500">Estado:</span> <span class="text-green-500">PAGADO</span></p>
          </div>

          <button @click="finalizar" class="w-full mt-2 py-3 border border-zinc-700 hover:border-white text-zinc-300 hover:text-white font-bold rounded-xl uppercase tracking-widest text-xs transition-all">
            Cerrar y Limpiar Carrito
          </button>
        </div>

      </div>
    </div>
  </div>
</template>