# CarbonKisan

A carbon credit micro-marketplace connecting Indian smallholder farmers directly
to corporate carbon-offset buyers. Built for the AMIEE Hackathon.

## Structure
- `backend/` — FastAPI + XGBoost carbon estimation service
- `frontend/` — React 19 farmer/buyer/impact PWA
- `docs/schema.sql` — full database schema, paste into Supabase SQL Editor
- `docs/` — add `CarbonKisan_PRD.md` and `CarbonKisan_TechStack.md` here from the earlier deliverables

## Quickstart
1. Create a Supabase project, run `docs/schema.sql` in the SQL Editor.
2. Import `backend/data/maharashtra_districts.csv` into the `districts` table via Supabase's CSV import.
3. `cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
4. `cp backend/.env.example backend/.env` — fill in real values.
5. `python app/ml/generate_synthetic.py && python app/ml/train.py` — trains and saves the model.
6. `fastapi dev app/main.py --port 8000` — backend running.
7. `cd frontend && npm install && cp .env.example .env.local` — fill in real values.
8. `npm run dev` — frontend running at localhost:5173.

## Known gaps in this starter (marked in-code with comments, not hidden)
- District soil/rainfall data is placeholder, not sourced ICRISAT/FAO data — see `backend/data/maharashtra_districts.csv` header.
- `purchase.py`'s order→listing mapping is a simplified placeholder — replace before real money moves.
- Several routes described in the PRD (`/farmer/my-listings` UI, `/buyer/checkout` UI, `/admin/queue` UI, `/verify/:id` UI) have working backend endpoints but no frontend page yet — same pattern as `Estimator.jsx`, extend `App.jsx`.
- Supabase Storage wiring for certificate PDFs is stubbed, not implemented.
