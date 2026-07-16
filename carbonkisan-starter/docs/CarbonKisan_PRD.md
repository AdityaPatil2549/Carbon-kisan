# CarbonKisan — Product Requirements Document

**A carbon credit micro-marketplace connecting Indian farmers directly to corporate carbon-offset buyers**

---

## Document Control

| Field | Value |
|---|---|
| Product name | CarbonKisan |
| Document type | Product Requirements Document (PRD) |
| Version | 1.0 |
| Status | Draft — Hackathon MVP scope + Post-MVP roadmap |
| Track | AMIEE Hackathon — Environment & Sustainability / Entrepreneurship & Startup Ideas |
| Author | Product & Engineering (Aditya) |
| Last updated | 12 July 2026 |
| Target build window | 4 days (hackathon) + phased post-hackathon roadmap |

---

## 1. Executive Summary

CarbonKisan is a two-sided marketplace that lets Indian smallholder farmers convert sustainable farming practices (no-till, cover cropping, agroforestry, reduced chemical input) into verifiable, sellable carbon credits, and lets corporate CSR/ESG buyers purchase those credits directly, at micro scale, with full traceability.

India's government launched a formal Voluntary Carbon Market (VCM) framework for agriculture on 29 January 2024, with methodologies approved by the Bureau of Energy Efficiency (BEE) in March 2025. A pilot by IIT Roorkee and the Uttar Pradesh government (December 2025) projects ₹5,000–₹8,000 per hectare in supplementary farmer income. India's overall carbon credit market was valued at USD 33.69 billion in 2025, projected to reach USD 405.47 billion by 2034. Despite this, no consumer-facing product exists that lets a 2-hectare farmer list and sell credits the way they'd list a product on any e-commerce app. Global standards bodies (Verra, Gold Standard) have minimum project sizes of 1,000+ hectares and certification costs of $50,000–$200,000 — structurally excluding smallholders. CarbonKisan is the missing product layer on top of an already-live government framework.

---

## 2. Problem Statement

### 2.1 The core problem
Sustainable farming practices sequester measurable carbon (0.04–1.43 tonnes CO₂ per hectare per year depending on practice, per peer-reviewed meta-analysis). Farmers who adopt these practices receive **zero direct financial return** for the climate benefit they create. Meanwhile, Indian corporations spend crores on CSR/ESG carbon offsetting, often through opaque international intermediaries, while a compliant domestic voluntary market sits underused.

### 2.2 Why existing solutions fail
| Existing option | Why it fails smallholders |
|---|---|
| Verra / Gold Standard | Minimum 1,000 ha project size; 3-year MRV cycle; $50K–$200K certification cost |
| Government CCTS (compliance market) | Targets 9 industrial sectors only — power, steel, cement, etc. Not agriculture |
| Corporate CSR programs (ad hoc) | One-off, non-transparent, no direct farmer payment traceability |
| Manual carbon consultancies | Expensive, slow, require large aggregated landholding to be viable |

### 2.3 Why now
- Government VCM-for-agriculture framework is live (Jan 2024) but has no consumer product built on top of it.
- BEE approved 8 domestic offset methodologies (March 2025).
- A real pilot (IIT Roorkee × UP Government, Dec 2025) has proven the income model works at ₹5,000–8,000/ha.
- India's carbon market is in a documented high-growth phase (10x projected growth to 2034).

---

## 3. Goals & Success Metrics

### 3.1 Product goals
1. Let any farmer with as little as 0.5 hectares generate a carbon credit estimate in under 2 minutes.
2. Let any corporate/NGO buyer purchase verifiable, traceable micro-credits in under 3 clicks.
3. Make every credit estimate explainable — no black-box numbers.
4. Achieve first transaction (farmer listing → buyer purchase → certificate issued) within the 4-day hackathon build.

### 3.2 Success metrics (Hackathon MVP)
| Metric | Target |
|---|---|
| End-to-end demo completion time | < 90 seconds |
| Carbon estimator model RMSE | < 0.15 tonne CO₂e on held-out test set |
| Time from farmer login to listing published | < 3 minutes |
| Time from buyer landing to completed purchase | < 2 minutes |
| Number of seeded demo listings | 12, across 5+ districts |
| API p95 latency (`/estimate`) | < 800ms |

### 3.3 Success metrics (Post-MVP, 6-month horizon)
| Metric | Target |
|---|---|
| Registered farmers | 5,000 in Maharashtra |
| Verified listings | 2,000 |
| GMV (gross credit value transacted) | ₹1 crore+ |
| Average farmer payout per hectare per year | ₹1,500–₹2,500 |
| Buyer retention (repeat purchase within 90 days) | 40%+ |

---

## 4. Non-Goals (Out of Scope for MVP)

- **Not** building a full Verra/Gold Standard-equivalent MRV (Measurement, Reporting, Verification) pipeline with satellite verification — that is Phase 2.
- **Not** supporting international buyers or non-INR currency in MVP.
- **Not** supporting crops/practices outside the 4 core practice types in MVP (no-till, cover crop, no-till+cover crop combined, agroforestry).
- **Not** building a native mobile app — MVP is a responsive PWA only.
- **Not** handling KYC/AML compliance for payouts beyond what Razorpay's payout API requires natively — full RBI Payment Aggregator compliance is a legal workstream, not a hackathon deliverable.
- **Not** building blockchain/smart-contract credit issuance for MVP — credit records are relational database rows with cryptographic hashes, not on-chain tokens (this is a deliberate, defensible simplification — flag if asked).

---

## 5. Personas

### 5.1 Persona A — Ramesh, the Farmer (Primary user, supply side)
- **Age:** 38. **Location:** Baramati taluka, Pune district, Maharashtra.
- **Land:** 2.3 hectares, mixed cropping (jowar + cotton), recently adopted no-till on 1.5 ha.
- **Device:** Android smartphone (₹8,000 range), 4G with intermittent connectivity, occasionally 2G in-field.
- **Literacy:** Reads Marathi fluently, functional Hindi, minimal English.
- **Tech comfort:** Uses WhatsApp and UPI daily; has never used a "dashboard" style app.
- **Core need:** "I changed how I farm. Does anyone actually pay me for that?"
- **Trust barrier:** Has been approached by scheme agents before with unclear promises. Needs transparent, simple language and a real payout, not a "coming soon" claim.

