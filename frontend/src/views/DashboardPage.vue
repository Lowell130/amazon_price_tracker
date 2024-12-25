<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">
      <div
        class="bg-white dark:bg-gray-800 relative shadow-md rounded-t-lg overflow-hidden"
      >
        <div class="flex-1 flex items-center space-x-2">
          <span class="pl-5 pt-4 text-sm text-gray-900 dark:text-white">Welcome: <span class="font-bold">{{ username }}</span></span>
        </div>

        <div
          class="flex flex-col md:flex-row items-stretch md:items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4"
        >
          <!-- Dropdown categoria -->
          <div class="">
            <select
              v-model="selectedCategory"
              class="block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg p-2 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
              required
            >
              <option value="" disabled>Select a category</option>
              <option
                v-for="category in categories"
                :key="category"
                :value="category"
              >
                {{ category }}
              </option>
            </select>
          </div>

          <!-- Campo di input fluido -->
          <div class="flex-grow">
            <input
              v-model="productUrl"
              type="text"
              id="simple-search"
              placeholder="Amazon product URL"
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              required
            />
          </div>

          <!-- Pulsanti -->
          <div
            class="flex flex-col md:flex-row space-y-3 md:space-y-0 md:space-x-3 w-full md:w-auto"
          >
            <button
              @click="addProduct"
              type="button"
              class="uppercase text-white bg-[#2557D6] hover:bg-[#2557D6]/90 focus:ring-4 focus:ring-[#2557D6]/50 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#2557D6]/50"
            >
              Add Product
            </button>

            <button
  @click="openConfirmModal"
  :disabled="isLoading"
  class="uppercase hover:bg-red-800 text-white bg-red-600 focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500"
>
  update all
</button>
          </div>
        </div>

        <!-- <div>       
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <div
            v-if="isLoading"
            role="status"
            class="flex items-center justify-center mb-4"
          >
            <svg
              aria-hidden="true"
              class="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-red-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="currentColor"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="currentFill"
              />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        </div> -->
      </div>
      <!-- Modale per lo stato di aggiornamento -->
      <UpdateProd :isVisible="isLoading" :message="modalMessage" />
    </div>
    <!-- <CombinedPriceChart :products="products" /> -->

    <ProductList :products="products" @refresh-products="fetchProducts" />
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
  <div class="relative bg-white rounded-lg shadow dark:bg-gray-700 w-11/12 max-w-md p-6">
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
import { jwtDecode } from "jwt-decode"; // Importazione specifica
import { fetchWithToken } from "@/api";

export default {
  name: "DashboardPage",
  components: { ProductList, UpdateProd },
  data() {
    return {
      showConfirmModal: false, // Stato della visibilità della modale di conferma
      modalMessage: "", // Messaggio dinamico della modale
      productUrl: "",
      selectedCategory: "", // Nuova variabile per la categoria selezionata
      showModal: false, // Stato della visibilità della modale
      categories: [
        "Automotive",
        "Baby Products",
        "Beauty & Personal Care",
        "Books",
        "DIY",
        "Electronics",
        "Fashion",
        "Garden",
        "Groceries",
        "Health & Wellness",
        "Home",
        "Kitchen",
        "Monitor",
        "Office Supplies",
        "Pets",
        "Smart-TV",
        "Smartphones",
        "Smartwatches",
        "Sports",
        "Tablet",
        "Technology",
        "Toys & Games",
        "Travel Gear",
      ], // Lista categorie
      products: [],
      username: "",
      errorMessage: "",
      isLoading: false,
      
    };
  },
  async created() {
    this.getUsername();
    await this.fetchProducts();
  },
  methods: {
    getUsername() {
      const token = localStorage.getItem("token");
      if (token) {
        const decodedToken = jwtDecode(token);
        this.username = decodedToken.sub;
      }
    },
    // Funzione per bonificare il link Amazon
    cleanAmazonUrl(url) {
      // Rimuovi i backslash di escape davanti a '/'
      const match = url.match(
        /(https:\/\/www\.amazon\.[a-z.]+\/[^/]+\/dp\/[A-Z0-9]+)/
      );
      return match ? match[0] : url;
    },

    async addProduct() {
  try {
    if (!this.selectedCategory) {
      this.showModal = true;
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
      throw new Error(errorData.detail);
    }

    const data = await response.json();
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

