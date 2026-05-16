# BigWaves Performance Dashboard
# Light theme — BigWaves.nl + Pinterest inspired
import streamlit as st
import json
import os
from pathlib import Path
from io import BytesIO
from pdf_export import genereer_pdf
from groei_team_ui import render_pakket_badge, GROEI_TEAM_CSS
from sidebar_ui import render_sidebar

DATA_DIR = Path(__file__).parent / "data"
st.set_page_config(
    page_title="BigWaves Conversiebureau",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Forceer verse sessie: als gebruiker ingelogd is maar sidebar_v2 ontbreekt, log uit
if st.session_state.get("ingelogd") and "sidebar_v2" not in st.session_state:
    for k in ["ingelogd", "klant_naam", "data", "admin_logged_in"]:
        st.session_state.pop(k, None)
    st.session_state.sidebar_v2 = True
    st.rerun()

# Detect mobiel via JavaScript — sluit sidebar in als small screen
st.markdown("""<script>
if (window.innerWidth < 768) {
    const sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        const btn = parent.document.querySelector('[data-testid="stSidebarCollapsedControl"]');
        if (btn) btn.click();
    }
}
</script>""", unsafe_allow_html=True)

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">""", unsafe_allow_html=True)

st.markdown("""<style>
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
    /* page links inside sidebar */
    background: transparent !important;
}
section[data-testid="stSidebar"] .stPageLink {
    background: transparent !important;
}
/* Sidebar page links */
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
/* Show Streamlit's auto-generated multi-page navigation */
/* (keeping it visible — it's cleaner without emoji page_links) */

/* But: hide auto-nav and use our own page_links for proper ordering */
section[data-testid="stSidebar"] ul.st-emotion-cache-1gczx66 {
    display: none !important;
}
section[data-testid="stSidebar"] .st-caption {
    color: var(--sidebar-text-muted) !important;
}
/* Sidebar health badge text */
section[data-testid="stSidebar"] div[style*="color"] {
    color: var(--sidebar-text) !important;
}/* Restore selectbox default colors */
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
    color: var(--sidebar-text) !important;
}
/* Sidebar selectbox */
section[data-testid="stSidebar"] .stSelectbox label p {
    color: var(--sidebar-text-muted) !important;
}
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
section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
    padding: 0.5rem !important;
    order: -1 !important;
}
/* Streamlit sidebar is flex, reverse the order so our content goes on top */
section[data-testid="stSidebar"] > div {
    display: flex !important;
    flex-direction: column !important;
}
/* Put Streamlit's auto-nav below our content */
section[data-testid="stSidebar"] ul.st-emotion-cache-1gczx66 {
    order: 1 !important;
}
/* Logo altijd bovenaan */
.sidebar-logo {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    padding: 0;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}
.sidebar-logo span {
    font-weight: 800;
}
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
.stButton button[kind="primary"] p {
    color: #ffffff !important;
}
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
/* ─── Sidebar collapse ──────────────────── */
@media screen and (min-width: 769px) {
    div[data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 999 !important;
        background: rgba(30, 33, 49, 0.9) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 8px !important;
        width: 32px !important;
        height: 32px !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stSidebarCollapsedControl"]:hover {
        background: rgba(139, 92, 246, 0.2) !important;
        border-color: rgba(139, 92, 246, 0.6) !important;
    }
    div[data-testid="stSidebarCollapsedControl"] svg {
        color: #8b5cf6 !important;
        fill: #8b5cf6 !important;
        width: 18px !important;
        height: 18px !important;
        display: block !important;
    }
    button[title*=\"sidebar\"] { display: none !important; }
    button[aria-label*=\"sidebar\"] { display: none !important; }
    /* Als sidebar collapsed is, toon de collapse knop linksboven */
    section[data-testid="stSidebar"][aria-expanded="false"] + div button[data-testid="stBaseButton-headerNoPadding"] {
        display: none !important;
    }
}

/* Als sidebar gecollapsed is, toon een eigen herstel knopje linksboven */
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
.kpi-dots { color: var(--text-muted); font-size: 1.1rem; cursor: pointer; }
.kpi-label {
    font-size: 0.7rem; color: var(--text-muted); font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
}
.kpi-val {
    font-size: 1.7rem; font-weight: 700; color: var(--text);
    line-height: 1.2; margin: 4px 0 3px 0;
    letter-spacing: -0.02em;
}
.kpi-target { font-size: 0.68rem; color: var(--text-muted); }
.kpi-foot { font-size: 0.68rem; margin-top: 5px; font-weight: 500; }
.kpi-foot.up { color: var(--green); }
.kpi-foot.down { color: var(--red); }
.kpi-foot.neutral { color: var(--text-muted); }
.kpi-uitleg { font-size: 0.68rem; color: var(--text-sec); margin-top: 4px; padding-top: 4px; border-top: 1px solid var(--border); }
.kpi-vs { font-size: 0.72rem; color: var(--text-sec); margin: 2px 0; }
.kpi-vs-label { color: var(--text-muted); font-size: 0.65rem; }
.kpi-vs-diff { font-weight: 600; color: var(--primary); }

/* ─── Section heading ───────────────────── */
.sec-head {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text);
    margin: 1.2rem 0 0.6rem 0;
    letter-spacing: -0.01em;
}
.sec-head .pill {
    font-size: 0.62rem;
    font-weight: 500;
    background: var(--primary-light);
    color: var(--primary);
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    vertical-align: middle;
    margin-left: 0.4rem;
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
div[data-testid="stMetricDelta"] {
    color: var(--green) !important;
    font-size: 0.78rem !important;
}

/* ─── Kanban-style cards ────────────────── */
.kanban-card {
    background: #ffffff;
    border: 1px solid #e2e0dd;
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transition: all 0.2s ease;
}
.kanban-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transform: translateY(-1px);
}

/* ─── Responsive — Mobiel & Tablet ──────── */
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
</style>""", unsafe_allow_html=True)

