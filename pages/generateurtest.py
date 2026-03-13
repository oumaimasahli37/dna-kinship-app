# generate_test_csv.py - Générateur de données ADN avec relations familiales

import pandas as pd
import numpy as np
import random
from itertools import combinations

def generate_base_snp(origin_type="EUR"):
    """Génère un SNP de base selon l'origine ethnique"""
    # Profils génétiques approximatifs par population
    profiles = {
        "EUR": {"A": 0.3, "T": 0.25, "C": 0.25, "G": 0.2},    # Européen
        "EAS": {"A": 0.25, "T": 0.3, "C": 0.2, "G": 0.25},    # Asie de l'Est  
        "AFR": {"A": 0.35, "T": 0.2, "C": 0.25, "G": 0.2},    # Africain
        "SAS": {"A": 0.28, "T": 0.27, "C": 0.23, "G": 0.22},  # Asie du Sud
        "AMR": {"A": 0.3, "T": 0.25, "C": 0.23, "G": 0.22}    # Amériques
    }
    
    prob = profiles.get(origin_type, profiles["EUR"])
    bases = ["A", "T", "C", "G"]
    weights = [prob[base] for base in bases]
    
    return ''.join(np.random.choice(bases, size=1000, p=weights))

def create_related_snp(parent_snp, relationship_type):
    """Crée un SNP avec un degré de parenté spécifique"""
    parent_snp = list(parent_snp)
    child_snp = parent_snp.copy()
    
    # Taux de similitude selon le type de relation
    similarity_rates = {
        "identical_twin": 1.0,          # Jumeaux identiques
        "parent_child": 0.5,            # Parent-enfant  
        "full_sibling": 0.5,            # Frères-sœurs
        "half_sibling": 0.25,           # Demi-frères-sœurs
        "grandparent": 0.25,            # Grand-parent
        "uncle_aunt": 0.25,             # Oncle/tante
        "first_cousin": 0.125,          # Cousins germains
        "second_cousin": 0.0625,        # Cousins au second degré
        "distant_cousin": 0.03          # Cousins éloignés
    }
    
    similarity = similarity_rates.get(relationship_type, 0.0)
    
    # Nombre de positions à garder identiques
    positions_to_keep = int(1000 * similarity)
    
    # Positions à modifier
    positions_to_change = random.sample(range(1000), 1000 - positions_to_keep)
    
    bases = ["A", "T", "C", "G"]
    for pos in positions_to_change:
        # Mutation aléatoire
        child_snp[pos] = random.choice(bases)
    
    return ''.join(child_snp)

