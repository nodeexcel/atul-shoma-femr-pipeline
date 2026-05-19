"""
Temporary discovery script — find exact Oracle API account_name strings
for GL codes 5007, 5098, 5099.

Queries the MV endpoint for 2ADP001 (known to have 5007 and 5099 data)
and lists ALL unique account_name values returned, so we can confirm
the exact strings to use in ACTUALS_BUDGET_ACCOUNTS.
"""

import base64
import json
import os
import urllib.parse
import urllib.request
from collections import defaultdict

BASE_URL = "https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user"
MV_URL   = f"{BASE_URL}/mv_femr_report/"
TOKEN_URL = f"{BASE_URL}/oauth/token"

SEQUENCE = "2ADP001"


def get_token():
    client_id     = os.environ.get("ORACLE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("ORACLE_SECRET_KEY", "").strip()
    if not client_id or not client_secret:
        raise RuntimeError("ORACLE_CLIENT_ID and ORACLE_SECRET_KEY must be set.")
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req  = urllib.request.Request(TOKEN_URL, data=body, headers={
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    print(f"Token OK — valid {data.get('expires_in')}s\n")
    return data["access_token"]


def fetch_page(token, q_filter, offset=0, limit=500, retries=5):
    url = f"{MV_URL}?q={urllib.parse.quote(json.dumps(q_filter))}&limit={limit}&offset={offset}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt == retries - 1:
                raise
            wait = 3 * (attempt + 1)
            print(f"  Retrying (attempt {attempt+2}/{retries}) after {wait}s — {e}")
            import time; time.sleep(wait)


def main():
    token = get_token()

    # Fetch all rows for 2ADP001 across all segments (paginate)
    q = {"display_sequence": SEQUENCE}
    all_items = []
    offset = 0
    while True:
        data  = fetch_page(token, q, offset=offset, limit=500)
        items = data.get("items", [])
        all_items.extend(items)
        print(f"  Fetched {len(all_items)} rows so far...")
        if len(items) < 500:
            break
        offset += 500

    print(f"\nTotal rows for {SEQUENCE}: {len(all_items)}")

    # Collect unique (segment, account_name) pairs with sample amounts
    accounts = defaultdict(lambda: defaultdict(float))
    for item in all_items:
        seg  = item.get("segment", "")
        acc  = item.get("account_name", "")
        amt  = item.get("netamount") or 0.0
        accounts[seg][acc] += float(amt)

    print("\n=== All unique account_name values by segment ===\n")
    for seg in sorted(accounts):
        print(f"SEGMENT: {seg}")
        for acc in sorted(accounts[seg]):
            total = accounts[seg][acc]
            # Flag GL codes we're looking for
            flag = ""
            if any(code in str(acc) for code in ["5007", "5098", "5099"]):
                flag = "  ← TARGET"
            print(f"  {acc:<45} total={total:>15,.2f}{flag}")
        print()

    # Summary of target accounts
    print("=== TARGET GL CODE SUMMARY ===")
    targets = ["5007", "5098", "5099"]
    for seg in sorted(accounts):
        for acc in sorted(accounts[seg]):
            if any(t in str(acc) for t in targets):
                print(f"  Segment={seg:12s}  account_name={acc!r}  total={accounts[seg][acc]:,.2f}")


if __name__ == "__main__":
    main()
