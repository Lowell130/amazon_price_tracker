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
}

</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>