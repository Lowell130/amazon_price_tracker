<template>
  <div id="app">
    



    <HeaderTemplate />
    <main class="pt-28 md:pt-32 min-h-screen">
      <router-view />
    </main>
    <FooterTemplate />
    <ToastNotification />
  </div>
 
</template>

<script>


import FooterTemplate from './components/Template/FooterTemplate.vue';
import HeaderTemplate from './components/Template/HeaderTemplate.vue';
import ToastNotification from './components/ToastNotification.vue';

export default {
  components: {
    FooterTemplate, 
    HeaderTemplate,
    ToastNotification
  },
  mounted() {
    this.trackVisit();
  },
  methods: {
    async trackVisit() {
      // Check if it's a new session or we already tracked this visit
      if (sessionStorage.getItem('visit_tracked')) return;

      const referrer = document.referrer;
      const urlParams = new URLSearchParams(window.location.search);
      
      const visitData = {
        referrer: referrer || 'direct',
        path: window.location.pathname,
        utm_source: urlParams.get('utm_source'),
        utm_medium: urlParams.get('utm_medium'),
        utm_campaign: urlParams.get('utm_campaign')
      };

      try {
        await fetch(`${process.env.VUE_APP_API_BASE_URL}/analytics/visit`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(visitData)
        });
        sessionStorage.setItem('visit_tracked', 'true');
        if (referrer && !referrer.includes(window.location.hostname)) {
          sessionStorage.setItem('original_referrer', referrer);
        }
      } catch (e) {
        console.error("Analytics error:", e);
      }
    }
  }
}

</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>