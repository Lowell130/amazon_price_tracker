<template>
  <section class="bg-gray-50 dark:bg-gray-900 p-3 sm:p-5 antialiased min-h-screen">
    <div class="mx-auto max-w-screen-2xl px-4 lg:px-8">
      <div class="bg-white dark:bg-gray-800 relative shadow-md rounded-lg overflow-hidden">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row items-center justify-between space-y-3 md:space-y-0 md:space-x-4 p-4 border-b dark:border-gray-700">
          <div class="w-full md:w-1/2">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Admin Users Management</h1>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Manage users, roles, and view tracked products.</p>
          </div>
          <div class="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 items-stretch md:items-center justify-end md:space-x-3 flex-shrink-0">
             <!-- Placeholder for future search/filter controls -->
          </div>
        </div>

        <!-- Loading/Error States -->
        <div v-if="loading" class="p-8 text-center">
            <div role="status">
                <svg aria-hidden="true" class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-primary-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                </svg>
                <span class="sr-only">Loading...</span>
            </div>
        </div>
        <div v-else-if="error" class="p-4 text-center text-red-500 bg-red-50 dark:bg-red-900/20 rounded-lg m-4">
            {{ error }}
        </div>

        <!-- Table -->
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
              <tr>
                <th scope="col" class="px-4 py-3">Username</th>
                <th scope="col" class="px-4 py-3">Email</th>
                <th scope="col" class="px-4 py-3">Role</th>
                <th scope="col" class="px-4 py-3 text-center">Products</th>
                <th scope="col" class="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.username" class="border-b dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                <th scope="row" class="px-4 py-3 font-medium text-gray-900 whitespace-nowrap dark:text-white flex items-center">
                  <div class="w-8 h-8 rounded-full bg-primary-100 text-primary-600 flex items-center justify-center mr-3 font-bold text-xs">
                    {{ user.username.charAt(0).toUpperCase() }}
                  </div>
                  {{ user.username }}
                </th>
                <td class="px-4 py-3">{{ user.email }}</td>
                <td class="px-4 py-3">
                  <span v-if="user.admin" class="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded dark:bg-green-900 dark:text-green-300 border border-green-200 dark:border-green-800">Admin</span>
                  <span v-else class="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded dark:bg-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-600">User</span>
                </td>
                <td class="px-4 py-3 text-center">
                    <span class="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded dark:bg-blue-900 dark:text-blue-300">
                        {{ user.products_count }}
                    </span>
                </td>
                <td class="px-4 py-3 flex items-center justify-end space-x-2">
                  
                  <!-- View Products -->
                  <button @click="viewProducts(user)" class="p-2 text-gray-500 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-600 dark:hover:text-white transition-colors" title="View Products">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                  </button>

                  <!-- Toggle Admin -->
                  <button v-if="!user.admin" @click="toggleAdmin(user)" class="p-2 text-blue-600 rounded-lg hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600 transition-colors" title="Make Admin">
                     <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016zM12 9v2m0 4h.01"></path></svg>
                  </button>

                  <!-- Reset Password -->
                  <button @click="resetPassword(user)" class="p-2 text-yellow-600 rounded-lg hover:bg-yellow-100 dark:text-yellow-500 dark:hover:bg-gray-600 transition-colors" title="Reset Password">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11.536 19.464a6 6 0 01-1.414 0l-1.828-1.828a2 2 0 010-2.828l.828-.828a2 2 0 011.414 0L15.344 15H18a2 2 0 002-2V9a2 2 0 00-2-2h-1m-4 0a6 6 0 100 12 6 6 0 000-12z"></path></svg>
                  </button>

                  <!-- Delete User -->
                  <button @click="deleteUser(user)" class="p-2 text-red-600 rounded-lg hover:bg-red-100 dark:text-red-500 dark:hover:bg-gray-600 transition-colors" title="Delete User">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>

                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Products Modal -->
      <div v-if="showProductsModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 backdrop-blur-sm p-4">
        <div class="bg-white rounded-lg shadow-2xl dark:bg-gray-700 w-full max-w-2xl p-6 relative flex flex-col max-h-[90vh]">
          <button @click="closeModal" class="absolute top-3 right-3 text-gray-400 hover:text-gray-900 dark:hover:text-white rounded-lg p-1 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
          
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4 border-b pb-2 dark:border-gray-600">
            Products for <span class="text-primary-600 dark:text-primary-400">{{ selectedUser?.username }}</span>
          </h3>
          
          <div v-if="userProducts.length === 0" class="text-center py-12 text-gray-500 dark:text-gray-400 flex flex-col items-center">
             <svg class="w-16 h-16 mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>
             <p>No products tracked by this user.</p>
          </div>
          
          <ul v-else class="space-y-3 overflow-y-auto pr-2 custom-scrollbar flex-1">
            <li v-for="product in userProducts" :key="product.asin" class="flex items-center space-x-4 p-3 bg-gray-50 dark:bg-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-500 transition-colors border border-gray-100 dark:border-gray-500">
              <img :src="product.image_url" class="w-16 h-16 rounded object-contain bg-white p-1 border dark:border-gray-500" alt="Product Image">
              <div class="flex-1 min-w-0">
                <p class="text-sm font-semibold text-gray-900 truncate dark:text-white">{{ product.title }}</p>
                <div class="flex items-center mt-1 space-x-2">
                   <span class="text-lg font-bold text-gray-900 dark:text-white">{{ product.price }} €</span>
                   <span v-if="product.condition !== 'Nuovo'" class="text-xs bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded dark:bg-yellow-900 dark:text-yellow-300">{{ product.condition }}</span>
                </div>
              </div>
              <a :href="product.product_url" target="_blank" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-600 transition-colors" title="View on Amazon">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
              </a>
            </li>
          </ul>
          
          <div class="mt-4 pt-4 border-t dark:border-gray-600 flex justify-end">
            <button @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 dark:bg-gray-600 dark:text-white dark:hover:bg-gray-500 transition-colors font-medium">
                Close
            </button>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script>
