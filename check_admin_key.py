import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(override=True)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"Service Key Length: {len(key) if key else 'None'}")

if not key:
    print("FATAL: No SUPABASE_SERVICE_ROLE_KEY found in .env")
    exit(1)

try:
    print("Attempting to connect with Service Role Key...")
    # Service Role client should verify simply by creation or simple request
    admin_client = create_client(url, key)
    
    # Try an admin operation: List users (requires admin rights usually)
    # The python client might exposes 'auth.admin'
    print("Client created. Attempting admin fetch...")
    
    # Try to select from a table, ignoring RLS
    # If we are admin, RLS is bypassed. If not, meaningful RLS would block us (but we can't easily test RLS bypass without a blocking policy).
    # Instead, let's just check if we can select from 'riders' or 'users'
    
    # Just check if we can query 'riders' without error
    res = admin_client.table('riders').select('*').limit(1).execute()
    print(f"Admin Table Query Success: {len(res.data) if res.data else 0} rows found.")
    
    print(">>> SERVICE ROLE KEY SEEMS VALID.")
    
except Exception as e:
    print(f"\n>>> SERVICE ROLE KEY FAILED: {e}")
    print("This means the app is falling back to the public 'anon' key, which is blocked by RLS.")
