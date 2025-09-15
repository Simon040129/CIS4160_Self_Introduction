# homepage.py
from pathlib import Path
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import secrets

st.set_page_config(page_title="Yiming Wei · Self Intro", page_icon="📈", layout="centered")

# --- 轻量样式，压缩顶部留白 & 控制图片最大宽度 --- #
# Lightweight style, compress top whitespace & control max image width
st.markdown("""
<style>
/* 去一点顶部留白 */
/* Remove some top whitespace */
section.main > div:first-child { padding-top: 1rem; }
/* 右侧栏内容行距更紧凑 */
/* Make right sidebar content line spacing more compact */
.small p { margin: 0.25rem 0; }
</style>
""", unsafe_allow_html=True)

# ============ 顶部：左右布局 ============ #
# Top: left-right layout
col_photo, col_text = st.columns([1, 1.4], vertical_alignment="center")

with col_photo:
    # 照片：放与脚本同目录的 my_photo.jpg；若无则允许上传  
    # Photo: use my_photo.jpg in the same directory as the script; if not found, allow upload
    PHOTO = Path(__file__).with_name("my_photo.jpg")
    img = None

    def load_and_orient(pil_img):
        # 自动根据 EXIF 旋转，保证“竖直”方向（很多手机横拍会写入EXIF）  
        # Automatically rotate according to EXIF to ensure "vertical" orientation (many phones write EXIF when shooting horizontally)
        return ImageOps.exif_transpose(pil_img)

    if PHOTO.exists():
        img = load_and_orient(Image.open(PHOTO))
    else:
        st.warning("未找到 my_photo.jpg，请上传一张图片（建议竖图）。")
        uploaded = st.file_uploader("上传照片（jpg/png）", type=["jpg", "jpeg", "png"])
        if uploaded:
            img = load_and_orient(Image.open(uploaded))

    if img is not None:
        # 控制显示尺寸（竖图会更紧凑），可微调 width  
        # Control display size (portrait images are more compact), can fine-tune width
        st.image(img, width=280)

        st.markdown(
            """
            <div style="text-align: center; font-size: 0.9em; color: gray;">
                me @MoMA the other day<br>
                with an awkward smile
            </div>
            """,
            unsafe_allow_html=True
        )

with col_text:
    st.title("Yiming Wei")
    st.markdown("### Financial Engineering, UIBE")
    st.markdown("You might have heard of the University of International Business and Economics (my home uni) from the Study Abroad Fair. It's located in Chaoyang, Beijing. ")
    st.markdown("#### Exchange Student at Baruch")
    st.markdown("I am an exchange student at Baruch College this semester, it's my first time in NYC, loving it so far!")

st.divider()

# ============ 下方：随机游走模拟 ============  # 
# Below: random walk simulation
st.subheader("📈 Random Walk Simulation")
st.markdown(
    """
    I was thinking about what I shoud do down in this section that is interactive and not that boring 🤔. So this is waht I've come up with (still kinda nerdy). 
    
    This is a simple simulation of a ***1D random walk***. You can adjust the number of steps and choose to fix the random seed for reproducibility. Hope you get one that goses up all the way! I hope the same for your investment) 🚀
    """
)
# 初始化用于重生成的种子（仅在未固定随机种子时生效）  
# Initialize seed for regeneration (only effective when random seed is not fixed)
if "regen_seed" not in st.session_state:
    st.session_state["regen_seed"] = None

# 控件区域：放到同一行 
# Control area: place on the same row
c_steps, c_fix, c_regen = st.columns([2, 2, 1])
with c_steps:
    steps = st.slider("Steps", 50, 500, 150)
with c_fix:
    seed_box = st.toggle("Fix random seed (reproducible)", value=False)
with c_regen:
    regen = st.button("🔁 Regenerate")

# 选择随机数生成器：如果固定种子，始终使用 42；否则使用 session_state 中的种子，并在点击 Regenerate 时更新  
# Choose random number generator: if seed is fixed, always use 42; else use seed from session_state, update on Regenerate click
if seed_box:
    rng = np.random.default_rng(42)
else:
    if regen or st.session_state["regen_seed"] is None:
        # 生成一个新的随机种子，用于重新模拟  
        # Generate a new random seed for resimulation
        st.session_state["regen_seed"] = secrets.randbits(32)
    rng = np.random.default_rng(st.session_state["regen_seed"])

# 使用选定的生成器进行随机游走模拟  
# Use the selected generator to simulate random walk
path = np.cumsum(rng.standard_normal(steps))

# 计算简单指标  
# Calculate simple metrics
endpoint = float(path[-1]) if len(path) else 0.0
running_max = np.maximum.accumulate(path) if len(path) else np.array([0.0])
max_dd_abs = float(np.max(running_max - path)) if len(path) else 0.0
step_vol = float(np.std(np.diff(path))) if len(path) > 1 else 0.0

# 绘图  
# Plotting
fig, ax = plt.subplots()
ax.plot(path)
ax.set_xlabel("Step")
ax.set_ylabel("Cumulative Sum")
st.pyplot(fig)

# 指标展示  
# Metrics display
m1, m2, m3 = st.columns(3)
m1.metric(label="Endpoint", value=f"{endpoint:.2f}")
m2.metric(label="Max Drawdown", value=f"-{max_dd_abs:.2f}")
m3.metric(label="Step Volatility (σ)", value=f"{step_vol:.2f}")

st.caption("Built with Python & Streamlit")  # 使用 Python 和 Streamlit 构建