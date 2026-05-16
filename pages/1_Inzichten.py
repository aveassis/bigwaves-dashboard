# BigWaves Inzichten Pagina — zelfde look als home
import streamlit as st

st.set_page_config(page_title="Inzichten — BigWaves", page_icon="📈", layout="wide")

from shared_css import setup_subpage
setup_subpage()

data = st.session_state.data
klant_naam = st.session_state.klant_naam

# ─── Header (zelfde stijl als home) ─────────────────────────
logo = data.get("logo", "🌊")
st.markdown(
    f"<div style='display:flex;align-items:center;gap:0.8rem;'>"
    f"<span style='font-size:2.5rem;'>{logo}</span>"
    f"<div><h1 style='margin:0;'>Inzichten</h1>"
    f"<p style='margin:0;color:var(--text-muted);font-size:0.82rem;'>"
    f"Voortgang • Resultaten • Status — {klant_naam}</p></div></div>",
    unsafe_allow_html=True,
)

# ─── Helper functies ───────────────────────────────────────
def status_icon(s):
    return {"groen": "🟢", "oranje": "🟠", "rood": "🔴"}.get(s, "⚪")

# ─── Data ophalen ──────────────────────────────────────────
gt = data.get("groei_team", {})
checkins = gt.get("checkin_historie", []) if gt else []
workflows = gt.get("workflows", []) if gt else []
bn = data.get("bottleneck", {})
kpis = data.get("kpis", {})
kanalen = data.get("kanalen", {})
periodes = data.get("periodes", {})
periode_lijst = list(periodes.keys()) if periodes else []

# ─── 1. VOORTGANG — check-in + workflows ──────────────────
st.markdown('<div class="sec-head">🚀 Voortgang</div>', unsafe_allow_html=True)

vcols = st.columns([1, 1])

with vcols[0]:
    st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="kpi-label">📅 Laatste check-in</div>',
        unsafe_allow_html=True,
    )
    if checkins:
        laatste = checkins[0]
        s = laatste.get("status", "groen")
        clr = {"groen": "#22c55e", "oranje": "#f59e0b", "rood": "#ef4444"}.get(s, "#22c55e")
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<span style="font-size:0.82rem;color:var(--text-sec);">{laatste.get("datum","")}</span>'
            f'<span style="color:{clr};">{status_icon(s)}</span>'
            f'</div>'
            f'<div style="font-size:0.85rem;color:var(--text);margin-top:4px;">'
            f'{laatste.get("notities","")}</div>',
            unsafe_allow_html=True
        )
        if len(checkins) > 1:
            st.caption(f"➕ {len(checkins)-1} eerdere check-ins")
    else:
        st.caption("Nog geen check-in historie beschikbaar.")
    st.markdown('</div>', unsafe_allow_html=True)

with vcols[1]:
    st.markdown('<div class="kpi-box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="kpi-label">⚙️ Workflow status</div>',
        unsafe_allow_html=True,
    )
    if workflows:
        for wf in workflows:
            s = wf.get("status", "groen")
            clr = {"groen": "#22c55e", "oranje": "#f59e0b", "rood": "#ef4444"}.get(s, "#22c55e")
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;align-items:center;'
                f'padding:0.5rem 0;border-bottom:1px solid var(--border);">'
                f'<div><span style="color:var(--text);font-size:0.82rem;">{wf.get("naam","")}</span>'
                f'<br><span style="font-size:0.7rem;color:var(--text-muted);">'
                f'{wf.get("items_verwerkt",0)} items verwerkt</span></div>'
                f'<span style="color:{clr};font-size:1rem;">{status_icon(s)}</span>'
                f'</div>',
                unsafe_allow_html=True
            )
    else:
        st.caption("Geen actieve workflows.")
    st.markdown('</div>', unsafe_allow_html=True)

# Bottleneck (zelfde stijl als home)
if bn and bn.get("tekst"):
    st.markdown(
        f'<div class="bn-card">'
        f'<strong>🔍 Bottleneck-analyse</strong><br>'
        f'{bn["tekst"]}</div>',
        unsafe_allow_html=True,
    )

# ─── 2. RESULTATEN — KPIs in home-stijl ────────────────────
st.markdown('<div class="sec-head">📊 Resultaten</div>', unsafe_allow_html=True)

if kpis:
    hoeveel = 2 if st.session_state.get("mobile", False) else 3
    rcols = st.columns(hoeveel)
    colors = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}
    for i, (name, info) in enumerate(list(kpis.items())):
        w = info.get("waarde", 0)
        e = info.get("eenheid", "")
        dsp = f"€{w:,}" if e == "euro" else f"{w}{'s' if e=='seconden' else '%' if e=='%' else ''}"
        if e not in ("euro", "seconden", "%"):
            dsp = f"{w:,}" if isinstance(w, int) else str(w)
        sts = info.get("status", "groen")
        clr = colors.get(sts, "#10b981")
        tc = "up" if "+" in info.get("trend","") or "lager" in info.get("trend","").lower() else "down" if "-" in info.get("trend","") else ""
        arrow = "↑" if tc == "up" else "↓" if tc == "down" else "→"
        with rcols[i % hoeveel]:
            st.html(f"""<div class="kpi-box">
                <div class="kpi-top">
                    <div class="kpi-icon">{status_icon(sts)}</div>
                    <div class="kpi-dots">⋯</div>
                </div>
                <div class="kpi-label">{name}</div>
                <div class="kpi-val">{dsp}</div>
                <div class="kpi-target">Doel: {info.get('doel','')}</div>
                <div class="kpi-foot {"up" if tc=="up" else "down" if tc=="down" else "neutral"}">{arrow} {info.get('trend','')}</div>
                {f'<div class="kpi-uitleg">ⓘ {info.get("uitleg","")}</div>' if info.get('uitleg') else ''}
            </div>""")

