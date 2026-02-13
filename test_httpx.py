import httpx
print(f"HTTPX Version: {httpx.__version__}")
try:
    print("Trying httpx.Client(proxy='http://test')...")
    client = httpx.Client(proxy="http://test")
    print("Success!")
except Exception as e:
    print(f"Failed: {e}")

try:
    print("Trying httpx.Client(proxies='http://test')...")
    client = httpx.Client(proxies="http://test") 
    print("Success! (proxies)")
except Exception as e:
    print(f"Failed (proxies): {e}")
