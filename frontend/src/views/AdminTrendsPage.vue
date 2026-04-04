<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12 antialiased">
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-8 pt-8">
      <!-- Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-gray-900 dark:text-white tracking-tight flex items-center gap-2">
            Trend Explorer <span class="text-xl">📈</span>
          </h1>
          <p class="text-sm sm:text-base text-gray-500 dark:text-gray-400 mt-1">Trova ispirazione analizzando le notizie e i social con l'AI.</p>
        </div>
        <div class="flex items-center gap-3">
          <button @click="showSettingsModal = true" class="inline-flex items-center justify-center p-3 sm:px-4 sm:py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-bold rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 transition-all text-sm">
            <span class="mr-0 sm:mr-2 text-lg">⚙️</span> <span class="hidden sm:inline">Impostazioni Motore</span>
          </button>
          <router-link to="/dashboard" class="inline-flex items-center justify-center px-4 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-bold rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 transition-all text-sm sm:text-base">
            <span class="mr-2">&larr;</span> Indietro
          </router-link>
          <button @click="refreshTrends" :disabled="loading" class="inline-flex items-center justify-center px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-black rounded-2xl shadow-lg shadow-blue-500/30 hover:scale-105 active:scale-95 disabled:opacity-50 transition-all text-sm sm:text-base">
            <svg v-if="loading" class="w-5 h-5 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            <svg v-else class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            {{ loading ? 'Analisi...' : 'Nuova Scansione AI' }}
          </button>
        </div>
      </div>

      <!-- Content -->
      <div v-if="loading && trends.length === 0" class="flex flex-col items-center justify-center py-32">
         <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-6"></div>
         <h2 class="text-xl font-bold dark:text-white">Il super cervello ci sta pensando...</h2>
         <p class="text-gray-500 mt-2 text-center max-w-sm">Sto leggendo centinaia di notizie e post per estrarre i trend più caldi del momento. Potrebbe volerci qualche istante.</p>
      </div>

      <div v-else-if="trends.length === 0" class="rounded-3xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-800/80 p-16 text-center shadow-xl">
        <div class="text-6xl mb-4">💤</div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white">Nessun Trend Recente</h3>
        <p class="text-gray-500 dark:text-gray-400 mt-2 mb-6">Avvia una scansione per scoprire cosa sta pompando sul web oggi.</p>
        <button @click="refreshTrends" class="px-8 py-3 bg-blue-600 text-white font-bold rounded-xl shadow-lg hover:bg-blue-700">Analizza Ora</button>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
         <!-- Trend Cards -->
         <div v-for="(trend, index) in sortedTrends" :key="index" class="rounded-[2.5rem] bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 shadow-xl overflow-hidden group hover:-translate-y-1 transition-all duration-300">
            <div class="p-8">
               <div class="flex items-start justify-between mb-6">
                 <div>
                   <div class="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest mb-3" :class="getScoreColor(trend.score)">
                     Score: {{ trend.score }}/100
                   </div>
                   <h2 class="text-2xl font-black text-gray-900 dark:text-white leading-tight">
                     {{ trend.topic }}
                   </h2>
                 </div>
                 <div class="text-4xl filter drop-shadow-md">{{ getEmoji(trend.score) }}</div>
               </div>

               <p class="text-gray-600 dark:text-gray-300 text-sm italic mb-6 leading-relaxed">
                 "{{ trend.reason }}"
               </p>

               <div class="bg-gray-50 dark:bg-gray-900 rounded-2xl p-4 border border-gray-100 dark:border-gray-800 mb-8">
                 <div class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Keyword Suggerita 🎯</div>
                 <div class="text-sm font-semibold text-blue-600 dark:text-blue-400">{{ trend.seo_keyword }}</div>
               </div>

               <div class="flex flex-col gap-3">
                  <button @click="writeArticle(trend)" class="w-full flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-black rounded-xl shadow-lg shadow-purple-500/20 hover:scale-105 active:scale-95 transition-all text-sm uppercase tracking-widest">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                    Scrivi Articolo Info
                  </button>
                  <button @click="searchAmazon(trend)" class="w-full flex items-center justify-center gap-2 px-6 py-4 bg-white dark:bg-gray-900 text-gray-800 dark:text-white font-bold rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 active:scale-95 transition-all text-sm">
                    <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
                    Cerca su Amazon
                  </button>
               </div>
            </div>
         </div>
      </div>

      <!-- Settings Modal -->
      <div v-if="showSettingsModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-fadeIn">
        <div class="bg-white dark:bg-gray-900 rounded-3xl shadow-2xl p-6 sm:p-8 w-full max-w-xl max-h-[90vh] overflow-y-auto border border-white/20 dark:border-gray-800">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-black text-gray-900 dark:text-white">Impostazioni Motore AI</h2>
            <button @click="showSettingsModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>

          <div class="space-y-8">
            <!-- Count Setting -->
            <div>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Quantità di Trend da generare: <span class="text-blue-600">{{ targetCount }}</span></label>
              <input type="range" v-model.number="targetCount" min="3" max="25" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-blue-600" />
              <p class="text-xs text-gray-500 mt-2">Maggiore è il numero, più nicchie verranno trovate, ma la qualità media scenderà o richiederà più tempo.</p>
            </div>

            <hr class="border-gray-100 dark:border-gray-800" />

            <!-- Sources Setting -->
            <div>
              <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4">Fonti Notizie (RSS)</h3>
              
              <!-- Add Source -->
              <div class="flex gap-2 mb-4">
                <input v-model="newSourceUrl" type="url" placeholder="https://example.com/rss" class="flex-1 px-4 py-2 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 dark:text-white text-sm" />
                <button @click="addSource" :disabled="!newSourceUrl || addingSource" class="px-4 py-2 bg-blue-600 text-white font-bold rounded-xl shadow-sm hover:bg-blue-700 disabled:opacity-50 transition-all text-sm shrink-0">
                  <span v-if="!addingSource">Aggiungi</span>
                  <span v-else>...</span>
                </button>
              </div>

              <!-- Sources List -->
              <div v-if="loadingSources" class="text-center py-4"><span class="animate-pulse text-gray-400">Caricamento fonti...</span></div>
              <ul v-else class="space-y-2 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
                <li v-for="source in rssSources" :key="source" class="flex items-center justify-between p-3 rounded-xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700">
                  <span class="text-xs font-mono text-gray-600 dark:text-gray-300 truncate mr-3" :title="source">{{ source }}</span>
                  <button @click="removeSource(source)" class="text-rose-500 hover:text-rose-600 p-1 bg-rose-50 dark:bg-rose-900/20 rounded-lg shrink-0 transition-colors">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                </li>
              </ul>
              <p v-if="rssSources.length === 0 && !loadingSources" class="text-sm text-gray-400 italic">Nessuna fonte trovata. Verranno usate quelle di base.</p>
            </div>
          </div>
          
          <div class="mt-8 pt-4 border-t border-gray-100 dark:border-gray-800 flex justify-end">
            <button @click="showSettingsModal = false" class="px-6 py-2 bg-gray-100 text-gray-800 font-bold rounded-xl hover:bg-gray-200 transition-all">Chiudi</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { fetchWithToken } from "@/api";
