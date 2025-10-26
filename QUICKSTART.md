# 🚀 Quick Start Guide

**Get the Animal Endangerment Predictor running in 5 minutes!**

---

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI (API framework)
- Requests (HTTP client)
- NumPy/Pandas (data processing)
- Python-dotenv (environment variables)

---

## Step 2: Get API Keys (Optional)

**Most features work without any keys!** But for complete data:

### IUCN Red List Token (Free)
Get species conservation status:

1. Visit: https://apiv3.iucnredlist.org/api/v3/token
2. Request a token (instant approval)
3. Add to `.env`: `IUCN_TOKEN=your_token_here`

### NASA FIRMS Key (Free)
Get fire detection data:

1. Visit: https://firms.modaps.eosdis.nasa.gov/api/
2. Sign up for API key
3. Add to `.env`: `FIRMS_KEY=your_key_here`

**Note:** GBIF, Global Forest Watch, World Bank, Open-Meteo, OpenAQ, and OpenStreetMap require **no authentication**!

---

## Step 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env and add your tokens
nano .env
```

Or just create `.env` manually:

```bash
IUCN_TOKEN=your_token_here
FIRMS_KEY=your_key_here
API_PORT=8000
```

---

## Step 4: Start the API

```bash
python run_api.py
```

You should see:

```
🌍 Animal Endangerment Predictor API
📡 Starting API server on http://0.0.0.0:8000
📚 API Documentation: http://0.0.0.0:8000/docs
```

---

## Step 5: Test with Example Queries

### Option A: Use cURL

```bash
curl -X POST "http://localhost:8000/risk" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the tiger risk in India?"}'
```

### Option B: Use the Interactive UI

Open in your browser:
- http://localhost:8000/docs

Click "Try it out" on any endpoint!

### Option C: Run Example Script

```bash
python examples/example_usage.py
```

This runs 8 different example queries and generates output files.

---

## Example Queries

Try these natural language queries:

```python
"What is the tiger risk in India?"

"Show snow leopard risk in Nepal by 2035 if deforestation rises 10%"

"Is the African elephant endangered in Kenya?"

"Hawksbill turtle risk in the Caribbean if ocean heat increases 15%"

"Compare panda risk with and without habitat protection"

"What happens to orangutan populations if logging increases 20%?"

"Assess polar bear risk in the Arctic with 2°C warming"
```

---

## Understanding the Response

```json
{
  "risk_score": 73.2,           // 0-100 endangerment risk
  "confidence": "medium",        // low/medium/high
  "contributions": {
    "habitat": 34.9,             // % contribution from each driver
    "climate": 24.0,
    "exploitation": 8.7,
    "pollution": 3.8,
    "invasives": 1.2,
    "governance": 0.6
  },
  "explanation": "The species faces high endangerment risk...",
  "sources": [                   // All data sources used
    "GBIF occurrences",
    "Global Forest Watch",
    "World Bank Governance",
    ...
  ]
}
```

---

## Troubleshooting

### "Cannot connect to API"
Make sure the server is running: `python run_api.py`

### "IUCN_TOKEN not set"
This is just a warning. Most features work without it. Add the token to `.env` for species status data.

### "No temperature data"
Some regions may have limited climate data. The system will use other available drivers.

### "Species not found"
Try the scientific name instead of common name. Search first: `GET /species?query=panda`

### Port already in use
Change the port in `.env`: `API_PORT=8001`

---

## Next Steps

1. **Read the full docs:** See `README_RISK_PREDICTOR.md`
2. **Explore examples:** Check `examples/example_usage.py`
3. **Customize:** Adjust weights in `src/api/risk_scoring.py`
4. **Visualize:** Generate maps with `/ui/mapbox` endpoint
5. **Integrate:** Use the API in your own applications

---

## Common Use Cases

### 1. Single Species Assessment

```python
import requests

response = requests.post("http://localhost:8000/risk", json={
    "query": "tiger risk in India"
})

print(response.json()["risk_score"])
```

### 2. Scenario Analysis

```python
baseline = requests.post("http://localhost:8000/risk", json={
    "query": "elephant risk in Kenya"
}).json()

scenario = requests.post("http://localhost:8000/risk", json={
    "query": "elephant risk in Kenya if poaching decreases 50%"
}).json()

delta = scenario["risk_score"] - baseline["risk_score"]
print(f"Risk change: {delta:+.1f} points")
```

### 3. Multi-Region Comparison

```python
regions = ["India", "Nepal", "Bhutan"]

for region in regions:
    result = requests.post("http://localhost:8000/risk", json={
        "query": f"snow leopard risk in {region}"
    }).json()
    
    print(f"{region}: {result['risk_score']:.1f}/100")
```

### 4. Generate Report

```python
import json

result = requests.post("http://localhost:8000/risk", json={
    "query": "orangutan risk in Borneo"
}).json()

# Save complete assessment
with open("orangutan_report.json", "w") as f:
    json.dump(result, f, indent=2)

# Generate map
map_code = requests.post("http://localhost:8000/ui/mapbox", json={
    "query": "orangutan risk in Borneo"
}).json()["code"]

with open("orangutan_map.html", "w") as f:
    f.write(map_code)
```

---

## Help & Support

- 📖 Full documentation: `README_RISK_PREDICTOR.md`
- 🐛 Issues: Open on GitHub
- 💬 Questions: See examples or API docs

---

**You're ready to start predicting endangerment risk!** 🎉

