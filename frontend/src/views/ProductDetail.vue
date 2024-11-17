<template>
  <!-- Start block -->
<section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">
      <button  @click="$router.go(-1)" data-dropdown-toggle="actionsDropdown" class="w-full md:w-auto flex items-center justify-center py-2 px-4 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700" type="button">
                            <svg class="-ml-1 mr-1.5 w-5 h-5" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                <path clip-rule="evenodd" fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                            </svg>
                            Back
                        </button>
      <h1 class="text-2xl font-bold text-gray-800 mb-6">
        Price history for {{ productTitle }}
    </h1>
        <!-- Start coding here -->
        <div class="bg-white dark:bg-gray-800 relative shadow-md sm:rounded-lg overflow-hidden">
            <div class="flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">

              <div>ApexChart</div>
              
                <div class="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 items-stretch md:items-center justify-end md:space-x-3 flex-shrink-0">
              
                    <div class="flex items-center space-x-3 w-full md:w-auto">
                        <button  @click="$router.go(-1)" data-dropdown-toggle="actionsDropdown" class="w-full md:w-auto flex items-center justify-center py-2 px-4 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-primary-700 focus:z-10 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700" type="button">
                            <svg class="-ml-1 mr-1.5 w-5 h-5" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                <path clip-rule="evenodd" fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                            </svg>
                            Back
                        </button>
                       
                     
                     
                    </div>
                </div>
            </div>
            <div class="overflow-x-auto" v-if="priceHistory.length">
                <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead  class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" class="px-4 py-4">Date</th>
                            <th scope="col" class="px-4 py-3">Price</th>
                            <th scope="col" class="px-4 py-3">Variation</th>
                           
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(entry, index) in priceHistory" :key="entry.date" class="border-b dark:border-gray-700">
                            <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">{{ formatDate(entry.date) }}</th>                          
                            <td class="px-4 py-3"><span :class="getPriceClass(entry.price)">{{ parseFloat(entry.price).toFixed(2) }}€</span></td>
                            <td class="px-4 py-3"><span v-if="index > 0">{{ getPriceChange(index) }}</span><span v-else>-</span>
                            </td>
                        </tr>
                      
                    </tbody>
                </table>
            </div>
            <!-- <nav class="flex flex-col md:flex-row justify-between items-start md:items-center space-y-3 md:space-y-0 p-4" aria-label="Table navigation">
                <span class="text-sm font-normal text-gray-500 dark:text-gray-400">
                    Showing
                    <span class="font-semibold text-gray-900 dark:text-white">1-10</span>
                    of
                    <span class="font-semibold text-gray-900 dark:text-white">1000</span>
                </span>
             
            </nav> -->
        </div>
    </div>
</section>
<!-- End block -->

 
</template>

<script>
export default {
  name: "ProductDetail",
  data() {
    return {
      productTitle: "",
      priceHistory: [],
    };
  },
  async created() {
    const asin = this.$route.params.asin; // Recupera l'ASIN dai parametri dell'URL
    await this.fetchPriceHistory(asin);
  },
  methods: {
    async fetchPriceHistory(asin) {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(
          `${process.env.VUE_APP_API_BASE_URL}/price-history/${asin}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        const data = await response.json();
        this.priceHistory = data;
        this.productTitle = `${asin}`; // Sostituisci con il titolo reale se disponibile
      } catch (error) {
        console.error("Errore nel caricamento dello storico dei prezzi:", error);
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

<style>
/* Non è necessario aggiungere stili CSS qui poiché Tailwind CSS li copre. */
</style>
