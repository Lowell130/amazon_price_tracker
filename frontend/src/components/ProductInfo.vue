<template>
  <section class="relative overflow-hidden bg-white dark:bg-gray-900 antialiased rounded-3xl shadow-xl border border-gray-100 dark:border-gray-800 backdrop-blur-md bg-opacity-80 dark:bg-opacity-80 transition-all duration-300">
    <!-- Decoro Sfondo (Subtle Glows) -->
    <div class="absolute -top-24 -right-24 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-screen-xl px-6 py-10 mx-auto lg:py-16">
      <div class="lg:grid lg:grid-cols-12 lg:gap-12 items-start">
        
        <!-- Colonna Immagine -->
        <div class="lg:col-span-5 xl:col-span-5">
          <div class="relative group p-6 bg-gradient-to-tr from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 rounded-3xl shadow-inner border border-gray-100 dark:border-gray-700 flex items-center justify-center min-h-[400px] overflow-hidden">
            <img
              class="w-full h-full max-h-[350px] object-contain transform group-hover:scale-110 transition-transform duration-700 ease-out"
              :src="product.image_url"
              :alt="product.title"
              @error="handleImageError"
            />
            
            <!-- Badge Condizione Premium -->
            <div class="absolute top-6 left-6">
               <div v-if="product.condition === 'Nuovo'"
                class="flex items-center gap-1.5 bg-emerald-500 text-white text-[10px] uppercase tracking-widest font-black px-4 py-1.5 rounded-full shadow-lg shadow-emerald-500/30">
                <span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>
                Nuovo
              </div>
              <div v-else-if="product.condition === 'Usato'"
                class="flex items-center gap-1.5 bg-amber-500 text-white text-[10px] uppercase tracking-widest font-black px-4 py-1.5 rounded-full shadow-lg shadow-amber-500/30">
                Usato
              </div>
              <div v-else
                class="bg-rose-500 text-white text-[10px] uppercase tracking-widest font-black px-4 py-1.5 rounded-full shadow-lg shadow-rose-500/30">
                N/A
              </div>
            </div>
          </div>
        </div>

        <!-- Colonna Informazioni -->
        <div class="mt-10 lg:mt-0 lg:col-span-7 xl:col-span-7 flex flex-col justify-center">
          <!-- Header info -->
          <div class="flex items-center gap-2 mb-4">
            <span class="text-[10px] font-bold uppercase tracking-widest text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/40 px-3 py-1 rounded-lg">
              {{ product.category }}
            </span>
            <span class="text-xs font-mono text-gray-400 dark:text-gray-500">
              ASIN: {{ product.asin }}
            </span>
          </div>

          <h1 class="text-3xl font-black text-gray-900 lg:text-4xl dark:text-white mb-6 leading-[1.15] tracking-tight">
            {{ product.title }}
          </h1>

          <!-- Card Prezzo Dinamica -->
          <div class="relative p-6 mb-8 bg-white/50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-3xl overflow-hidden group">
            <div class="flex items-start justify-between">
              <div>
                <p class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-2">Prezzo Attuale</p>
                <div class="flex items-end gap-3 flex-wrap">
                    <p v-if="product.availability !== 'Non disponibile'" class="text-5xl font-black text-gray-900 dark:text-white tracking-tighter">
                        {{ product.price }}<span class="text-2xl ml-0.5">€</span>
                    </p>
                    <p v-else class="text-5xl font-black text-gray-900 dark:text-white tracking-tighter">
                        N/A
                    </p>
                    
                    <!-- Coupon High Visibility -->
                    <div v-if="product.coupon_value" class="mb-1 pointer-events-none select-none">
                      <div class="relative flex items-center bg-emerald-50 border border-emerald-200 text-emerald-700 dark:bg-emerald-900/30 dark:border-emerald-700 dark:text-emerald-400 px-4 py-1.5 rounded-xl font-bold text-sm shadow-sm group-hover:scale-105 transition-transform duration-300">
                        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20"><path d="M5 5a3 3 0 015-2.236A3 3 0 0114.83 6H16a2 2 0 110 4h-5V9a1 1 0 10-2 0v1H4a2 2 0 110-4h1.17C5.06 5.687 5 5.35 5 5zm4 1V5a1 1 0 10-1 1h1zm3 0a1 1 0 10-1-1v1h1z" clip-rule="evenodd"></path><path d="M9 11H3v5a2 2 0 002 2h4v-7zM11 18h4a2 2 0 002-2v-5h-6v7z"></path></svg>
                        COUPON -€{{ product.coupon_value }}
                      </div>
                    </div>
                </div>
                <p class="text-[10px] text-gray-400 dark:text-gray-500 mt-4 uppercase tracking-[0.2em] font-medium">Aggiornato il {{ formatDate(product.insertion_date) }}</p>
              </div>

              <!-- Rating / Altri info? (Placeholders for rich details) -->
              <div v-if="product.rating" class="flex flex-col items-end">
                <div class="flex items-center gap-1 text-amber-400">
                  <svg v-for="i in 5" :key="i" class="w-4 h-4" :fill="i <= Math.round(product.rating) ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.175 0l-3.976 2.888c-.783.57-1.838-.197-1.539-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.381-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path></svg>
                </div>
              </div>
            </div>
          </div>

          <!-- Pulsanti d'Azione -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <a :href="product.affiliate" target="_blank"
              class="relative overflow-hidden group flex items-center justify-center text-white bg-slate-900 dark:bg-blue-600 font-black rounded-2xl text-base px-8 py-5 transition-all shadow-xl hover:shadow-2xl hover:-translate-y-1">
              <span class="flex items-center relative z-10 uppercase tracking-widest text-sm">
                Acquista ora
                <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-blue-600 to-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </a>
            
            <button @click="showModal = true"
              class="flex items-center justify-center text-gray-800 dark:text-white bg-white dark:bg-gray-800 border-2 border-gray-100 dark:border-gray-700 font-bold rounded-2xl text-base px-8 py-5 transition-all hover:border-blue-400 dark:hover:border-blue-500 hover:text-blue-600 dark:hover:text-blue-400 shadow-lg shadow-gray-200/20 dark:shadow-none hover:-translate-y-1">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
              <span class="uppercase tracking-widest text-sm">Pianifica avviso</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale Glassmorphism -->
    <Teleport to="body">
      <div v-if="showModal"
        class="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/40 backdrop-blur-xl px-4 p-6 overflow-y-auto">
        <div class="bg-white/95 dark:bg-gray-900/95 p-8 md:p-12 rounded-[2.5rem] w-full max-w-lg relative shadow-[0_35px_100px_-15px_rgba(0,0,0,0.3)] border border-white/20 dark:border-gray-700 transform transition-all duration-500 ease-out scale-100"
             @click.stop>
          
          <!-- Chiudi -->
          <button @click="showModal = false"
            class="absolute top-6 right-6 p-2 rounded-full text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-all">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>

          <div class="text-center mb-10">
              <div class="mx-auto flex items-center justify-center h-20 w-20 rounded-3xl bg-blue-600 text-white shadow-xl shadow-blue-500/30 mb-8 rotate-3 hover:rotate-0 transition-transform duration-500">
                  <svg class="h-10 w-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
              </div>
              <h3 class="text-3xl font-black text-gray-900 dark:text-white leading-tight">
              Monitoraggio Prezzi
              </h3>
              <p class="text-gray-500 dark:text-gray-400 mt-4 text-base font-medium px-4">
              Ricevi una notifica istantanea appena il prezzo scende sotto la tua soglia desiderata.
              </p>
          </div>

          <div class="space-y-6">
            <div class="relative group">
              <input v-model="email" type="email" placeholder="Inserisci la tua email..."
                class="w-full pl-6 pr-6 py-5 bg-gray-50 dark:bg-gray-800/50 border-2 border-gray-100 dark:border-gray-700 rounded-2xl text-gray-900 dark:text-white placeholder:text-gray-400 dark:placeholder:text-gray-500 outline-none focus:border-blue-500 transition-all duration-300" />
            </div>

            <div class="flex flex-col gap-4">
              <button @click="subscribeToPriceDrop"
                class="w-full py-5 text-sm font-black uppercase tracking-[0.2em] text-white bg-blue-600 hover:bg-blue-700 rounded-2xl shadow-xl shadow-blue-500/20 transition-all active:scale-95 flex items-center justify-center"
                :disabled="isLoading">
                <span v-if="!isLoading">Attiva Monitoraggio</span>
                <span v-else class="flex items-center">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24 text-white"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                  Elaborazione...
                </span>
              </button>
              
              <button @click="unsubscribeFromPriceDrop"
                class="w-full py-4 text-xs font-bold uppercase tracking-widest text-gray-400 hover:text-rose-500 transition-colors"
                :disabled="isLoading">
                Rimuovi iscrizione precedente
              </button>
            </div>

            <!-- Feedback Mesages Removed - Handled by Toasts -->
          </div>
        </div>
      </div>
    </Teleport>
  </section>
