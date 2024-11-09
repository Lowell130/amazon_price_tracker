<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Username" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      async login() {
        try {
          const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: this.username, password: this.password })
          });
          const data = await response.json();
          if (data.access_token) {
            localStorage.setItem('token', data.access_token);
            this.$router.push('/dashboard'); // Redirect alla dashboard dopo il login
          } else {
            alert('Login fallito');
          }
        } catch (error) {
          console.error('Errore nel login:', error);
        }
      }
    }
  }
  </script>
  