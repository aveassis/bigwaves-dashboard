# BigWaves Performance Dashboard
# Streamlit multi-page app — read-only voor klanten
import streamlit as st
import json
import os
from pathlib import Path
import hashlib
from io import BytesIO
from pdf_export import genereer_pdf

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
        --bw-primary: #0A4DA4;
        --bw-accent: #00B4D8;
        --bw-dark: #0f0f0f;
        --bw-surface: #171717;
        --bw-card: #1a1a1a;
        --bw-border: #2e2e2e;
        --bw-border-light: #363636;
        --bw-text: #fafafa;
        --bw-text-secondary: #b4b4b4;
        --bw-text-muted: #898989;
        --bw-green: #00C853;
        --bw-orange: #FF9100;
        --bw-red: #D50000;
    }

    .stApp { background: var(--bw-surface) !important; }
    .main > div { padding-top: 1.5rem; }

    .stApp, .st-emotion-cache-1avcm0n, .st-emotion-cache-1r4qj8v {
        background: var(--bw-surface) !important;
    }

    section[data-testid="stSidebar"] {
        background: var(--bw-dark) !important;
        border-right: 1px solid var(--bw-border) !important;
    }
    section[data-testid="stSidebar"] .st-emotion-cache-1wmy9hl {
        background: var(--bw-dark) !important;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: var(--bw-text) !important;
        font-weight: 500 !important;
    }
    .stApp p, .stApp li, .stApp span, .stApp label {
        color: var(--bw-text-secondary) !important;
    }
    .stApp .st-caption, .stApp caption, .stApp .caption {
        color: var(--bw-text-muted) !important;
    }

    .kpi-card {
        background: var(--bw-card) !important;
        border-radius: 12px !important;
        padding: 1.2rem 1.5rem !important;
        border: 1px solid var(--bw-border) !important;
        border-left: 4px solid var(--bw-primary) !important;
        margin-bottom: 0.8rem !important;
    }
    .kpi-card.groen { border-left-color: var(--bw-green) !important; }
    .kpi-card.oranje { border-left-color: var(--bw-orange) !important; }
    .kpi-card.rood { border-left-color: var(--bw-red) !important; }
    .kpi-label {
        font-size: 0.8rem !important;
        color: var(--bw-text-muted) !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .kpi-waarde {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: var(--bw-text) !important;
        margin-top: 4px !important;
    }
    .kpi-doel {
        font-size: 0.75rem !important;
        color: var(--bw-text-muted) !important;
        margin-top: 2px !important;
    }
    .kpi-trend {
        font-size: 0.75rem !important;
        margin-top: 4px !important;
        font-weight: 500 !important;
    }
    .kpi-trend.positief { color: var(--bw-green) !important; }
    .kpi-trend.negatief { color: var(--bw-red) !important; }

    .status-badge {
        display: inline-block !important;
        padding: 2px 12px !important;
        border-radius: 9999px !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .status-badge.groen { background: rgba(0, 200, 83, 0.15) !important; color: var(--bw-green) !important; }
    .status-badge.oranje { background: rgba(255, 145, 0, 0.15) !important; color: var(--bw-orange) !important; }
    .status-badge.rood { background: rgba(213, 0, 0, 0.15) !important; color: var(--bw-red) !important; }

    .bottleneck-card {
        background: var(--bw-card) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        border: 1px solid var(--bw-border) !important;
        border-left: 4px solid var(--bw-orange) !important;
        margin: 1rem 0 !important;
        color: var(--bw-text-secondary) !important;
    }
    .bottleneck-card.hoog { border-left-color: var(--bw-red) !important; }
    .bottleneck-card.medium { border-left-color: var(--bw-orange) !important; }
    .bottleneck-card.laag { border-left-color: var(--bw-green) !important; }
    .bottleneck-card strong { color: var(--bw-text) !important; }

    .section-header {
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: var(--bw-text) !important;
        margin: 1.5rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid var(--bw-border) !important;
    }

    .login-box {
        max-width: 400px !important;
        margin: 6rem auto !important;
        padding: 2.5rem !important;
        background: var(--bw-card) !important;
        border-radius: 16px !important;
        border: 1px solid var(--bw-border) !important;
        text-align: center !important;
    }
    .login-box h2, .login-box h3, .login-box h4 {
        color: var(--bw-text) !important;
    }
    .login-box p {
        color: var(--bw-text-muted) !important;
        margin-bottom: 2rem !important;
    }

    .stTextInput input {
        background: var(--bw-dark) !important;
        color: var(--bw-text) !important;
        border-color: var(--bw-border) !important;
    }
    .stTextInput input:focus {
        border-color: var(--bw-primary) !important;
    }

    .stButton button {
        border-radius: 9999px !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    .stButton button[kind="primary"] {
        background: var(--bw-primary) !important;
        border: 1px solid var(--bw-primary) !important;
        color: white !important;
    }
    .stButton button[kind="primary"]:hover {
        background: #0B5BCC !important;
    }

    [data-testid="stMetricLabel"] p {
        color: var(--bw-text-muted) !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stMetricValue"] {
        color: var(--bw-text) !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricDelta"] {
        color: var(--bw-text-secondary) !important;
    }

    .stApp hr { border-color: var(--bw-border) !important; }
    .stProgress > div > div { background: var(--bw-primary) !important; }

    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}

    ::selection { background: rgba(10, 77, 164, 0.3); }
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
    st.markdown("## 🌊 BigWaves")
    st.markdown("#### Performance Dashboard")
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

ADMIN_USER = "admin"
ADMIN_PASS = "bigwaves2026"

if "ingelogd" not in st.session_state or not st.session_state.ingelogd:
    login_screen()

data = st.session_state.data
klant_naam = st.session_state.klant_naam

# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🌊 {klant_naam}")
    st.caption(f"Periode: {data.get('periode', 'Huidige maand')}")
    st.caption(f"Laatste update: {data.get('laatste_update', '—')}")
    st.divider()
    st.markdown("**Navigatie**")
    st.page_link("dashboard.py", label="📊  Overzicht", use_container_width=True)
    st.page_link("pages/1_HITL.py", label="👤  HITL-detail", use_container_width=True)

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
st.title(f"🌊 {klant_naam}")
st.caption(f"Performance overzicht • {data['periode']}")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Welkomstbericht met uitleg ──────────────────────────
with st.expander("💡 Wat zie ik hier?", expanded=False):
    st.markdown("""
    Dit dashboard geeft je een compleet overzicht van hoe jouw AI-processen presteren.

    **De KPI-kaarten** (hieronder) laten de belangrijkste prestaties zien:
    - 🟢 **Groen** = op of boven doel
    - 🟠 **Oranje** = aandacht nodig, benadert limiet  
    - 🔴 **Rood** = onder doel, actie gewenst

    **Trends** geven aan of het beter of slechter gaat dan vorige maand.

    **Human In The Loop (HITL)** is BigWaves' unieke aanpak: elk AI-proces heeft een menselijke check.
    Een lagere HITL-ratio betekent dat de AI meer zelfstandig kan — dat is goed!
    """)

# ─── KPI-kaartjes in rows van 3 ────────────────────────
st.markdown('<div class="section-header">Kern-KPI\'s</div>', unsafe_allow_html=True)
kpi_data = data.get("kpis", {})

# Helper
def status_emoji(s):
    return {"groen": "🟢", "oranje": "🟠", "rood": "🔴"}.get(s, "⚪")

cols = st.columns(3)
for i, (kpi, info) in enumerate(kpi_data.items()):
    status = info.get("status", "groen")
    trend_class = "positief" if "+" in info.get("trend", "") or "lager" in info.get("trend", "").lower() else "negatief" if "-" in info.get("trend", "") else ""
    waarde_str = info["waarde"]
    eenheid = info.get("eenheid", "")
    display_waarde = f"{waarde_str:,}" if isinstance(waarde_str, int) else waarde_str
    if eenheid == "euro":
        display_waarde = f"€{waarde_str:,}" if isinstance(waarde_str, int) else f"€{waarde_str}"
    elif eenheid == "seconden":
        display_waarde = f"{waarde_str}s"

    with cols[i % 3]:
        st.markdown(f"""
        <div class="kpi-card {status}">
            <div class="kpi-label">{status_emoji(status)} {kpi}</div>
            <div class="kpi-waarde">{display_waarde}</div>
            <div class="kpi-doel">Doel: {info['doel']}{'' if eenheid == 'items' else ' ' + eenheid if eenheid not in ('euro','seconden') else ''}</div>
            <div class="kpi-trend {trend_class}">{info.get('trend', '')}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── Grafieken ──────────────────────────────────────────
grafieken = data.get("grafieken", {})
if grafieken:
    st.markdown('<div class="section-header">Trends</div>', unsafe_allow_html=True)
    st.caption("Deze grafieken laten de dagelijkse en wekelijkse ontwikkelingen zien. De oranje stippellijn is het streefdoel.")
    import plotly.graph_objects as go
    gcols = st.columns(2)

    for idx, (key, g) in enumerate(grafieken.items()):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=g["labels"],
            y=g["waarden"],
            name=g["titel"],
            marker_color="#0A4DA4",
            opacity=0.85,
        ))
        if "doel" in g:
            fig.add_hline(
                y=g["doel"],
                line_dash="dash",
                line_color="#FF9100",
                annotation_text=f"Doel: {g['doel']}",
                annotation_position="top left",
            )
        fig.update_layout(
            title=g["titel"],
            height=280,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font=dict(size=11, color="#b4b4b4"),
            title_font=dict(color="#fafafa"),
            yaxis=dict(gridcolor="#2e2e2e", color="#898989"),
            xaxis=dict(gridcolor="#2e2e2e", color="#898989"),
        )
        with gcols[idx % 2]:
            st.plotly_chart(fig, use_container_width=True)

# ─── Bottleneck-analyse ─────────────────────────────────
bottleneck = data.get("bottleneck", {})
if bottleneck and bottleneck.get("tekst"):
    prio = bottleneck.get("prioriteit", "laag")
    st.markdown(f"""
    <div class="bottleneck-card {prio}">
        <strong>Bottleneck-analyse</strong> <span class="status-badge {prio}">{prio.upper()} PRIORITEIT</span><br>
        {bottleneck['tekst']}
    </div>
    """, unsafe_allow_html=True)

# ─── HITL-status (samenvatting) ─────────────────────────
hitl = data.get("hitl_detail", None)
if hitl:
    st.markdown('<div class="section-header">Human In The Loop</div>', unsafe_allow_html=True)
    st.caption("HITL = elk AI-proces heeft een menselijke check. Een lager percentage betekent dat de AI meer zelfstandig werkt. BigWaves' unieke aanpak.")
    hitl_ratio = data.get("kpis", {}).get("HITL-ratio", {}).get("waarde", 0)
    hitl_cols = st.columns(4)
    with hitl_cols[0]:
        st.metric("Totaal acties", f"{hitl['totaal_acties']:,}")
    with hitl_cols[1]:
        st.metric("Menselijke check", f"{hitl['menselijke_check']:,}")
    with hitl_cols[2]:
        st.metric("Geautomatiseerd", f"{hitl['geautomatiseerd']:,}")
    with hitl_cols[3]:
        st.metric("Bespaarde uren", f"{hitl['bespaarde_uren']}u")

    # Mini progress bar
    st.progress(min(int(hitl_ratio) / 100, 1.0))
    st.caption(f"HITL-ratio: {hitl_ratio}% — { '✅ onder doel' if hitl_ratio <= data.get('kpis',{}).get('HITL-ratio',{}).get('doel',100) else '⚠️ boven doel'}")
    st.caption("👤 Bekijk de HITL-detailpagina voor een uitsplitsing per categorie.")

# ─── Kostenbesparing ────────────────────────────────────
if data.get("kosten_besparing"):
    st.markdown('<div class="section-header">💰 Kostenbesparing</div>', unsafe_allow_html=True)
    st.caption("Dit is de prognose van wat AI-automatisering deze maand oplevert aan bespaarde kosten.")
    vorige = data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)
    delta = data["kosten_besparing"] - vorige
    st.metric("Prognose deze maand", f"€{data['kosten_besparing']:,}", delta=f"{'+' if delta >= 0 else ''}€{delta:,} vs vorige maand")

# ─── PDF Download ──────────────────────────────────────
st.divider()
dl_cols = st.columns([3, 1, 1])
with dl_cols[1]:
    if st.button("📄 Download PDF-rapport", type="primary", use_container_width=True):
        try:
            pdf_bytes = genereer_pdf(data)
            st.download_button(
                label="📥 Klik om te downloaden",
                data=pdf_bytes,
                file_name=f"BigWaves_Rapport_{data['naam'].replace(' ', '_')}_{data.get('periode', '').replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Fout bij genereren PDF: {e}")

# ─── Footer ─────────────────────────────────────────────
st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
