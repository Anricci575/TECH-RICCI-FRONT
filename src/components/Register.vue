<template>
  <div class="relative min-h-screen flex items-center justify-center bg-[#010101] selection:bg-red-500/80 selection:text-white overflow-hidden px-4">
    
    <div class="absolute inset-0 bg-[linear-gradient(to_right,#ffffff05_1px,transparent_1px),linear-gradient(to_bottom,#ffffff05_1px,transparent_1px)] bg-[size:32px_32px] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_40%,transparent_100%)] pointer-events-none"></div>
    <div class="absolute inset-0 bg-[linear-gradient(to_bottom,transparent_50%,rgba(255,0,0,0.05)_50%)] bg-[size:100%_4px] animate-scan pointer-events-none opacity-30"></div>
    
    <div class="absolute top-[-10%] left-[-10%] w-[600px] h-[600px] bg-red-600/10 rounded-full blur-[120px] pointer-events-none animate-[pulse_8s_ease-in-out_infinite]"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-red-900/10 rounded-full blur-[100px] pointer-events-none"></div>

    <div class="absolute left-6 top-1/2 -translate-y-1/2 font-mono text-[9px] text-red-500/30 uppercase tracking-[0.3em] hidden xl:block [writing-mode:vertical-rl] space-y-4 opacity-50">
      <p class="animate-flicker">> SECURE_CONNECTION_ESTABLISHED</p>
      <p>> ENCRYPTION: SHA-256 //> AWAITING_INPUT</p>
    </div>

    <div class="relative z-10 w-full max-w-md">
      
      <div class="text-center mb-10 slide-up" style="animation-delay: 0.1s;">
        <div class="inline-flex items-center gap-3 px-4 py-1.5 rounded-full border border-red-500/20 bg-red-500/5 backdrop-blur-md text-[10px] font-mono text-red-400 uppercase tracking-[0.2em] mb-6">
          <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
          AUTH_GATEWAY
        </div>
        <h1 class="text-4xl font-light tracking-tighter text-white uppercase group">
          <span class="font-serif italic text-red-500 mr-2">System</span> 
          <span class="relative group-hover:animate-chromatic transition-all">Access</span>
        </h1>
      </div>

      <form class="glass-card bg-black/60 backdrop-blur-2xl border border-white/10 p-8 rounded-[2rem] shadow-[0_0_50px_rgba(0,0,0,0.5)] slide-up" style="animation-delay: 0.3s;">
        
        <div class="mb-5 group">
          <label class="block text-[10px] font-mono text-white/50 uppercase tracking-widest mb-2 group-focus-within:text-red-400 transition-colors">
            > Identifier [Username]
          </label>
          <input 
            type="text" 
            class="w-full bg-[#0a0a0a] border border-white/5 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-red-500/50 focus:bg-white/[0.02] transition-all font-mono"
            placeholder="sys_admin_01"
            required
          />
        </div>

        <div class="mb-5 group">
          <label class="block text-[10px] font-mono text-white/50 uppercase tracking-widest mb-2 group-focus-within:text-red-400 transition-colors">
            > Comm_Link [Email]
          </label>
          <input 
            type="email" 
            class="w-full bg-[#0a0a0a] border border-white/5 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-red-500/50 focus:bg-white/[0.02] transition-all font-mono"
            placeholder="user@techricci.dev"
            required
          />
        </div>

        <div class="mb-5 group">
          <label class="block text-[10px] font-mono text-white/50 uppercase tracking-widest mb-2 group-focus-within:text-red-400 transition-colors">
            > Security_Key [Password]
          </label>
          <input 
            type="password" 
            class="w-full bg-[#0a0a0a] border border-white/5 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-red-500/50 focus:bg-white/[0.02] transition-all tracking-[0.3em] font-mono"
            placeholder="••••••••"
            required
          />
        </div>

        <div class="mb-8 group">
          <label class="block text-[10px] font-mono text-white/50 uppercase tracking-widest mb-2 group-focus-within:text-red-400 transition-colors">
            > Access_Level [Role]
          </label>
          <div class="relative">
            <select class="w-full bg-[#0a0a0a] border border-white/5 rounded-xl px-4 py-3 text-sm text-white/80 focus:outline-none focus:border-red-500/50 focus:bg-white/[0.02] transition-all appearance-none font-mono cursor-pointer">
              <option value="user">USER (Standard Access)</option>
              <option value="admin">ROOT (Administrator)</option>
            </select>
            <div class="absolute inset-y-0 right-4 flex items-center pointer-events-none text-red-500 text-xs">▼</div>
          </div>
        </div>

        <button type="submit" class="w-full relative overflow-hidden rounded-xl bg-white/5 border border-white/10 py-4 text-[11px] font-bold text-white uppercase tracking-[0.2em] transition-all duration-500 hover:border-red-500/50 hover:shadow-[0_0_30px_rgba(255,0,0,0.3)] group/btn">
          <span class="relative z-10 transition-transform duration-300 group-hover/btn:scale-105 inline-block group-hover/btn:text-white">Inicializar Registro</span>
          <div class="absolute inset-0 bg-gradient-to-r from-red-800 to-red-600 translate-y-full group-hover/btn:translate-y-0 transition-transform duration-300 ease-out"></div>
        </button>

      </form>

      <p class="text-center text-[10px] font-mono text-white/30 uppercase tracking-widest mt-8 slide-up" style="animation-delay: 0.5s;">
        ¿Ya posees credenciales? <a href="#" class="text-red-500 hover:text-red-400 transition-colors border-b border-red-500/30 pb-0.5">Iniciar Sesión</a>
      </p>

    </div>
  </div>
</template>