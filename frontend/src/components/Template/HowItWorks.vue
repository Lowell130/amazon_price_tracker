<template>
    <section class="bg-white dark:bg-gray-900 py-16 lg:py-24">
        <div class="max-w-screen-xl px-4 mx-auto text-center">
            <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-gray-900 md:text-4xl dark:text-white">
                Come funziona <span class="text-blue-600 dark:text-blue-500">PriceHub</span>?
            </h2>
            <p class="mb-12 text-lg font-light text-gray-500 dark:text-gray-400 sm:text-xl">
                Risparmiare sui tuoi acquisti Amazon è semplice come contare fino a 3.
            </p>
            
            <div class="grid gap-8 lg:gap-12 lg:grid-cols-3">
                <!-- Step 1 -->
                <div class="relative p-6 bg-white rounded-xl shadow-xl dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-shadow duration-300 group">
                    <div class="absolute -top-6 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg group-hover:scale-110 transition-transform">
                        1
                    </div>
                    <div class="mt-8 mb-4 flex justify-center text-blue-600 dark:text-blue-400">
                        <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
                    </div>
                    <h3 class="mb-2 text-xl font-bold dark:text-white">Copia il Link</h3>
                    <p class="text-gray-500 dark:text-gray-400">
                        Trova il prodotto che desideri su Amazon e copia l'URL dalla barra degli indirizzi o dall'app.
                    </p>
                </div>

                <!-- Step 2 -->
                <div class="relative p-6 bg-white rounded-xl shadow-xl dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-shadow duration-300 group">
                    <div class="absolute -top-6 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-purple-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg group-hover:scale-110 transition-transform">
                        2
                    </div>
                    <div class="mt-8 mb-4 flex justify-center text-purple-600 dark:text-purple-400">
                        <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
                    </div>
                    <h3 class="mb-2 text-xl font-bold dark:text-white">Incolla in PriceHub</h3>
                    <p class="text-gray-500 dark:text-gray-400">
                        Incolla il link nella tua dashboard. Noi recupereremo automaticamente tutti i dettagli.
                    </p>
                </div>

                <!-- Step 3 -->
                <div class="relative p-6 bg-white rounded-xl shadow-xl dark:bg-gray-800 border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-shadow duration-300 group">
                    <div class="absolute -top-6 left-1/2 transform -translate-x-1/2 w-12 h-12 bg-green-500 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg group-hover:scale-110 transition-transform">
                        3
                    </div>
                    <div class="mt-8 mb-4 flex justify-center text-green-500 dark:text-green-400">
                        <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                    <h3 class="mb-2 text-xl font-bold dark:text-white">Risparmia</h3>
                    <p class="text-gray-500 dark:text-gray-400">
                        Ricevi una notifica appena il prezzo scende. Compra al momento giusto e risparmia soldi veri.
                    </p>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'HowItWorks'
}
</script>
