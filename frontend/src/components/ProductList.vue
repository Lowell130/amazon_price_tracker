<template>
  <div>
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">


      <div class="bg-white dark:bg-gray-800 relative shadow-md overflow-hidden flex flex-wrap border-b dark:border-gray-600 justify-start gap-4 items-center p-4 bg-gray-50 dark:bg-gray-700">
  <!-- Search Product -->
  <div class="mb-2 sm:mb-0 w-full sm:w-auto">
    <div class="relative">
      <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/>
            </svg>
        </div>
    <input
      v-model="filters.searchQuery"
      @input="applyFilters"
      type="text"
      placeholder="Search product"
      class="lock w-full ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    />
  </div>
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

  <!-- filtro stato -->
<div class="mb-2 sm:mb-0 w-full sm:w-auto">
  <select
  v-model="filters.selectedCondition"
  @change="applyFilters"
  class="block w-full text-sm text-gray-900 bg-gray-50 border border-gray-300 rounded-lg p-2 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
>
  <option value="">All Conditions</option>
  <option value="Nuovo">New</option>
  <option value="Usato">Used</option>
  <option value="Non disponibile">Unavailable</option>
</select>
</div>

   <!-- show favorite -->
   <div class="mb-2 sm:mb-0 w-full sm:w-auto">
  <button
    @click="filterFavorites"
    class="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2 text-center dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
  >
    Show Favorites
  </button>
</div>



  <!-- Clear Filters Button -->
  <div class="mb-2 sm:mb-0 w-full sm:w-auto">
    <button
      @click="clearFilters"
      class="text-green-700 hover:text-white border border-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2 text-center me-2 dark:border-green-500 dark:text-green-500 dark:hover:text-white dark:hover:bg-green-600 dark:focus:ring-green-800"
    >
      Clear Filters
    </button>
  </div>

 

</div>




      <div class="bg-white dark:bg-gray-800 relative shadow-md overflow-hidden rounded-b-lg">
        <!-- Spinner -->

        <SpinnerComp v-if="isLoading" />
        <!-- PRODUCTS LIST START -->
        <div v-else class="overflow-x-auto">


















          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400"
          >
            <thead
              class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400"
            >
              <tr>
     
                <th scope="col" class="p-4">
                  <button
  @click="deleteSelectedProducts"
  class="flex bg-red-600 text-white p-2 rounded hover:bg-red-700"
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
      d="M5 7h14m-9 3v8m4-8v8M10 3h4a1 1 0 0 1 1 1v3H9V4a1 1 0 0 1 1-1ZM6 7h12v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7Z"
    />
  </svg>
  {{ selectedAsins.length }}
</button>

                </th>
                <th scope="col" class="p-4">Product</th>
                <th scope="col" class="p-4">Condition</th>
                <th scope="col" class="p-4">Rating</th>
                <th scope="col" class="p-4">Alert</th>
   
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
        Current
        <svg class="w-4 h-4 ms-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m8 15 4 4 4-4m0-6-4-4-4 4"/>
                    </svg>
      </span>
    </th>
    <th scope="col" class="p-4">Diff</th>
                <th scope="col" class="p-4">Max price</th>
                <!-- <th scope="col" class="p-4">asin</th> -->
                <th scope="col" class="p-4">&nbsp;</th>
                <th scope="col" class="p-4">&nbsp;</th>
              
              </tr>
            </thead>
            <tbody v-for="product in paginatedProducts" :key="product.asin">

              <tr
                class="border-b border-t dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
             
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
                      {{ product.title.substring(0, 20)
                      }}{{ product.title.length > 20 ? "..." : "" }} <span class="text-xs text-gray-400 dark:text-white">{{ product.asin }}</span>
                    </span>
                  </div>
                </th>

                <td
  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
>
  <span
    class="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300"
    v-if="product.rating"
    >{{ product.rating }}</span
  >

  <span v-else>-</span>
