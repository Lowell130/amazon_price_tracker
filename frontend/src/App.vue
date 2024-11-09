<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link>
      <router-link v-if="!isAuthenticated" to="/register">Register</router-link>
      <router-link v-if="!isAuthenticated" to="/login">Login</router-link>
      <router-link v-if="isAuthenticated" to="/dashboard">Dashboard</router-link>
      <router-link v-if="isAuthenticated" to="/profile">Profile</router-link>
      <button v-if="isAuthenticated" @click="logout">Logout</button>
    </nav>
    <router-view /> <!-- Mostra il componente della pagina in base alla rotta attuale -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: !!localStorage.getItem('token') // Imposta lo stato di autenticazione
    }
  },
  watch: {
    // Monitora il token nel localStorage e aggiorna lo stato di autenticazione
    '$route'() {
      this.isAuthenticated = !!localStorage.getItem('token');
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token'); // Rimuove il token per il logout
      this.isAuthenticated = false; // Aggiorna lo stato di autenticazione
      this.$router.push('/login'); // Redirige al login
    }
  }
}
</script>

<style>
/* Stili semplici per la navbar */
nav {
  padding: 1em;
  background-color: #f3f3f3;
}
nav a, nav button {
  margin-right: 10px;
  text-decoration: none;
  color: #333;
}
</style>
