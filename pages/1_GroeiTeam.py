# BigWaves Dashboard — GroeiTeam overzichtspagina
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from groei_team_ui import (
    PAKKETTEN,
    render_pakket_badge,
    render_health_ring,
    render_workflow_card,
    render_hitl_samenvatting,
    render_checkin_item,
    GROEI_TEAM_CSS,
)

st.markdown(GROEI_TEAM_CSS, unsafe_allow_html=True)

# ─── Data uit session_state ───────────────────────────────
if "data" not in st.session_state:
    st.warning("Geen data geladen. Log eerst in via het dashboard.")
    st.stop()

data = st.session_state.data
gt = data.get("groei_team", {})

if not gt:
    st.warning("Dit account heeft nog geen GroeiTeam abonnement. Neem contact op met BigWaves.")
    st.stop()

# ─── Header met health ring + badge ──────────────────────
pakket = gt.get("pakket", "Start")
cfg = PAKKETTEN.get(pakket, PAKKETTEN["Start"])
health = gt.get("health_score", 70)
status = gt.get("status", "actief")
status_dot = "🟢" if status == "actief" else "🔴"
volgende = gt.get("volgende_checkin", "—")

st.markdown(f"""
<div class="gt-header">
    {render_health_ring(health)}
    <div class="gt-header-info">
        <h2>📈 Mijn GroeiTeam</h2>
        <p>{render_pakket_badge(pakket, groot=True)} · {status_dot} {status} · Volgende check-in: <strong>{volgende}</strong></p>
        <p style="margin-top:0.3rem;font-size:0.72rem;color:var(--text-muted);">
            Sinds {gt.get("sinds","—")} · {cfg["workflows"]} workflows · {cfg["prijs_maand"]:,} EUR/mnd
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Snelle stats ─────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)
wf = gt.get("workflows", [])
actieve_wf = sum(1 for w in wf if w.get("actief"))
hitl = gt.get("hitl_samenvatting", {})
totaal_verwerkt = sum(w.get("items_verwerkt", 0) for w in wf)
hitl_goed = hitl.get("deze_maand_goedgekeurd", 0)

with col1:
    st.markdown(f'<div class="gt-stat"><div class="gt-stat-num">{len(wf)}</div><div class="gt-stat-lab">Workflows</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="gt-stat"><div class="gt-stat-num">{actieve_wf}</div><div class="gt-stat-lab">Actief</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="gt-stat"><div class="gt-stat-num">{totaal_verwerkt:,}</div><div class="gt-stat-lab">Verwerkt</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="gt-stat"><div class="gt-stat-num">{cfg["workflows"]}</div><div class="gt-stat-lab">Incl. pakket</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="gt-stat"><div class="gt-stat-num">{cfg["prijs_maand"]:,}</div><div class="gt-stat-lab">/mnd</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Workflows ────────────────────────────────────────────
st.markdown("### 🤖 Workflows")
if wf:
    wcols = st.columns(2)
    for i, w in enumerate(wf):
        with wcols[i % 2]:
            st.markdown(render_workflow_card(w), unsafe_allow_html=True)
else:
    st.info("Geen workflows geconfigureerd.")

# ─── HITL Samenvatting ────────────────────────────────────
if hitl:
    st.markdown("### 👤 Human In The Loop")
    st.markdown(render_hitl_samenvatting(hitl), unsafe_allow_html=True)

# ─── KPI Koppeling ────────────────────────────────────────
kpi_kopp = gt.get("kpi_koppeling", {})
if kpi_kopp:
    st.markdown("### 🔗 KPI-Koppeling")
    st.markdown(f"""
    <div style="background:var(--card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:0.8rem;">
        <table style="width:100%;font-size:0.78rem;color:var(--text-sec);">
            <tr><th style="text-align:left;color:var(--text-muted);font-weight:500;padding:0.3rem 0;">GroeiTeam Belofte</th>
                <th style="text-align:right;color:var(--text-muted);font-weight:500;padding:0.3rem 0;">Gekoppelde KPI</th></tr>
            {''.join(f'<tr><td style="padding:0.3rem 0;">{b}</td><td style="text-align:right;padding:0.3rem 0;color:var(--primary);font-weight:500;">{k}</td></tr>' for b, k in kpi_kopp.items())}
        </table>
    </div>
    """, unsafe_allow_html=True)

# ─── Check-in Historie ────────────────────────────────────
hist = gt.get("checkin_historie", [])
if hist:
    st.markdown("### 📅 Check-in Historie")
    for item in hist[:5]:
        st.markdown(render_checkin_item(item), unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────
st.markdown('<div class="gt-footer">🌊 BigWaves — uw AI-groeiteam · Wekelijkse check-in · Datagedreven · Menselijk gecheckt</div>', unsafe_allow_html=True)
