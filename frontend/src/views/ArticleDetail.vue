<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 pb-20 antialiased selection:bg-blue-100 selection:text-blue-700">
    <div v-if="loading" class="pt-20 text-center animate-pulse">
      <div class="h-8 w-64 bg-gray-200 dark:bg-gray-800 mx-auto rounded mb-4"></div>
      <div class="max-w-2xl mx-auto h-40 bg-gray-200 dark:bg-gray-800 rounded"></div>
    </div>
    
    <div v-else-if="!article" class="pt-20 text-center">
      <h1 class="text-2xl font-bold dark:text-white">Articolo non trovato</h1>
      <router-link to="/blog" class="text-blue-500 hover:underline mt-4 inline-block">Torna al Blog</router-link>
    </div>

    <div v-else class="mx-auto max-w-screen-xl px-4 pt-12 pb-24">
      <!-- Article Header -->
      <nav class="mb-14 flex items-center justify-center text-[10px] font-black text-gray-400 uppercase tracking-[0.4em] gap-4">
        <router-link to="/blog" class="hover:text-blue-500 transition-colors">Blog</router-link>
        <span class="opacity-20">/</span>
        <span class="text-gray-900 dark:text-white truncate max-w-[400px]">{{ article.title }}</span>
      </nav>

      <div class="max-w-6xl mx-auto">
        <!-- Main Title -->
        <h1 class="text-3xl md:text-5xl font-black text-gray-900 dark:text-white mb-12 leading-[1.1] tracking-tighter text-center">
          {{ article.title }}
        </h1>

        <!-- PREMIUM PRODUCT HERO SECTION (Solo per singolo prodotto) -->
        <div v-if="!isMultiProduct && article.product" class="mb-20">
          <div class="relative p-1 rounded-[4rem] bg-gray-100 dark:bg-gray-800 shadow-2xl overflow-hidden group">
            <div class="relative bg-white dark:bg-gray-950 rounded-[3.8rem] p-8 md:p-14 border border-gray-100 dark:border-gray-800">
              <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
                
                <!-- Product Image + Floating Recommendation -->
                <div class="lg:col-span-5 relative">
                  <div class="aspect-square bg-white dark:bg-gray-950 rounded-[3rem] p-10 flex items-center justify-center relative border border-gray-100 dark:border-gray-800 group-hover:scale-105 transition-transform duration-700">
                    <img :src="article.product?.image_url || article.amazon_product_image_url" class="w-full h-full object-contain" :alt="article.title" />
                    
                    <!-- Floating Recommendation Badge -->
                    <div v-if="article.product?.analysis" class="absolute -top-4 -right-4">
                       <div class="px-8 py-3 rounded-2xl text-xs font-black uppercase tracking-widest text-white shadow-2xl scale-110" :class="recommendationClasses">
                         AI: {{ article.product.analysis.recommendation }}
                       </div>
                    </div>
                  </div>
                </div>

                <!-- Product Content -->
                <div class="lg:col-span-7 space-y-8">
                  <div class="text-center lg:text-left">
                    <div class="text-[10px] font-black text-blue-600 dark:text-blue-400 uppercase tracking-[0.3em] mb-3">
                       Prezzo Attuale Amazon
                    </div>
                    <div class="text-6xl font-black dark:text-white tracking-tighter inline-flex items-start">
                      <span class="text-2xl mt-2 mr-1">€</span>
                      {{ article.product?.price || article.amazon_product_price }}
                    </div>
                  </div>

                  <!-- Integrated AI Advice (Intuitive explanation) -->
                  <div v-if="article.product?.analysis" class="p-6 bg-gray-50 dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 space-y-4">
                     <p class="text-gray-900 dark:text-white font-bold leading-relaxed text-lg italic">
                        "{{ article.product.analysis.reason }}"
                     </p>
                     <div class="flex items-center gap-6">
                        <div class="flex-1 space-y-1.5">
                           <div class="flex justify-between text-[10px] uppercase font-black tracking-widest text-gray-400">
                             <span>Prezzo Minimo</span>
                             <span>Prezzo Massimo</span>
                           </div>
                           <!-- Price Range Bar -->
                           <div class="relative h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                              <div 
                                class="absolute h-full bg-gradient-to-r from-emerald-500 via-blue-500 to-rose-500"
                                :style="{ 
                                  left: 0,
                                  right: 0
                                }"
                              ></div>
                              <!-- Current Price Marker -->
                              <div 
                                class="absolute top-0 w-2 h-full bg-white shadow-md border border-gray-300 pointer-events-none"
                                :style="{ 
                                  left: calculatePricePosition(article.product) + '%' 
                                }"
                              ></div>
                           </div>
                           <div class="flex justify-between text-[11px] font-black dark:text-white">
                              <span>{{ article.product.min_price }}€</span>
                              <span class="text-blue-500">Oggi: {{ article.product.price }}€</span>
                              <span>{{ article.product.max_price }}€</span>
                           </div>
                        </div>
                     </div>
                  </div>

                  <!-- CTA Section -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                    <a :href="affiliateUrl" target="_blank" rel="nofollow" class="flex items-center justify-center gap-3 px-8 py-5 bg-gradient-to-r from-orange-500 to-orange-600 text-white font-black rounded-2xl shadow-xl shadow-orange-500/30 hover:-translate-y-1 transition-all uppercase tracking-[0.2em] text-[11px] group">
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                      Vedi su Amazon
                    </a>
                    <router-link :to="`/products/${article.asin}`" class="flex items-center justify-center px-8 py-5 bg-blue-600 hover:bg-blue-700 text-white font-black rounded-2xl shadow-xl shadow-blue-500/20 hover:-translate-y-1 transition-all uppercase tracking-[0.2em] text-[11px]">
                      Grafici & Alert
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Meta info -->
        <div class="flex items-center gap-4 mb-20 px-8">
           <div class="w-12 h-12 rounded-2xl bg-gray-900 flex items-center justify-center text-white font-black text-sm shadow-xl">AI</div>
           <div>
             <div class="text-[10px] font-black text-gray-900 dark:text-white uppercase tracking-[0.2em]">Data Analysis Insights</div>
             <div class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{{ formatDate(article.published_at) }}</div>
           </div>
        </div>

        <!-- Main Content (PROSE) -->
        <div class="prose prose-2xl prose-blue dark:prose-invert max-w-none 
                    prose-headings:text-gray-900 dark:prose-headings:text-white 
                    prose-headings:font-black prose-headings:tracking-tighter
                    prose-p:text-gray-600/90 dark:prose-p:text-gray-400 
                    prose-p:leading-[1.9] prose-p:mb-10
                    prose-strong:text-gray-900 dark:prose-strong:text-white
                    prose-img:rounded-[3rem] prose-img:shadow-2xl">
          
          <template v-if="isMultiProduct">
            <template v-for="(chunk, idx) in parsedContentChunks" :key="idx">
               <!-- Parsed HTML Chunk -->
               <div v-if="chunk.type === 'html'" v-html="chunk.content"></div>
               
               <!-- Injected Product Feature Widget -->
               <div v-else-if="chunk.type === 'product'" class="not-prose my-16 p-6 sm:p-10 bg-white dark:bg-gray-950 rounded-[3rem] border border-gray-100 dark:border-gray-800 shadow-2xl relative overflow-hidden group">
                  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
                    
                    <!-- Image Area -->
                    <div class="lg:col-span-4 relative flex items-center justify-center p-6 bg-gray-50 dark:bg-gray-900 rounded-[2rem] aspect-square">
                      <img :src="chunk.product.image_url" class="w-full h-full object-contain max-h-[250px] group-hover:scale-105 transition-transform duration-500" />
                    </div>

                    <!-- Details Area -->
                    <div class="lg:col-span-8 flex flex-col justify-center space-y-6">
                      <div>
                        <div class="text-xs font-black text-blue-600 dark:text-blue-400 uppercase tracking-widest mb-2">Prezzo Dinamico</div>
                        <div class="text-5xl font-black text-gray-900 dark:text-white tracking-tighter">€{{ chunk.product.price }}</div>
                      </div>
                      
                      <!-- AI Advice inline -->
                      <div v-if="chunk.product.analysis" class="p-6 bg-gray-50 dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 space-y-5">
                         <p class="text-gray-900 dark:text-white font-bold text-sm italic leading-relaxed">
                            "{{ chunk.product.analysis.reason }}"
                         </p>
                         <div class="space-y-1.5">
                               <div class="flex justify-between text-[10px] uppercase font-black tracking-widest text-gray-400">
                                 <span>Minimo</span>
                                 <span>Massimo</span>
                               </div>
                               <!-- Price Range Bar -->
                               <div class="relative h-2 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                                  <div class="absolute h-full bg-gradient-to-r from-emerald-500 via-blue-500 to-rose-500" style="left: 0; right: 0;"></div>
                                  <div class="absolute top-0 w-2 h-full bg-white shadow-md border border-gray-300 pointer-events-none" :style="{ left: calculatePricePosition(chunk.product) + '%' }"></div>
                               </div>
                               <div class="flex justify-between text-[11px] font-black dark:text-white">
                                  <span>{{ chunk.product.min_price }}€</span>
                                  <span class="text-blue-500">Oggi: {{ chunk.product.price }}€</span>
                                  <span>{{ chunk.product.max_price }}€</span>
                               </div>
                         </div>
                      </div>

                      <!-- Purchase Button -->
                      <div class="pt-4">
                        <a :href="chunk.url" target="_blank" rel="nofollow" class="flex items-center justify-center gap-3 w-full md:w-auto px-8 py-5 bg-gradient-to-r from-orange-400 to-orange-600 text-white font-black rounded-2xl shadow-xl shadow-orange-500/20 hover:-translate-y-1 transition-all uppercase tracking-[0.2em] text-[11px]">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                          Acquista Ora a {{ chunk.product.price }}€
                        </a>
                      </div>

                    </div>
                  </div>
               </div>
            </template>
          </template>
          
          <div v-else v-html="renderedContent"></div>

        </div>

        <!-- Technical Specs Section (Solo Singolo Prodotto) -->
        <div v-if="!isMultiProduct" class="mt-32 space-y-24">
          <!-- Specs -->
          <div v-if="article.product?.details?.length">
             <div class="text-center mb-12">
               <h3 class="text-4xl font-black text-gray-900 dark:text-white tracking-widest uppercase">SCHEDA <span class="text-emerald-500">TECNICA</span></h3>
               <div class="w-16 h-1 bg-emerald-500 mx-auto mt-4 rounded-full"></div>
             </div>
             <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div v-for="(detail, index) in article.product.details" :key="index" class="p-6 bg-white dark:bg-gray-950 rounded-3xl border border-gray-100 dark:border-gray-800 shadow-sm flex items-center justify-between">
                  <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ Object.keys(detail)[0] }}</span>
                  <span class="text-sm font-bold dark:text-white text-right max-w-[60%]">{{ Object.values(detail)[0] }}</span>
                </div>
             </div>
          </div>

          <!-- Chart -->
          <div v-if="article.product?.price_history">
            <div class="text-center mb-12">
              <h3 class="text-4xl font-black text-gray-900 dark:text-white tracking-widest uppercase">ANALISI <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">PREZZI</span></h3>
              <div class="w-16 h-1 bg-blue-600 mx-auto mt-4 rounded-full"></div>
            </div>
            <div class="bg-white dark:bg-gray-950 p-10 rounded-[3rem] border border-gray-100 dark:border-gray-800 shadow-2xl">
              <ChartPage :priceHistory="article.product.price_history" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ChartPage from "../components/ChartPage.vue";

