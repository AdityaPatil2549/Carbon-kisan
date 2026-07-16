# CarbonKisan Backend

FastAPI backend for the CarbonKisan carbon credit micro-marketplace.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real values
```

## Train the model (required before first run)
```bash
python app/ml/generate_synthetic.py
python app/ml/train.py
```

## Run
```bash
fastapi dev app/main.py --port 8000
```

## Test
```bash
pytest tests/ -v
```

See `/docs/CarbonKisan_PRD.md` and `/docs/CarbonKisan_TechStack.md` in the repo root for full specification.
