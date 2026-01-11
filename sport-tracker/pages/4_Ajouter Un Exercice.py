import streamlit as st
import json
import os

st.set_page_config(page_title="Ajouter un exercice", layout="centered")
st.title("➕ Ajouter un exercice brut")

# --- Chemin fichier exercises.json ---
DATA_PATH = "data/exercises.json"

# --- Charger les exercices existants ---
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        exercises = json.load(f)
else:
    exercises = {}

# --- Choisir le groupe musculaire ---
muscle_list = list(exercises.keys())
muscle = st.selectbox("Choisir un groupe musculaire", options=muscle_list)

# --- Ajouter un exercice brut ---
new_exercise = st.text_input("Nom de l'exercice à ajouter")

# --- Bouton pour ajouter ---
if st.button("💾 Ajouter l'exercice"):
    if not new_exercise.strip():
        st.warning("Veuillez entrer un nom d'exercice valide !")
    else:
        # Ajouter l'exercice avec valeur initiale 0
        if new_exercise in exercises[muscle]:
            st.info(f"L'exercice '{new_exercise}' existe déjà dans {muscle}.")
        else:
            exercises[muscle][new_exercise] = 0  # juste un int
            # Sauvegarder
            with open(DATA_PATH, "w") as f:
                json.dump(exercises, f, indent=2)
            st.success(f"Exercice '{new_exercise}' ajouté à {muscle} ✅")
