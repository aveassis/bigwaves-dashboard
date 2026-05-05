# BigWaves HITL Detail Pagina
import streamlit as st

if "data" not in st.session_state:
    st.switch_page("dashboard.py")

data = st.session_state.data
klant_naam = st.session_state.klant_naam

st.set_page_config(page_title="HITL Detail — BigWaves", page_icon="👤", layout="wide")

# ─── Styling ─────────────────────────────────────────────
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
    :root {
        --bg: #f5f7fa; --surface: #ffffff; --card: #ffffff; --border: #e8ecf1;
        --text: #1a1d23; --text-secondary: #6b7280; --text-muted: #9ca3af;
        --primary: #059669; --primary-light: #d1fae5; --shadow: 0 1px 3px rgba(0,0,0,0.06);
        --radius: 12px;
    }
    .stApp { background: var(--bg) !important; }
    .stApp h1 { font-size: 1.5rem; color: var(--text); font-weight: 600; }
    .stApp h2, .stApp h3, .stApp h4 { color: var(--text) !important; font-weight: 600; }
    .stApp p, .stApp li, .stApp span, .stApp label { color: var(--text-secondary) !important; font-size: 0.85rem; }
    .stApp .st-caption { color: var(--text-muted) !important; font-size: 0.75rem; }

    .section-header {
        font-size: 0.95rem !important; font-weight: 600 !important;
        color: var(--text) !important; margin: 1.5rem 0 1rem 0 !important;
    }
    .hitl-card {
        background: var(--card) !important; border-radius: var(--radius) !important;
        padding: 1.2rem !important; box-shadow: var(--shadow) !important;
        text-align: center !important; margin-bottom: 0.8rem !important;
    }
    .hitl-card .big-number { font-size: 2rem !important; font-weight: 700 !important; color: var(--text) !important; }
    .hitl-card .label { font-size: 0.75rem !important; color: var(--text-muted) !important; }

    .cat-card {
        background: var(--card) !important; border-radius: var(--radius) !important;
        padding: 1rem !important; box-shadow: var(--shadow) !important; margin-bottom: 0.8rem !important;
    }
    .cat-card .cat-naam { font-weight: 600; color: var(--text) !important; }
    .cat-card .cat-hitl { font-size: 0.85rem; color: var(--text-muted); }
    .cat-card .cat-getallen { display: flex; gap: 1.5rem; font-size: 0.8rem; color: var(--text-secondary) !important; margin-top: 0.3rem; }

    .stProgress > div > div { background: var(--primary) !important; }
    .stProgress > div { background: var(--primary-light) !important; }
    .stApp hr { border-color: var(--border) !important; }
    .stButton button { border-radius: 8px !important; }
    .stButton button[kind="primary"] { background: var(--primary) !important; border-color: var(--primary) !important; color: white !important; }

    #MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────
st.title("👤 Human In The Loop")
st.caption(f"{klant_naam} • BigWaves' USP: AI die veilig meedenkt")

# ─── Why HITL ────────────────────────────────────────────
with st.expander("💡 Wat is Human In The Loop?", expanded=False):
    st.markdown("""
    **Human In The Loop (HITL)** betekent dat elk AI-proces een menselijke check heeft.  
    - **Laag % HITL** = veel geautomatiseerd, systeem draait zelfstandig  
    - **Hoog % HITL** = veel handmatige controles, minder efficiënt  
    - **Doel**: zo laag mogelijk, zonder in te leveren op kwaliteit
    """)

