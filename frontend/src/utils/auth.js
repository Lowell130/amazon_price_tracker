import router from '../router';

// Funzione per gestire gli errori di autenticazione
export function handleAuthError(error) {
  if (
    error.response &&
    error.response.status === 401 &&
    (error.response.data.detail === "Token scaduto" || error.response.data.detail === "Token non valido")
  ) {
    logoutAndRedirect();
  }
}

// Funzione per effettuare il logout e reindirizzare
export function logoutAndRedirect() {
  localStorage.removeItem('token'); // Rimuove il token
  router.push('/login'); // Reindirizza alla pagina di login
}
