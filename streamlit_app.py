import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🗺️ Map Making App")

# Tool selector
tool = st.sidebar.radio(
    "Select Tool",
    ["Line", "Rectangle", "Circle/Ellipse", "Arc", "Polygon"],
    help="Choose a drawing tool. Shapes are point-editable."
)

polygon_sides = None
if tool == "Polygon":
    polygon_sides = st.sidebar.slider("Polygon sides", min_value=3, max_value=12, value=5)

snap_to_grid = st.sidebar.toggle("Snap to Grid", value=True)
show_grid = st.sidebar.toggle("Show Grid", value=True)

# Load the canvas
with open("frontend/drawing.html", "r") as f:
    html = f.read()

components.html(html, height=750, scrolling=False)
