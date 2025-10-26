"""
Fetch REAL threatened species from GBIF API
Gets hundreds of species with actual data
"""

import requests
import json
import time

print("Fetching REAL species from GBIF API...")
print("="*60)

# IUCN Red List threatened species
# These are species codes we can fetch from GBIF
threatened_species_names = [
    # Mammals - Big cats
    "Panthera tigris", "Panthera leo", "Panthera pardus", "Panthera onca", "Panthera uncia",
    "Neofelis nebulosa", "Lynx pardinus", "Acinonyx jubatus",
    
    # Primates  
    "Pongo abelii", "Pongo pygmaeus", "Gorilla gorilla", "Gorilla beringei", 
    "Pan troglodytes", "Pan paniscus", "Nomascus concolor", "Hylobates moloch",
    
    # Elephants
    "Loxodonta africana", "Loxodonta cyclotis", "Elephas maximus",
    
    # Rhinoceros
    "Diceros bicornis", "Ceratotherium simum", "Rhinoceros unicornis", 
    "Rhinoceros sondaicus", "Dicerorhinus sumatrensis",
    
    # Bears
    "Ursus maritimus", "Ursus arctos", "Ailuropoda melanoleuca", "Tremarctos ornatus",
    "Helarctos malayanus", "Melursus ursinus",
    
    # Whales & Dolphins
    "Balaenoptera musculus", "Balaenoptera physalus", "Megaptera novaeangliae",
    "Physeter macrocephalus", "Eubalaena glacialis", "Eschrichtius robustus",
    "Phocoena sinus", "Neophocaena asiaeorientalis", "Lipotes vexillifer",
    
    # Sea Turtles
    "Chelonia mydas", "Caretta caretta", "Eretmochelys imbricata", 
    "Dermochelys coriacea", "Lepidochelys kempii", "Lepidochelys olivacea",
    
    # Birds - Eagles & Raptors
    "Haliaeetus leucocephalus", "Aquila chrysaetos", "Harpia harpyja",
    "Pithecophaga jefferyi", "Gypaetus barbatus",
    
    # Penguins
    "Aptenodytes forsteri", "Spheniscus mendiculus", "Spheniscus humboldti",
    "Eudyptula minor",
    
    # Parrots
    "Strigops habroptila", "Ara glaucogularis", "Amazona imperialis",
    "Psittacula krameri",
    
    # Reptiles
    "Varanus komodoensis", "Gavialis gangeticus", "Crocodylus porosus",
    "Alligator sinensis",
    
    # Amphibians
    "Ambystoma mexicanum", "Andrias davidianus", "Andrias japonicus",
    "Atelopus zeteki",
]

all_species = []
count = 0

print(f"Querying GBIF for {len(threatened_species_names)} species...\n")

for scientific_name in threatened_species_names:
    try:
        # Get species info
        match_url = f"https://api.gbif.org/v1/species/match?name={scientific_name}"
        match_response = requests.get(match_url, timeout=10)
        match_data = match_response.json()
        
        if match_data.get("usageKey"):
            gbif_key = match_data["usageKey"]
            
            # Get occurrences to find coordinates
            occ_url = f"https://api.gbif.org/v1/occurrence/search?taxonKey={gbif_key}&hasCoordinate=true&limit=50"
            occ_response = requests.get(occ_url, timeout=10)
            occ_data = occ_response.json()
            
            if "results" in occ_data and len(occ_data["results"]) > 0:
                # Calculate centroid
                lats = [r["decimalLatitude"] for r in occ_data["results"] if "decimalLatitude" in r]
                lons = [r["decimalLongitude"] for r in occ_data["results"] if "decimalLongitude" in r]
                countries = [r.get("country", "") for r in occ_data["results"]]
                
                if lats and lons:
                    species_entry = {
                        "scientific": scientific_name,
                        "name": match_data.get("canonicalName", scientific_name),
                        "gbif_key": gbif_key,
                        "lat": sum(lats) / len(lats),
                        "lon": sum(lons) / len(lons),
                        "occurrence_count": len(lats),
                        "taxon_class": match_data.get("class", "Unknown"),
                        "order": match_data.get("order", ""),
                        "family": match_data.get("family", ""),
                        "countries": list(set(c for c in countries if c)),
                        "region": _infer_region(sum(lats)/len(lats), sum(lons)/len(lons))
                    }
                    
                    all_species.append(species_entry)
                    count += 1
                    
                    if count % 10 == 0:
                        print(f"  Fetched {count} species...")
                    
        time.sleep(0.1)  # Rate limiting
        
    except Exception as e:
        print(f"  Error fetching {scientific_name}: {e}")
        continue

def _infer_region(lat, lon):
    """Infer region from coordinates"""
    if lat > 66:
        return "Arctic"
    elif lat < -60:
        return "Antarctica"
    elif lon > 60 and lon < 150 and lat > 0:
        return "Asia"
    elif lon > -20 and lon < 60 and lat < 35 and lat > -35:
        return "Africa"
    elif lon < -30 and lat > 15:
        return "North America"
    elif lon < -30 and lat < 15:
        return "South America"
    elif lon > -20 and lon < 60 and lat > 35:
        return "Europe"
    elif abs(lat) < 30 and (lon < -60 or lon > 100):
        return "Pacific Ocean"
    else:
        return "Atlantic Ocean"

# Save to JSON
output_file = "real_species_from_gbif.json"
with open(output_file, 'w') as f:
    json.dump(all_species, f, indent=2)

print(f"\n{'='*60}")
print(f"SUCCESS! Fetched {len(all_species)} REAL species from GBIF")
print(f"Saved to: {output_file}")
print(f"{'='*60}\n")

# Show breakdown
from collections import Counter
taxon_counts = Counter(s["taxon_class"] for s in all_species)
print("By taxonomic class:")
for taxon, count in taxon_counts.most_common():
    print(f"  {taxon}: {count}")

region_counts = Counter(s["region"] for s in all_species)
print(f"\nBy region:")
for region, count in region_counts.most_common():
    print(f"  {region}: {count}")

print(f"\nTotal occurrences: {sum(s['occurrence_count'] for s in all_species):,}")

