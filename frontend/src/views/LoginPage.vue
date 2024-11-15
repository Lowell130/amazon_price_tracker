<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button v-if="!isLoading" type="submit">Login</button>
      <div v-else class="loading-animation">Caricamento...</div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      isLoading: false
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      try {
        const response = await fetch(`${process.env.VUE_APP_API_BASE_URL}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username, password: this.password })
        });
        
        const data = await response.json();
        
        if (data.access_token) {
          localStorage.setItem('token', data.access_token);  // Salva il token nel localStorage
          this.$router.push('/dashboard');  // Redirect alla dashboard
        } else {
          alert('Login fallito');
        }
      } catch (error) {
        console.error('Errore nel login:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.loading-animation {
  font-size: 16px;
  color: #333;
  margin-top: 10px;
  text-align: center;
}
</style>
