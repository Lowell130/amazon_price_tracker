<template>
  <section class="bg-gray-50 py-8 antialiased dark:bg-gray-900 md:py-12">
    <div class="h-56">
      <ProductSearch />
    </div>

    <div class="mx-auto max-w-screen-xl px-4 2xl:px-0">
      <div v-if="isLoading" class="flex justify-center items-center h-96">
        <p class="text-lg text-gray-500 dark:text-gray-400">Loading...</p>
      </div>

      <div v-else-if="error" class="flex justify-center items-center h-96">
        <p class="text-lg text-red-500">{{ error }}</p>
      </div>

      <div v-else-if="products && products.length === 0" class="flex justify-center items-center h-96">
        <p class="text-lg text-gray-500 dark:text-gray-400">No price drops available.</p>
      </div>

      <div v-else class="mb-4 grid gap-4 sm:grid-cols-2 md:mb-8 lg:grid-cols-3 xl:grid-cols-4">
        <div
          v-for="product in products"
          :key="product.asin"
          class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800"
        >
          <div class="h-56 w-full">
            <a :href="`/products/${product.asin}`" target="_blank">
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
                :href="`/products/${product.asin}`"
                type="button"
                class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-900 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white"
              >
                <span class="sr-only">Quick look</span>
                <svg
                  class="h-5 w-5"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke="currentColor"
                    stroke-width="2"
                    d="M21 12c0 1.2-4.03 6-9 6s-9-4.8-9-6c0-1.2 4.03-6 9-6s9 4.8 9 6Z"
                  />
                  <path
                    stroke="currentColor"
                    stroke-width="2"
                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                  />
                </svg>
              </a>
            </div>
          </div>

          <div class="pt-6">
            <a
              :href="`/products/${product.asin}`"
              target="_blank"
              class="text-lg font-semibold leading-tight text-gray-900 hover:underline dark:text-white"
            >
              {{ product.title.length > 25 ? product.title.substring(0, 25) + "..." : product.title }}
            </a>

            <p class="mt-2 text-primary-800 text-xs font-medium">Category: {{ product.category }}</p>

            <p class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">
              Old Price: <span class="line-through">€{{ product.old_price }}</span>
            </p>
            <p class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">
              New Price: <span class="font-bold">€{{ product.new_price }}</span>
            </p>

            <p
              v-if="product.price_drop"
              class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400"
            >
              Price dropped:
              <span
                class="bg-green-100 text-green-800 text-sm font-medium me-2 px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300"
              >
                - €{{ product.price_drop }}
              </span>
            </p>

            <!-- ✅ COUPON -->
            <p
              v-if="product.coupon && product.coupon_value"
              class="mt-2 text-sm font-medium text-green-600 dark:text-green-400"
            >
              Coupon disponibile:
              <span
                class="bg-green-100 text-green-800 text-sm font-medium px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300"
              >
                -€{{ product.coupon_value }}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ProductSearch from "@/components/ProductSearch.vue";

export default {
  components: {
    ProductSearch,
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