### 5.2 Persona B — Priya, the CSR/ESG Buyer (Primary user, demand side)
- **Role:** Sustainability Manager at a mid-size IT services company (Pune-based).
- **Mandate:** Purchase 500 tonnes CO₂e offset annually for the company's net-zero pledge, report it in BRSR (Business Responsibility and Sustainability Report) filings.
- **Device:** Laptop, corporate network, English UI expected.
- **Core need:** Verifiable, exportable, audit-ready purchase records with minimal procurement friction.
- **Trust barrier:** Needs to defend the purchase to auditors — traceability and methodology transparency are non-negotiable.

### 5.3 Persona C — Platform Verifier / Admin (Internal/operational user)
- **Role:** Either an internal ops team member or a partnered FPO (Farmer Producer Organisation) coordinator.
- **Core need:** Review flagged listings, resolve disputes, manually override incorrect estimates, monitor fraud signals.
- **MVP scope:** Basic admin console; full workflow tooling is Phase 2.

---

## 6. User Journeys

### 6.1 Farmer journey (happy path)
1. Opens CarbonKisan PWA link (shared via WhatsApp by FPO coordinator or self-discovered).
2. Registers with name, phone number (OTP via Supabase Auth), district (dropdown, 35 Maharashtra districts).
3. Selects farming practice from 4 illustrated options (icons + one-line description in Marathi/Hindi/English toggle).
4. Enters land area via a slider (0.5–10 ha) — no keyboard typing required.
5. Sees live carbon estimate appear: tonnes CO₂e, INR estimate range, simple visual breakdown ("your soil type adds a bonus," "your rainfall zone is neutral").
6. Taps "List for Sale" — sets asking price (pre-filled with suggested market price, editable).
7. Listing appears in "My Listings" with status "Pending Verification" → "Live."
8. Receives SMS notification when a buyer purchases.
9. Receives payout via UPI (Razorpay payout) — 85% of sale price, platform retains 15%.

### 6.2 Buyer journey (happy path)
1. Lands on CarbonKisan buyer dashboard (desktop, English).
2. Browses listing grid — filters by district, practice type, price range, minimum CO₂e.
3. Opens a listing detail — sees farmer name (first name + district only, for privacy), practice, SHAP-based estimate breakdown, asking price.
4. Adds to cart / buys directly.
5. Completes payment via Razorpay checkout (UPI/card/netbanking).
6. Receives instant PDF certificate — farmer detail (anonymised to district level), CO₂e tonnage, transaction hash, date.
7. Downloads a CSR reporting CSV export of all purchases to date for BRSR filing.

### 6.3 Admin journey (happy path)
1. Logs into `/admin` console (separate auth role).
2. Sees queue of listings flagged for review (e.g., estimate above 95th percentile for district).
3. Reviews farmer-submitted practice details, optionally requests photo evidence (Phase 2 feature — flagged as future in MVP).
4. Approves or rejects listing; rejection sends a reason back to farmer via SMS.

---

## 7. Functional Requirements

Each module below lists: description, user stories, functional requirements, acceptance criteria, priority (P0 = must-have for hackathon demo, P1 = strong add-on if time allows, P2 = explicitly post-hackathon).

### 7.1 Module: Authentication & Onboarding — **P0**

**User story:** As a farmer, I want to register with just my phone number so that I don't need an email or password I'll forget.

**Functional requirements:**
- FR-1.1: Phone number + OTP authentication via Supabase Auth (SMS OTP, 6-digit, 5-minute expiry).
- FR-1.2: Separate auth flow for buyers — email + password, or Google OAuth (buyers are corporate users comfortable with this).
- FR-1.3: Role field on user record: `farmer` | `buyer` | `admin`. Role determines which UI is served.
- FR-1.4: Session persistence for 30 days on farmer PWA (avoid repeated OTP friction for low-connectivity users).
- FR-1.5: Language selector shown on first launch: Marathi / Hindi / English. Stored in user profile, applied on every subsequent screen.

**Acceptance criteria:**
- A new farmer can go from "open app" to "authenticated, language set" in under 60 seconds.
- OTP retry limited to 3 attempts per 10 minutes (basic abuse prevention).

---

### 7.2 Module: Farmer Profile & Land Registration — **P0**

**User story:** As a farmer, I want to register my land details once so I don't have to re-enter them for every future listing.

**Functional requirements:**
- FR-2.1: Profile fields: full name, phone (from auth), district (dropdown), village (free text or dropdown if data available), total landholding (ha).
- FR-2.2: Support multiple land parcels per farmer (a farmer may practice different methods on different parcels).
- FR-2.3: Each parcel: area (ha), primary crop (dropdown: cotton, jowar, sugarcane, soybean, wheat, other), soil type (auto-suggested from district lookup, farmer can override if known).
- FR-2.4: Profile completion is NOT a blocking gate — a farmer can generate an estimate before completing full profile (reduce friction), but cannot publish a listing until profile is complete.

**Acceptance criteria:**
- Profile + first parcel can be completed in under 90 seconds on a low-end Android device.

---

### 7.3 Module: Practice Logging & Carbon Estimator — **P0 (core differentiator)**

**User story:** As a farmer, I want to know exactly how much money my farming practice is worth before I commit to listing it.

**Functional requirements:**
- FR-3.1: Practice selector — 4 options for MVP:
  1. No-till only
  2. Cover crop only
  3. No-till + cover crop (combined)
  4. Agroforestry
- FR-3.2: Each practice option shows an illustrated icon, one-line description, and expected sequestration range (transparency before commitment).
- FR-3.3: Season duration input: 6 or 12 months (dropdown).
- FR-3.4: On submission, call `POST /estimate` (see API spec §11) — returns tonnes CO₂e, confidence interval, INR estimate, and SHAP-based feature contribution breakdown.
- FR-3.5: SHAP breakdown rendered as a simple horizontal bar chart with plain-language labels: "Your practice: +1.43", "Your soil (Pune vertisol): +0.31", "Your rainfall zone: +0.05" — NOT raw SHAP values or technical jargon.
- FR-3.6: An "How we calculate this" info button opens a plain-language explainer modal (see §7.11 content requirements).
- FR-3.7: Estimate is saved to the `estimates` table regardless of whether the farmer proceeds to list it (useful data for future model retraining).

