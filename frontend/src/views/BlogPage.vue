<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12 antialiased">
    <!-- Hero / Header -->
    <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 pt-16 pb-12 mb-12">
      <div class="mx-auto max-w-screen-xl px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-black text-gray-900 dark:text-white mb-4 tracking-tight">
          Recensioni Esperte & <span class="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">Offerte Amazon</span>
        </h1>
        <p class="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
          Scopri le migliori occasioni selezionate dai nostri esperti e analizzate con intelligenza artificiale per garantirti il miglior prezzo.
        </p>
      </div>
    </div>

    <div class="mx-auto max-w-screen-xl px-4">
      <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <div v-for="i in 6" :key="i" class="bg-white dark:bg-gray-800 rounded-3xl p-6 h-80 animate-pulse border border-gray-100 dark:border-gray-700"></div>
      </div>
      
      <div v-else-if="articles.length === 0" class="text-center py-20">
        <p class="text-gray-400">Nessun articolo pubblicato al momento. Torna a trovarci presto!</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <router-link 
          v-for="article in articles" 
          :key="article.id" 
          :to="'/blog/' + article.slug"
          class="group bg-white dark:bg-gray-800 rounded-[2rem] border border-gray-100 dark:border-gray-700 overflow-hidden shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all duration-500"
        >
          <!-- Image Section -->
          <div class="aspect-[16/10] relative overflow-hidden bg-white dark:bg-gray-900 flex items-center justify-center p-8">
            <img 
              :src="article.amazon_product_image_url || 'https://placehold.co/400x200?text=Amazon+Product'" 
              class="w-full h-full object-contain group-hover:scale-110 transition-transform duration-700 ease-out" 
            />
            <!-- Badges Overlay -->
            <div class="absolute top-4 left-4 flex flex-col gap-2">
              <div v-if="article.amazon_product_price && article.amazon_product_price !== 'N/A'" class="bg-slate-900/90 dark:bg-blue-600/90 backdrop-blur-md text-white text-xs font-black px-4 py-2 rounded-xl shadow-lg border border-white/10">
                €{{ article.amazon_product_price }}
              </div>
            </div>
          </div>

          <!-- Content Section -->
          <div class="p-8">
            <h2 class="text-xl font-black text-gray-900 dark:text-white mb-4 group-hover:text-blue-600 transition-colors line-clamp-2 leading-tight tracking-tight">
              {{ article.title }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-3 mb-8 font-medium leading-relaxed">
              {{ article.meta_description }}
            </p>
            <div class="flex items-center justify-between border-t border-gray-50 dark:border-gray-700 pt-6">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
                <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ formatDate(article.published_at) }}</span>
              </div>
              <span class="text-blue-600 dark:text-blue-400 font-black text-xs uppercase tracking-widest group-hover:translate-x-2 transition-transform inline-flex items-center">
                Leggi tutto <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" /></svg>
              </span>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BlogPage",
  data() {
    return {
      articles: [],
      loading: true
    };
  },
  async created() {
    try {
      const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/articles`);
      if (response.ok) {
        this.articles = await response.json();
      }
    } catch (e) {
      console.error("Error loading articles:", e);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return "";
      return new Date(dateStr).toLocaleDateString("it-IT", {
        day: "numeric",
        month: "short",
        year: "numeric"
      });
    }
  }
};
</script>
