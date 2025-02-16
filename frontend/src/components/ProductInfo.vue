<template>
  <section class="py-8 bg-white md:py-16 dark:bg-gray-900 antialiased rounded-t-lg">
    <div class="max-w-screen-xl px-4 mx-auto 2xl:px-0">
      <div class="lg:grid lg:grid-cols-2 lg:gap-8 xl:gap-16 px-3">
        <div class="shrink-0 max-w-md lg:max-w-lg mx-auto">
          <img class="w-full dark:hidden" :src="product.image_url" alt="" />
          <!-- <img class="w-full hidden dark:block" src="https://flowbite.s3.amazonaws.com/blocks/e-commerce/imac-front-dark.svg" alt="" /> -->
        </div>

        <div class="mt-6 sm:mt-8 lg:mt-0 p-3">
          <h1
            class="text-xl font-semibold text-gray-900 sm:text-2xl dark:text-white mb-3"
          >
            {{ product.title }}
          </h1>

          <p class="text-gray-600 text-sm mb-2">Category: {{ product.category }}</p>
          <p class="text-gray-600 text-sm mb-2">ASIN: {{ product.asin }}</p>
          <p class="text-gray-600 text-sm mb-2">
            Insertion Date: {{ formatDate(product.insertion_date) }}
          </p>

          <!-- Condizione del prodotto -->
          <p class="text-gray-600 text-sm mb-2">
            Condition:
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
          </p>

          <p v-if="product.availability !== 'Non disponibile'" class="text-2xl font-extrabold text-gray-900 sm:text-3xl dark:text-white">
            {{ product.price }}€
          </p>
          <p v-else class="text-2xl font-extrabold text-gray-900 sm:text-3xl dark:text-white flex items-center">
            N/A
            <svg class="w-5 h-5 ml-1 text-gray-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v8m4-4H8" />
            </svg>
          </p>       

          <p class="mt-4">
  <a
    :href="product.affiliate"
    target="_blank"
    class="flex items-center justify-center text-black bg-[#FF9900] hover:bg-[#FFB74D] focus:ring-4 focus:ring-yellow-300 font-bold rounded-lg text-lg px-6 py-3 transition duration-300 ease-in-out transform hover:scale-105 focus:outline-none shadow-lg w-full md:w-auto"
  >
    Vedi su Amazon.it
  </a>
</p>






        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "ProductInfo",
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  methods: {
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
  },
};
</script>

<style scoped>
.product-info {
  max-width: 600px;
  margin: 0 auto;
}
</style>
