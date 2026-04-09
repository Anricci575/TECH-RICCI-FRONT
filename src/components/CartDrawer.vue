<script setup>
import { cartState, cartTotal, removeFromCart, updateQuantity, toggleCart } from '../store/cart'
import { ref } from 'vue' 
import BillingModal from './BillingModal.vue' 

// --- NUEVO: Control del Modal de Facturación ---
const isBillingOpen = ref(false)

const handlePaymentSuccess = () => {
  cartState.items = [] // Vaciamos el carrito tras pagar
  isBillingOpen.value = false // Cerramos el modal
  toggleCart() // Ocultamos el panel lateral
}
// ----------------------------------------------

const getImageUrl = (path) => {
  if (!path) return null
  return `http://127.0.0.1:8000/${path}`
}
</script>

<template>
  <div>
    <div 
      v-if="cartState.isOpen" 
      @click="toggleCart"
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[90] transition-opacity"
    ></div>

    <div 
      class="fixed top-0 right-0 h-full w-full sm:w-[400px] bg-[var(--color-main-bg)] border-l border-[var(--color-glass-border)] shadow-2xl z-[100] transform transition-transform duration-500 ease-in-out flex flex-col"
      :class="cartState.isOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      <div class="p-6 border-b border-[var(--color-glass-border)] flex justify-between items-center bg-zinc-900/50">
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,1)]"></div>
          <h2 class="text-xl font-bold uppercase tracking-widest text-[var(--color-main-text)]">Terminal_Cart</h2>
        </div>
        <button @click="toggleCart" class="text-zinc-500 hover:text-red-500 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>

      <div class="flex-grow overflow-y-auto p-6 space-y-4 hide-scrollbar">
        <p v-if="cartState.items.length === 0" class="text-center text-zinc-600 font-mono text-xs uppercase tracking-widest mt-10">
          La bandeja de entrada está vacía.
        </p>

        <div v-for="item in cartState.items" :key="item.id" class="flex gap-4 p-3 border border-[var(--color-glass-border)] rounded-xl bg-black/20 group">
          
          <div class="w-20 h-20 bg-zinc-900 rounded-lg overflow-hidden flex items-center justify-center shrink-0 border border-zinc-800">
            <img v-if="item.imagen" :src="getImageUrl(item.imagen)" class="w-full h-full object-contain p-2" />
            <span v-else class="text-2xl">💻</span>
          </div>

          <div class="flex flex-col flex-grow justify-between">
            <div class="flex justify-between items-start">
              <h4 class="text-sm font-bold text-white leading-tight capitalize">{{ item.nombre }}</h4>
              <button @click="removeFromCart(item.id)" class="text-zinc-600 hover:text-red-500 transition-colors">✕</button>
            </div>
            
            <span class="text-red-500 font-mono text-xs font-bold">${{ item.precio }}</span>

            <div class="flex items-center gap-3 mt-2">
              <button @click="updateQuantity(item.id, -1)" class="w-6 h-6 flex items-center justify-center border border-zinc-700 rounded hover:border-red-500 hover:text-red-500 text-zinc-400 transition-colors">-</button>
              <span class="text-xs font-mono text-white">{{ item.quantity }}</span>
              <button @click="updateQuantity(item.id, 1)" class="w-6 h-6 flex items-center justify-center border border-zinc-700 rounded hover:border-red-500 hover:text-red-500 text-zinc-400 transition-colors">+</button>
            </div>
          </div>
        </div>
      </div>

      <div class="p-6 border-t border-[var(--color-glass-border)] bg-zinc-900/50">
        <div class="flex justify-between items-center mb-6">
          <span class="text-xs font-mono text-zinc-400 uppercase tracking-widest">Total Estimado</span>
          <span class="text-2xl font-black text-white">${{ cartTotal.toFixed(2) }}</span>
        </div>
        
        <button 
          @click="isBillingOpen = true"
          :disabled="cartState.items.length === 0"
          class="w-full py-4 bg-red-600 hover:bg-red-500 disabled:bg-zinc-800 disabled:text-zinc-600 text-white font-bold rounded-xl uppercase tracking-widest transition-all hover:shadow-[0_0_20px_rgba(255,0,0,0.4)] flex justify-center items-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Proceder al Pago
        </button>
      </div>
    </div>

    <BillingModal 
      :isOpen="isBillingOpen" 
      :total="cartTotal" 
      @close="isBillingOpen = false"
      @paymentSuccess="handlePaymentSuccess"
    />

  </div>
</template>

<style scoped>
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>