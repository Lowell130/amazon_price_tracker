<template>
  <section class="py-16 bg-white dark:bg-gray-900 overflow-hidden">
    <div class="max-w-screen-xl px-4 mx-auto">
      <div class="relative p-8 md:p-12 rounded-[3rem] bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800/50 dark:to-blue-900/20 border border-blue-100 dark:border-blue-900/30 overflow-hidden shadow-2xl shadow-blue-500/5 group">
        
        <!-- Decorative background elements -->
        <div class="absolute -top-24 -right-24 w-64 h-64 bg-blue-400/10 rounded-full blur-3xl group-hover:bg-blue-400/20 transition-colors duration-700"></div>
        <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-indigo-400/10 rounded-full blur-3xl group-hover:bg-indigo-400/20 transition-colors duration-700"></div>

        <div class="relative z-10 grid lg:grid-cols-12 gap-12 items-center">
          <!-- Text Content -->
          <div class="lg:col-span-7 space-y-6 text-center lg:text-left">
            <div class="inline-flex items-center px-4 py-2 rounded-2xl bg-blue-600/10 text-blue-600 dark:text-blue-400 text-xs font-black uppercase tracking-widest border border-blue-200 dark:border-blue-800">
               Novità: Chrome Extension
            </div>
            <h2 class="text-3xl md:text-5xl font-black text-gray-900 dark:text-white leading-tight">
              Monitora i prezzi <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">senza uscire</span> da Amazon
            </h2>
            <p class="text-lg text-gray-600 dark:text-gray-400 font-medium leading-relaxed max-w-2xl mx-auto lg:mx-0">
              Con la nostra estensione ufficiale, puoi aggiungere prodotti a PriceHub con un solo clic mentre navighi su Amazon. Semplice, veloce e integrata.
            </p>
            
            <div class="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-4">
              <button 
                @click="downloadExtension"
                class="w-full sm:w-auto px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-bold shadow-xl shadow-blue-600/20 transition-all transform hover:-translate-y-1 active:scale-95 flex items-center justify-center gap-3 group/btn"
              >
                <svg class="w-6 h-6 group-hover/btn:animate-bounce" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
                </svg>
                Scarica Estensione
              </button>
              <p class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-tighter">
                Disponibile per Chrome & Edge
              </p>
            </div>
          </div>

          <!-- Graphic/Preview Content -->
          <div class="lg:col-span-5 relative flex justify-center">
            <div class="relative">
              <!-- Glass Card for the Extension Icon -->
              <div class="w-48 h-48 md:w-64 md:h-64 bg-white/40 dark:bg-gray-800/40 backdrop-blur-xl rounded-[2.5rem] border border-white/40 dark:border-white/10 shadow-2xl flex items-center justify-center p-8 transform rotate-3 hover:rotate-0 transition-transform duration-500">
                <img 
                  :src="require('@/assets/extension-icon.png')" 
                  alt="PriceHub Extension Icon" 
                  class="w-full h-full object-contain filter drop-shadow-2xl"
                >
              </div>
              
              <!-- Floating UI Badges -->
              <div class="absolute -top-4 -left-4 bg-emerald-500 text-white p-3 rounded-2xl shadow-xl shadow-emerald-500/20 animate-pulse-subtle">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <div class="absolute -bottom-6 -right-6 bg-white dark:bg-gray-800 p-4 rounded-3xl shadow-2xl border border-gray-100 dark:border-gray-700 transform -rotate-6">
                <div class="flex items-center gap-3">
                  <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span class="text-xs font-black text-gray-900 dark:text-white">-€120.50</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ExtensionPromo',
  methods: {
    downloadExtension() {
      const apiBaseUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000';
      window.location.href = `${apiBaseUrl}/extension/download`;
    }
  }
}
</script>

<style scoped>
.animate-pulse-subtle {
  animation: pulse-subtle 3s ease-in-out infinite;
}
@keyframes pulse-subtle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.9; transform: scale(1.05); }
}
</style>
