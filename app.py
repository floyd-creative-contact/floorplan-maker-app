import streamlit as st
from streamlit_drawable_canvas import st_canvas
import math

# ---------------------------
# 🔧 App Config
# ---------------------------
st.set_page_config(page_title="Celestial Library Map Tool", layout="wide")
st.title("📜 Celestial Library Floorplan Creator")

# ---------------------------
# 🧠 Session State Defaults
# ---------------------------
if "drawing_mode" not in st.session_state:
    st.session_state.drawing_mode = "line"
if "show_grid" not in st.session_state:
    st.session_state.show_grid = True

# ---------------------------
# 🎛️ Sidebar Controls
# ---------------------------
st.sidebar.header("Canvas Settings")
stroke_width = st.sidebar.slider("Stroke width", 1, 10, 2)
grid_size = st.sidebar.slider("Grid Size", 20, 100, 40)
bg_color = st.sidebar.color_picker("Canvas background", "#f0e6d2")
stroke_color = st.sidebar.color_picker("Stroke color", "#2f2f2f")
show_grid = st.sidebar.checkbox("Show Grid", value=st.session_state.show_grid)
st.session_state.show_grid = show_grid

# ---------------------------
# 🧰 Tool Selector
# ---------------------------
st.sidebar.markdown("### 🧰 Tools")
tool_cols = st.sidebar.columns(4)
tools = {
    "freedraw": "✏️",
    "line": "📏",
    "rect": "▭",
    "circle": "⚪",
    "transform": "🔧"
}
for i, (tool, icon) in enumerate(tools.items()):
    if tool_cols[i % 4].button(icon, help=f"{tool.title()} Tool"):
        st.session_state.drawing_mode = tool

# ---------------------------
# 📐 Canvas Area
# ---------------------------
canvas_width = 1000
canvas_height = 800

canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=True,
    height=canvas_height,
    width=canvas_width,
    drawing_mode=st.session_state.drawing_mode,
    key="canvas",
)

# ---------------------------
# 🔲 Grid Overlay
# ---------------------------
if st.session_state.show_grid:
    grid_html = f"<div style='position:absolute;top:0;left:0;width:{canvas_width}px;height:{canvas_height}px;z-index:1;'>"
    for x in range(0, canvas_width, grid_size):
        grid_html += f"<div style='position:absolute;top:0;left:{x}px;width:1px;height:{canvas_height}px;background:#ddd;opacity:0.5;'></div>"
    for y in range(0, canvas_height, grid_size):
        grid_html += f"<div style='position:absolute;top:{y}px;left:0;width:{canvas_width}px;height:1px;background:#ddd;opacity:0.5;'></div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

# ---------------------------
# 🧲 Snap-to-Grid Logic
# ---------------------------
def snap(val, grid):
    return grid * round(val / grid)

snapped_shapes = []
if canvas_result.json_data is not None:
    for obj in canvas_result.json_data["objects"]:
        shape_type = obj["type"]
        snapped_obj = obj.copy()

        if shape_type == "line":
            snapped_obj["x1"] = snap(obj["x1"], grid_size)
            snapped_obj["y1"] = snap(obj["y1"], grid_size)
            snapped_obj["x2"] = snap(obj["x2"], grid_size)
            snapped_obj["y2"] = snap(obj["y2"], grid_size)

        elif shape_type in {"rect", "circle"}:
            snapped_obj["left"] = snap(obj["left"], grid_size)
            snapped_obj["top"] = snap(obj["top"], grid_size)

        elif shape_type == "path":
            snapped_obj["path"] = [
                [p[0]] + [snap(p[1], grid_size), snap(p[2], grid_size)] for p in obj["path"]
            ]

        snapped_shapes.append(snapped_obj)

# ---------------------------
# 🧾 Shape Debug Output
# ---------------------------
with st.expander("📋 Snapped Shape Data"):
    st.json(snapped_shapes)

# ---------------------------
# 🧹 Toolbar Buttons
# ---------------------------
st.markdown("### ✨ Tools")
tool_cols = st.columns([1, 1, 1, 1])
with tool_cols[0]:
    st.button("🗑️", help="Clear all", on_click=lambda: st.rerun())
with tool_cols[1]:
    st.button("↩️", help="Undo (Coming Soon)")
with tool_cols[2]:
    st.button("↪️", help="Redo (Coming Soon)")
with tool_cols[3]:
    if st.button("📷", help="Download image"):
        st.warning("Image export coming soon (Streamlit does not yet support canvas PNG download).")

# TODO: Replace shape drawing with snapped versions (requires custom canvas)
