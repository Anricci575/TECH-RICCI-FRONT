// src/store/cart.js
import { reactive, computed, watch } from 'vue'

// 1. Estado centralizado del carrito
export const cartState = reactive({
  isOpen: false, // Controla si el panel lateral está abierto
  items: JSON.parse(localStorage.getItem('richitech_cart')) || [] // Carga de memoria si existe
})

// 2. Funciones de acción
export const addToCart = (product) => {
  // Buscamos si el producto ya está en el carrito (por ID)
  const existingItem = cartState.items.find(item => item.id === product.id)
  
  if (existingItem) {
    existingItem.quantity += 1
  } else {
    // Si es nuevo, lo agregamos con cantidad 1
    cartState.items.push({ ...product, quantity: 1 })
  }
  
  // Abrimos el carrito automáticamente al agregar algo
  cartState.isOpen = true
}

export const removeFromCart = (productId) => {
  cartState.items = cartState.items.filter(item => item.id !== productId)
}

export const updateQuantity = (productId, amount) => {
  const item = cartState.items.find(item => item.id === productId)
  if (item) {
    item.quantity += amount
    if (item.quantity <= 0) removeFromCart(productId)
  }
}

export const toggleCart = () => {
  cartState.isOpen = !cartState.isOpen
}

// 3. Cálculos automáticos
export const cartTotal = computed(() => {
  return cartState.items.reduce((total, item) => total + (item.precio * item.quantity), 0)
})

export const cartItemCount = computed(() => {
  return cartState.items.reduce((count, item) => count + item.quantity, 0)
})

// 4. Guardar en memoria automáticamente si hay cambios
watch(() => cartState.items, (newItems) => {
  localStorage.setItem('richitech_cart', JSON.stringify(newItems))
}, { deep: true })