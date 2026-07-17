# CarbonKisan

**A carbon credit micro-marketplace connecting Indian smallholder farmers directly to corporate carbon-offset buyers.**

CarbonKisan empowers smallholder farmers in India to generate verifiable carbon credits through sustainable agricultural practices, and enables corporate CSR buyers to purchase these credits transparently at a micro-scale.

---

## 🌟 How It Works

### For the Farmer (Supply Side)
1. **Registration & Profile:** A farmer signs up via their mobile phone using an OTP. They provide basic details like their district and land size (in hectares).
2. **Practice Logging & Estimation:** The farmer selects sustainable farming practices (e.g., No-till, Cover Cropping, Agroforestry) they have adopted. 
3. **Instant Explainable Estimates:** A Machine Learning model immediately calculates an estimated CO₂e (Carbon Dioxide Equivalent) captured by their land. The platform provides a transparent breakdown (using SHAP values) showing exactly *why* their estimate is what it is (factoring in soil type, rainfall zone, and land area).
4. **Marketplace Listing:** The farmer lists their generated carbon credits for sale on the marketplace, setting their asking price within a suggested market band.
5. **Direct Payouts:** Once a buyer purchases their credits, the farmer receives an instant UPI payout (85% of the transaction value) and an SMS notification.

### For the Corporate Buyer (Demand Side)
1. **Discovery & Browsing:** Corporate CSR/ESG managers log into the desktop dashboard to browse a grid of live listings from verified farmers.
2. **Transparent Due Diligence:** Buyers can filter by district, practice type, or CO₂ volume. Every listing exposes the underlying ML SHAP breakdown, proving exactly how the credit amount was calculated.
3. **Frictionless Purchase:** Buyers can purchase micro-credits using standard payment gateways (Razorpay). 
4. **Instant Verification:** Upon successful payment, a cryptographically hashed, immutable PDF certificate is generated instantly. This certificate can be used for compliance reporting (e.g., BRSR filings).
5. **Impact Tracking:** A public `/impact` dashboard tracks platform-wide CO₂e sold and farmer income generated in real time.

---

## 🏗️ Technical Architecture

CarbonKisan uses a decoupled, modern web stack to handle everything from frontend user flows to machine learning inference and transaction processing.

### The Stack
- **Frontend (Buyer & Farmer Portals):** React + Vite (HTML/CSS/Vanilla JS ecosystem). Mobile-first for farmers, desktop-focused for buyers.
- **Backend API:** FastAPI (Python), providing high-performance, asynchronous endpoints.
- **Database & Auth:** Supabase (PostgreSQL). Handles user authentication (SMS OTPs & Email/Password) and complex relational data, leveraging Row-Level Security (RLS) to restrict unauthorized access.
- **Machine Learning Inference:** XGBoost Regressor for calculating CO₂e yield, coupled with the `shap` (TreeExplainer) library to generate human-readable breakdowns of the model's logic.
- **Payments:** Razorpay for INR transactions and automated payouts.
- **Certificate Generation:** Server-side PDF generation using standard Python PDF rendering tools.

### Database Schema Highlights
The platform uses a relational model heavily reliant on UUIDs and foreign keys to ensure data integrity:
- `farmers`, `buyers`, and `admins` manage the user personas.
- `estimates` store the ML output alongside the SHAP JSON breakdowns.
- `listings` link an estimate to the marketplace with a lifecycle state (`pending_verification` -> `live` -> `sold`).
- `transactions` and `certificates` handle the financial leg and cryptographic proof of purchase.
- `districts` serves as a lookup table providing baseline Soil Organic Carbon (SOC) and rainfall data used by the ML model.

---

## 🧠 Machine Learning Engine

CarbonKisan replaces expensive manual audits with an AI-driven estimator tailored for the Indian subcontinent.

### Model Specs
- **Algorithm:** XGBoost Regressor (chosen for its capability to handle non-linear soil × practice interactions).
- **Features:** Practice Type, Area (ha), Season Duration, Soil Type, Baseline SOC, and Rainfall Zone.
- **Explainability:** 
  We believe in *zero black boxes*. Every prediction is passed through a SHAP (SHapley Additive exPlanations) explainer. The raw SHAP values are translated into plain-language modifiers (e.g., "Your soil type adds a bonus") so both the farmer and the buyer understand the estimate perfectly.

---

## 🚀 Running the Project Locally

To run the local development environment for demonstration purposes:

### 1. Database Setup
The project requires a Supabase instance.
1. Create a project on Supabase.
2. Run the SQL initialization script found in `docs/schema.sql` in your Supabase SQL Editor.
3. Import the required district reference data (`maharashtra_districts.csv`) into the `districts` table.

### 2. Backend (FastAPI)
Navigate to the backend directory and set up the environment:
```bash
cd backend
python -m venv venv
source venv/Scripts/activate # (Or venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
```

Create a `.env` file with your credentials:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
GEMINI_API_KEY=your_gemini_api_key
ENVIRONMENT=development
```

Start the backend server (ensure UTF-8 encoding for console logs):
```bash
# On Windows PowerShell
$env:PYTHONUTF8=1; fastapi dev app/main.py --port 8000
```

### 3. Frontend (React/Vite App)
In a separate terminal, start the frontend server:
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and the backend API at `http://localhost:8000`.

---

## 🤝 Roadmap & Future Scope
- **Satellite MRV Integration:** Moving beyond estimation to full Measurement, Reporting, and Verification (MRV) using multispectral satellite imagery.
- **Blockchain Issuance:** Tokenizing certificates on a public ledger for global traceability.
- **WhatsApp Bot Integration:** Allowing low-literacy farmers to register and list credits entirely via WhatsApp voice notes and text.
