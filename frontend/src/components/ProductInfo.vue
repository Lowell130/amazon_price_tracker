<template>
  <section class="py-8 bg-white md:py-16 dark:bg-gray-900 antialiased rounded-t-lg">
    <div class="max-w-screen-xl px-4 mx-auto 2xl:px-0">
      <div class="lg:grid lg:grid-cols-2 lg:gap-8 xl:gap-16 px-3">
        <!-- Immagine -->
        <div class="shrink-0 max-w-md lg:max-w-lg mx-auto">
          <img
            class="w-full max-h-[300px] sm:max-h-[400px] object-contain mx-auto dark:hidden"
            :src="product.image_url"
            :alt="product.title"
          />
        </div>

        <!-- Dettagli -->
        <div class="mt-6 sm:mt-8 lg:mt-0 p-3">
          <h1 class="text-xl font-semibold text-gray-900 sm:text-2xl dark:text-white mb-3">
            {{ product.title }}
          </h1>
          <p class="text-gray-600 text-sm mb-2">Category: {{ product.category }}</p>
          <p class="text-gray-600 text-sm mb-2">ASIN: {{ product.asin }}</p>
          <p class="text-gray-600 text-sm mb-2">
            Insertion Date: {{ formatDate(product.insertion_date) }}
          </p>

          <!-- Condizione -->
          <p class="text-gray-600 text-sm mb-2">
            Condition:
            <span v-if="product.condition === 'Nuovo'"
              class="bg-green-100 text-green-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-green-900 dark:text-green-300">New</span>
            <span v-else-if="product.condition === 'Usato'"
              class="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300">Used</span>
            <span v-else
              class="bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-red-900 dark:text-red-300">Unavailable</span>
          </p>

          <!-- Prezzo -->
          <p v-if="product.availability !== 'Non disponibile'"
            class="text-2xl font-extrabold text-gray-900 sm:text-3xl dark:text-white">
            {{ product.price }}€
          </p>
          <p v-else
            class="text-2xl font-extrabold text-gray-900 sm:text-3xl dark:text-white flex items-center">
            N/A
            <svg class="w-5 h-5 ml-1 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v8m4-4H8" />
            </svg>
          </p>

          <!-- Coupon -->
          <div v-if="product.coupon_value" class="mt-2">
            <span
              class="inline-block bg-green-100 text-green-800 text-sm font-medium px-3 py-1 rounded dark:bg-green-900 dark:text-green-300">
              Coupon disponibile: -€{{ product.coupon_value }}
            </span>
          </div>

          <!-- Pulsante Amazon -->
          <p class="mt-4">
            <a :href="product.affiliate" target="_blank"
              class="flex items-center justify-center text-black bg-[#FF9900] hover:bg-[#FFB74D] focus:ring-4 focus:ring-yellow-300 font-bold rounded-lg text-lg px-6 py-3 transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none shadow-lg w-full md:w-auto">
              Vedi su Amazon.it
            </a>
          </p>

          <!-- Pulsante Alert -->
          <div class="mt-4">
            <button @click="showModal = true"
              class="w-full md:w-auto mt-2 px-6 py-2.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg focus:outline-none focus:ring-4 focus:ring-blue-300">
              Ricevi avvisi prezzo
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modale -->
    <div v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 px-4">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg w-full max-w-md relative">
        <!-- Chiudi -->
        <button @click="showModal = false"
          class="absolute top-3 right-3 text-gray-500 hover:text-gray-800 dark:hover:text-white">
          ✕
        </button>

        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
          Gestione avvisi di prezzo
        </h3>
        <p class="mb-4 text-sm text-gray-500 dark:text-gray-300">
          Inserisci la tua email per ricevere o annullare le notifiche su questo prodotto.
        </p>

        <input v-model="email" type="email" placeholder="Inserisci la tua email"
          class="w-full p-3 mb-4 border border-gray-300 rounded-lg dark:bg-gray-700 dark:text-white" />

        <div class="flex flex-col gap-2 sm:flex-row sm:justify-end">
          <button @click="subscribeToPriceDrop"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
            :disabled="isLoading">
            Iscriviti
          </button>
          <button @click="unsubscribeFromPriceDrop"
            class="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 border border-red-500 rounded-lg"
            :disabled="isLoading">
            Disiscriviti
          </button>
        </div>

        <div class="mt-3">
          <p v-if="successMessage" class="text-green-500">{{ successMessage }}</p>
          <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
          <p v-if="isLoading" class="text-gray-500 text-sm mt-2">Attendere...</p>
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
