<template>
  <div>
    
    <TopMessage />
    <HomePageSale />
    <FeatureSection />
    <HeroSection />
  </div>
</template>

<script>
import FeatureSection from '@/components/Template/FeatureSection.vue';
import HeroSection from '@/components/Template/HeroSection.vue';
import HomePageSale from '@/components/HomePageSale.vue';
import TopMessage from "@/components/TopMessage.vue";

export default {
  name: 'HomePage',
  components: {
    HeroSection,
    FeatureSection,
    HomePageSale,
    TopMessage
  },

};
</script>
