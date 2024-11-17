export async function fetchWithToken(url, options = {}) {
  let token = localStorage.getItem("token");

  // Aggiungi l'header di autorizzazione con il token
  options.headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
  };

  // Esegui la richiesta
  let response = await fetch(url, options);

  // Controlla se il token è scaduto
  if (response.status === 401) {
    try {
      // Prova a ottenere un nuovo access token tramite refresh token
      const refreshResponse = await fetch(`${process.env.VUE_APP_API_BASE_URL}/refresh-token`, {
        method: "POST",
        credentials: "include",  // Questo include i cookie per il refresh token
      });

      if (refreshResponse.ok) {
        const refreshData = await refreshResponse.json();
        localStorage.setItem("token", refreshData.access_token);

        // Aggiorna l'header con il nuovo token e ripeti la richiesta originale
        options.headers.Authorization = `Bearer ${refreshData.access_token}`;
        response = await fetch(url, options);  // Riprova con il nuovo token
      } else {
        console.error("Impossibile aggiornare il token. Reindirizzamento al login.");
        handleLogout(); // Logout e redirect
      }
    } catch (error) {
      console.error("Errore durante il refresh del token:", error);
      handleLogout(); // Logout e redirect
    }
  }

  return response;
}

// Funzione per gestire il logout e reindirizzare
function handleLogout() {
  localStorage.removeItem("token"); // Rimuove il token
  window.location.href = "/login"; // Reindirizza alla pagina di login
}