**Acceptance criteria:**
- Estimate returns in under 800ms (p95) from submission tap.
- SHAP breakdown values sum correctly to the total estimate (validated in testing).
- Every estimate has a persisted, retrievable ID for audit purposes.

---

### 7.4 Module: Listing Management — **P0**

**User story:** As a farmer, I want to list my estimated credits for sale at a price I control.

**Functional requirements:**
- FR-4.1: "List for Sale" button on estimate result screen.
- FR-4.2: Asking price pre-filled at suggested market rate (₹1,200–₹2,800/tonne band, mid-point default), editable by farmer within a sane band (±40% of suggested price — prevents absurd pricing that would damage buyer trust).
- FR-4.3: Listing status lifecycle: `pending_verification` → `live` → `sold` | `expired` | `rejected`.
- FR-4.4: Listings auto-expire after 90 days if unsold (configurable).
- FR-4.5: "My Listings" screen shows all of a farmer's listings with current status, and total lifetime earnings summary at the top.
- FR-4.6: Farmer can edit price or withdraw a listing while status is `live` (not after `sold`).

**Acceptance criteria:**
- Listing appears in buyer-facing marketplace within 5 seconds of status changing to `live`.
- Farmer cannot list more CO₂e than their estimate supports (server-side validation, not just client-side).

---

### 7.5 Module: Marketplace Browse & Discovery (Buyer side) — **P0**

**User story:** As a buyer, I want to filter listings by the criteria that matter for my CSR report so I can find credible, relevant credits fast.

**Functional requirements:**
- FR-5.1: Grid view of all `live` listings — card shows: district, practice type icon, CO₂e tonnes, price, farmer first name only (privacy).
- FR-5.2: Filters: district (multi-select), practice type (multi-select), price range (slider), minimum CO₂e (slider).
- FR-5.3: Sort options: price ascending/descending, CO₂e descending, most recent.
- FR-5.4: Listing detail view: full SHAP breakdown (same as farmer sees, buyer-facing framing), methodology summary, "Buy Now" button.
- FR-5.5: Search is client-side filterable for MVP scale (< 500 listings); server-side pagination required beyond that (flagged as Phase 2 trigger).

**Acceptance criteria:**
- Filter changes reflect in the grid in under 300ms (client-side filtering, no server round-trip for MVP data volume).

---

### 7.6 Module: Purchase & Payment — **P0**

**User story:** As a buyer, I want a fast, trustworthy checkout so procurement doesn't become a blocker.

**Functional requirements:**
- FR-6.1: "Buy Now" opens a confirmation modal showing: listing summary, total price, platform fee disclosure (transparency — show the 15% split explicitly to build trust), final total.
- FR-6.2: Razorpay Checkout integration — supports UPI, card, netbanking.
- FR-6.3: On successful payment, backend verifies Razorpay payment signature (HMAC-SHA256) before marking listing `sold` — never trust client-side success callback alone.
- FR-6.4: On confirmed sale: (a) listing status → `sold`, (b) transaction record created, (c) certificate PDF generated, (d) farmer payout initiated via Razorpay Payouts API (85% of sale price), (e) SMS sent to farmer.
- FR-6.5: Idempotency: duplicate webhook calls for the same payment must not create duplicate transactions (use Razorpay payment ID as idempotency key).

**Acceptance criteria:**
- A failed/cancelled payment leaves the listing in `live` status, unaffected.
- Payment confirmation to certificate availability is under 5 seconds end-to-end.

---

### 7.7 Module: Certificate Generation & Verification — **P0**

**User story:** As a buyer, I need a document I can hand to an auditor that proves this purchase is real and traceable.

**Functional requirements:**
- FR-7.1: PDF certificate generated server-side (ReportLab or WeasyPrint) containing: certificate ID (UUID), buyer name/org, farmer district + anonymised ID, practice type, CO₂e tonnes, issue date, SHA-256 hash of the underlying record, platform methodology version number.
- FR-7.2: A public verification page at `/verify/{certificate_id}` — anyone can paste a certificate ID and see a read-only confirmation that it's genuine, without exposing farmer PII.
- FR-7.3: Certificates are immutable once issued — no edit capability, only reissue-with-new-ID if a genuine correction is needed (with the old certificate marked `superseded`).

**Acceptance criteria:**
- Certificate PDF generates in under 3 seconds.
- Verification page correctly returns "not found" for invalid/tampered IDs.

---

### 7.8 Module: Impact Dashboard (Public Stats) — **P0 (demo-critical)**

**User story:** As anyone (judge, buyer, farmer, journalist), I want to see the platform's real aggregate impact at a glance.

**Functional requirements:**
- FR-8.1: Public page at `/impact` — no login required.
- FR-8.2: Live stats pulled from Supabase: total CO₂e listed (tonnes), total CO₂e sold (tonnes), total farmer income generated (₹), number of registered farmers, number of districts represented.
- FR-8.3: Simple bar chart: top 5 districts by CO₂e generated.
- FR-8.4: Auto-refreshes every 30 seconds (or on page load — sufficient for hackathon demo).

**Acceptance criteria:**
- Numbers on this page must always exactly match underlying database aggregates — this is the page judges will scrutinize hardest for internal consistency.

---

### 7.9 Module: Notifications — **P1**

**User story:** As a farmer, I want to know immediately when someone buys my credits, without having to check the app.

**Functional requirements:**
- FR-9.1: SMS notification via Twilio (or MSG91 for India-optimised pricing) on: listing approved, listing sold, payout completed.
- FR-9.2: Messages sent in farmer's selected language (Marathi/Hindi/English templates).
- FR-9.3 (P2 — post-hackathon): WhatsApp Business API integration for richer notifications with images/PDF certificate attachment.

**Acceptance criteria:**
- SMS delivery confirmed via provider webhook; failures logged for retry.

---

### 7.10 Module: Admin & Verification Console — **P1**

**User story:** As an admin, I want to review anomalous listings before they go live, so the platform maintains credibility.

**Functional requirements:**
- FR-10.1: Separate `/admin` route, role-gated.
- FR-10.2: Queue view: listings where estimate exceeds 95th percentile for that district+practice combination (statistical anomaly flag — simple z-score check, not ML in MVP).
- FR-10.3: Approve / Reject actions with mandatory reason text on reject.
- FR-10.4: Basic audit log: every admin action timestamped and attributed.

