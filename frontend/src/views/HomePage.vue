<template>
<div>
<HeroSection />


<FeatureSection />
</div>

 

  </template>
  
  <script>
import FeatureSection from '@/components/Template/FeatureSection.vue';
import HeroSection from '@/components/Template/HeroSection.vue';

  export default {
    name: 'HomePage',
    components: {
    HeroSection, FeatureSection
  }
  }
 
  </script>
  