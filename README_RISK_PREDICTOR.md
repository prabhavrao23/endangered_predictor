# Animal Endangerment Predictor & Globe

**Real-time species risk assessment using public APIs**

Predict and visualize endangerment risk for any animal species using real data from IUCN, GBIF, Global Forest Watch, NASA, World Bank, and other public sources. 

---

## 🎯 Mission

Predict a **composite risk score** (0-100) for any species in any location, combining:

- **Habitat loss** (forest loss, roads, fragmentation)
- **Climate exposure** (temperature anomalies, ocean heat stress)
- **Exploitation pressure** (population density, fishing effort)
- **Pollution** (air quality PM2.5)
- **Invasive species** (GRIIS records)
- **Governance risk** (World Bank indicators)
- **Species sensitivity** (IUCN status, traits)
- **Adaptive capacity** (range, mobility, protected areas)

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repo-url>
cd endangered_predictor

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` and add your API keys:

```bash
IUCN_TOKEN=your_token_here       # Get at: https://apiv3.iucnredlist.org/api/v3/token
FIRMS_KEY=your_key_here          # Get at: https://firms.modaps.eosdis.nasa.gov/api/
```

**Note:** Many APIs (GBIF, Global Forest Watch, World Bank, Open-Meteo, OpenAQ, OSM) require **no authentication**.

### 3. Run the API

```bash
cd src/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit:
- **API docs:** http://localhost:8000/docs
- **Interactive UI:** http://localhost:8000

---

## 📡 API Endpoints

### POST `/risk` - Natural Language Risk Assessment

Ask questions in plain English:

```bash
curl -X POST "http://localhost:8000/risk" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the snow leopard risk in Nepal by 2035 if deforestation rises 10% and warming increases by 1.5°C?",
    "iucn_token": "your_token"
  }'
```

**Example queries:**
- "Show hawksbill turtle risk in the Caribbean in 2040 if ocean heat stress increases 15%"
- "Is the Sunda pangolin likely to face higher risk in Malaysia?"
- "Assess African elephant endangerment in Kenya"

**Response:**

```json
{
  "query": {
    "species_scientific": "Panthera uncia",
    "species_gbif_key": 5219404,
    "region": {"type": "country", "iso3": "NPL"},
    "horizon": 2035,
    "scenario": {
      "deforestation_pct": 0.10,
      "warming_c": 1.5
    }
  },
  "features": {
    "habitat_loss_recent_pct": 8.2,
    "road_density_km_per_km2": 0.4,
    "temp_anomaly_c": 1.1,
    "pm25_ugm3": 42.3,
    "invasive_count": 3,
    "rule_of_law": -0.65,
    "control_corruption": -0.71,
    "protected_area_pct": 23.4,
    "population_density": 203.5
  },
  "normalized": {
    "H": 0.35,
    "C": 0.37,
    "X": 0.41,
    "P": 0.56,
    "I": 0.06,
    "G": 0.68,
    "S": 0.85,
    "AC": 0.42
  },
  "risk_score": 72.4,
  "contributions": {
    "habitat": 24.1,
    "climate": 25.5,
    "exploitation": 14.2,
    "pollution": 20.4,
    "invasives": 2.1,
    "governance": 13.7
  },
  "confidence": "medium",
  "sources": [
    "GBIF species match API",
    "IUCN Red List API",
    "GBIF occurrences",
    "Global Forest Watch umd_tree_cover_loss",
    "OpenStreetMap Overpass API",
    "Open-Meteo ERA5 archive",
    "OpenAQ air quality API",
    "World Bank Governance Indicators (RL.EST)",
    "World Bank Governance Indicators (CC.EST)",
    "World Bank Protected Areas",
    "World Bank Population Density"
  ],
  "explanation": "The species faces high endangerment risk with a score of 72.4/100. The primary drivers are climate exposure (25.5% contribution) and habitat loss (24.1% contribution). Under the specified scenario, risk increases by 8.2 points from baseline. This assessment is based on available public data and should be interpreted alongside local expert knowledge and on-ground monitoring.",
  "timestamp": "2025-10-26T15:32:18.123456"
}
```

### GET `/species?query={name}` - Search Species

```bash
curl "http://localhost:8000/species?query=tiger"
```

Returns GBIF taxonomy match with scientific name, GBIF key, and classification.

### GET `/regions?query={name}` - Search Regions

```bash
curl "http://localhost:8000/regions?query=himalayas"
```

Returns ISO3 codes or bounding boxes for countries and regions.

### GET `/layers` - Map Layer Metadata

```bash
curl "http://localhost:8000/layers"
```

Returns available map layers (forest loss, protected areas, fires, roads, etc.) with tile URLs and attributions.

### POST `/ui/mapbox` - Generate Visualization Code

```bash
curl -X POST "http://localhost:8000/ui/mapbox" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show tiger risk in India"
  }'
```

Returns complete HTML/JavaScript code for interactive Mapbox GL map.

---

## 🧮 Risk Model

### Composite Score Formula

```
Base = wH×H + wC×C + wX×X + wP×P + wI×I + wG×G
Mod  = α×S + β×(1 - AC)
Risk = 100 × clamp(Base × (1 + Mod), 0, 1)
```

**Default Weights:**
- `wH = 0.25` (Habitat loss)
- `wC = 0.25` (Climate exposure)
- `wX = 0.20` (Exploitation)
- `wP = 0.10` (Pollution)
- `wI = 0.10` (Invasive species)
- `wG = 0.10` (Governance risk)
- `α = 0.30` (Species sensitivity)
- `β = 0.20` (Adaptive capacity)

### Feature Normalization

All features normalized to [0, 1]:

