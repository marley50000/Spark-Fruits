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
query = client.table('products')
print(f"Type of query: {type(query)}")
print(f"Dir of query: {dir(query)}")
