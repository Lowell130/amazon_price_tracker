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
          const decodedToken = jwtDecode(token);
          this.username = decodedToken.sub; // Estrae il nome dell'utente dal token JWT
        }
      }
    }
  }
  </script>
  
  <style>
  /* Stili per la pagina Profilo */
  </style>
  