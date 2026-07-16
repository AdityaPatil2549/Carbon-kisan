# CarbonKisan — Technology Stack & Environment Setup

**Companion document to `CarbonKisan_PRD.md`. This is the build reference — every version, every command, every config file.**

---

## 0. How to read this document

Versions marked **✓ verified** were confirmed live against PyPI/npm during this session (July 2026) — use them as-is. Versions without the checkmark are latest-stable at time of writing for lower-churn packages; run the lock commands in §5.4 immediately after your first install to pin your actual resolved versions into `requirements.lock` / `package-lock.json`, and treat *those* files as the source of truth from that point forward, not this document.

---

## 1. Locked Stack — Final Decision Table

| Layer | Technology | Version | Verified |
|---|---|---|---|
| Backend language | Python | 3.12+ | Required by XGBoost 3.3.0 |
| Backend framework | FastAPI | 0.139.0 | ✓ verified |
| ASGI server | Uvicorn | 0.38.0 | latest-stable |
| Data validation | Pydantic | 2.11.0 | latest-stable |
| ML model | XGBoost | 3.3.0 | ✓ verified |
| ML explainability | SHAP | 0.47.0 | latest-stable |
| ML preprocessing | scikit-learn | 1.6.1 | latest-stable |
| Data handling | pandas | 2.3.0 | latest-stable |
| Numerics | numpy | 2.2.0 | latest-stable |
| Database + Auth | Supabase (Postgres 17) | managed cloud | — |
| Supabase Python client | `supabase-py` | 2.15.0 | latest-stable |
| Payments | Razorpay | API v1 | — |
| Razorpay Python SDK | `razorpay` | 1.4.2 | latest-stable |
| PDF generation | ReportLab | 4.3.0 | latest-stable |
| Frontend runtime | Node.js | 22 LTS | Required — Node 20 reached EOL 30 Apr 2026 |
| Frontend library | React | 19.2.7 | ✓ verified |
| Build tool | Vite | 8.1.4 | ✓ verified |
| Supabase JS client | `@supabase/supabase-js` | 2.108.2 | ✓ verified |
| Routing | React Router | 7.2.0 | latest-stable |
| Charts | Recharts | 2.15.0 | latest-stable |
| Localization | react-i18next / i18next | 15.4.0 / 24.2.0 | latest-stable |
| Styling | Tailwind CSS | 4.0.0 | latest-stable |
| Frontend hosting | Vercel | — | — |
| Backend hosting | Railway | — | — |
| SMS | MSG91 (India-optimised) | REST API | — |
| Error tracking | Sentry | JS + Python SDK | latest-stable |
| Testing (backend) | pytest / pytest-asyncio | 8.4.0 / 0.26.0 | latest-stable |
| Testing (frontend) | Vitest / Testing Library | 3.0.0 / 16.2.0 | latest-stable |
| E2E testing | Playwright | 1.51.0 | latest-stable |

---

## 2. Decision Rationale (why each choice beats its alternative)

| Choice | Alternative considered | Why we rejected the alternative |
|---|---|---|
| Python 3.12 | Python 3.11 | XGBoost 3.3.0 requires Python ≥3.12 — non-negotiable, this is the newest stable XGBoost and carries real performance improvements over 3.2.x |
| FastAPI | Flask, Django REST | FastAPI gives native async, automatic OpenAPI docs, and Pydantic validation with zero extra config — critical for a 4-day build with no time for boilerplate |
| XGBoost | Random Forest, Linear Regression, Neural Net | Soil × practice interactions are non-linear and multiplicative; XGBoost captures this natively without manual feature crosses. A neural net is unjustified at 10,000 training rows and 6 features — added complexity with no accuracy gain |
| Supabase | Firebase, self-hosted Postgres | Row-Level Security is native Postgres — critical for per-farmer data isolation. Firebase's document model is the wrong shape for relational marketplace transactions. Self-hosted Postgres adds DevOps overhead you don't have time for in 4 days |
| React + Vite | Next.js | You don't need server-side rendering or API routes — the FastAPI backend already serves that role. Next.js adds a routing/rendering paradigm with no benefit here and slower cold builds during rapid iteration |
| Razorpay | Stripe | Stripe requires an international card for test AND production in India-first flows; Razorpay natively supports UPI payouts to Indian bank accounts, which is how your farmer persona actually gets paid |
| Vercel + Railway split | Single full-stack host (e.g. Render for both) | Vercel's edge network is materially faster for static React delivery; Railway's Docker-native deploy is simpler for a Python ML service with binary dependencies (XGBoost compiled libs). Splitting costs nothing extra on free tiers |
| MSG91 over Twilio | Twilio | MSG91 is priced for the Indian SMS market specifically — meaningfully cheaper per message at the volumes this product will see, and has better native DLT (Distributed Ledger Technology) compliance support required for commercial SMS in India |

