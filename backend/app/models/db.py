"""
CarbonKisan — Database client.

Uses real Supabase when credentials are provided.
Falls back to an in-memory mock store for local development.
The mock store implements the same interface so all router code
works identically — just swap SUPABASE_URL in .env to go live.
"""
import csv
import os
import uuid
from datetime import datetime, timezone
from app.config import settings


# ─── In-memory mock store for development ───

class MockQueryResult:
    """Mimics supabase-py response shape."""
    def __init__(self, data):
        self.data = data


class MockTableQuery:
    """Minimal mock of supabase table query builder — supports the chained
    methods used in routers (select, eq, gte, lte, insert, update, single)."""

    def __init__(self, store, table_name):
        self._store = store
        self._table = table_name
        self._filters = []
        self._select_cols = "*"
        self._is_single = False
        self._mode = "select"
        self._insert_data = None
        self._update_data = None

    def select(self, cols="*"):
        self._select_cols = cols
        self._mode = "select"
        return self

    def insert(self, data):
        self._mode = "insert"
        self._insert_data = data
        return self

    def update(self, data):
        self._mode = "update"
        self._update_data = data
        return self

    def eq(self, col, val):
        self._filters.append(("eq", col, val))
        return self

    def gte(self, col, val):
        self._filters.append(("gte", col, val))
        return self

    def lte(self, col, val):
        self._filters.append(("lte", col, val))
        return self

    def single(self):
        self._is_single = True
        return self

    def _apply_filters(self, rows):
        result = rows
        for op, col, val in self._filters:
            if op == "eq":
                result = [r for r in result if r.get(col) == val]
            elif op == "gte":
                result = [r for r in result if r.get(col, 0) >= val]
            elif op == "lte":
                result = [r for r in result if r.get(col, 0) <= val]
        return result

    def execute(self):
        table_data = self._store.setdefault(self._table, [])

        if self._mode == "insert":
            row = dict(self._insert_data)
            if "id" not in row:
                row["id"] = str(uuid.uuid4())
            if "created_at" not in row:
                row["created_at"] = datetime.now(timezone.utc).isoformat()
            table_data.append(row)
            return MockQueryResult([row])

        elif self._mode == "update":
            filtered = self._apply_filters(table_data)
            for row in filtered:
                row.update(self._update_data)
            return MockQueryResult(filtered)

        else:  # select
            filtered = self._apply_filters(table_data)

            # Handle embedded resource selects (e.g., "*, estimates(*)")
            if "estimates(" in self._select_cols or "farmers(" in self._select_cols:
                for row in filtered:
                    if "estimate_id" in row and "estimates" not in row:
                        estimates = self._store.get("estimates", [])
                        match = [e for e in estimates if e.get("id") == row.get("estimate_id")]
                        row["estimates"] = match[0] if match else {}
                    if "farmer_id" in row and "farmers" not in row:
                        farmers = self._store.get("farmers", [])
                        match = [f for f in farmers if f.get("id") == row.get("farmer_id")]
                        row["farmers"] = match[0] if match else {}
                    if "listing_id" in row and "listings" not in row:
                        listings_data = self._store.get("listings", [])
                        match = [l for l in listings_data if l.get("id") == row.get("listing_id")]
                        row["listings"] = match[0] if match else {}
                    if "transaction_id" in row and "transactions" not in row:
                        txns = self._store.get("transactions", [])
                        match = [t for t in txns if t.get("id") == row.get("transaction_id")]
                        row["transactions"] = match[0] if match else {}

            if self._is_single:
                return MockQueryResult(filtered[0] if filtered else None)
            return MockQueryResult(filtered)


