<template>
  <div class="mx-auto max-w-screen-2xl px-4 lg:px-8">
    <!-- Filters Bar (Glassmorphism) -->
    <div class="mb-8 p-5 rounded-3xl border border-white/20 bg-white/60 dark:bg-gray-800/60 backdrop-blur-xl shadow-xl flex flex-wrap items-center gap-4 transition-all duration-300">
      <!-- Search Product -->
      <div class="flex-grow min-w-[240px]">
        <div class="relative group">
          <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-gray-400 group-focus-within:text-blue-500 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            v-model="filters.searchQuery"
            @input="applyFilters"
            type="text"
            placeholder="Cerca per titolo o ASIN..."
            class="block w-full pl-12 pr-4 py-2.5 rounded-2xl border-transparent bg-white/50 dark:bg-gray-700/50 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 focus:bg-white dark:focus:bg-gray-700 transition-all shadow-sm"
          />
        </div>
      </div>

      <!-- Category Filter -->
      <div class="min-w-[180px]">
        <select
          v-model="filters.selectedCategory"
          @change="applyFilters"
          class="block w-full rounded-2xl border-transparent bg-white/50 dark:bg-gray-700/50 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 transition-all shadow-sm"
        >
          <option value="">Tutte le categorie</option>
          <option v-for="category in uniqueCategories" :key="category" :value="category">{{ category }}</option>
        </select>
      </div>

      <!-- Price Range Filter -->
      <div class="min-w-[180px]">
        <select
          v-model="filters.selectedPriceRange"
          @change="applyFilters"
          class="block w-full rounded-2xl border-transparent bg-white/50 dark:bg-gray-700/50 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 transition-all shadow-sm"
        >
          <option value="">Tutti i prezzi</option>
          <option v-for="range in priceRanges" :key="range.label" :value="range.value">{{ range.label }}</option>
        </select>
      </div>

      <!-- Condition Filter -->
      <div class="min-w-[160px]">
        <select
          v-model="filters.selectedCondition"
          @change="applyFilters"
          class="block w-full rounded-2xl border-transparent bg-white/50 dark:bg-gray-700/50 dark:text-white text-sm focus:ring-2 focus:ring-blue-500 transition-all shadow-sm"
        >
          <option value="">Tutte le condizioni</option>
          <option value="Nuovo">Nuovo</option>
          <option value="Usato">Usato</option>
          <option value="Non disponibile">N/A</option>
        </select>
      </div>

      <!-- Coupon Toggle -->
      <label class="flex items-center px-5 py-2.5 rounded-2xl bg-white/40 dark:bg-gray-700/40 border border-white/20 cursor-pointer hover:bg-white/60 transition-colors shadow-sm">
        <input
          type="checkbox"
          v-model="filters.onlyWithCoupon"
          @change="applyFilters"
          class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 transition-all"
        />
        <span class="ml-3 text-sm font-semibold text-gray-700 dark:text-gray-300">Coupon %</span>
      </label>

      <!-- Actions -->
      <div class="flex items-center gap-3">
        <button
          @click="filterFavorites"
          class="p-2.5 rounded-2xl border border-red-100 bg-red-50/50 text-red-500 dark:bg-red-900/20 dark:border-red-900/30 hover:bg-red-500 hover:text-white dark:hover:bg-red-600 transition-all duration-300 shadow-sm"
          title="Mostra Preferiti"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
          </svg>
        </button>
        <button
          @click="clearFilters"
          class="px-5 py-2.5 rounded-2xl border border-gray-100 bg-white/50 text-gray-600 dark:bg-gray-700/50 dark:text-gray-300 text-sm font-bold hover:bg-gray-900 hover:text-white dark:hover:bg-white dark:hover:text-gray-900 transition-all duration-300 shadow-sm"
        >
          Reset
        </button>
      </div>
    </div>

    <!-- Table Container -->
    <div class="rounded-3xl border border-white/20 bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl shadow-2xl overflow-hidden mb-12 transition-all duration-500">
      <SpinnerComp v-if="isLoading" />
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm text-left text-gray-600 dark:text-gray-300">
          <thead class="text-[11px] font-black uppercase text-gray-400 bg-gray-50/50 dark:bg-gray-900/50 dark:text-gray-500 border-b border-gray-100 dark:border-gray-700">
            <tr>
              <th scope="col" class="px-6 py-5">
                <button
                  @click="deleteSelectedProducts"
                  class="flex items-center px-3 py-1.5 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-xl hover:bg-red-500 hover:text-white transition-all duration-300 border border-red-100 dark:border-red-800 shadow-sm"
                >
                  <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  <span>{{ selectedAsins.length }}</span>
                </button>
              </th>
              <th scope="col" class="px-6 py-5 min-w-[280px]">Prodotto</th>
              <th scope="col" class="px-6 py-5">Rating</th>
              <th scope="col" class="px-6 py-5">Stato</th>
              <th scope="col" class="px-6 py-5 cursor-pointer group" @click="sort('coupon_value')">
                <div class="flex items-center group-hover:text-blue-500 transition-colors" :class="{ 'text-blue-500': sortBy === 'coupon_value' }">
                  Coupon
                  <span class="ml-1.5 flex items-center">
                    <svg v-if="sortBy === 'coupon_value'" class="w-3 h-3 transition-transform duration-300" :class="{ 'rotate-180': sortDirection === 'asc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                    <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </div>
              </th>
              <th scope="col" class="px-6 py-5">Alert</th>
              <th scope="col" class="px-6 py-5 cursor-pointer group" @click="sort('category')">
                <div class="flex items-center group-hover:text-blue-500 transition-colors" :class="{ 'text-blue-500': sortBy === 'category' }">
                  Categoria
                  <span class="ml-1.5 flex items-center">
                    <svg v-if="sortBy === 'category'" class="w-3 h-3 transition-transform duration-300" :class="{ 'rotate-180': sortDirection === 'asc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                    <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </div>
              </th>
              <th scope="col" class="px-6 py-5 cursor-pointer group text-right" @click="sort('price')">
                <div class="flex items-center justify-end group-hover:text-blue-500 transition-colors" :class="{ 'text-blue-500': sortBy === 'price' }">
                  Prezzo
                  <span class="ml-1.5 flex items-center">
                    <svg v-if="sortBy === 'price'" class="w-3 h-3 transition-transform duration-300" :class="{ 'rotate-180': sortDirection === 'asc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                    <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </div>
              </th>
              <th scope="col" class="px-6 py-5 cursor-pointer group text-center" @click="sort('DIFF')">
                <div class="flex items-center justify-center group-hover:text-blue-500 transition-colors" :class="{ 'text-blue-500': sortBy === 'DIFF' }">
                  Δ %
                  <span class="ml-1.5 flex items-center">
                    <svg v-if="sortBy === 'DIFF'" class="w-3 h-3 transition-transform duration-300" :class="{ 'rotate-180': sortDirection === 'asc' }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                    <svg v-else class="w-3 h-3 opacity-0 group-hover:opacity-100 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
                  </span>
                </div>
              </th>
              <th scope="col" class="px-6 py-5 text-right">Azioni</th>
            </tr>
          </thead>
          <tbody v-for="product in paginatedProducts" :key="product.asin">
            <tr class="group border-b border-gray-100/50 dark:border-gray-800 hover:bg-blue-50/20 dark:hover:bg-blue-900/5 transition-all duration-300">
              <!-- Checkbox -->
              <td class="px-6 py-5">
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="selectedAsins" :value="product.asin" class="sr-only peer" />
                  <div class="w-9 h-5 bg-gray-200 dark:bg-gray-700 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                </label>
              </td>

              <!-- Product -->
              <td class="px-6 py-5">
                <div class="flex items-center">
                  <div class="h-14 w-14 flex-shrink-0 bg-white dark:bg-gray-700 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-600 p-1.5 group-hover:scale-110 transition-transform duration-500">
                    <img v-if="product.image_url" :src="product.image_url" :alt="product.title" class="h-full w-full object-contain" />
                  </div>
                  <div class="ml-4">
                    <div class="text-[13px] font-bold text-gray-900 dark:text-white truncate max-w-[200px] group-hover:text-blue-600 transition-colors" :title="product.title">
                      {{ product.title }}
                    </div>
                    <div class="text-[10px] font-mono font-medium text-gray-400 uppercase tracking-widest mt-0.5">{{ product.asin }}</div>
                  </div>
                </div>
              </td>

              <!-- Rating -->
              <td class="px-6 py-5">
                <div v-if="product.rating" class="flex items-center px-2 py-1 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg w-fit">
                  <svg class="w-3 h-3 text-yellow-500 mr-1.5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                  <span class="text-xs font-black text-yellow-700 dark:text-yellow-400">{{ product.rating }}</span>
                </div>
                <span v-else class="text-gray-300">-</span>
              </td>

              <!-- Status -->
              <td class="px-6 py-5">
                <span
                  class="inline-flex items-center px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest transition-all"
                  :class="{
                    'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400 ring-1 ring-emerald-200 dark:ring-emerald-800': product.condition === 'Nuovo',
                    'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400 ring-1 ring-amber-200 dark:ring-amber-800': product.condition === 'Usato',
                    'bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-400 ring-1 ring-rose-200 dark:ring-rose-800': product.condition === 'Non disponibile'
                  }"
                >
                  {{ product.condition === 'Nuovo' ? 'Nuovo' : (product.condition === 'Usato' ? 'Usato' : 'N/A') }}
                </span>
              </td>

              <!-- Coupon -->
              <td class="px-6 py-5">
                <div v-if="product.coupon_value" class="flex flex-col">
                  <span class="text-xs font-black text-emerald-600 dark:text-emerald-400">€{{ product.coupon_value }}</span>
                  <span class="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">Coupon</span>
                </div>
                <span v-else class="text-gray-300">-</span>
              </td>

              <!-- Favorite -->
              <td class="px-6 py-5">
                <button @click="toggleFavorite(product)" class="focus:outline-none transition-all hover:scale-125 active:scale-90">
                  <svg v-if="product.is_favorite" class="w-7 h-7 text-red-500 drop-shadow-sm" fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                  <svg v-else class="w-7 h-7 text-gray-200 dark:text-gray-700 hover:text-red-300 transition-colors" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                </button>
              </td>

              <!-- Category -->
              <td class="px-6 py-5">
                <select
                  v-model="product.category"
                  @change="updateProductCategory(product)"
                  class="block w-full py-1.5 px-3 rounded-xl border-transparent bg-gray-50 dark:bg-gray-700/50 dark:text-white text-[11px] font-bold focus:ring-2 focus:ring-blue-500 transition-all cursor-pointer"
                >
                  <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
                </select>
              </td>

              <!-- Price -->
              <td class="px-6 py-5 text-right font-mono">
                <div v-if="product.price" class="text-[15px] font-black text-gray-900 dark:text-white tracking-tighter">€{{ product.price }}</div>
                <div v-else class="text-[10px] font-black text-rose-500 uppercase tracking-widest">N/A</div>
                <div class="text-[10px] text-gray-400 line-through opacity-60" v-if="product.max_price && product.max_price != product.price">€{{ product.max_price }}</div>
              </td>

              <!-- Delta % -->
              <td class="px-6 py-5 text-center font-mono font-bold">
                 <div v-html="calculatePriceDiff(product)"></div>
              </td>

              <!-- Actions -->
              <td class="px-6 py-5 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button @click="viewPriceHistory(product.asin)" class="p-2 rounded-xl bg-blue-50 text-blue-500 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-100 dark:border-blue-900/50 hover:bg-blue-500 hover:text-white transition-all duration-300 shadow-sm" title="Dettagli">
                    <!-- Modern Eye Icon -->
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </button>
                  <button @click.prevent="updateProductPrice(product)" class="p-2 rounded-xl bg-emerald-50 text-emerald-500 dark:bg-emerald-900/30 dark:text-emerald-400 border border-emerald-100 dark:border-emerald-900/50 hover:bg-emerald-500 hover:text-white transition-all duration-300" title="Aggiorna">
                    <svg :class="{ 'animate-spin': loadingProducts[product.asin] }" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                  </button>
                  <button 
                    @click="toggleAccordion(product.asin)" 
                    class="p-2 rounded-xl border transition-all duration-300 focus:outline-none"
                    :class="currentOpenAccordion === product.asin 
                      ? 'bg-blue-600 text-white border-blue-600 shadow-lg shadow-blue-100 dark:shadow-none animate-pulse-subtle' 
                      : 'bg-gray-50/50 text-gray-400 border-gray-100 dark:bg-gray-900/30 dark:text-gray-500 dark:border-gray-800 hover:bg-blue-500 hover:text-white hover:border-blue-500 hover:shadow-lg'"
                  >
                    <svg :class="{ 'rotate-180': currentOpenAccordion === product.asin }" class="w-4 h-4 transition-transform duration-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                  </button>
                </div>
              </td>
            </tr>

            <!-- Accordion Content -->
            <tr v-if="currentOpenAccordion === product.asin">
              <td colspan="10" class="px-8 pt-8 pb-4 bg-gray-50/50 dark:bg-gray-900/30 border-b border-gray-100 dark:border-gray-800 animate-fadeIn text-gray-900 dark:text-white">
                <!-- Product Header Info -->
                <div class="mb-8 flex flex-col md:flex-row items-start md:items-center gap-6 bg-white dark:bg-gray-800/80 p-6 rounded-3xl border border-white/20 shadow-xl backdrop-blur-md">
                  <div class="h-20 w-20 flex-shrink-0 bg-white dark:bg-gray-700 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-600 p-2 group-hover:scale-105 transition-transform duration-500">
                    <img v-if="product.image_url" :src="product.image_url" :alt="product.title" class="h-full w-full object-contain" />
                  </div>
                  <div class="flex-grow">
                    <h2 class="text-2xl font-black text-gray-900 dark:text-white leading-tight mb-2">{{ product.title }}</h2>
                    <div class="flex flex-wrap items-center gap-3">
                      <span class="inline-flex items-center px-3 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-[10px] font-black uppercase tracking-widest rounded-lg border border-blue-100 dark:border-blue-800">
                        ASIN: {{ product.asin }}
                      </span>
                      <span class="inline-flex items-center px-3 py-1 bg-gray-50 dark:bg-gray-700/50 text-gray-500 dark:text-gray-400 text-[10px] font-black uppercase tracking-widest rounded-lg border border-gray-100 dark:border-gray-600">
                        {{ product.category }}
                      </span>
                      <div v-if="product.rating" class="flex items-center px-3 py-1 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-100 dark:border-yellow-800/30">
                        <svg class="w-3.5 h-3.5 text-yellow-500 mr-1.5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                        <span class="text-[11px] font-black text-yellow-700 dark:text-yellow-400">{{ product.rating }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-4 ml-auto">
                    <div class="text-right">
                      <div class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1">Prezzo Attuale</div>
                      <div class="text-2xl font-black text-gray-900 dark:text-white">€{{ product.price }}</div>
                    </div>
                  </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <!-- Details -->
                  <div class="rounded-3xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden shadow-xl">
                    <div class="px-6 py-4 bg-gray-50 dark:bg-gray-900/50 border-b border-gray-100 dark:border-gray-700 flex items-center">
                      <svg class="w-4 h-4 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                      <span class="text-xs font-black uppercase tracking-widest text-gray-500">Specifiche Prodotto</span>
                    </div>
                    <div class="overflow-x-auto max-h-[300px] shadow-inner custom-scrollbar">
                      <table class="w-full text-[12px] text-left">
                        <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                          <tr v-for="(detail, index) in product.details" :key="index" class="hover:bg-gray-50 dark:hover:bg-gray-900/40 transition-colors">
                            <td class="px-6 py-3 font-bold text-gray-900 dark:text-white w-1/3 bg-gray-50/30 dark:bg-gray-900/20">{{ Object.keys(detail)[0] }}</td>
                            <td class="px-6 py-3 text-gray-600 dark:text-gray-400 font-medium">{{ Object.values(detail)[0] }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <!-- Chart -->
                  <div class="flex flex-col">
                    <div class="flex items-center justify-between mb-4">
                      <h3 class="text-xl font-black text-gray-900 dark:text-white flex items-center">
                        <span class="bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 p-2 rounded-xl mr-3">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
                          </svg>
                        </span>
                        Andamento Prezzo
                      </h3>
                      <button @click="viewPriceHistory(product.asin)" class="text-xs font-bold text-blue-500 hover:underline">Vedi dettagli completi &rarr;</button>
                    </div>
                    <div class="h-full">
                      <ChartPage v-if="product && product.price_history" :priceHistory="product.price_history" />
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Premium -->
      <nav class="flex flex-col md:flex-row justify-between items-center px-8 py-6 bg-gray-50/50 dark:bg-gray-900/50 border-t border-gray-100 dark:border-gray-700 gap-4">
        <span class="text-xs font-bold text-gray-500 uppercase tracking-widest">
          Mostrando <span class="text-gray-900 dark:text-white">{{ startIndex + 1 }}-{{ endIndex }}</span> di <span class="text-gray-900 dark:text-white">{{ filteredProducts.length }}</span> prodotti
        </span>
        
        <ul class="flex items-center gap-1.5 h-10">
  <!-- First Button -->
  <li>
    <button
      :disabled="currentPage === 1"
      @click="changePage(1)"
      class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-s-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
    >
      <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m17 16-4-4 4-4m-6 8-4-4 4-4"/>
      </svg>
    </button>
  </li>

  <!-- Previous Button -->
  <li>
    <button
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
      class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
    >
      <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m14 8-4 4 4 4"/>
      </svg>
    </button>
  </li>

  <!-- Dynamic Page Numbers -->
  <li v-for="page in visiblePages" :key="page">
    <button
      @click="changePage(page)"
      :class="{
        'flex items-center justify-center px-3 h-8 leading-tight': true,
        'text-blue-600 border border-gray-300 bg-blue-50 hover:bg-blue-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white': currentPage === page,
        'text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white': currentPage !== page,
      }"
    >
      {{ page }}
    </button>
  </li>

  <!-- Next Button -->
  <li>
    <button
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
      class="flex items-center justify-center px-3 h-8 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
    >
      <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m10 16 4-4-4-4"/>
      </svg>
    </button>
  </li>

  <!-- Last Button -->
  <li>
    <button
      :disabled="currentPage === totalPages"
      @click="changePage(totalPages)"
      class="flex items-center justify-center px-3 h-8 ms-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-e-lg hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-600 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white disabled:opacity-50"
    >
      <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m7 16 4-4-4-4m6 8 4-4-4-4"/>
      </svg>
    </button>
  </li>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script>