</td>

  

                <td class="px-4 py-3 font-medium">
  <span
    v-if="product.condition === 'Nuovo'"
    class="bg-green-100 text-green-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-green-900 dark:text-green-300"
  >
    New
  </span>
  <span
    v-else-if="product.condition === 'Usato'"
    class="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300"
  >
    Used
  </span>
  <span
    v-else
    class="bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-red-900 dark:text-red-300"
  >
    Unavailable
  </span>
</td>

                <td class="px-4 py-3 font-medium">
  <!-- Cuore cliccabile -->
  <span class="flex items-center text-gray-500 cursor-pointer" @click="toggleFavorite(product)">
    <svg v-if="product.is_favorite"
      class="w-6 h-6 text-red-500 dark:text-red-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 24 24">
  <path d="M11.209 3.816a1 1 0 0 0-1.966.368l.325 1.74a5.338 5.338 0 0 0-2.8 5.762l.276 1.473.055.296c.258 1.374-.228 2.262-.63 2.998-.285.52-.527.964-.437 1.449.11.586.22 1.173.75 1.074l12.7-2.377c.528-.1.418-.685.308-1.27-.103-.564-.636-1.123-1.195-1.711-.606-.636-1.243-1.306-1.404-2.051-.233-1.085-.275-1.387-.303-1.587-.009-.063-.016-.117-.028-.182a5.338 5.338 0 0 0-5.353-4.39l-.298-1.592Z"/>
  <path fill-rule="evenodd" d="M6.539 4.278a1 1 0 0 1 .07 1.412c-1.115 1.23-1.705 2.605-1.83 4.26a1 1 0 0 1-1.995-.15c.16-2.099.929-3.893 2.342-5.453a1 1 0 0 1 1.413-.069Z" clip-rule="evenodd"/>
  <path d="M8.95 19.7c.7.8 1.7 1.3 2.8 1.3 1.6 0 2.9-1.1 3.3-2.5l-6.1 1.2Z"/>
</svg>
<svg v-else
      class="w-6 h-6 text-gray-300 dark:text-white"
 aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m10.827 5.465-.435-2.324m.435 2.324a5.338 5.338 0 0 1 6.033 4.333l.331 1.769c.44 2.345 2.383 2.588 2.6 3.761.11.586.22 1.171-.31 1.271l-12.7 2.377c-.529.099-.639-.488-.749-1.074C5.813 16.73 7.538 15.8 7.1 13.455c-.219-1.169.218 1.162-.33-1.769a5.338 5.338 0 0 1 4.058-6.221Zm-7.046 4.41c.143-1.877.822-3.461 2.086-4.856m2.646 13.633a3.472 3.472 0 0 0 6.728-.777l.09-.5-6.818 1.277Z"/>
</svg>
  </span>
</td>




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

                <td class="px-4 py-3 font-medium">
  <span v-if="product.price !== null">{{ product.price }}</span>
  <span v-else class="text-red-500">Unavailable</span>
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
                <!-- <td
                  class="px-4 py-3 font-medium"
                >
                  <span class="text-gray-500 dark:text-gray-400">{{
                    product.asin
                  }}</span>
                </td> -->





  <!-- Pulsante per l'accordion -->
 <!-- Accordion Toggle Button -->
 <td class="px-4 py-3">
                  <button
                    @click="toggleAccordion(product.asin)"
                    class="flex items-center text-xs font-medium px-2 py-0.5 rounded dark:text-white"
                  >
                    <svg
                      :class="{ 'rotate-180': currentOpenAccordion === product.asin }"
                      class="w-5 h-5 transition-transform"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </button>
                </td>


                <td
                  class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                >
                  <div class="flex items-center space-x-4">
                    <a
                      :href="product.affiliate"
                      target="_blank"
                      type="button"
                      class="text-xs font-medium px-2 py-0.5 rounded dark:text-white"
                    >
                      <svg
                        class="w-6 h-6 text-orange-400 hover:text-orange-700"
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
                      class="text-xs font-medium px-2 py-0.5 rounded dark:text-white"
                    >
                    <svg class="w-6 h-6 text-blue-400 hover:text-blue-600 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 11h2v5m-2 0h4m-2.592-8.5h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>
