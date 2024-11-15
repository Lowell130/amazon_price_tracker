<template>
  <div>
    <h3>Andamento Prezzi di Tutti i Prodotti Monitorati</h3>
    <line-chart
      v-if="chartData && chartData.labels.length && chartData.datasets.length"
      :key="chartKey"
      :data="chartData"
      :options="chartOptions"
    />
    <div v-else>
      <p>Dati insufficienti per visualizzare il grafico dell'andamento dei prezzi dei prodotti.</p>
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default {
  name: 'CombinedPriceChart',
  components: {
    LineChart: Line
  },
  props: {
    products: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: []
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            display: true
          },
          title: {
            display: true,
            text: 'Andamento Prezzi dei Prodotti'
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Data e Ora (hh:mm)'
            },
            ticks: {
        display: false // Nasconde le etichette delle date sull'asse X
      }
          },
          y: {
            title: {
              display: true,
              text: 'Prezzo (€)'
            }
          }
        }
      },
      chartKey: 0 // Chiave dinamica per forzare il re-render
    };
  },
  watch: {
    products: {
      handler() {
        this.generateChartData();
        this.chartKey += 1;
      },
      immediate: true,
      deep: true
    }
  },
  methods: {
    generateChartData() {
      // Consolida le date ignorando i secondi, mantenendo solo data, ora e minuti
      const uniqueDateTimes = Array.from(new Set(
        this.products.flatMap(product =>
          product.price_history
            ? product.price_history.map(entry => entry.date.substring(0, 16)) // Conserva solo data, ora e minuti
            : []
        )
      )).sort();

      this.chartData.labels = uniqueDateTimes;

      // Funzione di conversione del prezzo
      const convertPrice = (price) => {
        const sanitizedPrice = price.replace(/\.(?=\d{3})/g, '').replace(',', '.');
        return parseFloat(sanitizedPrice);
      };

      // Genera dataset per ogni prodotto e converte i prezzi
      this.chartData.datasets = this.products.map((product, index) => {
        const color = `hsl(${(index * 50) % 360}, 70%, 50%)`;
        let lastKnownPrice = null;

        const dataPoints = uniqueDateTimes.map(dateTime => {
          // Trova il prezzo senza considerare i secondi
          const entry = product.price_history?.find(e => e.date.startsWith(dateTime));
          if (entry) {
            lastKnownPrice = convertPrice(entry.price);
            return lastKnownPrice;
          } else {
            return lastKnownPrice;
          }
        });

        return {
          label: product.asin,
          data: dataPoints,
          fill: false,
          borderColor: color,
          backgroundColor: color,
          borderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointBackgroundColor: color,
          tension: 0.2,
          borderDash: index % 2 === 0 ? [] : [5, 5]
        };
      });

      // Configura l'asse Y
      const allPrices = this.chartData.datasets.flatMap(dataset => dataset.data).filter(price => price !== null);
      const minPrice = Math.min(...allPrices);
      const maxPrice = Math.max(...allPrices);

      this.chartOptions.scales.y = {
        ...this.chartOptions.scales.y,
        min: minPrice - 10,
        max: maxPrice + 10,
        reverse: false
      };
    }
  }
};
</script>

<style scoped>
/* Stili opzionali per il grafico */
</style>