// import PriceHistory from "./PriceHistory.vue";
import { fetchWithToken } from "@/api";
import SpinnerComp from "./SpinnerComp.vue";
import ChartPage from "../components/ChartPage.vue";


export default {
  components: { SpinnerComp, ChartPage },
  props: ["products", "categories"],

  data() {
    return {
      localProducts: [], // Copia dei prodotti per il componente
      filteredProducts: [], // Prodotti filtrati
      selectedAsins: [],
      loadingProducts: {}, // Stato di caricamento per i singoli prodotti
      currentOpenAccordion: null, // Tracks the currently open accordion
      isLoading: false,
      currentPage: 1,
      itemsPerPage: 50,
      sortBy: null,
      sortDirection: "asc",
      filters: {
        searchQuery: "",
        selectedCategory: "",
        selectedPriceRange: "",
        selectedCondition: "", // Aggiunto valore predefinito corretto
      },
      priceRanges: [
        { label: "€0 - €10", value: [0, 10] },
        { label: "€10 - €50", value: [10, 50] },
        { label: "€50 - €100", value: [50, 100] },
        { label: "€100 - €300", value: [100, 300] },
        { label: "€300 - €600", value: [300, 600] },
        { label: "€600 - €1000", value: [600, 1000] },
        { label: "€1200+", value: [1200, Infinity] },
      ],
    }
  },


  watch: {
  products: {
    immediate: true,
    handler(newProducts) {
      this.localProducts = [...newProducts]; // Crea una copia dei prodotti
      this.filteredProducts = [...newProducts];
      this.isLoading = newProducts.length === 0;
    },
  },
},


computed: {
  visiblePages() {
    const pages = [];
    const maxVisible = 5; // Numero massimo di pagine visibili
    const total = this.totalPages;

    if (total <= maxVisible) {
      for (let i = 1; i <= total; i++) {
        pages.push(i);
      }
    } else {
      const half = Math.floor(maxVisible / 2);
      let start = Math.max(this.currentPage - half, 1);
      let end = Math.min(start + maxVisible - 1, total);

      if (end - start + 1 < maxVisible) {
        start = Math.max(end - maxVisible + 1, 1);
      }

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      if (start > 1) pages.unshift("...");
      if (end < total) pages.push("...");
    }

    return pages;
  },
    uniqueCategories() {
      return [...new Set(this.products.map((product) => product.category))];
    },
    totalPages() {
      return Math.ceil(this.filteredProducts.length / this.itemsPerPage);
    },
    paginatedProducts() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredProducts.slice(start, end);
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage;
    },
    endIndex() {
      return Math.min(this.startIndex + this.itemsPerPage, this.filteredProducts.length);
    },

  },


  methods: {
    async updateProductCategory(product) {
    try {
      const response = await fetchWithToken(
        `${process.env.VUE_APP_API_BASE_URL}/update-product-info/${product.asin}`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ category: product.category }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      const data = await response.json();
      alert(`Category updated: ${data.updated_product.category}`);
    } catch (error) {
      console.error("Error updating product category:", error);
    }
  },
    extractPriceDiffPercentage(priceHistory) {
      if (!priceHistory || priceHistory.length < 2) {
        return 0; // Nessuna differenza se non ci sono abbastanza dati
      }
      const lastPrice = priceHistory[priceHistory.length - 1].price;
      const previousPrice = priceHistory[priceHistory.length - 2].price;
      if (previousPrice === 0) return 0;
      return ((lastPrice - previousPrice) / previousPrice) * 100;
    },
    changePage(page) {
    if (page === '...') return; // Non fare nulla se cliccato su '...'

    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  },

  async deleteSelectedProducts() {
  if (this.selectedAsins.length === 0) {
    alert("Select at least one product to delete.");
    return;
  }

  const confirmDelete = confirm(
    "Are you sure you want to delete the selected products?"
  );
  if (!confirmDelete) return;

  try {
    // Chiamata API per eliminare i prodotti
    const response = await fetchWithToken(
      `${process.env.VUE_APP_API_BASE_URL}/remove-products/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.selectedAsins),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const data = await response.json();
    alert(`Deleted products: ${data.removed_asins.join(", ")}`);

    // Rimuovi i prodotti localmente mantenendo i filtri
    this.localProducts = this.localProducts.filter(
      (product) => !this.selectedAsins.includes(product.asin)
    );
    this.filteredProducts = this.filteredProducts.filter(
      (product) => !this.selectedAsins.includes(product.asin)
    );

    // Gestione della paginazione: Riduci la pagina se rimane vuota
    if (this.startIndex >= this.filteredProducts.length && this.currentPage > 1) {
      this.currentPage -= 1;
    }

    // Deseleziona tutti i prodotti
    this.selectedAsins = [];
  } catch (error) {
    console.error("Error deleting selected products:", error);
  }
}
,


    toggleAccordion(asin) {
      if (this.currentOpenAccordion === asin) {
        this.currentOpenAccordion = null;
      } else {
        this.currentOpenAccordion = asin;
      }
    },



    async toggleFavorite(product) {
    try {
      // Chiamata API per aggiornare lo stato del preferito
      const response = await fetchWithToken(
        `${process.env.VUE_APP_API_BASE_URL}/favorite/${product.asin}`,
        {
          method: "PATCH",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      const data = await response.json();
      // Aggiorna lo stato del prodotto nel frontend
      product.is_favorite = data.is_favorite;
    } catch (error) {
      console.error("Errore durante l'aggiornamento del preferito:", error);
    }
  },
  filterFavorites() {
    this.filteredProducts = this.localProducts.filter((product) => product.is_favorite);
    this.currentPage = 1; // Reset paginazione
  },
    calculatePriceDiff(product) {
  const history = product.price_history;
  if (!history || history.length < 2) {
    return "="; // Non c'è abbastanza cronologia per calcolare la differenza
  }

  const lastPrice = history[history.length - 1].price; // Prezzo attuale
  const previousPrice = history[history.length - 2].price; // Prezzo precedente

  if (lastPrice === previousPrice) {
    return `<span><svg class="w-5 h-5 text-gray-300 dark:text-gray-200" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 20V10m0 10-3-3m3 3 3-3m5-13v10m0-10 3 3m-3-3-3 3"/>
</svg>
</span>`; // Prezzo invariato
  }

  const diffPercentage = ((lastPrice - previousPrice) / previousPrice) * 100;

  if (diffPercentage > 0) {
    return `<span class="text-red-500 flex">+${diffPercentage.toFixed(2)}% <svg class="w-5 h-5 text-red-500 dark:text-red-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v13m0-13 4 4m-4-4-4 4"/>
</svg>
</span>`; // Incremento positivo
  } else {
    return `<span class="text-green-500 flex items-center">
  ${diffPercentage.toFixed(2)}%
  <svg class="w-5 h-5 text-green-500 dark:text-green-500 ml-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19V5m0 14-4-4m4 4 4-4"/>
  </svg>
</span>
`; // Decremento negativo
  }
},


applyFilters() {
  const { searchQuery, selectedCategory, selectedPriceRange, selectedCondition } = this.filters;

  this.filteredProducts = this.localProducts.filter((product) => {
    // Filtra per ricerca
    const matchesSearchQuery =  product.title.toLowerCase().includes(searchQuery.toLowerCase()) || product.asin.toLowerCase().includes(searchQuery.toLowerCase());

    // Filtra per categoria
    const matchesCategory = !selectedCategory || product.category === selectedCategory;

    // Filtra per range di prezzo
    const matchesPriceRange = !selectedPriceRange ||
      (product.price >= selectedPriceRange[0] && product.price <= selectedPriceRange[1]);

    // Filtra per condizione
    const matchesCondition = !selectedCondition || product.condition === selectedCondition;

    const matchesCoupon = !this.filters.onlyWithCoupon || product.coupon_value > 0;

    return matchesSearchQuery && matchesCategory && matchesPriceRange && matchesCondition && matchesCoupon;
    

    




  });

  this.currentPage = 1; // Resetta la paginazione quando filtri
},

  clearFilters() {
    // Resetta i filtri
    this.filters.searchQuery = "";
    this.filters.selectedCategory = "";
    this.filters.selectedPriceRange = "";
    this.filters.selectedCondition = ""; // Ripristina la condizione
    this.filters.onlyWithCoupon = false;


    // Ripristina la lista di prodotti
    this.filteredProducts = [...this.localProducts];

    this.currentPage = 1; // Resetta la paginazione
  },



  sort(column) {
    if (this.sortBy === column) {
      this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
    } else {
      this.sortBy = column;
      // Default to desc for price and DIFF, asc for others
      this.sortDirection = (column === "price" || column === "DIFF") ? "desc" : "asc";
    }

    this.filteredProducts.sort((a, b) => {
      let valueA, valueB;

      if (column === "DIFF") {
        valueA = this.extractPriceDiffPercentage(a.price_history);
        valueB = this.extractPriceDiffPercentage(b.price_history);
      } else {
        valueA = a[column];
        valueB = b[column];

        if (typeof valueA === "string") {
          valueA = valueA.toLowerCase();
          valueB = valueB.toLowerCase();
        }
      }

      // Handle null/undefined values
      if (valueA === null || valueA === undefined) valueA = (this.sortDirection === "asc" ? Infinity : -Infinity);
      if (valueB === null || valueB === undefined) valueB = (this.sortDirection === "asc" ? Infinity : -Infinity);

      if (this.sortDirection === "asc") {
        return valueA > valueB ? 1 : valueA < valueB ? -1 : 0;
      } else {
        return valueA < valueB ? 1 : valueA > valueB ? -1 : 0;
      }
    });

    // Reset to page 1 after sorting
    this.currentPage = 1;
  },

  async updateProductPrice(product) {
  if (this.loadingProducts[product.asin]) return; // Evita aggiornamenti multipli

  const confirmUpdate = confirm(
    `Do you want to manually update the price for ${product.title}?`
  );
  if (!confirmUpdate) return;

  // Imposta lo stato di caricamento
  this.loadingProducts = {
    ...this.loadingProducts,
    [product.asin]: true,
  };

  try {
    const response = await fetchWithToken(
      `${process.env.VUE_APP_API_BASE_URL}/update-product/${product.asin}`,
      {
        method: "POST",
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail);
    }

    const data = await response.json();
    alert(`Updated price for ${product.title}: €${data.product.price}`);

    // Aggiorna i dettagli del prodotto direttamente nel frontend
    product.price = data.product.price;
    product.price_history = data.product.price_history;
    product.max_price = data.product.max_price;
    product.min_price = data.product.min_price;
    product.average_price = data.product.average_price;
    product.availability = data.product.availability;
    product.condition = data.product.condition;
  } catch (error) {
    console.error("Error updating product price:", error);
  } finally {
    // Resetta lo stato di caricamento
    this.loadingProducts = {
      ...this.loadingProducts,
      [product.asin]: false,
    };
  }
},


    async updateSelectedPrices() {
      try {
        if (this.selectedAsins.length === 0) {
          alert("Select at least one product to update.");
          return;
        }

        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/update-selected-prices/`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(this.selectedAsins),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        const data = await response.json();
        alert(`Updated products: ${data.updated_products.join(", ")}`);

        // Emetti l'evento per informare il genitore di aggiornare i prodotti
        this.$emit("refresh-products");
      } catch (error) {
        console.error("Error updating selected prices:", error);
      }
    },

    async removeProduct(asin) {
    const confirmDelete = confirm(
      "Sei sicuro di voler eliminare questo prodotto dal monitoraggio?"
    );
    if (!confirmDelete) return;

    try {
      const response = await fetchWithToken(
        `${process.env.VUE_APP_API_BASE_URL}/remove-product/${asin}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail);
      }

      // Aggiorna localmente la lista dei prodotti
      this.localProducts = this.localProducts.filter(
        (product) => product.asin !== asin
      );

      // Applica i filtri per aggiornare la vista
      this.applyFilters();
    } catch (error) {
      console.error("Errore durante l'eliminazione del prodotto:", error);
    }
  },

    viewPriceHistory(asin) {
      this.$router.push(`/products/${asin}`);
    },
    // removeProduct(asin) {
    //   this.$emit("remove-product", asin);
    // },
    
  },
  
};
</script>


<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.3);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.5);
}

/* Animations are now global in main.css */
.animate-fadeIn {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.animate-spin {
  animation: spin 1s linear infinite;
}
</style>