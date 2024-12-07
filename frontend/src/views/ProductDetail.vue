<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
      <!-- Pulsante Back -->
      <div class="mb-4">
        <button
          @click="goBack"
          class="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-400"
        >
          <svg
            class="w-4 h-4 mr-2"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Back to Dashboard
        </button>
      </div>

      <!-- Dettagli del prodotto -->
      <ProductInfo v-if="product" :product="product" />

      <div class="bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden mt-6">
        <div v-if="product" class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="px-4 py-4">Metric</th>
                <th scope="col" class="px-4 py-3">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  Maximum Price
                </th>
                <td v-if="product.max_price" class="px-4 py-3">
                  {{ product.max_price }}€ <span class="text-xs text-gray-900 dark:text-white" v-if="product.max_price_date">({{ formatDate(product.max_price_date) }})</span>
                </td>
                <td v-else class="px-4 py-3">-</td>
              </tr>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  Minimum Price
                </th>
                <td v-if="product.min_price" class="px-4 py-3">
                  {{ product.min_price }}€ <span class="text-xs text-gray-900 dark:text-white" v-if="product.min_price_date">({{ formatDate(product.min_price_date) }})</span>
                </td>
                <td v-else class="px-4 py-3">-</td>
              </tr>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  Average Price
                </th>
                <td v-if="product.average_price" class="px-4 py-3">{{ product.average_price }}€</td>
                <td v-else class="px-4 py-3">-</td>
              </tr>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  Current Price
                </th>
                <td v-if="product.price" class="px-4 py-3">
                  {{ product.price }}€ 
                </td>
                <td v-else class="px-4 py-3">-</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="mb-3 mt-3">
        <!-- Monta ChartPage solo quando product e price_history sono disponibili -->
        <ChartPage v-if="product && product.price_history" :priceHistory="product.price_history" />
      </div>
    </div>
  </section>
</template>

<script>
import ChartPage from "../components/ChartPage.vue";
import ProductInfo from "../components/ProductInfo.vue";

export default {
  name: "ProductDetail",
  components: { ChartPage, ProductInfo },
  data() {
    return {
      product: null,
    };
  },
  async created() {
    const asin = this.$route.params.asin;
    await this.fetchProductDetails(asin);
  },
  methods: {
    async fetchProductDetails(asin) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `${process.env.VUE_APP_API_BASE_URL}/product-details/${asin}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.product = await response.json();
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    },
    formatDate(date) {
      if (!date) return null;
      const options = { year: "numeric", month: "short", day: "numeric" };
      return new Date(date).toLocaleDateString("en-US", options);
    },
    goBack() {
      this.$router.push({ name: "Dashboard" }); // Reindirizza alla pagina "Dashboard"
    },
  },
};
</script>
