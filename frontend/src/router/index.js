import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from "jwt-decode"; // Importazione specifica
import HomePage from "../views/HomePage.vue";
import RegisterPage from "../views/RegisterPage.vue";
import LoginPage from "../views/LoginPage.vue";
import DashboardPage from "../views/DashboardPage.vue";
import ProfilePage from "../views/ProfilePage.vue";
import ProductDetail from "../views/ProductDetail.vue";
import SearchResults from "../views/SearchResults.vue"; // 🔥 Nuova pagina per la ricerca
import PasswordResetRequest from "../views/PasswordResetRequest.vue";
import PasswordReset from "../views/PasswordReset.vue";

const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/register", name: "Register", component: RegisterPage },
  { path: "/login", name: "Login", component: LoginPage },
  { path: "/dashboard", name: "Dashboard", component: DashboardPage, meta: { requiresAuth: true } },
  { path: "/profile", name: "Profile", component: ProfilePage, meta: { requiresAuth: true } },
  { path: "/products/:asin", name: "ProductDetail", component: ProductDetail }, // 🔥 RESO PUBBLICO
  { path: "/search", name: "SearchResults", component: SearchResults }, // 🔥 Nuova route per la ricerca dei prodotti
  { path: "/password-reset-request", name: "PasswordResetRequest", component: PasswordResetRequest },
  { path: "/reset-password", name: "ResetPassword", component: PasswordReset },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// Protezione delle route con autenticazione
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!token) {
      next("/login");
    } else {
      try {
        const decoded = jwtDecode(token);
        const now = Math.floor(Date.now() / 1000);
        if (decoded.exp > now) {
          next();
        } else {
          localStorage.removeItem("token");
          next("/login");
        }
      } catch {
        localStorage.removeItem("token");
        next("/login");
      }
    }
  } else {
    next(); // 🔥 Ora le pagine pubbliche possono essere visitate senza login
  }
});

export default router;