**Acceptance criteria:**
- Flagged listings never reach `live` status without explicit admin approval.

---

### 7.11 Module: Localization & Content — **P0 for farmer-facing, P1 for full toggle**

**Functional requirements:**
- FR-11.1: All farmer-facing UI strings externalised into a translation dictionary (`react-i18next` or equivalent), minimum 3 languages: Marathi, Hindi, English.
- FR-11.2: Buyer-facing UI is English-only for MVP (buyer persona is corporate, English is safe default) — flag Hindi buyer UI as P2.
- FR-11.3: "How we calculate this" explainer content — plain-language, no jargon, translated into all 3 languages. Content draft:
  > *"We estimate how much carbon your farming practice captures using real scientific research and your local soil and rainfall data. This is not a guarantee — it's our best estimate, shown as a range."*
- FR-11.4: Numeric formatting respects Indian numbering convention (lakh/crore separators) throughout.

**Acceptance criteria:**
- Zero hardcoded user-facing strings in farmer-side component code — all pulled from translation files.

---

### 7.12 Module: Offline / Low-Bandwidth Resilience — **P1**

**User story:** As a farmer in a field with poor signal, I don't want to lose my in-progress estimate.

**Functional requirements:**
- FR-12.1: Form state persisted to local storage as the farmer fills the estimator — recoverable if connection drops mid-flow.
- FR-12.2: Graceful degradation: if `/estimate` call fails, show a clear retry state, never a blank screen or raw error.
- FR-12.3: All images/icons served compressed (WebP, < 30KB each) — target total page weight under 500KB for the farmer flow.

**Acceptance criteria:**
- Farmer flow usable and testable on throttled "Slow 3G" network profile in Chrome DevTools.

---

## 8. Machine Learning Model Requirements

### 8.1 Problem framing
Regression task: predict `co2e_tonnes` (continuous, tonnes CO₂e per listing) given practice type, land area, and location-derived soil/rainfall features.

### 8.2 Features
| Feature | Type | Source |
|---|---|---|
| `practice_type` | Categorical (4 classes) | Farmer input |
| `area_ha` | Continuous | Farmer input |
| `season_months` | Categorical (6 or 12) | Farmer input |
| `soil_type` | Categorical | FAO HWSD India subset, looked up by district |
| `soc_baseline` | Continuous | ICRISAT district soil data |
| `rainfall_zone` | Categorical (low/medium/high) | IMD district rainfall normals |

### 8.3 Target variable
`co2e_tonnes` — synthetically generated for MVP using the formula:
```
co2e_tonnes = base_rate[practice] × area_ha × soil_modifier × (season_months / 12) + noise
```
where `base_rate` is drawn from the peer-reviewed meta-analysis range table (§8.5) and `noise ~ N(0, 0.1)`.

### 8.4 Model choice & justification
- **Algorithm:** XGBoost Regressor (`XGBRegressor`, objective `reg:squarederror`).
- **Why not linear regression:** soil × practice interactions are non-linear (confirmed in literature — XGBoost outperforms Adaboost/Bagging/Random Forest for Indian carbon stock prediction per published comparative study).
- **Why not a neural network:** dataset size (10,000 synthetic rows) and feature count (6) don't justify the complexity; XGBoost is more interpretable and faster to train/iterate within a 4-day window.
- **Hyperparameters (starting point):** `max_depth=6`, `n_estimators=200`, `learning_rate=0.05`, 5-fold cross-validation.

### 8.5 Ground-truth base rates (from peer-reviewed literature)
| Practice | Mean rate (t C/ha/yr) | Range |
|---|---|---|
| No-till + cover crop | 1.43 | 0.9–2.1 |
| Cover crop alone | 1.31 | 0.7–1.8 |
| No-till alone | 0.73 | 0.3–1.2 |
| Agroforestry | 0.67 | 0.4–1.1 |

### 8.6 Explainability requirement (non-negotiable)
- Every prediction MUST ship with a SHAP value breakdown.
- SHAP explainer (`TreeExplainer`) fit alongside the model, serialized separately (`explainer.pkl`).
- No estimate may be shown to a user without its explanation available.

### 8.7 Evaluation & acceptance thresholds
- RMSE on held-out test set (10% split): **< 0.15 tonnes CO₂e**.
- Top 2 SHAP features across the validation set must be `practice_type` and `soil_modifier` (sanity check that the model learned the right relationships, not spurious correlations).
- Manual validation: 10 hand-crafted test cases with literature-derived expected ranges must all fall within the model's predicted confidence interval.

### 8.8 Model card (required deliverable)
A `model_card.md` file must document: training data provenance (synthetic, parameterised by cited literature), feature list, evaluation metrics, known limitations (synthetic training data, no real-world field validation yet, Maharashtra-only soil data coverage), and intended use (estimate generation for marketplace listing — NOT for regulatory-grade MRV certification in current form).

### 8.9 Bias & fairness considerations
- Model must not systematically under-estimate credits for small landholdings (area < 1 ha) relative to large ones — check for size-based bias in validation.
- Soil data coverage must not silently exclude marginalized districts — if ICRISAT/FAO data is sparse for a district, the UI must show a wider confidence interval, not silently default to a generic value.

### 8.10 Retraining policy (post-MVP)
- As real transaction and verification data accumulates, retrain quarterly, blending synthetic and real-world verified outcomes.
- Version every model (`model_v1.pkl`, `model_v2.pkl`); every estimate stores which model version generated it (traceability for old certificates).

---

## 9. System Architecture

### 9.1 High-level component diagram (textual)
```
┌─────────────────────┐        ┌──────────────────────┐        ┌──────────────────────┐
│   Farmer PWA         │        │   Buyer Dashboard      │        │   Admin Console        │
│   React + Vite        │        │   React + Vite          │        │   React + Vite          │
│   (mobile-first)       │        │   (desktop-first)        │        │   (role-gated)           │
└──────────┬───────────┘        └──────────┬───────────┘        └──────────┬───────────┘
           │                                │                                │
           └────────────────────┬───────────┴────────────────────┬──────────┘
                                 │                                │
                          ┌──────▼────────────────────────────────▼──────┐
                          │             FastAPI Backend (Railway)          │
                          │  /estimate  /listings  /purchase  /certificate │
                          │  /admin/*   /auth/*    /notify                  │
                          └──────┬─────────────────┬────────────────┬─────┘
                                 │                 │                │
                    ┌────────────▼───┐   ┌─────────▼────────┐  ┌───▼──────────┐
                    │  XGBoost Model   │   │  Supabase          │  │  External APIs │
                    │  + SHAP Explainer │   │  (Postgres + Auth) │  │  Razorpay, SMS  │
                    │  (loaded in-process)│  │                    │  │                 │
                    └──────────────────┘   └────────────────────┘  └────────────────┘
```

