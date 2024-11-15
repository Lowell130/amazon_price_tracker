<template>
  <div>
    <h1>Profilo Utente</h1>
    <p>Nome utente: {{ username }}</p>
    <p>Benvenuto nella tua area personale!</p>
  </div>
</template>

<script>
 import { jwtDecode } from 'jwt-decode' // Importazione specifica

export default {
  name: 'ProfilePage',
  data() {
    return {
      username: ''
    }
  },
  created() {
    this.getUserInfo();
  },
  methods: {
    getUserInfo() {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const decodedToken = jwtDecode(token);
          this.username = decodedToken.sub;  // Estrae l'username dal token JWT
        } catch (error) {
          console.error('Errore nella decodifica del token:', error);
          this.$router.push('/login');  // Reindirizza al login se il token non è valido
        }
      } else {
        this.$router.push('/login');  // Reindirizza al login se il token non è presente
      }
    }
  }
};
</script>
