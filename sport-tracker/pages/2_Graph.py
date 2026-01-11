import streamlit as st
import json
from utils import HISTORY_PATH, load_current_week
import pandas as pd
import plotly.express as px
# Historique des semaines
history = []
try:
    with open(HISTORY_PATH, "r") as f:
        content = f.read().strip()
        if content:
            history = json.loads(content)
except:
    history = []

# Ajouter la semaine en cours pour afficher la progression en temps réel
current_week = load_current_week()

history.append(current_week)
# Préparer les données mouvements
mvt_data = []
muscle_data = []

for i, week in enumerate(history, start=1):
    # Mouvements
    for mvt, val in week["movements"].items():
        mvt_data.append({"Semaine": i, "Mouvement": mvt, "Séries": val})
    # Muscles
    for muscle, val in week["muscles"].items():
        muscle_data.append({"Semaine": i, "Muscle": muscle, "Séries": val})

df_mvt = pd.DataFrame(mvt_data)
df_muscle = pd.DataFrame(muscle_data)

st.subheader("📈 Progression mouvements")
fig_mvt = px.bar(
    df_mvt,
    x="Semaine",
    y="Séries",
    color="Mouvement",
    barmode="group",
    title="Séries par mouvement par semaine"
)
st.plotly_chart(fig_mvt, use_container_width=True)
st.subheader("📊 Progression muscles")

# Filtre muscles
selected_muscles = st.multiselect(
    "Choisir muscles",
    options=df_muscle["Muscle"].unique(),
    default=list(df_muscle["Muscle"].unique())
)

# Appliquer le filtre
df_muscle_filtered = df_muscle[df_muscle["Muscle"].isin(selected_muscles)]

# Créer le graphique avec le DataFrame filtré
fig_muscle = px.bar(
    df_muscle_filtered,
    x="Semaine",
    y="Séries",
    color="Muscle",
    barmode="group",
    title="Séries par muscle par semaine"
)
st.plotly_chart(fig_muscle, use_container_width=True)
