<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12 antialiased">
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-8 pt-8">
      <!-- Header -->
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">Gestione Articoli AI</h1>
          <p class="text-gray-500 dark:text-gray-400 mt-1">Monitora lo stato della coda di generazione e gestisci i contenuti pubblicati.</p>
        </div>
        <router-link to="/dashboard" class="px-5 py-2.5 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 font-bold rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 transition-all">
          &larr; Torna alla Dashboard
        </router-link>
      </div>

      <!-- Articles Table -->
      <div class="rounded-3xl border border-white/20 bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl shadow-2xl overflow-hidden">
        <!-- Initial Loading State (only if list is empty) -->
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
          <p class="text-gray-500 dark:text-gray-400 mt-2">Inizia a generare recensioni dalla tua dashboard prodotti.</p>
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm text-left table-fixed">
            <thead class="bg-gray-50/50 dark:bg-gray-900/50 text-[10px] font-black uppercase text-gray-400 tracking-[0.2em]">
              <tr>
                <th class="px-6 py-5 w-32">Data</th>
                <th class="px-6 py-5 w-48">Prodotto</th>
                <th class="px-6 py-5">Keyword / Titolo</th>
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
                      <div class="font-mono font-black text-[11px] text-blue-600 dark:text-blue-400">{{ article.asin }}</div>
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
      articles: [],
      loading: true,
      polling: null
    };
  },
  async created() {
    await this.fetchArticles();
    this.startPolling();
  },
  beforeUnmount() {
    if (this.polling) clearInterval(this.polling);
  },
  methods: {
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