# ─── Data ────────────────────────────────────────────────
@st.cache_data
def laad_klanten():
    kl = {}
    if not DATA_DIR.exists(): return kl
    for f in sorted(DATA_DIR.glob("*.json")):
        with open(f) as fh: d=json.load(fh); kl[d["naam"]]=d
    return kl

# ─── Login ───────────────────────────────────────────────
def login_screen():
    # Hide sidebar on login maar laat collapse knop zichtbaar
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    .main > div { padding: 1.2rem 1.8rem !important; max-width: 1440px; margin: 0 auto; }
    button[kind="header"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    section.main { margin-left: 0 !important; }
    @media screen and (max-width: 768px) {
        .main > div { padding: 0.6rem 0.8rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<span style='font-size:2.2rem;'>🌊</span>", unsafe_allow_html=True)
    st.markdown("## BigWaves")
    st.markdown("<p style='color:#949494;margin-bottom:1.5rem;'>Performance Dashboard</p>", unsafe_allow_html=True)
    klanten=laad_klanten()
    if not klanten:
        st.warning("Geen klanten. Voeg JSON toe in data/.")
        st.stop()
    kn=st.selectbox("Klant", list(klanten.keys()))
    ww=st.text_input("Wachtwoord", type="password", placeholder="Voer wachtwoord in")
    if st.button("Inloggen", type="primary", width="stretch"):
        d=klanten[kn]
        if ww==d.get("wachtwoord","demo"):
            st.session_state.ingelogd=True; st.session_state.klant_naam=kn; st.session_state.data=d; st.rerun()
        else: st.error("Onjuist wachtwoord.")
    st.markdown("---")
    st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;margin-top:1rem;'>", unsafe_allow_html=True)
    if st.button("🔐 Admin", width="stretch"): st.switch_page("pages/2_Admin.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if "ingelogd" not in st.session_state or not st.session_state.ingelogd: login_screen()
data=st.session_state.data; kn=st.session_state.klant_naam

# ─── GroeiTeam sidebar badge ─────────────────────────────
# badge wordt geregeld in sidebar_ui.py — niet dupliceren
gt = data.get("groei_team", {})

# ─── Periode selector ─────────────────────────────────────
# Check of de data periodes heeft (nieuw formaat) of plat (oud formaat)
periodes = data.get("periodes", None)
if periodes:
    periode_lijst = list(periodes.keys())
    # Eerste keer of bij switchen
    if "huidige_periode" not in st.session_state or st.session_state.klant_naam != kn:
        st.session_state.huidige_periode = periode_lijst[0]
    # Data uit gekozen periode halen
    pd = periodes[st.session_state.huidige_periode]
    data.update(pd)  # voeg periode-data toe aan hoofd-data
    data["periode"] = st.session_state.huidige_periode
    # Vergelijk-data laden
    vergelijk_data = None
    vergelijk_pd = None
    if st.session_state.get("vergelijk_modus", False) and len(periode_lijst) > 1:
        v_periode = st.session_state.get("vergelijk_periode", "")
        if v_periode and v_periode in periodes:
            vergelijk_pd = periodes[v_periode]
            vergelijk_data = {k: v for k, v in data.items()}
            vergelijk_data.update(vergelijk_pd)
            vergelijk_data["periode"] = v_periode
else:
    # Oud formaat: platte data, geen periodes
    pass

# ─── Sidebar ─────────────────────────────────────────────
render_sidebar(data, kn, gt, periodes, periode_lijst if periodes else None)

# ─── Header ──────────────────────────────────────────────
logo = data.get("logo", "🌊")
accent = data.get("accent_kleur", "#10b981")
st.markdown(f"<div style='display:flex;align-items:center;gap:0.8rem;'><span style='font-size:2.5rem;'>{logo}</span><div><h1 style='margin:0;'>Dashboard</h1><p style='margin:0;color:var(--text-muted);font-size:0.82rem;'>Performance overzicht • {data.get('periode','Huidige maand')}{' vs ' + vergelijk_data.get('periode','') if vergelijk_data else ''}</p></div></div>", unsafe_allow_html=True)

# ─── Knoppen over volle breedte ──────────────────────────
bcols = st.columns([1, 1, 1, 1])
with bcols[0]:
    if st.button("📄 PDF", type="secondary", width="stretch"):
        try:
            pb=genereer_pdf(data)
            st.session_state.pdf_data = pb
            st.download_button("📥 Download",pb,file_name=f"BigWaves_{data['naam'].replace(' ','_')}.pdf",mime="application/pdf",width="stretch")
        except Exception as e: st.error(f"Fout: {e}")
with bcols[1]:
    # PDF per mail (toont input veld na klik)
    if st.button("📧 Mail PDF", type="secondary", width="stretch"):
        st.session_state.show_mail_input = not st.session_state.get("show_mail_input", False)
if st.session_state.get("show_mail_input", False):
    mc1, mc2 = st.columns([3, 1])
    with mc1:
        mail_adres = st.text_input("E-mailadres", placeholder="naam@bedrijf.nl", key="mail_adres")
    with mc2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📤 Verstuur", type="primary", width="stretch", key="send_mail"):
            if mail_adres and "@" in mail_adres:
                pb = st.session_state.get("pdf_data") or genereer_pdf(data)
                try:
                    import smtplib, ssl
                    from email.mime.text import MIMEText
                    from email.mime.multipart import MIMEMultipart
                    from email.mime.base import MIMEBase
                    from email import encoders
                    msg = MIMEMultipart()
                    msg["Subject"] = f"BigWaves Dashboard — {data['naam']} ({data.get('periode','')})"
                    msg["From"] = "dashboard@bigwaves.ai"
                    msg["To"] = mail_adres
                    msg.attach(MIMEText(f"""Beste lezer,\n\nHierbij ontvangt u de BigWaves Performance Dashboard rapportage voor {data['naam']}.\n\nPeriode: {data.get('periode', '—')}\n\nMet vriendelijke groet,\nBigWaves AI-bureau\ndatagedreven · menselijk gecheckt\nwww.bigwaves.ai""", "plain"))
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(pb.getvalue())
                    encoders.encode_base64(part)
                    st.success(f"PDF verstuurd naar {mail_adres}")
                except Exception as e:
                    st.error(f"Fout bij versturen: {e}")
                st.session_state.show_mail_input = False
                st.rerun()

with bcols[2]:
    # CSV download
    if st.button("📊 CSV", type="secondary", width="stretch"):
        import csv, io
        kd = data.get("kpis", {})
        if kd:
            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(["KPI", "Waarde", "Doel", "Trend"])
            for nm, inf in kd.items():
                w.writerow([nm, inf.get("waarde",""), inf.get("doel",""), inf.get("trend","")])
            csv_str = buf.getvalue()
            st.session_state["csv_data"] = csv_str
    if st.session_state.get("csv_data"):
        st.download_button("📥 Download CSV", st.session_state["csv_data"], file_name=f"BigWaves_{data['naam'].replace(' ','_')}.csv", mime="text/csv", use_container_width=True, key="csv_dl")
        if st.button("✕ Sluit", key="csv_close", use_container_width=True):
            del st.session_state["csv_data"]
            st.rerun()

with bcols[3]:
    # Notificaties genereren uit data
    alerts = []
    kpi_data = data.get("kpis", {})
    for name, info in kpi_data.items():
        d_ora_not = info.get("drempel_oranje", 10)
        d_rood_not = info.get("drempel_rood", 25)
        w = info.get("waarde", 0)
        doel = info.get("doel", 0)
        sts = info.get("status", "groen")
        if isinstance(w, (int,float)) and isinstance(doel, (int,float)) and doel > 0:
            pct_afwijking = max(0, round((doel - w) / doel * 100, 1))
            if pct_afwijking >= d_rood_not:
                sts = "rood"
            elif pct_afwijking >= d_ora_not:
                sts = "oranje"
            else:
                sts = "groen"
        if sts == "rood":
            alerts.append(("🔴", f"**{name}** is onder doel! {info.get('waarde','')} vs doel {info.get('doel','')}"))
        elif sts == "oranje":
            alerts.append(("🟠", f"**{name}** nadert zijn limiet. {info.get('waarde','')} / {info.get('doel','')}"))
        trend = info.get("trend", "")
        if "+" in trend:
            alerts.append(("🟢", f"**{name}** {trend}"))
    bn = data.get("bottleneck", {})
    if bn and bn.get("tekst") and bn.get("tekst") != "Geen knelpunten deze week. Alle processen draaien binnen de gestelde doelen.":
        alerts.append(("⚠️", bn["tekst"]))
    update = data.get("laatste_update", "")
    if update:
        alerts.append(("📅", f"Data geüpdatet op {update}"))

    # Badge alleen als niet gelezen
    show_badge = not st.session_state.get("notifications_read", False) and len(alerts) > 0
    badge = f" ({len(alerts)})" if show_badge else ""
    if st.button(f"🔔 Notificaties{badge}", type="secondary", width="stretch"):
        st.session_state.show_notifications = not st.session_state.get("show_notifications", False)

# Notificatie paneel (buiten de kolom, over volle breedte)
if st.session_state.get("show_notifications", False):
    with st.container():
        st.markdown(f"""<div style="background:#ffffff;border:1px solid #e2e0dd;border-radius:14px;padding:1rem;margin-bottom:0.5rem;max-height:350px;overflow-y:auto;box-shadow:0 2px 12px rgba(0,0,0,0.04);">
            <div style="font-size:0.85rem;font-weight:600;color:#121213;margin-bottom:0.5rem;">🔔 Meldingen</div>
            {''.join([f'<div style="padding:0.4rem 0;border-bottom:1px solid #e2e0dd;font-size:0.8rem;color:#5a5a5a;">{a[0]} {a[1]}</div>' for a in alerts[:8]])}
        </div>""", unsafe_allow_html=True)
        if st.button("✅ Markeer als gelezen", width="stretch"):
            st.session_state.notifications_read = True
            st.session_state.show_notifications = False
            st.rerun()

# ─── KPI Cards ──────────────────────────────────────────
kpis=data.get("kpis",{})
def se(s): return {"groen":"🟢","oranje":"🟠","rood":"🔴"}.get(s,"⚪")
def tc(t):
    if "+" in t or "lager" in t.lower(): return "up"
    if "-" in t: return "down"
    return "neutral"

if kpis:
    kpi_ncols = 2 if st.session_state.get("mobile", False) else 4
    kpi_cols = st.columns(kpi_ncols)
    colors = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}
    for i, (kpi, info) in enumerate(list(kpis.items())[:4]):
        # Bepaal status op basis van drempelwaarden
        d_ora = info.get("drempel_oranje", 10)
        d_rood = info.get("drempel_rood", 25)
        sts = info.get("status", "groen")
        w = info.get("waarde", 0)
        doel = info.get("doel", 0)
        if isinstance(w, (int,float)) and isinstance(doel, (int,float)) and doel > 0:
            pct_afwijking = max(0, round((doel - w) / doel * 100, 1))
            if pct_afwijking >= d_rood:
                sts = "rood"
            elif pct_afwijking >= d_ora:
                sts = "oranje"
            else:
                sts = "groen"
        w = info["waarde"]
        e = info.get("eenheid", "")
        dsp = f"{w:,}" if isinstance(w, int) else str(w)
        if e == "euro": dsp = f"€{w:,}" if isinstance(w, int) else f"€{w}"
        elif e == "seconden": dsp = f"{w}s"
        tc = "up" if "+" in info.get("trend","") or "lager" in info.get("trend","").lower() else "down" if "-" in info.get("trend","") else ""
        arrow = "↑" if tc == "up" else "↓" if tc == "down" else "→"
        clr = colors.get(sts, "#10b981")
        # Vergelijk waarde ophalen
        v_dsp = ""
        v_diff = ""
        if vergelijk_data and vergelijk_data.get("kpis", {}).get(kpi):
            v_info = vergelijk_data["kpis"][kpi]
            v_w = v_info["waarde"]
            v_dsp = f"{v_w:,}" if isinstance(v_w, int) else str(v_w)
            if e == "euro": v_dsp = f"€{v_w:,}" if isinstance(v_w, int) else f"€{v_w}"
            elif e == "seconden": v_dsp = f"{v_w}s"
            verschil = w - v_w
            if e == "euro": v_diff = f"{'+' if verschil >= 0 else ''}€{verschil:,}"
            elif isinstance(w, (int,float)) and isinstance(v_w, (int,float)):
                pct = round((w - v_w) / v_w * 100, 1) if v_w else 0
                v_diff = f"{'+' if pct >= 0 else ''}{pct}%"
        with kpi_cols[i]:
            extra = ""
            if v_dsp:
                extra = f'<div class="kpi-vs"><span class="kpi-vs-label">{vergelijk_data["periode"]}:</span> {v_dsp} <span class="kpi-vs-diff">{v_diff}</span></div>'
            st.html(f"""<div style="background:#ffffff;border:1px solid #e2e0dd;border-radius:14px;padding:1.2rem 1.4rem;box-shadow:0 2px 12px rgba(0,0,0,0.04);margin-bottom:0.5rem;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;">
                    <div style="width:38px;height:38px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;background:rgba(82,115,255,0.08);border:1px solid rgba(82,115,255,0.12);">{se(sts)}</div>
                    <div style="color:#949494;font-size:1.1rem;">⋯</div>
                </div>
                <div style="font-size:0.7rem;color:#949494;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">{kpi}</div>
                <div style="font-size:1.5rem;font-weight:700;color:#121213;margin:0.4rem 0 0.25rem 0;letter-spacing:-0.02em;">{dsp}</div>
                {extra}
                <div style="font-size:0.68rem;color:#949494;">Doel: {info['doel']}</div>
                <div style="font-size:0.68rem;margin-top:5px;font-weight:500;color:#{"22c55e" if tc=="up" else "ef4444" if tc=="down" else "949494"};">{arrow} {info.get('trend','')}</div>
                {f'<div style="font-size:0.68rem;color:#5a5a5a;margin-top:4px;padding-top:4px;border-top:1px solid #e2e0dd;">ⓘ {info.get("uitleg","")}</div>' if info.get('uitleg') else ''}
            </div>""")

# ─── Grafieken ──────────────────────────────────────────
g=data.get("grafieken",{})
if g:
    st.markdown('<div class="sec-head">📈 Trends <span class="pill">live</span></div>', unsafe_allow_html=True)
    import plotly.graph_objects as go
    gc=st.columns(2)
    for idx,(k,gr) in enumerate(g.items()):
        fig=go.Figure()
        fig.add_trace(go.Bar(x=gr["labels"],y=gr["waarden"],name=gr["titel"],
            marker_color="#5273ff",opacity=0.85,marker_line_width=0))
        if "doel" in gr:
            fig.add_hline(y=gr["doel"],line_dash="dash",line_color="#f59e0b",
                annotation_text=f"Doel: {gr['doel']}",annotation_position="top left",
                annotation_font=dict(color="#f59e0b",size=11))
        fig.update_layout(title=gr["titel"],height=280,margin=dict(l=20,r=20,t=40,b=20),
            paper_bgcolor="#ffffff",plot_bgcolor="#ffffff",
            font=dict(size=11,color="#5a5a5a"),title_font=dict(color="#121213",size=13),
            yaxis=dict(gridcolor="#f1efed",color="#949494"),xaxis=dict(gridcolor="#f1efed",color="#949494"),
            hoverlabel=dict(bgcolor="#5273ff",font_color="white"))
        with gc[idx%2]: st.plotly_chart(fig, use_container_width=True)

# ─── Kanalen (Website / Mail / WhatsApp / Telefoon) ─────
kanalen = data.get("kanalen", {})
if kanalen:
    st.markdown('<div class="sec-head">📬 Kanalen <span class="pill">live</span></div>', unsafe_allow_html=True)
    kc = st.columns(len(kanalen))
    for idx, (kanaal, info) in enumerate(sorted(kanalen.items())):
        icoon = {"website": "🌐", "mail": "📧", "whatsapp": "💬", "telefoon": "📞"}.get(kanaal.lower(), "📨")
        with kc[idx]:
            st.markdown(f"""
            <div class="kanban-card">
                <div style="font-size:1.8rem;margin-bottom:0.3rem;">{icoon}</div>
                <div style="color:#949494;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.5px;">{kanaal}</div>
                <div style="color:#121213;font-size:1.5rem;font-weight:700;margin:0.2rem 0;">{info.get('verwerkt',0)}</div>
                <div style="color:#5273ff;font-size:0.78rem;">{info.get('bestellingen',0)} bestellingen</div>
            </div>
            """, unsafe_allow_html=True)

# ─── Bottleneck ─────────────────────────────────────────
bn=data.get("bottleneck",{})
if bn and bn.get("tekst"):
    p=bn.get("prioriteit","laag")
    st.markdown(f"""<div class="bn-card {p}"><strong>🔍 Bottleneck-analyse</strong> <span class="s-badge {'grn' if p=='laag' else 'org' if p=='medium' else 'red'}">{p.upper()} PRIORITEIT</span><br>{bn['tekst']}</div>""", unsafe_allow_html=True)

# ─── Inzichten + Kosten in 2 kolommen ────────────────────
cl,cr=st.columns([1,1])
with cl:
    st.markdown('<div class="sec-head">📈 Inzichten</div>', unsafe_allow_html=True)
    # Voortgang check-in
    gt_local = data.get("groei_team", {})
    checkins_local = gt_local.get("checkin_historie", []) if gt_local else []
    if checkins_local:
        laatste = checkins_local[0]
        s = laatste.get("status", "groen")
        c = "#22c55e" if s == "groen" else "#f59e0b" if s == "oranje" else "#ef4444"
        st.markdown(
            f'<div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.8rem 1rem;">'
            f'<div style="font-size:0.72rem;color:var(--text-muted);">Laatste check-in ({laatste.get("datum","")})</div>'
            f'<div style="font-size:0.82rem;color:var(--text);margin-top:4px;">{laatste.get("notities","")}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    # Kostenbesparing
    if data.get("kosten_besparing"):
        st.metric(
            "Kostenbesparing",
            f"€{data['kosten_besparing']:,}",
            delta=f"+{data['kosten_besparing'] - data.get('doelen_vorige_maand',{}).get('kosten_besparing',0):,}"
        )
    st.caption("📈 Bekijk alle inzichten op de Inzichten-pagina.")
with cr:
    if data.get("kosten_besparing"):
        st.markdown('<div class="sec-head">💰 Kostenbesparing</div>', unsafe_allow_html=True)
        v=data.get("doelen_vorige_maand",{}).get("kosten_besparing",0)
        d=data["kosten_besparing"]-v
        st.metric("Prognose deze maand",f"€{data['kosten_besparing']:,}",delta=f"{'+'if d>=0 else ''}€{d:,} vs vorige maand")

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")

# ─── Tijdlijn / Changelog ──────────────────────────────────
if periodes and len(periode_lijst) > 1:
    st.markdown('<div class="sec-head">📈 Voortgang over periodes</div>', unsafe_allow_html=True)
    # Verzamel trends per KPI over alle periodes
    kpi_trends = {}
    for p_naam in periode_lijst:
        p_data = periodes[p_naam]
        for kpi_nm, kpi_info in p_data.get("kpis", {}).items():
            if kpi_nm not in kpi_trends:
                kpi_trends[kpi_nm] = []
            kpi_trends[kpi_nm].append((p_naam, kpi_info.get("waarde", 0), kpi_info.get("doel", 0)))

    for kpi_nm, pts in sorted(kpi_trends.items()):
        if len(pts) < 2:
            continue
        waarden = [p[1] for p in pts]
        doelen = [p[2] for p in pts]
        namen = [p[0] for p in pts]
        # Alleen tonen als er variatie is
        if len(set(str(w) for w in waarden)) <= 1:
            continue
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=namen, y=waarden, mode="lines+markers",
            name=kpi_nm, line=dict(color="#5273ff", width=2.5),
            marker=dict(size=8, color="#5273ff", line=dict(color="#ffffff", width=2))))
        fig.add_trace(go.Scatter(x=namen, y=doelen, mode="lines",
            name="Doel", line=dict(dash="dash", color="#f59e0b", width=1.5)))
        fig.update_layout(title=kpi_nm, height=200, margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(size=10, color="#5a5a5a"), title_font=dict(color="#121213", size=12),
            yaxis=dict(gridcolor="#f1efed", color="#949494"),
            xaxis=dict(gridcolor="#f1efed", color="#949494"),
            showlegend=False, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
