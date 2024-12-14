<template>
  <div>
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">
      <div class="bg-white dark:bg-gray-800 relative shadow-md overflow-hidden">
        <!-- Spinner -->

        <SpinnerComp v-if="isLoading" />
        <!-- PRODUCTS LIST START -->
        <div v-else class="overflow-x-auto">





          <div class="flex flex-wrap border-b justify-start gap-4 items-center p-4 bg-gray-50 dark:bg-gray-700">
  <!-- Search Product -->
  <div class="mb-2 sm:mb-0 w-full sm:w-auto">
    <input
      v-model="filters.searchQuery"
      @input="applyFilters"
      type="text"
      placeholder="Search product"
      class="block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg p-2 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
    />
  </div>

  <!-- Filter by Category -->
  <div class="mb-2 sm:mb-0 w-full sm:w-auto">
    <select
      v-model="filters.selectedCategory"
      @change="applyFilters"
      class="block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg p-2 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
    >
      <option value="">All Categories</option>
      <option v-for="category in uniqueCategories" :key="category" :value="category">
        {{ category }}
      </option>
    </select>
  </div>

  <!-- Filter by Price Range -->
  <div class="mb-2 sm:mb-0 w-full sm:w-auto">
    <select
      v-model="filters.selectedPriceRange"
      @change="applyFilters"
      class="block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg p-2 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
    >
      <option value="">All Price Ranges</option>
      <option v-for="range in priceRanges" :key="range.label" :value="range.value">
        {{ range.label }}
      </option>
    </select>
  </div>

  <!-- Clear Filters Button -->
  <div class="mb-2 sm:mb-0 w-full sm:w-auto">
    <button
      @click="clearFilters"
      class="block w-full text-sm text-white bg-red-500 hover:bg-red-600 border border-red-600 rounded-lg p-2 dark:bg-red-600 dark:hover:bg-red-700"
    >
      Clear Filters
    </button>
  </div>
</div>

















          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
            >
              <tr>
     
                <th scope="col" class="p-4">
                  <button
                    @click="updateSelectedPrices"
                    class="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700"
                  >
                    <svg
                      class="w-4 h-4 text-white dark:text-white"
                      aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke="currentColor"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M17.651 7.65a7.131 7.131 0 0 0-12.68 3.15M18.001 4v4h-4m-7.652 8.35a7.13 7.13 0 0 0 12.68-3.15M6 20v-4h4"
                      />
                    </svg>
                    <!-- ({{ selectedAsins.length }}) -->
                  </button>
                </th>
                <th scope="col" class="p-4">Product</th>
   
                <th scope="col" class="p-4">
      <span class="flex items-center" @click="sort('category')">
        Category
        <svg class="w-4 h-4 ms-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m8 15 4 4 4-4m0-6-4-4-4 4"/>
                    </svg>
      </span>
    </th>
   
    <th scope="col" class="p-4">
      <span class="flex items-center" @click="sort('price')">
        Current price
        <svg class="w-4 h-4 ms-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m8 15 4 4 4-4m0-6-4-4-4 4"/>
                    </svg>
      </span>
    </th>
    <th scope="col" class="p-4">Diff</th>
                <th scope="col" class="p-4">Max price</th>
                <th scope="col" class="p-4">asin</th>
                <th scope="col" class="p-4">&nbsp;</th>
              
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
                      class="relative w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-red-300 dark:peer-focus:ring-red-800 dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-red-600"
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
                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <span
                    class="bg-primary-100 text-primary-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-primary-900 dark:text-primary-300"
                    v-if="product.category"
                    >{{ product.category }}</span
                  >

                  <span v-else>-</span>
                </td>


                <td v-if="product.availability !== 'Non disponibile' && product.price && product.price !== 'null'" class="px-4 py-3 font-medium">
  <span>{{ product.price }}</span>
</td>
<td v-else class="px-4 py-3 font-medium">
  <span class="flex items-center text-gray-500">
    <div class="inline-block w-4 h-4 mr-2 bg-red-700 rounded-full"></div>
  </span>
</td>
       
<td class="px-4 py-3 font-medium">
  <span v-html="calculatePriceDiff(product)"></span>
