# Gedeelde CSS voor alle dashboard pagina's
import streamlit as st
from sidebar_ui import render_sidebar

DASHBOARD_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
--bg: #f1efed;
--surface: #ffffff;
--card: #ffffff;
--border: #e2e0dd;
--border-light: #d1cdc9;
--text: #121213;
--text-sec: #5a5a5a;
--text-muted: #949494;
--sidebar-bg: #2d1b69;
--sidebar-text: #ffffff;
--sidebar-text-muted: #ffffff;
--primary: #5273ff;
--primary-hover: #3f5ee6;
--primary-light: rgba(82,115,255,0.08);
--green: #22c55e;
--orange: #f59e0b;
--red: #ef4444;
--shadow: 0 4px 24px rgba(0,0,0,0.06);
--shadow-sm: 0 2px 12px rgba(0,0,0,0.04);
--radius: 14px;
--radius-sm: 10px;
--radius-pill: 200px;
}
.stApp { background: var(--bg) !important; }
.main > div { padding: 1.5rem 2rem !important; max-width: 1440px; margin: 0 auto; }
/* ─── Sidebar ──────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
    min-width: 240px !important;
    max-width: 260px !important;
}
section[data-testid="stSidebar"] .stApp h1,
section[data-testid="stSidebar"] .stApp h2,
section[data-testid="stSidebar"] .stApp p,
section[data-testid="stSidebar"] .stApp label,
section[data-testid="stSidebar"] .st-caption {
    color: var(--sidebar-text) !important;
}
section[data-testid="stSidebar"] .st-caption {
    color: var(--sidebar-text-muted) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}
section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
    padding: 0.5rem !important;
}
section[data-testid="stSidebar"] .st-emotion-cache-6qob1r {
    background: transparent !important;
}
section[data-testid="stSidebar"] .stPageLink {
    background: transparent !important;
}
section[data-testid="stSidebar"] div[data-testid="stPageLink"] p {
    color: var(--sidebar-text) !important;
    font-size: 0.85rem !important;
}
/* Force light text on ALL sidebar text elements */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] li {
    color: var(--sidebar-text) !important;
}
/* Hide auto-nav — we use page_links for proper ordering */
section[data-testid="stSidebar"] ul.st-emotion-cache-1gczx66 {
    display: none !important;
}
/* Sidebar selectbox */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: var(--radius-sm) !important;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
    color: var(--sidebar-text) !important;
}
section[data-testid="stSidebar"] .stToggle label p {
    color: var(--sidebar-text) !important;
}
section[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,0.08) !important;
    color: var(--sidebar-text) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(255,255,255,0.15) !important;
}
/* Logo */
.sidebar-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    padding: 0;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}
.sidebar-logo span { font-weight: 800; }
.sidebar-sec {
    font-size: 0.68rem;
    color: var(--sidebar-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 0.6rem 0.3rem 0.3rem 0.3rem;
    font-weight: 500;
}
/* ─── Typography ────────────────────────── */
.stApp h1 { font-size: 1.5rem !important; font-weight: 700 !important; color: var(--text) !important; letter-spacing: -0.02em !important; }
.stApp h2 { font-size: 1.15rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp h3 { font-size: 1rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp p, .stApp li, .stApp label { color: var(--text-sec) !important; font-size: 0.82rem !important; }
.stApp .st-caption { color: var(--text-muted) !important; font-size: 0.72rem !important; }
/* ─── Buttons ───────────────────────────── */
.stButton button {
    border-radius: var(--radius-pill) !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
.stButton button[kind="primary"] {
    background: var(--primary) !important;
    border: none !important;
    color: #ffffff !important;
}
.stButton button[kind="primary"]:hover {
    background: var(--primary-hover) !important;
    box-shadow: 0 4px 16px rgba(82,115,255,0.3) !important;
}
.stButton button[kind="primary"] p { color: #ffffff !important; }
.stButton button[kind="secondary"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}
.stButton button[kind="secondary"]:hover {
    border-color: var(--primary) !important;
    color: var(--primary) !important;
}
/* ─── Inputs ────────────────────────────── */
.stTextInput input {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem 0.8rem !important;
}
.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-light) !important;
}
.stApp hr { border-color: var(--border) !important; }
.stProgress > div > div { background: var(--primary) !important; }
.stProgress > div { background: var(--primary-light) !important; }
/* ─── Hide Streamlit chrome ──────────────── */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
/* ─── KPI card styling ──────────────────── */
.kpi-box {
    background: #ffffff;
    border: 1px solid #e2e0dd;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 0.5rem;
    transition: all 0.25s ease;
}
.kpi-box:hover {
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    transform: translateY(-2px);
    border-color: #d1cdc9;
}
.kpi-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem; }
.kpi-icon {
    width: 38px; height: 38px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    background: rgba(82,115,255,0.08);
    border: 1px solid rgba(82,115,255,0.12);
}
.kpi-label {
    font-size: 0.7rem; color: var(--text-muted); font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.kpi-val {
    font-size: 1.7rem; font-weight: 700; color: var(--text);
    line-height: 1.2; margin: 4px 0 3px 0;
    letter-spacing: -0.02em;
}
.kpi-foot { font-size: 0.68rem; margin-top: 5px; font-weight: 500; }
.kpi-foot.up { color: var(--green); }
.kpi-foot.down { color: var(--red); }
.kpi-foot.neutral { color: var(--text-muted); }
/* ─── Section heading ───────────────────── */
.sec-head {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
    margin: 1.2rem 0 0.6rem 0;
    letter-spacing: -0.01em;
}
/* ─── Bottleneck card ───────────────────── */
.bn-card {
    background: #ffffff;
    border: 1px solid #e2e0dd;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.82rem;
    color: var(--text-sec);
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    border-left: 4px solid #5273ff;
}
/* ─── Login screen ──────────────────────── */
.login-box {
    max-width: 380px;
    margin: 4rem auto;
    text-align: center;
    background: #ffffff;
    border: 1px solid #e2e0dd;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
/* ─── Metric cards ──────────────────────── */
.stMetric {
    background: #ffffff !important;
    border: 1px solid #e2e0dd !important;
    border-radius: 14px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
}
div[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-weight: 700 !important;
    font-size: 1.4rem !important;
}
div[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
}
div[data-testid="stMetricDelta"] { color: var(--green) !important; font-size: 0.78rem !important; }
/* ─── Responsive ────────────────────────── */
@media screen and (max-width: 768px) {
    .main > div { padding: 0.8rem 1rem !important; }
    section[data-testid="stSidebar"] { min-width: 100% !important; max-width: 100% !important; }
    .stApp h1 { font-size: 1.15rem !important; }
    .stApp h2 { font-size: 1rem !important; }
    .kpi-val { font-size: 1.3rem !important; }
    .kpi-box { padding: 0.9rem !important; }
    div[data-testid="column"] { min-width: 45% !important; flex: 1 1 45% !important; }
    div.stButton button { font-size: 0.78rem !important; padding: 0.3rem 0.8rem !important; }
    .login-box { margin: 2rem auto; padding: 1.5rem; }
}
@media screen and (max-width: 480px) {
    .main > div { padding: 0.5rem 0.6rem !important; }
    .stApp h1 { font-size: 1rem !important; }
    .stApp h2 { font-size: 0.9rem !important; }
    .kpi-val { font-size: 1.1rem !important; }
    .kpi-box { padding: 0.7rem !important; }
    .kpi-icon { width: 32px; height: 32px; font-size: 0.9rem; }
    div[data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
    .insight-card { padding: 0.8rem !important; }
    .big-number { font-size: 1.5rem !important; }
}
</style>"""


def setup_subpage():
    """Zet de shared CSS + sidebar op een subpagina.
    Moet NA set_page_config() worden aangeroepen.
    Gaat ervan uit dat st.session_state.data en st.session_state.klant_naam bestaan.
    """
    if "data" not in st.session_state or not st.session_state.get("ingelogd"):
        st.switch_page("dashboard.py")

    data = st.session_state.data
    kn = st.session_state.klant_naam

    # Shared CSS
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

    # GroeiTeam data voor sidebar badge
    gt_data = data.get("groei_team", {})

    # Periodes voorbereiden
    periodes = data.get("periodes", None)
    periode_lijst = list(periodes.keys()) if periodes else None

    # Sidebar renderen
    render_sidebar(data, kn, gt_data, periodes, periode_lijst)