</svg>

                    </a>



                    <a
  href="#"
  @click.prevent="updateProductPrice(product)"
  class="text-xs font-medium px-2 py-0.5 rounded dark:text-white"
>
  <svg
    :class="{ 'animate-spin': loadingProducts[product.asin] }"
    class="w-6 h-6 text-green-400 hover:text-green-600"
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
</a>




                  </div>
                </td>

  
   
    </tr>
    <!-- Riga dell'accordion -->
   <!-- Accordion Content Row -->
   <tr v-if="currentOpenAccordion === product.asin">
                <td colspan="12" class="p-5">
                  <p class="p-4">{{ product.title }}</p>
                  <ChartPage v-if="product && product.price_history" :priceHistory="product.price_history" />
                </td>
              </tr>
            </tbody>
          </table>
       
        
        </div>
        <nav class="flex items-center flex-column flex-wrap md:flex-row justify-between pt-4 text-xs bg-gray-50 dark:bg-gray-700 rounded-b-lg">
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
      class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
    >
      Previous
    </button>
  </li>

  <!-- Dynamic Page Numbers -->
  <li v-for="page in visiblePages" :key="page">
    <button
      @click="changePage(page)"
      :class="{
        'flex items-center justify-center px-3 h-8 leading-tight': true,
        'text-blue-600 border border-gray-300 bg-blue-50 hover:bg-blue-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white': currentPage === page,
        'text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white': currentPage !== page,
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
      class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
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
import ChartPage from "../components/ChartPage.vue";