</td>
                <td v-if="product.max_price"
                  class="px-4 py-3 font-medium"
                >
                  <span>{{ product.max_price }}</span>
                </td>
                <td v-else
                  class="px-4 py-3 font-medium"
                >
                  <span>-</span>
                </td>
                <td
                  class="px-4 py-3 font-medium"
                >
                  <span class="text-gray-500 dark:text-gray-400">{{
                    product.asin
                  }}</span>
                </td>
                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <div class="flex items-center space-x-4">
                    <a
                      :href="product.product_url"
                      target="_blank"
                      type="button"
                      class="text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-400 dark:text-white"
                    >
                      <svg
                        class="w-6 h-6 text-gray-400"
                        aria-hidden="true"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke="currentColor"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M13.213 9.787a3.391 3.391 0 0 0-4.795 0l-3.425 3.426a3.39 3.39 0 0 0 4.795 4.794l.321-.304m-.321-4.49a3.39 3.39 0 0 0 4.795 0l3.424-3.426a3.39 3.39 0 0 0-4.794-4.795l-1.028.961"
                        />
                      </svg>
                    </a>
                    <a
                      href="#"
                      @click="viewPriceHistory(product.asin)"
                      type="button"
                      class="text-xs font-medium px-2 py-0.5 rounded dark:bg-green-500 dark:text-white"
                    >
                      <svg
                        class="w-6 h-6 text-gray-400"
                        aria-hidden="true"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke="currentColor"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M4 4v15a1 1 0 0 0 1 1h15M8 16l2.5-5.5 3 3L17.273 7 20 9.667"
                        />
                      </svg>
                    </a>

                    <a
                      href="#"
                      type="button"
                      @click="removeProduct(product.asin)"
                      class="text-xs font-medium px-2 py-0.5 rounded dark:bg-red-600 dark:text-white"
                      ><svg
                        class="w-6 h-6 text-gray-400"
                        aria-hidden="true"
                        xmlns="http://www.w3.org/2000/svg"
                        width="24"
                        height="24"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke="currentColor"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z"
                        />
                      </svg>
                    </a>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
       
        
        </div>
        <nav
  class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4"
  aria-label="Table navigation"
>
  <span
    class="text-sm font-normal text-gray-500 dark:text-gray-400 mb-4 md:mb-0 block w-full md:inline md:w-auto"
  >
    Showing
    <span class="font-semibold text-gray-900 dark:text-white">{{ startIndex + 1 }}</span>
    -
    <span class="font-semibold text-gray-900 dark:text-white">{{ endIndex }}</span>
    of
    <span class="font-semibold text-gray-900 dark:text-white">{{ products.length }}</span>
  </span>
  <ul class="inline-flex -space-x-px rtl:space-x-reverse text-sm h-8">
    <!-- Previous Button -->
    <li>
      <button
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
        class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
      >
        Previous
      </button>
    </li>

    <!-- Page Numbers -->
    <li
      v-for="page in totalPages"
      :key="page"
    >
      <button
        @click="changePage(page)"
        :class="{
          'flex items-center justify-center px-3 h-8 leading-tight': true,
          'text-blue-600 border border-gray-300 bg-blue-50 hover:bg-blue-100 dark:border-gray-700 dark:bg-gray-700 dark:text-white': currentPage === page,
          'text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white': currentPage !== page,
        }"
      >
        {{ page }}
      </button>
    </li>

    <!-- Next Button -->
    <li>
      <button
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
        class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
      >
        Next
      </button>
    </li>
  </ul>
</nav>
      </div>
    </div>
  </div>
</template>

<script>
// import PriceHistory from "./PriceHistory.vue";
import { fetchWithToken } from "@/api";
import SpinnerComp from "./SpinnerComp.vue";


