<template>

<header>
    <nav class="bg-white border-gray-200 dark:bg-gray-900">
  <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
    <a href="https://flowbite.com/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Flowbite Logo" />
        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Grabbb-It</span>
    </a>
    <button data-collapse-toggle="navbar-default" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-xs text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-default" aria-expanded="false">
        <span class="sr-only">Open main menu</span>
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
        </svg>
    </button>
    <div class="hidden w-full md:block md:w-auto" id="navbar-default">
      <ul class="font-small flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
       
      <router-link to="/" class="block py-2 px-3 text-black  rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Home</router-link>
      <router-link v-if="!isAuthenticated" to="/register" class="block py-2 px-3 text-black  rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Register</router-link>
      <router-link v-if="!isAuthenticated" to="/login" class="block py-2 px-3 text-black  rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Login</router-link>
      <router-link v-if="isAuthenticated" to="/dashboard" class="block py-2 px-3 text-black  rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Dashboard</router-link>
      <router-link v-if="isAuthenticated" to="/profile" class="block py-2 px-3 text-black  rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-black md:dark:text-blue-500">Profile</router-link>
      
      <button v-if="isAuthenticated" @click="logout">Logout</button>
    </ul>
    </div>
  </div>
</nav>
</header>

 

</template>

<script>
 import { jwtDecode } from 'jwt-decode' // Importazione specifica
 import { onMounted } from 'vue'
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
      };
    },
    
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