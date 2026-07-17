import os
import sys
import uuid
import time
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "carbonkisan-starter", "backend", ".env"))

# Add backend directory to sys.path so we can import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), "carbonkisan-starter", "backend"))

from app.models.db import supabase
from supabase import create_client
import os

def seed_accounts():
    print("Seeding test accounts in Supabase...")
    
    # Create a separate client for auth to avoid polluting the service client session
    from app.config import settings
    auth_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

    # Define test users
    pro_farmer_phone = "9999999999"
    pro_farmer_email = "farmer_long@carbonkisan.com"
    new_farmer_phone = "8888888888"
    new_farmer_email = "farmer_new@carbonkisan.com"
    password = "password123"

    print("Creating auth users...")
    # Create or update Pro Farmer
    try:
        pro_user = auth_client.auth.admin.create_user({
            "email": pro_farmer_email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"role": "farmer", "phone": pro_farmer_phone}
        })
        pro_id = pro_user.user.id
        print(f"Created Pro Farmer: {pro_id}")
    except Exception as e:
        print(f"Pro Farmer may already exist: {e}")
        # Try to fetch existing
        # Using a workaround if we don't have list_users easily
        # For simplicity, we can't easily fetch user by email without listing them all, but let's assume they were created or just proceed.
        # Actually, let's just use the exception to get the ID if we can't, but wait, the easiest is to just proceed if it fails or try to sign in to get the ID.
        try:
            res = auth_client.auth.sign_in_with_password({"email": pro_farmer_email, "password": password})
            pro_id = res.user.id
            print(f"Found existing Pro Farmer: {pro_id}")
        except Exception as e2:
            print("Failed to login as Pro Farmer to get ID:", e2)
            sys.exit(1)

    # Create or update New Farmer
    try:
        new_user = auth_client.auth.admin.create_user({
            "email": new_farmer_email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"role": "farmer", "phone": new_farmer_phone}
        })
        new_id = new_user.user.id
        print(f"Created New Farmer: {new_id}")
    except Exception as e:
        print(f"New Farmer may already exist: {e}")
        try:
            res = auth_client.auth.sign_in_with_password({"email": new_farmer_email, "password": password})
            new_id = res.user.id
            print(f"Found existing New Farmer: {new_id}")
        except Exception as e2:
            print("Failed to login as New Farmer to get ID:", e2)
            sys.exit(1)

    print("Creating Buyer...")
    # Create a buyer for the transactions
    buyer_email = "buyer_seed@carbonkisan.com"
    try:
        buyer_user = auth_client.auth.admin.create_user({
            "email": buyer_email,
            "password": password,
            "email_confirm": True,
            "user_metadata": {"role": "buyer", "org_name": "EcoCorp India"}
        })
        buyer_id = buyer_user.user.id
    except Exception as e:
        res = auth_client.auth.sign_in_with_password({"email": buyer_email, "password": password})
        buyer_id = res.user.id

    print("Deleting old profile data for these users...")
    # Delete from transactions, listings, estimates, farmers
    supabase.table("transactions").delete().eq("buyer_id", buyer_id).execute()
    supabase.table("listings").delete().eq("farmer_id", pro_id).execute()
    supabase.table("listings").delete().eq("farmer_id", new_id).execute()
    supabase.table("estimates").delete().eq("farmer_id", pro_id).execute()
    supabase.table("estimates").delete().eq("farmer_id", new_id).execute()
    supabase.table("buyers").delete().eq("id", buyer_id).execute()
    supabase.table("farmers").delete().eq("id", pro_id).execute()
    supabase.table("farmers").delete().eq("id", new_id).execute()

    print("Inserting profiles...")
    # Insert farmers
    supabase.table("farmers").insert({
        "id": pro_id,
        "phone": pro_farmer_phone,
        "full_name": "Ramesh Kumar (Pro)",
        "district_code": "MH_NASHIK",
        "village": "Pimpalgaon",
        "preferred_language": "mr",
        "profile_complete": True
    }).execute()

    supabase.table("farmers").insert({
        "id": new_id,
        "phone": new_farmer_phone,
        "full_name": "Suresh Patel (New)",
        "district_code": "MH_PUNE",
        "village": "Shirur",
        "preferred_language": "hi",
        "profile_complete": True
    }).execute()

    # Insert buyer
    supabase.table("buyers").insert({
        "id": buyer_id,
        "email": buyer_email,
        "org_name": "EcoCorp India",
        "contact_name": "Ananya Sharma"
    }).execute()

    print("Inserting history for Pro Farmer...")
    # Insert 5 old sold listings and 1 live listing for Pro Farmer
    for i in range(5):
        est_id = str(uuid.uuid4())
        co2 = 5.0 + i
        inr = int(co2 * 1500)
        
        # 1. Estimate
        supabase.table("estimates").insert({
            "id": est_id,
            "farmer_id": pro_id,
            "practice_type": "agroforestry" if i % 2 == 0 else "no_till",
            "area_ha": 2.5 + (i * 0.5),
            "season_months": 12,
            "co2e_tonnes": co2,
            "confidence_low": co2 * 0.9,
            "confidence_high": co2 * 1.1,
            "inr_estimate": inr,
            "model_version": "xgb_v1",
            "shap_breakdown": {"base_practice": 2.0, "soil_modifier": 1.0, "rainfall_zone": 1.0, "area_scaling": 1.0},
            "created_at": (datetime.now(timezone.utc) - timedelta(days=(i+1)*30)).isoformat()
        }).execute()
        
        # 2. Listing
        list_id = str(uuid.uuid4())
        supabase.table("listings").insert({
            "id": list_id,
            "estimate_id": est_id,
            "farmer_id": pro_id,
            "asking_price_inr": inr,
            "status": "sold",
            "published_at": (datetime.now(timezone.utc) - timedelta(days=(i+1)*29)).isoformat()
        }).execute()

        # 3. Transaction
        supabase.table("transactions").insert({
            "id": str(uuid.uuid4()),
            "listing_id": list_id,
            "buyer_id": buyer_id,
            "razorpay_payment_id": f"pay_mock_pro_{i}",
            "amount_paid_inr": inr,
            "platform_fee_inr": int(inr * 0.1),
            "farmer_payout_inr": int(inr * 0.9),
            "payout_status": "completed",
            "paid_at": (datetime.now(timezone.utc) - timedelta(days=(i+1)*28)).isoformat()
        }).execute()

    # One live listing
    est_id = str(uuid.uuid4())
    supabase.table("estimates").insert({
        "id": est_id,
        "farmer_id": pro_id,
        "practice_type": "no_till_cover_crop",
        "area_ha": 4.0,
        "season_months": 6,
        "co2e_tonnes": 8.5,
        "confidence_low": 8.0,
        "confidence_high": 9.0,
        "inr_estimate": 17000,
        "model_version": "xgb_v1",
        "shap_breakdown": {"base_practice": 4.0, "soil_modifier": 2.0, "rainfall_zone": 1.5, "area_scaling": 1.0},
    }).execute()
    
    supabase.table("listings").insert({
        "id": str(uuid.uuid4()),
        "estimate_id": est_id,
        "farmer_id": pro_id,
        "asking_price_inr": 17500,
        "status": "live",
        "published_at": datetime.now(timezone.utc).isoformat()
    }).execute()
    
    print("Seed complete!")
    print("\n--- TEST CREDENTIALS ---")
    print("1. PRO FARMER (Long customer with sales history)")
    print("   Phone: 9999999999")
    print("   OTP:   123456")
    print("\n2. NEW FARMER (Just created, no history)")
    print("   Phone: 8888888888")
    print("   OTP:   123456")
    print("--------------------------\n")

if __name__ == "__main__":
    seed_accounts()
