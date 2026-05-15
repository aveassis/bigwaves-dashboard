# BigWaves Inzichten Pagina — Voortgang · Resultaten · Status
import streamlit as st

if "data" not in st.session_state:
    st.switch_page("dashboard.py")

data = st.session_state.data
klant_naam = st.session_state.klant_naam

st.set_page_config(page_title="Inzichten — BigWaves", page_icon="📈", layout="wide")

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
rel="stylesheet">
<style>
* { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
:root {
--bg:#0f1117; --surface:#1a1d27; --card:#1e2231; --border:#2a2e3d;
--text:#edf2f7; --text-sec:#94a3b8; --text-muted:#64748b;
--primary:#10b981; --primary-light:rgba(16,185,129,0.1);
--shadow:0 2px 8px rgba(0,0,0,0.2); --radius:14px; --radius-sm:10px;
}
.stApp { background: var(--bg) !important; }
.stApp h1 { font-size: 1.4rem; font-weight: 700; color: var(--text); }
.stApp h2 { font-size: 1.1rem; font-weight: 600; color: var(--text); }
.stApp h3 { font-size: 0.95rem; font-weight: 600; color: var(--text); }
.stApp p, .stApp li, .stApp label { color: var(--text-sec) !important; font-size: 0.82rem !important; }
.stApp .st-caption { color: var(--text-muted) !important; font-size: 0.72rem !important; }
.stButton button { border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; color: #fff
!important; }
.stButton button[kind="primary"]:hover { background: #059669 !important; }
.stApp hr { border-color: var(--border) !important; }
.stProgress > div > div { background: var(--primary) !important; }
.stProgress > div { background: var(--primary-light) !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }

.insight-card {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; padding: 1.2rem !important;
    box-shadow: var(--shadow) !important;
    margin-bottom: 0.8rem !important;
}
.insight-card .big-number { font-size: 2rem !important; font-weight: 700 !important; color: var(--primary); }
.insight-card .label { font-size: 0.72rem !important; color: var(--text-muted) !important; text-transform: uppercase;
letter-spacing: 0.3px; }
.sec-head {
    font-size: 0.9rem !important; font-weight: 600 !important; color: var(--text) !important;
    margin: 1.2rem 0 0.8rem 0 !important;
}
.timeline-item {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; padding: 0.8rem 1rem !important;
    margin-bottom: 0.6rem !important;
    border-left: 3px solid #10b981 !important;
}
.timeline-item.amber { border-left-color: #f59e0b !important; }
.timeline-item.red { border-left-color: #ef4444 !important; }
.result-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.5rem 0; border-bottom: 1px solid var(--border);
}
</style>
""", unsafe_allow_html=True)

st.title("📈 Inzichten")
st.caption(f"{klant_naam} • Wat er speelt, wat het oplevert, waar het staat")

# ─── Helper functies ────────────────────────────────────
def status_icon(s):
    return {"groen": "🟢", "oranje": "🟠", "rood": "🔴"}.get(s, "⚪")

def status_color(s):
    return {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}.get(s, "#64748b")

# ─── 1. VOORTGANG — Check-in historie & workflow status ─
gt = data.get("groei_team", {})
checkins = gt.get("checkin_historie", []) if gt else []
workflows = gt.get("workflows", []) if gt else []
bn = data.get("bottleneck", {})

st.markdown('<div class="sec-head">📋 Voortgang</div>', unsafe_allow_html=True)

# Workflow overzicht (compact)
if workflows:
    wcols = st.columns(min(len(workflows), 4))
    for i, wf in enumerate(workflows[:4]):
        s = wf.get("status", "onbekend")
        c = status_color(s)
        with wcols[i]:
            st.markdown(f"""<div class="insight-card" style="text-align:center">
                <div class="big-number" style="color:{c}">{status_icon(s)}</div>
                <div class="label">{wf.get('naam','Workflow')}</div>
                <div style="font-size:0.72rem;color:var(--text-muted);margin-top:4px">{s.title()}</div>
            </div>""", unsafe_allow_html=True)

# Laatste check-ins (timeline)
if checkins:
    st.markdown('<div style="font-size:0.82rem;font-weight:600;color:var(--text);margin:0.6rem 0 0.4rem 0">📅 Check-in historie</div>', unsafe_allow_html=True)
    for ch in checkins[:5]:
        s = ch.get("status", "groen")
        cls = "timeline-item"
        if s == "oranje": cls += " amber"
        elif s == "rood": cls += " red"
        st.markdown(f"""<div class="{cls}">
            <div style="display:flex;justify-content:space-between">
                <strong style="color:var(--text)">{ch.get('datum','')}</strong>
                <span>{status_icon(s)} {s.title()}</span>
            </div>
            <div style="font-size:0.78rem;color:var(--text-sec);margin-top:4px">{ch.get('notitie','')}</div>
        </div>""", unsafe_allow_html=True)
else:
    st.info("Nog geen check-ins geregistreerd.")

# Bottleneck
if bn and bn.get("tekst"):
    p = bn.get("prioriteit", "laag")
    st.markdown(f"""<div class="bn-card {p}" style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.8rem 1rem;margin-top:0.6rem">
        <strong style="color:var(--text)">🔍 Bottleneck</strong>
        <span class="s-badge" style="color:{status_color(p)}">{p.upper()}</span>
        <div style="font-size:0.78rem;color:var(--text-sec);margin-top:4px">{bn['tekst']}</div>
    </div>""", unsafe_allow_html=True)

# ─── 2. RESULTATEN — KPI's & Kanalen ───────────────────
st.markdown('<div class="sec-head">📊 Resultaten</div>', unsafe_allow_html=True)

kpis = data.get("kpis", {})
if kpis:
    # KPI metrics in 2 rijen
    kpi_items = list(kpis.items())
    for row_start in range(0, len(kpi_items), 4):
        row = kpi_items[row_start:row_start+4]
        cols = st.columns(4)
        for i, (k, v) in enumerate(row):
            val = v.get("waarde", "—") if isinstance(v, dict) else v
            doel = v.get("doel", "") if isinstance(v, dict) else ""
            delta = v.get("delta", "") if isinstance(v, dict) else ""
            with cols[i]:
                st.markdown(f"""<div class="insight-card" style="text-align:center">
                    <div class="big-number" style="color:var(--primary)">{val}</div>
                    <div class="label">{k}</div>
                    {f'<div style="font-size:0.72rem;color:var(--text-muted)">Doel: {doel}</div>' if doel else ''}
                    {f'<div style="font-size:0.72rem;color:var(--text-sec)">{delta}</div>' if delta else ''}
                </div>""", unsafe_allow_html=True)

# Kanalen
kanalen = data.get("kanalen", {})
if kanalen:
    st.markdown('<div style="font-size:0.82rem;font-weight:600;color:var(--text);margin:0.6rem 0 0.4rem 0">📡 Kanalen</div>', unsafe_allow_html=True)
    for k, v in kanalen.items():
        if isinstance(v, dict):
            verwerkt = v.get("verwerkt", "—")
            bestellingen = v.get("bestellingen", "—")
            st.markdown(f"""<div class="result-row">
                <span style="color:var(--text)">{k.title()}</span>
                <span style="color:var(--text-sec);font-size:0.82rem">
                    {verwerkt} verwerkt · {bestellingen} bestellingen
                </span>
            </div>""", unsafe_allow_html=True)

# ─── 3. STATUS — Pakket, Health, Update ──────────────────
st.markdown('<div class="sec-head">🏷️ Status</div>', unsafe_allow_html=True)

scols = st.columns(3)
with scols[0]:
    pakket = gt.get("pakket", "—") if gt else "—"
    st.markdown(f"""<div class="insight-card" style="text-align:center">
        <div class="big-number" style="font-size:1.4rem">{pakket}</div>
        <div class="label">Pakket</div>
    </div>""", unsafe_allow_html=True)

with scols[1]:
    health = data.get("health_score", "—")
    hcolor = "#10b981" if isinstance(health, (int, float)) and health >= 80 else "#f59e0b" if isinstance(health, (int, float)) and health >= 60 else "#ef4444"
    st.markdown(f"""<div class="insight-card" style="text-align:center">
        <div class="big-number" style="color:{hcolor}">{health}{'%' if isinstance(health, (int, float)) else ''}</div>
        <div class="label">Health</div>
    </div>""", unsafe_allow_html=True)

with scols[2]:
    update = data.get("update_datum", "—")
    st.markdown(f"""<div class="insight-card" style="text-align:center">
        <div class="big-number" style="font-size:1.4rem">{update}</div>
        <div class="label">Laatste update</div>
    </div>""", unsafe_allow_html=True)

# Kostenbesparing
if data.get("kosten_besparing"):
    st.markdown(f"""<div class="insight-card" style="margin-top:0.6rem">
        <div class="label">💰 Geschatte kostenbesparing</div>
        <div class="big-number" style="font-size:1.6rem">€{data['kosten_besparing']:,}</div>
    </div>""", unsafe_allow_html=True)

st.caption("🌊 BigWaves AI-bureau · datagedreven · menselijk gecheckt")
