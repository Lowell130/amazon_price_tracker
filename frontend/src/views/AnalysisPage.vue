<template>
  <div class="min-h-screen bg-[#f8fafc] dark:bg-gray-950 pt-32 pb-20 overflow-x-hidden">
    <!-- Background Decor -->
    <div class="fixed top-0 left-0 w-full h-full pointer-events-none overflow-hidden z-0">
      <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-blue-500/5 rounded-full blur-[120px]"></div>
      <div class="absolute top-[20%] -right-[5%] w-[30%] h-[30%] bg-indigo-500/5 rounded-full blur-[100px]"></div>
    </div>

    <div class="max-w-7xl mx-auto px-6 relative z-10">
      <!-- Header -->
      <div class="mb-12 animate-fadeIn">
        <div class="flex items-center gap-3 mb-4">
          <span class="px-4 py-1.5 rounded-2xl bg-blue-600 text-white text-[10px] font-black uppercase tracking-[0.2em] shadow-lg shadow-blue-500/30">
            Intelligenza Artificiale
          </span>
          <div class="h-px flex-grow bg-gray-200 dark:bg-gray-800 opacity-50"></div>
        </div>
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white tracking-tight mb-4">
          Price <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-500">Insights</span>
        </h1>
        <p class="text-lg text-gray-500 dark:text-gray-400 font-medium max-w-2xl leading-relaxed">
          Analizziamo milioni di variazioni di prezzo per darti consigli strategici su quando acquistare.
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-40">
        <div class="relative w-16 h-16">
          <div class="absolute inset-0 border-4 border-blue-500/10 rounded-full"></div>
          <div class="absolute inset-0 border-4 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
        </div>
        <p class="mt-8 text-gray-400 font-black uppercase tracking-[0.4em] text-[10px] animate-pulse">Analisi in corso...</p>
      </div>

      <div v-else-if="analysisData && analysisData.summary" class="animate-fadeIn">
        
        <!-- Analysis Guide Section -->
        <div class="mb-12 p-8 bg-white/40 dark:bg-gray-800/40 backdrop-blur-xl rounded-[2.5rem] border border-gray-100 dark:border-gray-700 shadow-sm">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-8 flex items-center gap-4">
            <span class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 text-white flex items-center justify-center shadow-lg shadow-blue-500/20 shrink-0">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-7.714 2.143L11 21l-2.286-6.857L1 12l7.714-2.143L11 3z" />
              </svg>
            </span>
            Analisi AI: Guida alle Metriche
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div class="flex flex-col gap-2">
              <span class="text-[10px] font-black uppercase tracking-widest text-blue-600 dark:text-blue-400">Suggerimento</span>
              <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                Determina se è il momento di comprare (<b>BUY</b>), aspettare (<b>WAIT</b>) o monitorare (<b>HOLD</b>) in base ai minimi storici e alla media.
              </p>
            </div>
            <div class="flex flex-col gap-2">
              <span class="text-[10px] font-black uppercase tracking-widest text-indigo-600 dark:text-indigo-400">Volatilità</span>
              <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                Indica quanto varia il prezzo. Più è alta, più è probabile che si presentino forti sconti improvvisi.
              </p>
            </div>
            <div class="flex flex-col gap-2">
              <span class="text-[10px] font-black uppercase tracking-widest text-amber-600 dark:text-amber-400">Rischio</span>
              <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                Basato sulla stabilità dei prezzi. Un rischio alto indica variazioni repentine e imprevedibili.
              </p>
            </div>
            <div class="flex flex-col gap-2">
              <span class="text-[10px] font-black uppercase tracking-widest text-emerald-600 dark:text-emerald-400">Probab. Calo</span>
              <p class="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                La probabilità statistica che il prezzo scenda ulteriormente rispetto al valore attuale.
              </p>
            </div>
          </div>
        </div>

        <!-- Summary Stats Grid (Bento Style) -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <!-- Market Sentiment Card -->
           <div class="lg:col-span-2 p-8 bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl rounded-[2.5rem] border border-gray-100 dark:border-gray-700 shadow-xl flex flex-col justify-between overflow-hidden relative group">
             <div class="absolute top-0 right-0 p-8 opacity-5 group-hover:scale-110 transition-transform duration-700">
               <svg class="w-24 h-24" fill="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
             </div>
             <div>
                <p class="text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.3em] mb-6">Sentiment Mercato</p>
                <h2 class="text-4xl font-bold text-gray-900 dark:text-white tracking-tight mb-2">{{ analysisData.summary.market_sentiment }}</h2>
                <p class="text-gray-500 dark:text-gray-400 font-medium text-sm">Analisi statistica su {{ analysisData.summary.total_tracked }} prodotti monitorati.</p>
             </div>
             <div class="mt-10 flex gap-3 flex-wrap">
               <div class="px-4 py-2 bg-emerald-500/10 dark:bg-emerald-500/20 rounded-2xl border border-emerald-500/20">
                 <span class="text-[10px] font-black text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">{{ analysisData.summary.buy_opportunities }} Occasioni</span>
               </div>
               <div class="px-4 py-2 bg-blue-500/10 dark:bg-blue-500/20 rounded-2xl border border-blue-500/20">
                 <span class="text-[10px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-wider">{{ analysisData.summary.at_all_time_low }} Minimi Storici</span>
               </div>
             </div>
           </div>

           <!-- Volatility Card -->
           <div class="p-8 bg-white/70 dark:bg-gray-800/70 backdrop-blur-xl rounded-[2.5rem] border border-gray-100 dark:border-gray-700 shadow-xl relative overflow-hidden group flex flex-col justify-between">
             <div>
                <p class="text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-[0.3em] mb-4">Volatilità Media</p>
                <div class="text-5xl font-bold text-blue-600 dark:text-blue-400 tracking-tight group-hover:rotate-3 transition-transform">{{ analysisData.summary.avg_volatility }}%</div>
             </div>
             <p class="text-[10px] text-gray-400 mt-6 font-bold uppercase tracking-[0.1em] leading-relaxed">Indice di variazione dei prezzi nell'ultimo periodo.</p>
           </div>

           <!-- Stability Card -->
           <div class="p-8 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-[2.5rem] shadow-2xl text-white relative overflow-hidden shadow-blue-500/30 flex flex-col justify-between">
             <div class="absolute -bottom-4 -right-4 w-24 h-24 bg-white/10 rounded-full blur-2xl"></div>
             <div>
                <p class="text-[10px] font-black text-white/50 uppercase tracking-[0.3em] mb-4">Prezzi Stabili</p>
                <div class="text-5xl font-black tracking-tighter">{{ analysisData.summary.stable_items }}</div>
             </div>
             <div class="mt-6 flex items-center gap-2">
               <span class="p-1.5 bg-white/20 rounded-xl backdrop-blur-md">
                 <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
               </span>
               <span class="text-[10px] font-black uppercase tracking-widest">Hold suggerito</span>
             </div>
           </div>
        </div>

        <!-- Recommendations Section -->
        <div class="flex flex-col lg:flex-row items-center justify-between mb-10 gap-6">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-4 shrink-0">
            <span class="w-10 h-10 rounded-2xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 flex items-center justify-center text-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
            </span>
            Analisi per Prodotto
          </h3>
          
          <!-- Advanced Controls -->
          <div class="flex flex-col md:flex-row items-center gap-4 w-full lg:w-auto">
            <!-- Search Bar -->
            <div class="relative w-full md:w-64">
              <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-gray-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </div>
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Cerca prodotto..."
                class="block w-full pl-10 pr-4 py-2.5 rounded-2xl border-transparent bg-white/60 dark:bg-gray-800/60 dark:text-white text-xs focus:ring-2 focus:ring-blue-500 transition-all shadow-sm"
              >
            </div>

            <!-- Filter Groups -->
            <div class="flex items-center gap-2 bg-white/50 dark:bg-gray-800/50 p-1.5 rounded-2xl border border-gray-100 dark:border-gray-700 backdrop-blur-md">
              <button 
                v-for="f in ['TUTTI', 'BUY', 'HOLD', 'WAIT']" 
                :key="f"
                @click="selectedFilter = f"
                class="px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all duration-300"
                :class="selectedFilter === f 
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' 
                  : 'text-gray-400 hover:text-gray-600 dark:hover:text-gray-200'"
              >
                {{ f }}
              </button>
            </div>

            <!-- Sort Select -->
            <select 
              v-model="sortBy"
              class="px-4 py-2.5 rounded-2xl border-transparent bg-white/60 dark:bg-gray-800/60 dark:text-white text-[10px] font-black uppercase tracking-widest focus:ring-2 focus:ring-blue-500 transition-all shadow-sm cursor-pointer"
            >
              <option value="recent">Recenti</option>
              <option value="price-asc">Prezzo: Crescente</option>
              <option value="price-desc">Prezzo: Decrescente</option>
              <option value="drop-chance">Probab. Calo</option>
              <option value="volatility">Volatilità</option>
            </select>
          </div>
        </div>

        <div v-if="filteredItems.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
           <InsightCard v-for="item in filteredItems" :key="item.asin" :item="item" class="animate-fadeIn" />
        </div>
        
        <div v-else class="py-20 px-6 text-center bg-white/40 dark:bg-gray-800/40 backdrop-blur-xl rounded-[3rem] border border-dashed border-gray-200 dark:border-gray-700 shadow-inner overflow-hidden relative group">
           <!-- Decorative Background -->
           <div class="absolute inset-0 bg-gradient-to-b from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
           
           <div class="relative z-10 max-w-md mx-auto">
             <div class="w-24 h-24 bg-gradient-to-br from-blue-600 to-indigo-600 rounded-[2rem] flex items-center justify-center mx-auto mb-8 shadow-2xl shadow-blue-500/20 transform group-hover:rotate-12 transition-transform duration-500">
               <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
               </svg>
             </div>
             
             <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight mb-4">
               Analisi in <span class="text-blue-600">Elaborazione</span>
             </h3>
             
             <p class="text-gray-500 dark:text-gray-400 font-medium leading-relaxed mb-10">
               L'IA di PriceHub ha bisogno di raccogliere dati per almeno <b>2-3 giorni</b> per generare previsioni accurate e analisi dei rischi. Inizia a monitorare i tuoi primi prodotti per vedere le magie accadere!
             </p>

             <router-link 
               to="/dashboard"
               class="inline-flex items-center gap-3 px-8 py-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-2xl font-black text-sm uppercase tracking-widest transition-all transform hover:-translate-y-1 hover:shadow-2xl active:scale-95"
             >
               Vai alla Dashboard
               <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5-5 5M6 12h12" />
               </svg>
             </router-link>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InsightCard from '@/components/InsightCard.vue'

