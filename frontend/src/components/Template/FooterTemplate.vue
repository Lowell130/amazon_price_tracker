<template>
  <footer class="relative p-4 bg-white md:p-8 lg:p-10 dark:bg-gray-800">
    <div class="mx-auto max-w-screen-xl text-center">
      <div class="flex justify-center items-center text-2xl font-black text-gray-900 dark:text-white mb-6">
        <div class="p-1.5 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-600 shadow-md mr-3">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        PriceHub.it
      </div>
      <div class="max-w-3xl mx-auto my-8 text-sm text-gray-500 dark:text-gray-400 space-y-4">
        <p>
          <span class="font-bold text-gray-900 dark:text-white">PriceHub.it</span> è lo strumento intelligente per il monitoraggio dei prezzi su Amazon. Ti aiutiamo a risparmiare analizzando lo storico dei prezzi, impostando avvisi in tempo reale e offrendoti insight basati sull'intelligenza artificiale per i tuoi acquisti.
        </p>
        <p class="text-xs opacity-75 italic leading-relaxed">
          In qualità di Affiliato Amazon, <span class="not-italic font-medium text-gray-900 dark:text-white">PriceHub.it</span> riceve un guadagno dagli acquisti idonei. PriceHub.it partecipa al Programma Affiliazione Amazon EU, un programma pubblicitario che consente ai siti di percepire una commissione pubblicitaria tramite i link ad Amazon.it. Come affiliato, riceviamo una piccola commissione sugli acquisti idonei, senza alcun costo aggiuntivo per te.
        </p>
      </div>
      <span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">
        © {{ currentYear }} All Rights Reserved.
      </span>
    </div>

    <button
      v-if="showScrollTop"
      @click="scrollToTop"
      class="fixed bottom-4 right-4 z-50 bg-gray-800 text-white p-3 rounded-full shadow-lg hover:bg-gray-700 dark:bg-gray-600 dark:hover:bg-gray-500"
    >
      <svg class="w-[27px] h-[27px] text-white dark:text-gray-800" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 6v13m0-13 4 4m-4-4-4 4" />
      </svg>
    </button>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      showScrollTop: false,
    };
  },
  computed: {
    currentYear() {
      return new Date().getFullYear();
    },
  },
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    handleScroll() {
      this.showScrollTop = window.scrollY > 200;
    },
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
button {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}
button:hover {
  transform: translateY(-2px);
}
</style>
