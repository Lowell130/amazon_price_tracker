<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20 antialiased selection:bg-blue-100 selection:text-blue-700">
    <div class="mx-auto max-w-screen-2xl px-6 lg:px-12 pt-12">
      
      <!-- Header -->
      <div class="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <nav class="mb-4 flex items-center text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] gap-2">
            <router-link to="/dashboard" class="hover:text-blue-500 transition-colors">Admin</router-link>
            <span>/</span>
            <span class="text-gray-900 dark:text-white">Analytics</span>
          </nav>
          <h1 class="text-4xl md:text-5xl font-black text-gray-900 dark:text-white tracking-tight">
            Monitor <span class="text-blue-600">Performance</span>
          </h1>
          <p class="text-gray-500 dark:text-gray-400 mt-2 font-medium">Analisi del traffico in ingresso e dei clic in uscita verso Amazon.</p>
        </div>
        <div class="flex gap-3">
            <button @click="clearAnalytics" class="px-6 py-3 bg-red-50 dark:bg-red-900/10 text-red-600 font-black rounded-2xl shadow-sm border border-red-100 dark:border-red-900/20 hover:bg-red-600 hover:text-white transition-all flex items-center gap-2 group">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              Reset Dati
            </button>
            <button @click="fetchStats" class="px-6 py-3 bg-white dark:bg-gray-900 text-gray-900 dark:text-white font-black rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800 hover:shadow-xl transition-all flex items-center gap-2 group">
              <svg :class="{ 'animate-spin': loading }" class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
              Aggiorna Dati
            </button>
        </div>
      </div>

      <!-- Main Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <!-- Visits -->
        <div class="p-8 rounded-[2.5rem] bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-xl group hover:shadow-blue-500/5 transition-all">
          <div class="flex items-center justify-between mb-6">
            <div class="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-2xl text-blue-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            </div>
            <span class="text-[10px] font-black text-emerald-500 uppercase tracking-widest">Live</span>
          </div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Visite Totali</p>
          <h3 class="text-4xl font-black text-gray-900 dark:text-white tracking-tighter">{{ stats?.summary?.total_visits || 0 }}</h3>
        </div>

        <!-- Clicks -->
        <div class="p-8 rounded-[2.5rem] bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-xl group hover:shadow-orange-500/5 transition-all">
          <div class="flex items-center justify-between mb-6">
            <div class="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-2xl text-orange-500">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            </div>
            <span class="text-[10px] font-black text-orange-500 uppercase tracking-widest">Affiliazione</span>
          </div>
          <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Clic Amazon</p>
          <h3 class="text-4xl font-black text-gray-900 dark:text-white tracking-tighter">{{ stats?.summary?.total_clicks || 0 }}</h3>
        </div>

        <!-- CTR -->
        <div class="p-8 rounded-[2.5rem] bg-blue-600 text-white shadow-2xl shadow-blue-500/20 group transition-all">
          <div class="flex items-center justify-between mb-6">
            <div class="p-4 bg-white/20 backdrop-blur-md rounded-2xl">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            <span class="text-[10px] font-black uppercase tracking-widest opacity-80">Conversion</span>
          </div>
          <p class="text-[10px] font-black uppercase tracking-widest mb-1 opacity-60">Click-Through Rate (CTR)</p>
          <h3 class="text-4xl font-black tracking-tighter">{{ stats?.summary?.ctr || 0 }}%</h3>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Top Referrers -->
        <div class="p-8 rounded-[2.5rem] bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-xl overflow-hidden">
          <div class="flex items-center justify-between mb-8">
            <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Sorgenti <span class="text-blue-600">Traffico</span></h3>
            <div class="w-10 h-1 text-blue-500/20 bg-blue-500/20 rounded-full"></div>
          </div>
          
          <div v-if="!stats?.top_referrers?.length" class="py-20 text-center">
            <p class="text-gray-400 font-bold">Nessun dato sorgente disponibile.</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="(ref, i) in stats.top_referrers" :key="i" class="flex items-center justify-between p-4 bg-gray-50/50 dark:bg-gray-800/50 rounded-2xl group hover:bg-white dark:hover:bg-gray-800 transition-all border border-transparent hover:border-gray-100 dark:hover:border-gray-700">
              <div class="flex items-center gap-4 overflow-hidden">
                <div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-[10px] font-black text-blue-600">
                  {{ i + 1 }}
                </div>
                <span class="text-sm font-bold text-gray-700 dark:text-gray-200 truncate">{{ ref.source }}</span>
              </div>
              <div class="text-right">
                <span class="text-sm font-black text-gray-900 dark:text-white">{{ ref.count }}</span>
                <span class="text-[10px] text-gray-400 font-bold ml-1 uppercase">v</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Products -->
        <div class="p-8 rounded-[2.5rem] bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-xl overflow-hidden">
          <div class="flex items-center justify-between mb-8">
            <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Prodotti <span class="text-orange-500">Top</span></h3>
            <div class="h-1 flex-1 mx-6 bg-gray-50 dark:bg-gray-800 rounded-full"></div>
          </div>

          <div v-if="!stats?.top_products?.length" class="py-20 text-center">
            <p class="text-gray-400 font-bold">Nessun clic registrato sui prodotti.</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="prod in stats.top_products" :key="prod.asin" class="flex items-center justify-between p-4 bg-gray-50/50 dark:bg-gray-800/50 rounded-2xl group hover:bg-white dark:hover:bg-gray-800 transition-all border border-transparent hover:border-gray-100 dark:hover:border-gray-700">
              <div class="flex items-center gap-4 overflow-hidden">
                <div class="w-12 h-12 bg-white dark:bg-gray-700 rounded-xl p-1 border border-gray-100 dark:border-gray-600 shadow-sm flex-shrink-0">
                  <img :src="prod.image_url" class="w-full h-full object-contain" />
                </div>
                <div class="overflow-hidden">
                  <span class="text-xs font-black text-gray-900 dark:text-white truncate block">{{ prod.title }}</span>
                  <span class="text-[9px] font-mono text-gray-400 uppercase">{{ prod.asin }}</span>
                </div>
              </div>
              <div class="text-right flex-shrink-0 ml-4">
                <span class="text-lg font-black text-orange-500">{{ prod.count }}</span>
                <span class="text-[9px] text-gray-400 font-bold ml-1 uppercase block">click</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchWithToken } from "@/api";

export default {
  name: "AdminAnalytics",
  data() {
    return {
      stats: null,
      loading: true
    };
  },
  async created() {
    await this.fetchStats();
  },
  methods: {
    async fetchStats() {
      this.loading = true;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/analytics/admin/stats`);
        if (response.ok) {
          this.stats = await response.json();
        }
      } catch (e) {
        console.error("Error fetching stats:", e);
      } finally {
        this.loading = false;
      }
    },
    async clearAnalytics() {
      if (!confirm("Sei sicuro di voler cancellare tutti i dati analytics? Questa operazione non è reversibile.")) return;
      
      try {
        console.log("Attempting to clear analytics...");
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/analytics/admin/clear`, {
          method: 'DELETE'
        });
        
        if (response.ok) {
          const resData = await response.json();
          console.log("Analytics cleared:", resData);
          this.stats = null;
          await this.fetchStats();
          alert("Dati analytics resettati con successo.");
        } else {
          const errData = await response.json().catch(() => ({}));
          console.error("Failed to clear analytics:", response.status, errData);
          alert(`Errore durante il reset: ${response.status} ${errData.detail || ''}`);
        }
      } catch (e) {
        console.error("Error clearing analytics:", e);
        alert("Errore di connessione durante il reset.");
      }
    }
  }
};
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
