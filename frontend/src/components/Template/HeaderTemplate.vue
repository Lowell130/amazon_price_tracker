<template>
  <header :class="{'pt-16': isBannerVisible}"> 
    <!-- Banner -->
    <div 
      v-if="isBannerVisible"
      id="sticky-banner" 
      class="fixed top-0 start-0 z-50 flex justify-between w-full p-4 border-b border-gray-200 bg-gray-50 dark:bg-gray-700 dark:border-gray-600"
    >
      <div class="flex items-center mx-auto">
        <p class="flex items-center text-sm font-normal text-gray-500 dark:text-gray-400">
          <span class="inline-flex p-1 me-3 bg-gray-200 rounded-full dark:bg-gray-600 w-6 h-6 items-center justify-center shrink-0">
            <svg class="w-3 h-3 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 19">
              <path d="M15 1.943v12.114a1 1 0 0 1-1.581.814L8 11V5l5.419-3.871A1 1 0 0 1 15 1.943ZM7 4H2a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2v5a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2V4ZM4 17v-5h1v5H4ZM16 5.183v5.634a2.984 2.984 0 0 0 0-5.634Z"/>
            </svg>
            <span class="sr-only">Light bulb</span>
          </span>
          <span>Ricevi aggiornamenti di prezzo, entra nel canale
            <a href="https://t.me/amz_it_price_drop" class="inline font-medium text-blue-600 underline dark:text-blue-500 hover:no-underline">
              Telegram
            </a>
          </span>
        </p>
      </div>
      <div class="flex items-center">
        <button @click="closeBanner" class="shrink-0 inline-flex justify-center w-7 h-7 items-center text-gray-400 hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 dark:hover:bg-gray-600 dark:hover:text-white">
          <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
          </svg>
          <span class="sr-only">Close banner</span>
        </button>
      </div>
    </div>

    <!-- Navbar -->
    <nav class="bg-white border-gray-200 dark:bg-gray-900">
      <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <router-link to="/" class="flex items-center space-x-3 rtl:space-x-reverse">
          <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Logo" />
          <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">PriceHub.it</span>
        </router-link>
        <button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-xs text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
          <span class="sr-only">Open main menu</span>
          <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
          </svg>
        </button>
        <div class="hidden w-full md:block md:w-auto" id="navbar-default">
          <ul class="font-small flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <router-link to="/" class="block py-2 px-3 text-black rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Home</router-link>
            <router-link v-if="!isAuthenticated" to="/register" class="block py-2 px-3 text-black rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Registrati</router-link>
            <router-link v-if="!isAuthenticated" to="/login" class="block py-2 px-3 text-black rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Login</router-link>
            <router-link v-if="isAuthenticated" to="/dashboard" class="block py-2 px-3 text-black rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Dashboard</router-link>
            <router-link v-if="isAuthenticated" to="/profile" class="block py-2 px-3 text-black rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Profile</router-link>
            <button class="block py-2 px-3 text-black rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500" v-if="isAuthenticated" @click="logout">Logout</button>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>


<script>
 import { jwtDecode } from 'jwt-decode' // Importazione specifica
 import { onMounted } from 'vue'
//  import ThemeToggle from '../ThemeToggle.vue';
import { 
    initAccordions, 
    initCarousels, 
    initCollapses, 
    initDials, 
    initDismisses, 
    initDrawers, 
    initDropdowns, 
    initModals, 
    initPopovers, 
    initTabs, 
    initTooltips } from 'flowbite'
export default {
 
    data() {
      return {
        isAuthenticated: false, // Stato iniziale dell'autenticazione
        isBannerVisible: true, // Inizialmente il banner è visibile
      };
    },
    // components: {
    //   ThemeToggle
    // },
    
    mounted() {
      this.checkAuth();
    },
    watch: {
      "$route"() {
        this.checkAuth();
      },
    },
    methods: {
      checkAuth() {
        const token = localStorage.getItem("token");
        if (token) {
          try {
            const decoded = jwtDecode(token);
            const now = Math.floor(Date.now() / 1000); // Tempo attuale in secondi
            if (decoded.exp > now) {
              this.isAuthenticated = true; // Token valido
            } else {
              this.logout(); // Token scaduto
            }
          } catch (error) {
            console.error("Errore nella decodifica del token:", error);
            this.logout(); // Token non valido
          }
        } else {
          this.isAuthenticated = false; // Nessun token presente
        }
      },
      logout() {
        localStorage.removeItem("token"); // Rimuove il token
        this.isAuthenticated = false; // Aggiorna lo stato
        this.$router.push("/login"); // Reindirizza al login
      },
      closeBanner() {
      this.isBannerVisible = false;
    },
    },
  };
  onMounted(() => {
      initAccordions();
      initCarousels();
      initCollapses();
      initDials();
      initDismisses();
      initDrawers();
      initDropdowns();
      initModals();
      initPopovers();
      initTabs();
      initTooltips();
  })
  </script>