<template>
  <div class="bg-white dark:bg-gray-800 p-6 md:p-8 rounded-3xl border border-gray-100 dark:border-gray-700 shadow-xl overflow-hidden">
    <div class="flex justify-between">
      <div>
        <h5 class="leading-none text-3xl font-bold text-gray-900 dark:text-white pb-2">
          {{ latestPrice }}€
        </h5>
        <p class="text-base font-normal text-gray-500 dark:text-gray-400">Attuale</p>
      </div>
 

      <div
  v-if="priceChange !== null"
  class="flex items-center px-2.5 py-0.5 text-base font-semibold text-gray-400 dark:text-gray-300"
  :class="{
    'text-red-500': priceChange > 0,
    'text-green-500': priceChange < 0,
    'text-gray-200 dark:text-gray-300': priceChange === 0
  }"
>
  {{ priceChange > 0 ? '+' : priceChange < 0 ? '' : '' }}{{ priceChange }}%
  <svg
    v-if="priceChange > 0 || priceChange < 0"
    class="w-3 h-3 ms-1"
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 10 14"
    :class="{
      'text-red-500': priceChange > 0,
      'text-green-500': priceChange < 0,
    }"
  >
    <path
      stroke="currentColor"
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      :d="priceChange > 0 ? 'M5 13V1m0 0L1 5m4-4 4 4' : 'M5 1v12m0 0L1 9m4 4 4-4'"
    />
  </svg>
  <svg
    v-else
    class="w-6 h-6 text-gray-200 dark:text-white ms-1"
    aria-hidden="true"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
  >
    <path
      stroke="currentColor"
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M8 20V7m0 13-4-4m4 4 4-4m4-12v13m0-13 4 4m-4-4-4 4"
    />
  </svg>
</div>


    </div>
    <div ref="chartContainer" class="min-h-[280px] w-full"></div>
  </div>
</template>

<script>
import ApexCharts from "apexcharts";

export default {
  name: "ChartPage",
  props: {
    priceHistory: {
      type: Array,
      required: true, // Assumiamo che priceHistory sia sempre fornito
    },
  },
  data() {
    return {
      latestPrice: null,
      priceChange: null,
      chart: null,
      chartData: null,
    };
  },
  mounted() {
    this.prepareData();
    this.renderChart();
  },
  methods: {
    prepareData() {
      // Estrai prezzi e date
      const prices = this.priceHistory.map((entry) => parseFloat(entry.price));
      const dates = this.priceHistory.map((entry) =>
        new Date(entry.date).toLocaleDateString("it-IT", {
          year: "numeric",
          month: "short",
          day: "numeric",
        })
      );

      this.latestPrice = prices[prices.length - 1];

      if (prices.length > 1) {
        const previousPrice = prices[prices.length - 2];
        this.priceChange = (((this.latestPrice - previousPrice) / previousPrice) * 100).toFixed(2);
      } else {
        this.priceChange = null;
      }

      this.chartData = { dates, prices };
    },
    renderChart() {
      if (!this.chartData || !this.$refs.chartContainer) return;

      const options = {
        chart: {
          type: "area",
          height: "100%",
          fontFamily: "Inter, sans-serif",
          toolbar: { show: false },
          zoom: { enabled: false },
          sparkline: { enabled: false }
        },
        tooltip: {
          enabled: true,
          theme: 'dark',
          x: { show: true, format: 'dd MMM' },
          style: { fontSize: '12px' },
          custom: function({series, seriesIndex, dataPointIndex, w}) {
            return '<div class="px-4 py-2 bg-slate-900 text-white border-blue-500 border-l-4 shadow-xl rounded-lg font-bold">' +
              '<span class="text-[10px] text-gray-400 block uppercase tracking-widest mb-1">' + w.globals.categoryLabels[dataPointIndex] + '</span>' +
              '<span class="text-lg">' + series[seriesIndex][dataPointIndex] + ' €</span>' +
              '</div>'
          }
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.45,
            opacityTo: 0.05,
            stops: [20, 100],
            gradientToColors: ["#3b82f6"],
          },
        },
        markers: {
          size: 0,
          colors: ["#3b82f6"],
          strokeColors: "#fff",
          strokeWidth: 2,
          hover: { size: 6 }
        },
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth', width: 4, lineCap: 'round' },
        grid: {
          show: true,
          borderColor: 'rgba(156, 163, 175, 0.1)',
          strokeDashArray: 4,
          padding: { left: 10, right: 10, top: 0, bottom: 20 }
        },
        series: [
          {
            name: "Prezzo",
            data: this.chartData.prices,
            color: "#3b82f6",
          },
        ],
        xaxis: {
          categories: this.chartData.dates,
          labels: {
            show: false,
            style: { colors: '#94a3b8', fontSize: '10px', fontWeight: 600 },
            rotate: -45,
            offsetY: 5
          },
          axisBorder: { show: false },
          axisTicks: { show: false },
        },
        yaxis: {
          labels: {
            show: true,
            style: { colors: '#94a3b8', fontSize: '10px', fontWeight: 600 },
            formatter: (val) => val.toFixed(0) + '€'
          }
        },
      };

      this.chart = new ApexCharts(this.$refs.chartContainer, options);
      this.chart.render();
    },
  },
  watch: {
    priceHistory: {
      immediate: true,
      handler() {
        if (this.chart) {
          this.chart.destroy();
        }
        this.prepareData();
        this.renderChart();
      },
    },
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy();
    }
  },
};
</script>
