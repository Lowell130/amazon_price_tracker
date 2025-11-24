<template>
    <section class="bg-gray-50 dark:bg-gray-900 py-16 lg:py-24">
      <div class="py-8 px-4 mx-auto max-w-screen-xl sm:py-16 lg:px-6">
          <div class="max-w-screen-md mb-8 lg:mb-16 text-center mx-auto">
              <h2 class="mb-4 text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white">
                 Tutto ciò che ti serve per <span class="text-blue-600">comprare meglio</span>
              </h2>
              <p class="text-gray-500 sm:text-xl dark:text-gray-400">
                PriceHub non è solo un tracker. È il tuo assistente personale per lo shopping intelligente.
              </p>
          </div>
          <div class="space-y-8 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-12 md:space-y-0">
              <!-- Feature 1 -->
              <div class="p-8 bg-white/60 dark:bg-gray-800/60 backdrop-blur-lg rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                  <div class="flex justify-center items-center mb-4 w-12 h-12 rounded-xl bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-300">
                      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                      </svg>
                  </div>
                  <h3 class="mb-2 text-xl font-bold dark:text-white">Cronologia Completa</h3>
                  <p class="text-gray-500 dark:text-gray-400">
                      Visualizza grafici dettagliati dell'andamento dei prezzi. Scopri se l'offerta di oggi è davvero un affare o se il prezzo è stato gonfiato.
                  </p>
              </div>

              <!-- Feature 2 -->
              <div class="p-8 bg-white/60 dark:bg-gray-800/60 backdrop-blur-lg rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                  <div class="flex justify-center items-center mb-4 w-12 h-12 rounded-xl bg-purple-100 dark:bg-purple-900/50 text-purple-600 dark:text-purple-300">
                      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z"></path>
                      </svg>
                  </div>
                  <h3 class="mb-2 text-xl font-bold dark:text-white">Avvisi in Tempo Reale</h3>
                  <p class="text-gray-500 dark:text-gray-400">
                      Non perdere mai un'offerta. Ricevi una notifica via email o Telegram non appena il prezzo tocca la soglia desiderata.
                  </p>
              </div>

              <!-- Feature 3 -->
              <div class="p-8 bg-white/60 dark:bg-gray-800/60 backdrop-blur-lg rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                  <div class="flex justify-center items-center mb-4 w-12 h-12 rounded-xl bg-green-100 dark:bg-green-900/50 text-green-600 dark:text-green-300">
                      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                          <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd"></path><path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z"></path>
                      </svg>                    
                  </div>
                  <h3 class="mb-2 text-xl font-bold dark:text-white">Controllo Totale</h3>
                  <p class="text-gray-500 dark:text-gray-400">
                      Organizza i tuoi prodotti, aggiorna i prezzi manualmente quando vuoi e gestisci la tua lista dei desideri in un unico posto.
                  </p>
              </div>
          </div>
      </div>
    </section>
</template>
