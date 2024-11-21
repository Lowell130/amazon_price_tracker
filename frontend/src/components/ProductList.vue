<template>
  <div>
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">
      <div class="bg-white dark:bg-gray-800 relative shadow-md overflow-hidden">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">
          <!-- Posizione per eventuali filtri o azioni aggiuntive -->
        </div>

        <!-- PRODUCTS LIST START -->
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="p-4"></th>
                <th scope="col" class="p-4">mail</th>
                <th scope="col" class="p-4">Product</th>
                <th scope="col" class="p-4">Current price</th>
                <th scope="col" class="p-4">Previous price</th>
                <th scope="col" class="p-4">Max price</th>
                <th scope="col" class="p-4">asin</th>
                <th scope="col" class="p-4"></th>
              </tr>
            </thead>
            <tbody v-for="product in paginatedProducts" :key="product.asin">
              <tr class="border-b dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700">
                <td class="p-4 w-4"></td>
                <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <label class="inline-flex items-center cursor-pointer">
                    <input type="checkbox" value="" class="sr-only peer" />
                    <div class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </td>
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <div class="flex items-center">
                    <div class="h-10 w-10 flex-shrink-0 flex items-center justify-center rounded">
                      <img v-if="product.image_url" :src="product.image_url" :alt="product.title" class="h-full w-full object-contain" />
                    </div>
                    <span class="ml-3 text-right">{{ product.title.substring(0, 20) }}{{ product.title.length > 20 ? '...' : '' }}</span>
                  </div>
                </th>
                <td class="px-4 py-3 font-medium">
  <strong :class="getCurrentPriceClass(product)">
    {{ formatPrice(product.price) }}€
  </strong>
  <span v-if="getPriceDifference(product) < 0" class="text-green-500">
    ({{ getSavingsPercentage(product) }})
  </span>
</td>

                <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <strong>{{ formatPrice(getLastMonitoredPrice(product)) }}€</strong>
                </td>
                <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <strong>{{ formatPrice(getMaxPrice(product)) }}€</strong>
                </td>
                <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <span class="text-gray-500 dark:text-gray-400">{{ product.asin }}</span>
                </td>
                <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  <div class="flex items-center space-x-4">
                    <a :href="product.product_url" target="_blank" class="uppercase text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50">
                      Open
                    </a>
                    <button @click="viewPriceHistory(product.asin)" class="uppercase text-gray-900 bg-gray-100 hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500">
                      History
                    </button>
                    <button @click="removeProduct(product.asin)" class="uppercase hover:bg-red-800 text-white bg-red-600 focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- FOOTER TAB -->
        <nav class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4" aria-label="Table navigation">
          <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
            Showing
            <span class="font-semibold text-gray-900 dark:text-white">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
            -
            <span class="font-semibold text-gray-900 dark:text-white">{{ Math.min(currentPage * itemsPerPage, sortedProducts.length) }}</span>
            of
            <span class="font-semibold text-gray-900 dark:text-white">{{ sortedProducts.length }}</span>
          </span>
          <ul class="inline-flex items-stretch -space-x-px">
            <li>
              <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1" class="flex items-center justify-center h-full py-1.5 px-3 ml-0 text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                Previous
              </button>
            </li>
            <li v-for="page in totalPages" :key="page">
              <button @click="goToPage(page)" :class="{ 'bg-primary-50 text-primary-600': page === currentPage }" class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                {{ page }}
              </button>
            </li>
            <li>
              <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages" class="flex items-center justify-center h-full py-1.5 px-3 leading-tight text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
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
import PriceHistory from './PriceHistory.vue';

export default {
  components: { PriceHistory },
  props: ['products'],
  data() {
    return {
      priceHistory: [],
      currentPage: 1,
      itemsPerPage: 20,
    };
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
        const changeA = Math.abs(parseFloat(this.getPriceChangePercentageRaw(a)));
        const changeB = Math.abs(parseFloat(this.getPriceChangePercentageRaw(b)));

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
    getPriceChangePercentageRaw(product) {
      const maxPrice = this.getMaxPrice(product);
      const currentPrice = parseFloat(product.price);
      if (maxPrice > 0) {
        return (((currentPrice - maxPrice) / maxPrice) * 100).toFixed(2);
      }
      return '0.00';
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
  return '0.00%';
},
    getCurrentPriceClass(product) {
      return this.getPriceDifference(product) < 0 ? 'text-green-500' : 'text-gray-900';
    },
    getMaxPrice(product) {
      if (product.price_history) {
        return Math.max(...product.price_history.map(entry => parseFloat(entry.price)));
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
      this.$emit('remove-product', asin);
    },
  },
};
</script>

