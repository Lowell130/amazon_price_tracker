<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p>Benvenuto, {{ username }}</p>
    <form @submit.prevent="addProduct" class="product-form">
      <input v-model="productUrl" placeholder="Inserisci URL prodotto Amazon" required />
      <button type="submit" class="add-button">Aggiungi Prodotto</button>
    </form>
    <div style="text-align: center;">
      <button @click="updatePricesManual" :disabled="isLoading" class="update-button">
        Aggiorna Prezzi Manualmente
      </button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="isLoading" class="loading-message">Caricamento in corso...</p>
    </div>
    <CombinedPriceChart :products="products" />
    <ProductList :products="products" @remove-product="removeProduct" />
  </div>
</template>

<script>
import ProductList from '../components/ProductList.vue';
import CombinedPriceChart from '../components/CombinedPriceChart.vue';
import { jwtDecode } from 'jwt-decode' // Importazione specifica
import { fetchWithToken } from '@/api';

export default {
  name: 'DashboardPage',
  components: { ProductList, CombinedPriceChart },
  data() {
    return {
      productUrl: '',
      products: [],
      username: '',
      errorMessage: '',
      isLoading: false
    }
  },
  async created() {
    this.getUsername();
    await this.fetchProducts();
  },
  methods: {
    getUsername() {
      const token = localStorage.getItem('token');
      if (token) {
        const decodedToken = jwtDecode(token);
        this.username = decodedToken.sub;
      }
    },
    // Funzione per bonificare il link Amazon
    cleanAmazonUrl(url) {
  // Rimuovi i backslash di escape davanti a '/'
  const match = url.match(/(https:\/\/www\.amazon\.[a-z.]+\/[^/]+\/dp\/[A-Z0-9]+)/);
  return match ? match[0] : url;

    },
    async addProduct() {
      try {
        this.isLoading = true;
        const cleanedUrl = this.cleanAmazonUrl(this.productUrl);  // Bonifica il link
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/add-product/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product_url: cleanedUrl })  // Usa il link bonificato
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        this.productUrl = '';  // Resetta il campo input
        this.errorMessage = '';
        await this.fetchProducts();
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
    },
    async fetchProducts() {
      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/dashboard`);
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }
        const data = await response.json();
        this.products = data.products;
      } catch (error) {
        console.error('Errore nel caricamento dei prodotti:', error);
      }
    },
    async updatePricesManual() {
      try {
        this.isLoading = true;
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/update-prices-manual/`, {
          method: 'POST'
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        await this.fetchProducts();
      } catch (error) {
        this.errorMessage = 'Errore durante l\'aggiornamento manuale dei prezzi';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },
    async removeProduct(asin) {
      const confirmDelete = confirm("Sei sicuro di voler eliminare questo prodotto dal monitoraggio?");
      if (!confirmDelete) return;

      try {
        const response = await fetchWithToken(`${process.env.VUE_APP_API_BASE_URL}/remove-product/${asin}`, {
          method: 'DELETE'
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        await this.fetchProducts();
      } catch (error) {
        console.error('Errore durante l\'eliminazione del prodotto:', error);
      }
    }
  }
}
</script>

<style scoped>
/* Stile della dashboard */
.dashboard {
  max-width: 100%;
  margin: auto;
  padding: 20px;
}

.product-form {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 20px;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  width: 60%;
}

.add-button, .update-button {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-button {
  background-color: #4caf50;
  color: white;
}

.add-button:hover {
  background-color: #45a049;
}

.update-button {
  background-color: #2196f3;
  color: white;
  margin-top: 10px;
}

.update-button:hover {
  background-color: #1976d2;
}

.update-button:disabled {
  background-color: #b3e5fc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  font-weight: bold;
}

.loading-message {
  color: blue;
  font-weight: bold;
}
</style>