export default {
  name: "ArticleDetail",
  components: { ChartPage },
  data() {
    return {
      article: null,
      loading: true
    };
  },
  computed: {
    isMultiProduct() {
      return this.article && this.article.asins && this.article.asins.length > 0;
    },
    parsedContentChunks() {
      if (!this.article) return [];
      if (!this.article.content_html) return [{ type: 'html', content: "<div class='py-20 text-center'><div class='inline-block animate-bounce mb-4 text-4xl'>✍️</div><p class='text-gray-400 font-bold'>L'AI sta ancora scrivendo o c'è stato un errore nel recupero del testo.</p></div>" }];

      const affiliateBaseUrl = `${process.env.VUE_APP_API_BASE_URL}/analytics/r/`;
      let chunks = [];

      if (this.isMultiProduct) {
        // Regex match {{AMAZON_BUTTON_XYZ}} oppure {AMAZON_BUTTON_XYZ}
        const regex = /\{{1,2}AMAZON_BUTTON_([A-Z0-9]+)\}{1,2}/g;
        let lastIndex = 0;
        let match;

        let html = this.article.content_html;
        while ((match = regex.exec(html)) !== null) {
          if (match.index > lastIndex) {
            chunks.push({ type: 'html', content: html.substring(lastIndex, match.index) });
          }
          
          const asin = match[1];
          const product = this.article.products?.find(p => p.asin === asin);
          
          if (product) {
              chunks.push({ type: 'product', product: product, url: affiliateBaseUrl + asin });
          } else {
              // fallback
              chunks.push({ type: 'html', content: `<a href="${affiliateBaseUrl + asin}" target="_blank" rel="nofollow" class="not-prose inline-block mt-4 px-6 py-3 bg-orange-500 text-white font-bold rounded-xl shadow no-underline hover:bg-orange-600">Vedi su Amazon</a>` });
          }
          
          lastIndex = regex.lastIndex;
        }

        if (lastIndex < html.length) {
          chunks.push({ type: 'html', content: html.substring(lastIndex) });
        }
      }
      return chunks;
    },
    renderedContent() {
      // Usato solo per articolo SINGOLO prodotto
      if (this.isMultiProduct || !this.article) return "";
      if (!this.article.content_html) return "<div class='py-20 text-center'><div class='inline-block animate-bounce mb-4 text-4xl'>✍️</div><p class='text-gray-400 font-bold'>L'AI sta scrivendo...</p></div>";
      
      let html = this.article.content_html;
      const affiliateUrl = this.affiliateUrl;
      const buttonHtml = `
        <div class="my-10 flex justify-center">
            <a href="${affiliateUrl}" target="_blank" rel="nofollow" class="not-prose inline-flex items-center px-12 py-5 bg-gradient-to-r from-orange-400 to-orange-600 text-white font-black rounded-2xl shadow-2xl hover:scale-105 transition-transform uppercase tracking-widest text-sm no-underline group hover:text-white">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                Acquista al Miglior Prezzo
            </a>
        </div>
      `;
      html = html.replace(/\{{1,2}AMAZON_BUTTON\}{1,2}/g, buttonHtml);
      html = html.replace(/\{{1,2}AMAZON_LINK\}{1,2}/g, affiliateUrl);
      
      const currentPrice = this.article.product?.price || this.article.amazon_product_price;
      html = html.replace(/\{{1,2}\s*CURRENT_PRICE\s*\}{1,2}/g, currentPrice);
      
      return html;
    },
    affiliateUrl() {
      if (!this.article) return "#";
      return `${process.env.VUE_APP_API_BASE_URL}/analytics/r/${this.article.asin}`;
    },
    recommendationClasses() {
      const rec = this.article.product?.analysis?.recommendation;
      switch(rec) {
        case 'BUY': return 'bg-emerald-500 text-white';
        case 'WAIT': return 'bg-rose-500 text-white';
        case 'HOLD': return 'bg-amber-500 text-white';
        default: return 'bg-gray-500 text-white';
      }
    }
  },
  async created() {
    const slug = this.$route.params.slug;
    try {
      const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/articles/${slug}`);
      if (response.ok) {
        this.article = await response.json();
        this.updateMetaTags();
        this.injectJsonLd();
      }
    } catch (e) {
      console.error("Error loading article:", e);
    } finally {
      this.loading = false;
    }
  },
  beforeUnmount() {
    this.removeJsonLd();
  },
  methods: {
    updateMetaTags() {
      if (!this.article) return;
      document.title = `${this.article.title} | PriceHub.it`;
      let metaDesc = document.querySelector('meta[name="description"]');
      if (!metaDesc) {
        metaDesc = document.createElement('meta');
        metaDesc.setAttribute('name', 'description');
        document.head.appendChild(metaDesc);
      }
      metaDesc.setAttribute('content', this.article.meta_description || this.article.title);
    },
    injectJsonLd() {
      this.removeJsonLd();
      const script = document.createElement('script');
      script.type = 'application/ld+json';
      script.id = 'json-ld-article';
      const product = this.article.product;
      const jsonLd = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": product?.title || this.article.amazon_product_title,
        "image": [product?.image_url || this.article.amazon_product_image_url],
        "description": this.article.meta_description,
        "sku": this.article.asin,
        "offers": {
          "@type": "Offer",
          "url": window.location.href,
          "priceCurrency": "EUR",
          "price": product?.price || this.article.amazon_product_price,
          "availability": "https://schema.org/InStock"
        }
      };
      script.text = JSON.stringify(jsonLd);
      document.head.appendChild(script);
    },
    removeJsonLd() {
      const script = document.getElementById('json-ld-article');
      if (script) script.remove();
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      return new Date(dateStr).toLocaleDateString("it-IT", {
        day: "numeric",
        month: "long",
        year: "numeric"
      });
    },
    calculatePricePosition(product) {
      if (!product || !product.min_price || !product.max_price || !product.price) return 0;
      const range = product.max_price - product.min_price;
      if (range === 0) return 50;
      const position = ((product.price - product.min_price) / range) * 100;
      return Math.min(Math.max(position, 0), 100);
    }
  }
};
</script>

<style scoped>
:deep(h2) {
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
  color: #111827; /* dark text-gray-900 */
}
.dark :deep(h2) {
  color: #f9fafb; /* text-gray-50 */
}
</style>
