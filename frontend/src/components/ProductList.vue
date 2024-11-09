<template>
    <div>
      <h2>I tuoi prodotti monitorati</h2>
      <ul>
        <li v-for="product in products" :key="product.asin">
        <img v-if="product.image_url" :src="product.image_url" alt="Product Image" style="width: 150px; height: auto; margin-right: 10px;">
       ASIN: {{ product.asin }} - {{ product.title }} - Prezzo corrente: {{ product.price }}
        <button @click="removeProduct(product.asin)">Elimina</button>
      </li>
      <li v-if="products.length == 0">
non ci sono prodotti
      </li>
      </ul>
      <PriceHistory v-if="priceHistory.length" :history="priceHistory" />
    </div>
  </template>
  
  <script>
  import PriceHistory from './PriceHistory.vue';
  
  export default {
    components: { PriceHistory },
    props: ['products'],
    data() {
      return {
        priceHistory: []
      }
    },
    methods: {
      async showPriceHistory(asin) {
        try {
          const token = localStorage.getItem('token');
          const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/price-history/${asin}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          this.priceHistory = await response.json();
        } catch (error) {
          console.error('Errore nel caricamento dello storico dei prezzi:', error);
        }
      },
      async removeProduct(asin) {
      this.$emit('remove-product', asin); // Invia l'asin al componente parent
    }
    }
  }
  </script>
  