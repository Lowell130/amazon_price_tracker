<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
 
 
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">
      
      <div class="bg-white dark:bg-gray-800 relative shadow-md sm:rounded-t-lg overflow-hidden">
        <div class="flex-1 flex items-center space-x-2">
                    
                        <span class="text-gray-500 pl-5 pt-4">Welcome: {{username}} </span>
                      
                    
                   
                </div>

  <div class="flex flex-col md:flex-row items-stretch md:items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">
    
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
  <div class="flex flex-col md:flex-row space-y-3 md:space-y-0 md:space-x-3 w-full md:w-auto">
    <button  @click="addProduct" type="button" class="uppercase text-white bg-[#2557D6] hover:bg-[#2557D6]/90 focus:ring-4 focus:ring-[#2557D6]/50 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#2557D6]/50">
      <svg class="w-10 h-4 me-2 -ms-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 7.757v8.486M7.757 12h8.486M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
</svg>Add Product
</button>


    <!-- <button
      @click="addProduct"
      class="flex-shrink-0 flex items-center justify-center text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-primary-600 dark:hover:bg-primary-700 focus:outline-none dark:focus:ring-primary-800"
    >
      Aggiungi Prodotto
    </button> -->

    <button
      @click="updatePricesManual"
            :disabled="isLoading"
      class="uppercase  hover:bg-red-800  text-white bg-red-600  focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500"
    >  <svg class="w-10 h-4 me-2 -ms-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 11h2v5m-2 0h4m-2.592-8.5h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
</svg>
      update now
    </button>

 
  </div>
</div>


      
    
        <!-- <form @submit.prevent="addProduct" class="product-form">
          <input
            v-model="productUrl"
            placeholder="Inserisci URL prodotto Amazon"
            required
          />
          <button type="submit" class="add-button">Aggiungi Prodotto</button>
        </form> -->
        <div style="text-align: center">
          <!-- <button
            @click="updatePricesManual"
            :disabled="isLoading"
            class="update-button"
          >
            Aggiorna Prezzi Manualmente
          </button> -->
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <div v-if="isLoading" role="status" class="flex items-center justify-center">
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

        </div>
      </div>
    </div>
    <!-- <CombinedPriceChart :products="products" /> -->

    <ProductList :products="products" @remove-product="removeProduct" />
  </section>
</template>

<script>
import ProductList from "../components/ProductList.vue";
// import CombinedPriceChart from '../components/CombinedPriceChart.vue';
import { jwtDecode } from "jwt-decode"; // Importazione specifica
import { fetchWithToken } from "@/api";

export default {
  name: "DashboardPage",
  components: { ProductList },
  data() {
    return {
      productUrl: "",
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
        this.isLoading = true;
        const cleanedUrl = this.cleanAmazonUrl(this.productUrl); // Bonifica il link
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/add-product/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ product_url: cleanedUrl }), // Usa il link bonificato
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        this.productUrl = ""; // Resetta il campo input
        this.errorMessage = "";
        await this.fetchProducts();
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
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
    async removeProduct(asin) {
      const confirmDelete = confirm(
        "Sei sicuro di voler eliminare questo prodotto dal monitoraggio?"
      );
      if (!confirmDelete) return;

      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/remove-product/${asin}`,
          {
            method: "DELETE",
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        await this.fetchProducts();
      } catch (error) {
        console.error("Errore durante l'eliminazione del prodotto:", error);
      }
    },
  },
};
</script>

<!-- <style scoped>
/* Stile della dashboard */
.dashboard {
  max-width: 100%;
  margin: auto;
  /* padding: 20px; */
}

.product-form {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  width: 60%;
}

.add-button, .update-button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-button {
  background-color: #4caf50;
  color: white;
}

.add-button:hover {
  background-color: #45a049;
}

.update-button {
  background-color: #2196f3;
  color: white;
  margin-top: 10px;
}

.update-button:hover {
  background-color: #1976d2;
}

.update-button:disabled {
  background-color: #b3e5fc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  font-weight: bold;
}

.loading-message {
  color: blue;
  font-weight: bold;
}
</style> -->
