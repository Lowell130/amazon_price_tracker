<template>
  <section class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12 antialiased">
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-8 pt-4">
      <!-- AI Insights Promo Banner -->
      <div class="mb-8 p-6 rounded-3xl bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-xl shadow-blue-500/20 relative overflow-hidden group animate-fadeIn">
        <div class="absolute -top-12 -right-12 w-48 h-48 bg-white/10 rounded-full blur-3xl group-hover:scale-125 transition-transform duration-1000"></div>
        <div class="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
          <div class="flex items-center gap-6">
            <div class="w-16 h-16 rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center text-3xl shadow-inner border border-white/20">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            </div>
            <div>
              <h2 class="text-2xl font-black tracking-tighter mb-1">Analisi Prezzi AI</h2>
              <p class="text-blue-100 font-medium text-sm">Scopri le previsioni di prezzo e ricevi consigli strategici personalizzati.</p>
            </div>
          </div>
          <router-link to="/analysis" class="px-8 py-4 bg-white text-blue-600 font-black rounded-2xl shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all uppercase tracking-widest text-xs">
            Vedi Intuizioni AI
          </router-link>
        </div>
      </div>

      <!-- Welcome & Action Bar -->
      <div class="mb-8 p-6 rounded-3xl border border-white/20 bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl shadow-xl">
        <div class="flex flex-col space-y-4">
          <div class="flex items-center justify-between">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
              <span class="bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 p-2 rounded-xl mr-3">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </span>
              Bentornato, <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 ml-2">{{ username }}</span>
            </h1>
            
            <button
              v-if="isAdmin"
              @click="openConfirmModal"
              :disabled="isLoading"
              class="hidden md:flex items-center px-5 py-2.5 text-sm font-semibold text-white bg-gradient-to-r from-indigo-600 to-blue-600 rounded-2xl hover:shadow-lg hover:scale-105 transition-all duration-300 disabled:opacity-50"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Update all prices
            </button>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-end">
            <!-- Category Select -->
            <div class="lg:col-span-3">
              <label class="block mb-2 text-xs font-bold text-gray-500 uppercase tracking-wider dark:text-gray-400">Categoria</label>
              <select
                v-model="selectedCategory"
                class="block w-full rounded-2xl border-gray-200 bg-white/50 dark:bg-gray-700/50 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 transition-all"
              >
                <option value="" disabled>Seleziona categoria</option>
                <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
              </select>
            </div>

            <!-- URL Input -->
            <div class="lg:col-span-7">
              <label class="block mb-2 text-xs font-bold text-gray-500 uppercase tracking-wider dark:text-gray-400">Link Prodotto Amazon</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
                <input
                  v-model="productUrl"
                  type="text"
                  placeholder="Incolla l'URL del prodotto qui..."
                  class="block w-full pl-12 rounded-2xl border-gray-200 bg-white/50 dark:bg-gray-700/50 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-blue-500 transition-all"
                  required
                />
              </div>
            </div>

            <!-- Add Button -->
            <div class="lg:col-span-2">
              <button
                @click="addProduct"
                type="button"
                class="w-full flex items-center justify-center h-[42px] px-6 py-2 text-sm font-bold text-white bg-blue-600 border border-transparent rounded-2xl shadow-md hover:bg-blue-700 hover:shadow-lg transition-all duration-300 transform active:scale-95"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                Aggiungi
              </button>
            </div>
          </div>
        </div>
      </div>
      <!-- Modale per lo stato di aggiornamento -->
      <UpdateProd :isVisible="isLoading" :message="modalMessage" />
    </div>
    <!-- <CombinedPriceChart :products="products" /> -->

    <ProductList
      :products="products"
      :categories="categories"
      @refresh-products="fetchProducts"
    />

    <!-- Modale -->
    <div
      v-if="showModal"
      id="popup-modal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div
        class="relative bg-white rounded-lg shadow dark:bg-gray-700 w-11/12 max-w-md p-6"
      >
        <button
          @click="closeModal"
          class="absolute top-3 right-3 text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8"
        >
          <svg
            class="w-4 h-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        <div class="text-center">
          <svg
            class="mx-auto mb-4 text-gray-400 w-12 h-12"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 16h-1v-4h-1m-1-4h4m1 5a7.5 7.5 0 11-15 0 7.5 7.5 0 0115 0z"
            />
          </svg>
          <h3 class="mb-5 text-lg font-medium text-gray-700">
            Seleziona una categoria prima di aggiungere un prodotto.
          </h3>
          <button
            @click="closeModal"
            class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-800"
          >
            Ok
          </button>
        </div>
      </div>
    </div>
    <!-- EndModale -->
    <!-- Modale update all -->
    <!-- Modale di conferma per Update All -->
    <div
      v-if="showConfirmModal"
      class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
    >
      <div
        class="relative bg-white rounded-lg shadow dark:bg-gray-700 w-11/12 max-w-md p-6"
      >
        <button
          @click="closeConfirmModal"
          class="absolute top-3 right-3 text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-4 h-4"
        >
          <svg
            class="w-4 h-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
        <div class="text-center">
          <h3 class="mb-5 text-lg font-medium text-gray-700">
            Are you sure you want to update all prices?
          </h3>
          <div class="flex justify-center space-x-4">
            <button
              @click="confirmUpdateAll"
              class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-800"
            >
              Yes
            </button>
            <button
              @click="closeConfirmModal"
              class="px-4 py-2 text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- end modale update all -->
  </section>
