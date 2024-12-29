<template>
  <div class="bg-white dark:bg-gray-800 p-4 md:p-6 rounded-b-lg">
    <div class="flex justify-between">
      <div>
        <h5 class="leading-none text-3xl font-bold text-gray-900 dark:text-white pb-2">
          {{ latestPrice }}€
        </h5>
        <p class="text-base font-normal text-gray-500 dark:text-gray-400">Latest Price</p>
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
    <div ref="chartContainer" class="h-50 w-full"></div>
    <div class="grid grid-cols-1 items-center border-gray-200 border-t dark:border-gray-700 justify-between">
      <div class="flex justify-between items-center pt-5">
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Price History</p>
      </div>
    </div>
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
          toolbar: { show: true },
          zoom: { enabled: false }, // Disabilita lo zoom
        },
        tooltip: { enabled: true, x: { show: false } },
        fill: {
          type: "gradient",
          gradient: {
            opacityFrom: 0.55,
            opacityTo: 0,
            gradientToColors: ["#1C64F2"],
          },
        },
        dataLabels: { enabled: false },
        stroke: { width: 6 },
        grid: { show: false, strokeDashArray: 4, padding: { left: 10, right: 2, top: 0 } },
        series: [
          {
            name: "Price",
            data: this.chartData.prices,
            color: "#1A56DB",
          },
        ],
        xaxis: {
          categories: this.chartData.dates,
          labels: { show: false },
          axisBorder: { show: false },
          axisTicks: { show: false },
        },
        yaxis: { show: true },
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
