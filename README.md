# 🧬 DNA Kinship — Analyse Génétique & Carte des Origines

Application web interactive développée avec **Streamlit** pour analyser des données génétiques, identifier les origines ethniques d'individus et détecter les liens de parenté entre eux.

---

##  Fonctionnalités

-  **Analyse de vecteurs SNP** — traitement de séquences de 1000 positions génétiques (bases A, T, C, G)
- **Prédiction des origines ethniques** — classification parmi 6 populations :
  - Européen · Africain · Est-Asiatique · Sud-Asiatique · Moyen-Oriental · Américain mixte
- **Détection de liens de parenté** — identification des relations familiales entre individus
-  **Carte mondiale interactive** — visualisation géographique des origines avec clustering
- **Tableau de bord analytique** — métriques et graphiques de synthèse

---

##  Lancer l'application

### 1. Cloner le dépôt
```bash
git clone https://github.com/ton-utilisateur/dna-kinship.git
cd dna-kinship
```

### 2. Installer les dépendances
```bash
pip install streamlit pandas numpy scikit-learn folium
```

### 3. Lancer
```bash
streamlit run app.py
```

---

##  Structure du projet

```
dna-kinship/
├── app.py                        # Page d'accueil & upload
├── pages/
│   └── 1_🌍_CarteADN.py         # Page carte & résultats
├── genetic_analyzer.py           # Analyse SNP & prédiction d'origines
├── coordinate_generator.py       # Génération automatique de coordonnées
├── map_visualizer.py             # Visualisation sur carte Folium
├── kinship_model.pkl             # Modèle ML de parenté (pré-entraîné)
├── kinship_scaler.pkl            # Scaler associé au modèle
└── test_dna_kinship.csv          # Fichier de test
```

---

##  Format de données requis

Le fichier CSV d'entrée doit contenir exactement **deux colonnes** :

| Colonne | Description |
|---------|-------------|
| `ID` | Identifiant unique de l'individu (ex: `PERSON_001`) |
| `SNP_Vector` | Séquence de **1000 caractères** parmi `A`, `T`, `C`, `G` |

**Exemple :**
```
ID,SNP_Vector
PERSON_001,ATCGATCG...  (1000 caractères)
PERSON_002,GCTAGCTA...  (1000 caractères)
```

> Un fichier de test `test_dna_kinship.csv` est fourni pour tester l'application directement.

---

##  Stack technique

| Outil | Usage |
|-------|-------|
| Python 3.10+ | Langage principal |
| Streamlit | Interface web |
| Pandas / NumPy | Traitement des données |
| scikit-learn | Modèle de parenté (ML) |
| Folium | Carte interactive |


---
