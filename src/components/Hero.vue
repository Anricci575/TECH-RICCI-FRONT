<template>
  <section class="relative min-h-screen pt-32 pb-20 px-6 md:px-12 overflow-hidden flex items-center bg-[var(--color-main-bg)] text-[var(--color-main-text)] transition-colors duration-500">
    
    <div class="absolute inset-0 bg-grid-tech [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_40%,transparent_100%)] pointer-events-none fade-in opacity-20 dark:opacity-40" style="animation-delay: 0.2s;"></div>

    <div class="absolute top-[-10%] right-[-10%] w-[1200px] h-[1200px] pointer-events-none fade-in" style="animation-delay: 0.5s;">
      <div class="absolute inset-0 bg-gradient-to-b from-red-600/20 via-red-800/10 to-transparent rounded-full blur-[150px] animate-[pulse_8s_ease-in-out_infinite]"></div>
      <div class="absolute top-[20%] right-[20%] w-[500px] h-[500px] bg-red-500/20 rounded-full blur-[80px] animate-[pulse_4s_ease-in-out_infinite_reverse]"></div>
    </div>

    <div class="max-w-[1400px] mx-auto w-full grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
      
      <div class="lg:col-span-8 flex flex-col justify-center">
        
        <div class="group inline-flex items-center gap-3 px-4 py-1.5 rounded-full bg-[var(--color-glass)] border border-[var(--color-glass-border)] backdrop-blur-md text-[10px] font-mono uppercase tracking-[0.2em] mb-12 w-max hover:border-red-500/50 transition-colors cursor-pointer slide-up" style="animation-delay: 0.1s;">
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-red-600"></span>
          </span>
          <span class="opacity-80">IT-Driven Agency</span>
        </div>

        <h1 class="text-7xl md:text-[110px] lg:text-[130px] font-medium tracking-tighter leading-[0.8] mb-8 slide-up" style="animation-delay: 0.3s;">
          Tu equipo <br/>
          <span class="font-serif italic text-transparent bg-clip-text bg-gradient-to-r from-red-600 to-red-500 pr-8">hardware</span><br/>
          Sprint.
        </h1>

        <p class="opacity-60 max-w-lg text-sm md:text-base leading-relaxed mb-12 font-light slide-up transition-opacity duration-500" style="animation-delay: 0.5s;">
          Desde diagnóstico hasta ensamblaje de alto rendimiento, nos conectamos a tu ecosistema y lanzamos las máquinas que tus usuarios realmente necesitan.
        </p>

        <div class="flex flex-wrap gap-6 items-center slide-up" style="animation-delay: 0.7s;">
          <button class="relative px-8 py-4 bg-red-600 text-white font-bold rounded-full overflow-hidden group transition-all hover:scale-105 hover:shadow-[0_0_40px_rgba(255,0,0,0.4)]">
            <span class="relative z-10 text-sm tracking-wide">Ver Inventario</span>
            <div class="absolute inset-0 bg-gradient-to-r from-red-500 to-red-700 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </button>
          
          <button class="px-8 py-4 font-medium rounded-full hover:text-red-500 transition-colors text-sm flex items-center gap-3 border border-transparent hover:border-[var(--color-glass-border)] opacity-80 hover:opacity-100">
            Explorar Servicios
            <span class="text-lg">→</span>
          </button>
        </div>
      </div>

      <div class="lg:col-span-4 relative h-[600px] hidden lg:block mt-20">
        
        <div class="absolute top-0 right-0 w-72 bg-[var(--color-glass)] backdrop-blur-2xl border border-[var(--color-glass-border)] p-8 rounded-[2rem] shadow-xl group hover:border-red-500/30 transition-all duration-500 hover:-translate-y-2 slide-up" style="animation-delay: 0.6s;">
          <div class="flex justify-between items-start mb-12">
            <div class="flex flex-col gap-1">
              <span class="text-[9px] opacity-50 uppercase font-mono tracking-widest">TechStore Ricci</span>
              <span class="text-[9px] text-red-500 uppercase font-mono tracking-widest flex items-center gap-2">
                <span class="w-1 h-1 bg-red-500 rounded-full"></span> Live
              </span>
            </div>
            <span class="text-[10px] opacity-40 font-mono border border-[var(--color-glass-border)] px-2 py-1 rounded-md">01/04</span>
          </div>
          
          <div class="relative">
            <h3 class="text-7xl font-light tracking-tighter mb-2">500<span class="text-red-500 text-5xl">+</span></h3>
            <svg class="absolute right-0 bottom-4 w-16 h-8 opacity-30 group-hover:opacity-100 transition-opacity group-hover:text-red-500" viewBox="0 0 100 30" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M0 30 L20 20 L40 25 L60 10 L80 15 L100 0" />
            </svg>
          </div>
          <p class="text-xs opacity-60 mt-4 border-t border-[var(--color-glass-border)] pt-4">Equipos ensamblados <br>exitosamente.</p>
        </div>

        <div class="absolute top-64 left-[-2rem] w-80 bg-[var(--color-glass)] backdrop-blur-xl border border-[var(--color-glass-border)] p-8 rounded-[2rem] group hover:border-[var(--color-glass-border)] transition-all duration-500 slide-up shadow-lg" style="animation-delay: 0.8s;">
          <div class="flex justify-between items-end mb-6">
            <h3 class="text-5xl font-light tracking-tighter">98<span class="text-red-500 text-3xl">%</span></h3>
            <span class="text-[10px] opacity-50 font-mono mb-2">Precision</span>
          </div>
          <p class="text-xs opacity-60 mb-8 leading-relaxed">Tasa de éxito en reparaciones de placas base y micro-soldadura.</p>
          
          <div class="w-full bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] rounded-full p-1 mb-3 shadow-inner">
            <div class="h-2 w-[98%] bg-gradient-to-r from-red-800 to-red-500 rounded-full relative overflow-hidden">
              <div class="absolute top-0 left-0 w-full h-full bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,0.2)_50%,transparent_75%)] bg-[length:20px_20px] animate-[slide_1s_linear_infinite]"></div>
            </div>
          </div>
          <div class="flex justify-between text-[9px] font-mono uppercase tracking-widest">
            <span class="opacity-50">Diagnóstico</span>
            <span class="text-red-500 font-bold">Completado</span>
          </div>
        </div>

        <div class="absolute bottom-[-2rem] right-10 bg-[var(--color-main-bg)] border border-[var(--color-glass-border)] p-3 pr-6 rounded-full flex items-center gap-4 hover:border-red-500/50 hover:shadow-[0_0_20px_rgba(255,0,0,0.15)] transition-all cursor-pointer group slide-up shadow-xl" style="animation-delay: 1s;">
          <div class="w-12 h-12 rounded-full bg-red-900/10 flex items-center justify-center border border-red-500/30 group-hover:bg-red-600 transition-colors overflow-hidden">
            <img src="https://ui-avatars.com/api/?name=Andres+Ricci&background=ff0000&color=fff" alt="Andrés" class="w-full h-full grayscale group-hover:grayscale-0 transition-all">
          </div>
          <div>
            <p class="text-[9px] text-red-500 uppercase font-mono tracking-widest mb-0.5">Soporte Directo</p>
            <p class="text-sm font-medium tracking-tight">Hablar con un Ing.</p>
          </div>
        </div>

      </div>
    </div>

    <div class="absolute right-6 top-1/2 -translate-y-1/2 hidden xl:flex flex-col items-center gap-8 opacity-40 fade-in" style="animation-delay: 1.5s;">
      <div class="w-px h-24 bg-gradient-to-b from-transparent via-[var(--color-main-text)] to-transparent opacity-50"></div>
      <span class="text-[9px] font-mono [writing-mode:vertical-rl] tracking-[0.3em] uppercase opacity-70">Desplázate</span>
      <div class="w-px h-24 bg-gradient-to-b from-transparent via-red-500 to-transparent"></div>
    </div>
  </section>
</template>