export default {
  name: 'AnalysisPage',
  components: { InsightCard },
  data() {
    return {
      analysisData: null,
      loading: true,
      error: null,
      selectedFilter: 'TUTTI',
      searchQuery: '',
      sortBy: 'recent'
    }
  },
  computed: {
    filteredItems() {
      if (!this.analysisData || !this.analysisData.items) return []
      
      let items = [...this.analysisData.items]

      // Filter by Recommendation
      if (this.selectedFilter !== 'TUTTI') {
        items = items.filter(item => item.recommendation === this.selectedFilter)
      }

      // Filter by Search Query
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        items = items.filter(item => 
          item.title.toLowerCase().includes(query) || 
          item.asin.toLowerCase().includes(query)
        )
      }

      // Sort
      switch(this.sortBy) {
        case 'price-asc':
          items.sort((a, b) => a.current_price - b.current_price)
          break
        case 'price-desc':
          items.sort((a, b) => b.current_price - a.current_price)
          break
        case 'drop-chance':
          items.sort((a, b) => b.chance_of_drop - a.chance_of_drop)
          break
        case 'volatility':
          items.sort((a, b) => b.volatility - a.volatility)
          break
        default:
          // Keep original order (recent)
          break
      }

      return items
    }
  },
  async created() {
    await this.fetchAnalysis()
  },
  methods: {
    async fetchAnalysis() {
      this.loading = true
      try {
        const token = localStorage.getItem('token')
        const apiUrl = process.env.VUE_APP_API_BASE_URL || ''
        const res = await fetch(`${apiUrl}/analysis/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        })
        if (!res.ok) throw new Error('Errore nel caricamento dei dati')
        this.analysisData = await res.json()
      } catch (err) {
        this.error = err.message
        console.error('Analysis fetch error:', err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
</style>
