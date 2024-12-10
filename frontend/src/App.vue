<template>
  <div id="app">
    



<HeaderTemplate />
    <router-view />
    <FooterTemplate />
  </div>
 
</template>

<script>


import FooterTemplate from './components/Template/FooterTemplate.vue';
import HeaderTemplate from './components/Template/HeaderTemplate.vue';

export default {
  components: {
    FooterTemplate, HeaderTemplate
  },
}

</script>

<style>
nav {
  padding: 1em;
  background-color: #f3f3f3;
}
nav a,
nav button {
  margin-right: 10px;
  text-decoration: none;
  color: #333;
}
</style>