export default {
  components: { SpinnerComp, ChartPage },
  props: ["products"],
  data() {
    return {
      localProducts: [], // Copia dei prodotti per il componente
      filteredProducts: [], // Prodotti filtrati
      selectedAsins: [],
      loadingProducts: {}, // Stato di caricamento per i singoli prodotti
      currentOpenAccordion: null, // Tracks the currently open accordion
      isLoading: false,
      currentPage: 1,
      itemsPerPage: 30,
      sortBy: null,
      sortDirection: "asc",
      filters: {
        searchQuery: "",
        selectedCategory: "",
        selectedPriceRange: "",
        selectedCondition: "", // Aggiunto valore predefinito corretto
      },
      priceRanges: [
        { label: "€0 - €10", value: [0, 10] },
        { label: "€10 - €50", value: [10, 50] },
        { label: "€50 - €100", value: [50, 100] },
        { label: "€100 - €300", value: [100, 300] },
        { label: "€300 - €600", value: [300, 600] },
        { label: "€600 - €1000", value: [600, 1000] },
        { label: "€1200+", value: [1200, Infinity] },
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
  visiblePages() {
    const pages = [];
    const maxVisible = 5; // Numero massimo di pagine visibili
    const total = this.totalPages;

    if (total <= maxVisible) {
      for (let i = 1; i <= total; i++) {
        pages.push(i);
      }
    } else {
      const half = Math.floor(maxVisible / 2);
      let start = Math.max(this.currentPage - half, 1);
      let end = Math.min(start + maxVisible - 1, total);

      if (end - start + 1 < maxVisible) {
        start = Math.max(end - maxVisible + 1, 1);
      }

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (start > 1) pages.unshift("...");
      if (end < total) pages.push("...");
    }

    return pages;
  },
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
    changePage(page) {
    if (page === '...') return; // Non fare nulla se cliccato su '...'

    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  },

    async deleteSelectedProducts() {
  if (this.selectedAsins.length === 0) {
    alert("Select at least one product to delete.");
    return;
  }

  const confirmDelete = confirm(
    "Are you sure you want to delete the selected products?"
  );
  if (!confirmDelete) return;

  try {
    const response = await fetchWithToken(
      `${process.env.VUE_APP_API_BASE_URL}/remove-products/`,
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
    alert(`Deleted products: ${data.removed_asins.join(", ")}`);

    // Aggiorna la lista localmente
    this.localProducts = this.localProducts.filter(
      (product) => !this.selectedAsins.includes(product.asin)
    );
    this.applyFilters();
    this.selectedAsins = []; // Deselect all
  } catch (error) {
    console.error("Error deleting selected products:", error);
  }
},


    toggleAccordion(asin) {
      if (this.currentOpenAccordion === asin) {
        this.currentOpenAccordion = null;
      } else {
        this.currentOpenAccordion = asin;
      }
    },



    async toggleFavorite(product) {
    try {
      // Chiamata API per aggiornare lo stato del preferito
      const response = await fetchWithToken(
        `${process.env.VUE_APP_API_BASE_URL}/favorite/${product.asin}`,
        {
          method: "PATCH",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      const data = await response.json();
      // Aggiorna lo stato del prodotto nel frontend
      product.is_favorite = data.is_favorite;
    } catch (error) {
      console.error("Errore durante l'aggiornamento del preferito:", error);
    }
  },
  filterFavorites() {
    this.filteredProducts = this.localProducts.filter((product) => product.is_favorite);
    this.currentPage = 1; // Reset paginazione
  },
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
  const { searchQuery, selectedCategory, selectedPriceRange, selectedCondition } = this.filters;

  this.filteredProducts = this.localProducts.filter((product) => {
    // Filtra per ricerca
    const matchesSearchQuery =  product.title.toLowerCase().includes(searchQuery.toLowerCase()) || product.asin.toLowerCase().includes(searchQuery.toLowerCase());

    // Filtra per categoria
    const matchesCategory = !selectedCategory || product.category === selectedCategory;

    // Filtra per range di prezzo
    const matchesPriceRange = !selectedPriceRange ||
      (product.price >= selectedPriceRange[0] && product.price <= selectedPriceRange[1]);

    // Filtra per condizione
    const matchesCondition = !selectedCondition || product.condition === selectedCondition;

    return matchesSearchQuery && matchesCategory && matchesPriceRange && matchesCondition;
  });

  this.currentPage = 1; // Resetta la paginazione quando filtri
},

  clearFilters() {
    // Resetta i filtri
    this.filters.searchQuery = "";
    this.filters.selectedCategory = "";
    this.filters.selectedPriceRange = "";
    this.filters.selectedCondition = ""; // Ripristina la condizione

    // Ripristina la lista di prodotti
    this.filteredProducts = [...this.localProducts];

    this.currentPage = 1; // Resetta la paginazione
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

  async updateProductPrice(product) {
  if (this.loadingProducts[product.asin]) return; // Evita aggiornamenti multipli

  const confirmUpdate = confirm(
    `Do you want to manually update the price for ${product.title}?`
  );
  if (!confirmUpdate) return;

  // Imposta lo stato di caricamento
  this.loadingProducts = {
    ...this.loadingProducts,
    [product.asin]: true,
  };

  try {
    const response = await fetchWithToken(
      `${process.env.VUE_APP_API_BASE_URL}/update-product/${product.asin}`,
      {
        method: "POST",
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const data = await response.json();
    alert(`Updated price for ${product.title}: €${data.product.price}`);

    // Aggiorna i dettagli del prodotto direttamente nel frontend
    product.price = data.product.price;
    product.price_history = data.product.price_history;
    product.max_price = data.product.max_price;
    product.min_price = data.product.min_price;
    product.average_price = data.product.average_price;
    product.availability = data.product.availability;
    product.condition = data.product.condition;
  } catch (error) {
    console.error("Error updating product price:", error);
  } finally {
    // Resetta lo stato di caricamento
    this.loadingProducts = {
      ...this.loadingProducts,
      [product.asin]: false,
    };
  }
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

      // Aggiorna localmente la lista dei prodotti
      this.localProducts = this.localProducts.filter(
        (product) => product.asin !== asin
      );

      // Applica i filtri per aggiornare la vista
      this.applyFilters();
    } catch (error) {
      console.error("Errore durante l'eliminazione del prodotto:", error);
    }
  },

    viewPriceHistory(asin) {
      this.$router.push(`/products/${asin}`);
    },
    // removeProduct(asin) {
    //   this.$emit("remove-product", asin);
    // },
    
  },
  
};
</script>


<style scoped>
.paginator-ellipsis {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  font-size: 14px;
  color: gray;
}
nav a, nav button {
    margin-right: 0!important
    
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>