</template>

<script>
import { useToast } from '@/store/toast';

export default {
  name: "ProductInfo",
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const { success, error, warning } = useToast();
    return { success, error, warning };
  },
  data() {
    return {
      showModal: false,
      email: "",
      isLoading: false,
    };
  },
  methods: {
    formatDate(date) {
      const options = {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(date).toLocaleDateString("it-IT", options);
    },
    handleImageError(e) {
      e.target.src = 'https://via.placeholder.com/400x400?text=Immagine+non+disponibile';
    },

    async subscribeToPriceDrop() {
      this.isLoading = true;

      if (!this.email.includes("@")) {
        this.error("Inserisci un'email valida.");
        this.isLoading = false;
        return;
      }

      try {
        const res = await fetch(`${process.env.VUE_APP_API_BASE_URL}/public/subscribe-alert`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, asin: this.product.asin }),
        });

        const data = await res.json();

        if (!res.ok) throw new Error(data.detail || "Errore durante la registrazione.");

        this.success(data.message || "Iscrizione avvenuta con successo!");
        this.email = "";
        this.showModal = false;
      } catch (err) {
        this.error(err.message || "Errore generico. Riprova.");
      } finally {
        this.isLoading = false;
      }
    },

    async unsubscribeFromPriceDrop() {
      this.isLoading = true;

      if (!this.email.includes("@")) {
        this.error("Inserisci un'email valida.");
        this.isLoading = false;
        return;
      }

      try {
        const res = await fetch(
          `${process.env.VUE_APP_API_BASE_URL}/public/unsubscribe-alert?email=${encodeURIComponent(
            this.email
          )}&asin=${this.product.asin}`,
          { method: "DELETE" }
        );

        const data = await res.json();

        if (!res.ok) throw new Error(data.detail || "Errore durante la disiscrizione.");

        this.success(data.message || "Disiscrizione completata!");
        this.email = "";
        this.showModal = false;
      } catch (err) {
        this.error(err.message || "Errore generico durante la disiscrizione.");
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