class MockSupabaseClient:
    """In-memory mock that replaces supabase-py for local development."""

    def __init__(self):
        self._store = {}
        self._seed_districts()

    def table(self, name):
        return MockTableQuery(self._store, name)

    def _seed_districts(self):
        """Load Maharashtra districts from CSV into the mock store."""
        csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "maharashtra_districts.csv")
        csv_path = os.path.normpath(csv_path)
        districts = []
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    districts.append({
                        "code": row["code"],
                        "name": row["name"],
                        "rainfall_zone": row["rainfall_zone"],
                        "dominant_soil_type": row["dominant_soil_type"],
                        "soil_modifier": float(row["soil_modifier"]),
                        "verified": row.get("verified", "FALSE") == "TRUE",
                    })
        self._store["districts"] = districts
        self._store["districts"].extend([
            {"code": "GJ_SURAT", "name": "Surat", "rainfall_zone": "medium", "dominant_soil_type": "vertisol", "soil_modifier": 1.10, "verified": False},
            {"code": "KA_BENGALURU", "name": "Bengaluru", "rainfall_zone": "medium", "dominant_soil_type": "laterite", "soil_modifier": 1.05, "verified": False}
        ])
    def seed_demo_data(self):
        """Seed demo farmers, estimates, listings for development."""
        demo_districts = ["MH_PUNE", "MH_NAGPUR", "GJ_SURAT", "KA_BENGALURU", "MH_SATARA"]
        practices = ["no_till", "cover_crop", "no_till_cover_crop", "agroforestry"]
        names = [
            "Rajesh Patil", "Sunita Jadhav", "Anil Deshmukh", "Priya Kulkarni",
            "Manoj Shinde", "Kavita Pawar", "Sachin More", "Lata Bhosale",
            "Deepak Chavan", "Anita Gaikwad", "Vikram Sarode", "Suman Kale"
        ]

        # Demo farmers
        for i, name in enumerate(names):
            district = demo_districts[i % len(demo_districts)]
            farmer_id = str(uuid.uuid4())
            self._store.setdefault("farmers", []).append({
                "id": farmer_id,
                "phone": f"98{20000000 + i}",
                "full_name": name,
                "district_code": district,
                "village": f"Village {i+1}",
                "preferred_language": "mr",
                "profile_complete": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

            # Each farmer gets 1 estimate + listing
            practice = practices[i % len(practices)]
            area = round(1.0 + (i * 0.7), 2)
            co2e = round(area * (0.73 + i * 0.1), 3)
            inr = int(co2e * 1800)
            estimate_id = str(uuid.uuid4())
            self._store.setdefault("estimates", []).append({
                "id": estimate_id,
                "farmer_id": farmer_id,
                "practice_type": practice,
                "area_ha": area,
                "season_months": 12 if i % 2 == 0 else 6,
                "co2e_tonnes": co2e,
                "confidence_low": round(co2e * 0.8, 3),
                "confidence_high": round(co2e * 1.2, 3),
                "inr_estimate": inr,
                "shap_breakdown": {
                    "base_practice": round(co2e * 0.4, 3),
                    "soil_modifier": round(co2e * 0.3, 3),
                    "rainfall_zone": round(co2e * 0.15, 3),
                    "area_scaling": round(co2e * 0.15, 3),
                },
                "model_version": "xgb_v1",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })

            listing_id = str(uuid.uuid4())
            status = "live" if i < 10 else "pending_verification"
            self._store.setdefault("listings", []).append({
                "id": listing_id,
                "estimate_id": estimate_id,
                "farmer_id": farmer_id,
                "asking_price_inr": inr,
                "status": status,
                "published_at": datetime.now(timezone.utc).isoformat() if status == "live" else None,
                "expires_at": "2026-10-15T00:00:00Z",
            })

        # Demo buyers
        for j in range(2):
            self._store.setdefault("buyers", []).append({
                "id": str(uuid.uuid4()),
                "email": f"buyer{j+1}@example.com",
                "org_name": f"GreenCorp {j+1}",
                "contact_name": f"Buyer Contact {j+1}",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })


# ─── Factory ───

def _create_client():
    if settings.use_mock_db:
        print("WARNING: Using in-memory mock database (no Supabase credentials found)")
        client = MockSupabaseClient()
        client.seed_demo_data()
        return client
    else:
        from supabase import create_client
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def get_supabase():
    return supabase


supabase = _create_client()
