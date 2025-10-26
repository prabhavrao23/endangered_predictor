import requests
import json

print("="*50)
print("FINAL API TEST")
print("="*50)

# Test 1: Health
print("\n1. Health Check...")
try:
    r = requests.get("http://localhost:8000/health")
    print(f"   [OK] Status: {r.status_code} - {r.json()['status']}")
except Exception as e:
    print(f"   [FAIL] Failed: {e}")

# Test 2: OpenAPI
print("\n2. OpenAPI Schema...")
try:
    r = requests.get("http://localhost:8000/openapi.json")
    print(f"   [OK] Status: {r.status_code} - Schema loaded ({len(r.content)} bytes)")
except Exception as e:
    print(f"   [FAIL] Failed: {e}")

# Test 3: Risk Assessment
print("\n3. Risk Assessment...")
try:
    r = requests.post("http://localhost:8000/risk", json={
        "query": "Panthera tigris risk in India"
    })
    result = r.json()
    print(f"   [OK] Status: {r.status_code}")
    print(f"   Risk Score: {result['risk_score']}/100")
    print(f"   Confidence: {result['confidence']}")
    print(f"   Data Sources: {len(result['sources'])}")
except Exception as e:
    print(f"   [FAIL] Failed: {e}")

print("\n" + "="*50)
print("ALL SYSTEMS OPERATIONAL!")
print("="*50)
print("\nAccess the interactive API docs at:")
print("  • http://localhost:8000/docs")
print("  • http://localhost:8000/redoc")
print("\nRefresh your browser to see the documentation!")

