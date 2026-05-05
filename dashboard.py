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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*{font-family:'Inter',system-ui,-apple-system,sans-serif!important;}

:root{
--bg:#0f1117;
--surface:#1a1d27;
--card:#1e2231;
--border:#2a2e3d;
--border-light:#363b4d;
--text:#edf2f7;
--text-sec:#94a3b8;
--text-muted:#64748b;
--primary:#10b981;
--primary-glow:rgba(16,185,129,0.15);
--primary-light:rgba(16,185,129,0.1);
--green:#10b981;
--orange:#f59e0b;
--red:#ef4444;
--shadow:0 4px 20px rgba(0,0,0,0.25);
--shadow-sm:0 2px 8px rgba(0,0,0,0.2);
--radius:14px;
--radius-sm:10px;
}

.stApp{background:var(--bg)!important;}
.main > div{padding:1.2rem 1.8rem!important;max-width:1440px;margin:0 auto;}
.stApp,.st-emotion-cache-1avcm0n,.st-emotion-cache-1r4qj8v{background:var(--bg)!important;}

/* Sidebar */
section[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;min-width:220px!important;max-width:240px!important;}
section[data-testid="stSidebar"] .st-emotion-cache-16txtl3{padding:1.2rem!important;}
.sidebar-logo{font-size:1.4rem;font-weight:700;color:var(--text);margin-bottom:1.8rem;display:flex;align-items:center;gap:0.6rem;}
.sidebar-logo span{color:var(--primary);}
.sidebar-sec{font-size:0.65rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.8px;margin:1.2rem 0 0.6rem 0;font-weight:600;}

/* Typography */
.stApp h1{font-size:1.4rem!important;font-weight:700!important;color:var(--text)!important;margin-bottom:0.15rem!important;}
.stApp h2{font-size:1.1rem!important;font-weight:600!important;color:var(--text)!important;}
.stApp h3{font-size:0.95rem!important;font-weight:600!important;color:var(--text)!important;}
.stApp p,.stApp li,.stApp span,.stApp label{color:var(--text-sec)!important;font-size:0.82rem!important;}
.stApp .st-caption,.stApp caption{color:var(--text-muted)!important;font-size:0.72rem!important;}

/* KPI Cards */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin:0.5rem 0 1.5rem 0;}
.kpi-card{
background:var(--card)!important;border-radius:var(--radius)!important;
padding:1.1rem 1.3rem!important;border:1px solid var(--border)!important;
box-shadow:var(--shadow-sm)!important;transition:all 0.25s ease;position:relative;overflow:hidden;
}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--primary);opacity:0;transition:opacity 0.25s;}
.kpi-card:hover::before{opacity:1;}
.kpi-card:hover{box-shadow:var(--shadow)!important;transform:translateY(-2px);border-color:var(--border-light);}
.kpi-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;}
.kpi-icon{
width:38px;height:38px;border-radius:12px;display:flex;align-items:center;justify-content:center;
font-size:1.1rem;background:var(--primary-light);border:1px solid rgba(16,185,129,0.15);
}
.kpi-dots{color:var(--text-muted);font-size:1.1rem;cursor:pointer;opacity:0.6;transition:opacity 0.2s;}
.kpi-dots:hover{opacity:1;}
.kpi-label{font-size:0.72rem!important;color:var(--text-muted)!important;font-weight:500!important;text-transform:uppercase;letter-spacing:0.4px;}
.kpi-val{font-size:1.6rem!important;font-weight:700!important;color:var(--text)!important;line-height:1.2;margin:2px 0 3px 0;}
.kpi-target{font-size:0.68rem!important;color:var(--text-muted)!important;}
.kpi-foot{font-size:0.68rem!important;margin-top:5px;display:flex;align-items:center;gap:4px;font-weight:500;}
.kpi-foot.up{color:var(--green)!important;}
.kpi-foot.down{color:var(--red)!important;}
.kpi-foot.neutral{color:var(--text-muted)!important;}

/* Section headers */
.sec-head{
font-size:0.9rem!important;font-weight:600!important;color:var(--text)!important;
margin:1.2rem 0 0.8rem 0!important;display:flex;align-items:center;gap:0.5rem;
}
.sec-head .pill{
background:var(--primary-light);color:var(--primary);font-size:0.6rem;
padding:2px 9px;border-radius:20px;font-weight:600;letter-spacing:0.3px;border:1px solid rgba(16,185,129,0.15);
}

