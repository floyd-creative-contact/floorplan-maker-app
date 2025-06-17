import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🗺️ Celestial Library Floorplan Maker")

# Tool buttons (can be expanded later)
cols = st.columns([1, 1, 1, 5])
with cols[0]:
    st.button("➕ Add Line", on_click=lambda: st.session_state.update({"add_line": True}))
with cols[1]:
    st.button("📤 Export PNG", on_click=lambda: st.session_state.update({"export_png": True}))

# Embed the canvas HTML
with open("frontend/drawing.html", "r") as f:
    html = f.read()

components.html(html, height=750, scrolling=False)
