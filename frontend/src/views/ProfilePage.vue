<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 py-12 px-4 sm:px-6 lg:px-12">
    <div class="max-w-4xl mx-auto space-y-8">
      
      <!-- Top Section: Header & Profile Card -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Profile info card (1 col) -->
        <div class="lg:col-span-1 bg-white dark:bg-gray-900 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden group">
          <div class="h-24 bg-gradient-to-br from-blue-600 to-indigo-700"></div>
          <div class="px-6 pb-8 text-center relative">
            <div class="-mt-12 mb-4 flex justify-center">
              <div class="p-1 bg-white dark:bg-gray-800 rounded-full shadow-xl">
                <img :src="avatarUrl" class="h-24 w-24 rounded-full bg-gray-50 dark:bg-gray-700" :alt="username" />
              </div>
            </div>
            <h2 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">{{ username }}</h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ email }}</p>
            <div class="flex justify-center">
              <span v-if="isAdmin" class="px-3 py-1 bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 text-[10px] font-black uppercase tracking-widest rounded-lg border border-rose-100 dark:border-rose-900/50">
                Administrator
              </span>
              <span v-else class="px-3 py-1 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 text-[10px] font-black uppercase tracking-widest rounded-lg border border-blue-100 dark:border-blue-900/50">
                Member
              </span>
            </div>
          </div>
        </div>

        <!-- Stats & Highlights (2 cols) -->
        <div class="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="bg-white dark:bg-gray-900 p-8 rounded-[2rem] shadow-sm border border-gray-100 dark:border-gray-800 flex flex-col justify-between group hover:border-blue-500/30 transition-all">
            <div>
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-[0.2em] mb-2">Monitoraggio Attivo</p>
              <h3 class="text-4xl font-black text-gray-900 dark:text-white">{{ productsCount }}</h3>
            </div>
            <p class="text-sm text-gray-500 mt-4 leading-relaxed font-medium">Prodotti attualmente sotto il tuo controllo.</p>
          </div>
          <div class="bg-gradient-to-br from-slate-900 to-slate-800 dark:from-blue-600 dark:to-indigo-700 p-8 rounded-[2rem] shadow-xl text-white flex flex-col justify-between">
            <div class="flex justify-between items-start">
              <div>
                <p class="text-[10px] font-black opacity-60 uppercase tracking-[0.2em] mb-2">Canale Telegram</p>
                <h3 class="text-xl font-bold">Notifiche Smart</h3>
              </div>
              <div class="p-3 bg-white/10 rounded-2xl backdrop-blur-md">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              </div>
            </div>
            <button @click="connectTelegram" class="mt-6 w-full py-3 bg-white text-slate-900 dark:text-blue-600 font-black text-xs uppercase tracking-widest rounded-xl hover:bg-blue-50 transition-colors">
              Configura Bot
            </button>
          </div>
        </div>
      </div>

      <!-- Admin Tools Section -->
      <div v-if="isAdmin" class="bg-white dark:bg-gray-900 rounded-[2.5rem] shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden">
        <div class="p-8 border-b border-gray-50 dark:border-gray-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">
              Strumenti <span class="text-rose-500">Amministratore</span>
            </h3>
            <p class="text-sm text-gray-500 font-medium mt-1">Gestione globale del sistema di tracciamento</p>
          </div>
          <div class="flex items-center gap-3">
             <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
             <span class="text-[10px] font-black text-emerald-600 uppercase tracking-widest">Automation Active</span>
          </div>
        </div>
        <div class="p-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="p-6 bg-gray-50 dark:bg-gray-800/50 rounded-3xl border border-transparent hover:border-gray-200 dark:hover:border-gray-750 transition-all">
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-4">Ultimo Report</p>
            <div class="text-lg font-bold text-gray-900 dark:text-white mb-6">
              {{ lastUpdateDate || 'In attesa...' }}
            </div>
            <button @click="generatePriceDropsReport" 
                    class="w-full py-3 px-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 text-[10px] font-black uppercase tracking-widest rounded-xl hover:opacity-90 transition-opacity">
              Rigenera Manualmente
            </button>
          </div>
          
          <div class="md:col-span-2 p-6 bg-blue-50 dark:bg-blue-900/10 rounded-3xl border border-blue-100/50 dark:border-blue-900/30 flex items-center gap-6">
            <div class="h-12 w-12 rounded-2xl bg-blue-100 dark:bg-blue-800 flex items-center justify-center flex-shrink-0 text-blue-600">
               <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
            </div>
            <div>
              <h4 class="font-bold text-blue-900 dark:text-blue-100">Aggiornamento Automatico</h4>
              <p class="text-sm text-blue-700/70 dark:text-blue-300/60 leading-relaxed mt-1">
                Il sistema scansiona i prezzi e aggiorna Telegram e la Home Page ogni 12 ore.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- General Settings & Footer -->
      <div class="flex flex-col md:flex-row items-center justify-between gap-6 px-4">
        <button @click="logout" class="text-red-500 font-black text-xs uppercase tracking-widest hover:bg-red-50 dark:hover:bg-red-900/20 px-6 py-3 rounded-xl transition-colors inline-flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          Scollegati Account
        </button>
        <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Amazon Tracker Premium v2.0</p>
      </div>

    </div>
  </div>
</template>

<script>
import { fetchWithToken } from "@/api";

export default {
  name: "ProfilePage",
  data() {
    return {
      username: "",
      email: "",
      isAdmin: false,
      productsCount: 0,
      lastUpdateDate: null,
    };
  },
  computed: {
    avatarUrl() {
      const seed = this.username || "default";
      return `https://robohash.org/${seed}?set=set4&bgset=&size=400x400`;
    }
  },
  created() {
    this.getUserInfo();
    this.getLastUpdateStatus();
  },
  methods: {
    async getUserInfo() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/auth/users/me`
        );
        if (!response.ok) throw new Error();
        const userData = await response.json();
        this.username = userData.username;
        this.email = userData.email;
        this.isAdmin = userData.admin;
        this.productsCount = userData.products_count || 0;
      } catch (error) {
        this.logout();
      }
    },
    async getLastUpdateStatus() {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/public/price-drops`);
        if (response.ok) {
          const data = await response.json();
          if (data.generation_date) {
            const date = new Date(data.generation_date);
            this.lastUpdateDate = date.toLocaleString('it-IT', {
              day: '2-digit', month: '2-digit', year: 'numeric',
              hour: '2-digit', minute: '2-digit'
            });
          }
        }
      } catch (e) {
        console.error("Errore recupero stato aggiornamento:", e);
      }
    },
    async generatePriceDropsReport() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/admin/generate-price-drops-report`,
          { method: "POST" }
        );
        if (response.ok) {
           alert("Report rigenerato con successo!");
           this.getLastUpdateStatus();
        }
      } catch (error) {
        alert("Errore durante la generazione.");
      }
    },
    async connectTelegram() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/auth/connect-telegram`,
          { method: "POST" }
        );
        if (response.ok) {
          const data = await response.json();
          window.open(data.telegram_link, '_blank');
        }
      } catch (error) {
        alert("Impossibile generare il link Telegram.");
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  }
};
</script>
