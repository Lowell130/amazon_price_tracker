<template>
  <div>
    <HeroSection />
    <HomePageSale />
    <FeatureSection />
  </div>
</template>

<script>
import FeatureSection from '@/components/Template/FeatureSection.vue';
import HeroSection from '@/components/Template/HeroSection.vue';
import HomePageSale from '@/components/HomePageSale.vue';

export default {
  name: 'HomePage',
  components: {
    HeroSection,
    FeatureSection,
    HomePageSale
  },

};
</script>
