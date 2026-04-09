<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from './ThemeToggle.vue'

const router = useRouter()
const isLogin = ref(true)

const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('user')
const errorMessage = ref('')

const toggleMode = () => {
  isLogin.value = !isLogin.value
  errorMessage.value = ''
}

const handleSubmit = async () => {
  errorMessage.value = '' 
  
  try {
    if (!isLogin.value) {
      // ---> LÓGICA DE REGISTRO REAL <---
      const response = await fetch('/api/v1/users/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: username.value,
          email: email.value,
          password: password.value,
          role: role.value
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Error en el sistema central. Reintente.')
      }

      const data = await response.json()
      console.log("Usuario registrado en DB:", data)
      
      localStorage.setItem('techricci_session', `token_${data.id}`)
      localStorage.setItem('techricci_username', data.username) 
      localStorage.setItem('techricci_role', data.role || role.value) // Aseguramos guardar el rol al registrar
      
      // Si el que se acaba de registrar es admin, va al panel; si no, a la tienda.
      if (role.value === 'admin') {
        router.push('/admin')
      } else {
        router.push('/store')
      }

    } else {
      // ---> LÓGICA DE LOGIN REAL <---
      const response = await fetch('http://127.0.0.1:8000/api/v1/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.value,
          password: password.value
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Acceso Denegado: Credenciales Inválidas.')
      }

      const data = await response.json()
      console.log("Acceso concedido:", data.message)
      
      localStorage.setItem('techricci_session', `token_${data.user.id}`)
      localStorage.setItem('techricci_role', data.user.role)
      localStorage.setItem('techricci_username', data.user.username || email.value.split('@')[0])
      
      // ---> LA MAGIA SUCEDE AQUÍ <---
      // Evaluamos el rol devuelto por la Base de Datos
      if (data.user.role === 'admin') {
        router.push('/admin') // Ruta del Panel de Control
      } else {
        router.push('/store') // Ruta de la Tienda de Usuarios
      }
    }
  } catch (error) {
    console.error("Fallo de conexión:", error)
    errorMessage.value = error.message
  }
}
</script>

