# Carbon Kisan 🌿

> India's first farmer-led carbon credit marketplace

**Carbon Kisan** connects rural Indian farmers with urban CSR buyers through verifiable carbon credits. Farmers log sustainable practices, our ML model estimates CO₂ sequestration, and CSR teams purchase verified micro-credits — creating direct income for rural India.

---

## 🌐 Live Pages

| Page | Description |
|------|-------------|
| `index.html` | Landing page with estimator and how-it-works |
| `farmer-login.html` | Farmer OTP login (mobile number + 6-digit OTP) |
| `farmer-dashboard.html` | Farmer dashboard — credits, wallet, referrals |
| `log-practice.html` | Log a sustainable farming practice |
| `buyer-login.html` | Corporate CSR buyer login |
| `buyer-dashboard.html` | Buyer dashboard — purchases, CSV export, certificates |
| `marketplace.html` | Carbon credit marketplace with heatmap and filters |

---

## 🚀 Run Locally

```bash
npm run dev
```

Then open [http://localhost:3000](http://localhost:3000)

---

## 🌍 Features

- 🌾 **Farmer portal** — OTP login, land verification, credit wallet
- 🏢 **Corporate buyer portal** — Blue theme, dashboard, marketplace
- 📊 **ML carbon estimator** — XGBoost model (ICRISAT soil data, R² 0.81)
- 💬 **Multi-language** — English, हिंदी, मराठी
- 📥 **Export CSV** and **Download Impact Certificates**
- 📱 **Mobile responsive** — bottom nav for farmers on mobile

---

## 🛠️ Tech Stack

- Vanilla HTML, CSS, JavaScript (no frameworks)
- Google Fonts (Inter, Noto Sans)
- `localStorage` for session persistence
- `npx serve` for local development

---

© 2026 Carbon Kisan. All rights reserved.
