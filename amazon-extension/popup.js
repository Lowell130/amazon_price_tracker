const API_BASE = "http://127.0.0.1:8000";

/**
 * Toast con icone (success, error, info)
 */
function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.style.padding = "10px 14px";
    toast.style.borderRadius = "8px";
    toast.style.fontSize = "13px";
    toast.style.color = "white";
    toast.style.boxShadow = "0 2px 6px rgba(0,0,0,0.15)";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.25s ease";
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.gap = "8px";

    let bg = "#6b7280";
    let iconChar = "ℹ️";
    if (type === "success") {
        bg = "linear-gradient(to right, #16a34a, #22c55e)";
        iconChar = "✔️";
    } else if (type === "error") {
        bg = "linear-gradient(to right, #dc2626, #ef4444)";
        iconChar = "❌";
    } else if (type === "info") {
        bg = "linear-gradient(to right, #2563eb, #3b82f6)";
        iconChar = "ℹ️";
    }
    toast.style.background = bg;

    const icon = document.createElement("span");
    icon.textContent = iconChar;
    icon.style.fontSize = "14px";

    const text = document.createElement("span");
    text.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(text);
    container.appendChild(toast);

    // Animazione entrata
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });

    // Rimozione automatica
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(10px)";
        setTimeout(() => toast.remove(), 200);
    }, 2500);
}

/**
 * Gestione stato loading sui bottoni (testo + spinner)
 */
function setButtonLoading(button, isLoading, loadingText, useDarkSpinner = false) {
    if (!button) return;

    if (isLoading) {
        button.disabled = true;
        button.dataset.originalText = button.dataset.originalText || button.textContent;
        button.innerHTML = "";
        const spinner = document.createElement("span");
        spinner.className = "spinner" + (useDarkSpinner ? " spinner-dark" : "");
        const spanText = document.createElement("span");
        spanText.textContent = loadingText || "Attendere...";
        button.appendChild(spinner);
        button.appendChild(spanText);
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || button.textContent;
    }
}

/**
 * Funzione per bonificare il link Amazon (come nel frontend)
 */
function cleanAmazonUrl(url) {
    const match = url.match(
        /(https?:\/\/(?:www\.)?amazon\.[a-z.]+(?:\/.*)?\/(?:dp|gp\/product)\/[A-Z0-9]{10})/i
    );
    return match ? match[0] : url;
}

