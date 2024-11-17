<template>
  <div>
    <!-- Start block -->

    <div class="mx-auto max-w-screen-2xl px-4 lg:px-12">
        <div class="bg-white dark:bg-gray-800 relative shadow-md overflow-hidden">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between space-y-3 md:space-y-0 md:space-x-4 p-4">             
            </div>         

            <!-- PRODUCTS LIST START -->
            <div class="overflow-x-auto">
                <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                        <tr>
                            <th scope="col" class="p-4">
                               
                            </th>
                            <th scope="col" class="p-4">mail</th>
                           
                            <th scope="col" class="p-4">Product</th>
                            <th scope="col" class="p-4">Current price</th>
                            <th scope="col" class="p-4">Previous price</th>
                            <th scope="col" class="p-4">asin</th>
                            <th scope="col" class="p-4"></th>
                       
                        </tr>
                    </thead>
                    <tbody v-for="product in sortedProducts" :key="product.asin">
                        <tr class="border-b dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700">
                            <td class="p-4 w-4">
                              
                            </td>
                            <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                              <div>
                            <label class="inline-flex items-center cursor-pointer">
  <input type="checkbox" value="" class="sr-only peer">
  <div class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
</label></div>
                            </td>
                            <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
  <div class="flex items-center mr-3">
    <!-- Contenitore dell'immagine con dimensioni fisse -->
    <div class="h-10 w-10 flex-shrink-0 flex items-center justify-center rounded">
      <img
        v-if="product.image_url"
        :src="product.image_url"
        :alt="product.title"
        class="h-full w-full object-contain"
      />
    </div>
    <!-- Testo allineato a destra -->
    <span class="ml-3 text-right">{{ product.title.substring(0, 20) }}{{ product.title.length > 20 ? '...' : '' }}</span>
  </div>
</th>

                        
                            <td class="px-4 py-3 font-medium">
                              <strong :class="getPriceChangeClass(product)">
                {{ formatPrice(product.price) }}€
              </strong>
              <span v-if="getPriceChangePercentage(product) !== '0.00%'" :class="getPriceChangeClass(product)">
                ({{ getPriceChangePercentage(product) }}%)
              </span></td>
                            <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white"><strong>{{ formatPrice(getLastMonitoredPrice(product)) }}€</strong></td>
                            <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                <div class="flex items-center">
                                
                                    <span class="text-gray-500 dark:text-gray-400 ml-1">{{ product.asin }}</span>
                                </div>
                            </td>
                          
                            <td class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                                <div class="flex items-center space-x-4">
                                  <a :href="product.product_url" target="_blank" type="button" class="uppercase text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50">
<svg class="w-4 h-4 me-2 -ms-1" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="paypal" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M257.2 162.7c-48.7 1.8-169.5 15.5-169.5 117.5 0 109.5 138.3 114 183.5 43.2 6.5 10.2 35.4 37.5 45.3 46.8l56.8-56S341 288.9 341 261.4V114.3C341 89 316.5 32 228.7 32 140.7 32 94 87 94 136.3l73.5 6.8c16.3-49.5 54.2-49.5 54.2-49.5 40.7-.1 35.5 29.8 35.5 69.1zm0 86.8c0 80-84.2 68-84.2 17.2 0-47.2 50.5-56.7 84.2-57.8v40.6zm136 163.5c-7.7 10-70 67-174.5 67S34.2 408.5 9.7 379c-6.8-7.7 1-11.3 5.5-8.3C88.5 415.2 203 488.5 387.7 401c7.5-3.7 13.3 2 5.5 12zm39.8 2.2c-6.5 15.8-16 26.8-21.2 31-5.5 4.5-9.5 2.7-6.5-3.8s19.3-46.5 12.7-55c-6.5-8.3-37-4.3-48-3.2-10.8 1-13 2-14-.3-2.3-5.7 21.7-15.5 37.5-17.5 15.7-1.8 41-.8 46 5.7 3.7 5.1 0 27.1-6.5 43.1z"/>
</svg>
Open
</a>
<button @click="viewPriceHistory(product.asin)" type="button" class="uppercase text-gray-900 bg-gray-100 hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500">
  <svg class="w-4 h-4 me-2 -ms-1 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v15a1 1 0 0 0 1 1h15M8 16l2.5-5.5 3 3L17.273 7 20 9.667"/>
</svg>History
</button>

<button @click="removeProduct(product.asin)" type="button" class="uppercase  hover:bg-red-800  text-white bg-red-600  focus:ring-4 focus:outline-none focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-500">
  <svg class="w-4 h-4 me-2 -ms-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
  <path d="M18.3 5.7a1 1 0 0 1 0 1.4L13.4 12l4.9 4.9a1 1 0 0 1-1.4 1.4L12 13.4l-4.9 4.9a1 1 0 0 1-1.4-1.4l4.9-4.9-4.9-4.9a1 1 0 1 1 1.4-1.4L12 10.6l4.9-4.9a1 1 0 0 1 1.4 0z"/>