import { fetchWithToken } from "@/api";

export default {
  name: "AdminUsersPage",
  data() {
    return {
      users: [],
      loading: true,
      error: null,
      showProductsModal: false,
      selectedUser: null,
      userProducts: [],
    };
  },
  async mounted() {
    await this.loadUsers();
  },
  methods: {
    async loadUsers() {
      this.loading = true;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/users`);
        if (response.ok) {
          this.users = await response.json();
        } else {
          this.error = "Errore nel caricamento degli utenti.";
        }
      } catch (err) {
        this.error = "Errore di connessione.";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    async toggleAdmin(user) {
      if (!confirm(`Sei sicuro di voler cambiare lo stato admin per ${user.username}?`)) return;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/users/${user.username}/toggle-admin`, {
          method: "PATCH"
        });
        if (response.ok) {
          const data = await response.json();
          user.admin = data.admin;
        } else {
          alert("Errore durante l'aggiornamento.");
        }
      } catch (e) {
        console.error(e);
        alert("Errore di connessione.");
      }
    },
    async deleteUser(user) {
      if (!confirm(`Sei sicuro di voler eliminare l'utente ${user.username}? Questa azione è irreversibile.`)) return;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/users/${user.username}`, {
          method: "DELETE"
        });
        if (response.ok) {
          this.users = this.users.filter(u => u.username !== user.username);
        } else {
          alert("Errore durante l'eliminazione.");
        }
      } catch (e) {
        console.error(e);
        alert("Errore di connessione.");
      }
    },
    async resetPassword(user) {
      if (!confirm(`Inviare email di reset password a ${user.email}?`)) return;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/users/${user.username}/reset-password`, {
          method: "POST"
        });
        if (response.ok) {
          alert("Email di reset inviata.");
        } else {
          alert("Errore durante l'invio della richiesta.");
        }
      } catch (e) {
        console.error(e);
        alert("Errore di connessione.");
      }
    },
    async viewProducts(user) {
      this.selectedUser = user;
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/admin/users/${user.username}/products`);
        if (response.ok) {
          this.userProducts = await response.json();
          this.showProductsModal = true;
        } else {
          alert("Impossibile caricare i prodotti.");
        }
      } catch (e) {
        console.error(e);
        alert("Errore di connessione.");
      }
    },
    closeModal() {
      this.showProductsModal = false;
      this.selectedUser = null;
      this.userProducts = [];
    }
  },
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 20px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.8);
}
</style>
