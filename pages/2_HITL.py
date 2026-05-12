# BigWaves Dashboard — HITL Detailpagina
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="HITL — BigWaves", page_icon="👤", layout="wide")

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root { --bg:#0f1117; --surface:#1a1d27; --card:#1e2231; --border:#2a2e3d; --border-light:#363b4d; --text:#edf2f7; --text-sec:#94a3b8; --text-muted:#64748b; --primary:#10b981; --primary-light:rgba(16,185,129,0.1); --shadow:0 2px 8px rgba(0,0,0,0.2); --radius:14px; --radius-sm:10px; }
.stApp { background: var(--bg) !important; }
.stApp h1 { font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text) !important; }
.stApp h2 { font-size: 1.1rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp h3 { font-size: 0.95rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp p, .stApp li, .stApp span, .stApp label { color: var(--text-sec) !important; font-size: 0.82rem !important; }
.stApp .st-caption { color: var(--text-muted) !important; font-size: 0.72rem !important; }
section[data-testid=\"stSidebar\"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
.stApp hr { border-color: var(--border) !important; }
.stButton button { border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stButton button[kind=\"primary\"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; }
.stMetric label { color: var(--text-sec) !important; }
.stMetric [data-testid=\"stMetricValue\"] { color: var(--text) !important; }
.stMetric [data-testid=\"stMetricDelta\"] { color: var(--primary) !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
</style>""", unsafe_allow_html=True)

if "data" not in st.session_state or not st.session_state.get("ingelogd"):
    st.warning("Niet ingelogd. Ga naar het dashboard om in te loggen.")
    st.page_link("dashboard.py", label="← Naar dashboard", use_container_width=True)
    st.stop()

data = st.session_state.data
hitl = data.get("hitl_detail", {})
kpis = data.get("kpis", {})
hitl_ratio = kpis.get("HITL-ratio", {}).get("waarde", 0)

st.title("👤 Human In The Loop")
st.caption(f"{data.get('naam', 'Klant')} • BigWaves' USP: AI die veilig meedenkt")

with st.expander("💡 Wat is Human In The Loop?"):
    st.markdown("""
    HITL betekent dat AI-automatisering wordt gecontroleerd door een mens voordat
    belangrijke acties worden uitgevoerd. Dit verhoogt veiligheid en kwaliteit.
    
    **BigWaves streeft naar ≤ 20% HITL-ratio** — dat betekent dat minimaal 80%
    van alle acties volledig geautomatiseerd verloopt.
    """)

# ─── HITL Overzicht ────────────────────────────────
st.markdown("### 📊 HITL-overzicht")
if hitl:
    cols = st.columns(4)
    cols[0].metric("Totaal", f"{hitl.get('totaal_acties', 0):,}")
    cols[1].metric("👤 Menselijk", f"{hitl.get('menselijke_check', 0):,}",
                   f"{hitl.get('menselijke_check', 0)/max(hitl.get('totaal_acties', 1),1)*100:.0f}%")
    cols[2].metric("🤖 Auto", f"{hitl.get('geautomatiseerd', 0):,}",
                   f"{hitl.get('geautomatiseerd', 0)/max(hitl.get('totaal_acties', 1),1)*100:.0f}%")
    cols[3].metric("⏱ Uren", f"{hitl.get('bespaarde_uren', 0)}u")

    # HITL-ratio meter
    st.markdown("##### 📈 HITL-ratio")
    doel = kpis.get("HITL-ratio", {}).get("doel", 20)
    ratio_bar = min(hitl_ratio / max(doel, 1), 1.0)
    st.progress(ratio_bar)
    col1, col2 = st.columns(2)
    col1.metric("Huidige ratio", f"{hitl_ratio:.0f}%")
    col2.metric("Doel", f"≤ {doel}%")

    # Grafiek
    st.markdown("###### Ratio ontwikkeling")
    grafieken = data.get("grafieken", {})
    hitl_chart = grafieken.get("hitl_trend")
    if hitl_chart:
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hitl_chart["labels"],
            y=hitl_chart["waarden"],
            name="HITL-ratio",
            marker_color="#10b981",
            opacity=0.85,
        ))
        if "doel" in hitl_chart:
            fig.add_hline(
                y=hitl_chart["doel"],
                line_dash="dash",
                line_color="#f59e0b",
                annotation_text=f"Doel: {hitl_chart['doel']}%",
            )
        fig.update_layout(
            height=300,
            paper_bgcolor="#1e2231",
            plot_bgcolor="#1e2231",
            font=dict(color="#94a3b8", size=11),
            yaxis=dict(gridcolor="#2a2e3d"),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ─── Uitsplitsing per categorie ────────────────
    st.markdown("### 📋 Uitsplitsing per categorie")
    cat = hitl.get("categorieen", {})
    if cat:
        for naam, info in cat.items():
            with st.container():
                c1, c2 = st.columns([3, 1])
                pct = info.get("percentage", 0)
                c1.markdown(f"**{naam}**")
                c1.markdown(f"📥 {info['totaal']:,}  👤 {info['hitl']:,}  🤖 {info['totaal'] - info['hitl']:,}")
                c2.markdown(f"<h3 style='color:{\"#10b981\" if pct <= 20 else \"#f59e0b\" if pct <= 30 else \"#ef4444\"};'>{pct}%</h3>", unsafe_allow_html=True)
                st.progress(min(pct / 100, 1.0))
                st.caption(f"HITL {pct}%")

        # Vergelijking grafiek
        st.markdown("### 📊 Vergelijking")
        import plotly.graph_objects as go
        names = list(cat.keys())
        pcts = [cat[n]["percentage"] for n in names]
        fig = go.Figure()
        colors = ["#10b981" if p <= 20 else "#f59e0b" if p <= 30 else "#ef4444" for p in pcts]
        fig.add_trace(go.Bar(
            x=names, y=pcts,
            marker_color=colors,
            text=[f"{p}%" for p in pcts],
            textposition="outside",
        ))
        fig.add_hline(y=20, line_dash="dash", line_color="#10b981", annotation_text="Doel: ≤20%")
        fig.update_layout(
            height=350,
            title="HITL-percentage per categorie",
            paper_bgcolor="#1e2231",
            plot_bgcolor="#1e2231",
            font=dict(color="#94a3b8", size=11),
            yaxis=dict(gridcolor="#2a2e3d", range=[0, max(pcts) * 1.3]),
            xaxis=dict(gridcolor="#2a2e3d"),
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Geen HITL-data beschikbaar voor deze klant.")

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
