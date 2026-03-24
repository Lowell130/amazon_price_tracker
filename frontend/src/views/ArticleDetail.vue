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

    <div v-else class="mx-auto max-w-screen-lg px-4 pt-12">
      <!-- Article Header -->
      <nav class="mb-8 flex items-center text-xs font-bold text-gray-400 uppercase tracking-widest gap-2">
        <router-link to="/blog" class="hover:text-blue-500 transition-colors">Blog</router-link>
        <span>/</span>
        <span class="text-gray-900 dark:text-white truncate max-w-[200px] sm:max-w-[400px]">{{ article.title }}</span>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12">
        <!-- Main Content Area (Left/Center) -->
        <div class="lg:col-span-8">
          <h1 class="text-4xl md:text-5xl font-black text-gray-900 dark:text-white mb-6 leading-tight tracking-tight">
            {{ article.title }}
          </h1>

          <!-- Meta Info -->
          <div class="flex items-center gap-4 mb-10 py-6 border-y border-gray-100 dark:border-gray-800">
            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-black text-lg shadow-lg">
              AI
            </div>
            <div>
              <div class="text-sm font-bold text-gray-900 dark:text-white">Autore: AI Insights</div>
              <div class="text-xs text-gray-500">{{ formatDate(article.published_at) }}</div>
            </div>
          </div>

          <!-- AI INSIGHT BOX (Analisi Convenienza) -->
          <div v-if="article.product?.analysis" class="mb-12 p-8 rounded-3xl bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-xl relative overflow-hidden group">
            <div class="flex items-start justify-between mb-6">
              <div 
                class="px-6 py-2 rounded-2xl text-xs font-black uppercase tracking-[0.2em] shadow-lg"
                :class="recommendationClasses"
              >
                {{ article.product.analysis.recommendation }}
              </div>
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-full animate-pulse" :class="trendColor"></div>
                <span class="text-[10px] uppercase font-black text-gray-400 tracking-widest">{{ trendLabel }}</span>
              </div>
            </div>
            
            <div class="bg-blue-50/30 dark:bg-blue-900/10 rounded-2xl p-6 mb-8 relative">
              <p class="text-lg leading-relaxed text-gray-800 dark:text-gray-200 font-bold italic tracking-tight italic">
                "{{ article.product.analysis.reason }}"
              </p>
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div>
                <span class="text-[10px] uppercase font-black text-gray-400 tracking-widest block mb-2">Rischio</span>
                <span class="text-sm font-black" :class="riskColor">{{ article.product.analysis.risk_level }}</span>
              </div>
              <div class="text-right">
                <span class="text-[10px] uppercase font-black text-gray-400 tracking-widest block mb-2">Probab. Calo</span>
                <div class="flex items-center justify-end gap-3">
                  <div class="w-24 h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-blue-500 to-indigo-600" :style="{ width: article.product.analysis.chance_of_drop + '%' }"></div>
                  </div>
                  <span class="text-sm font-black dark:text-white">{{ article.product.analysis.chance_of_drop }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Main Article Content (AI Generated) -->
          <div class="prose prose-lg dark:prose-invert max-w-none 
                      prose-headings:font-black prose-headings:tracking-tight
                      prose-h1:text-4xl prose-h2:text-3xl
                      prose-p:text-gray-600 dark:prose-p:text-gray-300
                      prose-a:text-blue-600 dark:prose-a:text-blue-400 prose-a:font-bold
                      prose-strong:text-gray-900 dark:prose-strong:text-white">
            <div v-html="renderedContent"></div>
          </div>

          <!-- Price History Chart -->
          <div v-if="article.product?.price_history" class="mt-16 bg-white dark:bg-gray-900 rounded-3xl border border-gray-100 dark:border-gray-800 overflow-hidden shadow-xl">
            <div class="p-8 border-b border-gray-50 dark:border-gray-800">
              <h3 class="text-2xl font-black text-gray-900 dark:text-white tracking-tight">Storico <span class="text-blue-600">Prezzi</span></h3>
            </div>
            <div class="p-6">
              <ChartPage :priceHistory="article.product.price_history" />
            </div>
          </div>

          <!-- Tech Specs Grid -->
          <div v-if="article.product?.details?.length" class="mt-16">
            <h3 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight mb-8">Scheda <span class="text-emerald-500">Tecnica</span></h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div v-for="(detail, index) in article.product.details" :key="index" class="p-5 bg-white dark:bg-gray-900 rounded-2xl border border-gray-100 dark:border-gray-800">
                <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ Object.keys(detail)[0] }}</p>
                <p class="text-sm font-bold dark:text-white leading-relaxed">{{ Object.values(detail)[0] }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar / Floating Data -->
        <div class="lg:col-span-4 space-y-8">
          <!-- Buy Now Product Card -->
          <div class="sticky top-24 p-8 rounded-[2.5rem] bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-2xl">
            <div class="aspect-square bg-white dark:bg-gray-800 rounded-2xl p-6 mb-8 shadow-inner border border-gray-50 dark:border-gray-700">
              <img :src="article.product?.image_url || article.amazon_product_image_url || 'https://placehold.co/400x400?text=Amazon+Product'" class="w-full h-full object-contain" :alt="article.title" />
            </div>
            
            <div class="space-y-6">
              <div class="text-center">
                <span class="text-[10px] uppercase font-black text-gray-400 tracking-widest block mb-2">Prezzo Attuale su Amazon</span>
                <div class="text-4xl font-black dark:text-white tracking-tighter">€{{ article.product?.price || article.amazon_product_price }}</div>
              </div>

              <!-- Metriche Chiave -->
              <div v-if="article.product" class="space-y-3 pt-6 border-t border-gray-100 dark:border-gray-800">
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold text-gray-400 uppercase">Minimo</span>
                  <span class="text-sm font-black text-emerald-500">{{ article.product.min_price }}€</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold text-gray-400 uppercase">Massimo</span>
                  <span class="text-sm font-black text-rose-500">{{ article.product.max_price }}€</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-[10px] font-bold text-gray-400 uppercase">Media</span>
                  <span class="text-sm font-black text-blue-500">{{ article.product.average_price }}€</span>
                </div>
              </div>

              <a :href="affiliateUrl" target="_blank" rel="nofollow" class="block w-full py-5 bg-orange-500 hover:bg-orange-600 text-white text-center font-black rounded-2xl shadow-lg shadow-orange-500/30 transition-all uppercase tracking-widest text-sm active:scale-95">
                Vedi su Amazon
              </a>
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
    renderedContent() {
      if (!this.article) return "";
      if (!this.article.content_html) return "<div class='py-20 text-center'><div class='inline-block animate-bounce mb-4 text-4xl'>✍️</div><p class='text-gray-400 font-bold'>L'AI sta ancora scrivendo o c'è stato un errore nel recupero del testo.</p></div>";
      
      let html = this.article.content_html;
      const affiliateUrl = this.affiliateUrl;
      
      const buttonHtml = `
        <div class="my-10 flex justify-center">
            <a href="${affiliateUrl}" target="_blank" rel="nofollow" class="inline-flex items-center px-12 py-5 bg-gradient-to-r from-orange-400 to-orange-600 text-white font-black rounded-2xl shadow-2xl hover:scale-105 transition-transform uppercase tracking-widest text-sm no-underline group">
                <svg class="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                Acquista al Miglior Prezzo
            </a>
        </div>
      `;
      
      html = html.replace(/\{AMAZON_BUTTON\}/g, buttonHtml);
      html = html.replace(/\{AMAZON_LINK\}/g, affiliateUrl);
      
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
    },
    trendColor() {
      const trend = this.article.product?.analysis?.trend;
      if (trend === 'down') return 'bg-emerald-400';
      if (trend === 'up') return 'bg-rose-400';
      return 'bg-gray-400';
    },
    trendLabel() {
      const trend = this.article.product?.analysis?.trend;
      if (trend === 'down') return 'In ribasso';
      if (trend === 'up') return 'In rialzo';
      return 'Stabile';
    },
    riskColor() {
      const risk = this.article.product?.analysis?.risk_level;
      if (risk === 'Alto') return 'text-rose-500';
      if (risk === 'Medio') return 'text-amber-500';
      return 'text-emerald-500';
    }
  },
  async created() {
    const slug = this.$route.params.slug;
    try {
      const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/articles/${slug}`);
      if (response.ok) {
        this.article = await response.json();
      }
    } catch (e) {
      console.error("Error loading article:", e);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return "";
      return new Date(dateStr).toLocaleDateString("it-IT", {
        day: "numeric",
        month: "long",
        year: "numeric"
      });
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