| Feature | Range | Source |
|---------|-------|--------|
| Forest loss | 0-30% over 10 years | Global Forest Watch |
| Road density | 0-3 km/km² | OpenStreetMap |
| Temp anomaly | 0-3°C above baseline | Open-Meteo ERA5 |
| DHW (marine) | 0-12 weeks | NOAA Coral Reef Watch |
| PM2.5 | 0-75 μg/m³ | OpenAQ |
| Invasive count | Scaled by max observed | GRIIS/GBIF |
| Governance | World Bank -2.5 to 2.5 | World Bank WGI |

### Scenario Adjustments

Apply "what-if" scenarios by adjusting drivers:

- **Deforestation:** `+10%` increases habitat loss
- **Warming:** `+1.5°C` increases climate exposure
- **Fishing:** `+20%` increases exploitation
- **Pollution:** `+15%` increases pollution
- **Governance:** `+0.1` improves governance (reduces risk)

---

## 🗺️ Data Sources

All sources are **public** and **free** (some require free registration):

| Source | Data Type | Token Required | URL |
|--------|-----------|----------------|-----|
| IUCN Red List | Species status, threats | ✅ Yes | https://apiv3.iucnredlist.org |
| GBIF | Species occurrences | ❌ No | https://api.gbif.org |
| Global Forest Watch | Forest loss | ❌ No | https://data-api.globalforestwatch.org |
| NASA FIRMS | Active fires | ✅ Yes | https://firms.modaps.eosdis.nasa.gov |
| OpenStreetMap | Roads, infrastructure | ❌ No | https://overpass-api.de |
| Open-Meteo | Climate data | ❌ No | https://archive-api.open-meteo.com |
| NOAA Coral Reef Watch | Ocean heat stress | ❌ No | https://coastwatch.pfeg.noaa.gov |
| World Bank | Governance, protected areas | ❌ No | http://api.worldbank.org |
| OpenAQ | Air quality | ❌ No | https://api.openaq.org |
| GRIIS | Invasive species | ❌ No | Via GBIF dataset search |

---

## 🎨 Visualization

### Mapbox GL Integration

The API generates ready-to-use Mapbox GL code:

```javascript
// Generated code includes:
- Interactive map centered on species range
- Risk score display with color coding
- Layer toggles (forest loss, fires, roads, etc.)
- Bounding box overlay
- Navigation controls
```

### Available Layers

- Forest loss (Global Forest Watch)
- Protected areas (WDPA)
- Active fires (NASA FIRMS)
- Road network (OpenStreetMap)
- Population density (WorldPop)
- Night lights (NOAA VIIRS)
- Coral heat stress (NOAA CRW)

---

## 🧪 Example Use Cases

### Example 1: Hawksbill Turtle in Caribbean

```python
import requests

response = requests.post("http://localhost:8000/risk", json={
    "query": "Show hawksbill turtle risk in the Caribbean in 2040 if ocean heat stress increases 15%"
})

result = response.json()
print(f"Risk Score: {result['risk_score']}/100")
print(f"Top Driver: {max(result['contributions'].items(), key=lambda x: x[1])}")
```

### Example 2: Snow Leopard Scenario Analysis

```python
# Baseline
baseline = requests.post("http://localhost:8000/risk", json={
    "query": "Snow leopard risk in Nepal"
}).json()

# Scenario with improved governance
scenario = requests.post("http://localhost:8000/risk", json={
    "query": "Snow leopard risk in Nepal if governance improves by 20%"
}).json()

delta = scenario['risk_score'] - baseline['risk_score']
print(f"Risk change: {delta:+.1f} points")
```

---

## 🔧 Architecture

```
src/api/
├── main.py                 # FastAPI endpoints
├── orchestrator.py         # Main assessment pipeline
├── data_fetchers.py        # API clients for all data sources
├── normalization.py        # Feature engineering and normalization
├── risk_scoring.py         # Composite risk model
├── nlp_parser.py           # Natural language query parser
└── ui_helpers.py           # Mapbox GL code generation
```

---

## 📊 Confidence Levels

The system assigns confidence based on:

- **High:** All 6+ drivers available, data < 1 year old, 5+ sources
- **Medium:** 4-5 drivers available, 3-4 sources
- **Low:** < 4 drivers available, or data > 2 years old

---

## ⚠️ Limitations & Caveats

1. **Not conservation advice** - This is a data-driven model, not a substitute for expert assessment
2. **Data freshness** - Some APIs have lag times (World Bank updates annually)
3. **Missing drivers** - If data is unavailable, confidence decreases
4. **Spatial resolution** - Country-level aggregates may miss local variations
5. **API rate limits** - Some APIs have request limits (caching mitigates this)

---

## 🛠️ Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
black src/
flake8 src/
```

### Adding New Data Sources

1. Add fetcher function to `data_fetchers.py`
2. Add normalization logic to `normalization.py`
3. Update orchestrator to fetch and incorporate new feature
4. Update weights in `risk_scoring.py` if needed

---

## 📜 License

MIT License - See LICENSE file

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional data sources (fishing effort, genetic diversity, etc.)
- Species-specific weight tuning
- UI/dashboard improvements
- Validation against expert assessments
- Performance optimization

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

## 🙏 Acknowledgments

Data sources:
- IUCN Red List Partnership
- Global Biodiversity Information Facility (GBIF)
- Global Forest Watch / World Resources Institute
- NASA FIRMS / LANCE
- OpenStreetMap Contributors
- Open-Meteo / ECMWF
- NOAA Coral Reef Watch
- World Bank Group
- OpenAQ Community
- GRIIS / ISSG

---

**Built with ❤️ for conservation and biodiversity monitoring**

