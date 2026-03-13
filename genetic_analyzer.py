# genetic_analyzer.py - Module d'analyse génétique
import numpy as np
import pandas as pd
import random
from typing import Dict, Tuple, List

class GeneticAnalyzer:
    """Analyseur génétique pour prédiction d'origines"""
    
    def __init__(self):
        # Signatures génétiques par population
        self.population_signatures = {
            "European": {
                "gc_range": (0.45, 0.55),
                "at_range": (0.45, 0.55),
                "countries": ["France", "Germany", "Italy", "Spain", "United_Kingdom", "Netherlands", "Poland"],
                "priority": 0.8
            },
            "East_Asian": {
                "gc_range": (0.52, 0.62),
                "at_range": (0.38, 0.48),
                "countries": ["China", "Japan", "South_Korea", "Thailand", "Vietnam"],
                "priority": 0.9
            },
            "African": {
                "gc_range": (0.38, 0.48),
                "at_range": (0.52, 0.62),
                "countries": ["Nigeria", "Kenya", "South_Africa", "Ethiopia"],
                "priority": 0.85
            },
            "South_Asian": {
                "gc_range": (0.48, 0.58),
                "at_range": (0.42, 0.52),
                "countries": ["India", "Iran"],
                "priority": 0.87
            },
            "Admixed_American": {
                "gc_range": (0.44, 0.54),
                "at_range": (0.46, 0.56),
                "countries": ["United_States", "Canada", "Mexico", "Brazil", "Argentina"],
                "priority": 0.75
            },
            "Middle_Eastern": {
                "gc_range": (0.46, 0.56),
                "at_range": (0.44, 0.54),
                "countries": ["Morocco", "Algeria", "Tunisia", "Egypt", "Turkey"],
                "priority": 0.82
            }
        }

    def analyze_snp_composition(self, snp_vector: str) -> Dict:
        """Analyse la composition des bases du vecteur SNP"""
        if len(snp_vector) != 1000:
            return None
        
        counts = {base: snp_vector.count(base) for base in 'ATCG'}
        freqs = {base: count/1000 for base, count in counts.items()}
        
        return {
            'gc_content': freqs['G'] + freqs['C'],
            'at_content': freqs['A'] + freqs['T'],
            'base_freqs': freqs,
            'diversity': len([f for f in freqs.values() if f > 0.15])
        }

    def predict_origin(self, snp_vector: str) -> Tuple[str, float, str]:
        """Prédit l'origine génétique"""
        composition = self.analyze_snp_composition(snp_vector)
        if not composition:
            return "Unknown", 0.1, "Données insuffisantes"
        
        gc_content = composition['gc_content']
        at_content = composition['at_content']
        
        best_match = None
        best_score = 0
        
        for population, signature in self.population_signatures.items():
            gc_match = signature['gc_range'][0] <= gc_content <= signature['gc_range'][1]
            at_match = signature['at_range'][0] <= at_content <= signature['at_range'][1]
            
            if gc_match and at_match:
                gc_center = sum(signature['gc_range']) / 2
                at_center = sum(signature['at_range']) / 2
                
                gc_distance = abs(gc_content - gc_center)
                at_distance = abs(at_content - at_center)
                
                score = signature['priority'] * (1 - (gc_distance + at_distance))
                
                if score > best_score:
                    best_match = population
                    best_score = score
        
        if best_match:
            countries = self.population_signatures[best_match]['countries']
            selected_country = random.choice(countries)
            confidence = min(0.95, max(0.3, best_score))
            return selected_country, confidence, f"Analyse génétique: {best_match}"
        else:
            # Fallback
            if gc_content > 0.55:
                return random.choice(["China", "Japan"]), 0.4, "GC élevé - Asie"
            elif at_content > 0.55:
                return random.choice(["Nigeria", "Kenya"]), 0.4, "AT élevé - Afrique"
            else:
                return random.choice(["France", "Germany"]), 0.3, "Composition équilibrée"

class KinshipAnalyzer:
    """Analyseur de relations familiales"""
    
    def __init__(self):
        self.relationship_types = {
            "Père-Fils": {"threshold": 0.45, "color": "#FF0080"},
            "Mère-Fille": {"threshold": 0.42, "color": "#FF1493"},
            "Frères": {"threshold": 0.40, "color": "#FF4500"},
            "Sœurs": {"threshold": 0.38, "color": "#FF6347"},
            "Frère-Sœur": {"threshold": 0.35, "color": "#FFA500"},
            "Grand-père-Petit-fils": {"threshold": 0.22, "color": "#32CD32"},
            "Oncle-Neveu": {"threshold": 0.18, "color": "#00CED1"},
            "Cousins germains": {"threshold": 0.12, "color": "#9370DB"},
            "Cousins éloignés": {"threshold": 0.06, "color": "#B0C4DE"},
            "Apparentés distants": {"threshold": 0.03, "color": "#708090"}
        }
    
    def calculate_kinship_coefficient(self, snp1: str, snp2: str, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcule le coefficient de parenté"""
        if len(snp1) != len(snp2) or len(snp1) != 1000:
            return 0
        
        # Conversion en arrays
        arr1 = np.array([{'A': 0, 'T': 1, 'C': 2, 'G': 3}[base] for base in snp1])
        arr2 = np.array([{'A': 0, 'T': 1, 'C': 2, 'G': 3}[base] for base in snp2])
        
        # Similarité de base
        ibs = np.mean(arr1 == arr2)
        
        # Facteur géographique
        geo_distance = np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
        geo_factor = max(0.1, 1 - (geo_distance / 100))
        
        # Score final
        final_score = ibs * geo_factor
        noise = np.random.normal(0, 0.02)
        return max(0, min(0.5, final_score + noise))
    
    def determine_relationship(self, coefficient: float) -> Tuple[str, str]:
        """Détermine le type de relation"""
        sorted_relations = sorted(self.relationship_types.items(), 
                                key=lambda x: x[1]["threshold"], 
                                reverse=True)
        
        for relation_name, relation_data in sorted_relations:
            if coefficient >= relation_data["threshold"]:
                return relation_name, relation_data["color"]
        
        return "Non apparentés", "#404040"
    
    def analyze_relationships(self, df: pd.DataFrame, threshold: float = 0.03) -> List[Dict]:
        """Analyse toutes les relations dans le dataset"""
        relationships = []
        
        for i in range(len(df)):
            for j in range(i + 1, len(df)):
                ind1 = df.iloc[i]
                ind2 = df.iloc[j]
                
                coefficient = self.calculate_kinship_coefficient(
                    ind1['SNP_Vector'], ind2['SNP_Vector'],
                    ind1['Generated_Latitude'], ind1['Generated_Longitude'],
                    ind2['Generated_Latitude'], ind2['Generated_Longitude']
                )
                
                if coefficient >= threshold:
                    relation_type, color = self.determine_relationship(coefficient)
                    
                    relationships.append({
                        'ID1': ind1['ID'],
                        'ID2': ind2['ID'],
                        'Coefficient': round(coefficient, 4),
                        'Relation': relation_type,
                        'Color': color,
                        'Lat1': ind1['Generated_Latitude'],
                        'Lon1': ind1['Generated_Longitude'],
                        'Lat2': ind2['Generated_Latitude'],
                        'Lon2': ind2['Generated_Longitude']
                    })
        
        return relationships
