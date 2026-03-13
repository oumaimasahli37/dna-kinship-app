# app.py - Version modifiée sans coordonnées GPS obligatoires

import streamlit as st
import pandas as pd
import base64
import os
import time

# Configuration de base
st.set_page_config(
    page_title="DNA KINSHIP", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fonction pour le background
def set_background(image_file):
    """Applique un background image ou gradient"""
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        bg_style = f'url("data:image/jpg;base64,{b64}")'
    else:
        # Gradient par défaut si pas d'image
        bg_style = 'linear-gradient(-45deg, #0f1419, #1a202c, #2d3748, #1a365d)'
    
    st.markdown(f"""
    <style>
    .stApp {{
        background: {bg_style};
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }}
    
    /* Overlay semi-transparent pour améliorer la lisibilité */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 20, 25, 0.7);
        z-index: -1;
    }}

    .main-title {{
        font-family: 'Arial Black', Arial, sans-serif;
        font-size: 4rem;
        color: #00d4ff;
        text-align: center;
        margin: 3rem 0;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.8), 0 0 40px rgba(0, 212, 255, 0.5);
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 50%, #00ffaa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .subtitle {{
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 3rem;
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.8);
    }}

    .upload-section {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        backdrop-filter: blur(20px);
        padding: 3rem;
        margin: 2rem auto;
        max-width: 700px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }}

    .upload-title {{
        color: #00d4ff;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    }}

    .upload-description {{
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.2rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }}

    .success-message {{
        background: linear-gradient(135deg, rgba(0, 255, 150, 0.2) 0%, rgba(0, 200, 120, 0.1) 100%);
        border: 2px solid #00ff96;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #00ff96;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 255, 150, 0.2);
    }}

    .error-message {{
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2) 0%, rgba(200, 0, 0, 0.1) 100%);
        border: 2px solid #ff4444;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #ff4444;
        text-align: center;
        box-shadow: 0 10px 30px rgba(255, 0, 0, 0.2);
    }}

    .info-section {{
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        backdrop-filter: blur(15px);
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    }}

    .info-title {{
        color: #00d4ff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }}

    .info-list {{
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        line-height: 1.8;
    }}

    .info-list li {{
        margin-bottom: 0.8rem;
        padding-left: 1rem;
    }}

    .info-list strong {{
        color: #00ffaa;
        text-shadow: 0 0 5px rgba(0, 255, 170, 0.3);
    }}

    .footer {{
        text-align: center;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.6);
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* Responsive */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2.5rem;
        }}
        
        .upload-section {{
            padding: 2rem 1.5rem;
            margin: 1rem;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def check_system_requirements():
    """Vérifie que tout est en place pour la navigation"""
    checks = {
        "pages_folder": os.path.exists("pages"),
        "target_file": os.path.exists("pages/1_🌍_CarteADN.py"),
        "write_permissions": True
    }
    
    # Test des permissions d'écriture
    try:
        with open("test_write.tmp", "w") as f:
            f.write("test")
        os.remove("test_write.tmp")
    except:
        checks["write_permissions"] = False
    
    return checks

def main():
    # Nettoyer les anciens fichiers temporaires
    temp_files = ["temp_uploaded.csv", "kinship_analysis_done.flag", "navigation_status.txt"]
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass  # Ignorer les erreurs de suppression
    
    # Appliquer le background
    set_background("myfond.jpg")
    
    # Logo si disponible
    logo_html = ""
    if os.path.exists("mylogo.jpg"):
        with open("mylogo.jpg", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        logo_html = f'<img src="data:image/jpg;base64,{b64}" width="120" style="border-radius: 50%; margin-bottom: 2rem; box-shadow: 0 0 30px rgba(0, 212, 255, 0.5);"/><br>'
    
    # Header principal
    st.markdown(f"""
    <div style="text-align: center; margin-top: 2rem;">
        {logo_html}
        <h1 class="main-title">DNA KINSHIP</h1>
    </div>
    """, unsafe_allow_html=True)

    # Vérification système
    system_checks = check_system_requirements()
    
    if not system_checks["pages_folder"]:
        st.error("Dossier 'pages' manquant. Création en cours...")
        os.makedirs("pages")
        st.rerun()
    
    if not system_checks["target_file"]:
        st.error("Fichier 'pages/1_🌍_CarteADN.py' manquant. Veuillez le créer avec le code fourni.")
        return
    
    if not system_checks["write_permissions"]:
        st.error("Problème de permissions d'écriture dans le dossier.")
        return

    # Section upload
    st.markdown("""
    <div class="upload-section">
        <h2 class="upload-title">Analysez votre ADN</h2>
        <p class="upload-description">
            Analysez vos données génétiques pour identifier vos origines et relations familiales
        </p>
    """, unsafe_allow_html=True)

    # Upload du fichier
    uploaded_file = st.file_uploader(
        "Choisissez votre fichier CSV", 
        type="csv",
        help="Format requis: ID, SNP_Vector (les coordonnées seront générées automatiquement)",
        label_visibility="collapsed"
    )

    if uploaded_file:
        try:
            # Lire le fichier
            df = pd.read_csv(uploaded_file)
            
            # Validation simplifiée - plus besoin de Latitude/Longitude
            required_cols = ["SNP_Vector", "ID"]
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.markdown(f"""
                <div class="error-message">
                    <h3>Colonnes manquantes</h3>
                    <p>Les colonnes suivantes sont requises : {', '.join(missing_cols)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Vérifications détaillées
                valid_file = True
                error_messages = []
                
                # Vérifier les IDs uniques
                if df["ID"].duplicated().any():
                    error_messages.append("Des IDs dupliqués ont été détectés")
                    valid_file = False
                
                # Vérifier la longueur des SNP
                snp_lengths = df["SNP_Vector"].apply(len)
                if not all(snp_lengths == 1000):
                    invalid_snp_count = sum(snp_lengths != 1000)
                    error_messages.append(f"{invalid_snp_count} vecteurs SNP n'ont pas exactement 1000 positions")
                    valid_file = False
                
                # Vérifier les caractères SNP
                if valid_file:
                    all_snps = ''.join(df["SNP_Vector"].tolist())
                    invalid_chars = set(all_snps) - set('ATCG')
                    if invalid_chars:
                        error_messages.append(f"Caractères invalides détectés : {invalid_chars}")
                        valid_file = False
                
                if not valid_file:
                    for error in error_messages:
                        st.markdown(f"""
                        <div class="error-message">
                            <h3>Erreur de validation</h3>
                            <p>{error}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Fichier valide
                    st.markdown(f"""
                    <div class="success-message">
                        <h3>Fichier validé avec succès</h3>
                        <p><strong>{len(df)} individus</strong> détectés et prêts pour l'analyse génétique</p>
                        <p>Données validées • Coordonnées automatiques • Prêt pour l'analyse des origines</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # SECTION NAVIGATION CORRIGÉE
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        # Initialiser session state si nécessaire
                        if 'data_uploaded' not in st.session_state:
                            st.session_state.data_uploaded = False
                        
                        analyze_clicked = st.button(
                            "🚀 ANALYSER LES ORIGINES GÉNÉTIQUES", 
                            use_container_width=True,
                            type="primary",
                            key="analyze_origins_btn"
                        )
                        
                        if analyze_clicked:
                            # Vérifications système
                            target_file = "pages/1_🌍_CarteADN.py"
                            
                            if not os.path.exists(target_file):
                                st.error(f"Fichier manquant: {target_file}")
                                st.info("Assurez-vous que le fichier existe dans le dossier 'pages'")
                                st.stop()
                            
                            # Sauvegarder les données
                            try:
                                # Sauvegarder sur disque
                                df.to_csv("temp_uploaded.csv", index=False)
                                
                                # Sauvegarder dans session state comme backup
                                st.session_state.uploaded_data = df.to_dict('records')
                                st.session_state.data_uploaded = True
                                
                                # Message de confirmation
                                st.success("Données sauvegardées avec succès")
                                
                                # Navigation directe SANS rerun
                                st.switch_page(target_file)
                                
                            except Exception as e:
                                st.error(f"Erreur lors de la sauvegarde : {e}")
                                st.stop()
        
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                <h3>Erreur de lecture</h3>
                <p>Impossible de lire le fichier : {str(e)}</p>
                <p>Vérifiez que le fichier est au format CSV valide</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Informations sur le format
    st.markdown("""
    <div class="info-section">
        <h3 class="info-title">Format de fichier requis</h3>
        <ul class="info-list">
            <li><strong>ID</strong> : Identifiant unique pour chaque individu (ex: PERSON_001, INDIV_A23)</li>
            <li><strong>SNP_Vector</strong> : Séquence de 1000 positions génétiques utilisant les bases A, T, C, G</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Exemple de données
    st.markdown("""
    <div class="info-section">
        <h3 class="info-title">Exemple de données</h3>
        <p style="color: rgba(255, 255, 255, 0.8); margin-bottom: 1rem;">
            Voici un exemple du format attendu (coordonnées générées automatiquement) :
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    example_data = pd.DataFrame({
        'ID': ['PERSON_001', 'PERSON_002', 'PERSON_003'],
        'SNP_Vector': ['A' * 100 + 'T' * 900, 'G' * 200 + 'C' * 800, 'A' * 300 + 'G' * 700]
    })
    
    # Tronquer les SNP pour l'affichage
    example_display = example_data.copy()
    example_display['SNP_Vector'] = example_display['SNP_Vector'].apply(lambda x: x[:20] + "..." + x[-10:])
    st.dataframe(example_display, use_container_width=True, hide_index=True)

    # Section diagnostic (temporaire pour debug)
    with st.expander("🔧 Diagnostic système"):
        st.write("**Vérifications système :**")
        
        checks = check_system_requirements()
        for check_name, status in checks.items():
            if status:
                st.write(f"✅ {check_name}")
            else:
                st.write(f"❌ {check_name}")
        
        st.write("**Fichiers présents :**")
        if os.path.exists("pages"):
            files_in_pages = os.listdir("pages")
            st.write(f"Dans 'pages/': {files_in_pages}")
        else:
            st.write("Dossier 'pages' n'existe pas")
        
        st.write("**Session State :**")
        st.write(dict(st.session_state))

    # Footer
    st.markdown("""
    <div class="footer">
     <p><strong>DNA KINSHIP</strong> • Analyse génétique</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
