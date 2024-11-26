<template>
  <div>
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">
      <div class="bg-white dark:bg-gray-800 relative shadow-md overflow-hidden">
        <!-- Spinner -->
        <div v-if="isLoading" class="flex justify-center items-center py-8">
          <div role="status">
            <svg
              aria-hidden="true"
              class="inline w-10 h-10 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
              />
            </svg>
            <span class="sr-only">Loading...</span>
          </div>
        </div>

        <!-- PRODUCTS LIST START -->
        <div v-else class="overflow-x-auto">
          <table
            class="w-full text-sm text-left text-gray-500 dark:text-gray-400"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
            >
              <tr>
                <!-- <th scope="col" class="p-4"></th> -->
                <th scope="col" class="p-4">
                  <button
    @click="updateSelectedPrices"
    class="uppercase bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
>
    <svg class="w-4 h-4 text-white dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.651 7.65a7.131 7.131 0 0 0-12.68 3.15M18.001 4v4h-4m-7.652 8.35a7.13 7.13 0 0 0 12.68-3.15M6 20v-4h4"/>
    </svg>
    <!-- ({{ selectedAsins.length }}) -->
</button>

                </th>
                <th scope="col" class="p-4">Product</th>
                <th scope="col" class="p-4">Category</th>
                <th scope="col" class="p-4">Current price</th>
                <!-- <th scope="col" class="p-4">Previous price</th> -->
                <th scope="col" class="p-4">Max price</th>
                <th scope="col" class="p-4">asin</th>
               <th scope="col" class="p-4">&nbsp;</th>
                
                <!-- <th scope="col" class="p-4"></th> -->
              </tr>
            </thead>
            <tbody v-for="product in paginatedProducts" :key="product.asin">
              <tr
                class="border-b dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <!-- <td class="p-4 w-4"></td> -->
                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <label class="inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      v-model="selectedAsins"
                      :value="product.asin"
                      class="sr-only peer"
                    />
                    <div
                      class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"
                    ></div>
                  </label>
                </td>
                <th
                  scope="row"
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <div class="flex items-center">
                    <div
                      class="h-10 w-10 flex-shrink-0 flex items-center justify-center rounded"
                    >
                      <img
                        v-if="product.image_url"
                        :src="product.image_url"
                        :alt="product.title"
                        class="h-full w-full object-contain"
                      />
                    </div>
                    <span class="ml-3 text-right">
                      {{ product.title.substring(0, 30)
                      }}{{ product.title.length > 30 ? "..." : "" }}
                      </span>
                  </div>
                </th>
                <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <span class="bg-primary-100 text-primary-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-primary-900 dark:text-primary-300" v-if="product.category">{{ product.category }}</span>
  
  <span v-else>-</span>
</td>
                <td class="px-4 py-3 font-medium">
                  <strong :class="getCurrentPriceClass(product)">
                    {{ formatPrice(product.price) }}€
                  </strong>
                  <span
                    v-if="getPriceDifference(product) < 0"
                    class="text-green-500"
                  >
                    ({{ getSavingsPercentage(product) }})
                  </span>
                </td>

                

                <!-- <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <strong
                    >{{ formatPrice(getLastMonitoredPrice(product)) }}€</strong
                  >
                </td> -->
                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <strong>{{ formatPrice(getMaxPrice(product)) }}€</strong>
                </td>
                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <span class="text-gray-500 dark:text-gray-400">{{
                    product.asin
                  }}</span>
                </td>
                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >




                 <div class="flex items-center space-x-4">
                    <!-- <a
                      :href="product.product_url"
                      target="_blank"
                      class="uppercase text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50"
                    >
                      Open
                    </a> -->
                    <!-- <button
                      @click="viewPriceHistory(product.asin)"
                      class="uppercase text-gray-900 bg-gray-100 hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500"
                    >
                      History
                    </button> -->
                     <a :href="product.product_url" target="_blank" type="button" class="bg-yellow-400 text-white text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-400 dark:text-white">Open</a>
                   <a href="#" @click="viewPriceHistory(product.asin)" type="button" class="bg-green-500 text-white text-xs font-medium px-2 py-0.5 rounded dark:bg-green-500 dark:text-white">History</a>

                    <a href="#" type="button" @click="removeProduct(product.asin)" class="bg-red-600 text-white text-xs font-medium px-2 py-0.5 rounded dark:bg-red-600 dark:text-white">Remove</a>

                    <!-- <button
                      @click="removeProduct(product.asin)"
                      class="uppercase hover:bg-red-800 text-white bg-red-600 focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500"
                    >
                      Delete
                    </button> -->
                  </div> 




                
                  <!-- <div class="inline-flex flex-col w-full rounded-md shadow-sm md:w-auto md:flex-row" role="group">
          <button type="button"
                  class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-t-lg md:rounded-tr-none md:rounded-l-lg hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-2 focus:ring-primary-700 focus:text-primary-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-primary-500 dark:focus:text-white">
            History
          </button>
          <button type="button"
                  class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border-gray-200 border-x md:border-x-0 md:border-t md:border-b hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-2 focus:ring-primary-700 focus:text-primary-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-primary-500 dark:focus:text-white">
            Link
          </button>
          <button type="button"
                  class="px-4 py-2 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-b-lg md:rounded-bl-none md:rounded-r-lg hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-2 focus:ring-primary-700 focus:text-primary-700 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:hover:text-white dark:hover:bg-gray-600 dark:focus:ring-primary-500 dark:focus:text-white">
            Delete
          </button>
        
        </div>  -->
                
                </td>
               
              </tr>
            </tbody>
          </table>
        </div>

        <!-- FOOTER TAB -->
        <nav
          class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4"
          aria-label="Table navigation"
        >
          <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
            Showing
            <span class="font-semibold text-gray-900 dark:text-white">{{
              (currentPage - 1) * itemsPerPage + 1
            }}</span>
            -
            <span class="font-semibold text-gray-900 dark:text-white">{{
              Math.min(currentPage * itemsPerPage, sortedProducts.length)
            }}</span>
            of
            <span class="font-semibold text-gray-900 dark:text-white">{{
              sortedProducts.length
            }}</span>
          </span>
          <ul class="inline-flex items-stretch -space-x-px">
            <li>
              <button
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="flex items-center justify-center h-full py-1.5 px-3 ml-0 text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
              >
                Previous
              </button>
            </li>
            <li v-for="page in totalPages" :key="page">
              <button
                @click="goToPage(page)"
                :class="{
                  'bg-primary-50 text-primary-600': page === currentPage,
                }"
                class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
              >
                {{ page }}
              </button>
            </li>
            <li>
              <button
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="flex items-center justify-center h-full py-1.5 px-3 leading-tight text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
              >
                Next
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
    <PriceHistory v-if="priceHistory.length" :history="priceHistory" />
  </div>
