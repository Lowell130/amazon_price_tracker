<template>
    <section class="relative bg-white dark:bg-gray-900 overflow-hidden">
        <!-- Background Gradient Blob -->
        <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
            <div class="absolute -top-[10%] -left-[10%] w-[50%] h-[50%] rounded-full bg-purple-400/30 blur-[100px] animate-blob"></div>
            <div class="absolute top-[20%] -right-[10%] w-[40%] h-[60%] rounded-full bg-blue-400/30 blur-[100px] animate-blob animation-delay-2000"></div>
            <div class="absolute -bottom-[10%] left-[20%] w-[60%] h-[40%] rounded-full bg-pink-400/30 blur-[100px] animate-blob animation-delay-4000"></div>
        </div>

        <div class="relative z-10 grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-24 lg:grid-cols-12">
            <div class="mr-auto place-self-center lg:col-span-7">
                <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white">
                    Smetti di pagare troppo su <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400">Amazon</span>
                </h1>
                <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-300">
                    Il monitoraggio prezzi intelligente che stavi aspettando. Traccia i prodotti, analizza lo storico e ricevi notifiche istantanee quando il prezzo scende. <span class="font-semibold text-gray-900 dark:text-white">Gratis per sempre.</span>
                </p>
                <div class="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
                    <a href="/register" class="inline-flex items-center justify-center px-6 py-3.5 text-base font-medium text-center text-white rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-300 dark:focus:ring-blue-900 shadow-lg shadow-blue-500/30 transition-transform transform hover:-translate-y-1">
                        Inizia a Risparmiare
                        <svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                    </a>
                    <a href="/login" class="inline-flex items-center justify-center px-6 py-3.5 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800 backdrop-blur-sm bg-white/50 dark:bg-gray-800/50 transition-transform transform hover:-translate-y-1">
                        Accedi
                    </a> 
                </div>
            </div>
            <div class="hidden lg:mt-0 lg:col-span-5 lg:flex relative">
                <!-- Decorative Elements behind image -->
                <div class="absolute inset-0 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-full blur-3xl opacity-20 animate-pulse"></div>
                <img :src="require('@/assets/hero-image.png')" alt="App Mockup" class="relative z-10 drop-shadow-2xl transform hover:scale-105 transition-transform duration-500">
            </div>                
        </div>
    </section>
</template>

<style scoped>
@keyframes blob {
    0% { transform: translate(0px, 0px) scale(1); }
    33% { transform: translate(30px, -50px) scale(1.1); }
    66% { transform: translate(-20px, 20px) scale(0.9); }
    100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
    animation: blob 7s infinite;
}
.animation-delay-2000 {
    animation-delay: 2s;
}
.animation-delay-4000 {
    animation-delay: 4s;
}
</style>
