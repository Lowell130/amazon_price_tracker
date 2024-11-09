<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="register">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RegisterPage',
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      async register() {
        try {
          await fetch(`${process.env.VUE_APP_API_BASE_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: this.username, password: this.password })
          });
          this.$router.push('/login'); // Redirect al login dopo la registrazione
        } catch (error) {
          console.error('Errore nella registrazione:', error);
        }
      }
    }
  }
  </script>
  