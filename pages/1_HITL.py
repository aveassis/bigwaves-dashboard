# BigWaves HITL Detail Pagina
import streamlit as st

if "data" not in st.session_state:
    st.switch_page("dashboard.py")

data = st.session_state.data
klant_naam = st.session_state.klant_naam

st.set_page_config(page_title="HITL Detail — BigWaves", page_icon="👤", layout="wide")

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

.hitl-card {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; padding: 1.2rem !important;
    box-shadow: var(--shadow) !important; text-align: center !important;
    margin-bottom: 0.8rem !important;
}
.hitl-card .big-number { font-size: 2rem !important; font-weight: 700 !important; color: var(--text) !important; }
.hitl-card .label { font-size: 0.72rem !important; color: var(--text-muted) !important; text-transform: uppercase; letter-spacing: 0.3px; }
.sec-head {
    font-size: 0.9rem !important; font-weight: 600 !important; color: var(--text) !important;
    margin: 1.2rem 0 0.8rem 0 !important;
}
.cat-card {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; padding: 1rem !important;
    box-shadow: var(--shadow) !important; margin-bottom: 0.8rem !important;
}
.cat-card .cat-naam { font-weight: 600; color: var(--text) !important; }
.cat-card .cat-hitl { font-size: 0.82rem; color: var(--text-muted); }
.cat-card .cat-getallen { display: flex; gap: 1.5rem; font-size: 0.78rem; color: var(--text-sec) !important; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

st.title("👤 Human In The Loop")
st.caption(f"{klant_naam} • BigWaves' USP: AI die veilig meedenkt")

with st.expander("💡 Wat is Human In The Loop?", expanded=False):
    st.markdown("""
    **Human In The Loop (HITL)** betekent dat elk AI-proces een menselijke check heeft.  
    - **Laag % HITL** = veel geautomatiseerd  
    - **Hoog % HITL** = veel handmatige controles  
    - **Doel**: zo laag mogelijk, zonder in te leveren op kwaliteit
    """)

hitl = data.get("hitl_detail", {})
if hitl:
    st.markdown('<div class="sec-head">📊 HITL-overzicht</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    with cols[0]:
        t = hitl.get("totaal_acties", 0)
        st.markdown(f"""<div class="hitl-card"><div class="label">Totaal</div><div class="big-number">{t:,}</div></div>""", unsafe_allow_html=True)
    with cols[1]:
        m = hitl.get("menselijke_check", 0)
        p = round(m / t * 100) if t else 0
        st.markdown(f"""<div class="hitl-card"><div class="label">👤 Menselijk</div><div class="big-number">{m:,}</div><div class="label">{p}%</div></div>""", unsafe_allow_html=True)
    with cols[2]:
        a = hitl.get("geautomatiseerd", 0)
        p = round(a / t * 100) if t else 0
        st.markdown(f"""<div class="hitl-card"><div class="label">🤖 Auto</div><div class="big-number">{a:,}</div><div class="label">{p}%</div></div>""", unsafe_allow_html=True)
    with cols[3]:
        u = hitl.get("bespaarde_uren", 0)
        st.markdown(f"""<div class="hitl-card"><div class="label">⏱ Uren</div><div class="big-number">{u}u</div></div>""", unsafe_allow_html=True)

    hitl_r = data.get("kpis", {}).get("HITL-ratio", {})
    hr = hitl_r.get("waarde", 0)
    hd = hitl_r.get("doel", 20)

    st.markdown('<div class="sec-head">📈 HITL-ratio</div>', unsafe_allow_html=True)
    import plotly.graph_objects as go
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=hr,
        delta={"reference": hd, "decreasing": {"color": "#10b981"}, "increasing": {"color": "#ef4444"}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": f"Doel: ≤{hd}%", "font": {"size": 14, "color": "#edf2f7"}},
        gauge={
            "axis": {"range": [None, 50], "tickwidth": 1, "tickcolor": "#64748b"},
            "bar": {"color": "#10b981"},
            "bgcolor": "#1e2231", "borderwidth": 0,
            "steps": [
                {"range": [0, hd], "color": "rgba(16,185,129,0.15)"},
                {"range": [hd, 35], "color": "rgba(245,158,11,0.12)"},
                {"range": [35, 50], "color": "rgba(239,68,68,0.12)"},
            ],
            "threshold": {"line": {"color": "#ef4444", "width": 3}, "thickness": 0.75, "value": hd},
        },
    ))
    fig.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#1e2231", font={"color": "#94a3b8", "family": "Inter"})
    st.plotly_chart(fig, width="stretch")

    st.markdown('<div class="sec-head">📋 Uitsplitsing per categorie</div>', unsafe_allow_html=True)
    cats = hitl.get("categorieen", {})
    cc = st.columns(2)
    for idx, (cat, info) in enumerate(cats.items()):
        pct = info.get("percentage", 0)
        with cc[idx % 2]:
            st.markdown(f"""<div class="cat-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span class="cat-naam">{cat}</span>
                    <span class="cat-hitl">HITL: <strong style="color:var(--text)">{pct}%</strong></span>
                </div>
                <div class="cat-getallen">
                    <span>📥 {info['totaal']:,}</span>
                    <span>👤 {info['hitl']:,}</span>
                    <span>🤖 {info['totaal'] - info['hitl']:,}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            st.progress(min(pct / 50, 1.0), text=f"HITL {pct}%")

    if cats:
        st.markdown('<div class="sec-head">📊 Vergelijking</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        n = list(cats.keys())
        p = [v["percentage"] for v in cats.values()]
        fig2.add_trace(go.Bar(name="HITL %", x=n, y=p, marker_color="#10b981",
            text=[f"{x}%" for x in p], textposition="outside", textfont=dict(color="#94a3b8")))
        fig2.add_hline(y=hd, line_dash="dash", line_color="#f59e0b",
            annotation_text=f"Doel: ≤{hd}%", annotation_position="top left",
            annotation_font=dict(color="#f59e0b"))
        fig2.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#1e2231", plot_bgcolor="#1e2231",
            font=dict(size=11, color="#94a3b8"), title_font=dict(color="#edf2f7"),
            yaxis=dict(gridcolor="#2a2e3d", color="#64748b"), xaxis=dict(gridcolor="#2a2e3d", color="#64748b"))
        st.plotly_chart(fig2, width="stretch")
else:
    st.info("Geen HITL-data beschikbaar voor deze klant.")

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
