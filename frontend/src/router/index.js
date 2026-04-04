import { createRouter, createWebHistory } from "vue-router";
import { jwtDecode } from "jwt-decode"; // Importazione specifica
import HomePage from "../views/HomePage.vue";

// Lazy Loading delle views per ottimizzare le prestazioni
const RegisterPage = () => import(/* webpackChunkName: "auth" */ "../views/RegisterPage.vue");
const LoginPage = () => import(/* webpackChunkName: "auth" */ "../views/LoginPage.vue");
const PasswordResetRequest = () => import(/* webpackChunkName: "auth" */ "../views/PasswordResetRequest.vue");
const PasswordReset = () => import(/* webpackChunkName: "auth" */ "../views/PasswordReset.vue");

const DashboardPage = () => import(/* webpackChunkName: "user" */ "../views/DashboardPage.vue");
const ProfilePage = () => import(/* webpackChunkName: "user" */ "../views/ProfilePage.vue");
const AnalysisPage = () => import(/* webpackChunkName: "user" */ "../views/AnalysisPage.vue");

const ProductDetail = () => import(/* webpackChunkName: "products" */ "../views/ProductDetail.vue");
const SearchResults = () => import(/* webpackChunkName: "products" */ "../views/SearchResults.vue");

const AdminUsersPage = () => import(/* webpackChunkName: "admin" */ "../views/AdminUsersPage.vue");
const AdminArticlesPage = () => import(/* webpackChunkName: "admin" */ "../views/AdminArticlesPage.vue");
const BlogPage = () => import(/* webpackChunkName: "public" */ "../views/BlogPage.vue");
const ArticleDetail = () => import(/* webpackChunkName: "public" */ "../views/ArticleDetail.vue");
const AdminAnalytics = () => import(/* webpackChunkName: "admin" */ "../views/AdminAnalytics.vue");
const AdminSettings = () => import(/* webpackChunkName: "admin" */ "../views/AdminSettings.vue");
const AdminTrendsPage = () => import(/* webpackChunkName: "admin" */ "../views/AdminTrendsPage.vue");

const routes = [
  { path: "/", name: "Home", component: HomePage },
  { path: "/register", name: "Register", component: RegisterPage, meta: { forbidsAuth: true } },
  { path: "/login", name: "Login", component: LoginPage, meta: { forbidsAuth: true } },
  { path: "/dashboard", name: "Dashboard", component: DashboardPage, meta: { requiresAuth: true } },
  { path: "/profile", name: "Profile", component: ProfilePage, meta: { requiresAuth: true } },
  { path: "/products/:asin", name: "ProductDetail", component: ProductDetail },
  { path: "/search", name: "SearchResults", component: SearchResults },
  { path: "/password-reset-request", name: "PasswordResetRequest", component: PasswordResetRequest },
  { path: "/reset-password", name: "ResetPassword", component: PasswordReset },
  { path: "/admin/users", name: "AdminUsers", component: AdminUsersPage, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: "/analysis", name: "Analysis", component: AnalysisPage, meta: { requiresAuth: true } },
  { path: "/admin/articles", name: "AdminArticles", component: AdminArticlesPage, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: "/blog", name: "Blog", component: BlogPage },
  { path: "/blog/:slug", name: "ArticleDetail", component: ArticleDetail },
  { path: "/admin/analytics", name: "AdminAnalytics", component: AdminAnalytics, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: "/admin/settings", name: "AdminSettings", component: AdminSettings, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: "/admin/trends", name: "AdminTrends", component: AdminTrendsPage, meta: { requiresAuth: true, requiresAdmin: true } },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (savedPosition) {
          resolve(savedPosition);
        } else {
          resolve({ top: 0, left: 0 });
        }
      }, 100);
    });
  },
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
          if (to.matched.some((record) => record.meta.requiresAdmin)) {
            if (decoded.admin) {
              next();
            } else {
              next("/"); // Redirect non-admins to home
            }
          } else {
            next();
          }
        } else {
          localStorage.removeItem("token");
          next("/login");
        }
      } catch {
        localStorage.removeItem("token");
        next("/login");
      }
    }
  } else if (to.matched.some((record) => record.meta.forbidsAuth)) {
    if (token) {
      next("/dashboard");
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
