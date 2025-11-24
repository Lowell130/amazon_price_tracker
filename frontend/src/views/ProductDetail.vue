<template>
  <section class="bg-gray-50 dark:bg-gray-900 min-h-screen pb-12">
    <div class="mx-auto max-w-screen-xl px-4 lg:px-12 pt-8">

      <!-- Dettagli del prodotto -->
      <ProductInfo v-if="product" :product="product" />

      <!-- Tabella dei prezzi (Grid Layout) -->
      <div v-if="product" class="mt-12">
        <h3 class="mb-6 text-3xl font-extrabold text-gray-900 dark:text-white md:text-3xl lg:text-4xl">
            <span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">Storico</span> Prezzi
        </h3>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <!-- Max Price -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center">
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Prezzo Max</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ product.max_price || '-' }}€</p>
            </div>
            <!-- Min Price -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center">
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Prezzo Min</p>
                <p class="text-xl font-bold text-green-600 dark:text-green-400">{{ product.min_price || '-' }}€</p>
            </div>
            <!-- Avg Price -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center">
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Prezzo Medio</p>
                <p class="text-xl font-bold text-blue-600 dark:text-blue-400">{{ product.average_price || '-' }}€</p>
            </div>
            <!-- Current Price -->
            <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 text-center ring-2 ring-blue-50 dark:ring-blue-900">
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">Attuale</p>
                <p class="text-xl font-bold text-gray-900 dark:text-white">{{ product.price || '-' }}€</p>
            </div>
        </div>
      </div>

      <!-- Grafico della cronologia dei prezzi -->
      <div class="mt-8 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
        <ChartPage v-if="product && product.price_history" :priceHistory="product.price_history" />
      </div>

      <!-- Sezione Dettagli Prodotto (List Layout) -->
      <div v-if="product && product.details?.length" class="mt-12">
        <h3 class="mb-6 text-3xl font-extrabold text-gray-900 dark:text-white md:text-3xl lg:text-4xl">
            <span class="text-transparent bg-clip-text bg-gradient-to-r to-emerald-600 from-sky-400">Dettagli</span> Tecnici
        </h3>

        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
            <div class="grid grid-cols-1 md:grid-cols-2">
                <div v-for="(detail, index) in product.details" :key="index" 
                     class="p-4 border-b border-gray-100 dark:border-gray-700 last:border-b-0 md:nth-last-child-2:border-b-0 md:odd:border-r">
                    <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">
                        {{ Object.keys(detail)[0] }}
                    </p>
                    <p class="text-base font-medium text-gray-900 dark:text-white">
                        {{ Object.values(detail)[0] }}
                    </p>
                </div>
            </div>
        </div>
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

  setOrCreateMeta("title", `Storico prezzi per ${product.title}`);
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

// ✅ Aggiunge dati strutturati Schema.org JSON-LD correttamente
function setStructuredData(product) {
  if (!product || !product.price) return; // Evita errori se il prodotto non è ancora caricato

  const jsonLd = {
    "@context": "https://schema.org/",
    "@type": "Product",
    "name": product.title,
    "image": product.image_url || "/default-image.jpg",
    "description": `Monitora il prezzo di ${product.title}. Controlla la cronologia dei prezzi e ricevi notifiche sui ribassi.`,
    "offers": {
      "@type": "Offer",  // ✅ Corretto "Offer" (non "Offerta")
      "priceCurrency": "EUR",
      "price": parseFloat(product.price),  // ✅ Assicura che il prezzo sia numerico
      "availability": "https://schema.org/InStock",
      "seller": {
        "@type": "Organization",  // ✅ Corretto "Organization" (non "Organizzazione")
        "name": "Amazon"
      }
    }
  };

  // ✅ Inserisce il JSON-LD nella pagina
  let script = document.querySelector('script[type="application/ld+json"]');
  if (!script) {
    script = document.createElement("script");
    script.setAttribute("type", "application/ld+json");
    document.head.appendChild(script);
  }
  script.textContent = JSON.stringify(jsonLd);
}


</script>