def generate_family_data():
    """Génère une famille complète avec plusieurs générations"""
    family_data = []
    
    # Coordonnées géographiques pour différentes régions
    regions = {
        "France": {"lat_range": (42.0, 51.0), "lon_range": (-5.0, 8.0), "origin": "EUR"},
        "Japon": {"lat_range": (30.0, 46.0), "lon_range": (129.0, 146.0), "origin": "EAS"},
        "Nigeria": {"lat_range": (4.0, 14.0), "lon_range": (3.0, 15.0), "origin": "AFR"},
        "Inde": {"lat_range": (6.0, 37.0), "lon_range": (68.0, 97.0), "origin": "SAS"},
        "Mexique": {"lat_range": (14.0, 33.0), "lon_range": (-118.0, -86.0), "origin": "AMR"}
    }
    
    families = []
    
    # === FAMILLE FRANÇAISE ÉTENDUE ===
    region = regions["France"]
    base_lat = np.random.uniform(*region["lat_range"])
    base_lon = np.random.uniform(*region["lon_range"])
    
    # Grand-parents
    grandpa_snp = generate_base_snp(region["origin"])
    grandma_snp = generate_base_snp(region["origin"])
    
    families.extend([
        {"ID": "FR_GRANDPA_01", "SNP_Vector": grandpa_snp, 
         "Latitude": base_lat + np.random.normal(0, 0.1), 
         "Longitude": base_lon + np.random.normal(0, 0.1)},
        {"ID": "FR_GRANDMA_01", "SNP_Vector": grandma_snp,
         "Latitude": base_lat + np.random.normal(0, 0.1), 
         "Longitude": base_lon + np.random.normal(0, 0.1)}
    ])
    
    # Parents (enfants des grands-parents)
    father_snp = create_related_snp(grandpa_snp, "parent_child")
    mother_snp = create_related_snp(grandma_snp, "parent_child")
    
    families.extend([
        {"ID": "FR_FATHER_01", "SNP_Vector": father_snp,
         "Latitude": base_lat + np.random.normal(0, 0.2), 
         "Longitude": base_lon + np.random.normal(0, 0.2)},
        {"ID": "FR_MOTHER_01", "SNP_Vector": mother_snp,
         "Latitude": base_lat + np.random.normal(0, 0.2), 
         "Longitude": base_lon + np.random.normal(0, 0.2)}
    ])
    
    # Enfants (frères et sœurs)
    child1_snp = create_related_snp(father_snp, "parent_child")
    child2_snp = create_related_snp(mother_snp, "parent_child") 
    child3_snp = create_related_snp(father_snp, "parent_child")
    
    # Jumeaux identiques
    twin1_snp = create_related_snp(father_snp, "parent_child")
    twin2_snp = create_related_snp(twin1_snp, "identical_twin")
    
    families.extend([
        {"ID": "FR_CHILD_01", "SNP_Vector": child1_snp,
         "Latitude": base_lat + np.random.normal(0, 0.3), 
         "Longitude": base_lon + np.random.normal(0, 0.3)},
        {"ID": "FR_CHILD_02", "SNP_Vector": child2_snp,
         "Latitude": base_lat + np.random.normal(0, 0.3), 
         "Longitude": base_lon + np.random.normal(0, 0.3)},
        {"ID": "FR_CHILD_03", "SNP_Vector": child3_snp,
         "Latitude": base_lat + np.random.normal(0, 0.3), 
         "Longitude": base_lon + np.random.normal(0, 0.3)},
        {"ID": "FR_TWIN_A", "SNP_Vector": twin1_snp,
         "Latitude": base_lat + np.random.normal(0, 0.05), 
         "Longitude": base_lon + np.random.normal(0, 0.05)},
        {"ID": "FR_TWIN_B", "SNP_Vector": twin2_snp,
         "Latitude": base_lat + np.random.normal(0, 0.05), 
         "Longitude": base_lon + np.random.normal(0, 0.05)}
    ])
    
    # Oncle/Tante (frère du père)
    uncle_snp = create_related_snp(grandpa_snp, "parent_child")
    aunt_snp = generate_base_snp(region["origin"])
    
    families.extend([
        {"ID": "FR_UNCLE_01", "SNP_Vector": uncle_snp,
         "Latitude": base_lat + np.random.normal(0, 0.5), 
         "Longitude": base_lon + np.random.normal(0, 0.5)},
        {"ID": "FR_AUNT_01", "SNP_Vector": aunt_snp,
         "Latitude": base_lat + np.random.normal(0, 0.5), 
         "Longitude": base_lon + np.random.normal(0, 0.5)}
    ])
    
    # Cousins (enfants de l'oncle et tante)
    cousin1_snp = create_related_snp(uncle_snp, "parent_child")
    cousin2_snp = create_related_snp(aunt_snp, "parent_child")
    
    families.extend([
        {"ID": "FR_COUSIN_01", "SNP_Vector": cousin1_snp,
         "Latitude": base_lat + np.random.normal(0, 0.8), 
         "Longitude": base_lon + np.random.normal(0, 0.8)},
        {"ID": "FR_COUSIN_02", "SNP_Vector": cousin2_snp,
         "Latitude": base_lat + np.random.normal(0, 0.8), 
         "Longitude": base_lon + np.random.normal(0, 0.8)}
    ])

    # === FAMILLE JAPONAISE ===
    region = regions["Japon"]
    base_lat = np.random.uniform(*region["lat_range"])
    base_lon = np.random.uniform(*region["lon_range"])
    
    jp_father_snp = generate_base_snp(region["origin"])
    jp_mother_snp = generate_base_snp(region["origin"])
    jp_child1_snp = create_related_snp(jp_father_snp, "parent_child")
    jp_child2_snp = create_related_snp(jp_mother_snp, "parent_child")
    
    families.extend([
        {"ID": "JP_FATHER_01", "SNP_Vector": jp_father_snp,
         "Latitude": base_lat, "Longitude": base_lon},
        {"ID": "JP_MOTHER_01", "SNP_Vector": jp_mother_snp,
         "Latitude": base_lat + 0.1, "Longitude": base_lon + 0.1},
        {"ID": "JP_CHILD_01", "SNP_Vector": jp_child1_snp,
         "Latitude": base_lat + 0.2, "Longitude": base_lon + 0.2},
        {"ID": "JP_CHILD_02", "SNP_Vector": jp_child2_snp,
         "Latitude": base_lat + 0.3, "Longitude": base_lon + 0.3}
    ])

    # === FAMILLE NIGÉRIENNE ===
    region = regions["Nigeria"]
    base_lat = np.random.uniform(*region["lat_range"])
    base_lon = np.random.uniform(*region["lon_range"])
    
    ng_grandpa_snp = generate_base_snp(region["origin"])
    ng_father_snp = create_related_snp(ng_grandpa_snp, "parent_child")
    ng_mother_snp = generate_base_snp(region["origin"])
    ng_child_snp = create_related_snp(ng_father_snp, "parent_child")
    
    families.extend([
        {"ID": "NG_GRANDPA_01", "SNP_Vector": ng_grandpa_snp,
         "Latitude": base_lat, "Longitude": base_lon},
        {"ID": "NG_FATHER_01", "SNP_Vector": ng_father_snp,
         "Latitude": base_lat + 0.1, "Longitude": base_lon + 0.1},
        {"ID": "NG_MOTHER_01", "SNP_Vector": ng_mother_snp,
         "Latitude": base_lat + 0.1, "Longitude": base_lon + 0.1},
        {"ID": "NG_CHILD_01", "SNP_Vector": ng_child_snp,
         "Latitude": base_lat + 0.2, "Longitude": base_lon + 0.2}
    ])

    # === FAMILLE INDIENNE ===
    region = regions["Inde"]
    base_lat = np.random.uniform(*region["lat_range"])
    base_lon = np.random.uniform(*region["lon_range"])
    
    in_father_snp = generate_base_snp(region["origin"])
    in_mother_snp = generate_base_snp(region["origin"])
    in_brother1_snp = create_related_snp(in_father_snp, "parent_child")
    in_brother2_snp = create_related_snp(in_mother_snp, "parent_child")
    in_sister_snp = create_related_snp(in_father_snp, "parent_child")
    
    families.extend([
        {"ID": "IN_FATHER_01", "SNP_Vector": in_father_snp,
         "Latitude": base_lat, "Longitude": base_lon},
        {"ID": "IN_MOTHER_01", "SNP_Vector": in_mother_snp,
         "Latitude": base_lat, "Longitude": base_lon},
        {"ID": "IN_BROTHER_01", "SNP_Vector": in_brother1_snp,
         "Latitude": base_lat + 0.1, "Longitude": base_lon + 0.1},
        {"ID": "IN_BROTHER_02", "SNP_Vector": in_brother2_snp,
         "Latitude": base_lat + 0.1, "Longitude": base_lon + 0.1},
        {"ID": "IN_SISTER_01", "SNP_Vector": in_sister_snp,
         "Latitude": base_lat + 0.1, "Longitude": base_lon + 0.1}
    ])

    # === FAMILLE MEXICAINE ===
    region = regions["Mexique"]
    base_lat = np.random.uniform(*region["lat_range"])
    base_lon = np.random.uniform(*region["lon_range"])
    
    mx_mother_snp = generate_base_snp(region["origin"])
    mx_father_snp = generate_base_snp(region["origin"])
    mx_daughter_snp = create_related_snp(mx_mother_snp, "parent_child")
    mx_son_snp = create_related_snp(mx_father_snp, "parent_child")
    
    families.extend([
        {"ID": "MX_MOTHER_01", "SNP_Vector": mx_mother_snp,
         "Latitude": base_lat, "Longitude": base_lon},
        {"ID": "MX_FATHER_01", "SNP_Vector": mx_father_snp,
         "Latitude": base_lat, "Longitude": base_lon},
        {"ID": "MX_DAUGHTER_01", "SNP_Vector": mx_daughter_snp,
         "Latitude": base_lat + 0.2, "Longitude": base_lon + 0.2},
        {"ID": "MX_SON_01", "SNP_Vector": mx_son_snp,
         "Latitude": base_lat + 0.2, "Longitude": base_lon + 0.2}
    ])

    # === INDIVIDUS NON APPARENTÉS ===
    for i, (region_name, region_data) in enumerate(regions.items()):
        for j in range(3):  # 3 individus non apparentés par région
            individual_snp = generate_base_snp(region_data["origin"])
            lat = np.random.uniform(*region_data["lat_range"])
            lon = np.random.uniform(*region_data["lon_range"])
            
            families.append({
                "ID": f"UNRELATED_{region_name[:2]}_{i}_{j}",
                "SNP_Vector": individual_snp,
                "Latitude": lat,
                "Longitude": lon
            })
    
    return families

