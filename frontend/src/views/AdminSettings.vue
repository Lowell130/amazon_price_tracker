<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 pt-24 pb-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">
            Impostazioni di <span class="text-blue-600">Sistema</span>
          </h1>
          <p class="mt-2 text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-widest">
            Configura il comportamento globale dell'applicazione
          </p>
        </div>
        <router-link 
          to="/dashboard"
          class="flex items-center text-sm font-bold text-gray-500 hover:text-blue-600 transition-colors"
        >
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
          Torna alla Dashboard
        </router-link>
      </div>

      <!-- Settings Card -->
      <div class="bg-white dark:bg-gray-900 rounded-[2.5rem] shadow-xl border border-gray-100 dark:border-gray-800 p-8 md:p-12 overflow-hidden relative group">
        <div class="absolute -top-24 -right-24 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl group-hover:bg-blue-500/10 transition-colors duration-700"></div>

        <div class="relative z-10 space-y-10">
          <!-- Scraper Configuration Section -->
          <section>
            <div class="flex items-center gap-4 mb-6">
              <div class="p-3 bg-blue-600/10 rounded-2xl">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
              </div>
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">Configurazione Scraper Amazon</h2>
            </div>

            <p class="text-gray-500 dark:text-gray-400 mb-8 max-w-2xl">
              Scegli la modalità principale con cui il server estrae i dati da Amazon. Se la modalità avanzata non dovesse funzionare, il sistema proverà comunque un fallback automatico.
            </p>

            <div class="grid sm:grid-cols-2 gap-4">
              <!-- Method: Classic -->
              <label 
                class="relative flex flex-col p-6 rounded-3xl border-2 cursor-pointer transition-all focus-within:ring-2 focus-within:ring-blue-500"
                :class="settings.mode === 'classic' ? 'border-blue-600 bg-blue-50/50 dark:bg-blue-900/10' : 'border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-800'"
              >
                <input type="radio" v-model="settings.mode" value="classic" class="sr-only" />
                <div class="flex items-center justify-between mb-4">
                  <span class="text-sm font-black uppercase tracking-widest" :class="settings.mode === 'classic' ? 'text-blue-600' : 'text-gray-400'">Classic Mode</span>
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center" :class="settings.mode === 'classic' ? 'border-blue-600' : 'border-gray-300'">
                    <div v-if="settings.mode === 'classic'" class="w-2.5 h-2.5 bg-blue-600 rounded-full"></div>
                  </div>
                </div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">CSS Selectors</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                  Usa selettori CSS standard per trovare il prezzo. Molto veloce ma sensibile ai cambi di layout di Amazon.
                </p>
              </label>

              <!-- Method: Advanced -->
              <label 
                class="relative flex flex-col p-6 rounded-3xl border-2 cursor-pointer transition-all focus-within:ring-2 focus-within:ring-blue-500"
                :class="settings.mode === 'json' ? 'border-blue-600 bg-blue-50/50 dark:bg-blue-900/10' : 'border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-800'"
              >
                <input type="radio" v-model="settings.mode" value="json" class="sr-only" />
                <div class="flex items-center justify-between mb-4">
                  <span class="text-sm font-black uppercase tracking-widest" :class="settings.mode === 'json' ? 'text-blue-600' : 'text-gray-400'">Advanced Mode</span>
                  <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center" :class="settings.mode === 'json' ? 'border-blue-600' : 'border-gray-300'">
                    <div v-if="settings.mode === 'json'" class="w-2.5 h-2.5 bg-blue-600 rounded-full"></div>
                  </div>
                </div>
                <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">Deep JSON Parsing</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                  Estrae i dati direttamente dagli oggetti JSON interni di Amazon. Estremamente robusto e difficile da bloccare.
                </p>
              </label>
            </div>
          </section>
          
          <hr class="border-gray-100 dark:border-gray-800" />

          <!-- Proxy Configuration Section -->
          <section>
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-4">
                <div class="p-3 bg-amber-600/10 rounded-2xl">
                  <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                </div>
                <div>
                  <h2 class="text-xl font-bold text-gray-900 dark:text-white">Configurazione Proxy</h2>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Usa un proxy per evitare blocchi IP da Amazon</p>
                </div>
              </div>
              
              <!-- Toggle switch custom -->
              <button 
                @click="settings.use_proxy = !settings.use_proxy"
                class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ring-2 ring-transparent ring-offset-2"
                :class="settings.use_proxy ? 'bg-amber-600' : 'bg-gray-200 dark:bg-gray-700'"
              >
                <span 
                  class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
                  :class="settings.use_proxy ? 'translate-x-6' : 'translate-x-1'"
                />
              </button>
            </div>

            <div v-if="settings.use_proxy" class="space-y-6 animate-fadeIn">
              <div class="grid md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Proxy URL / Host</label>
                  <input 
                    type="text" 
                    v-model="settings.proxy_url" 
                    placeholder="es: http://proxy.example.com:8080"
                    class="w-full px-5 py-3 rounded-2xl bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 focus:ring-2 focus:ring-amber-500 transition-all text-sm"
                  />
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Username</label>
                    <input 
                      type="text" 
                      v-model="settings.proxy_user" 
                      placeholder="opzionale"
                      class="w-full px-5 py-3 rounded-2xl bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 focus:ring-2 focus:ring-amber-500 transition-all text-sm"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">Password</label>
                    <input 
                      type="password" 
                      v-model="settings.proxy_pass" 
                      placeholder="opzionale"
                      class="w-full px-5 py-3 rounded-2xl bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700 focus:ring-2 focus:ring-amber-500 transition-all text-sm"
                    />
                  </div>
                </div>
              </div>
              <p class="text-[10px] text-gray-400 dark:text-gray-500 italic">
                * Supporta proxy HTTP/HTTPS. Se usi un proxy rotante, inserisci l'URL dell'entry-point fornito.
              </p>
            </div>
          </section>

          <hr class="border-gray-100 dark:border-gray-800" />

          <!-- Session & Security Section -->
          <section>
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-4">
                <div class="p-3 bg-emerald-600/10 rounded-2xl">
                  <svg class="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-7.618 3.033A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                </div>
                <div>
                  <h2 class="text-xl font-bold text-gray-900 dark:text-white">Sessione & Sicurezza</h2>
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Configura il timeout e il rinnovo dei token di accesso</p>
                </div>
              </div>
              
              <!-- Toggle switch custom -->
              <button 
                @click="settings.auto_refresh = !settings.auto_refresh"
                class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ring-2 ring-transparent ring-offset-2"
                :class="settings.auto_refresh ? 'bg-emerald-600' : 'bg-gray-200 dark:bg-gray-700'"
              >
                <span 
                  class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
                  :class="settings.auto_refresh ? 'translate-x-6' : 'translate-x-1'"
                />
              </button>
            </div>

            <div class="p-6 rounded-3xl bg-gray-50 dark:bg-gray-800/50 border border-gray-100 dark:border-gray-700">
              <div class="flex items-start gap-4">
                <div class="mt-1">
                  <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <div>
                  <h4 class="text-sm font-bold text-gray-900 dark:text-white mb-1">Auto-refresh Token (Chrome Extension)</h4>
                  <p class="text-xs text-gray-500 dark:text-gray-400 leading-relaxed">
                    Se attivo, l'estensione rinnoverà il token prima di ogni operazione. Disattivandolo, l'estensione sarà più veloce ma richiederà un nuovo login manuale alla scadenza naturale del token (consigliato per utenti frequenti).
                  </p>
                </div>
              </div>
            </div>
          </section>

          <hr class="border-gray-100 dark:border-gray-800" />

          <!-- Save Button -->
          <div class="flex items-center justify-between pt-4">
            <p v-if="statusMessage" :class="statusType === 'success' ? 'text-emerald-600' : 'text-red-500'" class="text-sm font-bold italic animate-pulse">
              {{ statusMessage }}
            </p>
            <div v-else></div>

            <button 
              @click="saveSettings"
              :disabled="loading"
              class="px-10 py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-2xl font-black shadow-xl shadow-blue-600/20 transition-all transform hover:-translate-y-1 active:scale-95 flex items-center gap-3"
            >
              <svg v-if="loading" class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              <span>{{ loading ? 'Salvataggio...' : 'Salva Configurazione' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminSettings',
  data() {
    return {
      settings: {
        mode: 'classic',
        use_proxy: false,
        proxy_url: '',
        proxy_user: '',
        proxy_pass: '',
        auto_refresh: true
      },
      loading: false,
      statusMessage: '',
      statusType: 'success'
    };
  },
  async mounted() {
    await this.fetchSettings();
  },
  methods: {
    async fetchSettings() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/admin/settings`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.settings = {
          mode: response.data.mode || 'classic',
          use_proxy: response.data.use_proxy || false,
          proxy_url: response.data.proxy_url || '',
          proxy_user: response.data.proxy_user || '',
          proxy_pass: response.data.proxy_pass || '',
          auto_refresh: response.data.auto_refresh !== undefined ? response.data.auto_refresh : true
        };
      } catch (error) {
        console.error("Errore caricamento settings:", error);
      }
    },
    async saveSettings() {
      this.loading = true;
      this.statusMessage = '';
      try {
        const token = localStorage.getItem('token');
        await axios.post(`${process.env.VUE_APP_API_BASE_URL}/admin/settings`, this.settings, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.statusMessage = 'Configurazione salvata correttamente!';
        this.statusType = 'success';
        setTimeout(() => this.statusMessage = '', 3000);
      } catch (error) {
        this.statusMessage = 'Errore salvataggio!';
        this.statusType = 'error';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
