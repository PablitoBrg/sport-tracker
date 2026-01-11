import streamlit as st
from config import MOVEMENTS, MUSCLE_TARGETS

st.set_page_config(page_title="Objectifs", layout="centered")

st.title("⚙️ Modifier les objectifs")

# Init si nécessaire
if "movement_targets" not in st.session_state:
    st.session_state.movement_targets = {
        m: cfg["weekly_target"] for m, cfg in MOVEMENTS.items()
    }

if "muscle_targets" not in st.session_state:
    st.session_state.muscle_targets = MUSCLE_TARGETS.copy()

st.subheader("🏋️ Objectifs par mouvement")

for movement in st.session_state.movement_targets:
    st.session_state.movement_targets[movement] = st.number_input(
        movement,
        min_value=0,
        value=st.session_state.movement_targets[movement],
        key=f"page_target_move_{movement}"
    )

st.divider()

st.subheader("💪 Objectifs par muscle")

for muscle in st.session_state.muscle_targets:
    st.session_state.muscle_targets[muscle] = st.number_input(
        muscle,
        min_value=0,
        value=st.session_state.muscle_targets[muscle],
        key=f"page_target_muscle_{muscle}"
    )

st.success("Les objectifs sont appliqués en temps réel ✅")
