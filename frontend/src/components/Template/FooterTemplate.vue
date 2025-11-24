<template>
  <footer class="relative p-4 bg-white md:p-8 lg:p-10 dark:bg-gray-800">
    <div class="mx-auto max-w-screen-xl text-center">
      <div href="#" class="flex justify-center items-center text-2xl font-semibold text-gray-900 dark:text-white">
           PriceHub.it
      </div>
      <p class="my-6 text-sm text-gray-500 dark:text-white">
        PriceHub.it è un'applicazione web intuitiva progettata per aiutare gli utenti a monitorare le variazioni di prezzo dei loro prodotti preferiti su Amazon. Aggiungi prodotti, traccia lo storico dei prezzi, imposta i preferiti e ricevi avvisi sui ribassi. Semplifica la tua esperienza di shopping con un monitoraggio intelligente e approfondimenti utili.
        <br /><br />
        PriceHub.it partecipa al <span class="font-bold">Programma Affiliazione di Amazon Europa</span>, un programma che consente ai siti di percepire una commissione pubblicitaria fornendo link ad Amazon.it. Ciò significa che, se effettui un acquisto tramite i nostri link, potremmo ricevere una commissione senza alcun costo aggiuntivo per te.
      </p>
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
