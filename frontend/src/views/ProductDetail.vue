<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
      <div class="mb-6">
        <ChartPage :priceHistory="priceHistory" />
      </div>

      <!-- Dettagli del prodotto -->
      <ProductInfo v-if="product" :product="product" />

      <div class="bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden mt-6">
        <div v-if="priceHistory.length" class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="px-4 py-4">Date</th>
                <th scope="col" class="px-4 py-3">Price</th>
                <th scope="col" class="px-4 py-3">Variation</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(entry, index) in priceHistory" :key="entry.date" class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  {{ formatDate(entry.date) }}
                </th>
                <td class="px-4 py-3">
                  <span> {{ entry.price }}</span>
                </td>
                <td class="px-4 py-3">
                  <span v-if="index > 0">{{ getPriceChange(index) }}</span>
                  <span v-else>-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
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
      priceHistory: [],
    };
  },
  async created() {
    const asin = this.$route.params.asin;
    await this.fetchProductDetails(asin);
    await this.fetchPriceHistory(asin);
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
    async fetchPriceHistory(asin) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `${process.env.VUE_APP_API_BASE_URL}/price-history/${asin}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.priceHistory = await response.json();
      } catch (error) {
        console.error("Error fetching price history:", error);
      }
    },
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
    getPriceChange(index) {
      const previousPrice = parseFloat(this.priceHistory[index - 1].price);
      const currentPrice = parseFloat(this.priceHistory[index].price);
      const difference = currentPrice - previousPrice;
      const percentageChange = ((difference / previousPrice) * 100).toFixed(2);
      return `${difference > 0 ? "+" : ""}${percentageChange}%`;
    },
    getPriceClass(price) {
      const latestPrice = parseFloat(
        this.priceHistory[this.priceHistory.length - 1].price
      );
      const currentPrice = parseFloat(price);
      if (currentPrice > latestPrice) return "text-red-500";
      if (currentPrice < latestPrice) return "text-green-500";
      return "text-gray-700";
    },
  },
};
</script>
