<template>
  <div 
    @click="$router.push(`/products/${item.asin}`)"
    class="group relative bg-white/70 dark:bg-gray-800/70 backdrop-blur-md rounded-[2rem] border border-gray-100 dark:border-gray-700 p-6 shadow-xl hover:shadow-2xl hover:-translate-y-1 cursor-pointer transition-all duration-500 overflow-hidden flex flex-col h-full"
  >
    <!-- Header: Recommendation Badge -->
    <div class="flex justify-between items-start mb-6">
      <div 
        class="px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest shadow-lg transition-transform group-hover:scale-110"
        :class="recommendationClasses"
      >
        {{ item.recommendation }}
      </div>
      <div class="flex items-center gap-1.5">
        <div class="w-2 h-2 rounded-full animate-pulse" :class="trendColor"></div>
        <span class="text-[10px] uppercase font-bold text-gray-400 dark:text-gray-500 tracking-wider">{{ item.trend === 'down' ? 'In ribasso' : (item.trend === 'up' ? 'In rialzo' : 'Stabile') }}</span>
      </div>
    </div>

    <!-- Product Image & Title -->
    <div class="flex gap-4 mb-6">
      <div class="w-16 h-16 rounded-2xl bg-gray-50 dark:bg-gray-900 p-2 flex-shrink-0 border border-gray-100 dark:border-gray-700">
        <img :src="item.image_url" :alt="item.title" class="w-full h-full object-contain mix-blend-multiply dark:mix-blend-normal">
      </div>
      <div class="flex-grow min-w-0">
        <h3 class="text-xs font-black text-gray-900 dark:text-white line-clamp-2 leading-tight mb-1">{{ item.title }}</h3>
        <p class="text-[10px] font-bold text-blue-500 uppercase tracking-tight">{{ item.category }}</p>
      </div>
    </div>

    <!-- AI Reason -->
    <div class="bg-blue-50/50 dark:bg-blue-900/20 rounded-2xl p-4 mb-6 relative overflow-hidden">
        <div class="absolute top-0 right-0 p-2 opacity-10">
            <svg class="w-8 h-8 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
        </div>
        <p class="text-[11px] leading-relaxed text-gray-700 dark:text-gray-300 font-medium italic">"{{ item.reason }}"</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-3 mt-auto">
      <div class="p-3 rounded-xl bg-gray-50/50 dark:bg-gray-900/40 border border-gray-100/50 dark:border-gray-800">
        <p class="text-[9px] uppercase text-gray-400 font-extrabold mb-1">Attuale</p>
        <p class="text-base font-black text-gray-900 dark:text-white">{{ item.current_price }}€</p>
      </div>
      <div class="p-3 rounded-xl bg-gray-50/50 dark:bg-gray-900/40 border border-gray-100/50 dark:border-gray-800">
        <p class="text-[9px] uppercase text-gray-400 font-extrabold mb-1">Volatilità</p>
        <p class="text-base font-black" :class="volatilityColor">{{ item.volatility }}%</p>
      </div>
    </div>

    <!-- Drop Probability / Risk -->
    <div class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between">
      <div class="flex flex-col">
        <span class="text-[9px] uppercase font-bold text-gray-400 tracking-widest">Rischio</span>
        <span class="text-[11px] font-black" :class="riskColor">{{ item.risk_level }}</span>
      </div>
      <div class="text-right flex flex-col items-end">
        <span class="text-[9px] uppercase font-bold text-gray-400 tracking-widest">Probab. Calo</span>
         <div class="w-20 h-1.5 bg-gray-100 dark:bg-gray-700 rounded-full mt-1 overflow-hidden">
            <div 
              class="h-full bg-gradient-to-r from-blue-400 to-indigo-500 transition-all duration-1000" 
              :style="{ width: item.chance_of_drop + '%' }"
            ></div>
         </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['item'],
  computed: {
    recommendationClasses() {
      switch(this.item.recommendation) {
        case 'BUY': return 'bg-emerald-500 text-white shadow-emerald-500/30';
        case 'WAIT': return 'bg-rose-500 text-white shadow-rose-500/30';
        case 'HOLD': return 'bg-amber-500 text-white shadow-amber-500/30';
        default: return 'bg-gray-500 text-white';
      }
    },
    trendColor() {
      if (this.item.trend === 'down') return 'bg-emerald-400';
      if (this.item.trend === 'up') return 'bg-rose-400';
      return 'bg-gray-400';
    },
    volatilityColor() {
      if (this.item.volatility > 20) return 'text-rose-500';
      if (this.item.volatility > 10) return 'text-amber-500';
      return 'text-emerald-500';
    },
    riskColor() {
       if (this.item.risk_level === 'Alto') return 'text-rose-500';
       if (this.item.risk_level === 'Medio') return 'text-amber-500';
       return 'text-emerald-500';
    }
  }
}
</script>
