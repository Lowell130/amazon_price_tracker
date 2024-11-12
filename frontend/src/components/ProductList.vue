<template>
  <div>
    <h2>I tuoi prodotti monitorati</h2>
    <ul class="product-list">
      <li v-for="product in sortedProducts" :key="product.asin" class="product-item">
        <div class="product-info">
          <img
            v-if="product.image_url"
            :src="product.image_url"
            alt="Product Image"
            class="product-image"
          />
          <div class="product-details">
            <h3>{{ product.title }}</h3>
            <p>ASIN: <strong>{{ product.asin }}</strong></p>
            <p>
              Prezzo Corrente:
              <strong :class="getPriceChangeClass(product)">
                {{ formatPrice(product.price) }}€
              </strong>
              <span v-if="getPriceChangePercentage(product) !== '0.00%'" :class="getPriceChangeClass(product)">
                ({{ getPriceChangePercentage(product) }})
              </span>
            </p>
            <p>Ultimo Prezzo Monitorato: <strong>{{ formatPrice(getLastMonitoredPrice(product)) }}€</strong></p>
          </div>
          <button @click="removeProduct(product.asin)" class="remove-button">
            Elimina
          </button>
        </div>
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
    };
  },
  computed: {
    sortedProducts() {
      return [...this.products].sort((a, b) => {
        const changeA = this.getPriceChangePercentage(a);
        const changeB = this.getPriceChangePercentage(b);
        return parseFloat(changeA) - parseFloat(changeB);
      });
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
      this.$emit('remove-product', asin);
    },
    getLastMonitoredPrice(product) {
      if (product.price_history && product.price_history.length > 1) {
        return product.price_history[product.price_history.length - 2].price;
      }
      return product.price;
    },
    getPriceChangePercentage(product) {
      const lastPrice = this.getLastMonitoredPrice(product);
      const currentPrice = parseFloat(product.price);
      const lastMonitored = parseFloat(lastPrice);

      if (lastMonitored) {
        const percentageChange = (((currentPrice - lastMonitored) / lastMonitored) * 100).toFixed(2);
        return (percentageChange > 0 ? `+${percentageChange}` : percentageChange) + '%';
      }
      return '0.00%';
    },
    getPriceChangeClass(product) {
      const percentageChange = parseFloat(this.getPriceChangePercentage(product));
      if (percentageChange < 0) {
        return 'price-decrease';
      } else if (percentageChange > 0) {
        return 'price-increase';
      }
      return '';
    },
    formatPrice(price) {
      return parseFloat(price).toFixed(2);
    }
  }
};
</script>

<style scoped>
.product-list {
  list-style: none;
  padding: 0;
}

.product-item {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 10px;
  transition: box-shadow 0.2s;
}

.product-item:hover {
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.product-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.product-image {
  width: 50px;
  height: auto;
  margin-right: 15px;
  border-radius: 4px;
}

.product-details {
  flex: 1;
}

.remove-button {
  background-color: #ff4d4f;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.remove-button:hover {
  background-color: #ff7875;
}

.price-decrease {
  color: green;
  font-weight: bold;
}

.price-increase {
  color: red;
  font-weight: bold;
}
</style>
