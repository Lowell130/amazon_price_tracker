<template>
  <section class="bg-gray-50 py-8 antialiased dark:bg-gray-900 md:py-12">
    <!-- Barra di ricerca -->
    <div class="flex justify-center mb-10 px-4">
      <form @submit.prevent="redirectToSearch" class="flex items-center gap-4 w-full max-w-3xl">
        <input
          v-model="query"
          type="text"
          placeholder="Cerca un prodotto..."
          class="flex-grow rounded-lg border border-gray-300 text-gray-900 focus:ring-primary-600 focus:border-primary-600 block w-full p-3 text-base"
        />
        <button
          type="submit"
          class="text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5"
        >
          Cerca
        </button>
      </form>
    </div>

    <!-- Titolo -->
    <div class="flex flex-col justify-center items-center h-32">
      <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white md:text-4xl lg:text-5xl">
        <span class="text-transparent bg-clip-text bg-gradient-to-r to-red-600 from-amber-400">Risultati</span> della ricerca
      </h1>
    </div>

    <!-- Contenuto -->
    <div class="mx-auto max-w-screen-xl px-4 2xl:px-0">
      <div v-if="loading" class="flex justify-center items-center h-96">
        <p class="text-lg text-gray-500 dark:text-gray-400">Caricamento...</p>
      </div>

      <div v-else-if="error" class="flex justify-center items-center h-96">
        <p class="text-lg text-red-500">{{ error }}</p>
      </div>

      <div v-else-if="products.length === 0" class="flex justify-center items-center h-96">
        <p class="text-lg text-gray-500 dark:text-gray-400">Nessun prodotto trovato per "{{ query }}".</p>
      </div>

      <!-- Lista prodotti -->
      <div v-else class="mb-4 grid gap-4 sm:grid-cols-2 md:mb-8 lg:grid-cols-3 xl:grid-cols-4">
        <div
          v-for="product in products"
          :key="product.asin"
          class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800"
        >
          <!-- Immagine -->
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

          <!-- Condizione -->
          <div class="flex items-center justify-between gap-4 mt-4">
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
          </div>

          <!-- Dettagli prodotto -->
          <div class="pt-6">
            <a
              :href="`/products/${product.asin}`"
              target="_blank"
              class="text-lg font-semibold leading-tight text-gray-900 hover:underline dark:text-white"
            >
              {{ product.title.length > 25 ? product.title.substring(0, 25) + '...' : product.title }}
            </a>
            <p class="mt-2 text-primary-800 text-xs font-medium">Category: {{ product.category }}</p>

            <!-- Prezzi -->
            <p v-if="product.old_price" class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">
              Old Price: <span class="line-through">€{{ product.old_price }}</span>
            </p>
            <p v-if="product.new_price" class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">
              New Price: <span class="font-bold">€{{ product.new_price }}</span>
            </p>
            <p v-if="product.price_drop" class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400">
              Price dropped:
              <span class="bg-green-100 text-green-800 text-sm font-medium px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300">
                - €{{ product.price_drop }}
              </span>
            </p>

            <!-- Coupon -->
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
import { useRoute, useRouter } from "vue-router";
import { ref, watch, onMounted } from "vue";
import { fetchWithToken } from "@/api";

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();

    const query = ref(route.query.query || "");
    const products = ref([]);
    const loading = ref(true);
    const error = ref(null);

    const fetchResults = async () => {
      loading.value = true;
      error.value = null;
      products.value = [];

      try {
        const baseUrl = process.env.VUE_APP_API_BASE_URL;
        const searchUrl = `${baseUrl}/public/search-products?title=${query.value}`;
        const response = await fetchWithToken(searchUrl);

        if (!response.ok) throw new Error("Errore durante la ricerca.");

        const data = await response.json();
        const rawProducts = data.products || [];

        const detailedProducts = await Promise.all(
          rawProducts.map(async (p) => {
            try {
              const detailRes = await fetch(`${baseUrl}/public/product-details/${p.asin}`);
              if (!detailRes.ok) throw new Error();
              const full = await detailRes.json();

              const oldPrice = full.old_price ?? full.oldPrice ?? null;
              const newPrice = full.new_price ?? full.newPrice ?? full.price ?? null;
              const priceDrop = oldPrice && newPrice ? parseFloat((oldPrice - newPrice).toFixed(2)) : null;

              return {
                ...full,
                old_price: oldPrice,
                new_price: newPrice,
                price_drop: priceDrop,
              };
            } catch {
              return p;
            }
          })
        );

        products.value = detailedProducts;
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    };

    const redirectToSearch = () => {
      if (query.value.trim()) {
        router.push({ path: "/search", query: { query: query.value } });
      }
    };

    onMounted(fetchResults);

    watch(
      () => route.query.query,
      (newQuery) => {
        query.value = newQuery;
        fetchResults();
      }
    );

    return {
      query,
      products,
      loading,
      error,
      redirectToSearch,
    };
  },
};
</script>
