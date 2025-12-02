<template>
  <div class="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
    <div class="w-full max-w-sm bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
      <div class="flex justify-end px-4 pt-6">
        <!-- <button
          id="dropdownButton"
          data-dropdown-toggle="dropdown"
          class="inline-block text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:ring-4 focus:outline-none focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-1.5"
          type="button"
        >
          <span class="sr-only">Open dropdown</span>
          <svg
            class="w-5 h-5"
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 16 3"
          >
            <path
              d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"
            />
          </svg>
        </button> -->
      </div>
      <div class="flex flex-col items-center pb-10">
        <img
          class="w-24 h-24 mb-3 rounded-full shadow-lg"
          src="https://robohash.org/48972a5bc7159ad9bfd3e95e42895bcd?set=set4&bgset=&size=400x400"
          :alt="'Avatar ' + username"
        />
        <h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
          {{ username }}   
        </h5>
        <span class="text-sm text-gray-500 dark:text-gray-400">
          {{ email}}
        </span>
     
     
        <span class="text-sm text-gray-500 dark:text-gray-400">
          {{ isAdmin ? "Admin user" : "Regular user" }}
        </span>
     

        <!-- Pulsante visibile solo agli admin -->
        <div v-if="isAdmin" class="mt-6">
  <button
    @click="generatePriceDropsReport"
    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-red-700 rounded-lg hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800"
  >
    Generate Price Drops Report
  </button>
</div>
<p v-else>
  Admin status: {{ isAdmin }}
</p>
      </div>
    </div>
  </div>
</template>


<script>
// import { jwtDecode } from 'jwt-decode';

import { fetchWithToken } from "@/api"; // Importa la funzione API per chiamare l'endpoint

export default {
  name: "ProfilePage",
  data() {
    return {
      username: "",
      email: "",
      isAdmin: false, // Stato per verificare se l'utente è admin
    };
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
    console.log("User data:", userData); // Verifica i dati
    this.username = userData.username;
    this.email = userData.email;
    this.isAdmin = userData.admin;
  } catch (error) {
    console.error("Errore nel caricamento delle informazioni utente:", error);
    this.$router.push("/login");
  }
}
,
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
  },
};
</script>
