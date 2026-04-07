
# **Amazon.it Product Cart Manager and Monitoring**

A full-stack powerful web application for tracking and analyzing price changes on Amazon.it Cart. This project lets users monitor product prices, manage favorites, and visualize data trends with interactive charts.

Currently, the application supports **Amazon.it** and is built with a modern, high-performance stack:
- **Frontend**: Vue.js 3 with a premium, custom UI (Glassmorphism, Dark Mode, Micro-animations).
- **Backend**: FastAPI (Python) for high-speed asynchronous processing.
- **Database**: MongoDB for flexible data storage.
- **AI**: Integrated AI for SEO keyword enhancement and automated article generation.
- **Scraper**: Multi-mode scraper (CSS/JSON) with optional proxy support to ensure resilience.

---

![Screenshot of Amazon Price Tracker](https://github.com/Lowell130/amazon_price_tracker/blob/main/frontend/public/1.png)


---

## 🚀 **Features**
- **📊 Pannello Analytics Avanzato**: Monitora visite, sorgenti di traffico (referrers) e query di ricerca in tempo reale.
- **🤖 Bot Detection & Filtering**: Sistema integrato per identificare e filtrare il traffico dei crawler (Googlebot, Bingbot, etc.), garantendo dati puliti.
- **📑 Blog con Paginazione**: Gestione articoli con caricamento ottimizzato e navigazione fluida Precedente/Successivo.
- **⚙️ Configurazione Dinamica**: Impostazioni di sistema per modalità scraper (CSS vs JSON), proxy, tag affiliazione e parametri blog.
- **📈 Grafici Interattivi**: Visualizza la cronologia dei prezzi con grafici dinamici.
- **📬 Notifiche Multi-Canale**: Avvisi di calo prezzo tramite Email e Telegram Bot.
- **🌟 Gestione Preferiti & Ricerca**: Filtraggio avanzato per categoria, condizione e range di prezzo.
- **🧩 Estensione Chrome**: Integrazione diretta con Amazon per aggiungere prodotti in un click.

---

## ⚙️ **Installation**
Follow these steps to run the project locally.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lowell130/amazon_price_tracker.git
   cd amazon_price_tracker

   ```

2. **Install dependencies for backend:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install dependencies for frontend:**
   ```bash
   cd frontend/
   npm install
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory with the following structure:
   ```env
   # MongoDB Configuration
   MONGO_URI=mongodb+srv://your-username:your-password@cluster.mongodb.net

   # Email Configuration
   SENDER_EMAIL=your-email@example.com
   SENDER_PASSWORD=your-email-password
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587

   # Other Configurations
   VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
   FRONTEND_BASE_URL=http://localhost:8080
   ```

5. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```
6. **Run the frontend:**
   ```bash
   npm run serve
   ```

7. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 📂 **Project Structure**
```
amazon_price_tracker/
├── backend/            # FastAPI Backend
│   ├── app/
│   │   ├── routers/    # API Endpoints (Analytics, Articles, SEO, etc.)
│   │   ├── services/   # Business Logic (AI Generation, Scraping, Analysis)
│   │   ├── utils/      # Helpers (Email, Bot Detection)
│   │   ├── main.py     # Entry Point
│   │   └── schemas.py  # Pydantic Models
├── frontend/           # Vue.js 3 Frontend (Vite)
│   ├── src/
│   │   ├── views/      # Pages (Admin, Blog, Tracker)
│   │   ├── components/ # Reusable UI Components
│   │   └── store/      # State Management
├── amazon-extension/   # Chrome Extension for one-click tracking
├── README.md           # Documentation
└── requirements.txt    # Python Dependencies
```

---

## 🤝 **Contributing**
We welcome contributions! Follow these steps to get started:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request.

---

## 🌟 **Demo**
Link to the live demo (if available): [Product Cart Manager and Monitoring Demo](https://amazon-price-tracker-delta.vercel.app/)

---

## 📧 **Contact**
For questions or feedback, feel free to reach out:
- **Email**: blackfdayit@gmail.com


---

## 🛡️ **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