import { useToast } from "@/store/toast";

export default {
  name: "AdminTrendsPage",
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      trends: [],
      loading: true,
      
      // Settings variables
      showSettingsModal: false,
      targetCount: 10,
      rssSources: [],
      newSourceUrl: "",
      loadingSources: false,
      addingSource: false
    };
  },
  computed: {
    sortedTrends() {
      // Sort by score descending (it's safe to sort a copy)
      return [...this.trends].sort((a, b) => b.score - a.score);
    }
  },
  async created() {
    await this.fetchTrends();
  },
  methods: {
    async fetchTrends() {
      this.loading = true;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/trends`);
        if (response.ok) {
          const data = await response.json();
          this.trends = data || [];
        }
        await this.fetchSources(); // Pre-fetch sources for the modal
      } catch (e) {
        console.error("Error fetching trends", e);
        this.toast.error("Errore di caricamento trend.");
      } finally {
        this.loading = false;
      }
    },
    async refreshTrends() {
      this.showSettingsModal = false;
      this.loading = true;
      this.toast.info("L'AI sta analizzando le fonti. Attendi...");
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/trends/refresh`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ count: this.targetCount })
        });
        if (response.ok) {
          const data = await response.json();
          this.trends = data.trends || [];
          this.toast.success("Segnali aggiornati con successo!");
        } else {
          this.toast.error("Errore durante l'analisi. Riprova.");
        }
      } catch (e) {
        console.error("Error refreshing trends", e);
        this.toast.error("Errore di rete durante la scansione.");
      } finally {
        this.loading = false;
      }
    },
    async fetchSources() {
      this.loadingSources = true;
      try {
        const res = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/trends/sources`);
        if (res.ok) {
          this.rssSources = await res.json();
        }
      } catch (e) {
         console.error("Error fetching sources");
      } finally {
        this.loadingSources = false;
      }
    },
    async addSource() {
      if (!this.newSourceUrl) return;
      this.addingSource = true;
      try {
        const res = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/trends/sources`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: this.newSourceUrl })
        });
        if (res.ok) {
          const data = await res.json();
          this.rssSources = data.urls;
          this.newSourceUrl = "";
          this.toast.success("Fonte aggiunta!");
        }
      } catch (e) {
         this.toast.error("Errore aggiunta fonte.");
      } finally {
        this.addingSource = false;
      }
    },
    async removeSource(url) {
      if (!confirm("Rimuovere questa fonte?")) return;
      try {
        const res = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/trends/sources`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url })
        });
        if (res.ok) {
          const data = await res.json();
          this.rssSources = data.urls;
        }
      } catch (e) {
         this.toast.error("Errore rimozione.");
      }
    },
    writeArticle(trend) {
       // Possiamo reindirizzare ad AdminArticlesPage portando la keyword come query param o copiandola in clipboard
       navigator.clipboard.writeText(trend.seo_keyword);
       this.toast.success("Keyword copiata! Ti rinvio alla creazione...");
       setTimeout(() => {
          this.$router.push('/admin/articles');
       }, 1500);
    },
    searchAmazon(trend) {
       const url = `https://www.amazon.it/s?k=${encodeURIComponent(trend.topic)}`;
       window.open(url, '_blank');
    },
    getScoreColor(score) {
      if (score >= 85) return 'bg-rose-100/80 text-rose-700 dark:bg-rose-900/30 dark:text-rose-400 border border-rose-200 dark:border-rose-800';
      if (score >= 70) return 'bg-orange-100/80 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400 border border-orange-200 dark:border-orange-800';
      return 'bg-blue-100/80 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800';
    },
    getEmoji(score) {
      if (score >= 90) return '🔥';
      if (score >= 80) return '🚀';
      if (score >= 60) return '📈';
      return '👀';
    }
  }
};
</script>
<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.3); border-radius: 10px; }
</style>
