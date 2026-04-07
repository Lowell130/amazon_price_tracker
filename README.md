
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
- **📊 Advanced Analytics Dashboard**: Monitor visits, traffic sources (referrers), and search queries in real-time.
- **🤖 Bot Detection & Filtering**: Integrated system to identify and filter crawler traffic (Googlebot, Bingbot, etc.), ensuring clean and accurate data.
- **📑 Blog with Pagination**: Article management with optimized loading and smooth **Previous/Next** navigation.
- **⚙️ Dynamic Configuration**: Centralized system settings for scraper modes (CSS vs JSON), rotating proxies, affiliate tags, and blog parameters.
- **📈 Interactive Charts**: Beautiful price history visualization with dynamic, interactive graphs.
- **📬 Multi-Channel Notifications**: Instant price drop alerts delivered via **Email** and **Telegram Bot**.
- **🌟 Favorites & Advanced Search**: Powerful filtering and management by category, condition, and price range.
- **🧩 Chrome Extension**: Direct browser integration to track any Amazon product with a single click.

---

## ⚙️ **Installation**
Follow these steps to run the project locally.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Lowell130/amazon_price_tracker.git
   cd amazon_price_tracker
   ```

2. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory with the following structure:
   ```env
   # MongoDB Configuration
   MONGO_URI=mongodb+srv://your-username:your-password@cluster.mongodb.net

   # Email Configuration (SMTP)
   SENDER_EMAIL=your-email@example.com
   SENDER_PASSWORD=your-email-password
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587

   # Telegram Configuration (Optional)
   TELEGRAM_BOT_TOKEN=your-bot-token
   TELEGRAM_ADMIN_CHAT_ID=your-chat-id

   # Frontend URLs
   VUE_APP_API_BASE_URL=http://127.0.0.1:8000/api
   FRONTEND_BASE_URL=http://localhost:8080
   ```

5. **Run the server:**
   ```bash
   # From the backend directory
   python -m uvicorn app.main:app --reload
   ```

6. **Run the frontend:**
   ```bash
   # From the frontend directory
   npm run serve
   ```

7. **Access the application:**
   Open your browser and navigate to `http://localhost:8080`.

---

## 📂 **Project Structure**
```
amazon_price_tracker/
├── backend/            # FastAPI Backend
│   ├── app/
│   │   ├── routers/    # API Endpoints (Analytics, Articles, SEO, etc.)
│   │   ├── services/   # Business Logic (AI Generation, Scraping, Analysis)
│   │   ├── utils/      # Helpers (Email, Bot Detection)
│   │   ├── main.py     # Application Entry Point
│   │   └── schemas.py  # Pydantic Definition Models
├── frontend/           # Vue.js 3 Frontend (Vite/Vue CLI)
│   ├── src/
│   │   ├── views/      # Page Views (Admin Dashboard, Blog, Tracker)
│   │   ├── components/ # Reusable UI components
│   │   └── store/      # Global State Management
├── amazon-extension/   # Chrome Extension for browsing integration
├── README.md           # Project Documentation
└── requirements.txt    # Python Project Dependencies
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
