# BigWaves Dashboard — LinkedIn Outreach
import streamlit as st
from pathlib import Path

LINKEDIN_DIR = Path("/opt/data/bigwaves/linkedin-outreach")

st.set_page_config(page_title="LinkedIn — BigWaves", page_icon="🔗", layout="wide")

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root { --bg:#0f1117; --surface:#1a1d27; --card:#1e2231; --border:#2a2e3d; --border-light:#363b4d; --text:#edf2f7; --text-sec:#94a3b8; --text-muted:#64748b; --primary:#10b981; --primary-light:rgba(16,185,129,0.1); --shadow:0 2px 8px rgba(0,0,0,0.2); --radius:14px; --radius-sm:10px; }
.stApp { background: var(--bg) !important; }
.stApp h1 { font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text) !important; }
.stApp h2 { font-size: 1.1rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp h3 { font-size: 0.95rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp p, .stApp li, .stApp span, .stApp label { color: var(--text-sec) !important; font-size: 0.82rem !important; }
.stApp .st-caption { color: var(--text-muted) !important; font-size: 0.72rem !important; }
section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
.stApp hr { border-color: var(--border) !important; }
.stButton button { border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; }
.stMetric label { color: var(--text-sec) !important; }
.stMetric [data-testid="stMetricValue"] { color: var(--text) !important; }
.stMetric [data-testid="stMetricDelta"] { color: var(--primary) !important; }
.stExpander { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 14px !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
</style>""", unsafe_allow_html=True)

if "data" not in st.session_state or not st.session_state.get("ingelogd"):
    st.warning("Niet ingelogd. Ga naar het dashboard om in te loggen.")
    st.page_link("dashboard.py", label="← Naar dashboard", use_container_width=True)
    st.stop()

data = st.session_state.data
kn = st.session_state.klant_naam

# ─── Pro-pakket check ──────────────────────────
gt = data.get("groei_team", {})
pakket = gt.get("pakket", "")
if pakket != "Pro":
    st.warning("🔗 LinkedIn Outreach is exclusief voor **Pro** klanten.")
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(16,185,129,0.08),rgba(16,185,129,0.02));
                border:1px solid rgba(16,185,129,0.2);border-radius:14px;padding:2rem;text-align:center;margin:1.5rem 0;">
        <div style="font-size:3rem;margin-bottom:0.5rem;">🔗</div>
        <h3 style="color:var(--text);margin-bottom:0.5rem;">LinkedIn Outreach — alleen Pro</h3>
        <p style="color:var(--text-sec);max-width:500px;margin:0 auto 1rem;">
            De LinkedIn Outreach tool is exclusief beschikbaar in ons <strong>Pro</strong> pakket.
            Automatische prospect warming, connecties en opvolging — volledig beheerd door BigWaves.
        </p>
        <p style="color:var(--text-muted);font-size:0.78rem;">
            📈 Vanaf €2.499/maand · 5 workflows · setup begeleiding
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_GroeiTeam.py", label="📈 Bekijk GroeiTeam pakketten", use_container_width=True)
    st.stop()

st.title("🔗 LinkedIn Outreach")
st.caption(f"{kn} • Gedeelde warmup — BigWaves warmt prospects voor u op")

# ─── LinkedIn tool status ──────────────────────────
db_exists = (LINKEDIN_DIR / "data" / "linkedin.db").exists()
tool_exists = (LINKEDIN_DIR / "main.py").exists()

if not tool_exists:
    st.warning("LinkedIn outreach database niet gevonden. Voer eerst 'python main.py setup' uit in /opt/data/bigwaves/linkedin-outreach/")
    st.stop()

# Laad dashboard data
import subprocess
import json

try:
    result = subprocess.run(
        ["python", "main.py", "dashboard", "--format", "json"],
        capture_output=True, text=True, cwd=str(LINKEDIN_DIR),
        timeout=10,
    )
    if result.returncode == 0:
        dashboard_data = json.loads(result.stdout)
    else:
        dashboard_data = {"totalen": {}, "totaal": 0, "recente_acties": []}
except Exception:
    dashboard_data = {"totalen": {}, "totaal": 0, "recente_acties": []}

# ─── KPI overzicht ─────────────────────────────────
totalen = dashboard_data.get("totalen", {})
totaal = dashboard_data.get("totaal", 0)
laatste_acties = dashboard_data.get("recente_acties", [])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📊 Totaal", totaal)
col2.metric("🆕 Nieuw", totalen.get("new", 0))
col3.metric("🔥 Warmup", totalen.get("warming", 0) + totalen.get("warmed", 0))
col4.metric("🔗 Connecties", totalen.get("connecting", 0) + totalen.get("connected", 0))
col5.metric("✅ Replies", totalen.get("replied", 0) + totalen.get("meeting", 0))

# ─── Status visualisatie ───────────────────────────
st.markdown("### 📊 Prospect Pipeline")
status_order = ["new", "warming", "warmed", "connecting", "connected", "replied", "meeting", "rejected"]
status_labels = {
    "new": "🆕 Nieuw", "warming": "🔥 Warming", "warmed": "☀️ Opgewarmd",
    "connecting": "🔗 Connectie", "connected": "✅ Verbonden",
    "replied": "💬 Reply", "meeting": "📅 Meeting", "rejected": "❌ Afgewezen",
}
status_colors = {
    "new": "#64748b", "warming": "#f59e0b", "warmed": "#10b981",
    "connecting": "#3b82f6", "connected": "#8b5cf6",
    "replied": "#10b981", "meeting": "#10b981", "rejected": "#ef4444",
}

cols = st.columns(len(status_order))
for i, status in enumerate(status_order):
    cnt = totalen.get(status, 0)
    clr = status_colors.get(status, "#64748b")
    with cols[i]:
        st.markdown(f"""
        <div style="text-align:center; background:var(--card); border:1px solid var(--border);
                    border-radius:12px; padding:0.6rem 0.3rem;">
            <div style="font-size:1.5rem; font-weight:700; color:{clr};">{cnt}</div>
            <div style="font-size:0.62rem; color:var(--text-muted); line-height:1.2;">{status_labels.get(status, status)}</div>
        </div>
        """, unsafe_allow_html=True)

# Pipeline progress bar
if totaal > 0:
    pipeline_pct = (totalen.get("connected", 0) + totalen.get("replied", 0) + totalen.get("meeting", 0)) / max(totaal, 1) * 100
    st.progress(min(pipeline_pct / 100, 1.0))
    st.caption(f"Pipeline voltooid: {pipeline_pct:.0f}% (connected → meeting)")

# ─── Recente acties ────────────────────────────────
st.markdown("### 📋 Recente activiteit")
if laatste_acties:
    for a in laatste_acties[:10]:
        naam = f"{a.get('voornaam', '')} {a.get('achternaam', '')}".strip()
        st.markdown(f"""
        <div style="background:var(--card); border:1px solid var(--border); border-radius:10px;
                    padding:0.4rem 0.8rem; margin-bottom:0.3rem; display:flex; align-items:center; gap:1rem;">
            <span style="font-size:0.75rem; color:var(--text-muted);">{a.get('created_at', '')}</span>
            <span style="font-size:0.8rem; font-weight:500; color:var(--text);">{naam or 'Onbekend'}</span>
            <span style="font-size:0.72rem; color:var(--text-sec);">{a.get('action_type', '')}</span>
            <span style="font-size:0.68rem; color:var(--primary);">{a.get('result', '')}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Nog geen activiteit. Start de outreach tool met 'python main.py run'")

# ─── Configuratie ──────────────────────────────────
st.markdown("### ⚙️ Configuratie")
with st.expander("Limieten & instellingen"):
    st.markdown("""
    | Actie | Max/dag | Timing |
    |-------|---------|--------|
    | Connecties | 25 | 2-5 min tussen |
    | Profiel visits | 50 | 1-3 min tussen |
    | Likes | 30 | 1-2 min tussen |
    | Messages | 20 | 3-5 min tussen |
    | Weekend | Pauze | Geen acties |
    """)

    st.markdown("**Warmup sequence (Expandi-stijl)**")
    st.markdown("""
    - **Dag 1:** Profiel bezoeken
    - **Dag 2:** Post liken (indien relevant)
    - **Dag 3:** Connectie versturen met persoonlijke noot
    - **Dag 7-10:** Follow-up bij geen reactie
    """)

    st.markdown(
        "📋 Gebruik 'python main.py dashboard --format text' in de terminal "
        "voor een compleet overzicht."
    )

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
