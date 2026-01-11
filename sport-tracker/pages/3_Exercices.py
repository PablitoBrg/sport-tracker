import streamlit as st
import json
import os

st.set_page_config(page_title="Exercices / Charges", layout="centered")
st.title("🏋️ Exercices et charges habituelles")

DATA_PATH = "data/exercises.json"

# --- Charger les charges existantes ---
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        charges = json.load(f)
else:
    charges = {}

# --- EXERCICES AVEC SOUS-CATÉGORIES ---
EXERCISES = {
    "Pectoraux": {
        "Développé couché": ["Haltères", "Barre", "Smith"],
        "Développé incliné": ["Haltères", "Barre", "Smith"],
        "Écarté": ["Haltères", "Poulie"]
    },
    "Biceps": {
        "Curl barre": [],
        "Curl haltère": [],
        "Curl marteau": [],
        "Curl marteau poulie": [],
        "Curl incliné": [],
    },
    "Triceps": {
        "Overhead poulie": [],
        "Overhead smith": [],
        "Triceps Extension": [],
        "Développé couché smith": [],
    },
    "Abdos": {
        "Crunch Poulie": [],
        "Hypercrunch": [],
    },
    "Legz": {
        "Leg Press Sissy": [],
        "Leg Extension": [],
        "Leg Curl": [],
        "Jefferson Curl": [],
        "RDL": ["Barre", "Halteres", "Smith"],
        "Hip Trust": ["Unilateral", "Machine", "Barre"],
        "Deadlift Snatch" : [],
        "Abduction" : [],
        "Adduction": [],

    },
    "Epaules": {
        "Elévations Latérales": ["Poulie", "Halteres", "Machine"],
        "Elévations Frontales": [],
        "Face pull": [],
        "Elévations SOS": [],
        "Développe militaire": ["Barre", "Halteres", "Kettlebell"],
    },

}


# --- Initialisation des charges ---
for muscle, exs in EXERCISES.items():
    if muscle not in charges:
        charges[muscle] = {}
    for ex_main, sub_exs in exs.items():
        # Si pas de sous-exercices, on transforme en dict avec clé "Standard"
        if not sub_exs:
            if not isinstance(charges[muscle].get(ex_main), dict):
                charges[muscle][ex_main] = {"Standard": charges[muscle].get(ex_main, 0)}
        else:
            if ex_main not in charges[muscle] or not isinstance(charges[muscle][ex_main], dict):
                charges[muscle][ex_main] = {sub: 0 for sub in sub_exs}


# --- UI ---
for muscle, exs in EXERCISES.items():
    with st.expander(muscle, expanded=False):
        for ex_main, sub_exs in exs.items():
            # Remplacer le deuxième expander par un container
            with st.container():
                st.markdown(f"**{ex_main}**")  # titre de l'exercice principal
                for sub in charges[muscle][ex_main]:
                    label = f"{sub} — charge habituelle (kg)" if sub != "Standard" else f"{ex_main} — charge habituelle (kg)"
                    val = st.number_input(
                        label=label,
                        min_value=0,
                        value=charges[muscle][ex_main][sub],
                        step=1,
                        key=f"{muscle}_{ex_main}_{sub}"
                    )
                    charges[muscle][ex_main][sub] = val



# --- Bouton Sauvegarde ---
if st.button("💾 Sauvegarder les charges"):
    with open(DATA_PATH, "w") as f:
        json.dump(charges, f, indent=2)
    st.success("Charges sauvegardées ✅")
