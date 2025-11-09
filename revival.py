import requests
import time
from datetime import datetime

# 🛰️ Define each server and how often (in minutes) to ping it
SERVERS = [
    {"url": "https://miragestore.onrender.com/ping", "interval": 10, "method": "POST"},
    {"url": "https://gms-1-0.onrender.com/ping", "interval": 5, "method": "POST"},
    {"url": "https://gms-west-server.onrender.com/ping", "interval": 5, "method": "POST"},

    # Add more servers with custom intervals and methods below
    # {"url": "https://example.com", "interval": 3, "method": "POST"},
]

def ping_server(url, method="GET"):
    """Try to ping one server with specified HTTP method."""
    try:
        if method.upper() == "GET":
            r = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            r = requests.post(url, timeout=10)
        elif method.upper() == "HEAD":
            r = requests.head(url, timeout=10)
        elif method.upper() == "PUT":
            r = requests.put(url, timeout=10)
        elif method.upper() == "PATCH":
            r = requests.patch(url, timeout=10)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Unknown method '{method}' for {url}")
            return
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {method} {url} → {r.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {method} {url} failed: {e}")

if __name__ == "__main__":
    print("🚀 Multi-Server Pinger started.")
    print("Each server will ping on its own schedule.\n")

    # Convert minutes to seconds for easier timing
    for s in SERVERS:
        s["next_ping"] = time.time()  # first ping immediately
        s["interval"] *= 60           # convert to seconds
        if "method" not in s:
            s["method"] = "GET"       # default to GET if not specified

    while True:
        now = time.time()
        for s in SERVERS:
            if now >= s["next_ping"]:
                ping_server(s["url"], s["method"])
                s["next_ping"] = now + s["interval"]
        time.sleep(5)  # check every few seconds