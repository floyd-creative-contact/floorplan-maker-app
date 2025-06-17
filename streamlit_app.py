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

snap_to_grid = st.sidebar.checkbox("Snap to Grid", value=True)
show_grid = st.sidebar.checkbox("Show Grid", value=True)

with open("frontend/drawing.html", "r") as f:
    html = f.read()

# Inject tool and options into HTML via string replacements
html = html.replace("{{TOOL}}", tool)
html = html.replace("{{POLYGON_SIDES}}", str(polygon_sides or 5))
html = html.replace("{{SNAP_TO_GRID}}", "true" if snap_to_grid else "false")
html = html.replace("{{SHOW_GRID}}", "true" if show_grid else "false")

components.html(html, height=750, scrolling=False)
