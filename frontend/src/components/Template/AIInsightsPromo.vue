<template>
  <section class="py-16 bg-gray-50 dark:bg-gray-950 overflow-hidden">
    <div class="max-w-screen-xl px-4 mx-auto">
      <div class="grid lg:grid-cols-2 gap-16 items-center">
        
        <!-- Interactive Preview -->
        <div class="order-2 lg:order-1 relative">
          <!-- Main Card Mockup -->
          <div class="relative bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl p-8 rounded-[3rem] border border-gray-100 dark:border-gray-800 shadow-2xl">
            <div class="flex items-center justify-between mb-8">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-lg shadow-blue-600/20">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div>
                  <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest leading-none mb-1">AI Prediction</p>
                  <h4 class="text-sm font-black text-gray-900 dark:text-white leading-none">Strong Buy Signal</h4>
                </div>
              </div>
              <div class="px-3 py-1 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-600 dark:text-emerald-400 text-[10px] font-black uppercase rounded-lg">
                Prob. Calo: 87%
              </div>
            </div>

            <!-- Fake Chart Lines -->
            <div class="h-48 flex items-end gap-2 mb-6">
              <div v-for="h in [40, 60, 45, 70, 55, 80, 50, 65, 30, 45]" :key="h" 
                   :style="{ height: h + '%' }" 
                   class="flex-1 bg-blue-100 dark:bg-blue-900/30 rounded-t-lg group-hover:bg-blue-600 transition-colors"></div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="p-4 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-transparent">
                <p class="text-[9px] font-black text-gray-400 uppercase tracking-widest mb-1">Volatilità</p>
                <p class="text-lg font-black text-gray-900 dark:text-white">Media</p>
              </div>
              <div class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-2xl border border-blue-100 dark:border-blue-800/30">
                <p class="text-[9px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest mb-1">Prezzo Target</p>
                <p class="text-lg font-black text-blue-600 dark:text-blue-400">€449.00</p>
              </div>
            </div>
          </div>

          <!-- Floating Decoration -->
          <div class="absolute -top-6 -right-6 w-32 h-32 bg-indigo-500/10 rounded-full blur-3xl z-0"></div>
          <div class="absolute -bottom-10 -left-10 w-40 h-40 bg-blue-500/10 rounded-full blur-3xl z-0"></div>
        </div>

        <!-- Text Content -->
        <div class="order-1 lg:order-2 space-y-8">
          <div class="space-y-4 text-center lg:text-left">
            <div class="inline-flex items-center px-4 py-2 rounded-2xl bg-indigo-600 text-white text-[10px] font-black uppercase tracking-[0.2em] shadow-lg shadow-indigo-500/20">
               Smart Shopping
            </div>
            <h2 class="text-3xl md:text-5xl font-black text-gray-900 dark:text-white leading-tight">
              L'Intelligenza Artificiale al servizio dei tuoi <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-600">risparmi</span>
            </h2>
            <p class="text-lg text-gray-600 dark:text-gray-400 font-medium leading-relaxed">
              Non limitarti a guardare il prezzo. La nostra AI analizza lo storico e la volatilità per dirti esattamente qual è la probabilità di un calo imminente.
            </p>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div class="flex items-start gap-4">
              <div class="p-3 bg-white dark:bg-gray-800 rounded-2xl shadow-md border border-gray-100 dark:border-gray-700">
                <svg class="w-6 h-6 text-indigo-600 shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              </div>
              <div>
                <h4 class="font-black text-gray-900 dark:text-white text-sm uppercase tracking-tight">Analisi dei Rischi</h4>
                <p class="text-xs text-gray-500 dark:text-gray-500 mt-1 font-medium">Scopri se il prezzo è stabile o in attesa di ribassi.</p>
              </div>
            </div>
            <div class="flex items-start gap-4">
              <div class="p-3 bg-white dark:bg-gray-800 rounded-2xl shadow-md border border-gray-100 dark:border-gray-700">
                <svg class="w-6 h-6 text-blue-600 shadow-sm" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
              <div>
                <h4 class="font-black text-gray-900 dark:text-white text-sm uppercase tracking-tight">Price Predictions</h4>
                <p class="text-xs text-gray-500 dark:text-gray-500 mt-1 font-medium">Algoritmi predittivi basati sui Big Data di Amazon.</p>
              </div>
            </div>
          </div>

          <div class="flex justify-center lg:justify-start pt-4">
            <router-link 
              to="/analysis"
              class="group px-8 py-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-2xl font-bold transition-all transform hover:-translate-y-1 hover:shadow-2xl flex items-center gap-3"
            >
              Vedi AI Insights
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5-5 5M6 12h12"/></svg>
            </router-link>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'AIInsightsPromo'
}
</script>