</svg>delete
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
                    <span class="font-semibold text-gray-900 dark:text-white">1-10</span>
                    of
                    <span class="font-semibold text-gray-900 dark:text-white">1000</span>
                </span>
                <ul class="inline-flex items-stretch -space-x-px">
                    <li>
                        <a href="#" class="flex items-center justify-center h-full py-1.5 px-3 ml-0 text-gray-500 bg-white rounded-l-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                            <span class="sr-only">Previous</span>
                            <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                            </svg>
                        </a>
                    </li>
                    <li>
                        <a href="#" class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">1</a>
                    </li>
                    <li>
                        <a href="#" class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">2</a>
                    </li>
                    <li>
                        <a href="#" aria-current="page" class="flex items-center justify-center text-sm z-10 py-2 px-3 leading-tight text-primary-600 bg-primary-50 border border-primary-300 hover:bg-primary-100 hover:text-primary-700 dark:border-gray-700 dark:bg-gray-700 dark:text-white">3</a>
                    </li>
                    <li>
                        <a href="#" class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">...</a>
                    </li>
                    <li>
                        <a href="#" class="flex items-center justify-center text-sm py-2 px-3 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">100</a>
                    </li>
                    <li>
                        <a href="#" class="flex items-center justify-center h-full py-1.5 px-3 leading-tight text-gray-500 bg-white rounded-r-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                            <span class="sr-only">Next</span>
                            <svg class="w-5 h-5" aria-hidden="true" fill="currentColor" viewbox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                            </svg>
                        </a>
                    </li>
                </ul>
            </nav>
        </div>
    </div>

<!-- End block -->
    <PriceHistory v-if="priceHistory.length" :history="priceHistory" />
  </div>
</template>

<script>
import PriceHistory from './PriceHistory.vue';
// import AddProduct from '../components/AddProduct.vue';

export default {
  components: { PriceHistory},
  props: ['products'],
  data() {
    return {
      priceHistory: []
    };
  },
  computed: {
    sortedProducts() {
      return [...this.products].sort((a, b) => {
        const changeA = this.getPriceChangePercentage(a);
        const changeB = this.getPriceChangePercentage(b);
        return parseFloat(changeA) - parseFloat(changeB);
      });
    }
  },
  methods: {
    async showPriceHistory(asin) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/price-history/${asin}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        this.priceHistory = await response.json();
      } catch (error) {
        console.error('Errore nel caricamento dello storico dei prezzi:', error);
      }
    },
    async removeProduct(asin) {
      this.$emit('remove-product', asin);
    },
    viewPriceHistory(asin) {
      this.$router.push(`/products/${asin}`);
    },
    getLastMonitoredPrice(product) {
      if (product.price_history && product.price_history.length > 1) {
        return product.price_history[product.price_history.length - 2].price;
      }
      return product.price;
    },
    getPriceChangePercentage(product) {
      const lastPrice = this.getLastMonitoredPrice(product);
      const currentPrice = parseFloat(product.price);
      const lastMonitored = parseFloat(lastPrice);

      if (lastMonitored) {
        const percentageChange = (((currentPrice - lastMonitored) / lastMonitored) * 100).toFixed(2);
        return (percentageChange > 0 ? `+${percentageChange}` : percentageChange) + '%';
      }
      return '0.00%';
    },
    getPriceChangeClass(product) {
      const percentageChange = parseFloat(this.getPriceChangePercentage(product));
      if (percentageChange < 0) {
        return 'price-decrease';
      } else if (percentageChange > 0) {
        return 'price-increase';
      }
      return '';
    },
    formatPrice(price) {
      return parseFloat(price).toFixed(2);
    }
  }
};
</script>

<style scoped>
/* Stile per il pulsante "Apri su Amazon" */
.amazon-link-button {
  background-color: #ff9900;
  color: white;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-left: 10px;
  display: inline-block;
  text-align: center;
}

.amazon-link-button:hover {
  background-color: #e68a00;
}

.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 10px;
  transition: box-shadow 0.2s;
}

.product-item:hover {
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.product-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.product-image {
  width: 50px;
  height: auto;
  margin-right: 15px;
  border-radius: 4px;
}

.product-details {
  flex: 1;
}

.remove-button {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.remove-button:hover {
  background-color: #ff7875;
}

.view-history-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
  margin-left: 10px;
  transition: background-color 0.2s;
}

.view-history-button:hover {
  background-color: #66bb6a;
}

.price-decrease {
  color: green;
  font-weight: bold;
}

.price-increase {
  color: red;
  font-weight: bold;
}
</style>