### 9.2 Component responsibilities
| Component | Responsibility | Deployment |
|---|---|---|
| Farmer PWA | Practice logging, estimation UI, listing management | Vercel |
| Buyer Dashboard | Browse, filter, purchase, certificate download | Vercel (same repo, role-routed) |
| Admin Console | Listing review, approvals | Vercel (role-gated route) |
| FastAPI Backend | Business logic, model inference, orchestration | Railway (Docker) |
| XGBoost Model | Carbon estimation inference | Loaded in-process in FastAPI (no separate model server needed at MVP scale) |
| Supabase | Auth, Postgres database, Row-Level Security | Supabase managed cloud |
| Razorpay | Payment collection + farmer payouts | Third-party, India-native |
| SMS Provider (Twilio/MSG91) | Farmer notifications | Third-party |

### 9.3 Why this architecture (design rationale, for the PRD record)
- **Monolithic FastAPI backend, not microservices:** at hackathon/early-stage scale, a single deployable service minimizes operational overhead. Split into services only when a specific component (e.g., model inference) needs independent scaling.
- **Model loaded in-process, not a separate inference server:** XGBoost inference on 6 features is sub-millisecond; a separate model-serving layer (e.g., Seldon, BentoML) would add latency and complexity with no benefit at this scale.
- **Supabase over self-hosted Postgres:** eliminates DevOps overhead for auth, connection pooling, and row-level security — critical for a 4-day build window.

---

## 10. Data Model

### 10.1 Entity relationship summary
```
farmers ──1:N── land_parcels
farmers ──1:N── estimates
estimates ──1:1── listings
listings ──1:1── transactions
transactions ──1:1── certificates
buyers ──1:N── transactions
admins ──1:N── audit_log
```

### 10.2 Table: `farmers`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK, default `gen_random_uuid()` | Primary key |
| `phone` | VARCHAR(15) | UNIQUE, NOT NULL | Auth identifier |
| `full_name` | VARCHAR(120) | NOT NULL | Farmer's name |
| `district_code` | VARCHAR(10) | NOT NULL, FK → `districts.code` | Registered district |
| `village` | VARCHAR(120) | NULLABLE | Optional village name |
| `preferred_language` | ENUM('mr','hi','en') | DEFAULT 'mr' | UI language |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | Registration timestamp |
| `profile_complete` | BOOLEAN | DEFAULT false | Gate for listing creation |

### 10.3 Table: `land_parcels`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Primary key |
| `farmer_id` | UUID | FK → `farmers.id`, NOT NULL | Owner |
| `area_ha` | DECIMAL(6,2) | NOT NULL, CHECK > 0 | Parcel size |
| `primary_crop` | VARCHAR(50) | NOT NULL | e.g. cotton, jowar |
| `soil_type` | VARCHAR(50) | NOT NULL | Auto-suggested, overridable |
| `district_code` | VARCHAR(10) | FK → `districts.code` | For soil/rainfall lookup |

### 10.4 Table: `districts` (reference/lookup table)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `code` | VARCHAR(10) | PK | e.g. `MH_PUNE` |
| `name` | VARCHAR(80) | NOT NULL | District name |
| `soc_baseline` | DECIMAL(5,3) | NOT NULL | ICRISAT soil organic carbon baseline |
| `rainfall_zone` | ENUM('low','medium','high') | NOT NULL | IMD-derived classification |
| `dominant_soil_type` | VARCHAR(50) | NOT NULL | FAO HWSD lookup |
| `soil_modifier` | DECIMAL(4,3) | NOT NULL | Precomputed multiplier for model input |

### 10.5 Table: `estimates`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Primary key |
| `farmer_id` | UUID | FK → `farmers.id` | Requesting farmer |
| `parcel_id` | UUID | FK → `land_parcels.id`, NULLABLE | Linked parcel if selected |
| `practice_type` | ENUM(4 values) | NOT NULL | Practice used |
| `area_ha` | DECIMAL(6,2) | NOT NULL | Area used in this estimate |
| `season_months` | SMALLINT | NOT NULL, CHECK IN (6,12) | Duration |
| `co2e_tonnes` | DECIMAL(6,3) | NOT NULL | Model output |
| `confidence_low` | DECIMAL(6,3) | NOT NULL | Lower bound |
| `confidence_high` | DECIMAL(6,3) | NOT NULL | Upper bound |
| `inr_estimate` | INTEGER | NOT NULL | Estimated payout value |
| `shap_breakdown` | JSONB | NOT NULL | Feature contribution record |
| `model_version` | VARCHAR(20) | NOT NULL | e.g. `xgb_v1` |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

### 10.6 Table: `listings`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Primary key |
| `estimate_id` | UUID | FK → `estimates.id`, UNIQUE | One listing per estimate |
| `farmer_id` | UUID | FK → `farmers.id` | Denormalised for query speed |
| `asking_price_inr` | INTEGER | NOT NULL, CHECK > 0 | Farmer-set price |
| `status` | ENUM('pending_verification','live','sold','expired','rejected') | DEFAULT 'pending_verification' | Lifecycle state |
| `rejection_reason` | TEXT | NULLABLE | Set on admin reject |
| `published_at` | TIMESTAMPTZ | NULLABLE | When moved to `live` |
| `expires_at` | TIMESTAMPTZ | NOT NULL | `published_at + 90 days` |

### 10.7 Table: `buyers`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Primary key |
| `email` | VARCHAR(150) | UNIQUE, NOT NULL | Auth identifier |
| `org_name` | VARCHAR(150) | NOT NULL | Company/NGO name |
| `contact_name` | VARCHAR(120) | NOT NULL | Point of contact |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

