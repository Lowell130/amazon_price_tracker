<template>
  <div id="app">
    



    <HeaderTemplate />
    <main class="pt-28 md:pt-32 min-h-screen">
      <router-view />
    </main>
    <FooterTemplate />
    <ToastNotification />
    <MascotWidget v-if="hasToken" />
  </div>
 
</template>

<script>


import FooterTemplate from './components/Template/FooterTemplate.vue';
import HeaderTemplate from './components/Template/HeaderTemplate.vue';
import ToastNotification from './components/ToastNotification.vue';
import MascotWidget from './components/Mascot/MascotWidget.vue';

export default {
  components: {
    FooterTemplate, 
    HeaderTemplate,
    ToastNotification,
    MascotWidget
  },
  data() {
    return {
      hasToken: !!localStorage.getItem('token')
    }
  },
  mounted() {
    this.trackVisit();
    // Watch for login/logout (storage for cross-tab, auth-state-changed for same tab)
    const updateToken = () => {
      this.hasToken = !!localStorage.getItem('token');
    };
    window.addEventListener('storage', updateToken);
    window.addEventListener('auth-state-changed', updateToken);
  },
  methods: {
    async trackVisit() {
      // Check if it's a new session or we already tracked this visit
      if (sessionStorage.getItem('visit_tracked')) return;

      const referrer = document.referrer;
      const urlParams = new URLSearchParams(window.location.search);
      
      // Common search parameters to track
      const searchParams = ['q', 's', 'search', 'query', 'utm_term'];
      let searchQuery = null;
      for (const param of searchParams) {
        if (urlParams.get(param)) {
          searchQuery = urlParams.get(param);
          break;
        }
      }
      
      const visitData = {
        referrer: referrer || 'direct',
        path: window.location.pathname,
        utm_source: urlParams.get('utm_source'),
        utm_medium: urlParams.get('utm_medium'),
        utm_campaign: urlParams.get('utm_campaign'),
        search_query: searchQuery
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