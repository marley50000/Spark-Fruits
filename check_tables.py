import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(url, key)
    # Check if 'products' exists
    try:
        supabase.table('products').select("count", count='exact').limit(1).execute()
        print("Table 'products' exists.")
    except Exception as e:
        print(f"Table 'products' error: {e}")

    # Check if 'users' or 'profiles' exists (common trigger targets)
    try:
        supabase.table('users').select("count", count='exact').limit(1).execute()
        print("Table 'users' exists.")
    except Exception as e:
        print(f"Table 'users' likely does not exist or permissions are denied: {e}")

    try:
        supabase.table('profiles').select("count", count='exact').limit(1).execute()
        print("Table 'profiles' exists.")
    except Exception as e:
        print(f"Table 'profiles' likely does not exist or permissions are denied: {e}")

except Exception as e:
    print(f"Connection failed: {e}")
