# BigWaves Inzichten Pagina — Voortgang · Resultaten · Status
import streamlit as st

if "data" not in st.session_state:
    st.switch_page("dashboard.py")

data = st.session_state.data
klant_naam = st.session_state.klant_naam

st.set_page_config(page_title="Inzichten — BigWaves", page_icon="📈", layout="wide")

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
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
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; color: #fff !important; }
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
.insight-card .big-number { font-size: 2rem !important; font-weight: 700 !important; color: var(--text) !important; }
.insight-card .label { font-size: 0.72rem !important; color: var(--text-muted) !important; text-transform: uppercase; letter-spacing: 0.3px; }
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
@media screen and (max-width: 768px) {
    .insight-card { padding: 0.8rem !important; }
    .sec-head { font-size: 0.82rem !important; margin: 0.8rem 0 0.5rem 0 !important; }
    .result-row { font-size: 0.78rem !important; }
}
@media screen and (max-width: 480px) {
    .insight-card { padding: 0.6rem !important; }
    .big-number { font-size: 1.2rem !important; }
    .label { font-size: 0.65rem !important; }
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

st.markdown('<div class="sec-head">🚀 Voortgang</div>', unsafe_allow_html=True)

cols = st.columns([1, 1])
with cols[0]:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Check-in historie</div>', unsafe_allow_html=True)
    if checkins:
        for ci in checkins[:5]:
            s = ci.get("status", "groen")
            border = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}.get(s, "#10b981")
            st.markdown(
                f'<div class="timeline-item" style="border-left-color:{border};">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-size:0.78rem;color:var(--text-sec);">{ci.get("datum","")}</span>'
                f'<span style="font-size:0.7rem;color:var(--text-muted);">{ci.get("type","")}</span>'
                f'</div>'
                f'<div style="font-size:0.82rem;color:var(--text);margin-top:4px;">{ci.get("notities","")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        if len(checkins) > 5:
            st.caption(f"+{len(checkins)-5} eerdere check-ins")
    else:
        st.caption("Nog geen check-in historie beschikbaar.")
    st.markdown('</div>', unsafe_allow_html=True)

with cols[1]:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Workflow status</div>', unsafe_allow_html=True)
    if workflows:
        for wf in workflows:
            s = wf.get("status", "groen")
            c = status_color(s)
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;padding:0.5rem 0;border-bottom:1px solid var(--border);">'
                f'<div><span style="color:var(--text);font-size:0.82rem;">{wf.get("naam","")}</span>'
                f'<br><span style="font-size:0.7rem;color:var(--text-muted);">{wf.get("items_verwerkt",0)} items verwerkt</span></div>'
                f'<span style="color:{c};font-size:1rem;">{status_icon(s)}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("Geen actieve workflows.")
    st.markdown('</div>', unsafe_allow_html=True)

# Bottleneck
if bn and bn.get("tekst"):
    bp = bn.get("prioriteit", "laag")
    b_color = {"laag": "#10b981", "medium": "#f59e0b", "hoog": "#ef4444"}.get(bp, "#10b981")
    st.markdown(
        f'<div class="insight-card" style="border-left:3px solid {b_color};">'
        f'<div class="label">🔍 Signalering</div>'
        f'<div style="font-size:0.82rem;color:var(--text);margin-top:4px;">{bn["tekst"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

# ─── 2. RESULTATEN — KPI's & kanalen ────────────────────
st.markdown('<div class="sec-head">📊 Resultaten</div>', unsafe_allow_html=True)

kpis = data.get("kpis", {})
if kpis:
    rcols = st.columns(2)
    for i, (kpi, info) in enumerate(list(kpis.items())):
        w = info.get("waarde", 0)
        e = info.get("eenheid", "")
        dsp = f"€{w:,}" if e == "euro" else f"{w}{'s' if e=='seconden' else '%' if e=='%' else ''}"
        if e not in ("euro", "seconden", "%"):
            dsp = f"{w:,}" if isinstance(w, int) else str(w)
        s = info.get("status", "groen")
        with rcols[i % 2]:
            st.markdown(
                f'<div class="insight-card">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div class="label">{kpi}</div>'
                f'<span>{status_icon(s)}</span>'
                f'</div>'
                f'<div class="big-number">{dsp}</div>'
                f'<div style="font-size:0.72rem;color:var(--text-muted);">Doel: {info.get("doel","")} | {info.get("trend","")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# Kanalen
kanalen = data.get("kanalen", {})
if kanalen:
    st.markdown('<div class="sec-head">📬 Kanalen</div>', unsafe_allow_html=True)
    kc = st.columns(len(kanalen))
    icoon_map = {"website": "🌐", "mail": "📧", "whatsapp": "💬", "telefoon": "📞"}
    for idx, (kanaal, info) in enumerate(sorted(kanalen.items())):
        with kc[idx]:
            st.markdown(
                f'<div class="insight-card" style="text-align:center;">'
                f'<div style="font-size:1.8rem;">{icoon_map.get(kanaal.lower(), "📨")}</div>'
                f'<div class="label">{kanaal}</div>'
                f'<div class="big-number">{info.get("verwerkt",0)}</div>'
                f'<div style="color:#10b981;font-size:0.78rem;">{info.get("bestellingen",0)} bestellingen</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ─── 3. STATUS — Pakket, health, periode informatie ────
st.markdown('<div class="sec-head">✅ Status</div>', unsafe_allow_html=True)

stat_cols = st.columns(3)

with stat_cols[0]:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Pakket</div>', unsafe_allow_html=True)
    if gt:
        pkt = gt.get("pakket", "—")
        st.markdown(f'<div class="big-number">{pkt}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.72rem;color:var(--text-muted);">'
            f'Sinds {gt.get("sinds","—")} · {gt.get("status","")}'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        st.caption("Geen pakketgegevens.")
    st.markdown('</div>', unsafe_allow_html=True)

with stat_cols[1]:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Gezondheid</div>', unsafe_allow_html=True)
    health = gt.get("health_score") if gt else None
    if health is not None:
        c = "#10b981" if health >= 80 else "#f59e0b" if health >= 60 else "#ef4444"
        st.markdown(f'<div class="big-number" style="color:{c};">{health}%</div>', unsafe_allow_html=True)
        st.progress(min(health / 100, 1.0))
    else:
        st.caption("Nog niet beschikbaar.")
    st.markdown('</div>', unsafe_allow_html=True)

with stat_cols[2]:
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Updates</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.82rem;color:var(--text);">Periode: {data.get("periode","—")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.82rem;color:var(--text);">Laatste update: {data.get("laatste_update","—")}</div>', unsafe_allow_html=True)
    volgende = gt.get("volgende_checkin", "") if gt else ""
    if volgende:
        st.markdown(f'<div style="font-size:0.82rem;color:var(--text);">Volgende check-in: {volgende}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Kostenbesparing onderaan
if data.get("kosten_besparing"):
    st.markdown('<div class="insight-card">', unsafe_allow_html=True)
    v = data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)
    d = data["kosten_besparing"] - v
    st.markdown('<div class="label">💰 Kostenbesparing deze maand</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="big-number">€{data["kosten_besparing"]:,}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div style="font-size:0.78rem;color:var(--text-sec);">'
        f'{"+" if d >= 0 else ""}€{d:,} vs vorige maand (€{v:,})'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
