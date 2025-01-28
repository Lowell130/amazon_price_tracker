<template>
    <section class="bg-gray-50 py-8 antialiased dark:bg-gray-900 md:py-12">
      <div class="flex flex-col justify-center items-center h-56">
  <h1 class="mb-4 pb-3 text-3xl font-extrabold text-gray-900 dark:text-white md:text-5xl lg:text-6xl">
    <span class="text-transparent bg-clip-text bg-gradient-to-r to-red-600 from-amber-400">Best Price</span> Drop Today
  </h1>
  <svg class="w-10 h-10 text-gray-800 dark:text-white animate-bounce" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19V5m0 14-4-4m4 4 4-4"/>
  </svg>
</div>

    
      <div class="mx-auto max-w-screen-xl px-4 2xl:px-0">
        <!-- Loading State -->
        <div v-if="isLoading" class="flex justify-center items-center h-96">
          <p class="text-lg text-gray-500 dark:text-gray-400">Loading...</p>
        </div>
  
        <!-- Error State -->
        <div v-else-if="error" class="flex justify-center items-center h-96">
          <p class="text-lg text-red-500">{{ error }}</p>
        </div>
  
        <!-- No Products Found -->
        <div v-else-if="products && products.length === 0" class="flex justify-center items-center h-96">
          <p class="text-lg text-gray-500 dark:text-gray-400">No price drops available.</p>
        </div>
  
        <!-- Products List -->
         
        <div v-else class="mb-4 grid gap-4 sm:grid-cols-2 md:mb-8 lg:grid-cols-3 xl:grid-cols-4">
            <div
            v-for="product in products"
            :key="product.asin"
            class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800"
          >
            <div class="h-56 w-full">
              <a :href="product.affiliate" target="_blank">
                <img
                  class="mx-auto h-full object-contain dark:hidden"
                  :src="product.image_url"
                  :alt="product.title"
                />
                <img
                  v-if="product.image_url"
                  class="mx-auto hidden h-full object-contain dark:block"
                  :src="product.image_url"
                  :alt="product.title"
                />
              </a>
            </div>
        



            <div class="flex items-center justify-between gap-4">
            <span>
    <span
    v-if="product.condition === 'Nuovo'"
    class="bg-green-100 text-green-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-green-900 dark:text-green-300"
  >
    Condition: New
  </span>
  <span
    v-else-if="product.condition === 'Usato'"
    class="bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300"
  >
  Condition: Used
  </span>
  <span
    v-else
    class="bg-red-100 text-red-800 text-xs font-medium px-2 py-0.5 rounded dark:bg-red-900 dark:text-red-300"
  >
  Condition: Unavailable
  </span>

</span>

            <div class="flex items-center justify-end gap-1">
                <a
  :href="product.affiliate"
  type="button"
  data-tooltip-target="tooltip-quick-look-2"
  class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
>
  <span class="sr-only">Quick look</span>
  <svg
    class="h-5 w-5"
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="none"
    viewBox="0 0 24 24"
  >
    <path
      stroke="currentColor"
      stroke-width="2"
      d="M21 12c0 1.2-4.03 6-9 6s-9-4.8-9-6c0-1.2 4.03-6 9-6s9 4.8 9 6Z"
    ></path>
    <path
      stroke="currentColor"
      stroke-width="2"
      d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
    ></path>
  </svg>
</a>

              <div id="tooltip-quick-look-2" role="tooltip" class="tooltip absolute z-10 inline-block rounded-lg bg-gray-900 px-3 py-2 text-sm font-medium text-white shadow-sm transition-opacity duration-300 dark:bg-gray-700 opacity-0 invisible" data-popper-placement="top" style="position: absolute; inset: auto auto 0px 0px; margin: 0px; transform: translate3d(564.8px, -892px, 0px);">
                Quick look
                <div class="tooltip-arrow" data-popper-arrow="" style="position: absolute; left: 0px; transform: translate3d(43.2px, 0px, 0px);"></div>
              </div>

              
            </div>
          </div>




            <div class="pt-6">
              <a :href="product.affiliate" target="_blank" class="text-lg font-semibold leading-tight text-gray-900 hover:underline dark:text-white">
                {{ product.title.substring(0, 25)
                      }}{{ product.title.length > 25 ? "..." : "" }}
              </a>
              <p class="mt-2 text-primary-800 text-xs font-medium">Category: {{ product.category }}</p>
              <p class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">Old Price: <span class="line-through">€{{ product.old_price }}</span></p>
              <p class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">New Price: <span class="font-bold">€{{ product.new_price }}</span></p>
              <p v-if="product.price_drop" class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">
                Price dropped: <span class="bg-green-100 text-green-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">- €{{ product.price_drop }}</span>
              </p>
             
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    data() {
      return {
        products: [], // Inizializza come array vuoto
        isLoading: true, // Indica se i dati sono in caricamento
        error: null, // Memorizza eventuali errori
      };
    },
    async created() {
      try {
        // Effettua la chiamata API all'endpoint pubblico "price_drops".
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/public/price-drops`);
        if (!response.ok) {
          throw new Error(`Error fetching price drops: ${response.statusText}`);
        }
        const data = await response.json();
        this.products = data.data || []; // Utilizza "data" dalla risposta dell'API
      } catch (err) {
        this.error = err.message;
      } finally {
        this.isLoading = false; // Disattiva lo stato di caricamento
      }
    },
  };
  </script>
  
 
  