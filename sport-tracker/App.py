import streamlit as st
from config import MOVEMENTS, MUSCLE_TARGETS
from utils import load_current_week, increment_movement, reset_week
from utils import load_targets, save_targets
from utils import load_current_week, increment_movement, reset_week, increment_muscle



st.set_page_config(page_title="Sport Tracker", layout="centered")

st.title("🏋️ Sport Tracker")
data = load_current_week()
# Initialisation commune
if "movement_targets" not in st.session_state:
    st.session_state.movement_targets = {m: cfg["weekly_target"] for m, cfg in MOVEMENTS.items()}

if "muscle_targets" not in st.session_state:
    st.session_state.muscle_targets = MUSCLE_TARGETS.copy()

st.subheader("Mouvements")
for movement in st.session_state.movement_targets:  # <- ici movement est défini
    current = data["movements"][movement]
    target = st.session_state.movement_targets[movement]
    progress = min(current / target, 1.0)

    st.markdown(f"**{movement}** — {current} / {target}")
    st.progress(progress)

    if st.button(f"+1 série {movement}", key=f"move_{movement}"):
        increment_movement(movement)
        st.rerun()

st.subheader("Muscles")
for muscle in st.session_state.muscle_targets:  # <- muscle défini ici
    current = data["muscles"][muscle]
    target = st.session_state.muscle_targets[muscle]
    progress = min(current / target, 1.0)

    st.markdown(f"**{muscle}** — {current} / {target}")
    st.progress(progress)

    if st.button(f"+1 série {muscle}", key=f"muscle_{muscle}"):
        increment_muscle(muscle)
        st.rerun()

st.subheader("Mouvements")

st.divider()

if st.button("🔁 Reset semaine"):
    reset_week()
    st.success("Semaine sauvegardée et réinitialisée")
    st.rerun()
