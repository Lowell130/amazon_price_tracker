<template>
  <header class="fixed top-0 left-0 right-0 z-50 transition-all duration-300 px-4 md:px-8 py-4" :class="{ 'py-2': isScrolled }">
    <!-- Navbar Container (Floating Glassmorphism) -->
    <nav 
      class="max-w-7xl mx-auto rounded-2xl border border-white/20 bg-white/70 dark:bg-gray-900/70 backdrop-blur-xl shadow-lg transition-all duration-300"
      :class="{ 'shadow-xl border-white/30': isScrolled }"
    >
      <div class="px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          
          <!-- Logo & Brand -->
          <router-link to="/" class="flex items-center group space-x-2">
            <div class="p-2 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 shadow-md group-hover:scale-110 transition-transform duration-300">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 dark:from-white dark:to-gray-400">
              PriceHub.it
            </span>
          </router-link>

          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-1">
            <template v-for="link in navigationLinks" :key="link.to">
              <router-link
                v-if="link.show"
                :to="link.to"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 group relative"
                :class="[$route.path === link.to ? 'text-blue-600 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/30' : 'text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-100/50 dark:hover:bg-gray-800/50']"
              >
                {{ link.name }}
                <span 
                  class="absolute bottom-1 left-4 right-4 h-0.5 bg-blue-600 transform scale-x-0 transition-transform duration-300 group-hover:scale-x-100"
                  v-if="$route.path !== link.to"
                ></span>
              </router-link>
            </template>
            
            <button 
              v-if="isAuthenticated" 
              @click="logout"
              class="ml-4 px-5 py-2 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm font-semibold hover:bg-red-100 dark:hover:bg-red-900/40 transition-colors duration-200"
            >
              Logout
            </button>
          </div>

          <!-- Mobile Menu Button -->
          <div class="md:hidden flex items-center">
            <button 
              @click="isMobileMenuOpen = !isMobileMenuOpen"
              class="p-2 rounded-lg text-gray-600 dark:text-gray-300 hover:bg-gray-100/50 dark:hover:bg-gray-800/50 transition-colors"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform -translate-y-4 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform -translate-y-4 opacity-0"
      >
        <div v-if="isMobileMenuOpen" class="md:hidden border-t border-gray-100 dark:border-gray-800 overflow-hidden">
          <div class="px-4 pt-2 pb-6 space-y-2">
            <template v-for="link in navigationLinks" :key="link.to">
              <router-link
                v-if="link.show"
                :to="link.to"
                @click="isMobileMenuOpen = false"
                class="block px-4 py-3 rounded-xl text-base font-medium transition-colors"
                :class="[$route.path === link.to ? 'text-blue-600 dark:text-blue-400 bg-blue-50/50 dark:bg-blue-900/30' : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100/50 dark:hover:bg-gray-800/50']"
              >
                {{ link.name }}
              </router-link>
            </template>
            <button 
              v-if="isAuthenticated"
              @click="logout(); isMobileMenuOpen = false"
              class="w-full text-left px-4 py-3 rounded-xl text-base font-medium text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </transition>
    </nav>

    <!-- Telegram Promo Banner (Floating Tip) -->
    <transition
      enter-active-class="transition duration-500 ease-out"
      enter-from-class="transform translate-y-10 opacity-0 scale-95"
      enter-to-class="transform translate-y-0 opacity-100 scale-100"
      leave-active-class="transition duration-300 ease-in"
      leave-from-class="transform translate-y-0 opacity-100 scale-100"
      leave-to-class="transform translate-y-10 opacity-0 scale-95"
    >
      <div 
        v-if="isBannerVisible"
        class="fixed bottom-6 right-6 md:right-12 z-40 max-w-sm w-full"
      >
        <div class="bg-indigo-600 dark:bg-indigo-500 text-white rounded-2xl shadow-2xl p-4 flex items-center space-x-4 border border-indigo-400/30 backdrop-blur-md">
          <div class="flex-shrink-0 w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.12.02-1.96 1.25-5.54 3.69-.52.35-.99.53-1.39.52-.45-.01-1.31-.25-1.95-.45-.78-.25-1.4-.39-1.35-.82.02-.23.34-.46.95-.71 3.73-1.62 6.21-2.69 7.45-3.2 3.53-1.45 4.26-1.7 4.74-1.71.11 0 .34.03.5.15.13.11.17.26.19.38.01.07.02.21.01.28z"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm font-semibold">Prezzi più bassi?</p>
            <p class="text-xs text-white/80">Unisciti al nostro canale Telegram!</p>
          </div>
          <a 
            href="https://t.me/amz_it_price_drop" 
            target="_blank"
            class="bg-white text-indigo-600 px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-indigo-50 transition-colors"
          >
            Apri
          </a>
          <button @click="isBannerVisible = false" class="text-white/60 hover:text-white transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </transition>
  </header>
</template>

<script>
import { jwtDecode } from 'jwt-decode'

export default {
    name: "HeaderTemplate",
    data() {
      return {
        isAuthenticated: false,
        isAdmin: false,
        isBannerVisible: true,
        isScrolled: false,
        isMobileMenuOpen: false,
      };
    },
    computed: {
      navigationLinks() {
        return [
          { name: 'Home', to: '/', show: true },
          { name: 'Registrati', to: '/register', show: !this.isAuthenticated },
          { name: 'Login', to: '/login', show: !this.isAuthenticated },
          { name: 'Dashboard', to: '/dashboard', show: this.isAuthenticated },
          { name: 'AI Insights', to: '/analysis', show: this.isAuthenticated },
          { name: 'Profile', to: '/profile', show: this.isAuthenticated },
          { name: 'Admin', to: '/admin/users', show: this.isAuthenticated && this.isAdmin },
        ];
      }
    },
    mounted() {
      this.checkAuth();
      window.addEventListener('scroll', this.handleScroll);
    },
    beforeUnmount() {
      window.removeEventListener('scroll', this.handleScroll);
    },
    watch: {
      "$route"() {
        this.checkAuth();
        this.isMobileMenuOpen = false;
      },
    },
    methods: {
      handleScroll() {
        this.isScrolled = window.scrollY > 20;
      },
      checkAuth() {
        const token = localStorage.getItem("token");
        if (token) {
          try {
            const decoded = jwtDecode(token);
            const now = Math.floor(Date.now() / 1000);
            if (decoded.exp > now) {
              this.isAuthenticated = true;
              this.isAdmin = decoded.admin || false;
            } else {
              this.logout();
            }
          } catch (error) {
            console.error("Errore nella decodifica del token:", error);
            this.logout();
          }
        } else {
          this.isAuthenticated = false;
          this.isAdmin = false;
        }
      },
      logout() {
        localStorage.removeItem("token");
        this.isAuthenticated = false;
        this.isAdmin = false;
        this.$router.push("/login");
      },
    },
};
</script>

<style scoped>
.router-link-active {
  /* Using Tailwind for classes instead of scoped css when possible, but helper for clarity if needed */
}
</style>