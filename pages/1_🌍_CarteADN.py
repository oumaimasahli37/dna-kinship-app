# pages/1_🌍_CarteADN.py - Module principal avec cartes optimisées
import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import random

# Import des modules personnalisés
try:
    from genetic_analyzer import GeneticAnalyzer, KinshipAnalyzer
    from coordinate_generator import CoordinateGenerator
    from map_visualizer import MapVisualizer
except ImportError:
    st.error("⚠️ Modules manquants. Assurez-vous que tous les fichiers Python sont présents dans le même dossier.")
    st.stop()

st.set_page_config(
    page_title="Carte ADN - Origines", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# CSS optimisé pour les cartes
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #0f1419, #1a202c, #2d3748, #1a365d);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    color: white;
}

@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.results-header {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 150, 255, 0.08) 100%);
    border-radius: 25px;
    border: 2px solid rgba(0, 212, 255, 0.3);
    padding: 2rem;
    text-align: center;
    margin-bottom: 2rem;
    backdrop-filter: blur(20px);
}

.results-title {
    font-size: 2.5rem;
    color: #00d4ff;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.8);
}

.metric-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.04) 100%);
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(15px);
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
    color: #00d4ff;
    margin-bottom: 0.5rem;
}

.metric-label {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.85rem;
    text-transform: uppercase;
}

.section-container {
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.03) 100%);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(15px);
}

.section-title {
    color: #00d4ff;
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
    border-bottom: 2px solid rgba(0, 212, 255, 0.4);
    padding-bottom: 0.5rem;
}

.phase-indicator {
    background: linear-gradient(135deg, rgba(0, 255, 150, 0.15) 0%, rgba(0, 200, 120, 0.08) 100%);
    border-radius: 20px;
    border: 2px solid rgba(0, 255, 150, 0.3);
    padding: 1.5rem;
    text-align: center;
    margin-bottom: 2rem;
}

.kinship-phase {
    background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(255, 71, 87, 0.08) 100%);
    border-radius: 20px;
    border: 2px solid rgba(255, 107, 107, 0.3);
    padding: 1.5rem;
    text-align: center;
    margin: 1.5rem 0;
}

.success-message {
    background: linear-gradient(135deg, rgba(0, 255, 150, 0.2) 0%, rgba(0, 200, 120, 0.1) 100%);
    border: 2px solid #00ff96;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #00ff96;
    text-align: center;
}

.warning-message {
    background: linear-gradient(135deg, rgba(255, 200, 0, 0.2) 0%, rgba(255, 150, 0, 0.1) 100%);
    border: 2px solid #ffc800;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #ffc800;
    text-align: center;
}

/* Optimisation pour les cartes Plotly */
.js-plotly-plot .plotly .modebar {
    background: rgba(0,0,0,0.8) !important;
}

.js-plotly-plot .plotly .modebar .modebar-btn {
    color: white !important;
}