### 10.8 Table: `transactions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Primary key |
| `listing_id` | UUID | FK → `listings.id`, UNIQUE | One transaction per listing |
| `buyer_id` | UUID | FK → `buyers.id` | Purchaser |
| `razorpay_payment_id` | VARCHAR(60) | UNIQUE, NOT NULL | Idempotency key |
| `amount_paid_inr` | INTEGER | NOT NULL | Total charged |
| `platform_fee_inr` | INTEGER | NOT NULL | 15% cut |
| `farmer_payout_inr` | INTEGER | NOT NULL | 85% payout |
| `payout_status` | ENUM('pending','processing','completed','failed') | DEFAULT 'pending' | Razorpay payout state |
| `paid_at` | TIMESTAMPTZ | DEFAULT now() | |

### 10.9 Table: `certificates`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Certificate ID (public-facing) |
| `transaction_id` | UUID | FK → `transactions.id`, UNIQUE | Source transaction |
| `record_hash` | VARCHAR(64) | NOT NULL | SHA-256 of underlying data |
| `pdf_url` | TEXT | NOT NULL | Storage location |
| `methodology_version` | VARCHAR(20) | NOT NULL | For traceability |
| `status` | ENUM('active','superseded') | DEFAULT 'active' | |
| `issued_at` | TIMESTAMPTZ | DEFAULT now() | |

### 10.10 Table: `admin_audit_log`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | PK | Primary key |
| `admin_id` | UUID | FK → `admins.id` | Actor |
| `action` | VARCHAR(50) | NOT NULL | e.g. `listing_approved` |
| `target_id` | UUID | NOT NULL | Affected record ID |
| `reason` | TEXT | NULLABLE | For rejections |
| `created_at` | TIMESTAMPTZ | DEFAULT now() | |

### 10.11 Row-Level Security policy summary
- Farmers can `SELECT`/`UPDATE` only rows where `farmer_id = auth.uid()`.
- Buyers can `SELECT` only `live` or their own `sold` listings; can `INSERT` only into `transactions` via backend service role (never direct client writes to prevent payment bypass).
- Admins use a service-role key server-side only — never exposed to any frontend.

---

## 11. API Specification (Complete)

### 11.1 Authentication
| Endpoint | Method | Description |
|---|---|---|
| `/auth/otp/request` | POST | Send OTP to farmer phone number |
| `/auth/otp/verify` | POST | Verify OTP, return session token |
| `/auth/buyer/login` | POST | Email/password or OAuth for buyers |

### 11.2 Farmer & Estimation
| Endpoint | Method | Request body | Response |
|---|---|---|---|
| `/profile` | POST | `{full_name, district_code, village}` | `{farmer_id, profile_complete}` |
| `/parcels` | POST | `{area_ha, primary_crop, district_code}` | `{parcel_id, soil_type_suggested}` |
| `/estimate` | POST | `{practice_type, area_ha, district_code, season_months, parcel_id?}` | `{estimate_id, co2e_tonnes, confidence_low, confidence_high, inr_estimate, shap_breakdown}` |

### 11.3 Listings
| Endpoint | Method | Request | Response |
|---|---|---|---|
| `/listings` | POST | `{estimate_id, asking_price_inr}` | `{listing_id, status}` |
| `/listings` | GET | Query params: `district, practice, min_price, max_price, min_co2e, sort` | Array of listing summaries |
| `/listings/{id}` | GET | — | Full listing detail incl. SHAP breakdown |
| `/listings/{id}` | PATCH | `{asking_price_inr?}` or `{status: "withdrawn"}` | Updated listing |
| `/my-listings` | GET | (auth: farmer) | Farmer's own listings + lifetime earnings summary |

### 11.4 Purchase & Payment
| Endpoint | Method | Request | Response |
|---|---|---|---|
| `/purchase/initiate` | POST | `{listing_id}` | `{razorpay_order_id, amount}` |
| `/purchase/confirm` | POST | `{razorpay_payment_id, razorpay_order_id, razorpay_signature}` | `{transaction_id, certificate_id}` |
| `/purchase/webhook` | POST | (Razorpay server callback) | `200 OK` (idempotent handler) |

### 11.5 Certificates
| Endpoint | Method | Request | Response |
|---|---|---|---|
| `/certificate/{id}` | GET | — | PDF file stream |
| `/verify/{id}` | GET | — | `{valid: bool, district, practice, co2e_tonnes, issued_at}` (no PII) |
| `/buyer/export` | GET | (auth: buyer) | CSV of all purchases for CSR reporting |

### 11.6 Impact & Public Stats
| Endpoint | Method | Response |
|---|---|---|
| `/impact/stats` | GET | `{total_co2e_listed, total_co2e_sold, total_farmer_income_inr, farmer_count, district_count, top_districts[]}` |

### 11.7 Admin
| Endpoint | Method | Request | Response |
|---|---|---|---|
| `/admin/queue` | GET | (auth: admin) | Flagged listings pending review |
| `/admin/listings/{id}/approve` | POST | — | `{status: "live"}` |
| `/admin/listings/{id}/reject` | POST | `{reason}` | `{status: "rejected"}` |

### 11.8 Notifications (internal, triggered server-side)
| Trigger | Channel | Template key |
|---|---|---|
| Listing approved | SMS | `listing_approved_{lang}` |
| Listing sold | SMS | `listing_sold_{lang}` |
| Payout completed | SMS | `payout_completed_{lang}` |

### 11.9 Sample request/response — `POST /estimate`
```json
// Request
{
  "practice_type": "no_till_cover_crop",
  "area_ha": 2.5,
  "district_code": "MH_PUNE",
  "season_months": 6
}

// Response — 200 OK
{
  "estimate_id": "e7f3a2b1-...",
  "co2e_tonnes": 1.79,
  "confidence_low": 1.12,
  "confidence_high": 2.63,
  "inr_estimate": 2148,
  "model_version": "xgb_v1",
  "shap_breakdown": {
    "base_practice": 1.430,
    "soil_modifier": 0.312,
    "rainfall_zone": 0.048,
    "area_scaling": 0.000
  }
}
```

### 11.10 Error handling standard
All error responses follow a consistent shape:
```json
{
  "error": {
    "code": "INVALID_AREA",
    "message": "Land area must be between 0.5 and 10 hectares.",
    "field": "area_ha"
  }
}
```
HTTP status codes: `400` validation errors, `401` unauthenticated, `403` unauthorized (wrong role), `404` not found, `409` conflict (e.g., double-purchase attempt), `500` server error (logged to Sentry, generic message to client).