/* Bottleneck card */
.bn-card{
background:var(--card)!important;border-radius:var(--radius)!important;
padding:1rem 1.2rem!important;border:1px solid var(--border)!important;
border-left:4px solid var(--orange)!important;box-shadow:var(--shadow-sm)!important;
margin:0.3rem 0 1rem 0!important;font-size:0.85rem!important;color:var(--text-sec)!important;
}
.bn-card.hoog{border-left-color:var(--red)!important;}
.bn-card.medium{border-left-color:var(--orange)!important;}
.bn-card.laag{border-left-color:var(--green)!important;}
.bn-card strong{color:var(--text)!important;}

/* Status badge */
.s-badge{display:inline-block;padding:2px 10px;border-radius:20px;font-size:0.62rem;font-weight:600;letter-spacing:0.3px;}
.s-badge.grn{background:var(--primary-light);color:var(--primary);}
.s-badge.org{background:rgba(245,158,11,0.12);color:var(--orange);}
.s-badge.red{background:rgba(239,68,68,0.12);color:var(--red);}
.s-badge.purp{background:rgba(139,92,246,0.12);color:#8b5cf6;}

/* Login */
.login-box{
max-width:380px!important;margin:5rem auto!important;padding:2rem!important;
background:var(--card)!important;border-radius:var(--radius)!important;
border:1px solid var(--border)!important;box-shadow:var(--shadow)!important;text-align:center!important;
}
.login-box h2,.login-box h3,.login-box h4{color:var(--text)!important;}

/* Buttons */
.stButton button{border-radius:var(--radius-sm)!important;font-weight:500!important;font-size:0.85rem!important;padding:0.35rem 1rem!important;transition:all 0.2s;}
.stButton button[kind="primary"]{background:var(--primary)!important;border:1px solid var(--primary)!important;color:#fff!important;}
.stButton button[kind="primary"]:hover{background:#059669!important;box-shadow:0 0 20px var(--primary-glow);}
.stButton button[kind="secondary"]{background:transparent!important;border:1px solid var(--border)!important;color:var(--text-sec)!important;}
.stButton button[kind="secondary"]:hover{border-color:var(--border-light)!important;color:var(--text)!important;}

/* Inputs */
.stTextInput input{background:var(--surface)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:var(--radius-sm)!important;}
.stTextInput input:focus{border-color:var(--primary)!important;box-shadow:0 0 0 3px var(--primary-glow)!important;}

/* Metrics */
[data-testid="stMetricLabel"] p{color:var(--text-muted)!important;font-size:0.72rem!important;}
[data-testid="stMetricValue"]{color:var(--text)!important;font-weight:700!important;font-size:1.3rem!important;}
[data-testid="stMetricDelta"]{color:var(--green)!important;font-size:0.72rem!important;}
.stApp hr{border-color:var(--border)!important;}
.stProgress>div>div{background:var(--primary)!important;border-radius:10px!important;}
.stProgress>div{background:var(--primary-light)!important;border-radius:10px!important;}
.stSelectbox div[data-baseweb="select"]{border-color:var(--border)!important;background:var(--surface)!important;}

/* Page links */
.stPageLink{color:var(--text-sec)!important;font-size:0.85rem!important;padding:0.3rem 0!important;}
.stPageLink:hover{color:var(--primary)!important;}

/* Hide Streamlit */
#MainMenu{visibility:hidden!important;}footer{visibility:hidden!important;}.stDeployButton{display:none!important;}
::selection{background:rgba(16,185,129,0.3);}
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
    _,b1,b2=st.columns([1,1,1])
    with b1:
        if st.button("📄 PDF", type="primary", use_container_width=True):
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
    st.markdown("<div class='kpi-grid'>", unsafe_allow_html=True)
    for kpi,info in list(kpis.items())[:4]:
        sts=info.get("status","groen"); w=info["waarde"]; e=info.get("eenheid","")
        dsp=f"{w:,}" if isinstance(w,int) else str(w)
        if e=="euro": dsp=f"€{w:,}" if isinstance(w,int) else f"€{w}"
        elif e=="seconden": dsp=f"{w}s"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-top">
                <div class="kpi-icon">{se(sts)}</div>
                <div class="kpi-dots">⋯</div>
            </div>
            <div class="kpi-label">{kpi}</div>
            <div class="kpi-val">{dsp}</div>
            <div class="kpi-target">Doel: {info['doel']}</div>
            <div class="kpi-foot {tc(info.get('trend',''))}">{"↑" if tc(info.get('trend',''))=="up" else "↓" if tc(info.get('trend',''))=="down" else "→"} {info.get('trend','')}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

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
