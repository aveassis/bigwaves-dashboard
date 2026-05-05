# BigWaves HITL Detail Pagina
# Human In The Loop — de USP van BigWaves
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
        --bw-primary: #0A4DA4; --bw-accent: #00B4D8; --bw-dark: #0f0f0f; --bw-surface: #171717;
        --bw-card: #1a1a1a; --bw-border: #2e2e2e; --bw-text: #fafafa;
        --bw-text-secondary: #b4b4b4; --bw-text-muted: #898989;
        --bw-green: #00C853; --bw-orange: #FF9100; --bw-red: #D50000;
    }
    .stApp { background: var(--bw-surface) !important; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--bw-text) !important; font-weight: 500 !important; }
    .stApp p, .stApp li, .stApp span, .stApp label { color: var(--bw-text-secondary) !important; }
    .stApp .st-caption, .stApp caption { color: var(--bw-text-muted) !important; }

    .section-header {
        font-size: 1.1rem !important; font-weight: 500 !important;
        color: var(--bw-text) !important; margin: 1.5rem 0 1rem 0 !important;
        padding-bottom: 0.5rem !important; border-bottom: 1px solid var(--bw-border) !important;
    }
    .hitl-card {
        background: var(--bw-card) !important; border-radius: 12px !important;
        padding: 1.5rem !important; border: 1px solid var(--bw-border) !important;
        text-align: center !important; margin-bottom: 0.8rem !important;
    }
    .hitl-card .big-number {
        font-size: 2.5rem !important; font-weight: 600 !important; color: var(--bw-text) !important;
    }
    .hitl-card .label {
        font-size: 0.85rem !important; color: var(--bw-text-muted) !important;
    }
    .hitl-card.menselijk { border-top: 4px solid var(--bw-accent) !important; }
    .hitl-card.auto { border-top: 4px solid var(--bw-primary) !important; }
    .hitl-card.besparing { border-top: 4px solid var(--bw-green) !important; }
    .cat-card {
        background: var(--bw-card) !important; border-radius: 12px !important;
        padding: 1.2rem !important; border: 1px solid var(--bw-border) !important;
        margin-bottom: 0.8rem !important;
    }
    .cat-card .cat-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
    .cat-card .cat-naam { font-weight: 600; color: var(--bw-text) !important; }
    .cat-card .cat-hitl { font-size: 0.85rem; color: var(--bw-text-muted) !important; }
    .cat-card .cat-getallen { display: flex; gap: 2rem; font-size: 0.85rem; color: var(--bw-text-secondary) !important; margin-bottom: 0.3rem; }
    .stProgress > div > div { background: var(--bw-primary) !important; }
    .stApp hr { border-color: var(--bw-border) !important; }
    #MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ─── Header ──────────────────────────────────────────────
st.title(f"👤 Human In The Loop — {klant_naam}")
st.caption("BigWaves' USP: AI die veilig meedenkt, processen versterkt en de mens centraal stelt.")

# ─── Why HITL ────────────────────────────────────────────
with st.expander("💡 Wat is Human In The Loop?", expanded=False):
    st.markdown("""
    **Human In The Loop (HITL)** betekent dat elk AI-proces een menselijke check heeft.  
    Geen black-box AI — jij houdt controle over de belangrijke beslissingen.

    - **Laag % HITL** = veel geautomatiseerd, systeem draait zelfstandig  
    - **Hoog % HITL** = veel handmatige controles, minder efficiënt  
    - **Doel**: zo laag mogelijk, zonder in te leveren op kwaliteit

    *BigWaves garandeert dat geen enkel proces volledig op autopilot draait. Mensen blijven altijd in de loop.*
    """)

