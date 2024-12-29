
# **Amazon Price Tracker and monitoring**

A powerful web application for tracking and analyzing price changes on Amazon. This project lets users monitor product prices, manage favorites, and visualize data trends with interactive charts.

![Project Screenshot]([https://ibb.co/NN8qMCS]) <!-- Replace with an actual screenshot -->

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

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
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

4. **Run the server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:8000`.

---

## 📂 **Project Structure**
```
├── main.py            # Entry point for the application
├── db.py              # Database connection
├── email_service.py   # Email utility functions
├── static/            # Static assets
├── templates/         # HTML templates
├── requirements.txt   # Python dependencies
└── .env.example       # Example of environment variables file
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
