"""
Temporary test script — debug 2ADP099 Rollup 1099 401 error.

Hypothesis: _fetch_mv_by_identifier() in v16 does NOT send OAuth headers.
Single-identifier sequences use _fetch_netamount() which does send auth.
Multi-identifier sequences (like 2ADP099) use the MV path — no auth → 401.

This script tests:
  1. MV endpoint for 2ADP099 WITHOUT auth header  → expect 401
  2. MV endpoint for 2ADP099 WITH auth header     → expect data
  3. netamount endpoint for 2ADP099 WITH auth     → expect data (single-id style)
"""

import base64
import json
import os
import urllib.parse
import urllib.request

BASE_URL = "https://g22673cc0c08b7a-oax2132513753.adb.us-ashburn-1.oraclecloudapps.com/ords/oax_user"
MV_URL = f"{BASE_URL}/mv_femr_report/"
NETAMOUNT_URL = f"{BASE_URL}/femr/netamount/"
TOKEN_URL = f"{BASE_URL}/oauth/token"

SEQUENCE = "2ADP099"
FYE = "2026-09-30"
QUARTER = "Q4"
SEGMENT = "CONTRACTING"
ACCOUNT = "Committed"


def get_token():
    client_id = os.environ.get("ORACLE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("ORACLE_SECRET_KEY", "").strip()
    if not client_id or not client_secret:
        raise RuntimeError("ORACLE_CLIENT_ID and ORACLE_SECRET_KEY must be set in environment.")
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, headers={
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    token = data["access_token"]
    print(f"Token fetched OK — valid for {data.get('expires_in', '?')}s\n")
    return token


def mv_url():
    q = json.dumps({
        "display_sequence": SEQUENCE,
        "fiscal_year_end":  FYE,
        "fiscal_quarter":   QUARTER,
        "segment":          SEGMENT,
        "account_name":     ACCOUNT,
    })
    return f"{MV_URL}?q={urllib.parse.quote(q)}&limit=10"


def test(label, url, headers=None):
    print(f"--- {label} ---")
    print(f"URL: {url[:120]}...")
    try:
        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        items = data.get("items", [])
        print(f"STATUS: 200 OK — {len(items)} items returned")
        if items:
            print(f"First item keys: {list(items[0].keys())}")
            print(f"Sample netamount: {items[0].get('netamount')}")
            rollups = set(i.get('display_rollup_num') for i in items)
            print(f"Rollup nums in response: {rollups}")
    except urllib.error.HTTPError as e:
        print(f"STATUS: HTTP {e.code} {e.reason}")
    except Exception as e:
        print(f"ERROR: {e}")
    print()


if __name__ == "__main__":
    token = get_token()
    auth_header = {"Authorization": f"Bearer {token}"}

    # Test 1 — MV without auth (mirrors current v16 _fetch_mv_by_identifier behaviour)
    test("TEST 1: MV endpoint — NO auth header (current v16 behaviour for multi-id)",
         mv_url(), headers={})

    # Test 2 — MV with auth header (proposed fix)
    test("TEST 2: MV endpoint — WITH auth header",
         mv_url(), headers=auth_header)

    # Test 3 — netamount with auth (single-id path for comparison)
    params = {
        "display_sequence": SEQUENCE,
        "fiscal_year_end":  FYE,
        "fiscal_quarter":   QUARTER,
        "segment":          SEGMENT,
        "account_name":     ACCOUNT,
    }
    na_url = f"{NETAMOUNT_URL}?{urllib.parse.urlencode(params)}"
    test("TEST 3: netamount endpoint — WITH auth (single-id path)",
         na_url, headers=auth_header)
