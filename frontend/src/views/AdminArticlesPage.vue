<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12 antialiased">
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-8 pt-8">
      <!-- Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl sm:text-3xl font-black text-gray-900 dark:text-white tracking-tight">Gestione Articoli AI</h1>
          <p class="text-sm sm:text-base text-gray-500 dark:text-gray-400 mt-1">Monitora lo stato della coda e genera articoli "Top 10" multi-prodotto.</p>
        </div>
        <router-link to="/dashboard" class="inline-flex items-center justify-center px-5 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-bold rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 transition-all whitespace-nowrap text-sm sm:text-base">
          <span class="mr-2">&larr;</span> Torna alla Dashboard
        </router-link>
      </div>

      <!-- Tabs -->
      <div class="mb-6 flex gap-4 border-b border-gray-200 dark:border-gray-700">
        <button 
          @click="currentTab = 'list'"
          :class="['pb-4 px-2 font-bold text-sm tracking-wide border-b-2 transition-all', currentTab === 'list' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300']">
          Storico Articoli
        </button>
        <button 
          @click="currentTab = 'new_article'"
          :class="['pb-4 px-2 font-bold text-sm tracking-wide border-b-2 transition-all', currentTab === 'new_article' ? 'border-purple-500 text-purple-600 dark:text-purple-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300']">
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/></svg>
            Nuovo Articolo
          </span>
        </button>
      </div>

      <!-- NEW ARTICLE TAB -->
      <div v-if="currentTab === 'new_article'" class="space-y-6">
        <div class="rounded-3xl border border-white/20 bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl shadow-xl p-6 md:p-8">
          
          <!-- Mode Selector -->
          <div class="mb-8 flex gap-4">
            <label class="flex-1 cursor-pointer">
              <input type="radio" v-model="articleMode" value="single" class="peer sr-only" />
              <div class="p-4 rounded-2xl border-2 transition-all peer-checked:border-blue-500 peer-checked:bg-blue-50 dark:peer-checked:bg-blue-900/20 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:border-blue-300">
                <div class="font-black text-gray-900 dark:text-white">Recensione Singola</div>
                <div class="text-sm text-gray-500 mt-1">Analisi dettagliata di un solo prodotto.</div>
              </div>
            </label>
            <label class="flex-1 cursor-pointer">
              <input type="radio" v-model="articleMode" value="multi" class="peer sr-only" />
              <div class="p-4 rounded-2xl border-2 transition-all peer-checked:border-purple-500 peer-checked:bg-purple-50 dark:peer-checked:bg-purple-900/20 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:border-purple-300">
                <div class="font-black text-gray-900 dark:text-white">Formato Listicle (Classifica)</div>
                <div class="text-sm text-gray-500 mt-1">Classifica di più prodotti (es. "Top 10").</div>
              </div>
            </label>
          </div>

          <h2 class="text-xl font-black text-gray-900 dark:text-white mb-6">
            {{ articleMode === 'multi' ? 'Impostazioni Articolo Listicle (Multi-Prodotto)' : 'Impostazioni Recensione Prodotto' }}
          </h2>
          
          <div class="mb-8 space-y-4 max-w-2xl">
            <!-- Keyword Input Single/Multi -->
            <div v-if="articleMode === 'multi'">
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Keyword SEO Principale</label>
              <div class="flex items-center gap-2">
                <input type="text" v-model="multiArticle.keyword" placeholder="Es. Migliori notebook gaming 2026" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-purple-500 dark:text-white" />
                <button @click="enhanceKeyword" :disabled="!multiArticle.keyword || enhancingKeyword" class="shrink-0 px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow hover:scale-105 disabled:opacity-50 transition-all flex items-center justify-center">
                  <svg v-if="enhancingKeyword" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                  <span v-else>✨ Migliora Titolo</span>
                </button>
              </div>
            </div>

            <div v-else>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Keyword SEO (Opzionale)</label>
              <div class="flex items-center gap-2">
                <input type="text" v-model="singleArticle.keyword" placeholder="Es. Recensione completa Vivo X300 Ultra" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-blue-500 dark:text-white" />
                <button @click="enhanceKeyword" :disabled="!singleArticle.keyword || enhancingKeyword" class="shrink-0 px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-bold rounded-xl shadow hover:scale-105 disabled:opacity-50 transition-all flex items-center justify-center">
                  <svg v-if="enhancingKeyword" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                  <span v-else>✨ Ottimizza</span>
                </button>
              </div>
            </div>

            <!-- Filter Categories -->
            <div>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Filtra prodotti per Categoria (opzionale)</label>
              <select v-model="multiArticle.categoryFilter" class="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 focus:ring-2 focus:ring-purple-500 dark:text-white">
                <option value="">Tutte le categorie</option>
                <option v-for="cat in uniqueCategories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
          </div>

          <div class="mb-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-bold text-gray-700 dark:text-gray-300">
                Seleziona Prodotti ({{ articleMode === 'multi' ? multiArticle.selectedAsins.length + ' selezionati' : (singleArticle.selectedAsin ? '1 selezionato' : 'nessuno selezionato') }})
              </h3>
            </div>
            
            <div class="max-h-96 overflow-y-auto pr-2 custom-scrollbar">
              <div v-if="loadingProducts" class="text-center py-8 text-gray-500">Recupero prodotti in corso...</div>
              <div v-else-if="filteredProducts.length === 0" class="text-center py-8 text-gray-500">Nessun prodotto trovato.</div>
              <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <label v-for="prod in filteredProducts" :key="prod.asin" class="flex gap-3 p-4 rounded-2xl border transition-all cursor-pointer items-start" :class="(articleMode === 'multi' ? multiArticle.selectedAsins.includes(prod.asin) : singleArticle.selectedAsin === prod.asin) ? 'border-purple-500 bg-purple-50 dark:bg-purple-900/20 shadow-md' : 'border-gray-200 dark:border-gray-700 hover:border-purple-300 bg-white dark:bg-gray-800'">
                  <div class="pt-1">
                    <input v-if="articleMode === 'multi'" type="checkbox" v-model="multiArticle.selectedAsins" :value="prod.asin" class="w-5 h-5 text-purple-600 rounded focus:ring-purple-500" />
                    <input v-else type="radio" v-model="singleArticle.selectedAsin" :value="prod.asin" class="w-5 h-5 text-purple-600 focus:ring-purple-500" />
                  </div>
                  <div class="flex-1 flex gap-3 min-w-0">
                    <div class="w-12 h-12 rounded-xl bg-white flex-shrink-0 p-1 border border-gray-100">
                      <img :src="prod.image_url" class="w-full h-full object-contain" />
                    </div>
                    <div class="min-w-0">
                      <div class="text-sm font-bold text-gray-900 dark:text-white truncate" :title="prod.title">{{ prod.title }}</div>
                      <div class="text-xs text-gray-500 font-mono mt-1">{{ prod.asin }} • €{{ prod.price }}</div>
                    </div>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <div class="flex justify-end pt-6 border-t border-gray-200 dark:border-gray-700">
            <button @click="generateArticle" :disabled="!isFormValid || generating" class="px-8 py-3 bg-purple-600 text-white font-black rounded-2xl shadow-lg shadow-purple-500/30 hover:bg-purple-700 focus:scale-95 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center min-w-[200px]">
              <svg v-if="generating" class="w-5 h-5 mr-3 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              {{ generating ? 'Avvio...' : 'Genera Articolo' }}
            </button>
          </div>
        </div>
      </div>

      <!-- ARTICLES TABLE TAB (Original) -->
      <div v-show="currentTab === 'list'" class="rounded-3xl border border-white/20 bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl shadow-2xl overflow-hidden">
        <!-- Initial Loading State -->
        <div v-if="loading && articles.length === 0" class="p-12 text-center">
            <div class="animate-spin inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mb-4"></div>
            <p class="text-gray-500 font-bold">Caricamento articoli...</p>
        </div>
        
        <!-- Empty State -->
        <div v-else-if="articles.length === 0" class="p-16 text-center">
          <div class="text-gray-300 mb-4 inline-block p-4 bg-gray-50 dark:bg-gray-900 rounded-full">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10l4 4v10a2 2 0 01-2 2zM14 4v4h4" /></svg>
          </div>
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">Nessun articolo trovato</h3>
          <p class="text-gray-500 dark:text-gray-400 mt-2">Nessun contenuto generato al momento.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm text-left table-fixed">
            <thead class="bg-gray-50/50 dark:bg-gray-900/50 text-[10px] font-black uppercase text-gray-400 tracking-[0.2em]">
              <tr>
                <th class="px-6 py-5 w-32">Data</th>
                <th class="px-6 py-5 w-48">Copertina</th>
                <th class="px-6 py-5">Keyword / Titolo</th>
                <th class="px-6 py-5 w-28 text-center">Tipo</th>
                <th class="px-6 py-5 w-28 text-center">Stato</th>
                <th class="px-6 py-5 w-24 text-right">Azioni</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
              <tr v-for="article in articles" :key="article.id" class="group hover:bg-blue-50/20 dark:hover:bg-blue-900/5 transition-all">
                <td class="px-6 py-5 text-[11px] font-medium text-gray-400">{{ formatDate(article.created_at) }}</td>
                <td class="px-6 py-5">
                  <div class="flex items-center">
                    <div class="w-10 h-10 bg-white dark:bg-gray-700 rounded-lg shadow-sm border border-gray-100 dark:border-gray-600 p-1 flex-shrink-0">
                      <img v-if="article.product_image_url" :src="article.product_image_url" class="w-full h-full object-contain" />
                      <div v-else class="w-full h-full bg-gray-50 flex items-center justify-center"><span class="text-[8px]">NO IMG</span></div>
                    </div>
                    <div class="ml-3 overflow-hidden">
                      <div class="font-mono font-black text-[11px] text-blue-600 dark:text-blue-400">{{ article.asin || (article.asins ? article.asins[0]+' ...' : '') }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-5">
                  <div class="max-w-md">
                    <div class="font-black text-gray-900 dark:text-white truncate" :title="article.keyword">{{ article.keyword }}</div>
                    <div class="text-[10px] text-gray-400 truncate opacity-60" v-if="article.title">{{ article.title }}</div>
                  </div>
                </td>
                <td class="px-6 py-5 text-center">
                  <span v-if="article.asins && article.asins.length > 0" class="px-2 py-1 rounded bg-purple-100 text-purple-700 font-bold text-[9px] uppercase">Multiplo</span>
                  <span v-else class="px-2 py-1 rounded bg-gray-100 text-gray-700 font-bold text-[9px] uppercase">Singolo</span>
                </td>
                <td class="px-6 py-5 text-center">
                  <span :class="getStatusClass(article.status)" class="px-3 py-1 rounded-full text-[9px] font-black uppercase tracking-widest ring-1">
                    {{ article.status === 'queued' ? 'IN CODA' : (article.status === 'generating' ? 'ANALISI...' : article.status) }}
                  </span>
                </td>
                <td class="px-6 py-5 text-right flex items-center justify-end gap-2">
                  <a v-if="article.status === 'published'" :href="'/blog/' + article.slug" target="_blank" class="p-2 bg-blue-50 text-blue-600 rounded-xl hover:bg-blue-600 hover:text-white transition-all shadow-sm">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  </a>
                  <button @click="deleteArticle(article.id)" class="p-2 bg-rose-50 text-rose-600 rounded-xl hover:bg-rose-600 hover:text-white transition-all shadow-sm">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchWithToken } from "@/api";
