# BigWaves Performance Dashboard
# Dark theme — Dribbble Fireart inspired
import streamlit as st
import json
import os
from pathlib import Path
from io import BytesIO
from pdf_export import genereer_pdf

DATA_DIR = Path(__file__).parent / "data"
st.set_page_config(
    page_title="BigWaves Performance Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
:root {
--bg: #0f1117;
--surface: #1a1d27;
--card: #1e2231;
--border: #2a2e3d;
--border-light: #363b4d;
--text: #edf2f7;
--text-sec: #94a3b8;
--text-muted: #64748b;
--primary: #10b981;
--primary-glow: rgba(16,185,129,0.15);
--primary-light: rgba(16,185,129,0.1);
--green: #10b981;
--orange: #f59e0b;
--red: #ef4444;
--shadow: 0 4px 20px rgba(0,0,0,0.25);
--shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
--radius: 14px;
--radius-sm: 10px;
}
.stApp { background: var(--bg) !important; }
.main > div { padding: 1.2rem 1.8rem !important; max-width: 1440px; margin: 0 auto; }
section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; min-width: 220px !important; max-width: 240px !important; }
.stApp h1 { font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text) !important; }
.stApp h2 { font-size: 1.1rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp p, .stApp li, .stApp label { color: var(--text-sec) !important; font-size: 0.82rem !important; }
.stApp .st-caption { color: var(--text-muted) !important; font-size: 0.72rem !important; }
.stButton button { border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; color: #fff !important; }
.stButton button[kind="primary"]:hover { background: #059669 !important; box-shadow: 0 0 20px var(--primary-glow); }
.stTextInput input { background: var(--surface) !important; color: var(--text) !important; border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important; }
.stTextInput input:focus { border-color: var(--primary) !important; }
.stApp hr { border-color: var(--border) !important; }
.stProgress > div > div { background: var(--primary) !important; }
.stProgress > div { background: var(--primary-light) !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

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
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<span style='font-size:2.2rem;'>🌊</span>", unsafe_allow_html=True)
    st.markdown("## BigWaves")
    st.markdown("<p style='color:var(--text-muted);margin-bottom:1.5rem;'>Performance Dashboard</p>", unsafe_allow_html=True)
    klanten=laad_klanten()
    if not klanten:
        st.warning("Geen klanten. Voeg JSON toe in data/.")
        st.stop()
    kn=st.selectbox("Klant", list(klanten.keys()))
    ww=st.text_input("Wachtwoord", type="password", placeholder="Voer wachtwoord in")
    if st.button("Inloggen", type="primary", use_container_width=True):
        d=klanten[kn]
        if ww==d.get("wachtwoord","demo"):
            st.session_state.ingelogd=True; st.session_state.klant_naam=kn; st.session_state.data=d; st.rerun()
        else: st.error("Onjuist wachtwoord.")
    st.markdown("---")
    st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;margin-top:1rem;'>", unsafe_allow_html=True)
    if st.button("🔐 Admin", use_container_width=True): st.switch_page("pages/2_Admin.py")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

if "ingelogd" not in st.session_state or not st.session_state.ingelogd: login_screen()
data=st.session_state.data; kn=st.session_state.klant_naam

# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sec">Main</div>', unsafe_allow_html=True)
    st.page_link("dashboard.py", label="📊  Dashboard", use_container_width=True)
    st.page_link("pages/1_HITL.py", label="👤  HITL", use_container_width=True)
    st.markdown('<div class="sidebar-sec">Klant</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='padding:0.3rem 0;font-size:0.85rem;color:var(--text);font-weight:500;'>{data.get('logo','🌊')} {kn}</div>", unsafe_allow_html=True)
    st.caption(f"Periode: {data.get('periode','—')}")
    st.caption(f"Update: {data.get('laatste_update','—')}")
    st.divider()
    if st.button("🚪 Uitloggen", use_container_width=True):
        for k in["ingelogd","klant_naam","data"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
    st.divider()
    st.caption("🌊 BigWaves AI-bureau")
    st.caption("datagedreven · menselijk gecheckt")

# ─── Header ──────────────────────────────────────────────
hcol1, hcol2 = st.columns([1.5,1])
with hcol1:
    st.title("📊 Dashboard")
    st.caption(f"Performance overzicht • {data.get('periode','Huidige maand')}")
with hcol2:
    _,b1,b2=st.columns([0.5,1,1])
    with b1:
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-child(2) button p {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            gap: 0px !important;
            line-height: 1.2 !important;
        }
        div[data-testid="column"]:nth-child(2) button p span:first-child {
            font-size: 1.2rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("📄\nPDF", type="primary", use_container_width=True):
            try:
                pb=genereer_pdf(data)
                st.download_button("📥 Download",pb,file_name=f"BigWaves_{data['naam'].replace(' ','_')}.pdf",mime="application/pdf",use_container_width=True)
            except Exception as e: st.error(f"Fout: {e}")
    with b2:
        st.button("🔔 Notifications", type="secondary", use_container_width=True)

# ─── KPI Cards ──────────────────────────────────────────
kpis=data.get("kpis",{})
def se(s): return {"groen":"🟢","oranje":"🟠","rood":"🔴"}.get(s,"⚪")
def tc(t):
    if "+" in t or "lager" in t.lower(): return "up"
    if "-" in t: return "down"
    return "neutral"

if kpis:
    kpi_cols = st.columns(4)
    colors = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}
    for i, (kpi, info) in enumerate(list(kpis.items())[:4]):
        sts = info.get("status", "groen")
        w = info["waarde"]
        e = info.get("eenheid", "")
        dsp = f"{w:,}" if isinstance(w, int) else str(w)
        if e == "euro": dsp = f"€{w:,}" if isinstance(w, int) else f"€{w}"
        elif e == "seconden": dsp = f"{w}s"
        tc = "up" if "+" in info.get("trend","") or "lager" in info.get("trend","").lower() else "down" if "-" in info.get("trend","") else ""
        arrow = "↑" if tc == "up" else "↓" if tc == "down" else "→"
        clr = colors.get(sts, "#10b981")
        with kpi_cols[i]:
            st.markdown(f"""
            <div style="background:#1e2231; border:1px solid #2a2e3d; border-radius:14px; padding:1.1rem 1.3rem; box-shadow:0 2px 8px rgba(0,0,0,0.2); margin-bottom:0.5rem;">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.6rem;">
                    <div style="width:38px; height:38px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.15);">{se(sts)}</div>
                    <div style="color:#64748b; font-size:1.1rem; cursor:pointer;">⋯</div>
                </div>
                <div style="font-size:0.72rem; color:#64748b; font-weight:500; text-transform:uppercase; letter-spacing:0.4px;">{kpi}</div>
                <div style="font-size:1.6rem; font-weight:700; color:#edf2f7; line-height:1.2; margin:2px 0 3px 0;">{dsp}</div>
                <div style="font-size:0.68rem; color:#64748b;">Doel: {info['doel']}</div>
                <div style="font-size:0.68rem; margin-top:5px; font-weight:500; color:{'#10b981' if tc=='up' else '#ef4444' if tc=='down' else '#64748b'};">{arrow} {info.get('trend','')}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── Grafieken ──────────────────────────────────────────
g=data.get("grafieken",{})
if g:
    st.markdown('<div class="sec-head">📈 Trends <span class="pill">live</span></div>', unsafe_allow_html=True)
    import plotly.graph_objects as go
    gc=st.columns(2)
    for idx,(k,gr) in enumerate(g.items()):
        fig=go.Figure()
        fig.add_trace(go.Bar(x=gr["labels"],y=gr["waarden"],name=gr["titel"],
            marker_color="#10b981",opacity=0.85,marker_line_width=0))
        if "doel" in gr:
            fig.add_hline(y=gr["doel"],line_dash="dash",line_color="#f59e0b",
                annotation_text=f"Doel: {gr['doel']}",annotation_position="top left",
                annotation_font=dict(color="#f59e0b",size=11))
        fig.update_layout(title=gr["titel"],height=280,margin=dict(l=20,r=20,t=40,b=20),
            paper_bgcolor="#1e2231",plot_bgcolor="#1e2231",
            font=dict(size=11,color="#94a3b8"),title_font=dict(color="#edf2f7",size=13),
            yaxis=dict(gridcolor="#2a2e3d",color="#64748b"),xaxis=dict(gridcolor="#2a2e3d",color="#64748b"),
            hoverlabel=dict(bgcolor="#10b981",font_color="white"))
        with gc[idx%2]: st.plotly_chart(fig,use_container_width=True)

# ─── Bottleneck ─────────────────────────────────────────
bn=data.get("bottleneck",{})
if bn and bn.get("tekst"):
    p=bn.get("prioriteit","laag")
    st.markdown(f"""<div class="bn-card {p}"><strong>🔍 Bottleneck-analyse</strong> <span class="s-badge {'grn' if p=='laag' else 'org' if p=='medium' else 'red'}">{p.upper()} PRIORITEIT</span><br>{bn['tekst']}</div>""", unsafe_allow_html=True)

# ─── HITL + Kosten in 2 kolommen ────────────────────────
cl,cr=st.columns([1,1])
with cl:
    hitl=data.get("hitl_detail")
    if hitl:
        st.markdown('<div class="sec-head">👤 Human In The Loop</div>', unsafe_allow_html=True)
        hr=data.get("kpis",{}).get("HITL-ratio",{}).get("waarde",0)
        hc=st.columns(4)
        with hc[0]: st.metric("Totaal",f"{hitl['totaal_acties']:,}")
        with hc[1]: st.metric("👤 Check",f"{hitl['menselijke_check']:,}")
        with hc[2]: st.metric("🤖 Auto",f"{hitl['geautomatiseerd']:,}")
        with hc[3]: st.metric("⏱ Uren",f"{hitl['bespaarde_uren']}u")
        st.progress(min(int(hr)/100,1.0))
        st.caption(f"HITL-ratio: {hr}% — {'✅ onder doel' if hr<=data.get('kpis',{}).get('HITL-ratio',{}).get('doel',100) else '⚠️ boven doel'}")
        st.caption("👤 Bekijk HITL-detailpagina voor uitsplitsing per categorie.")
with cr:
    if data.get("kosten_besparing"):
        st.markdown('<div class="sec-head">💰 Kostenbesparing</div>', unsafe_allow_html=True)
        v=data.get("doelen_vorige_maand",{}).get("kosten_besparing",0)
        d=data["kosten_besparing"]-v
        st.metric("Prognose deze maand",f"€{data['kosten_besparing']:,}",delta=f"{'+'if d>=0 else ''}€{d:,} vs vorige maand")

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
