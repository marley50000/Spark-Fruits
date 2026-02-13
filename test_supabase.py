from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

print(f"URL: {url}")
# Mask Key for privacy
masked_key = key[:10] + "..." + key[-5:] if key else "None"
print(f"Key: {masked_key}")

try:
    print("Creating client...")
    supabase: Client = create_client(url, key)
    print("Client created successfully!")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error: {e}")