import { useToast } from "@/store/toast";

export default {
  name: "AdminArticlesPage",
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      currentTab: 'list',
      articles: [],
      loading: true,
      polling: null,
      
      // Multi-Product Form
      articleMode: 'single',
      allProducts: [],
      loadingProducts: true,
      generating: false,
      enhancingKeyword: false,
      multiArticle: {
        keyword: "",
        categoryFilter: "",
        selectedAsins: []
      },
      singleArticle: {
        keyword: "",
        selectedAsin: ""
      }
    };
  },
  computed: {
    isFormValid() {
      if (this.articleMode === 'multi') {
        return this.multiArticle.selectedAsins.length > 0 && this.multiArticle.keyword;
      } else {
        return !!this.singleArticle.selectedAsin;
      }
    },
    uniqueCategories() {
      const cats = this.allProducts.map(p => p.category).filter(c => c);
      return [...new Set(cats)];
    },
    filteredProducts() {
      let filtered = this.allProducts;
      if (this.multiArticle.categoryFilter) {
        filtered = filtered.filter(p => p.category === this.multiArticle.categoryFilter);
      }
      return filtered;
    }
  },
  async created() {
    await this.fetchArticles();
    await this.fetchDashboardProducts();
    this.startPolling();
  },
  beforeUnmount() {
    if (this.polling) clearInterval(this.polling);
  },
  methods: {
    async fetchDashboardProducts() {
      this.loadingProducts = true;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/dashboard`);
        if (!response.ok) throw new Error("Errore recupero prodotti");
        const data = await response.json();
        this.allProducts = data.products || [];
      } catch (error) {
        console.error("Error matching products:", error);
      } finally {
        this.loadingProducts = false;
      }
    },
    async fetchArticles() {
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/articles`);
        if (!response.ok) throw new Error("Errore fetch articoli");
        this.articles = await response.json();
      } catch (error) {
        console.error("Error fetching articles:", error);
      } finally {
        this.loading = false;
      }
    },
    async deleteArticle(id) {
      if (!confirm("Sicuro di voler eliminare questo articolo?")) return;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/articles/${id}`, {
          method: "DELETE"
        });
        if (response.ok) {
          this.articles = this.articles.filter(a => a.id !== id);
          this.toast.success("Articolo eliminato.");
        }
      } catch (error) {
        this.toast.error("Errore durante l'eliminazione.");
      }
    },
    async enhanceKeyword() {
      const kw = this.articleMode === 'multi' ? this.multiArticle.keyword : this.singleArticle.keyword;
      if (!kw) return;
      this.enhancingKeyword = true;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/articles/enhance-keyword`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ keyword: kw })
        });
        if (response.ok) {
          const data = await response.json();
          if (this.articleMode === 'multi') {
            this.multiArticle.keyword = data.keyword;
          } else {
            this.singleArticle.keyword = data.keyword;
          }
          this.toast.success("Titolo ottimizzato dall'AI!");
        } else {
          this.toast.error("Errore durante l'ottimizzazione.");
        }
      } catch (e) {
        console.error("Error enhancing keyword:", e);
        this.toast.error("Errore di rete.");
      } finally {
        this.enhancingKeyword = false;
      }
    },
    async generateArticle() {
      if (!this.isFormValid) return;
      
      this.generating = true;
      
      const payload = {};
      if (this.articleMode === 'multi') {
        payload.asins = this.multiArticle.selectedAsins;
        payload.keyword = this.multiArticle.keyword;
      } else {
        payload.asin = this.singleArticle.selectedAsin;
        // La keyword è raccomandata ma facoltativa per le singole review, usiamo asin come fallback
        payload.keyword = this.singleArticle.keyword || "Recensione " + this.singleArticle.selectedAsin;
      }

      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/admin/articles/trigger`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        const data = await response.json();
        if (data.status === "already_exists") {
          this.toast.info("Generazione già in corso per questo set.");
        } else {
          this.toast.success("Generazione articolo avviata!");
          this.currentTab = 'list';
          if (this.articleMode === 'multi') {
            this.multiArticle = { keyword: "", categoryFilter: "", selectedAsins: [] };
          } else {
            this.singleArticle = { keyword: "", selectedAsin: "" };
          }
          this.fetchArticles();
        }
      } catch (error) {
        console.error("Error triggering AI listicle generation:", error);
        this.toast.error("Errore durante l'avvio della generazione.");
      } finally {
        this.generating = false;
      }
    },
    startPolling() {
      this.polling = setInterval(() => {
        // Only poll if there are items in transition
        const hasActiveTasks = this.articles.some(a => ['queued', 'generating'].includes(a.status));
        if (hasActiveTasks) this.fetchArticles();
      }, 3000);
    },
    formatDate(dateStr) {
      if (!dateStr) return "-";
      return new Date(dateStr).toLocaleString("it-IT", {
        day: "2-digit",
        month: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
      });
    },
    getStatusClass(status) {
      switch (status) {
        case "published": return "bg-emerald-100 text-emerald-700 ring-emerald-200 dark:bg-emerald-900/30 dark:text-emerald-400";
        case "generating": return "bg-blue-100 text-blue-700 ring-blue-200 dark:bg-blue-900/30 dark:text-blue-400 animate-pulse";
        case "failed": return "bg-rose-100 text-rose-700 ring-rose-200 dark:bg-rose-900/30 dark:text-rose-400";
        default: return "bg-gray-100 text-gray-700 ring-gray-200 dark:bg-gray-900/30 dark:text-gray-400";
      }
    }
  }
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}
</style>