/* Container de cartes avec hauteur fixe */
.map-container {
    height: 700px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

def analyze_origins_batch(df: pd.DataFrame, genetic_analyzer: GeneticAnalyzer, coord_gen: CoordinateGenerator):
    """Analyse les origines avec génération de coordonnées optimisée"""
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Fixer la seed pour la reproductibilité
    random.seed(42)
    
    for idx, row in df.iterrows():
        progress = (idx + 1) / len(df)
        progress_bar.progress(progress)
        status_text.text(f"🧬 Analyse de {row['ID']}... ({idx + 1}/{len(df)})")
        
        # Prédire l'origine
        country, confidence, analysis_status = genetic_analyzer.predict_origin(row['SNP_Vector'])
        
        # Générer les coordonnées sécurisées
        lat, lon, country_name = coord_gen.generate_safe_coordinates(country)
        
        results.append({
            'ID': row['ID'],
            'SNP_Vector': row['SNP_Vector'],
            'Predicted_Origin': country,
            'Origin_Confidence': confidence,
            'Generated_Latitude': lat,
            'Generated_Longitude': lon,
            'Country_Name': country_name,
            'Analysis_Status': analysis_status
        })
    
    progress_bar.empty()
    status_text.empty()
    
    return pd.DataFrame(results)

@st.cache_data
def load_and_process_data():
    """Cache pour éviter de recharger les données"""
    if not os.path.exists("temp_uploaded.csv"):
        return None
    return pd.read_csv("temp_uploaded.csv")

def main():
    # Header
    st.markdown("""
    <div class="results-header">
        <h1 class="results-title"> ANALYSE GÉNÉTIQUE DNA KINSHIP</h1>
        <p style="color: rgba(255, 255, 255, 0.8); font-size: 1.1rem;">
            Prédiction d'origines • Génération de coordonnées • Relations familiales
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Charger les données avec cache
    df = load_and_process_data()
    if df is None:
        st.markdown("""
        <div class="warning-message">
            <h3>⬅️ Aucune donnée trouvée</h3>
            <p>Veuillez d'abord uploader un fichier depuis la page d'accueil</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(" Retour à l'accueil", use_container_width=True):
            st.switch_page("app.py")
        return
    
    # Initialiser les analyseurs
    genetic_analyzer = GeneticAnalyzer()
    kinship_analyzer = KinshipAnalyzer()
    coord_generator = CoordinateGenerator()
    visualizer = MapVisualizer()
    
    # Configuration sidebar optimisée
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        max_individuals = st.number_input(
            "Limite d'individus", 
            min_value=2, 
            max_value=min(50, len(df)), 
            value=min(20, len(df)),
            help="Limite recommandée pour des performances optimales"
        )
        
        st.markdown("###  Paramètres avancés")
        
        map_zoom = st.selectbox(
            "Niveau de zoom initial",
            ["Automatique", "Monde entier", "Continents", "Pays", "Régions"],
            index=0
        )
        
        kinship_threshold = st.slider(
            "Seuil relations familiales", 
            0.01, 0.3, 0.03, 0.01,
            help="Coefficient minimum pour détecter une relation"
        )
        
        show_connections = st.checkbox(
            "Afficher les connexions", 
            value=True,
            help="Afficher les lignes entre individus apparentés"
        )
        
        st.markdown("###  Statistiques")
        st.metric(" Individus totaux", len(df))
        
        if len(df) > 1:
            total_pairs = len(df) * (len(df) - 1) // 2
            st.metric("🔗 Paires possibles", f"{total_pairs:,}")
        
        st.markdown("---")
        if st.button("🔄 Réinitialiser tout", help="Efface toutes les données et analyses"):
            for temp_file in ["temp_uploaded.csv", "kinship_done.flag", "temp_relationships.csv"]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            st.cache_data.clear()
            st.rerun()
    
    # Limiter les données si nécessaire
    if len(df) > max_individuals:
        df = df.sample(n=max_individuals, random_state=42).reset_index(drop=True)
        st.info(f" Analyse limitée à {max_individuals} individus pour des performances optimales")
    
    # PHASE 1: ANALYSE DES ORIGINES
    st.markdown("""
    <div class="phase-indicator">
        <h2 style="color: #00ff96; margin: 0; font-size: 1.5rem;">PHASE 1: PRÉDICTION DES ORIGINES</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyser les origines avec spinner optimisé
    with st.spinner(" Analyse des signatures génétiques en cours..."):
        df_analyzed = analyze_origins_batch(df, genetic_analyzer, coord_generator)
    
    # Validation des données
    if df_analyzed.empty or 'Generated_Latitude' not in df_analyzed.columns:
        st.error("❌ Erreur dans l'analyse des données")
        return
    
    # Métriques compactes
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df_analyzed)}</div>
            <div class="metric-label">Individus</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        unique_countries = df_analyzed["Country_Name"].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{unique_countries}</div>
            <div class="metric-label">Pays</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_confidence = df_analyzed["Origin_Confidence"].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_confidence:.2f}</div>
            <div class="metric-label">Confiance</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        high_conf = len(df_analyzed[df_analyzed["Origin_Confidence"] > 0.8])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{high_conf}</div>
            <div class="metric-label">Haute Conf.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Affichage des résultats avec cartes optimisées
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">️ Carte des origines génétiques</h3>', unsafe_allow_html=True)
        
        try:
            fig_origins = visualizer.create_origins_map(df_analyzed)
            
            # Configuration Plotly optimisée
            config = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                'responsive': True
            }
            
            st.plotly_chart(
                fig_origins, 
                use_container_width=True, 
                config=config,
                key="origins_map"
            )
            
        except Exception as e:
            st.warning(f"Erreur avec la carte principale: {e}")
            st.info("Utilisation d'une carte simplifiée...")
            
            try:
                # Fallback vers une carte simplifiée
                fig_simple = visualizer.create_simple_scatter_map(df_analyzed)
                st.plotly_chart(fig_simple, use_container_width=True, key="origins_map_simple")
            except Exception as e2:
                st.error(f"Erreur d'affichage de la carte: {e2}")
                st.info("Réduisez le nombre d'individus dans les paramètres")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title"> Résultats détaillés</h3>', unsafe_allow_html=True)
        
        # Tableau compact des résultats
        display_df = df_analyzed[["ID", "Country_Name", "Origin_Confidence"]].copy()
        display_df["Origin_Confidence"] = display_df["Origin_Confidence"].round(3)
        display_df = display_df.rename(columns={
            "Country_Name": "Pays", 
            "Origin_Confidence": "Confiance"
        })
        
        st.dataframe(
            display_df, 
            use_container_width=True, 
            hide_index=True,
            height=300
        )
        
        # Graphique des pays si plusieurs origines
        if unique_countries > 1:
            try:
                charts = visualizer.create_statistics_charts(df_analyzed)
                if 'origins_pie' in charts:
                    st.plotly_chart(
                        charts['origins_pie'], 
                        use_container_width=True,
                        key="origins_chart"
                    )
            except Exception as e:
                st.warning(f"Graphique non disponible: {e}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # PHASE 2: RELATIONS FAMILIALES
    st.markdown("---")
    st.markdown("""
    <div class="kinship-phase">
        <h2 style="color: #ff6b6b; margin: 0; font-size: 1.5rem;">PHASE 2: ANALYSE DES RELATIONS FAMILIALES</h2>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255, 255, 255, 0.8);">
            Recherche des liens de parenté entre individus (optionnel)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Gestion des relations familiales
    kinship_done = os.path.exists("kinship_done.flag")
    
    if not kinship_done:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("‍👧 LANCER L'ANALYSE DES RELATIONS", 
                        use_container_width=True, 
                        type="secondary"):
                
                with st.spinner("🔍 Recherche des relations familiales..."):
                    relationships = kinship_analyzer.analyze_relationships(df_analyzed, kinship_threshold)
                
                if relationships:
                    # Sauvegarder les résultats
                    pd.DataFrame(relationships).to_csv("temp_relationships.csv", index=False)
                    
                    with open("kinship_done.flag", "w") as f:
                        f.write(f"done_{time.time()}")
                    
                    st.success(f"✅ {len(relationships)} relations familiales détectées!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("⚠️ Aucune relation familiale significative détectée avec ce seuil")
                    st.info(" Essayez de réduire le seuil dans les paramètres")
    
    else:
        # Charger et afficher les résultats des relations
        try:
            relationships_df = pd.read_csv("temp_relationships.csv")
            relationships = relationships_df.to_dict('records')
            
            st.markdown(f"""
            <div class="success-message">
                <h3>✅ Relations familiales analysées</h3>
                <p><strong>{len(relationships)}</strong> relations identifiées sur la carte</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Carte avec relations familiales
            st.markdown('<div class="section-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="section-title">🔗 Carte avec liens familiaux</h3>', unsafe_allow_html=True)
            
            try:
                if show_connections:
                    fig_kinship = visualizer.create_kinship_map(df_analyzed, relationships)
                else:
                    fig_kinship = visualizer.create_origins_map(df_analyzed)
                
                config = {
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
                    'responsive': True
                }
                
                st.plotly_chart(
                    fig_kinship, 
                    use_container_width=True, 
                    config=config,
                    key="kinship_map"
                )
                
            except Exception as e:
                st.error(f"❌ Erreur d'affichage de la carte des relations: {e}")
                # Afficher la carte des origines en fallback
                st.plotly_chart(visualizer.create_origins_map(df_analyzed), use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Détails des relations en colonnes
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="section-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="section-title"> Relations détaillées</h3>', unsafe_allow_html=True)
                
                # Tableau des relations
                relations_display = relationships_df[['ID1', 'ID2', 'Relation', 'Coefficient']].copy()
                relations_display = relations_display.sort_values('Coefficient', ascending=False)
                relations_display['Coefficient'] = relations_display['Coefficient'].round(4)
                
                st.dataframe(
                    relations_display, 
                    use_container_width=True, 
                    hide_index=True,
                    height=300
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="section-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="section-title"> Statistiques relations</h3>', unsafe_allow_html=True)
                
                # Métriques des relations
                st.metric(" Relations totales", len(relationships))
                st.metric("️ Types différents", relationships_df['Relation'].nunique())
                st.metric(" Coefficient max", f"{relationships_df['Coefficient'].max():.4f}")
                
                # Graphique des types de relations
                try:
                    charts = visualizer.create_statistics_charts(df_analyzed, relationships)
                    if 'relations_bar' in charts:
                        st.plotly_chart(
                            charts['relations_bar'], 
                            use_container_width=True,
                            key="relations_chart"
                        )
                except Exception as e:
                    st.info("Graphique des relations non disponible")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Option pour refaire l'analyse
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 REFAIRE L'ANALYSE DES RELATIONS", 
                            use_container_width=True,
                            help="Relancer avec de nouveaux paramètres"):
                    os.remove("kinship_done.flag")
                    if os.path.exists("temp_relationships.csv"):
                        os.remove("temp_relationships.csv")
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement des relations: {e}")
            # Nettoyer les fichiers corrompus
            for temp_file in ["kinship_done.flag", "temp_relationships.csv"]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            st.info("Fichiers corrompus nettoyés. Relancez l'analyse.")
    
    # Section export et téléchargements
    st.markdown("---")
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title"> Exporter les résultats</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export données d'origines
        origins_export = df_analyzed[[
            "ID", "Country_Name", "Predicted_Origin", 
            "Generated_Latitude", "Generated_Longitude", "Origin_Confidence"
        ]].copy()
        origins_csv = origins_export.to_csv(index=False)
        
        st.download_button(
            " Origines ",
            origins_csv,
            "origines_genetiques.csv",
            "text/csv",
            use_container_width=True,
            help="Télécharger les origines prédites avec coordonnées"
        )
    
    with col2:
        # Export relations si disponible
        if kinship_done and os.path.exists("temp_relationships.csv"):
            try:
                relations_csv = pd.read_csv("temp_relationships.csv").to_csv(index=False)
                st.download_button(
                    " Relations familiales",
                    relations_csv,
                    "relations_familiales.csv",
                    "text/csv",
                    use_container_width=True,
                    help="Télécharger les relations détectées"
                )
            except:
                st.info("Relations non disponibles")
        else:
            st.info("Relations non encore analysées")
    
    with col3:
        # Rapport complet
        report_content = f"""# RAPPORT ANALYSE DNA KINSHIP

## INFORMATIONS GÉNÉRALES
- Date d'analyse: {time.strftime("%Y-%m-%d %H:%M:%S")}
- Individus analysés: {len(df_analyzed)}
- Pays détectés: {df_analyzed['Country_Name'].nunique()}
- Confiance moyenne: {df_analyzed['Origin_Confidence'].mean():.3f}

## ORIGINES PRÉDITES
"""
        
        # Détails par individu
        for _, row in df_analyzed.iterrows():
            report_content += f"""- {row['ID']}: {row['Country_Name']} 
  * Origine: {row['Predicted_Origin']}
  * Confiance: {row['Origin_Confidence']:.3f}
  * Coordonnées: {row['Generated_Latitude']:.3f}, {row['Generated_Longitude']:.3f}
"""
        
        # Répartition par pays
        report_content += f"\n## RÉPARTITION PAR PAYS\n"
        country_counts = df_analyzed["Country_Name"].value_counts()
        for country, count in country_counts.items():
            percentage = (count / len(df_analyzed)) * 100
            report_content += f"- {country}: {count} individus ({percentage:.1f}%)\n"
        
        # Relations si disponibles
        if kinship_done and os.path.exists("temp_relationships.csv"):
            try:
                relationships_df = pd.read_csv("temp_relationships.csv")
                report_content += f"""
## RELATIONS FAMILIALES
- Nombre total: {len(relationships_df)}
- Types différents: {relationships_df['Relation'].nunique()}
- Coefficient le plus élevé: {relationships_df['Coefficient'].max():.4f}

### DÉTAIL DES RELATIONS
"""
                for _, rel in relationships_df.iterrows():
                    report_content += f"- {rel['ID1']} ↔ {rel['ID2']}: {rel['Relation']} (coefficient: {rel['Coefficient']:.4f})\n"
            except:
                report_content += "\n## RELATIONS FAMILIALES\nErreur dans les données de relations\n"
        else:
            report_content += "\n## RELATIONS FAMILIALES\nNon analysées dans cette session\n"
        
        report_content += f"""
## NOTES TECHNIQUES
- Coordonnées générées automatiquement selon limites géographiques réelles
- Prédiction basée sur composition A/T/C/G des vecteurs SNP
- Relations calculées avec facteur de distance géographique
- Algorithme: signatures génétiques par population + génération coordonnées
"""
        
        st.download_button(
            " Rapport complet",
            report_content,
            "rapport_analyse_complete.txt",
            "text/plain",
            use_container_width=True,
            help="Rapport détaillé de l'analyse"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Informations techniques
    with st.expander("ℹ️ Informations sur l'analyse"):
        st.markdown("""
        **Méthode de prédiction des origines:**
        - Analyse de la composition des bases A, T, C, G dans les vecteurs SNP
        - Comparaison avec signatures génétiques de 6 populations principales
        - Génération de coordonnées réalistes dans les limites géographiques du pays prédit
        
        **Analyse des relations familiales:**
        - Calcul de similarité génétique (IBS - Identity By State)
        - Facteur de correction basé sur la distance géographique
        - Classification en 10 types de relations avec seuils spécifiques
        
        **Visualisation cartographique:**
        - Points colorés par pays d'origine sur carte mondiale
        - Lignes reliant les individus apparentés (épaisseur = force de la relation)
        - Zoom automatique selon la dispersion géographique des données
        """)
    
    # Navigation finale
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(" NOUVELLE ANALYSE", 
                    use_container_width=True, 
                    type="primary",
                    help="Retour à l'accueil pour analyser de nouvelles données"):
            
            # Nettoyage complet
            temp_files = [
                "temp_uploaded.csv", 
                "kinship_done.flag", 
                "temp_relationships.csv"
            ]
            
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            
            # Clear cache et session state
            st.cache_data.clear()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            st.switch_page("app.py")

if __name__ == "__main__":
    main()