<template>
  <div class="relative min-h-screen bg-[var(--color-main-bg)] text-[var(--color-main-text)] transition-colors duration-500 selection:bg-red-500/80 selection:text-white overflow-hidden flex flex-col lg:flex-row">
    
    <div class="absolute top-6 right-6 z-50">
      <ThemeToggle />
    </div>

    <div class="absolute inset-0 bg-grid-tech opacity-30 pointer-events-none"></div>
    <div class="absolute inset-0 bg-[linear-gradient(to_bottom,transparent_50%,rgba(255,0,0,0.05)_50%)] bg-[size:100%_4px] animate-scan pointer-events-none opacity-20 dark:opacity-40"></div>

    <div class="relative w-full lg:w-1/2 p-8 md:p-16 flex flex-col justify-between border-b lg:border-b-0 lg:border-r border-[var(--color-glass-border)] z-10 bg-[var(--color-main-bg)]/40 backdrop-blur-sm">
      
      <div class="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-red-600/10 rounded-full blur-[120px] pointer-events-none mix-blend-multiply dark:mix-blend-screen"></div>

      <div>
        <div class="flex items-center gap-2 text-2xl font-bold tracking-tighter mb-12 slide-up">
          <div class="w-3 h-3 bg-red-600 rounded-full animate-pulse shadow-[0_0_10px_rgba(255,0,0,0.8)]"></div>
          TECH<span class="font-light">RICCI</span>
        </div>

        <h1 class="text-5xl md:text-7xl font-light tracking-tighter uppercase leading-[0.9] mb-6 slide-up" style="animation-delay: 0.2s;">
          <span class="font-serif italic text-red-500">Hardware</span> <br>
          Insurgency.
        </h1>
        
        <p class="opacity-50 max-w-md text-sm leading-relaxed font-mono slide-up transition-opacity" style="animation-delay: 0.3s;">
          > Acceso restringido al portal de despliegue y ensamblaje táctico. <br><br>
          > Optimizamos infraestructura a nivel de componentes y sistemas operativos de alta eficiencia. Solo personal autorizado.
        </p>
      </div>

      <div class="font-mono text-[10px] opacity-40 uppercase tracking-[0.2em] space-y-2 slide-up transition-opacity" style="animation-delay: 0.4s;">
        <p class="flex justify-between border-b border-[var(--color-glass-border)] pb-2"><span>Status:</span> <span class="text-red-500 font-bold opacity-100">SYSTEM_ONLINE</span></p>
        <p class="flex justify-between border-b border-[var(--color-glass-border)] pb-2"><span>Nodos Activos:</span> <span>500+</span></p>
        <p class="flex justify-between pb-2"><span>Cifrado:</span> <span>SHA-256</span></p>
      </div>
    </div>

    <div class="relative w-full lg:w-1/2 flex items-center justify-center p-8 z-10">
      
      <div class="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-red-900/10 dark:bg-red-900/20 rounded-full blur-[100px] pointer-events-none mix-blend-multiply dark:mix-blend-screen"></div>

      <div class="w-full max-w-md">
        
        <div class="text-center mb-8 slide-up" style="animation-delay: 0.1s;">
          <div class="inline-flex items-center gap-3 px-4 py-1.5 rounded-full border border-red-500/20 bg-red-500/5 backdrop-blur-md text-[10px] font-mono text-red-600 dark:text-red-400 uppercase tracking-[0.2em] mb-6">
            <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
            AUTH_GATEWAY
          </div>
          <h2 class="text-3xl font-light tracking-tighter uppercase group">
            <span class="font-serif italic text-red-500 mr-2">System</span> 
            <span class="relative group-hover:animate-chromatic transition-all">Access</span>
          </h2>
        </div>

        <form @submit.prevent="handleSubmit" class="glass-card bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] p-8 rounded-[2rem] shadow-xl dark:shadow-[0_0_50px_rgba(0,0,0,0.5)] slide-up transition-all duration-500" style="animation-delay: 0.3s;">
          
          <div v-if="errorMessage" class="mb-5 p-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-600 dark:text-red-400 text-[10px] font-mono tracking-widest uppercase text-center">
            [ERROR] {{ errorMessage }}
          </div>
          
          <div v-if="!isLogin" class="mb-5 group">
            <label class="block text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2 group-focus-within:text-red-500 transition-colors">
              > Identifier [Username]
            </label>
            <input v-model="username" type="text" class="w-full bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm text-[var(--color-main-text)] focus:outline-none focus:border-red-500/50 transition-all font-mono" placeholder="sys_admin_01" :required="!isLogin" />
          </div>

          <div class="mb-5 group">
            <label class="block text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2 group-focus-within:text-red-500 transition-colors">
              > Comm_Link [Email]
            </label>
            <input v-model="email" type="email" class="w-full bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm text-[var(--color-main-text)] focus:outline-none focus:border-red-500/50 transition-all font-mono" placeholder="user@techricci.dev" required />
          </div>

          <div class="mb-5 group">
            <label class="block text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2 group-focus-within:text-red-500 transition-colors">
              > Security_Key [Password]
            </label>
            <input v-model="password" type="password" class="w-full bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm text-[var(--color-main-text)] focus:outline-none focus:border-red-500/50 transition-all tracking-[0.3em] font-mono" placeholder="••••••••" required />
          </div>

          <div v-if="!isLogin" class="mb-8 group">
            <label class="block text-[10px] font-mono opacity-50 uppercase tracking-widest mb-2 group-focus-within:text-red-500 transition-colors">
              > Access_Level [Role]
            </label>
            <div class="relative">
              <select v-model="role" class="w-full bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-xl px-4 py-3 text-sm text-[var(--color-main-text)] opacity-80 focus:outline-none focus:border-red-500/50 transition-all appearance-none font-mono cursor-pointer">
                <option value="user">USER (Standard Access)</option>
                <option value="admin">ROOT (Administrator)</option>
              </select>
              <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none text-red-500 text-xs">▼</div>
            </div>
          </div>

          <button type="submit" class="w-full relative overflow-hidden rounded-xl bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] py-4 text-[11px] font-bold uppercase tracking-[0.2em] transition-all duration-500 hover:border-red-500/50 hover:shadow-[0_0_30px_rgba(255,0,0,0.3)] group/btn mt-4">
            <span class="relative z-10 transition-transform duration-300 group-hover/btn:scale-105 inline-block group-hover/btn:text-white">
              {{ isLogin ? 'Ejecutar Acceso' : 'Inicializar Registro' }}
            </span>
            <div class="absolute inset-0 bg-gradient-to-r from-red-800 to-red-600 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 ease-out z-0"></div>
          </button>

        </form>

        <p class="text-center text-[10px] font-mono opacity-40 uppercase tracking-widest mt-8 slide-up cursor-pointer transition-opacity" style="animation-delay: 0.5s;">
          <span v-if="isLogin">
            ¿No tienes credenciales? <a @click.prevent="toggleMode" class="text-red-500 hover:text-red-400 transition-colors border-b border-red-500/30 pb-0.5 opacity-100">Solicitar Acceso</a>
          </span>
          <span v-else>
            ¿Ya posees credenciales? <a @click.prevent="toggleMode" class="text-red-500 hover:text-red-400 transition-colors border-b border-red-500/30 pb-0.5 opacity-100">Iniciar Sesión</a>
          </span>
        </p>

      </div>
    </div>
  </div>
</template>