import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import RegisterPage from '../views/RegisterPage.vue';
import LoginPage from '../views/LoginPage.vue';
import DashboardPage from '../views/DashboardPage.vue';
import ProfilePage from '../views/ProfilePage.vue';
import ProductDetail from '../views/ProductDetail.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/dashboard', name: 'Dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: ProfilePage, meta: { requiresAuth: true } },
  { path: '/products/:asin', name: 'ProductDetail', component: ProductDetail, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');  // Verifica se il token è presente

  if (to.matched.some(record => record.meta.requiresAuth) && !token) {
    // Se la rotta richiede autenticazione e non c'è il token, reindirizza al login
    next('/login');
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    // Se l'utente è già autenticato e cerca di accedere al login o registrazione, reindirizzalo alla dashboard
    next('/dashboard');
  } else {
    next();  // Altrimenti, continua con la navigazione
  }
});

export default router;