# ─── 3. KANALEN (zelfde stijl als home) ────────────────────
if kanalen:
    st.markdown('<div class="sec-head">📬 Kanalen <span class="pill">live</span></div>', unsafe_allow_html=True)
    kc = st.columns(len(kanalen))
    icoon_map = {"website": "🌐", "mail": "📧", "whatsapp": "💬", "telefoon": "📞"}
    for idx, (kanaal, info) in enumerate(sorted(kanalen.items())):
        icoon = icoon_map.get(kanaal.lower(), "📨")
        with kc[idx]:
            st.markdown(f"""
            <div class="kanban-card">
                <div style="font-size:1.8rem;margin-bottom:0.3rem;">{icoon}</div>
                <div style="color:#949494;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.5px;">{kanaal}</div>
                <div style="color:#121213;font-size:1.5rem;font-weight:700;margin:0.2rem 0;">{info.get('verwerkt',0)}</div>
                <div style="color:#5273ff;font-size:0.78rem;">{info.get('bestellingen',0)} bestellingen</div>
            </div>
            """, unsafe_allow_html=True)

# ─── 4. GRAFIEKEN (zelfde stijl als home) ──────────────────
g = data.get("grafieken", {})
if g:
    st.markdown('<div class="sec-head">📈 Trends <span class="pill">live</span></div>', unsafe_allow_html=True)
    import plotly.graph_objects as go
    gc = st.columns(2)
    for idx, (k, gr) in enumerate(g.items()):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=gr["labels"], y=gr["waarden"], name=gr["titel"],
            marker_color="#5273ff", opacity=0.85, marker_line_width=0))
        if "doel" in gr and gr["doel"]:
            fig.add_hline(y=gr["doel"], line_dash="dash", line_color="#f59e0b",
                annotation_text=f"Doel: {gr['doel']}", annotation_position="top left",
                annotation_font=dict(color="#f59e0b", size=11))
        fig.update_layout(title=gr["titel"], height=280, margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(size=11, color="#5a5a5a"), title_font=dict(color="#121213", size=13),
            yaxis=dict(gridcolor="#f1efed", color="#949494"),
            xaxis=dict(gridcolor="#f1efed", color="#949494"),
            hoverlabel=dict(bgcolor="#5273ff", font_color="white"))
        with gc[idx % 2]:
            st.plotly_chart(fig, use_container_width=True)

# ─── 5. KOSTENBESPARING ────────────────────────────────────
if data.get("kosten_besparing"):
    st.markdown('<div class="sec-head">💰 Kostenbesparing</div>', unsafe_allow_html=True)
    kbcols = st.columns([1, 1])
    with kbcols[0]:
        st.metric(
            "Deze maand",
            f"€{data['kosten_besparing']:,}",
            delta=f"+{data['kosten_besparing'] - data.get('doelen_vorige_maand',{}).get('kosten_besparing',0):,}",
        )
    with kbcols[1]:
        if gt:
            pkt = gt.get("pakket", "—")
            st.markdown(
                f'<div class="kpi-box" style="text-align:center;">'
                f'<div class="kpi-label">GroeiTeam pakket</div>'
                f'<div class="kpi-val" style="font-size:1.3rem;">{pkt}</div>'
                f'<div style="font-size:0.72rem;color:var(--text-muted);">'
                f'Sinds {gt.get("sinds","—")}</div></div>',
                unsafe_allow_html=True
            )

# ─── 6. VOORTGANG OVER PERIODES (zelfde als home) ──────────
if len(periode_lijst) > 1:
    st.markdown('<div class="sec-head">📈 Voortgang over periodes</div>', unsafe_allow_html=True)
    kpi_trends = {}
    for p_naam in periode_lijst:
        p_data = periodes[p_naam]
        for kpi_nm, kpi_info in p_data.get("kpis", {}).items():
            if kpi_nm not in kpi_trends:
                kpi_trends[kpi_nm] = []
            kpi_trends[kpi_nm].append((p_naam, kpi_info.get("waarde", 0), kpi_info.get("doel", 0)))

    import plotly.graph_objects as go
    for kpi_nm, pts in sorted(kpi_trends.items()):
        if len(pts) < 2:
            continue
        waarden = [p[1] for p in pts]
        doelen = [p[2] for p in pts]
        namen = [p[0] for p in pts]
        if len(set(str(w) for w in waarden)) <= 1:
            continue
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=namen, y=waarden, mode="lines+markers",
            name=kpi_nm, line=dict(color="#5273ff", width=2.5),
            marker=dict(size=8, color="#5273ff", line=dict(color="#ffffff", width=2))))
        fig.add_trace(go.Scatter(x=namen, y=doelen, mode="lines",
            name="Doel", line=dict(dash="dash", color="#f59e0b", width=1.5)))
        fig.update_layout(title=kpi_nm, height=200, margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(size=10, color="#5a5a5a"), title_font=dict(color="#121213", size=12),
            yaxis=dict(gridcolor="#f1efed", color="#949494"),
            xaxis=dict(gridcolor="#f1efed", color="#949494"),
            showlegend=False, hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
