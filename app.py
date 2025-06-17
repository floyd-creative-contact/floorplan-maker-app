import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Celestial Library Map Tool", layout="wide")

st.title("📜 Celestial Library Floorplan Creator")

# Sidebar
st.sidebar.header("Canvas Settings")
stroke_width = st.sidebar.slider("Stroke width", 1, 10, 2)
grid_size = st.sidebar.slider("Grid Size", 20, 100, 40)
drawing_mode = st.sidebar.selectbox(
    "Drawing tool",
    ("freedraw", "line", "rect", "circle"),
)

bg_color = st.sidebar.color_picker("Canvas background", "#f0e6d2")
stroke_color = st.sidebar.color_picker("Stroke color", "#2f2f2f")

canvas_width = 1000
canvas_height = 800

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=True,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=drawing_mode,
    key="canvas",
)
