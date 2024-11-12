<template>
  <div>
    <h1>Dashboard</h1>
    <p>Benvenuto, {{ username }}</p>
    <form @submit.prevent="addProduct">
      <input v-model="productUrl" placeholder="Inserisci URL prodotto Amazon" required />
      <button type="submit">Aggiungi Prodotto</button>
    </form>
    <button @click="updatePricesManual" :disabled="isLoading">
      Aggiorna Prezzi Manualmente
    </button>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <p v-if="isLoading" style="color: blue;">Caricamento in corso...</p>
    <CombinedPriceChart :products="products" />
    <ProductList :products="products" @remove-product="removeProduct" />
  </div>
</template>

<script>
import ProductList from '../components/ProductList.vue'
import CombinedPriceChart from '../components/CombinedPriceChart.vue'
import { jwtDecode } from 'jwt-decode';
import { handleAuthError } from '../utils/auth';

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
    async addProduct() {
      try {
        this.isLoading = true;
        const token = localStorage.getItem('token');
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/add-product/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ product_url: this.productUrl })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        this.productUrl = '';
        this.errorMessage = '';
        await this.fetchProducts();
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false;
      }
      await this.fetchProducts();
    },
    async fetchProducts() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/dashboard`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }
        const data = await response.json();
        this.products = data.products;
      } catch (error) {
        handleAuthError(error);
        console.error('Errore nel caricamento dei prodotti:', error);
      }
    }
  ,
    async updatePricesManual() {
      try {
        this.isLoading = true;
        const token = localStorage.getItem('token');
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/update-prices-manual/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        await this.fetchProducts(); // Aggiorna i prodotti dopo l'aggiornamento manuale
      } catch (error) {
        this.errorMessage = 'Errore durante l\'aggiornamento manuale dei prezzi';
        console.error(error);
      } finally {
        this.isLoading = false;
      }
    },
    async removeProduct(asin) {
      const confirmDelete = confirm("Sei sicuro di voler eliminare questo prodotto dal monitoraggio?");
      if (!confirmDelete) {
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/remove-product/${asin}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail);
        }

        await this.fetchProducts();
      } catch (error) {
        console.error('Errore durante l\'eliminazione del prodotto:', error);
      }
      await this.fetchProducts();
    }
  }
}
</script>
