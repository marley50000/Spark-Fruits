import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(override=True)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"Testing with Service Key: {bool(service_key)}")
client = create_client(url, service_key if service_key else key)

data = {
    "customer": "Test PayRef",
    "total_price": 0,
    "email": "test@debug.com",
    "payment_ref": "REF_123" 
}

try:
    print("Attempting insert with payment_ref...")
    client.table('orders').insert(data).execute()
    print("SUCCESS! payment_ref column exists.")
except Exception as e:
    print(f"FAILED: {e}")
    if 'payment_ref' in str(e) and 'does not exist' in str(e):
        print(">>> DIAGNOSIS: 'payment_ref' column is MISSING.")
