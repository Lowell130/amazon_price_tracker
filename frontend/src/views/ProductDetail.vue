<template>
  <section class="bg-gray-50 dark:bg-gray-950 min-h-screen pb-20 selection:bg-blue-100 selection:text-blue-700">
    <div class="mx-auto max-w-screen-xl px-6 lg:px-12 pt-12">

      <!-- Product Meta/Main Card -->
      <div class="grid grid-cols-1 gap-8 mb-16">
        <ProductInfo v-if="product" :product="product" />
      </div>

      <!-- Bento Grid for Analysis & History -->
      <div v-if="product" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Left: Price Analysis & Stats (4 cols) -->
        <div class="lg:col-span-4 space-y-8">
          <div class="bg-white dark:bg-gray-900 p-8 rounded-[2.5rem] shadow-sm border border-gray-100 dark:border-gray-800 transition-all hover:shadow-xl hover:shadow-blue-500/5 group">
            <h3 class="mb-8 text-2xl font-black text-gray-900 dark:text-white tracking-tight">
               <span class="text-blue-600">Metriche</span> Chiave
            </h3>
            
            <div class="grid grid-cols-1 gap-4">
                <!-- Max Price Tile -->
                <div class="flex items-center justify-between p-5 bg-gray-50 dark:bg-gray-800/50 rounded-2xl border border-transparent hover:border-gray-200 dark:hover:border-gray-750 transition-colors">
                    <div>
                      <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">Massimo</p>
                      <p class="text-xl font-black text-gray-900 dark:text-white">{{ product.max_price || '-' }}<small class="text-xs ml-0.5 italic">€</small></p>
                    </div>
                    <div class="p-3 bg-rose-50 dark:bg-rose-900/20 rounded-xl">
                      <svg class="w-5 h-5 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                    </div>
                </div>
                <!-- Min Price Tile -->
                <div class="flex items-center justify-between p-5 bg-emerald-50/50 dark:bg-emerald-900/10 rounded-2xl border border-emerald-100/50 dark:border-emerald-800/30">
                    <div>
                      <p class="text-[10px] font-black text-emerald-600/70 dark:text-emerald-500/70 uppercase tracking-widest mb-1 font-bold">Minimo Storico</p>
                      <p class="text-xl font-black text-emerald-600 dark:text-emerald-400">{{ product.min_price || '-' }}<small class="text-xs ml-0.5 italic">€</small></p>
                    </div>
                    <div class="p-3 bg-emerald-100 dark:bg-emerald-800/40 rounded-xl">
                      <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6"></path></svg>
                    </div>
                </div>
                <!-- Avg Price Tile -->
                <div class="flex items-center justify-between p-5 bg-blue-50/50 dark:bg-blue-900/10 rounded-2xl border border-blue-100/50 dark:border-blue-800/30">
                    <div>
                      <p class="text-[10px] font-black text-blue-600/70 dark:text-blue-500/70 uppercase tracking-widest mb-1">Prezzo Medio</p>
                      <p class="text-xl font-black text-blue-600 dark:text-blue-400">{{ product.average_price || '-' }}<small class="text-xs ml-0.5 italic">€</small></p>
                    </div>
                    <div class="p-3 bg-blue-100 dark:bg-blue-800/40 rounded-xl">
                      <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                    </div>
                </div>
            </div>
          </div>

          <!-- Price Recommendation Tile -->
          <div class="p-8 rounded-[2.5rem] bg-gradient-to-br from-blue-600 to-indigo-700 text-white shadow-xl shadow-blue-500/20">
            <h4 class="text-lg font-black uppercase tracking-widest mb-4">Analisi Convenienza</h4>
            <p v-if="product.price <= product.average_price" class="text-blue-50 font-medium leading-relaxed">
              Il prezzo attuale è <span class="font-black underline decoration-2 underline-offset-4 tracking-tight">OTTIMO</span>. È inferiore alla media storica, rendendo questo un momento favorevole per l'acquisto.
            </p>
            <p v-else class="text-blue-50 font-medium leading-relaxed">
              Il prezzo è leggermente sopra la media. Ti consigliamo di attivare un avviso per monitorare un possibile ribasso a breve.
            </p>
          </div>
        </div>

        <!-- Right: Main Chart (8 cols) -->
        <div class="lg:col-span-8">
           <div class="bg-white dark:bg-gray-900 rounded-[2.5rem] shadow-sm border border-gray-100 dark:border-gray-800 overflow-hidden">
             <div class="p-8 border-b border-gray-50 dark:border-gray-800 flex items-center justify-between">
               <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Storico <span class="text-blue-600">Prezzi</span></h3>
               <div class="flex gap-2">
                  <span class="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></span>
               </div>
             </div>
             <div class="p-4 md:p-8">
               <ChartPage v-if="product && product.price_history" :priceHistory="product.price_history" />
             </div>
           </div>
        </div>
      </div>

      <!-- Advanced Details Section -->
      <div v-if="product && product.details?.length" class="mt-16">
        <div class="flex items-center gap-4 mb-8">
          <h3 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">
              Scheda <span class="text-emerald-500">Tecnica</span>
          </h3>
          <div class="h-[2px] flex-1 bg-gray-100 dark:bg-gray-800"></div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="(detail, index) in product.details" :key="index" 
                 class="group relative overflow-hidden p-6 bg-white dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 hover:border-emerald-200 dark:hover:border-emerald-900/50 transition-all hover:shadow-lg hover:shadow-emerald-500/5">
                <p class="text-[10px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-2 transition-colors group-hover:text-emerald-500">
                    {{ Object.keys(detail)[0] }}
                </p>
                <p class="text-sm font-bold text-gray-900 dark:text-white leading-relaxed">
                    {{ Object.values(detail)[0] }}
                </p>
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
