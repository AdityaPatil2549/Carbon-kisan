from collections import defaultdict
from fastapi import APIRouter
from app.models.db import supabase

router = APIRouter()


@router.get("/impact/stats")
async def get_impact_stats():
    # Fetch all necessary data
    estimates = supabase.table("estimates").select("*, farmers(district_code)").execute().data
    listings = supabase.table("listings").select("status, estimates(co2e_tonnes)").execute().data
    transactions = supabase.table("transactions").select("farmer_payout_inr").execute().data
    farmers = supabase.table("farmers").select("id, district_code").execute().data
    districts = supabase.table("districts").select("code, name").execute().data
    
    district_name_map = {d["code"]: d["name"] for d in districts} if districts else {}

    # Total CO2e Listed
    total_co2e_listed = round(sum(e["co2e_tonnes"] for e in estimates), 2)
    
    # Total CO2e Sold
    total_co2e_sold = 0
    for l in listings:
        if l.get("status") == "sold" and l.get("estimates"):
            total_co2e_sold += l["estimates"].get("co2e_tonnes", 0)
    total_co2e_sold = round(total_co2e_sold, 2)
            
    # Total Farmer Income
    total_farmer_income = sum(t["farmer_payout_inr"] for t in transactions)
    
    # District Count
    unique_districts = set(f["district_code"] for f in farmers if f.get("district_code"))
    district_count = len(unique_districts)
    
    # Top Districts by CO2e (listed + sold)
    district_co2e = defaultdict(float)
    for e in estimates:
        dcode = e.get("farmers", {}).get("district_code")
        if dcode:
            district_co2e[dcode] += e.get("co2e_tonnes", 0)
            
    sorted_districts = sorted(district_co2e.items(), key=lambda x: x[1], reverse=True)[:5]
    top_districts = [
        {
            "district_code": dcode,
            "district_name": district_name_map.get(dcode, dcode),
            "total_co2e": round(amount, 2)
        }
        for dcode, amount in sorted_districts
    ]

    return {
        "total_co2e_listed": total_co2e_listed,
        "total_co2e_sold": total_co2e_sold,
        "total_transactions": len(transactions),
        "total_farmer_income_inr": total_farmer_income,
        "farmer_count": len(farmers),
        "district_count": district_count,
        "top_districts": top_districts
    }
