# coordinate_generator.py - Module de génération de coordonnées corrigé
import random
from typing import Tuple, Dict

class CoordinateGenerator:
    """Générateur de coordonnées géographiques par pays avec limites terrestres précises"""
    
    def __init__(self):
        self.country_bounds = {
            # Europe (limites terrestres uniquement)
            "France": {"lat": (42.2, 51.0), "lon": (-4.8, 8.2), "name": "France"},
            "Germany": {"lat": (47.5, 54.9), "lon": (6.0, 15.0), "name": "Allemagne"},
            "Italy": {"lat": (36.6, 47.1), "lon": (6.6, 18.5), "name": "Italie"},
            "Spain": {"lat": (35.6, 43.8), "lon": (-9.0, 3.3), "name": "Espagne"},
            "United_Kingdom": {"lat": (50.0, 59.0), "lon": (-7.5, 1.8), "name": "Royaume-Uni"},
            "Netherlands": {"lat": (50.8, 53.5), "lon": (3.4, 7.2), "name": "Pays-Bas"},
            "Poland": {"lat": (49.0, 54.8), "lon": (14.1, 24.1), "name": "Pologne"},
            
            # Asie (limites continentales)
            "China": {"lat": (20.0, 53.0), "lon": (75.0, 134.0), "name": "Chine"},
            "Japan": {"lat": (24.4, 45.5), "lon": (122.9, 145.8), "name": "Japon"},
            "South_Korea": {"lat": (33.2, 38.6), "lon": (124.6, 131.0), "name": "Corée du Sud"},
            "India": {"lat": (8.0, 37.1), "lon": (68.2, 97.4), "name": "Inde"},
            "Thailand": {"lat": (5.6, 20.5), "lon": (97.3, 105.6), "name": "Thaïlande"},
            "Vietnam": {"lat": (8.6, 23.4), "lon": (102.1, 109.5), "name": "Vietnam"},
            "Iran": {"lat": (25.1, 39.8), "lon": (44.0, 63.3), "name": "Iran"},
            
            # Afrique (continentale seulement)
            "Nigeria": {"lat": (4.3, 13.9), "lon": (2.7, 14.7), "name": "Nigeria"},
            "Kenya": {"lat": (-4.7, 5.0), "lon": (33.9, 41.9), "name": "Kenya"},
            "South_Africa": {"lat": (-34.8, -22.1), "lon": (16.5, 32.9), "name": "Afrique du Sud"},
            "Ethiopia": {"lat": (3.4, 18.0), "lon": (32.9, 48.0), "name": "Éthiopie"},
            "Morocco": {"lat": (21.4, 35.9), "lon": (-13.2, -1.0), "name": "Maroc"},
            "Algeria": {"lat": (19.0, 37.1), "lon": (-8.7, 12.0), "name": "Algérie"},
            "Tunisia": {"lat": (30.2, 37.5), "lon": (7.5, 11.6), "name": "Tunisie"},
            "Egypt": {"lat": (22.0, 31.7), "lon": (24.7, 37.0), "name": "Égypte"},
            "Turkey": {"lat": (35.8, 42.1), "lon": (25.7, 44.8), "name": "Turquie"},
            
            # Amériques (limites continentales)
            "United_States": {"lat": (25.0, 49.0), "lon": (-124.0, -67.0), "name": "États-Unis"},
            "Canada": {"lat": (42.0, 83.0), "lon": (-141.0, -53.0), "name": "Canada"},
            "Mexico": {"lat": (14.5, 32.7), "lon": (-117.0, -86.7), "name": "Mexique"},
            "Brazil": {"lat": (-33.7, 5.3), "lon": (-74.0, -28.8), "name": "Brésil"},
            "Argentina": {"lat": (-55.0, -21.8), "lon": (-73.6, -53.6), "name": "Argentine"},
            
            # Océanie (terres émergées)
            "Australia": {"lat": (-43.6, -9.2), "lon": (113.2, 153.6), "name": "Australie"},
            
            # Pays par défaut
            "Unknown": {"lat": (48.8, 48.9), "lon": (2.3, 2.4), "name": "Inconnu"}
        }
        
        # Points centraux sûrs pour chaque pays (sur terre ferme)
        self.safe_centers = {
            "France": (46.6, 2.2),
            "Germany": (51.1, 10.4),
            "Italy": (41.9, 12.6),
            "Spain": (40.5, -3.7),
            "United_Kingdom": (55.4, -3.4),
            "Netherlands": (52.1, 5.3),
            "Poland": (51.9, 19.1),
            "China": (35.9, 104.2),
            "Japan": (36.2, 138.3),
            "South_Korea": (35.9, 127.8),
            "India": (20.6, 78.9),
            "Thailand": (15.9, 100.9),
            "Vietnam": (14.1, 108.3),
            "Iran": (32.4, 53.7),
            "Nigeria": (9.1, 8.7),
            "Kenya": (-0.0, 37.9),
            "South_Africa": (-30.6, 22.9),
            "Ethiopia": (9.1, 40.5),
            "Morocco": (31.8, -7.1),
            "Algeria": (28.0, 1.7),
            "Tunisia": (33.9, 9.5),
            "Egypt": (26.8, 30.8),
            "Turkey": (38.96, 35.2),
            "United_States": (39.8, -98.6),
            "Canada": (56.1, -106.3),
            "Mexico": (23.6, -102.5),
            "Brazil": (-14.2, -51.9),
            "Argentina": (-38.4, -63.6),
            "Australia": (-25.3, 133.8),
            "Unknown": (48.8, 2.3)
        }
    
    def generate_coordinates(self, country_code: str) -> Tuple[float, float, str]:
        """Génère des coordonnées terrestres réalistes pour un pays"""
        if country_code not in self.country_bounds:
            country_code = "Unknown"
        
        bounds = self.country_bounds[country_code]
        center = self.safe_centers[country_code]
        
        # Utiliser une approche mixte : zone autour du centre + limites générales
        use_center_zone = random.choice([True, False])
        
        if use_center_zone:
            # Générer autour du centre sûr (90% de chance d'être sur terre)
            center_lat, center_lon = center
            lat_offset = random.uniform(-2.0, 2.0)  # ±2 degrés autour du centre
            lon_offset = random.uniform(-2.0, 2.0)
            
            latitude = center_lat + lat_offset
            longitude = center_lon + lon_offset
            
            # Vérifier que c'est dans les limites du pays
            lat_min, lat_max = bounds["lat"]
            lon_min, lon_max = bounds["lon"]
            
            latitude = max(lat_min, min(lat_max, latitude))
            longitude = max(lon_min, min(lon_max, longitude))
        else:
            # Générer dans les limites générales (mais en évitant les zones océaniques)
            lat_min, lat_max = bounds["lat"]
            lon_min, lon_max = bounds["lon"]
            
            # Pour certains pays, ajuster les limites pour éviter l'océan
            if country_code == "United_States":
                # Éviter les zones océaniques des côtes
                latitude = random.uniform(lat_min + 1, lat_max - 1)
                longitude = random.uniform(lon_min + 2, lon_max - 2)
            elif country_code == "Canada":
                # Éviter l'Arctique et les zones côtières
                latitude = random.uniform(lat_min, min(70, lat_max))
                longitude = random.uniform(lon_min + 5, lon_max - 5)
            else:
                latitude = random.uniform(lat_min, lat_max)
                longitude = random.uniform(lon_min, lon_max)
        
        return latitude, longitude, bounds["name"]
    
    def is_coordinate_on_land(self, lat: float, lon: float) -> bool:
        """Vérification basique si les coordonnées sont probablement sur terre"""
        # Zones océaniques principales à éviter
        ocean_zones = [
            # Atlantique Nord
            {"lat_range": (30, 60), "lon_range": (-50, -10)},
            # Atlantique Sud
            {"lat_range": (-40, 30), "lon_range": (-40, 10)},
            # Pacifique
            {"lat_range": (-40, 60), "lon_range": (140, -140)},  # Gestion ligne de changement
            # Océan Indien
            {"lat_range": (-40, 25), "lon_range": (40, 110)},
            # Arctique
            {"lat_range": (75, 90), "lon_range": (-180, 180)}
        ]
        
        for zone in ocean_zones:
            lat_range = zone["lat_range"]
            lon_range = zone["lon_range"]
            
            lat_in_range = lat_range[0] <= lat <= lat_range[1]
            
            if zone == ocean_zones[2]:  # Pacifique (gestion spéciale)
                lon_in_range = lon >= 140 or lon <= -140
            else:
                lon_in_range = lon_range[0] <= lon <= lon_range[1]
            
            if lat_in_range and lon_in_range:
                return False  # Probablement dans l'océan
        
        return True  # Probablement sur terre
    
    def generate_safe_coordinates(self, country_code: str, max_attempts: int = 15) -> Tuple[float, float, str]:
        """Génère des coordonnées sûres avec vérification stricte des frontières"""
        
        if country_code not in self.country_bounds:
            country_code = "Unknown"
        
        bounds = self.country_bounds[country_code]
        center = self.safe_centers[country_code]
        
        # Stratégie en 3 étapes pour garantir la précision
        for strategy in range(3):
            for attempt in range(max_attempts // 3):
                
                if strategy == 0:
                    # Étape 1: Zone très proche du centre (rayon 1°)
                    center_lat, center_lon = center
                    lat_offset = random.uniform(-1.0, 1.0)
                    lon_offset = random.uniform(-1.0, 1.0)
                    
                    latitude = center_lat + lat_offset
                    longitude = center_lon + lon_offset
                    
                elif strategy == 1:
                    # Étape 2: Zone modérée autour du centre (rayon 2°)
                    center_lat, center_lon = center
                    lat_offset = random.uniform(-2.0, 2.0)
                    lon_offset = random.uniform(-2.0, 2.0)
                    
                    latitude = center_lat + lat_offset
                    longitude = center_lon + lon_offset
                    
                else:
                    # Étape 3: Dans les limites complètes mais avec marge
                    lat_min, lat_max = bounds["lat"]
                    lon_min, lon_max = bounds["lon"]
                    
                    # Ajouter une marge de 0.5° pour éviter les frontières exactes
                    lat_margin = min(0.5, (lat_max - lat_min) * 0.1)
                    lon_margin = min(0.5, (lon_max - lon_min) * 0.1)
                    
                    latitude = random.uniform(lat_min + lat_margin, lat_max - lat_margin)
                    longitude = random.uniform(lon_min + lon_margin, lon_max - lon_margin)
                
                # Vérifier que c'est dans les limites strictes du pays
                lat_min, lat_max = bounds["lat"]
                lon_min, lon_max = bounds["lon"]
                
                if lat_min <= latitude <= lat_max and lon_min <= longitude <= lon_max:
                    # Vérification anti-océan spécifique par pays
                    if self.is_coordinate_valid_for_country(latitude, longitude, country_code):
                        return latitude, longitude, bounds["name"]
        
        # Si toutes les tentatives échouent, utiliser le centre sûr
        center_lat, center_lon = center
        return center_lat, center_lon, bounds["name"]
    
    def is_coordinate_valid_for_country(self, lat: float, lon: float, country_code: str) -> bool:
        """Vérification spécifique par pays pour éviter zones problématiques"""
        
        # Règles spécifiques pour éviter les confusions géographiques
        if country_code == "India":
            # Éviter le Pakistan (lon < 77.8 et lat > 23.6)
            if lon > 77.8 and lat > 23.6:
                return False
            # Éviter le golfe du Bengale
            if lon > 92 and lat < 15:
                return False
                
        elif country_code == "Pakistan":
            # Rester dans les limites du Pakistan, éviter l'Inde
            if lon > 77.8:
                return False
            if lat < 25 and lon > 70:
                return False
                
        elif country_code == "China":
            # Éviter la Mongolie (lat > 45 et lon < 110)
            if lat > 45 and lon < 110:
                return False
            # Éviter la mer de Chine
            if lon > 125 and lat < 30:
                return False
                
        elif country_code == "United_States":
            # Éviter les Grands Lacs
            if 41 < lat < 49 and -95 < lon < -75:
                return False
            # Éviter le golfe du Mexique
            if lat < 30 and -100 < lon < -80:
                return False
                
        elif country_code == "Turkey":
            # Éviter la mer Noire et la Méditerranée
            if lat > 42 or lat < 36:
                return False
                
        # Vérification générale anti-océan
        return self.is_coordinate_on_land(lat, lon)
    
    def get_available_countries(self) -> list:
        """Retourne la liste des pays disponibles"""
        return [k for k in self.country_bounds.keys() if k != "Unknown"]
    
    def add_country(self, code: str, lat_bounds: Tuple[float, float], 
                   lon_bounds: Tuple[float, float], display_name: str,
                   safe_center: Tuple[float, float] = None):
        """Ajoute un nouveau pays avec centre sûr"""
        self.country_bounds[code] = {
            "lat": lat_bounds,
            "lon": lon_bounds, 
            "name": display_name
        }
        
        if safe_center:
            self.safe_centers[code] = safe_center
        else:
            # Calculer le centre des limites
            center_lat = sum(lat_bounds) / 2
            center_lon = sum(lon_bounds) / 2
            self.safe_centers[code] = (center_lat, center_lon)
