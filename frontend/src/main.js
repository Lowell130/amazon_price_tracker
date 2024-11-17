// src/main.js
import { createApp } from 'vue' // Usa createApp invece di importare Vue
import App from './App.vue'
import router from './router'
import './assets/main.css';


createApp(App).use(router).mount('#app') // Crea l'app Vue e monta il router
