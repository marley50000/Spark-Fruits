import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("No creds")
    exit()

client = create_client(url, key)

# Try to insert a dummy order with email
data = {
    "customer": "Test User",
    "total_price": 0,
    "email": "test@test.com"
}

try:
    print("Attempting to insert with email...")
    client.table('orders').insert(data).execute()
    print("Insert successful!")
except Exception as e:
    print("\n--- ERROR DURING INSERT ---")
    print(e)
    print("---------------------------\n")

    # Try without email
    del data['email']
    try:
        print("Attempting to insert WITHOUT email...")
        client.table('orders').insert(data).execute()
        print("Insert without email successful!")
    except Exception as e2:
        print(f"Even without email it failed: {e2}")
