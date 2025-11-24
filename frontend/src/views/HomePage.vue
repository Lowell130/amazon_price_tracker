<template>
  <div class="bg-gray-50 dark:bg-gray-900 min-h-screen">
    
    <!-- <TopMessage /> -->
    
    <!-- Hero Section: First impression -->
    <HeroSection />

    <!-- How It Works: Explain value prop immediately -->
    <HowItWorks />

    <!-- Live Deals: Show proof of value -->
    <HomePageSale />

    <!-- Features: Deep dive into capabilities -->
    <FeatureSection />

    <!-- Final CTA -->
    <section class="bg-white dark:bg-gray-800 py-16">
        <div class="max-w-screen-xl px-4 mx-auto text-center">
            <h2 class="mb-4 text-3xl font-extrabold tracking-tight text-gray-900 md:text-4xl dark:text-white">
                Pronto a risparmiare?
            </h2>
            <p class="mb-8 font-light text-gray-500 lg:mb-16 sm:text-xl dark:text-gray-400">
                Unisciti a migliaia di utenti che stanno già comprando al prezzo migliore.
            </p>
            <a href="/register" class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900">
                Crea il tuo account gratuito
            </a>
        </div>
    </section>

  </div>
</template>

<script>
import FeatureSection from '@/components/Template/FeatureSection.vue';
import HeroSection from '@/components/Template/HeroSection.vue';
import HowItWorks from '@/components/Template/HowItWorks.vue';
import HomePageSale from '@/components/HomePageSale.vue';
// import TopMessage from "@/components/TopMessage.vue";

export default {
  name: 'HomePage',
  components: {
    HeroSection,
    HowItWorks,
    FeatureSection,
    HomePageSale,
    // TopMessage
  },

};
</script>