document.addEventListener("DOMContentLoaded", () => {
    console.log("Popup caricato");

    const loginSection = document.getElementById("login-section");
    const productSection = document.getElementById("product-section");
    const loginBtn = document.getElementById("login-btn");
    const logoutBtn = document.getElementById("logout-btn");
    const productUrlEl = document.getElementById("product-url");
    const asinEl = document.getElementById("asin-value");
    const productStatusEl = document.getElementById("product-status");
    const categorySelect = document.getElementById("category");
    let addProductBtn = document.getElementById("add-product");

    // Ricorda ultima categoria scelta
    const savedCategory = localStorage.getItem("last_category");
    if (savedCategory) {
        const option = Array.from(categorySelect.options).find(
            (opt) => opt.value === savedCategory
        );
        if (option) categorySelect.value = savedCategory;
    }
    categorySelect.addEventListener("change", () => {
        localStorage.setItem("last_category", categorySelect.value);
    });

    // --------- FUNZIONI UI ---------

    function showLoginSection() {
        loginSection.style.display = "block";
        productSection.style.display = "none";
    }

    function showProductSection() {
        console.log("Mostro la schermata prodotti");

        loginSection.style.display = "none";
        productSection.style.display = "block";
        productStatusEl.textContent = "";
        productUrlEl.classList.remove("already-tracked");
        asinEl.textContent = "-";

        // Ottieni tab attiva
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            const tabId = tabs[0].id;

            // Inietta il content script
            chrome.scripting.executeScript(
                {
                    target: { tabId },
                    files: ["content.js"],
                },
                () => {
                    console.log("Content script iniettato!");

                    chrome.tabs.sendMessage(
                        tabId,
                        { action: "getProductUrl" },
                        async (response) => {
                            console.log("Risposta ricevuta da content.js:", response);

                            if (response && response.product_url) {
                                productUrlEl.innerText = response.product_url;

                                const asin = response.asin;
                                if (asin) {
                                    asinEl.textContent = asin;
                                    await checkIfProductAlreadyTracked(asin);
                                } else {
                                    asinEl.textContent = "Non rilevato";
                                    productStatusEl.textContent =
                                        "ASIN non rilevato dall'URL. Il prodotto verrà comunque aggiunto usando l'URL.";
                                    showToast(
                                        "ASIN non rilevato, uso solo l'URL del prodotto.",
                                        "info"
                                    );
                                }

                                // Evita listener multipli
                                addProductBtn.replaceWith(addProductBtn.cloneNode(true));
                                addProductBtn = document.getElementById("add-product");
                                addProductBtn.addEventListener("click", () =>
                                    addProduct(response.product_url)
                                );
                            } else {
                                console.error("Errore: Nessun URL ricevuto!");
                                productUrlEl.innerText =
                                    "Errore nel caricamento del prodotto (sei su una pagina Amazon?)";
                                asinEl.textContent = "-";
                                productStatusEl.textContent = "";
                                showToast(
                                    "Impossibile leggere l'URL del prodotto.",
                                    "error"
                                );
                            }
                        }
                    );
                }
            );
        });
    }

    // --------- TOKEN & REFRESH ---------

    async function getTokenOrRefresh() {
        let token = localStorage.getItem("token");
        if (!token) {
            console.warn("Nessun token presente");
            return null;
        }

        try {
            const response = await fetch(`${API_BASE}/api/auth/refresh-token`, {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const data = await response.json().catch(() => ({}));
            console.log("Risposta refresh-token:", response.status, data);

            if (response.ok && data.access_token) {
                localStorage.setItem("token", data.access_token);
                return data.access_token;
            }

            if (response.status === 401) {
                localStorage.removeItem("token");
                showToast("Sessione scaduta, effettua di nuovo il login.", "error");
                showLoginSection();
                return null;
            }

            return token;
        } catch (err) {
            console.error("Errore durante il refresh token:", err);
            return token;
        }
    }

    // --------- CHECK SE PRODOTTO ESISTE GIÀ ---------

    async function checkIfProductAlreadyTracked(asin) {
        if (!asin) return;

        const token = await getTokenOrRefresh();
        if (!token) return;

        try {
            const response = await fetch(`${API_BASE}/api/dashboard`, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const data = await response.json().catch(() => ({}));
            console.log("Risposta dashboard per check prodotto:", response.status, data);

            if (response.ok && Array.isArray(data.products)) {
                const found = data.products.find((p) => p.asin === asin);
                if (found) {
                    productUrlEl.classList.add("already-tracked");
                    productStatusEl.textContent =
                        "Questo prodotto è già presente nel tuo tracker.";
                    showToast(
                        "Questo prodotto è già presente nel tuo tracker.",
                        "info"
                    );
                }
            }
        } catch (err) {
            console.error("Errore durante il check prodotto:", err);
        }
    }

    // --------- INIT: controlla sessione ---------

    (async () => {
        const rawToken = localStorage.getItem("token");
        if (!rawToken) {
            showLoginSection();
            return;
        }

        const validToken = await getTokenOrRefresh();
        if (validToken) {
            showProductSection();
        } else {
            showLoginSection();
        }
    })();

    // --------- LOGIN ---------

    loginBtn.addEventListener("click", async () => {
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();

        console.log("Tentativo di login con:", username, password);

        if (!username || !password) {
            showToast("Inserisci username/email e password.", "error");
            return;
        }

        setButtonLoading(loginBtn, true, "Accesso in corso...");

        try {
            const response = await fetch(`${API_BASE}/api/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ login: username, password }),
            });

            let data = {};
            try {
                data = await response.json();
            } catch (e) {
                console.warn("Risposta non JSON:", e);
            }

            console.log("Status login:", response.status, data);

            if (response.ok && data.access_token) {
                localStorage.setItem("token", data.access_token);
                console.log("Login avvenuto, token salvato!");
                showToast("Accesso effettuato con successo.", "success");
                showProductSection();
            } else {
                showToast(
                    `Login fallito: ${data.detail || "Credenziali non valide"}`,
                    "error"
                );
            }
        } catch (error) {
            console.error("Errore nella richiesta API:", error);
            showToast("Errore di connessione al server.", "error");
        } finally {
            setButtonLoading(loginBtn, false);
        }
    });

    // --------- AGGIUNTA PRODOTTO ---------

    async function addProduct(productUrl) {
        const category = categorySelect.value || null;

        let token = await getTokenOrRefresh();
        if (!token) {
            return;
        }

        const cleanedUrl = cleanAmazonUrl(productUrl);

        const requestData = {
            product_url: cleanedUrl,
            category: category,
        };

        console.log("Invio richiesta a /api/add-product con:", requestData);
        setButtonLoading(addProductBtn, true, "Aggiungo al tracker...");

        try {
            const response = await fetch(`${API_BASE}/api/add-product/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(requestData),
            });

            const data = await response.json().catch(() => ({}));
            console.log("Risposta API add-product:", response.status, data);

            if (response.ok) {
                showToast("Prodotto aggiunto con successo!", "success");
                // la categoria è già salvata dal listener change, ma se vuoi forzare:
                if (category) {
                    localStorage.setItem("last_category", category);
                }
            } else if (response.status === 401) {
                localStorage.removeItem("token");
                showToast("Sessione scaduta, effettua di nuovo il login.", "error");
                showLoginSection();
            } else {
                showToast(
                    `Errore: ${data.detail || "Impossibile aggiungere il prodotto"}`,
                    "error"
                );
            }
        } catch (error) {
            console.error("Errore API add-product:", error);
            showToast("Errore di connessione al server.", "error");
        } finally {
            setButtonLoading(addProductBtn, false);
        }
    }

    // --------- LOGOUT ---------

    logoutBtn.addEventListener("click", () => {
        console.log("Logout eseguito");
        localStorage.removeItem("token");
        showToast("Sei stato disconnesso.", "info");
        showLoginSection();
    });
});
