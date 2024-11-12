<template>
  <div class="product-detail">
    <button class="go-back-button" @click="$router.go(-1)">⬅️ Torna indietro</button>
    <h1>Storico dei prezzi per {{ productTitle }}</h1>

    <div v-if="priceHistory.length">
      <table class="price-history-table">
        <thead>
          <tr>
            <th>Data</th>
            <th>Prezzo (€)</th>
            <th>Variazione</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(entry, index) in priceHistory" :key="entry.date">
            <td>{{ formatDate(entry.date) }}</td>
            <td :class="getPriceClass(entry.price)">
              {{ parseFloat(entry.price).toFixed(2) }}€
            </td>
            <td v-if="index > 0">
              {{ getPriceChange(index) }}
            </td>
            <td v-else>-</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else>Nessun dato di storico disponibile.</p>
  </div>
</template>

<script>
export default {
  name: 'ProductDetail',
  data() {
    return {
      productTitle: '',
      priceHistory: []
    };
  },
  async created() {
    const asin = this.$route.params.asin; // Recupera l'ASIN dai parametri dell'URL
    await this.fetchPriceHistory(asin);
  },
  methods: {
    async fetchPriceHistory(asin) {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/price-history/${asin}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        this.priceHistory = data;
        this.productTitle = `Prodotto ${asin}`; // Sostituisci con il titolo reale se disponibile
      } catch (error) {
        console.error('Errore nel caricamento dello storico dei prezzi:', error);
      }
    },
    formatDate(date) {
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(date).toLocaleDateString('it-IT', options);
    },
    getPriceChange(index) {
      const previousPrice = parseFloat(this.priceHistory[index - 1].price);
      const currentPrice = parseFloat(this.priceHistory[index].price);
      const difference = currentPrice - previousPrice;
      const percentageChange = ((difference / previousPrice) * 100).toFixed(2);
      return `${difference > 0 ? '+' : ''}${percentageChange}%`;
    },
    getPriceClass(price) {
      const latestPrice = parseFloat(this.priceHistory[this.priceHistory.length - 1].price);
      const currentPrice = parseFloat(price);
      if (currentPrice > latestPrice) return 'price-high';
      if (currentPrice < latestPrice) return 'price-low';
      return '';
    }
  }
};
</script>

<style scoped>
.product-detail {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  text-align: center;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.go-back-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
}

.go-back-button:hover {
  background-color: #45a049;
}

h1 {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}

.price-history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.price-history-table th,
.price-history-table td {
  padding: 12px 15px;
  text-align: center;
}

.price-history-table th {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
  text-transform: uppercase;
}

.price-history-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.price-history-table tr:nth-child(odd) {
  background-color: #eaf5ea;
}

.price-history-table .price-high {
  color: #d9534f;
  font-weight: bold;
}

.price-history-table .price-low {
  color: #5cb85c;
  font-weight: bold;
}

.price-history-table td {
  border-bottom: 1px solid #ddd;
  transition: background-color 0.2s;
}

.price-history-table tr:hover td {
  background-color: #f1f1f1;
}

.price-history-table td:first-child {
  font-weight: bold;
  color: #333;
}
</style>
