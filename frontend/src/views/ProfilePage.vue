<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8">
      <!-- Profile Card -->
      <div class="bg-white dark:bg-gray-800 shadow-xl rounded-2xl overflow-hidden transform transition-all hover:scale-[1.01] duration-300">
        
        <!-- Header / Banner -->
        <div class="h-32 bg-gradient-to-r from-blue-500 to-purple-600"></div>
        
        <!-- Profile Info -->
        <div class="relative px-6 pb-8">
          <div class="relative -mt-16 mb-6 flex justify-center">
            <img
              class="h-32 w-32 rounded-full border-4 border-white dark:border-gray-800 shadow-lg bg-white"
              :src="avatarUrl"
              :alt="'Avatar ' + username"
            />
          </div>
          
          <div class="text-center">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-1">
              {{ username }}
            </h2>
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
              {{ email }}
            </p>
            
            <span 
              v-if="isAdmin" 
              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
            >
              Administrator
            </span>
            <span 
              v-else 
              class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
            >
              Regular User
            </span>
          </div>

          <!-- Stats Section -->
          <div class="mt-8 grid grid-cols-1 gap-4 border-t border-gray-200 dark:border-gray-700 pt-6">
            <div class="text-center">
              <span class="block text-2xl font-bold text-gray-900 dark:text-white">
                {{ productsCount }}
              </span>
              <span class="text-sm text-gray-500 dark:text-gray-400">
                Products Tracked
              </span>
            </div>
          </div>

          <!-- Actions Section -->
          <div class="mt-8 space-y-3">
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3">
              Account Actions
            </h3>
            
            <!-- Admin Actions -->
            <div v-if="isAdmin" class="space-y-3 mb-6">
              <button
                @click="generatePriceDropsReport"
                class="w-full flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Generate Price Drops Report
              </button>
            </div>

            <!-- General Actions -->
            <button
              @click="logout"
              class="w-full flex justify-center items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </div>
      
      <!-- Footer Info -->
      <p class="text-center text-xs text-gray-500 dark:text-gray-400">
        Amazon Price Tracker v1.0
      </p>
    </div>
  </div>
</template>

<script>
import { fetchWithToken } from "@/api";

export default {
  name: "ProfilePage",
  data() {
    return {
      username: "",
      email: "",
      isAdmin: false,
      productsCount: 0,
    };
  },
  computed: {
    avatarUrl() {
      // Use a consistent avatar based on username or email if available, otherwise random
      const seed = this.username || "default";
      return `https://robohash.org/${seed}?set=set4&bgset=&size=400x400`;
    }
  },
  created() {
    this.getUserInfo();
  },
  methods: {
    async getUserInfo() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/auth/users/me`,
          { method: "GET" }
        );

        if (!response.ok) {
          throw new Error("Errore nel recupero delle informazioni utente");
        }

        const userData = await response.json();
        this.username = userData.username;
        this.email = userData.email;
        this.isAdmin = userData.admin;
        this.productsCount = userData.products_count || 0;
      } catch (error) {
        console.error("Errore nel caricamento delle informazioni utente:", error);
        this.logout(); // Redirect to login on error
      }
    },
    async generatePriceDropsReport() {
      try {
        const response = await fetchWithToken(
          `${process.env.VUE_APP_API_BASE_URL}/admin/generate-price-drops-report`,
          { method: "POST" }
        );
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }
        const data = await response.json();
        alert(`Price drops report generated: ${data.total_price_drops} drops.`);
      } catch (error) {
        console.error("Errore durante la generazione del report:", error);
        alert("Error generating price drops report.");
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.$router.push("/login");
    }
  },
};
</script>
