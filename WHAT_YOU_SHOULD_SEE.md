# 🌍 What You Should See in the Globe Dashboard

## Browser Window Layout

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🌍 Global Animal Endangerment Predictor                     ┃
┃  ML-powered predictions showing how environmental...         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                              ┃
┃                                                   ┏━━━━━━━━━━┓
┃         🗺️ WORLD MAP                              ┃ Global   ┃
┃                                                   ┃ Stats    ┃
┃    🔴 ← Endangered species markers                ┃ 71 | 8   ┃
┃    🟠    (colored dots on map)                    ┃ 15 | +12%┃
┃    🟡                                             ┣━━━━━━━━━━┫
┃                                                   ┃ Sliders: ┃
┃    Click dots to see species info!                ┃          ┃
┃                                                   ┃ 🌡️ +1.0°C┃
┃    Zoom/Pan with mouse                            ┃ [====o===]┃
┃                                                   ┃          ┃
┃                                                   ┃ 🌊 +0.5m ┃
┃                                                   ┃ [==o=====]┃
┃                                                   ┃          ┃
┃                                                   ┃ 🌳 +15%  ┃
┃                                                   ┃ [===o====]┃
┃                                                   ┃          ┃
┃  📊 Prediction info here                          ┃ 💨 +20%  ┃
┃  (bottom left box)                                ┃ [====o===]┃
┃                                                   ┃          ┃
┃                                                   ┃ 🎣 +10%  ┃
┃                                                   ┃ [==o=====]┃
┃                                                   ┃          ┃
┃                                                   ┃ 🏭 +25%  ┃
┃                                                   ┃ [=====o==]┃
┃                                                   ┃          ┃
┃                                                   ┃ [PREDICT]┃
┃                                                   ┃ [ RESET ]┃
┃                                                   ┣━━━━━━━━━━┫
┃                                                   ┃ Species: ┃
┃                                                   ┃ Vaquita  ┃
┃                                                   ┃ 95/100   ┃
┃                                                   ┃ ▮▮▮▮▮▮▮▮▮┃
┃                                                   ┃          ┃
┃                                                   ┃ Amur Leo ┃
┃                                                   ┃ 91/100   ┃
┃                                                   ┗━━━━━━━━━━┛
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## What Each Part Does

### 🗺️ MAP (Center/Left)
- **Blue/green world map** showing all continents
- **Colored dots** = endangered species locations
  - 🔴 Red = Critical (90-100 risk)
  - 🟠 Orange = Endangered (70-89)
  - 🟡 Yellow = Vulnerable (50-69)
- **Click any dot** to see species details in a popup
- **Drag to pan**, **scroll to zoom**

### 📊 STATS (Top Right)
Four boxes showing:
- **71** = Average risk score
- **8** = Number of critical species
- **15** = Total species tracked
- **+12%** = Predicted change

### 🎛️ SCENARIO SLIDERS (Right Panel)
Six sliders to control:
1. **🌡️ Climate Change** (0 to +5°C)
2. **🌊 Sea Level Rise** (0 to +5m)
3. **🌳 Deforestation** (0 to +100%)
4. **💨 Air Pollution** (0 to +100%)
5. **🎣 Overfishing** (0 to +100%)
6. **🏭 Habitat Loss** (0 to +100%)

### 🔘 BUTTONS
- **Purple "PREDICT IMPACT"** = Run ML model
- **Gray "RESET"** = Reset sliders to default

### 🦁 SPECIES LIST (Right Panel, scrollable)
Shows each species with:
- Name (e.g., "Vaquita")
- Location (e.g., "Mexico")
- Risk bar (color-coded)
- Score (e.g., "95/100")

---

## How to Test It

### Test 1: Basic View
- ✅ Can you see the world map?
- ✅ Can you see colored dots on the map?
- ✅ Can you see the right panel with sliders?

### Test 2: Moderate Climate Change
1. Move "🌡️ Climate Change" slider to **+2.0°C**
2. Move "🌳 Deforestation" to **+25%**
3. Click **"PREDICT IMPACT"**
4. Wait 2 seconds
5. **Numbers should update!**
   - Average risk goes UP
   - Critical species count increases
   - Species list re-sorts

### Test 3: Extreme Scenario
1. Move ALL sliders to the RIGHT (maximum)
   - Climate: +5.0°C
   - Sea Level: +5.0m
   - Deforestation: +100%
   - Pollution: +100%
   - Overfishing: +100%
   - Habitat: +100%
2. Click **"PREDICT IMPACT"**
3. **Watch everything go RED!**
   - Most species hit 100/100 risk
   - Critical count = 15 (all species)

### Test 4: Conservation Success
1. Click **"RESET"** button
2. Move sliders to LOW values:
   - Climate: +0.5°C
   - Deforestation: +5%
   - Everything else: +5%
3. Click **"PREDICT IMPACT"**
4. **Risk should be LOWER**
   - Fewer critical species
   - Lower average risk

---

## Troubleshooting

### "I don't see the map"
- **Refresh the page** (F5)
- Check browser console (F12) for errors
- Make sure you opened `globe_dashboard_simple.html`

### "Map is blank/white"
- Map tiles loading from OpenStreetMap
- Wait 5-10 seconds for tiles to download
- Check your internet connection

### "Predict Impact" does nothing
- Check console (F12) for errors
- Look for "API connection failed" message
- API server might have crashed - run: `python run_api.py`

### I see "API Connection Failed"
The bottom info box will show this error. To fix:
1. Open terminal
2. Run: `python run_api.py`
3. Wait 5 seconds
4. Refresh browser page

### Map shows but no dots
- Console should say "Sample data loaded: 10 species"
- If not, check browser console (F12) for errors

---

## What Should Happen When You Click "Predict Impact"

1. **Loading spinner appears** ("Analyzing global impacts...")
2. **API call is made** (check browser console to see URL)
3. **Response received** (200 OK status)
4. **Numbers update:**
   - Top stat boxes change
   - Species list re-sorts
   - Map markers update colors
5. **Bottom panel updates** with prediction details

---

## Current API Status

```
✅ Server: http://localhost:8000
✅ Global Prediction: /predict/global
✅ Top Species: /species/top-threatened
✅ Regional Data: /regions/breakdown

Species in database: 15
Regions covered: 13
ML Model: Active
```

---

## Expected Results

### Baseline (No changes)
- Average Risk: ~74/100
- Critical Species: 7

### Moderate (Climate +2°C, Deforestation +20%)
- Average Risk: ~90/100
- Critical Species: 12-15

### Severe (All sliders maxed)
- Average Risk: 100/100
- Critical Species: 15 (all)

### Conservation (All sliders minimal)
- Average Risk: ~80/100
- Critical Species: 9-10

---

## Files

- **globe_dashboard_simple.html** = Main dashboard (this one!)
- **API Server** = python run_api.py
- **Test** = test_connection.html

---

**Your interactive globe is ready! Just refresh the browser page!** 🌍