export default {
  components: { SpinnerComp },
  props: ["products"],
  data() {
    return {
      localProducts: [], // Copia dei prodotti per il componente
      filteredProducts: [], // Prodotti filtrati
      selectedAsins: [],
      isLoading: false,
      currentPage: 1,
      itemsPerPage: 20,
      sortBy: null,
      sortDirection: "asc",
      filters: {
        searchQuery: "",
        selectedCategory: "",
        selectedPriceRange: "",
      },
      priceRanges: [
        { label: "€0 - €10", value: [0, 10] },
        { label: "€10 - €50", value: [10, 50] },
        { label: "€50 - €100", value: [50, 100] },
        { label: "€100+", value: [100, Infinity] },
      ],
    }
  },


  watch: {
  products: {
    immediate: true,
    handler(newProducts) {
      this.localProducts = [...newProducts]; // Crea una copia dei prodotti
      this.filteredProducts = [...newProducts];
      this.isLoading = newProducts.length === 0;
    },
  },
},


computed: {
    uniqueCategories() {
      return [...new Set(this.products.map((product) => product.category))];
    },
    totalPages() {
      return Math.ceil(this.filteredProducts.length / this.itemsPerPage);
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredProducts.slice(start, end);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage;
    },
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage, this.filteredProducts.length);
    },
  },


  methods: {
    calculatePriceDiff(product) {
  const history = product.price_history;
  if (!history || history.length < 2) {
    return "="; // Non c'è abbastanza cronologia per calcolare la differenza
  }

  const lastPrice = history[history.length - 1].price; // Prezzo attuale
  const previousPrice = history[history.length - 2].price; // Prezzo precedente

  if (lastPrice === previousPrice) {
    return `<span><svg class="w-5 h-5 text-gray-300 dark:text-gray-200" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 20V10m0 10-3-3m3 3 3-3m5-13v10m0-10 3 3m-3-3-3 3"/>
</svg>
</span>`; // Prezzo invariato
  }

  const diffPercentage = ((lastPrice - previousPrice) / previousPrice) * 100;

  if (diffPercentage > 0) {
    return `<span class="text-red-500 flex">+${diffPercentage.toFixed(2)}% <svg class="w-5 h-5 text-red-500 dark:text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v13m0-13 4 4m-4-4-4 4"/>
</svg>
</span>`; // Incremento positivo
  } else {
    return `<span class="text-green-500 flex items-center">
  ${diffPercentage.toFixed(2)}%
  <svg class="w-5 h-5 text-green-500 dark:text-green-500 ml-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19V5m0 14-4-4m4 4 4-4"/>
  </svg>
</span>
`; // Decremento negativo
  }
},


applyFilters() {
    const { searchQuery, selectedCategory, selectedPriceRange } = this.filters;
    this.filteredProducts = this.localProducts.filter((product) => {
      // Filtra per ricerca
      const matchesSearchQuery = product.title
        .toLowerCase()
        .includes(searchQuery.toLowerCase());

      // Filtra per categoria
      const matchesCategory =
        !selectedCategory || product.category === selectedCategory;

      // Filtra per range di prezzo
      const matchesPriceRange =
        !selectedPriceRange ||
        (product.price >= selectedPriceRange[0] &&
          product.price <= selectedPriceRange[1]);

      return matchesSearchQuery && matchesCategory && matchesPriceRange;
    });

    this.currentPage = 1; // Resetta la paginazione quando filtri
  },

  clearFilters() {
    // Resetta i filtri
    this.filters.searchQuery = "";
    this.filters.selectedCategory = "";
    this.filters.selectedPriceRange = "";

    // Ripristina la lista di prodotti
    this.filteredProducts = [...this.localProducts];

    this.currentPage = 1; // Resetta la paginazione
  },

  changePage(page) {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  },

  sort(column) {
    if (this.sortBy === column) {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
    } else {
      this.sortBy = column;
      this.sortDirection = "asc";
    }

    this.filteredProducts.sort((a, b) => {
      let valueA = a[column];
      let valueB = b[column];

      if (typeof valueA === "string") {
        valueA = valueA.toLowerCase();
        valueB = valueB.toLowerCase();
      }

      if (this.sortDirection === "asc") {
        return valueA > valueB ? 1 : valueA < valueB ? -1 : 0;
      } else {
        return valueA < valueB ? 1 : valueA > valueB ? -1 : 0;
      }
    });
  },




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

    viewPriceHistory(asin) {
      this.$router.push(`/products/${asin}`);
    },
    removeProduct(asin) {
      this.$emit("remove-product", asin);
    },
    
  },
  
};
</script>


<style scoped>
nav a, nav button {
    margin-right: 0!important
    
}
</style>