---

## 3. Repository Structure

```
carbonkisan/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entrypoint
│   │   ├── config.py                # Environment variable loading
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── estimate.py
│   │   │   ├── listings.py
│   │   │   ├── purchase.py
│   │   │   ├── certificate.py
│   │   │   ├── impact.py
│   │   │   └── admin.py
│   │   ├── models/
│   │   │   ├── schemas.py           # Pydantic request/response models
│   │   │   └── db.py                # Supabase client wrapper
│   │   ├── services/
│   │   │   ├── carbon_estimator.py  # XGBoost inference + SHAP
│   │   │   ├── razorpay_client.py
│   │   │   ├── pdf_generator.py
│   │   │   └── notifications.py     # MSG91 wrapper
│   │   └── ml/
│   │       ├── train.py             # Model training script
│   │       ├── generate_synthetic.py
│   │       ├── model.pkl            # Trained model artifact
│   │       ├── explainer.pkl        # SHAP explainer artifact
│   │       └── model_card.md
│   ├── data/
│   │   ├── district_features.csv
│   │   ├── sequestration_rates.csv
│   │   └── train.csv
│   ├── tests/
│   │   ├── test_estimate.py
│   │   ├── test_payment_signature.py
│   │   └── test_model_validation.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── routes/
│   │   │   ├── farmer/
│   │   │   │   ├── Onboarding.jsx
│   │   │   │   ├── Estimator.jsx
│   │   │   │   ├── MyListings.jsx
│   │   │   ├── buyer/
│   │   │   │   ├── Marketplace.jsx
│   │   │   │   ├── ListingDetail.jsx
│   │   │   │   ├── Checkout.jsx
│   │   │   ├── admin/
│   │   │   │   └── ReviewQueue.jsx
│   │   │   └── Impact.jsx
│   │   ├── components/
│   │   │   ├── PracticeSelector.jsx
│   │   │   ├── ShapBreakdownChart.jsx
│   │   │   ├── ListingCard.jsx
│   │   │   ├── FilterSidebar.jsx
│   │   │   └── LanguageToggle.jsx
│   │   ├── lib/
│   │   │   ├── supabaseClient.js
│   │   │   └── api.js
│   │   ├── locales/
│   │   │   ├── mr.json
│   │   │   ├── hi.json
│   │   │   └── en.json
│   │   └── styles/
│   │       └── tokens.css           # Design system CSS variables
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── CarbonKisan_PRD.md
│   └── carboncredit_spec.html
└── README.md
```

---

## 4. Database Schema — Runnable SQL

Run this directly in the Supabase SQL Editor after project creation. This is the executable version of the PRD's §10 data model.

