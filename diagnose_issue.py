import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(override=True)

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"Anon Key present: {bool(key)}")
print(f"Service Key present: {bool(service_key)}")
if service_key:
    print(f"Service Key length: {len(service_key)}")
    print(f"Service Key start: {service_key[:10]}...")

def test_insert(client_name, client_obj):
    print(f"\n--- Testing Insert with {client_name} ---")
    if not client_obj:
        print("Client is None")
        return

    data = {
        "customer": f"Test {client_name}",
        "total_price": 0,
        "email": "test@debug.com"
    }
    
    try:
        # First check if email column exists by trying current schema
        # We'll just try the insert
        client_obj.table('orders').insert(data).execute()
        print("SUCCESS! Insert worked.")
    except Exception as e:
        print(f"FAILED: {e}")
        # explicit check for column error
        err_str = str(e)
        if 'column "email" of relation "orders" does not exist' in err_str or 'orders.email does not exist' in err_str:
            print(">>> DIAGNOSIS: The 'email' column is MISSING from the 'orders' table. You must run the add_email_column.sql script.")
        elif 'violates row-level security' in err_str:
             print(">>> DIAGNOSIS: RLS Policy blocked this. If this is the Admin/Service Key, the key might be invalid or not a service key.")

# 1. Test Anon Client
try:
    anon = create_client(url, key)
    test_insert("Anon Client", anon)
except Exception as e:
    print(f"Anon init failed: {e}")

# 2. Test Admin Client
if service_key:
    try:
        admin = create_client(url, service_key)
        test_insert("Start Service Role Client", admin)
    except Exception as e:
         print(f"Admin init failed: {e}")
else:
    print("\nSkipping Admin Test (No Key)")
