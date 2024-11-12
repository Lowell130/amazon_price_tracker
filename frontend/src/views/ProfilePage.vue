<template>
  <div>
    <h1>Profilo Utente</h1>
    <p>Nome utente: {{ username }}</p>
    <p>Benvenuto nella tua area personale!</p>
  </div>
</template>

<script>
 import { jwtDecode } from 'jwt-decode' // Importazione specifica
import { handleAuthError } from '../utils/auth';

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
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const decodedToken = jwtDecode(token);
          this.username = decodedToken.sub; // Estrae il nome dell'utente dal token JWT
        }
      } catch (error) {
        handleAuthError(error);
        console.error('Errore nella decodifica del token:', error);
      }
    }
  }
}
</script>