```sql
-- =========================================
-- CarbonKisan — Full Schema + RLS Policies
-- =========================================

create extension if not exists "uuid-ossp";

-- ---------- Reference table: districts ----------
create table districts (
  code               varchar(10) primary key,
  name               varchar(80) not null,
  soc_baseline       decimal(5,3) not null,
  rainfall_zone      varchar(10) not null check (rainfall_zone in ('low','medium','high')),
  dominant_soil_type varchar(50) not null,
  soil_modifier      decimal(4,3) not null
);

-- ---------- farmers ----------
create table farmers (
  id                  uuid primary key default uuid_generate_v4(),
  phone               varchar(15) unique not null,
  full_name           varchar(120) not null,
  district_code       varchar(10) references districts(code) not null,
  village             varchar(120),
  preferred_language  varchar(2) default 'mr' check (preferred_language in ('mr','hi','en')),
  profile_complete    boolean default false,
  created_at          timestamptz default now()
);

-- ---------- land_parcels ----------
create table land_parcels (
  id             uuid primary key default uuid_generate_v4(),
  farmer_id      uuid references farmers(id) not null,
  area_ha        decimal(6,2) not null check (area_ha > 0),
  primary_crop   varchar(50) not null,
  soil_type      varchar(50) not null,
  district_code  varchar(10) references districts(code) not null,
  created_at     timestamptz default now()
);

-- ---------- estimates ----------
create table estimates (
  id                uuid primary key default uuid_generate_v4(),
  farmer_id         uuid references farmers(id) not null,
  parcel_id         uuid references land_parcels(id),
  practice_type     varchar(30) not null check (practice_type in
                      ('no_till','cover_crop','no_till_cover_crop','agroforestry')),
  area_ha           decimal(6,2) not null,
  season_months     smallint not null check (season_months in (6,12)),
  co2e_tonnes       decimal(6,3) not null,
  confidence_low    decimal(6,3) not null,
  confidence_high   decimal(6,3) not null,
  inr_estimate      integer not null,
  shap_breakdown    jsonb not null,
  model_version     varchar(20) not null,
  created_at        timestamptz default now()
);

-- ---------- listings ----------
create table listings (
  id                 uuid primary key default uuid_generate_v4(),
  estimate_id        uuid references estimates(id) unique not null,
  farmer_id          uuid references farmers(id) not null,
  asking_price_inr   integer not null check (asking_price_inr > 0),
  status             varchar(20) default 'pending_verification' check (status in
                       ('pending_verification','live','sold','expired','rejected')),
  rejection_reason   text,
  published_at       timestamptz,
  expires_at         timestamptz not null default (now() + interval '90 days')
);

-- ---------- buyers ----------
create table buyers (
  id             uuid primary key default uuid_generate_v4(),
  email          varchar(150) unique not null,
  org_name       varchar(150) not null,
  contact_name   varchar(120) not null,
  created_at     timestamptz default now()
);

-- ---------- transactions ----------
create table transactions (
  id                     uuid primary key default uuid_generate_v4(),
  listing_id             uuid references listings(id) unique not null,
  buyer_id               uuid references buyers(id) not null,
  razorpay_payment_id    varchar(60) unique not null,
  amount_paid_inr        integer not null,
  platform_fee_inr       integer not null,
  farmer_payout_inr      integer not null,
  payout_status          varchar(20) default 'pending' check (payout_status in
                            ('pending','processing','completed','failed')),
  paid_at                timestamptz default now()
);

-- ---------- certificates ----------
create table certificates (
  id                     uuid primary key default uuid_generate_v4(),
  transaction_id         uuid references transactions(id) unique not null,
  record_hash            varchar(64) not null,
  pdf_url                text not null,
  methodology_version    varchar(20) not null,
  status                 varchar(15) default 'active' check (status in ('active','superseded')),
  issued_at              timestamptz default now()
);

-- ---------- admins ----------
create table admins (
  id            uuid primary key default uuid_generate_v4(),
  email         varchar(150) unique not null,
  full_name     varchar(120) not null
);

-- ---------- admin_audit_log ----------
create table admin_audit_log (
  id           uuid primary key default uuid_generate_v4(),
  admin_id     uuid references admins(id) not null,
  action       varchar(50) not null,
  target_id    uuid not null,
  reason       text,
  created_at   timestamptz default now()
);

-- =========================================
-- Row-Level Security
-- =========================================

alter table farmers enable row level security;
alter table land_parcels enable row level security;
alter table estimates enable row level security;
alter table listings enable row level security;
alter table transactions enable row level security;
alter table certificates enable row level security;

-- Farmers: full access to their own row only
create policy farmer_self_select on farmers
  for select using (auth.uid()::text = id::text);
create policy farmer_self_update on farmers
  for update using (auth.uid()::text = id::text);

-- Land parcels: farmer owns their parcels
create policy parcel_owner_select on land_parcels
  for select using (auth.uid()::text = farmer_id::text);
create policy parcel_owner_insert on land_parcels
  for insert with check (auth.uid()::text = farmer_id::text);

-- Estimates: farmer owns their estimates
create policy estimate_owner_select on estimates
  for select using (auth.uid()::text = farmer_id::text);

-- Listings: public read for 'live' status, farmer full access to own
create policy listing_public_read on listings
  for select using (status = 'live' or auth.uid()::text = farmer_id::text);
create policy listing_owner_write on listings
  for update using (auth.uid()::text = farmer_id::text);

-- Transactions and certificates: no direct client writes.
-- All writes happen via the backend service-role key only.
create policy transaction_buyer_read on transactions
  for select using (auth.uid()::text = buyer_id::text);
create policy certificate_public_verify on certificates
  for select using (true);  -- public verification page needs read access, PII excluded at query level

-- Seed reference data (Maharashtra districts — abbreviated example, extend to all 35)
insert into districts (code, name, soc_baseline, rainfall_zone, dominant_soil_type, soil_modifier) values
  ('MH_PUNE', 'Pune', 0.612, 'medium', 'vertisol', 1.180),
  ('MH_NASHIK', 'Nashik', 0.548, 'medium', 'inceptisol', 1.050),
  ('MH_NAGPUR', 'Nagpur', 0.701, 'high', 'vertisol', 1.230),
  ('MH_SOLAPUR', 'Solapur', 0.489, 'low', 'vertisol', 0.980),
  ('MH_AURANGABAD', 'Aurangabad', 0.522, 'low', 'vertisol', 1.010);
```