# ─── KPI cards ──────────────────────────────────────────
hitl = data.get("hitl_detail", {})
if hitl:
    st.markdown('<div class="section-header">HITL-overzicht</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        total = hitl.get("totaal_acties", 0)
        st.markdown(f"""
        <div class="hitl-card">
            <div class="label">Totaal verwerkte acties</div>
            <div class="big-number">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        mens = hitl.get("menselijke_check", 0)
        pct_mens = round(mens / total * 100) if total else 0
        st.markdown(f"""
        <div class="hitl-card menselijk">
            <div class="label">👤 Menselijke check</div>
            <div class="big-number">{mens:,}</div>
            <div class="label">{pct_mens}% van totaal</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        auto = hitl.get("geautomatiseerd", 0)
        pct_auto = round(auto / total * 100) if total else 0
        st.markdown(f"""
        <div class="hitl-card auto">
            <div class="label">🤖 Geautomatiseerd</div>
            <div class="big-number">{auto:,}</div>
            <div class="label">{pct_auto}% van totaal</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[3]:
        uren = hitl.get("bespaarde_uren", 0)
        st.markdown(f"""
        <div class="hitl-card besparing">
            <div class="label">⏱️ Bespaarde uren</div>
            <div class="big-number">{uren}u</div>
        </div>
        """, unsafe_allow_html=True)

    # ─── HITL ratio gauge ──────────────────────────────────
    hitl_ratio_kpi = data.get("kpis", {}).get("HITL-ratio", {})
    hitl_ratio = hitl_ratio_kpi.get("waarde", 0)
    hitl_doel = hitl_ratio_kpi.get("doel", 20)

    st.markdown('<div class="section-header">HITL-ratio</div>', unsafe_allow_html=True)

    import plotly.graph_objects as go

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=hitl_ratio,
        delta={"reference": hitl_doel, "decreasing": {"color": "#00C853"}, "increasing": {"color": "#D50000"}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": f"HITL-ratio (doel: ≤{hitl_doel}%)", "font": {"size": 14, "color": "#fafafa"}},
        gauge={
            "axis": {"range": [None, 50], "tickwidth": 1, "tickcolor": "#898989"},
            "bar": {"color": "#0A4DA4"},
            "bgcolor": "#1a1a1a",
            "borderwidth": 0,
            "steps": [
                {"range": [0, hitl_doel], "color": "rgba(0, 200, 83, 0.15)"},
                {"range": [hitl_doel, 35], "color": "rgba(255, 145, 0, 0.15)"},
                {"range": [35, 50], "color": "rgba(213, 0, 0, 0.15)"},
            ],
            "threshold": {
                "line": {"color": "#D50000", "width": 3},
                "thickness": 0.75,
                "value": hitl_doel,
            },
        },
    ))
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#1a1a1a",
        font={"color": "#b4b4b4", "family": "Inter"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # ─── Categorien uitsplitsing ──────────────────────────
    st.markdown('<div class="section-header">Uitsplitsing per categorie</div>', unsafe_allow_html=True)
    categorien = hitl.get("categorieen", {})
    cat_cols = st.columns(2)
    for idx, (cat, info) in enumerate(categorien.items()):
        pct = info.get("percentage", 0)
        with cat_cols[idx % 2]:
            st.markdown(f"""
            <div class="cat-card">
                <div class="cat-header">
                    <span class="cat-naam">{cat}</span>
                    <span class="cat-hitl">HITL: <strong style="color:var(--bw-text)">{pct}%</strong></span>
                </div>
                <div class="cat-getallen">
                    <span>📥 Totaal: {info['totaal']:,}</span>
                    <span>👤 Check: {info['hitl']:,}</span>
                    <span>🤖 Auto: {info['totaal'] - info['hitl']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            # Mini progress bar
            st.progress(min(pct / 50, 1.0), text=f"HITL {pct}%")

    # ─── Grafiek: Categorien vergelijking ─────────────────
    st.markdown('<div class="section-header">Vergelijking: beoogd vs. realiteit</div>', unsafe_allow_html=True)
    if categorien:
        fig2 = go.Figure()
        cat_namen = list(categorien.keys())
        cat_pct = [v["percentage"] for v in categorien.values()]
        cat_totaal = [v["totaal"] for v in categorien.values()]

        fig2.add_trace(go.Bar(
            name="HITL-percentage",
            x=cat_namen,
            y=cat_pct,
            marker_color="#00B4D8",
            text=[f"{p}%" for p in cat_pct],
            textposition="outside",
            textfont=dict(color="#b4b4b4"),
        ))
        fig2.add_hline(
            y=hitl_doel,
            line_dash="dash",
            line_color="#FF9100",
            annotation_text=f"Doel: ≤{hitl_doel}%",
            annotation_position="top left",
            annotation_font=dict(color="#FF9100"),
        )
        fig2.update_layout(
            title="HITL-percentage per categorie",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#1a1a1a",
            plot_bgcolor="#1a1a1a",
            font=dict(size=11, color="#b4b4b4"),
            title_font=dict(color="#fafafa"),
            yaxis=dict(title="HITL %", gridcolor="#2e2e2e", color="#898989", range=[0, max(cat_pct) * 1.3]),
            xaxis=dict(gridcolor="#2e2e2e", color="#898989"),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ─── Voordelen van HITL ──────────────────────────────
    st.markdown('<div class="section-header">Waarom HITL belangrijk is</div>', unsafe_allow_html=True)
    voordelen_cols = st.columns(3)
    with voordelen_cols[0]:
        st.markdown("""
        ✅ **Kwaliteitscontrole**  
        Mensen vangen edge-cases en uitzonderingen die AI mist.  
        *Resultaat: hogere nauwkeurigheid*
        """)
    with voordelen_cols[1]:
        st.markdown("""
        ✅ **Veiligheid & Compliance**  
        Geen black-box beslissingen. Altijd een mens die verantwoordelijk is.  
        *Resultaat: voldoen aan AVG en sectorregels*
        """)
    with voordelen_cols[2]:
        st.markdown("""
        ✅ **Continue verbetering**  
        Menselijke feedback traint het systeem beter. Hoe meer HITL, hoe slimmer de AI wordt.  
        *Resultaat: dalende HITL-ratio over tijd*
        """)

else:
    st.info("Geen HITL-data beschikbaar voor deze klant.")

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
