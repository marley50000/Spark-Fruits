import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(override=True)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

client = create_client(url, service_key if service_key else key)

print("Checking 'riders' table...")
try:
    # Try select count
    client.table('riders').select('*', count='exact').limit(1).execute()
    print("SUCCESS: 'riders' table exists.")
except Exception as e:
    print(f"ERROR: 'riders' table likely missing. {e}")
    if 'does not exist' in str(e):
        print(">>> ACTION: You MUST run 'setup_rider_system.sql' in Supabase SQL Editor.")

print("\nChecking 'orders' table for 'rider_id' column...")
try:
    client.table('orders').select('rider_id').limit(1).execute()
    print("SUCCESS: 'rider_id' column exists.")
except Exception as e:
    print(f"ERROR: 'rider_id' column likely missing. {e}")
    if 'does not exist' in str(e):
        print(">>> ACTION: You MUST run 'setup_rider_system.sql' in Supabase SQL Editor.")