---

## 5. Local Development Setup

### 5.1 Prerequisites
```bash
# Verify versions before starting
python3 --version   # must show 3.12.x or higher
node --version       # must show v22.x.x
git --version
```

### 5.2 Backend setup
```bash
mkdir -p carbonkisan/backend && cd carbonkisan/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# Install dependencies (requirements.txt content in §5.3)
pip install -r requirements.txt

# Copy env template and fill in real values
cp .env.example .env

# Run the dev server
fastapi dev app/main.py --port 8000
```

### 5.3 `requirements.txt`
```
fastapi[standard]==0.139.0
uvicorn[standard]==0.38.0
pydantic==2.11.0
xgboost==3.3.0
scikit-learn==1.6.1
shap==0.47.0
pandas==2.3.0
numpy==2.2.0
python-dotenv==1.1.0
supabase==2.15.0
razorpay==1.4.2
reportlab==4.3.0
httpx==0.28.0
pytest==8.4.0
pytest-asyncio==0.26.0
```

### 5.4 Lock your exact resolved versions (run immediately after install)
```bash
pip freeze > requirements.lock.txt
# From this point, requirements.lock.txt is your source of truth for reproducible installs
```

### 5.5 Frontend setup
```bash
cd carbonkisan/frontend

# Scaffold with Vite
npm create vite@latest . -- --template react

# Install dependencies (package.json content in §5.6)
npm install

# Copy env template
cp .env.example .env.local

# Run dev server
npm run dev
```

### 5.6 `package.json` (dependencies section)
```json
{
  "dependencies": {
    "react": "19.2.7",
    "react-dom": "19.2.7",
    "react-router-dom": "7.2.0",
    "@supabase/supabase-js": "2.108.2",
    "recharts": "2.15.0",
    "react-i18next": "15.4.0",
    "i18next": "24.2.0"
  },
  "devDependencies": {
    "vite": "8.1.4",
    "@vitejs/plugin-react": "5.0.0",
    "tailwindcss": "4.0.0",
    "vitest": "3.0.0",
    "@testing-library/react": "16.2.0",
    "playwright": "1.51.0"
  }
}
```

### 5.7 Lock frontend versions
```bash
npm install    # generates package-lock.json — commit this file to git, it is your source of truth
```

---

## 6. Environment Variables

### 6.1 `backend/.env.example`
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here   # server-only, never expose to frontend
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your-razorpay-secret-here
MSG91_AUTH_KEY=your-msg91-key-here
MSG91_SENDER_ID=CRBNKS
SENTRY_DSN=your-sentry-dsn-here
ENVIRONMENT=development
```

### 6.2 `frontend/.env.example`
```
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-public-key-here
VITE_RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
```

**Security note:** the Supabase `service_role` key and Razorpay `KEY_SECRET` must NEVER appear in any frontend file, env var prefixed `VITE_`, or client-side bundle. Only the `anon` public key and `RAZORPAY_KEY_ID` (public identifier, not the secret) belong on the frontend.

---

## 7. Backend Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# System dependencies for XGBoost + ReportLab
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
```

