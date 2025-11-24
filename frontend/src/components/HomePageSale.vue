<template>
  <section class="bg-gray-50 py-8 antialiased dark:bg-gray-900 md:py-12">
    <div class="h-56">
      <ProductSearch />
    </div>

    <div class="mx-auto max-w-screen-xl px-4 2xl:px-0">
      
      <!-- Section Header -->
      <div class="mb-8 lg:mb-16 text-center">
          <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-gray-900 md:text-4xl dark:text-white">
              🔥 Offerte <span class="text-red-600">Appena Ribassate</span>
          </h2>
          <p class="text-gray-500 sm:text-xl dark:text-gray-400">
              I migliori affari scovati dal nostro tracker nelle ultime ore.
          </p>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center h-96">
        <SpinnerComp />
      </div>

      <div v-else-if="error" class="flex justify-center items-center h-96">
        <p class="text-lg text-red-500">{{ error }}</p>
      </div>

      <div v-else-if="products && products.length === 0" class="flex justify-center items-center h-96">
        <p class="text-lg text-gray-500 dark:text-gray-400">Nessun ribasso recente trovato.</p>
      </div>

      <div v-else class="mb-4 grid gap-6 sm:grid-cols-2 md:mb-8 lg:grid-cols-3 xl:grid-cols-4">
        <div
          v-for="product in products"
          :key="product.asin"
          class="group relative rounded-2xl border border-gray-200 bg-white p-4 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 dark:border-gray-700 dark:bg-gray-800"
        >
          <div class="h-48 w-full overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-700 p-4 relative">
            <!-- Badge Sconto -->
            <div v-if="product.price_drop" class="absolute top-2 right-2 bg-red-600 text-white text-xs font-bold px-2 py-1 rounded-full shadow-md z-10">
                -€{{ product.price_drop }}
            </div>

            <a :href="`/products/${product.asin}`" target="_blank" class="block h-full">
              <img
                class="mx-auto h-full object-contain mix-blend-multiply dark:mix-blend-normal transform group-hover:scale-110 transition-transform duration-500"
                :src="product.image_url"
                :alt="product.title"
              />
            </a>
          </div>

          <div class="pt-4">
            <div class="mb-2 flex items-center justify-between">
                <span
                    v-if="product.condition === 'Nuovo'"
                    class="bg-green-100 text-green-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-green-900 dark:text-green-300"
                >
                    Nuovo
                </span>
                <span
                    v-else
                    class="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300"
                >
                    {{ product.condition }}
                </span>
                
                <p class="text-xs text-gray-500 dark:text-gray-400 truncate max-w-[50%]">{{ product.category }}</p>
            </div>

            <a
              :href="`/products/${product.asin}`"
              target="_blank"
              class="block text-lg font-semibold leading-tight text-gray-900 hover:text-blue-600 dark:text-white dark:hover:text-blue-400 line-clamp-2 h-14"
            >
              {{ product.title.length > 30 ? product.title.substring(0, 30) + "..." : product.title }}
            </a>

            <div class="mt-4 flex items-end justify-between">
                <div>
                    <p class="text-sm text-gray-500 line-through dark:text-gray-400">€{{ product.old_price }}</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">€{{ product.new_price }}</p>
                </div>
                
                <a :href="`/products/${product.asin}`" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm p-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
                    </svg>
                    <span class="sr-only">Vedi dettagli</span>
                </a>
            </div>

            <!-- ✅ COUPON -->
            <div v-if="product.coupon && product.coupon_value" class="mt-3 flex items-center gap-2 text-sm font-medium text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/30 p-2 rounded-lg border border-green-100 dark:border-green-800">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M5 5a3 3 0 015-2.236A3 3 0 0114.83 6H16a2 2 0 110 4h-5V9a1 1 0 10-2 0v1H4a2 2 0 110-4h1.17C5.06 5.687 5 5.35 5 5zm4 1V5a1 1 0 10-1 1h1zm3 0a1 1 0 10-1-1v1h1z" clip-rule="evenodd"></path><path d="M9 11H3v5a2 2 0 002 2h4v-7zM11 18h4a2 2 0 002-2v-5h-6v7z"></path></svg>
                Coupon: -€{{ product.coupon_value }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ProductSearch from "@/components/ProductSearch.vue";
import SpinnerComp from "@/components/SpinnerComp.vue";

export default {
  components: {
    ProductSearch,
    SpinnerComp
  },
  data() {
    return {
      products: [],
      isLoading: true,
      error: null,
    };
  },
  async created() {
    try {
      const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/public/price-drops`);
      if (!response.ok) {
        throw new Error(`Error fetching price drops: ${response.statusText}`);
      }
      const data = await response.json();
      this.products = data.data || [];
    } catch (err) {
      this.error = err.message;
    } finally {
      this.isLoading = false;
    }
  },
};
</script>
