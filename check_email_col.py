import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Missing env vars")
    exit()

try:
    supabase: Client = create_client(url, key)
    # Try to select email column
    try:
        supabase.table('orders').select("email").limit(1).execute()
        print("Column 'email' exists.")
    except Exception as e:
        print(f"Column 'email' seemingly missing or error: {e}")

except Exception as e:
    print(f"Connection failed: {e}")
