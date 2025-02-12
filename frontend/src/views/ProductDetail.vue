<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12">

      <!-- Pulsante Back -->
      <!-- <div class="mb-4">
        <button
          @click="goBack"
          class="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-blue-400"
        >
          <svg class="w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </button>
      </div> -->

      <!-- Dettagli del prodotto -->
      <ProductInfo v-if="product" :product="product" />

      <!-- Sezione Dettagli Prodotto -->
      <div v-if="product && product.details?.length" class="mt-6 bg-white dark:bg-gray-800 p-4">
        <h3 class="my-5 text-3xl font-extrabold text-gray-900 dark:text-white md:text-3xl lg:text-4xl"><span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">Product</span> Details</h3>

        <div class="relative overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="px-6 py-3">Detail</th>
                <th scope="col" class="px-6 py-3">Value</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(detail, index) in product.details" :key="index" class="border-b dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                  {{ Object.keys(detail)[0] }}
                </th>
                <td class="px-6 py-4">
                  {{ Object.values(detail)[0] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tabella dei prezzi -->
      <div class="mt-6 bg-white dark:bg-gray-800 p-4">
      <h3 class="my-5 text-3xl font-extrabold text-gray-900 dark:text-white md:text-3xl lg:text-4xl"><span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">Price</span> History</h3>

      <div class="bg-white dark:bg-gray-800 relative overflow-hidden mt-6">

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
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">Maximum Price</th>
                <td class="px-4 py-3">{{ product.max_price || '-' }}€</td>
              </tr>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">Minimum Price</th>
                <td class="px-4 py-3">{{ product.min_price || '-' }}€</td>
              </tr>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">Average Price</th>
                <td class="px-4 py-3">{{ product.average_price || '-' }}€</td>
              </tr>
              <tr class="border-b dark:border-gray-700">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white">Current Price</th>
                <td class="px-4 py-3">{{ product.price || '-' }}€</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

      <!-- Grafico della cronologia dei prezzi -->
      <div class="mb-3">
        <ChartPage v-if="product && product.price_history" :priceHistory="product.price_history" />
      </div>

    </div>
  </section>
</template>
<script>
import ChartPage from "../components/ChartPage.vue";
import ProductInfo from "../components/ProductInfo.vue";
import { onMounted, watch, onUnmounted, ref } from "vue";
import { useRoute } from "vue-router";

export default {
  name: "ProductDetail",
  components: { ChartPage, ProductInfo },
  setup() {
    const route = useRoute();
    const product = ref(null);

    const fetchProductDetails = async (asin) => {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/public/product-details/${asin}`);
        if (!response.ok) throw new Error("Product not found");
        product.value = await response.json();
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    };

    onMounted(() => {
      const asin = route.params.asin;
      fetchProductDetails(asin);
    });

    // ✅ Watch per aggiornare i meta tag quando il prodotto cambia
    watch(product, (newProduct) => {
      if (newProduct) {
        updateMetaTags(newProduct);
      }
    });

    // 🔄 Reset dei meta tag quando si lascia la pagina
    onUnmounted(() => {
      resetMetaTags();
    });

    return { product };
  },
};

// ✅ Funzione per aggiornare i meta tag in italiano
function updateMetaTags(product) {
  if (!product) return;

  const description = `Monitora il prezzo di ${product.title}. Controlla la cronologia dei prezzi e ricevi notifiche sui ribassi.`;

  setOrCreateMeta("title", `${product.title} - Monitor Prezzi Amazon`);
  setOrCreateMeta("description", description);
  setOrCreateMeta("og:title", `${product.title} - Monitor Prezzi Amazon`);
  setOrCreateMeta("og:description", description);
  setOrCreateMeta("og:image", product.image_url || "/default-image.jpg");
  setOrCreateMeta("og:url", window.location.href);
  setOrCreateMeta("twitter:card", "summary_large_image");
  setOrCreateMeta("twitter:title", `${product.title} - Monitor Prezzi Amazon`);
  setOrCreateMeta("twitter:description", description);
  setOrCreateMeta("twitter:image", product.image_url || "/default-image.jpg");

  // ✅ Aggiunge Schema.org JSON-LD per Google SEO
  setStructuredData(product);
}

// ✅ Funzione per creare o aggiornare i meta tag
function setOrCreateMeta(name, content) {
  if (name === "title") {
    document.title = content;
    return;
  }

  let meta = document.querySelector(`meta[name="${name}"], meta[property="${name}"]`);
  if (!meta) {
    meta = document.createElement("meta");
    if (name.startsWith("og:") || name.startsWith("twitter:")) {
      meta.setAttribute("property", name);
    } else {
      meta.setAttribute("name", name);
    }
    document.head.appendChild(meta);
  }
  meta.setAttribute("content", content);
}

// ✅ Ripristina i meta tag ai valori predefiniti in italiano quando si lascia la pagina
function resetMetaTags() {
  document.title = "Monitor Prezzi Amazon - Monitora e Trova Offerte";

  const defaultMetaTags = {
    "description": "Monitora i prezzi dei prodotti su Amazon e ricevi notifiche quando il prezzo scende.",
    "og:title": "Monitor Prezzi Amazon",
    "og:description": "Scopri la cronologia dei prezzi e trova le migliori offerte su Amazon.",
    "og:image": "/default-meta-image.jpg",
    "og:url": window.location.origin,
    "twitter:card": "summary_large_image",
    "twitter:title": "Monitor Prezzi Amazon",
    "twitter:description": "Segui i prezzi dei prodotti su Amazon e trova il momento migliore per acquistare.",
    "twitter:image": "/default-meta-image.jpg",
  };

  for (const [name, content] of Object.entries(defaultMetaTags)) {
    setOrCreateMeta(name, content);
  }

  // ❌ Rimuove il JSON-LD Schema.org della pagina prodotto
  const jsonLdScript = document.querySelector('script[type="application/ld+json"]');
  if (jsonLdScript) {
    jsonLdScript.remove();
  }
}

// ✅ Aggiunge dati strutturati Schema.org JSON-LD in italiano
function setStructuredData(product) {
  const jsonLd = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": product.title,
    "image": product.image_url || "/default-image.jpg",
    "description": `Monitora il prezzo di ${product.title}. Controlla la cronologia dei prezzi e ricevi notifiche sui ribassi.`,
    "offers": {
      "@type": "Offerta",
      "priceCurrency": "EUR",
      "price": product.price,
      "availability": "https://schema.org/InStock",
      "seller": { "@type": "Organizzazione", "name": "Amazon" },
    }
  };

  let script = document.querySelector('script[type="application/ld+json"]');
  if (!script) {
    script = document.createElement("script");
    script.setAttribute("type", "application/ld+json");
    document.head.appendChild(script);
  }
  script.textContent = JSON.stringify(jsonLd);
}

</script>
