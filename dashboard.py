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

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">""", unsafe_allow_html=True)
# Accentkleur per klant
accent = data.get("accent_kleur", "#10b981")
st.markdown(f"""<style>
:root {{
--primary: {accent};
--primary-glow: rgba(16,185,129,0.15);
--primary-light: rgba(16,185,129,0.1);
--bg: #0f1117;
--surface: #1a1d27;
--card: #1e2231;
--border: #2a2e3d;
--border-light: #363b4d;
--text: #edf2f7;
--text-sec: #94a3b8;
--text-muted: #64748b;
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
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; }
.stButton button[kind="primary"] p { color: #000 !important; }
.stButton button[kind="primary"]:hover { background: #059669 !important; }
.stButton button[kind="primary"]:hover p { color: #fff !important; }
.stTextInput input { background: var(--surface) !important; color: var(--text) !important; border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important; }
.stTextInput input:focus { border-color: var(--primary) !important; }
.stApp hr { border-color: var(--border) !important; }
.stProgress > div > div { background: var(--primary) !important; }
.stProgress > div { background: var(--primary-light) !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
button[title*="sidebar"] { display: none !important; }
button[aria-label*="sidebar"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] svg { display: none !important; }

/* KPI card styling */
.kpi-box {
    background: #1e2231;
    border: 1px solid #2a2e3d;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    margin-bottom: 0.5rem;
    transition: all 0.25s ease;
}
.kpi-box:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    transform: translateY(-2px);
    border-color: #363b4d;
}
.kpi-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.6rem;
}
.kpi-icon {
    width: 38px; height: 38px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.15);
}
.kpi-dots { color: #64748b; font-size: 1.1rem; cursor: pointer; }
.kpi-label {
    font-size: 0.72rem; color: #64748b; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.4px;
}
.kpi-val {
    font-size: 1.6rem; font-weight: 700; color: #edf2f7;
    line-height: 1.2; margin: 2px 0 3px 0;
}
.kpi-target { font-size: 0.68rem; color: #64748b; }
.kpi-foot { font-size: 0.68rem; margin-top: 5px; font-weight: 500; }
.kpi-foot.up { color: #10b981; }
.kpi-foot.down { color: #ef4444; }
.kpi-foot.neutral { color: #64748b; }
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
    # Hide sidebar on login
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    .main > div { padding: 1.2rem 1.8rem !important; max-width: 1440px; margin: 0 auto; }
    button[kind="header"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    section.main { margin-left: 0 !important; }
    </style>
    """, unsafe_allow_html=True)
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

# ─── Periode selector ─────────────────────────────────────
# Check of de data periodes heeft (nieuw formaat) of plat (oud formaat)
periodes = data.get("periodes", None)
if periodes:
    periode_lijst = list(periodes.keys())
    # Eerste keer of bij switchen
    if "huidige_periode" not in st.session_state or st.session_state.klant_naam != kn:
        st.session_state.huidige_periode = periode_lijst[0]
    # Selector in sidebar
    with st.sidebar:
        gekozen = st.selectbox("Periode", periode_lijst,
            index=periode_lijst.index(st.session_state.huidige_periode) if st.session_state.huidige_periode in periode_lijst else 0,
            key="periode_selector")
        if gekozen != st.session_state.huidige_periode:
            st.session_state.huidige_periode = gekozen
            st.rerun()
    # Data uit gekozen periode halen
    pd = periodes[st.session_state.huidige_periode]
    data.update(pd)  # voeg periode-data toe aan hoofd-data
    data["periode"] = st.session_state.huidige_periode
else:
    # Oud formaat: platte data, geen periodes
    pass

