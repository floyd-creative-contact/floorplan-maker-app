import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Celestial Library Map Tool", layout="wide")
st.title("📜 Celestial Library Floorplan Creator")

# Initialize session state
if "drawing_mode" not in st.session_state:
    st.session_state.drawing_mode = "line"
if "show_grid" not in st.session_state:
    st.session_state.show_grid = True

# Sidebar: Canvas settings
st.sidebar.header("Canvas Settings")
stroke_width = st.sidebar.slider("Stroke width", 1, 10, 2)
grid_size = st.sidebar.slider("Grid Size", 20, 100, 40)
bg_color = st.sidebar.color_picker("Canvas background", "#f0e6d2")
stroke_color = st.sidebar.color_picker("Stroke color", "#2f2f2f")
show_grid = st.sidebar.checkbox("Show Grid", value=st.session_state.show_grid)

st.session_state.show_grid = show_grid

# Tool selector
st.sidebar.markdown("### 🧰 Tools")
cols = st.sidebar.columns(4)

tools = {
    "freedraw": "✏️",
    "line": "📏",
    "rect": "▭",
    "circle": "⚪",
    "transform": "🔧"
}

for i, (tool, icon) in enumerate(tools.items()):
    if cols[i % 4].button(icon, help=f"{tool.title()} Tool"):
        st.session_state.drawing_mode = tool

# Canvas
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

# Show grid overlay
if st.session_state.show_grid:
    grid_html = "<div style='position:absolute;top:0;left:0;width:{}px;height:{}px;z-index:1;'>".format(canvas_width, canvas_height)
    for x in range(0, canvas_width, grid_size):
        grid_html += f"<div style='position:absolute;top:0;left:{x}px;width:1px;height:{canvas_height}px;background:#ddd;opacity:0.5;'></div>"
    for y in range(0, canvas_height, grid_size):
        grid_html += f"<div style='position:absolute;top:{y}px;left:0;width:{canvas_width}px;height:1px;background:#ddd;opacity:0.5;'></div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

# Toolbar
st.markdown("### ✨ Tools")
t_cols = st.columns([1, 1, 1, 1])
with t_cols[0]:
    st.button("🗑️", help="Clear all", on_click=lambda: st.rerun())
with t_cols[1]:
    st.button("↩️", help="Undo (Coming Soon)")
with t_cols[2]:
    st.button("↪️", help="Redo (Coming Soon)")
with t_cols[3]:
    if st.button("📷", help="Download image"):
        st.warning("Image download coming soon (Streamlit doesn't support canvas export yet).")

# TODO: Implement snapping
# Currently `st_canvas` doesn't provide direct x/y editing in real time
# A workaround requires post-processing shapes to snap them — we'll tackle that in the next step.
