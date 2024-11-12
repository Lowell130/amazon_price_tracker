// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import LoginPage from '../views/LoginPage.vue';
import DashboardPage from '../views/DashboardPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import ProductDetail from '../views/ProductDetail.vue'; // Importa il nuovo componente

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/dashboard', name: 'Dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/products/:asin', name: 'ProductDetail', component: ProductDetail, meta: { requiresAuth: true } } // Nuova rotta per la pagina di dettaglio del prodotto
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Usa createWebHistory per la cronologia del browser
  routes
});

// Protezione delle rotte per autenticazione
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('token');
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;