---

## 8. Deployment Configuration

### 8.1 Railway (backend)
- Connect GitHub repo, select `backend/` as root directory.
- Railway auto-detects the `Dockerfile`.
- Set all variables from `.env.example` in Railway's environment variables panel.
- Railway assigns a public URL automatically (e.g. `carbonkisan-backend.up.railway.app`).

### 8.2 Vercel (frontend)
`frontend/vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```
- Connect GitHub repo, select `frontend/` as root directory.
- Set `VITE_API_URL` to your live Railway backend URL in Vercel's environment variables panel.
- Every push to `main` auto-deploys.

---

## 9. CI Pipeline (lightweight — GitHub Actions)

`.github/workflows/ci.yml`:
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v

  frontend-tests:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: npm ci
      - run: npm run build
      - run: npm run test -- --run
```

---

## 10. Third-Party Service Setup — Exact Steps

### 10.1 Supabase
1. Go to supabase.com → New Project.
2. Choose a region close to India (Singapore — `ap-southeast-1`) for lowest latency.
3. Note the project URL and both keys (anon + service_role) from Settings → API.
4. Paste the full SQL from §4 into the SQL Editor and run it.
5. Enable Phone Auth: Authentication → Providers → Phone → toggle on, configure your SMS provider (MSG91 or Twilio) as the OTP delivery channel.

### 10.2 Razorpay
1. Go to razorpay.com → Sign up → Dashboard defaults to **Test Mode**.
2. Settings → API Keys → Generate Test Key — no KYC required for test mode.
3. Use these `rzp_test_...` keys throughout the hackathon. Never request live keys for a demo.
4. Enable UPI and Cards under Test Mode payment methods (on by default).

### 10.3 MSG91 (SMS)
1. Sign up at msg91.com — trial account includes free credits.
2. Create a Sender ID (6 characters, e.g. `CRBNKS`) — trial accounts get a shared test sender ID instantly.
3. Note your Auth Key from the dashboard.
4. DLT (Distributed Ledger Technology) template registration is required for production SMS in India — not needed for trial/demo credits during the hackathon.

### 10.4 Sentry (error tracking — optional but recommended)
1. Sign up at sentry.io → New Project → select Python (FastAPI) and separately React.
2. Copy the DSN into both `.env` files.
3. Add four lines to `main.py` and `main.jsx` per Sentry's quhowever-start — this is a 10-minute addition that turns an invisible production error into a stack trace you can actually read.

---

## 11. Testing Commands Reference

```bash
# Backend unit + integration tests
cd backend && pytest tests/ -v --cov=app

# Frontend unit tests
cd frontend && npm run test

# Frontend E2E (requires both servers running)
cd frontend && npx playwright test

# Model validation suite (the 10 hand-crafted literature cases from PRD §15.3)
cd backend && python app/ml/validate_model.py
```

---

## 12. Stack-to-Build-Plan Mapping

Ties this document back to the 4-day plan in the technical spec.

| Day | Stack pieces touched |
|---|---|
| Day 1 | Python 3.12 venv, pandas, numpy, XGBoost, SHAP — no web framework yet |
| Day 2 | FastAPI, Supabase (schema from §4), Razorpay test keys, Railway deploy |
| Day 3 | React 19, Vite, Recharts, Supabase JS client, Vercel deploy |
| Day 4 | MSG91 (if time allows), Sentry (if time allows), Playwright smoke test, demo data seeding via direct SQL insert into `listings`/`estimates` |

---

## 13. Version Upgrade Policy (post-hackathon)

- Pin exact versions in `requirements.lock.txt` / `package-lock.json` — never deploy off unpinned `requirements.txt`/`package.json` ranges to production.
- Re-run `pip list --outdated` and `npm outdated` monthly during the Phase 1 pilot (PRD §16.2).
- XGBoost and FastAPI both ship frequent minor releases — read changelogs before bumping major versions; both are pre-1.0/0.x software by convention, meaning minor version bumps can carry breaking changes.

---

*Companion to `CarbonKisan_PRD.md`. Keep both files in `docs/` in the repository root.*
