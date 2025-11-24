<template>
  <section class="py-8 bg-white md:py-16 dark:bg-gray-900 antialiased rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800">
    <div class="max-w-screen-xl px-4 mx-auto 2xl:px-0">
      <div class="lg:grid lg:grid-cols-2 lg:gap-12 xl:gap-16">
        
        <!-- Immagine -->
        <div class="shrink-0 max-w-md lg:max-w-lg mx-auto w-full">
          <div class="relative p-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 flex items-center justify-center h-[400px]">
            <img
              class="w-full h-full object-contain dark:hidden transform hover:scale-105 transition-transform duration-500"
              :src="product.image_url"
              :alt="product.title"
            />
            <img
              class="w-full h-full object-contain hidden dark:block transform hover:scale-105 transition-transform duration-500"
              :src="product.image_url"
              :alt="product.title"
            />
            
            <!-- Badge Condizione -->
            <div class="absolute top-4 left-4">
               <span v-if="product.condition === 'Nuovo'"
                class="bg-green-100 text-green-800 text-xs font-bold px-3 py-1.5 rounded-full dark:bg-green-900 dark:text-green-300 shadow-sm">
                Nuovo
              </span>
              <span v-else-if="product.condition === 'Usato'"
                class="bg-yellow-100 text-yellow-800 text-xs font-bold px-3 py-1.5 rounded-full dark:bg-yellow-900 dark:text-yellow-300 shadow-sm">
                Usato
              </span>
              <span v-else
                class="bg-red-100 text-red-800 text-xs font-bold px-3 py-1.5 rounded-full dark:bg-red-900 dark:text-red-300 shadow-sm">
                Non disponibile
              </span>
            </div>
          </div>
        </div>

        <!-- Dettagli -->
        <div class="mt-8 lg:mt-0 lg:pr-6">
          <h1 class="text-2xl font-extrabold text-gray-900 sm:text-3xl dark:text-white mb-4 leading-tight">
            {{ product.title }}
          </h1>

          <div class="flex items-center gap-4 mb-6">
             <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded dark:bg-blue-900 dark:text-blue-300">
                {{ product.category }}
             </span>
             <span class="text-gray-500 text-sm dark:text-gray-400">ASIN: {{ product.asin }}</span>
          </div>

          <!-- Prezzo -->
           <div class="lg:pr-6">
          <div class="mb-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Prezzo Attuale</p>
            <div class="flex items-end gap-3">
                <p v-if="product.availability !== 'Non disponibile'" class="text-4xl font-extrabold text-gray-900 dark:text-white tracking-tight">
                    {{ product.price }}€
                </p>
                <p v-else class="text-4xl font-extrabold text-gray-900 dark:text-white tracking-tight">
                    N/A
                </p>
                
                <!-- Coupon -->
                <span v-if="product.coupon_value" class="mb-1 bg-green-100 text-green-800 text-sm font-bold px-3 py-1 rounded-full dark:bg-green-900 dark:text-green-300 flex items-center gap-1">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5 5a3 3 0 015-2.236A3 3 0 0114.83 6H16a2 2 0 110 4h-5V9a1 1 0 10-2 0v1H4a2 2 0 110-4h1.17C5.06 5.687 5 5.35 5 5zm4 1V5a1 1 0 10-1 1h1zm3 0a1 1 0 10-1-1v1h1z" clip-rule="evenodd"></path><path d="M9 11H3v5a2 2 0 002 2h4v-7zM11 18h4a2 2 0 002-2v-5h-6v7z"></path></svg>
                    -€{{ product.coupon_value }}
                </span>
            </div>
            <p class="text-xs text-gray-500 mt-2">Rilevato il: {{ formatDate(product.insertion_date) }}</p>
          </div>

          <!-- Azioni -->
          <div class="flex flex-col sm:flex-row gap-4">
            <a :href="product.affiliate" target="_blank"
              class="flex-1 flex items-center justify-center text-white bg-gradient-to-r from-yellow-400 to-orange-500 hover:from-yellow-500 hover:to-orange-600 focus:ring-4 focus:ring-yellow-300 font-bold rounded-xl text-lg px-6 py-4 transition-all transform hover:-translate-y-1 shadow-lg shadow-orange-500/30">
              Vedi su Amazon
              <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </a>
            
            <button @click="showModal = true"
              class="flex-1 flex items-center justify-center text-blue-600 bg-blue-50 hover:bg-blue-100 border border-blue-200 focus:ring-4 focus:ring-blue-100 font-bold rounded-xl text-lg px-6 py-4 transition-all dark:bg-gray-800 dark:text-blue-400 dark:border-gray-700 dark:hover:bg-gray-700">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
              Avvisami quando scende
            </button>
          </div>
</div>
        </div>
      </div>
    </div>

    <!-- Modale -->
    <div v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4">
      <div class="bg-white dark:bg-gray-800 p-8 rounded-2xl w-full max-w-md relative shadow-2xl border border-gray-100 dark:border-gray-700 transform transition-all scale-100">
        <!-- Chiudi -->
        <button @click="showModal = false"
          class="absolute top-4 right-4 text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <div class="text-center mb-6">
            <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900 mb-4">
                <svg class="h-6 w-6 text-blue-600 dark:text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
            Avvisi di Prezzo
            </h3>
            <p class="text-gray-500 dark:text-gray-400 mt-2">
            Non perderti l'affare. Ti invieremo una mail appena il prezzo scende.
            </p>
        </div>

        <input v-model="email" type="email" placeholder="latua@email.com"
          class="w-full p-4 mb-4 border border-gray-300 rounded-xl bg-gray-50 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 transition-all" />

        <div class="flex flex-col gap-3">
          <button @click="subscribeToPriceDrop"
            class="w-full px-4 py-3.5 text-base font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-lg shadow-blue-500/30 transition-all transform hover:-translate-y-0.5"
            :disabled="isLoading">
            {{ isLoading ? 'Attendi...' : 'Iscriviti agli Avvisi' }}
          </button>
          <button @click="unsubscribeFromPriceDrop"
            class="w-full px-4 py-3.5 text-base font-medium text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-xl transition-colors"
            :disabled="isLoading">
            Disiscriviti
          </button>
        </div>

        <div class="mt-4 text-center">
          <p v-if="successMessage" class="text-green-500 font-medium bg-green-50 dark:bg-green-900/30 p-2 rounded-lg">{{ successMessage }}</p>
          <p v-if="errorMessage" class="text-red-500 font-medium bg-red-50 dark:bg-red-900/30 p-2 rounded-lg">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "ProductInfo",
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      email: "",
      successMessage: "",
      errorMessage: "",
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

    async subscribeToPriceDrop() {
      this.successMessage = "";
      this.errorMessage = "";
      this.isLoading = true;

      if (!this.email.includes("@")) {
        this.errorMessage = "Inserisci un'email valida.";
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

        if (!res.ok) throw new Error(data.detail || "Errore durante la registrazione e indirizzo presente.");

        this.successMessage = data.message || "Iscrizione avvenuta con successo!";
        this.email = "";
      } catch (err) {
        this.errorMessage = err.message || "Errore generico. Riprova.";
      } finally {
        this.isLoading = false;
      }
    },

    async unsubscribeFromPriceDrop() {
      this.successMessage = "";
      this.errorMessage = "";
      this.isLoading = true;

      if (!this.email.includes("@")) {
        this.errorMessage = "Inserisci un'email valida.";
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

        this.successMessage = data.message || "Disiscrizione completata!";
        this.email = "";
      } catch (err) {
        this.errorMessage = err.message || "Errore generico durante la disiscrizione.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
