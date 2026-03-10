import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite' // <-- Importa esto

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(), // <-- Agrégalo aquí
  ],
})