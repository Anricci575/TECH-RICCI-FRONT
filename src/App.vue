<template>
  <router-view />
</template>

<style>
/* Deja aquí TODAS las animaciones globales que tenías (@keyframes scan, slide-up, etc.) */
/* y las clases de ocultar scrollbar */
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

/* ... pega aquí el resto de tus keyframes de App.vue ... */
</style>