def create_test_csv(filename="test_dna_data.csv", num_additional_unrelated=10):
    """Crée un fichier CSV de test complet"""
    
    print("🧬 Génération des données de test ADN...")
    
    # Générer les familles
    family_data = generate_family_data()
    
    # Ajouter des individus non apparentés supplémentaires
    world_locations = [
        {"name": "USA", "lat": 39.8283, "lon": -98.5795, "origin": "EUR"},
        {"name": "Brasil", "lat": -14.2350, "lon": -51.9253, "origin": "AMR"},
        {"name": "China", "lat": 35.8617, "lon": 104.1954, "origin": "EAS"},
        {"name": "Russia", "lat": 61.5240, "lon": 105.3188, "origin": "EUR"},
        {"name": "Australia", "lat": -25.2744, "lon": 133.7751, "origin": "EUR"},
        {"name": "Egypt", "lat": 26.0975, "lon": 31.2357, "origin": "AFR"},
        {"name": "Thailand", "lat": 15.8700, "lon": 100.9925, "origin": "EAS"},
        {"name": "Argentina", "lat": -38.4161, "lon": -63.6167, "origin": "AMR"},
        {"name": "Turkey", "lat": 38.9637, "lon": 35.2433, "origin": "EUR"},
        {"name": "South_Africa", "lat": -30.5595, "lon": 22.9375, "origin": "AFR"}
    ]
    
    for i in range(num_additional_unrelated):
        location = random.choice(world_locations)
        individual_snp = generate_base_snp(location["origin"])
        
        # Ajouter du bruit géographique
        lat_noise = np.random.normal(0, 2.0)  # Plus de variation géographique
        lon_noise = np.random.normal(0, 2.0)
        
        family_data.append({
            "ID": f"UNRELATED_{location['name']}_{i:02d}",
            "SNP_Vector": individual_snp,
            "Latitude": location["lat"] + lat_noise,
            "Longitude": location["lon"] + lon_noise
        })
    
    # Créer le DataFrame
    df = pd.DataFrame(family_data)
    
    # Mélanger l'ordre des lignes
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Sauvegarder le fichier
    df.to_csv(filename, index=False)
    
    print(f"✅ Fichier CSV créé : {filename}")
    print(f"📊 Nombre total d'individus : {len(df)}")
    
    # Statistiques
    relations_expected = []
    
    # Compter les relations attendues par famille française (la plus complète)
    fr_family = [row for row in family_data if row["ID"].startswith("FR_")]
    print(f"👨‍👩‍👧‍👦 Famille française : {len(fr_family)} membres")
    print("   - 2 jumeaux identiques (coefficient ~1.0)")
    print("   - Relations parent-enfant multiples (coefficient ~0.5)")
    print("   - Relations frères-sœurs (coefficient ~0.5)")
    print("   - Relations oncle-tante/neveu-nièce (coefficient ~0.25)")
    print("   - Relations cousins (coefficient ~0.125)")
    print("   - Relations grands-parents (coefficient ~0.25)")
    
    # Aperçu du fichier
    print("\n👀 Aperçu des données :")
    preview = df.copy()
    preview["SNP_Vector"] = preview["SNP_Vector"].str[:20] + "..."
    print(preview.head(10).to_string())
    
    print(f"\n🎯 Relations familiales détectables :")
    print(f"   - Jumeaux identiques : 1 paire")
    print(f"   - Parent-enfant : ~15-20 paires") 
    print(f"   - Frères-sœurs : ~10-15 paires")
    print(f"   - Cousins : ~5-10 paires")
    print(f"   - Relations diverses : ~20-30 paires")
    
    return filename

# Fonction principale
if __name__ == "__main__":
    print("🚀 Générateur de données ADN avec relations familiales")
    print("=" * 60)
    
    # Créer le fichier de test
    csv_file = create_test_csv("test_family_dna.csv", num_additional_unrelated=15)
    
    print(f"\n✨ Fichier de test créé avec succès !")
    print(f"📁 Nom du fichier : {csv_file}")
    print(f"💡 Utilisez ce fichier pour tester votre application DNA KINSHIP")
    
    # Vérification finale
    test_df = pd.read_csv(csv_file)
    print(f"\n🔍 Vérification finale :")
    print(f"   - Lignes : {len(test_df)}")
    print(f"   - Colonnes : {list(test_df.columns)}")
    print(f"   - Longueur SNP : {len(test_df.iloc[0]['SNP_Vector'])}")
    print(f"   - Allèles valides : {set(''.join(test_df['SNP_Vector'].tolist())).issubset(set('ATCG'))}")
    
    print("\n🎉 Prêt pour l'analyse !")