</template>

<script>
import ProductList from "../components/ProductList.vue";
import UpdateProd from "../components/UpdateProd.vue";
// import CombinedPriceChart from '../components/CombinedPriceChart.vue';
// import { jwtDecode } from "jwt-decode"; // Importazione specifica
import { fetchWithToken } from "@/api";
import { useToast } from '@/store/toast';

export default {
  name: "DashboardPage",
  components: { ProductList, UpdateProd },
  setup() {
    const toast = useToast();
    return { toast };
  },
  data() {
    return {
      showConfirmModal: false, // Stato della visibilità della modale di conferma
      modalMessage: "", // Messaggio dinamico della modale
      productUrl: "",
      selectedCategory: "", // Nuova variabile per la categoria selezionata
      showModal: false, // Stato della visibilità della modale
      categories: [
       "Audio", "Automotive", "Baby Products", "Beauty Care", "Books", "Console", "DIY", "Electronics", "Fashion", "Gaming", "Garden", "Groceries", "Health & Wellness", "Home", "Kitchen", "Memory", "Monitor", "Notebook", "Office Supplies", "PC", "Pets", "Smart-TV", "Smartphones", "Smartwatches", "Sports", "Tablet", "Technology", "Toys & Games", "Travel Gear", "Video", "Watch", "WiFi"

      ], // Lista categorie
      products: [],
      username: "",
      errorMessage: "",
      isLoading: false,
      isAdmin: false, // Stato per controllare se l'utente è admin
    };
  },
  async created() {
    this.getUsername();
    await this.fetchProducts();
  },
  methods: {
    async getUsername() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/auth/users/me`,
          { method: "GET" }
        );

        if (!response.ok) {
          throw new Error("Errore nel recupero delle informazioni utente");
        }

        const userData = await response.json();
        console.log("User data:", userData); // Debug

        this.username = userData.username;
        this.isAdmin = userData.admin;
        console.log("Is Admin in Dashboard:", this.isAdmin); // Debug

        this.$forceUpdate(); // Forza l'aggiornamento della UI
      } catch (error) {
        console.error(
          "Errore nel caricamento delle informazioni utente:",
          error
        );
        this.$router.push("/login");
      }
    },

    // Funzione per bonificare il link Amazon
    cleanAmazonUrl(url) {
      // Regex più robusta per catturare l'URL fino all'ASIN
      // Supporta /dp/ e /gp/product/
      // Supporta con o senza slug (titolo)
      // Supporta http e https, con o senza www
      const match = url.match(
        /(https?:\/\/(?:www\.)?amazon\.[a-z.]+(?:\/.*)?\/(?:dp|gp\/product)\/[A-Z0-9]{10})/
      );
      return match ? match[0] : url;
    },

    async addProduct() {
      try {
        if (!this.selectedCategory) {
          this.toast.warning("Seleziona una categoria prima di aggiungere un prodotto.");
          return;
        }

        this.modalMessage = "Adding product...";
        this.isLoading = true;

        const cleanedUrl = this.cleanAmazonUrl(this.productUrl);
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/add-product/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              product_url: cleanedUrl,
              category: this.selectedCategory,
            }),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          if (errorData.detail === "Product already being tracked") {
            this.toast.warning("Questo prodotto è già tracciato!");
          } else {
            this.toast.error(errorData.detail || "Errore durante l'aggiunta del prodotto.");
          }
          throw new Error(errorData.detail);
        }

        const data = await response.json();
        this.toast.success("Prodotto aggiunto con successo!");
        console.log("Affiliate link generated:", data.affiliate); // Verifica il link affiliato

        this.productUrl = "";
        this.selectedCategory = "";
        await this.fetchProducts();
      } catch (error) {
        console.error(error.message);
      } finally {
        this.isLoading = false;
        this.modalMessage = ""; // Reset del messaggio della modale
      }
    },

    async fetchProducts() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/dashboard`
        );
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }
        const data = await response.json();
        this.products = data.products;
      } catch (error) {
        console.error("Errore nel caricamento dei prodotti:", error);
      }
    },
    async updatePricesManual() {
      try {
        this.modalMessage = "Update product please wait...";
        this.isLoading = true;
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/update-prices-manual/`,
          {
            method: "POST",
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        await this.fetchProducts();
      } catch (error) {
        this.errorMessage = "Errore durante l'aggiornamento manuale dei prezzi";
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },

    closeModal() {
      this.showModal = false; // Nasconde la modale
    },
    openConfirmModal() {
      this.showConfirmModal = true;
    },
    closeConfirmModal() {
      this.showConfirmModal = false;
    },
    async confirmUpdateAll() {
      this.closeConfirmModal();
      await this.updatePricesManual(); // Chiama la funzione originale per aggiornare i prezzi
    },
  },
};
</script>