# ─── KPI cards ──────────────────────────────────────────
hitl = data.get("hitl_detail", {})
if hitl:
    st.markdown("### 📊 HITL-overzicht")
    cols = st.columns(4)
    with cols[0]:
        total = hitl.get("totaal_acties", 0)
        st.markdown(f"""<div class="hitl-card"><div class="label">Totaal</div><div class="big-number">{total:,}</div></div>""", unsafe_allow_html=True)
    with cols[1]:
        mens = hitl.get("menselijke_check", 0)
        pct = round(mens / total * 100) if total else 0
        st.markdown(f"""<div class="hitl-card"><div class="label">👤 Menselijk</div><div class="big-number">{mens:,}</div><div class="label">{pct}%</div></div>""", unsafe_allow_html=True)
    with cols[2]:
        auto = hitl.get("geautomatiseerd", 0)
        pct = round(auto / total * 100) if total else 0
        st.markdown(f"""<div class="hitl-card"><div class="label">🤖 Auto</div><div class="big-number">{auto:,}</div><div class="label">{pct}%</div></div>""", unsafe_allow_html=True)
    with cols[3]:
        uren = hitl.get("bespaarde_uren", 0)
        st.markdown(f"""<div class="hitl-card"><div class="label">⏱️ Uren</div><div class="big-number">{uren}u</div></div>""", unsafe_allow_html=True)

    # ─── HITL ratio gauge ──────────────────────────────────
    hitl_ratio_kpi = data.get("kpis", {}).get("HITL-ratio", {})
    hitl_ratio = hitl_ratio_kpi.get("waarde", 0)
    hitl_doel = hitl_ratio_kpi.get("doel", 20)

    st.markdown("### 📈 HITL-ratio")
    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=hitl_ratio,
        delta={"reference": hitl_doel, "decreasing": {"color": "#059669"}, "increasing": {"color": "#ef4444"}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": f"Doel: ≤{hitl_doel}%", "font": {"size": 14, "color": "#1a1d23"}},
        gauge={
            "axis": {"range": [None, 50], "tickwidth": 1, "tickcolor": "#9ca3af"},
            "bar": {"color": "#059669"},
            "bgcolor": "#ffffff",
            "borderwidth": 0,
            "steps": [
                {"range": [0, hitl_doel], "color": "#d1fae5"},
                {"range": [hitl_doel, 35], "color": "#fef3c7"},
                {"range": [35, 50], "color": "#fee2e2"},
            ],
            "threshold": {
                "line": {"color": "#ef4444", "width": 3},
                "thickness": 0.75,
                "value": hitl_doel,
            },
        },
    ))
    fig.update_layout(
        height=260, margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#ffffff", font={"color": "#6b7280", "family": "Inter"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # ─── Categorien uitsplitsing ──────────────────────────
    st.markdown("### 📋 Uitsplitsing per categorie")
    categorien = hitl.get("categorieen", {})
    cat_cols = st.columns(2)
    for idx, (cat, info) in enumerate(categorien.items()):
        pct = info.get("percentage", 0)
        with cat_cols[idx % 2]:
            st.markdown(f"""
            <div class="cat-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span class="cat-naam">{cat}</span>
                    <span class="cat-hitl">HITL: <strong style="color:var(--text)">{pct}%</strong></span>
                </div>
                <div class="cat-getallen">
                    <span>📥 {info['totaal']:,}</span>
                    <span>👤 {info['hitl']:,}</span>
                    <span>🤖 {info['totaal'] - info['hitl']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(pct / 50, 1.0), text=f"HITL {pct}%")

    # ─── Grafiek ──────────────────────────────────────────
    if categorien:
        st.markdown("### 📊 Vergelijking")
        fig2 = go.Figure()
        cat_namen = list(categorien.keys())
        cat_pct = [v["percentage"] for v in categorien.values()]

        fig2.add_trace(go.Bar(
            name="HITL %", x=cat_namen, y=cat_pct,
            marker_color="#059669",
            text=[f"{p}%" for p in cat_pct], textposition="outside",
            textfont=dict(color="#6b7280"),
        ))
        fig2.add_hline(y=hitl_doel, line_dash="dash", line_color="#f59e0b",
            annotation_text=f"Doel: ≤{hitl_doel}%", annotation_position="top left",
            annotation_font=dict(color="#f59e0b"))
        fig2.update_layout(
            height=320, margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(size=11, color="#6b7280"),
            title_font=dict(color="#1a1d23"),
            yaxis=dict(gridcolor="#f3f4f6", color="#9ca3af"),
            xaxis=dict(gridcolor="#f3f4f6", color="#9ca3af"),
        )
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("Geen HITL-data beschikbaar voor deze klant.")

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
