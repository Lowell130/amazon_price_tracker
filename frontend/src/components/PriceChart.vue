<template>
    <div>
      <h3>Andamento del Prezzo per {{ title }}</h3>
      <div v-if="chartData && chartData.labels.length > 1">
        <!-- Visualizza il grafico solo se ci sono più di un punto storico -->
        <line-chart :chartData="chartData" :options="chartOptions" />
      </div>
      <div v-else>
        <p>Dati insufficienti per visualizzare il grafico dell'andamento del prezzo.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'
  
  // Registra i componenti necessari per Chart.js
  ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)
  
  export default {
    name: 'PriceChart',
    components: {
      LineChart: Line
    },
    props: {
      priceHistory: {
        type: Array,
        required: true
      },
      title: {
        type: String,
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
              text: 'Andamento del Prezzo'
            }
          },
          scales: {
            x: {
              title: {
                display: true,
                text: 'Data'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Prezzo (€)'
              }
            }
          }
        }
      }
    },
    watch: {
      // Osserva priceHistory e aggiorna chartData solo quando i dati sono disponibili
      priceHistory: {
        immediate: true,
        handler(newValue) {
          if (newValue && newValue.length > 1) { // Verifica che ci siano più di un punto storico
            this.chartData = {
              labels: newValue.map(entry => entry.date),
              datasets: [
                {
                  label: 'Prezzo (€)',
                  data: newValue.map(entry => parseFloat(entry.price)),
                  fill: false,
                  borderColor: 'blue',
                  tension: 0.1
                }
              ]
            }
          } else {
            this.chartData = { labels: [], datasets: [] }; // Reset se non ci sono dati sufficienti
          }
        }
      }
    }
  }
  </script>
  
  <style scoped>
  /* Stili opzionali per il grafico */
  </style>
  