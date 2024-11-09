<template>
  <div>
    <h1>Dashboard</h1>
    <p>Benvenuto, {{ username }}</p>
    <form @submit.prevent="addProduct">
      <input v-model="productUrl" placeholder="Inserisci URL prodotto Amazon" required />
      <button type="submit">Aggiungi Prodotto</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    <!-- Indicatore di caricamento -->
    <p v-if="isLoading" style="color: blue;">Caricamento in corso...</p>
     <!-- Grafico Combinato per tutti i prodotti -->
     <CombinedPriceChart :products="products" />
    <ProductList :products="products" @remove-product="removeProduct" />
   
  </div>
</template>

<script>
import ProductList from '../components/ProductList.vue'
import CombinedPriceChart from '../components/CombinedPriceChart.vue'
import { jwtDecode } from 'jwt-decode' // Importazione specifica


export default {
  name: 'DashboardPage',
  components: { ProductList, CombinedPriceChart },
  data() {
    return {
      productUrl: '',
      products: [],
      username: '',
      errorMessage: '',
      isLoading: false // Variabile per gestire il caricamento
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
        this.isLoading = true; // Attiva l'indicatore di caricamento
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
        await this.fetchProducts(); // Aggiorna la lista dei prodotti
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.isLoading = false; // Disattiva l'indicatore di caricamento
      }
    },



  async fetchProducts() {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/dashboard`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();

    // Aggiungi questo log per verificare i dati del prodotto e `price_history`
    console.log("Prodotti caricati:", data.products);

    this.products = data.products;
  } catch (error) {
    console.error('Errore nel caricamento dei prodotti:', error);
  }
},



    async removeProduct(asin) {
  const confirmDelete = confirm("Sei sicuro di voler eliminare questo prodotto dal monitoraggio?");
  if (!confirmDelete) {
    return; // Se l'utente annulla, interrompiamo la funzione
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

    await this.fetchProducts(); // Aggiorna la lista dei prodotti
  } catch (error) {
    console.error('Errore durante l\'eliminazione del prodotto:', error);
  }
}

  }
}
</script>