---

## 12. Non-Functional Requirements

### 12.1 Performance
| Requirement | Target |
|---|---|
| `/estimate` API p95 latency | < 800ms |
| `/listings` browse API p95 latency | < 500ms |
| Farmer PWA first contentful paint (Slow 3G) | < 3s |
| PDF certificate generation | < 3s |

### 12.2 Scalability
- MVP target: 500 concurrent users, 10,000 listings, no architectural changes needed.
- Beyond 10,000 listings: move `/listings` browse from client-side filtering to server-side paginated queries with Postgres indexes on `district_code`, `practice_type`, `status`.

### 12.3 Security
- All API traffic over HTTPS only (enforced at Railway/Vercel edge).
- Razorpay webhook signature verification mandatory — reject unsigned/invalid callbacks.
- Supabase Row-Level Security enforced on every table — no table accessible without RLS policy.
- No PII (farmer full name, phone) ever exposed to buyer-facing endpoints — only district + first name.
- Admin service-role key stored only in backend environment variables, never in any frontend bundle.
- Rate limiting on `/auth/otp/request`: max 3 requests per phone number per 10 minutes.

### 12.4 Compliance considerations (flagged, not fully implemented in MVP)
- **DPDP Act 2023 (India's data protection law):** farmer phone numbers and names are personal data. Consent language must be shown at registration. Data retention/deletion policy required before any real production launch — flagged as a pre-launch legal review item, not hackathon scope.
- **RBI Payment Aggregator guidelines:** the platform is currently a pass-through using Razorpay as the licensed PA — CarbonKisan itself does not need a separate PA license as long as funds flow through Razorpay's compliant rails. This must be verified with legal counsel before real-money production launch.
- **Carbon credit methodology compliance:** MVP explicitly does NOT claim Verra/Gold Standard equivalence. All UI copy must describe credits as "platform-estimated" not "internationally certified" to avoid misrepresentation.

### 12.5 Accessibility
- Buyer dashboard: WCAG 2.1 AA target — keyboard navigable, sufficient color contrast (all palette combinations in §13 checked against 4.5:1 minimum for body text).
- Farmer PWA: designed for low-literacy use — icon-first, minimal text-only decision points, large tap targets (minimum 44×44px).

### 12.6 Browser & device support
- Farmer PWA: Chrome/Android WebView on Android 8+, tested on low-end devices (2GB RAM baseline).
- Buyer Dashboard: Chrome, Edge, Firefox, Safari — latest 2 versions.

---

## 13. Design System

### 13.1 Color palette
| Token | Hex | Usage |
|---|---|---|
| `--soil` | `#2C1A0E` | Dark backgrounds, headers |
| `--leaf` | `#1A4A2E` | Primary brand dark |
| `--leaf-mid` | `#2D7A4F` | Primary interactive color |
| `--leaf-light` | `#4FAE7A` | Accents, success states |
| `--sky` | `#E8F4EC` | Light backgrounds, highlight fills |
| `--gold` | `#C8922A` | Price/value indicators |
| `--gold-light` | `#F5E4C0` | Warning/highlight fills |
| `--ink` | `#1C1C1A` | Primary text |
| `--muted` | `#6B6B62` | Secondary text |
| `--page` | `#F7F5F0` | Page background |

### 13.2 Typography
| Role | Typeface | Usage |
|---|---|---|
| Display | Fraunces (serif, italic for emphasis) | Headlines, brand moments |
| Body / UI | Space Grotesk (sans) | All interface text, buttons, labels |
| Data / Code | JetBrains Mono | Numbers, technical labels, certificate IDs |

### 13.3 Component inventory required
- Practice selector cards (illustrated, 4 variants)
- Area slider with live value display
- SHAP breakdown bar chart component (reusable for farmer + buyer views)
- Listing card (grid item)
- Filter sidebar (buyer dashboard)
- Confirmation modal (purchase flow)
- Status badge (5 variants matching listing lifecycle states)
- SMS-style toast notifications (in-app confirmation of async events)
- Language toggle switch (farmer PWA)

---

## 14. Analytics & Event Tracking

| Event name | Trigger | Key properties |
|---|---|---|
| `farmer_registered` | Successful OTP verification | `district_code`, `language` |
| `estimate_generated` | `/estimate` success | `practice_type`, `co2e_tonnes`, `district_code` |
| `listing_created` | Listing published | `listing_id`, `asking_price_inr` |
| `listing_viewed` | Buyer opens listing detail | `listing_id`, `buyer_id` |
| `purchase_initiated` | Razorpay checkout opened | `listing_id` |
| `purchase_completed` | Payment confirmed | `transaction_id`, `amount_paid_inr` |
| `certificate_downloaded` | PDF fetch | `certificate_id` |
| `csr_export_downloaded` | Buyer exports CSV | `buyer_id`, `record_count` |

Recommended tool: PostHog (self-hostable, generous free tier, works well with React).

---

## 15. Testing Requirements

### 15.1 Unit tests
- Model inference function: verify output shape and value bounds for known inputs.
- Estimate formula: verify SHAP values sum to total estimate.
- Payment signature verification function: verify rejects tampered signatures.

### 15.2 Integration tests
- Full farmer flow: register → estimate → list (automated via Playwright or Cypress).
- Full buyer flow: browse → filter → purchase → certificate download.
- Webhook idempotency: send duplicate Razorpay webhook, assert only one transaction created.

### 15.3 Model validation tests
- 10 hand-crafted cases against literature-derived expected ranges (see §8.7).
- Bias check: compare mean estimate per hectare across small (<1ha) vs large (>5ha) parcels — flag if statistically different beyond expected linear scaling.

### 15.4 User acceptance testing (UAT) script
1. A non-technical person (ideally someone who speaks Marathi) completes the farmer flow unassisted — time it, note every point of confusion.
2. A person unfamiliar with the project completes the buyer flow unassisted — same protocol.

---

## 16. Release Plan

### 16.1 Phase 0 — Hackathon MVP (4 days, this document's primary scope)
Everything marked **P0** above. Seeded demo data. Test-mode payments only.

### 16.2 Phase 1 — Post-hackathon pilot (Weeks 1–8)
- All **P1** features (notifications, admin console, offline resilience).
- Real Razorpay production credentials + KYC.
- Partner with 1–2 FPOs in Pune district for first 50 real farmer registrations.
- Legal review: DPDP Act consent flows, Payment Aggregator compliance confirmation.

### 16.3 Phase 2 — Verification & scale (Months 3–6)
- Satellite-based practice verification (Sentinel-2 NDVI analysis) to reduce self-report fraud risk.
- WhatsApp Business API notifications.
- Expand beyond Maharashtra to Punjab (strong no-till data availability) and Karnataka.
- Real-data model retraining (blend synthetic + verified field outcomes).

### 16.4 Phase 3 — Marketplace maturity (Months 6–12)
- Buyer subscription tier for bulk purchasing + advanced ESG reporting.
- FPO/cooperative bulk-listing tools (aggregate multiple small farmers into one certified project, approaching Verra-scale credibility for larger buyers).
- Blockchain-anchored certificate hashes for enhanced tamper-evidence (optional — evaluate real need vs. current SHA-256 approach first).

---

## 17. Risks, Assumptions & Dependencies (RAID Log)

| Type | Item | Impact | Mitigation |
|---|---|---|---|
| Risk | Self-reported practices cannot be verified in MVP | Medium — credibility risk with buyers | Disclose transparently; roadmap satellite verification in Phase 2; statistical anomaly flagging in admin console |
| Risk | Synthetic training data may not generalize to real field conditions | Medium | Model card discloses this explicitly; retraining policy defined for Phase 2 |
| Risk | RBI/DPDP compliance gaps in payment/data handling | High (for real launch, not hackathon) | Legal review gated before Phase 1 real-money launch |
| Assumption | Farmers have reliable access to a smartphone (own or shared/family) | — | Validated by existing UPI/WhatsApp usage patterns among target persona |
| Assumption | ICRISAT/FAO/IMD public datasets remain freely accessible | — | Cache downloaded datasets locally; don't depend on live API calls for core model features |
| Dependency | Razorpay account approval (may require business KYC) | High for real payments | Use Razorpay test mode for hackathon demo; start KYC process in parallel if pursuing Phase 1 |
| Dependency | Supabase free tier limits (500MB DB, 50K auth users) | Low for MVP scale | Sufficient for hackathon + early pilot; upgrade path is a config change, not a rearchitecture |

---

## 18. Required Materials & Resource Checklist

### 18.1 Accounts to create (all free tier sufficient for hackathon)
- [ ] Supabase project (database + auth)
- [ ] Razorpay account (test mode API keys — no KYC needed for test mode)
- [ ] Vercel account (frontend hosting)
- [ ] Railway or Render account (backend hosting)
- [ ] Twilio or MSG91 account (SMS — trial credits sufficient for demo)
- [ ] GitHub repository (public, for submission)
- [ ] Google Fonts (Fraunces, Space Grotesk, JetBrains Mono — free, no account needed)

### 18.2 Datasets to download before Day 1
- [ ] ICRISAT village-level soil data (vdsa.icrisat.org)
- [ ] IMD district rainfall normals (imdpune.gov.in) or Open-Meteo historical API as fallback
- [ ] FAO Harmonised World Soil Database v2, India/Maharashtra subset
- [ ] Frontiers meta-analysis (2023) Table 2 — sequestration rates by practice
- [ ] Maharashtra district boundary shapefile (data.gov.in)

### 18.3 Software / tooling
- [ ] Python 3.11 + virtual environment
- [ ] Node.js 18+ and npm/pnpm
- [ ] QGIS (free) — for clipping FAO soil shapefile to Maharashtra
- [ ] Docker (for Railway backend deployment)
- [ ] Postman or Thunder Client (API testing during development)

### 18.4 Team roles (even if solo-built, these are the hats to wear)
| Role | Responsibility | Day focus |
|---|---|---|
| Data/ML engineer | Dataset prep, model training, SHAP validation | Day 1 |
| Backend engineer | FastAPI, Supabase schema, Razorpay integration | Day 2 |
| Frontend engineer | React farmer + buyer flows | Day 3 |
| Product/QA + pitch | Demo data seeding, judge-question prep, pitch narrative | Day 4 |

### 18.5 Budget estimate (hackathon — should be ₹0)
All required services have free tiers sufficient for a hackathon MVP: Supabase free tier, Razorpay test mode (no cost), Vercel free tier, Railway free trial credits, Twilio trial credits, all datasets are free public government/research data.

### 18.6 Budget estimate (Phase 1 pilot, monthly)
| Item | Estimated monthly cost |
|---|---|
| Supabase Pro (if free tier exceeded) | ₹2,000 |
| Railway backend hosting | ₹1,500 |
| SMS (MSG91, ~2,000 messages) | ₹1,000 |
| Domain name + SSL | ₹100 (amortized) |
| **Total** | **~₹4,600/month** |

---

## 19. Glossary

| Term | Definition |
|---|---|
| CO₂e | Carbon dioxide equivalent — standard unit for expressing greenhouse gas impact |
| VCM | Voluntary Carbon Market |
| MRV | Measurement, Reporting, Verification — the process of validating claimed carbon impact |
| BEE | Bureau of Energy Efficiency (India) — regulates domestic carbon credit methodologies |
| CCTS | Carbon Credit Trading Scheme — India's compliance carbon market for industrial sectors |
| SHAP | SHapley Additive exPlanations — a method for explaining individual ML model predictions |
| FPO | Farmer Producer Organisation |
| BRSR | Business Responsibility and Sustainability Report — mandatory ESG disclosure for large Indian listed companies |
| RLS | Row-Level Security — database-enforced per-row access control |
| SOC | Soil Organic Carbon |

---

## 20. References

Data points and figures used throughout this document are drawn from: a Frontiers Sustainable Food Systems meta-analysis on regenerative agriculture carbon sequestration (2023); a Frontiers Climate study applying the RothC soil carbon model to western India croplands (2026); India's official carbon credit market size and CCTS reporting (IMARC market report, 2025); India's Ministry of Environment carbon pricing framework documentation (PIB); the Economic and Political Weekly's coverage of India's agricultural voluntary carbon market framework (2025); and current 2026 Indian carbon credit pricing data (Costmos, CarbonMinus, Grow Billion Trees market trackers).

---

*End of document. This PRD is a living document — update version number and changelog on every material revision post-hackathon.*
