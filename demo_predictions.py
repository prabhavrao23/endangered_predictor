"""
Live demo of ML predictions - shows what happens when you change scenarios
"""
import requests
import time

API = "http://localhost:8000"

print("\n" + "="*70)
print("  LIVE ML PREDICTION DEMO")
print("="*70)

print("\nBaseline (Current conditions):")
print("-" * 70)
baseline = requests.post(f"{API}/predict/global", params={
    "temperature": 0, "sea_level": 0, "deforestation": 0,
    "pollution": 0, "fishing": 0, "habitat_loss": 0
}).json()

print(f"Average Global Risk: {baseline['global_stats']['avg_baseline_risk']}/100")
print(f"Critical Species: {baseline['global_stats']['critical_species']}")
print(f"Total Species: {baseline['global_stats']['total_species']}")

print("\n\nSCENARIO 1: Moderate Climate Change (+2C)")
print("-" * 70)
scenario1 = requests.post(f"{API}/predict/global", params={
    "temperature": 2.0, "sea_level": 0.5, "deforestation": 15,
    "pollution": 20, "fishing": 10, "habitat_loss": 15
}).json()

print(f"New Average Risk: {scenario1['global_stats']['avg_predicted_risk']}/100")
print(f"Risk Increase: +{scenario1['global_stats']['avg_risk_increase']}")
print(f"Critical Species: {scenario1['global_stats']['critical_species']}")

print("\nMost Affected Species:")
for i, sp in enumerate(scenario1['species'][:5], 1):
    print(f"  {i}. {sp['name']}: {sp['baseline_risk']} -> {sp['predicted_risk']} (+{sp['risk_increase']})")

print("\n\nSCENARIO 2: Severe Crisis (+4C, +50% deforestation)")
print("-" * 70)
scenario2 = requests.post(f"{API}/predict/global", params={
    "temperature": 4.0, "sea_level": 1.5, "deforestation": 50,
    "pollution": 60, "fishing": 40, "habitat_loss": 45
}).json()

print(f"New Average Risk: {scenario2['global_stats']['avg_predicted_risk']}/100")
print(f"Risk Increase: +{scenario2['global_stats']['avg_risk_increase']}")
print(f"Critical Species: {scenario2['global_stats']['critical_species']}")

print("\nMost Affected Species:")
for i, sp in enumerate(scenario2['species'][:5], 1):
    print(f"  {i}. {sp['name']}: {sp['baseline_risk']} -> {sp['predicted_risk']} (+{sp['risk_increase']})")

print("\n\nSCENARIO 3: Conservation Success (+0.5C, +5% deforestation)")
print("-" * 70)
scenario3 = requests.post(f"{API}/predict/global", params={
    "temperature": 0.5, "sea_level": 0.2, "deforestation": 5,
    "pollution": 5, "fishing": 3, "habitat_loss": 5
}).json()

print(f"New Average Risk: {scenario3['global_stats']['avg_predicted_risk']}/100")
print(f"Risk Increase: +{scenario3['global_stats']['avg_risk_increase']}")
print(f"Critical Species: {scenario3['global_stats']['critical_species']}")

print("\n\n" + "="*70)
print("  COMPARISON SUMMARY")
print("="*70)
print(f"\nBaseline:            {baseline['global_stats']['avg_baseline_risk']}/100 ({baseline['global_stats']['critical_species']} critical)")
print(f"Moderate Change:     {scenario1['global_stats']['avg_predicted_risk']}/100 ({scenario1['global_stats']['critical_species']} critical) [+{scenario1['global_stats']['avg_risk_increase']}]")
print(f"Severe Crisis:       {scenario2['global_stats']['avg_predicted_risk']}/100 ({scenario2['global_stats']['critical_species']} critical) [+{scenario2['global_stats']['avg_risk_increase']}]")
print(f"Conservation:        {scenario3['global_stats']['avg_predicted_risk']}/100 ({scenario3['global_stats']['critical_species']} critical) [+{scenario3['global_stats']['avg_risk_increase']}]")

print("\n" + "="*70)
print("  ✓ ML MODEL IS WORKING!")
print("  ✓ Now use the interactive globe dashboard to explore!")
print("="*70 + "\n")

