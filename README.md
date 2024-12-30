
# **Amazon.it Price Tracker and monitoring**

A full-stack powerful web application for tracking and analyzing price changes on Amazon.it. This project lets users monitor product prices, manage favorites, and visualize data trends with interactive charts.

Currently, the application supports only **Amazon.it** and is built using **Vue.js**, **Python**, and **MongoDB**.



---

## 🚀 **Features**
- **📊 Interactive Charts**: Visualize price history with dynamic graphs.
- **🔍 Advanced Filtering**: Search and filter products by category, condition, and price range.
- **🌟 Favorites Management**: Save your favorite products for quick access.
- **📬 Email Notifications**: Get notified of price changes.

---

## ⚙️ **Installation**
Follow these steps to run the project locally.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/price-tracker.git
   cd price-tracker
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
├── app/                  # Backend dell'applicazione
│   ├── utils/           # Utility e moduli di supporto
│   │   └── email.py    # Modulo per l'invio di email
│   ├── auth.py          # Gestione dell'autenticazione
│   ├── config.py        # Configurazioni dell'applicazione
│   ├── crud.py          # Operazioni CRUD sul database
│   ├── db.py            # Configurazione del database
│   ├── main.py          # Entry point dell'applicazione
│   └── scraper.py       # Modulo per il web scraping
├── frontend/            # Frontend dell'applicazione
│   ├── public/         # File pubblici e asset statici
│   ├── src/            # Codice sorgente del frontend
│   └── ...             # Altri file e directory del frontend
├── README.md            # Documentazione del progetto
├── .gitignore           # File per escludere file e cartelle specifiche da Git
└── requirements.txt     # Dipendenze Python necessarie
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
Link to the live demo (if available): [Price Tracker Demo](https://amazon-price-tracker-delta.vercel.app/)

---

## 📧 **Contact**
For questions or feedback, feel free to reach out:
- **Email**: your-email@example.com


---

## 🛡️ **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
