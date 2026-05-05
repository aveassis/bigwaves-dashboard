# BigWaves Performance Dashboard
# Light theme — Fireart inspired design
import streamlit as st
import json
import os
from pathlib import Path
import hashlib
from io import BytesIO
from pdf_export import genereer_pdf
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data"
st.set_page_config(
    page_title="BigWaves Performance Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Styling ─────────────────────────────────────────────
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }

    :root {
        --bg: #f5f7fa;
        --surface: #ffffff;
        --sidebar: #ffffff;
        --card: #ffffff;
        --border: #e8ecf1;
        --text: #1a1d23;
        --text-secondary: #6b7280;
        --text-muted: #9ca3af;
        --primary: #059669;
        --primary-light: #d1fae5;
        --primary-dark: #047857;
        --accent: #10b981;
        --green: #059669;
        --orange: #f59e0b;
        --red: #ef4444;
        --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        --shadow-hover: 0 4px 12px rgba(0,0,0,0.08);
        --radius: 12px;
        --radius-sm: 8px;
    }

    .stApp { background: var(--bg) !important; }
    .main > div { padding: 1.5rem 2rem !important; max-width: 1400px; margin: 0 auto; }
    .stApp, .st-emotion-cache-1avcm0n, .st-emotion-cache-1r4qj8v { background: var(--bg) !important; }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: var(--sidebar) !important;
        border-right: 1px solid var(--border) !important;
        min-width: 220px !important;
        max-width: 240px !important;
        box-shadow: 1px 0 0 var(--border) !important;
    }
    section[data-testid="stSidebar"] .st-emotion-cache-16txtl3 { padding: 1.2rem !important; }
    section[data-testid="stSidebar"] .st-emotion-cache-1wmy9hl { background: var(--sidebar) !important; }

    /* Typography */
    .stApp h1 { font-size: 1.5rem !important; font-weight: 600 !important; color: var(--text) !important; margin-bottom: 0.2rem !important; }
    .stApp h2 { font-size: 1.2rem !important; font-weight: 600 !important; color: var(--text) !important; }
    .stApp h3 { font-size: 1rem !important; font-weight: 600 !important; color: var(--text) !important; }
    .stApp h4 { font-size: 0.9rem !important; font-weight: 500 !important; color: var(--text) !important; }
    .stApp p, .stApp li, .stApp span, .stApp label { color: var(--text-secondary) !important; font-size: 0.85rem !important; }
    .stApp .st-caption, .stApp caption { color: var(--text-muted) !important; font-size: 0.75rem !important; }

    /* Streamlit overrides */
    section[data-testid="stSidebar"] .st-emotion-cache-1gulkj5 { display: none; }

    /* KPI Cards — rounded, shadow, light */
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
    .kpi-card {
        background: var(--card) !important;
        border-radius: var(--radius) !important;
        padding: 1rem 1.2rem !important;
        border: none !important;
        box-shadow: var(--shadow) !important;
        transition: box-shadow 0.2s, transform 0.2s;
        position: relative;
    }
    .kpi-card:hover { box-shadow: var(--shadow-hover) !important; transform: translateY(-1px); }
    .kpi-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; }
    .kpi-icon {
        width: 36px; height: 36px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1rem;
    }
    .kpi-icon.groen { background: var(--primary-light); }
    .kpi-icon.oranje { background: #fef3c7; }
    .kpi-icon.rood { background: #fee2e2; }
    .kpi-icon.groen span { color: var(--primary); }
    .kpi-icon.oranje span { color: var(--orange); }
    .kpi-icon.rood span { color: var(--red); }
    .kpi-arrow { color: var(--text-muted); font-size: 0.8rem; cursor: pointer; }
    .kpi-label { font-size: 0.75rem !important; color: var(--text-muted) !important; font-weight: 500 !important; }
    .kpi-waarde { font-size: 1.5rem !important; font-weight: 700 !important; color: var(--text) !important; line-height: 1.2; }
    .kpi-doel { font-size: 0.7rem !important; color: var(--text-muted) !important; }
    .kpi-footer { font-size: 0.7rem !important; margin-top: 4px; display: flex; align-items: center; gap: 4px; }
    .kpi-footer.positief { color: var(--green) !important; }
    .kpi-footer.negatief { color: var(--red) !important; }

    /* Section headers */
    .section-header {
        font-size: 0.95rem !important; font-weight: 600 !important;
        color: var(--text) !important; margin: 1.5rem 0 1rem 0 !important;
        display: flex; align-items: center; gap: 0.5rem;
    }
    .section-header .badge {
        background: var(--primary-light); color: var(--primary);
        font-size: 0.65rem; padding: 2px 8px; border-radius: 20px;
        font-weight: 500;
    }

    /* Cards */
    .card {
        background: var(--card) !important;
        border-radius: var(--radius) !important;
        padding: 1.2rem !important;
        border: none !important;
        box-shadow: var(--shadow) !important;
        margin-bottom: 1rem !important;
    }
    .card-title { font-size: 0.85rem !important; font-weight: 600 !important; color: var(--text) !important; margin-bottom: 1rem !important; }

    /* Status badges */
    .status-badge {
        display: inline-block; padding: 2px 10px; border-radius: 20px;
        font-size: 0.65rem; font-weight: 500;
    }
    .status-badge.completed { background: var(--primary-light); color: var(--primary); }
    .status-badge.inprogress { background: #fef3c7; color: #b45309; }
    .status-badge.pending { background: #f3f4f6; color: #6b7280; }
    .status-badge.on-discuss { background: #ede9fe; color: #7c3aed; }

    /* Bottleneck card */
    .bottleneck-card {
        background: var(--card) !important;
        border-radius: var(--radius) !important;
        padding: 1rem 1.2rem !important;
        border-left: 4px solid var(--orange) !important;
        box-shadow: var(--shadow) !important;
        margin: 0.5rem 0 1rem 0 !important;
        font-size: 0.85rem !important;
        color: var(--text-secondary) !important;
    }
    .bottleneck-card.hoog { border-left-color: var(--red) !important; }
    .bottleneck-card.medium { border-left-color: var(--orange) !important; }
    .bottleneck-card.laag { border-left-color: var(--green) !important; }

    /* Login box */
    .login-box {
        max-width: 380px !important; margin: 5rem auto !important;
        padding: 2rem !important; background: var(--card) !important;
        border-radius: var(--radius) !important; box-shadow: var(--shadow) !important;
        text-align: center !important;
    }
    .login-box h2, .login-box h3, .login-box h4 { color: var(--text) !important; }

    /* Buttons */
    .stButton button {
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important; font-size: 0.85rem !important;
        padding: 0.4rem 1rem !important;
    }
    .stButton button[kind="primary"] {
        background: var(--primary) !important;
        border: 1px solid var(--primary) !important;
        color: white !important;
    }
    .stButton button[kind="primary"]:hover { background: var(--primary-dark) !important; }

    /* Inputs */
    .stTextInput input {
        background: #f9fafb !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
    }
    .stTextInput input:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1) !important; }

    /* Metric overrides */
    [data-testid="stMetricLabel"] p { color: var(--text-muted) !important; font-size: 0.75rem !important; }
    [data-testid="stMetricValue"] { color: var(--text) !important; font-weight: 700 !important; font-size: 1.3rem !important; }
    [data-testid="stMetricDelta"] { color: var(--green) !important; font-size: 0.75rem !important; }
    .stApp hr { border-color: var(--border) !important; }
    .stProgress > div > div { background: var(--primary) !important; }
    .stProgress > div { background: var(--primary-light) !important; }

    /* Sidebar nav */
    .sidebar-logo { font-size: 1.3rem; font-weight: 700; color: var(--text); margin-bottom: 1.5rem; display: flex; align-items: center; gap: 0.5rem; }
    .sidebar-logo span { color: var(--primary); }
    .sidebar-section { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; margin: 1rem 0 0.5rem 0; font-weight: 500; }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}

    /* Page link styling */
    .stPageLink { color: var(--text-secondary) !important; font-size: 0.85rem !important; padding: 0.3rem 0 !important; }
    .stPageLink:hover { color: var(--primary) !important; }

    /* Selectbox */
    .stSelectbox div[data-baseweb="select"] { border-color: var(--border) !important; }
    .stSelectbox div[data-baseweb="select"]:focus { border-color: var(--primary) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Data loading ────────────────────────────────────────
@st.cache_data
def laad_klanten():
    klanten = {}
    if not DATA_DIR.exists():
        return klanten
    for f in sorted(DATA_DIR.glob("*.json")):
        with open(f) as fh:
            data = json.load(fh)
            klanten[data["naam"]] = data
    return klanten

# ─── Login ───────────────────────────────────────────────
def login_screen():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<span style='font-size:2rem;'>🌊</span>", unsafe_allow_html=True)
    st.markdown("## BigWaves")
    st.markdown("##### Performance Dashboard")
    st.markdown("---")
    klanten = laad_klanten()
    if not klanten:
        st.warning("Nog geen klanten. Voeg een JSON-bestand toe in data/.")
        st.stop()
    klant_naam = st.selectbox("Selecteer klant", list(klanten.keys()))
    ww = st.text_input("Wachtwoord", type="password", placeholder="Voer je wachtwoord in")
    if st.button("Inloggen", type="primary", use_container_width=True):
        data = klanten[klant_naam]
        if ww == data.get("wachtwoord", "demo"):
            st.session_state.ingelogd = True
            st.session_state.klant_naam = klant_naam
            st.session_state.data = data
            st.rerun()
        else:
            st.error("Onjuist wachtwoord. Probeer opnieuw.")
    st.markdown("---")
    st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt")
    st.markdown('</div>', unsafe_allow_html=True)

    # Admin login link
    st.markdown("<div style='text-align:center; margin-top:1rem;'>", unsafe_allow_html=True)
    if st.button("🔐 Admin", use_container_width=True):
        st.switch_page("pages/2_Admin.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if "ingelogd" not in st.session_state or not st.session_state.ingelogd:
    login_screen()

data = st.session_state.data
klant_naam = st.session_state.klant_naam

# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Main</div>', unsafe_allow_html=True)
    st.page_link("dashboard.py", label="📊  Dashboard", use_container_width=True)
    st.page_link("pages/1_HITL.py", label="👤  HITL", use_container_width=True)

    st.markdown('<div class="sidebar-section">Klant</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='padding:0.5rem 0;'><span style='font-size:0.85rem;color:var(--text);font-weight:500;'>{data.get('logo','🌊')} {klant_naam}</span></div>", unsafe_allow_html=True)
    st.caption(f"Periode: {data.get('periode', '—')}")
    st.caption(f"Update: {data.get('laatste_update', '—')}")

    st.divider()
    if st.button("🚪 Uitloggen", use_container_width=True):
        for key in ["ingelogd", "klant_naam", "data"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.divider()
    st.caption("🌊 BigWaves AI-bureau")
    st.caption("datagedreven · menselijk gecheckt")

# ─── Hoofdpagina: Overzicht ──────────────────────────────
header_cols = st.columns([1, 1])
with header_cols[0]:
    st.title("📊 Dashboard")
    st.caption(f"Performance overzicht • {data.get('periode', 'Huidige maand')}")
with header_cols[1]:
    _, right = st.columns([3, 1])
    with right:
        if st.button("📄 PDF-rapport", type="primary", use_container_width=True):
            try:
                pdf_bytes = genereer_pdf(data)
                st.download_button(
                    label="📥 Download",
                    data=pdf_bytes,
                    file_name=f"BigWaves_Rapport_{data['naam'].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Fout: {e}")

# ─── KPI-kaartjes ────────────────────────────────────────
kpi_data = data.get("kpis", {})

def status_emoji(s):
    return {"groen": "🟢", "oranje": "🟠", "rood": "🔴"}.get(s, "⚪")

if kpi_data:
    st.markdown("<div style='display:grid; grid-template-columns:repeat(4, 1fr); gap:1rem;'>", unsafe_allow_html=True)
    kpi_list = list(kpi_data.items())
    for i, (kpi, info) in enumerate(kpi_list[:4]):
        status = info.get("status", "groen")
        waarde = info["waarde"]
        eenheid = info.get("eenheid", "")
        display = f"{waarde:,}" if isinstance(waarde, int) else str(waarde)
        if eenheid == "euro": display = f"€{waarde:,}" if isinstance(waarde, int) else f"€{waarde}"
        elif eenheid == "seconden": display = f"{waarde}s"

        trend_class = "positief" if "+" in info.get("trend", "") or "lager" in info.get("trend", "").lower() else "negatief" if "-" in info.get("trend", "") else ""
        trend_icon = "↑" if trend_class == "positief" else "↓" if trend_class == "negatief" else "→"

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon {status}"><span>{status_emoji(status)}</span></div>
                <div class="kpi-arrow">⋯</div>
            </div>
            <div class="kpi-label">{kpi}</div>
            <div class="kpi-waarde">{display}</div>
            <div class="kpi-doel">Doel: {info['doel']}</div>
            <div class="kpi-footer {trend_class}">{trend_icon} {info.get('trend', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Grafieken ──────────────────────────────────────────
grafieken = data.get("grafieken", {})
if grafieken:
    st.markdown('<div class="section-header">📈 Trends <span class="badge">live</span></div>', unsafe_allow_html=True)
    import plotly.graph_objects as go
    gcols = st.columns(2)

    for idx, (key, g) in enumerate(grafieken.items()):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=g["labels"],
            y=g["waarden"],
            name=g["titel"],
            marker_color="#059669",
            opacity=0.85,
            marker_line_width=0,
        ))
        if "doel" in g:
            fig.add_hline(
                y=g["doel"],
                line_dash="dash",
                line_color="#f59e0b",
                annotation_text=f"Doel: {g['doel']}",
                annotation_position="top left",
                annotation_font=dict(color="#f59e0b", size=11),
            )
        fig.update_layout(
            title=g["titel"],
            height=280,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(size=11, color="#6b7280"),
            title_font=dict(color="#1a1d23", size=13),
            yaxis=dict(gridcolor="#f3f4f6", color="#9ca3af"),
            xaxis=dict(gridcolor="#f3f4f6", color="#9ca3af"),
            hoverlabel=dict(bgcolor="#059669", font_color="white"),
        )
        with gcols[idx % 2]:
            st.plotly_chart(fig, use_container_width=True)

# ─── Bottleneck-analyse ─────────────────────────────────
bottleneck = data.get("bottleneck", {})
if bottleneck and bottleneck.get("tekst"):
    prio = bottleneck.get("prioriteit", "laag")
    st.markdown(f"""
    <div class="bottleneck-card {prio}">
        <strong>⚠️ Bottleneck-analyse</strong>
        <span class="status-badge on-discuss" style="margin-left:0.5rem;">{prio.upper()} PRIORITEIT</span><br>
        {bottleneck['tekst']}
    </div>
    """, unsafe_allow_html=True)

# ─── HITL-status + Kostenbesparing in 2 kolommen ────────
col_left, col_right = st.columns([1, 1])

with col_left:
    hitl = data.get("hitl_detail", None)
    if hitl:
        st.markdown('<div class="section-header">👤 Human In The Loop</div>', unsafe_allow_html=True)
        hitl_ratio = data.get("kpis", {}).get("HITL-ratio", {}).get("waarde", 0)
        hitl_cols = st.columns(4)
        with hitl_cols[0]:
            st.metric("Totaal", f"{hitl['totaal_acties']:,}")
        with hitl_cols[1]:
            st.metric("Menselijk", f"{hitl['menselijke_check']:,}")
        with hitl_cols[2]:
            st.metric("Auto", f"{hitl['geautomatiseerd']:,}")
        with hitl_cols[3]:
            st.metric("Uren", f"{hitl['bespaarde_uren']}u")

        st.progress(min(int(hitl_ratio) / 100, 1.0))
        st.caption(f"HITL-ratio: {hitl_ratio}% — {'✅ onder doel' if hitl_ratio <= data.get('kpis',{}).get('HITL-ratio',{}).get('doel',100) else '⚠️ boven doel'}")
        st.caption("👤 Bekijk de HITL-detailpagina voor uitsplitsing per categorie.")

with col_right:
    # Kostenbesparing
    if data.get("kosten_besparing"):
        st.markdown('<div class="section-header">💰 Kostenbesparing</div>', unsafe_allow_html=True)
        vorige = data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)
        delta = data["kosten_besparing"] - vorige
        st.metric("Prognose deze maand", f"€{data['kosten_besparing']:,}", delta=f"{'+' if delta >= 0 else ''}€{delta:,} vs vorige maand")

# ─── Footer ─────────────────────────────────────────────
st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
