<template>
    <div>
      <h3>Andamento Prezzi di Tutti i Prodotti Monitorati</h3>
      <line-chart v-if="chartData && chartData.datasets.length" :chartData="chartData" :options="chartOptions" />
      <div v-else>
        <p>Dati insufficienti per visualizzare il grafico dell'andamento dei prezzi dei prodotti.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { Line } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'
  
  // Registra i componenti necessari per Chart.js
  ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)
  
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
    mounted() {
      this.generateChartData()
    },
    methods: {
      generateChartData() {
        const allDates = new Set()
  
        // Prepara un set di date uniche per il grafico
        this.products.forEach(product => {
          if (product.price_history && product.price_history.length > 1) {
            product.price_history.forEach(entry => allDates.add(entry.date))
          }
        })
  
        const sortedDates = Array.from(allDates).sort()
        this.chartData.labels = sortedDates
  
        // Genera una linea per ogni prodotto solo se ha più di un punto dati
        this.chartData.datasets = this.products
          .filter(product => product.price_history && product.price_history.length > 1)
          .map((product, index) => {
            const color = `hsl(${(index * 50) % 360}, 70%, 50%)` // Colore unico per ogni prodotto
            const dataPoints = sortedDates.map(date => {
              const entry = product.price_history.find(e => e.date === date)
              return entry ? parseFloat(entry.price) : null // Usa `null` se non ci sono dati per una data
            })
  
            return {
              label: product.title,
              data: dataPoints,
              fill: false,
              borderColor: color,
              tension: 0.1
            }
          })
      }
    }
  }
  </script>
  
  <style scoped>
  /* Stili opzionali per il grafico */
  </style>
  