</template>

<script>
import PriceHistory from "./PriceHistory.vue";
import { fetchWithToken } from "@/api";

export default {
  components: { PriceHistory },
  props: ["products"],
  data() {
    return {
      priceHistory: [],
      selectedAsins: [], // Elenco degli ASIN selezionati
      currentPage: 1,
      itemsPerPage: 40,
      isLoading: false, // Nuova variabile per lo stato di caricamento
    };
  },
  watch: {
    products: {
      immediate: true,
      handler(newProducts) {
        this.isLoading = newProducts.length === 0;
      },
    },
  },
  computed: {
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedProducts.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.sortedProducts.length / this.itemsPerPage);
    },
    sortedProducts() {
      return [...this.products].sort((a, b) => {
        const changeA = Math.abs(
          parseFloat(this.getPriceChangePercentageRaw(a))
        );
        const changeB = Math.abs(
          parseFloat(this.getPriceChangePercentageRaw(b))
        );

        // Ordine decrescente per variazione assoluta
        if (changeA !== changeB) {
          return changeB - changeA;
        }

        // Ordina alfabeticamente se non c'è variazione
        return a.title.localeCompare(b.title);
      });
    },
  },
  methods: {
    async updateSelectedPrices() {
  try {
    if (this.selectedAsins.length === 0) {
      alert("Select at least one product to update.");
      return;
    }

    const response = await fetchWithToken(
      `${process.env.VUE_APP_API_BASE_URL}/update-selected-prices/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.selectedAsins),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const data = await response.json();
    alert(`Updated products: ${data.updated_products.join(", ")}`);

    // Emetti l'evento per informare il genitore di aggiornare i prodotti
    this.$emit("refresh-products");
  } catch (error) {
    console.error("Error updating selected prices:", error);
  }
},


    getPriceChangePercentageRaw(product) {
      const maxPrice = this.getMaxPrice(product);
      const currentPrice = parseFloat(product.price);
      if (maxPrice > 0) {
        return (((currentPrice - maxPrice) / maxPrice) * 100).toFixed(2);
      }
      return "0.00";
    },
    getPriceDifference(product) {
      const currentPrice = parseFloat(product.price);
      const maxPrice = this.getMaxPrice(product);
      return currentPrice - maxPrice;
    },
    getSavingsPercentage(product) {
      const currentPrice = parseFloat(product.price);
      const maxPrice = this.getMaxPrice(product);
      if (maxPrice > 0 && currentPrice < maxPrice) {
        return `-${(((maxPrice - currentPrice) / maxPrice) * 100).toFixed(2)}%`;
      }
      return "0.00%";
    },
    getCurrentPriceClass(product) {
      return this.getPriceDifference(product) < 0
        ? "text-green-500"
        : "text-gray-900";
    },
    getMaxPrice(product) {
      if (product.price_history) {
        return Math.max(
          ...product.price_history.map((entry) => parseFloat(entry.price))
        );
      }
      return parseFloat(product.price);
    },
    getLastMonitoredPrice(product) {
      if (product.price_history && product.price_history.length > 1) {
        return product.price_history[product.price_history.length - 2].price;
      }
      return product.price;
    },
    formatPrice(price) {
      return parseFloat(price).toFixed(2);
    },
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    viewPriceHistory(asin) {
      this.$router.push(`/products/${asin}`);
    },
    removeProduct(asin) {
      this.$emit("remove-product", asin);
    },
  },
};
</script>
