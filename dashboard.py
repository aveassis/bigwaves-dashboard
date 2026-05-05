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
st.markdown("""
<style>
    /* BigWaves brand colors */
    :root {
        --bigwaves-primary: #0A4DA4;
        --bigwaves-accent: #00B4D8;
        --bigwaves-dark: #0A1628;
        --bigwaves-card: #f8f9fa;
    }
    .stApp {
        background: #f4f6f9;
    }
    .main > div {
        padding-top: 1.5rem;
    }
    /* KPI metric cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 4px solid #0A4DA4;
        margin-bottom: 0.8rem;
    }
    .kpi-card.groen { border-left-color: #00C853; }
    .kpi-card.oranje { border-left-color: #FF9100; }
    .kpi-card.rood { border-left-color: #D50000; }
    .kpi-label { font-size: 0.85rem; color: #666; font-weight: 500; }
    .kpi-waarde { font-size: 1.8rem; font-weight: 700; color: #0A1628; }
    .kpi-doel { font-size: 0.8rem; color: #999; }
    .kpi-trend { font-size: 0.75rem; margin-top: 2px; }
    .kpi-trend.positief { color: #00C853; }
    .kpi-trend.negatief { color: #D50000; }
    /* Status badges */
    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .status-badge.groen { background: #E8F5E9; color: #2E7D32; }
    .status-badge.oranje { background: #FFF3E0; color: #E65100; }
    .status-badge.rood { background: #FFEBEE; color: #C62828; }
    /* Bottleneck cards */
    .bottleneck-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 4px solid #FF9100;
        margin: 1rem 0;
    }
    .bottleneck-card.hoog { border-left-color: #D50000; }
    .bottleneck-card.medium { border-left-color: #FF9100; }
    .bottleneck-card.laag { border-left-color: #00C853; }
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0A1628;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00B4D8;
    }
    /* Login */
    .login-box {
        max-width: 380px;
        margin: 6rem auto;
        padding: 2.5rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.1);
        text-align: center;
    }
    .login-box h1 { font-size: 1.8rem; margin-bottom: 0.3rem; }
    .login-box p { color: #666; margin-bottom: 2rem; }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
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
    if st.button("Inloggen", type="primary", width='stretch'):
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
    st.stop()

if "ingelogd" not in st.session_state or not st.session_state.ingelogd:
    login_screen()

data = st.session_state.data
klant_naam = st.session_state.klant_naam

# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### {data.get('logo', '🌊')} {klant_naam}")
    st.caption(f"Periode: {data.get('periode', 'Huidige maand')}")
    st.caption(f"Laatste update: {data.get('laatste_update', '—')}")
    st.divider()
    st.markdown("**Navigatie**")
    st.page_link("dashboard.py", label="📊  Overzicht", width='stretch')
    st.page_link("pages/1_HITL.py", label="👤  HITL-detail", width='stretch')

    st.divider()
    if st.button("🚪 Uitloggen", width='stretch'):
        for key in ["ingelogd", "klant_naam", "data"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.divider()
    st.caption("🌊 BigWaves AI-bureau")
    st.caption("datagedreven · menselijk gecheckt")

# ─── Hoofdpagina: Overzicht ──────────────────────────────
st.title(f"📊 {data.get('logo', '')} {klant_naam}")
st.caption(f"Performance overzicht • {data['periode']}")

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
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(size=11),
            yaxis=dict(gridcolor="#eee"),
            xaxis=dict(gridcolor="#eee"),
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
    st.markdown('<div class="section-header">Kostenbesparing</div>', unsafe_allow_html=True)
    vorige = data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)
    delta = data["kosten_besparing"] - vorige
    st.metric("Prognose deze maand", f"€{data['kosten_besparing']:,}", delta=f"{'+' if delta >= 0 else ''}€{delta:,} vs vorige maand")

# ─── PDF Download ──────────────────────────────────────
st.divider()
dl_cols = st.columns([3, 1, 1])
with dl_cols[1]:
    if st.button("📄 Download PDF-rapport", type="primary", width='stretch'):
        try:
            pdf_bytes = genereer_pdf(data)
            st.download_button(
                label="📥 Klik om te downloaden",
                data=pdf_bytes,
                file_name=f"BigWaves_Rapport_{data['naam'].replace(' ', '_')}_{data.get('periode', '').replace(' ', '_')}.pdf",
                mime="application/pdf",
                width='stretch',
            )
        except Exception as e:
            st.error(f"Fout bij genereren PDF: {e}")

# ─── Footer ─────────────────────────────────────────────
st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
