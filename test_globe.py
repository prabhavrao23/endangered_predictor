import requests
import json

print("="*60)
print("TESTING GLOBAL RISK PREDICTOR")
print("="*60)

# Test 1: Global prediction
print("\n1. Testing Global Prediction API...")
try:
    response = requests.post(
        "http://localhost:8000/predict/global",
        params={
            "temperature": 2.0,
            "sea_level": 1.0,
            "deforestation": 30,
            "pollution": 40,
            "fishing": 20,
            "habitat_loss": 35
        }
    )
    data = response.json()
    print(f"   [OK] Status: {response.status_code}")
    print(f"   Total Species Analyzed: {data['global_stats']['total_species']}")
    print(f"   Average Risk: {data['global_stats']['avg_predicted_risk']}/100")
    print(f"   Critical Species: {data['global_stats']['critical_species']}")
    print(f"   Risk Trend: {data['global_stats']['risk_trend']}")
    print(f"\n   Top 3 Most Threatened:")
    for i, species in enumerate(data['species'][:3], 1):
        print(f"     {i}. {species['name']}: {species['predicted_risk']}/100 (↑{species['risk_increase']})")
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 2: Top threatened species
print("\n2. Testing Top Threatened Species API...")
try:
    response = requests.get("http://localhost:8000/species/top-threatened?limit=5")
    data = response.json()
    print(f"   [OK] Status: {response.status_code}")
    print(f"   Count: {data['count']}")
    for i, species in enumerate(data['species'][:5], 1):
        print(f"     {i}. {species['name']} ({species['region']}): {species['baseline_risk']}/100 - {species['status']}")
except Exception as e:
    print(f"   [FAIL] {e}")

# Test 3: Regional breakdown
print("\n3. Testing Regional Breakdown API...")
try:
    response = requests.get("http://localhost:8000/regions/breakdown")
    data = response.json()
    print(f"   [OK] Status: {response.status_code}")
    print(f"   Regions: {data['count']}")
    for region, stats in list(data['regions'].items())[:5]:
        print(f"     {region}: {stats['species_count']} species, avg risk {stats['avg_risk']}/100")
except Exception as e:
    print(f"   [FAIL] {e}")

print("\n" + "="*60)
print("ALL TESTS COMPLETE!")
print("="*60)
print("\nNow open global_risk_dashboard.html in your browser!")
print("The interactive globe is connected to the live API.")