# ─── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sec">Main</div>', unsafe_allow_html=True)
    st.page_link("dashboard.py", label="📊  Dashboard", use_container_width=True)
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
    # Dark/light toggle
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True
    dark = st.toggle("🌙 Donker", value=st.session_state.dark_mode, key="dark_toggle")
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

    # Light mode CSS override
    if not st.session_state.dark_mode:
        st.markdown("""<style>
        :root {
        --bg: #f5f7fa !important;
        --surface: #ffffff !important;
        --card: #ffffff !important;
        --border: #e8ecf1 !important;
        --border-light: #d1d5db !important;
        --text: #1a1d23 !important;
        --text-sec: #6b7280 !important;
        --text-muted: #9ca3af !important;
        }
        section[data-testid="stSidebar"] { background: var(--surface) !important; }
        .kpi-box { background: var(--card) !important; }
        .kpi-val { color: var(--text) !important; }
        .kpi-label { color: var(--text-muted) !important; }
        .kpi-target { color: var(--text-muted) !important; }
        div[data-testid="column"]:nth-child(2) button { background: var(--surface) !important; border-color: var(--border) !important; color: var(--text) !important; }
        </style>""", unsafe_allow_html=True)
    st.divider()
    st.caption("🌊 BigWaves AI-bureau")
    st.caption("datagedreven · menselijk gecheckt")

# ─── Header ──────────────────────────────────────────────
hcol1, hcol2 = st.columns([1.5,1])
with hcol1:
    logo = data.get("logo", "🌊")
    accent = data.get("accent_kleur", "#10b981")
    st.markdown(f"<div style='display:flex;align-items:center;gap:0.8rem;'><span style='font-size:2.5rem;'>{logo}</span><div><h1 style='margin:0;'>Dashboard</h1><p style='margin:0;color:var(--text-muted);font-size:0.82rem;'>Performance overzicht • {data.get('periode','Huidige maand')}</p></div></div>", unsafe_allow_html=True)
with hcol2:
    with st.container():
        st.markdown("""
        <style>
        div[data-testid="column"]:nth-child(2) button, div[data-testid="column"]:nth-child(3) button {
            height: 50px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: nowrap !important;
            min-width: 140px !important;
        }
        div[data-testid="column"]:nth-child(2) button {
            background: #0f1117 !important;
            border: 1px solid #2a2e3d !important;
            color: #edf2f7 !important;
        }
        div[data-testid="column"]:nth-child(2) button:hover {
            background: #1a1d27 !important;
            border-color: #363b4d !important;
        }
        </style>
        """, unsafe_allow_html=True)
        _,b1,b2=st.columns([0.1,1,1])
        with b1:
            if st.button("📄 PDF", type="secondary", use_container_width=True):
                try:
                    pb=genereer_pdf(data)
                    st.download_button("📥 Download",pb,file_name=f"BigWaves_{data['naam'].replace(' ','_')}.pdf",mime="application/pdf",use_container_width=True)
                except Exception as e: st.error(f"Fout: {e}")
        with b2:
            # Notificaties genereren uit data
            alerts = []
            kpi_data = data.get("kpis", {})
            for name, info in kpi_data.items():
                sts = info.get("status", "groen")
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
            if st.button(f"🔔 Notificaties{badge}", type="secondary", use_container_width=True):
                st.session_state.show_notifications = not st.session_state.get("show_notifications", False)

        # Notificatie paneel
        if st.session_state.get("show_notifications", False):
            with st.container():
                st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);border-radius:14px;padding:1rem;margin-bottom:0.5rem;max-height:350px;overflow-y:auto;">
                    <div style="font-size:0.85rem;font-weight:600;color:var(--text);margin-bottom:0.5rem;">🔔 Meldingen</div>
                    {''.join([f'<div style="padding:0.4rem 0;border-bottom:1px solid var(--border);font-size:0.8rem;color:var(--text-sec);">{a[0]} {a[1]}</div>' for a in alerts[:8]])}
                </div>""", unsafe_allow_html=True)
                if st.button("✅ Markeer als gelezen", use_container_width=True):
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
            st.markdown(f"""<div class="kpi-box">
                <div class="kpi-top"><div class="kpi-icon">{se(sts)}</div><div class="kpi-dots">⋯</div></div>
                <div class="kpi-label">{kpi}</div>
                <div class="kpi-val">{dsp}</div>
                <div class="kpi-target">Doel: {info['doel']}</div>
                <div class="kpi-foot {tc}">{arrow} {info.get('trend','')}</div>
            </div>""", unsafe_allow_html=True)

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
