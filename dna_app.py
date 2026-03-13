import pandas as pd
import joblib
from Bio import SeqIO
import streamlit as st
import base64
import io
import os
from collections import Counter

# --------- CONFIGURATION PAGE ---------
st.set_page_config(page_title="DNAKin", layout="wide")

# --------- Récupérer le base64 de l'image ---------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Charger images (ajuste les chemins si besoin)
background_base64 = get_base64_image("myfond.jpg")
logo_base64 = get_base64_image("mylogo.jpg")

# Appliquer le CSS avec l'image de fond et le logo
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpeg;base64,{background_base64}');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .reportview-container .markdown-text-container {{
        font-family: 'Segoe UI', sans-serif;
        padding: 1rem;
    }}
    h1, h4 {{
        text-align: center;
    }}
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}
    .logo-container img {{
        height: 80px;
    }}
    </style>
""", unsafe_allow_html=True)

# Afficher le logo centré
st.markdown(f"<div class='logo-container'><img src='data:image/jpeg;base64,{logo_base64}' /></div>", unsafe_allow_html=True)

# Titre et sous-titre
st.markdown("<h1 style='text-align: center;'>DNAKin</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Analyse génétique & détection de population ethnique</h4>", unsafe_allow_html=True)
st.markdown("---")

# --------- CHARGEMENT DU MODÈLE, LABEL ENCODER ET K-MERS ---------
@st.cache_resource
def load_model_objects():
    model_path = os.path.join("1000genomes", "model.pkl")
    label_encoder_path = os.path.join("1000genomes", "label_encoder.pkl")
    all_kmers_path = os.path.join("1000genomes", "all_kmers.pkl")

    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)
    all_kmers = joblib.load(all_kmers_path)
    
    return model, label_encoder, all_kmers

model, label_encoder, all_kmers = load_model_objects()

# --------- FONCTIONS ---------
def extract_kmers(sequence, k=6):
    return [sequence[i:i+k] for i in range(len(sequence) - k + 1)]

# Mise à jour de la fonction featurize pour utiliser Counter
def featurize(sequence, all_kmers, k=6):
    kmers = extract_kmers(sequence.upper(), k)
    kmer_counts = Counter(kmers)
    # Créer un vecteur de longueur len(all_kmers), avec les valeurs correspondant aux k-mers
    # Si un k-mer n'est pas trouvé, sa fréquence est 0
    return [kmer_counts.get(kmer, 0) for kmer in all_kmers]

# --------- INTERFACE UPLOAD ---------
st.markdown("### 📤 Upload de vos séquences ADN (fichier FASTA multi-séquences possible)")
uploaded_file = st.file_uploader("", type=["fasta", "fa", "txt"])
submit = st.button("🔍 Téléverser et Analyser")

# --------- ANALYSE ETHNICITÉ ---------
if uploaded_file and submit:
    try:
        # Lire le fichier FASTA téléchargé
        file_contents = uploaded_file.getvalue().decode("utf-8")
        file_io = io.StringIO(file_contents)
        records = list(SeqIO.parse(file_io, "fasta"))

        if not records:
            st.error("❌ Aucun enregistrement FASTA trouvé.")
        else:
            st.success(f"✅ {len(records)} séquence(s) chargée(s) avec succès.")

            # Pour chaque séquence dans le fichier FASTA, faire la prédiction
            for idx, record in enumerate(records, 1):
                sequence = str(record.seq).upper()
                st.markdown(f"#### Séquence {idx} - ID: {record.id}")
                st.code(sequence[:100] + ("..." if len(sequence) > 100 else ""), language="plaintext")

                # Featurize & prédiction
                X_input = featurize(sequence, all_kmers)
                prediction_encoded = model.predict([X_input])[0]
                prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

                st.markdown(f"🌍 **Origine ethnique prédite** : <span style='color:green; font-weight:bold;'>{prediction_label}</span>", unsafe_allow_html=True)
            st.markdown("---")

    except Exception as e:
        st.error(f"❌ Erreur lors de la prédiction : {e}")

# --------- FOOTER ---------
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>🔒 Données 100% anonymisées et sécurisées.</p>", unsafe_allow_html=True)

