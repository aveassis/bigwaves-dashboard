# pages/1_GroeiTeam.py — Mijn GroeiTeam overzicht
import streamlit as st
from pathlib import Path
import json
import sqlite3
import sys
sys.path.insert(0, str(Path(__file__).parent))
from groei_team_ui import (
    render_health_ring, render_pakket_badge, render_workflow_card,
    render_hitl_samenvatting, bereken_health_score, GROEI_TEAM_CSS
)

# Geen set_page_config hier — overgenomen van dashboard.py

# Check login
if "ingelogd" not in st.session_state or not st.session_state.ingelogd:
    st.warning("Log eerst in via het dashboard.")
    st.stop()

# Laad klant data
klant_naam = st.session_state.get("klant_naam", None)
if not klant_naam:
    st.error("Geen klant geselecteerd.")
    st.stop()

data_dir = Path(__file__).parent.parent / "data"
klant_bestand = data_dir / f"{klant_naam.lower().replace(' ', '-')}.json"
if not klant_bestand.exists():
    klant_bestand = data_dir / "demo-klant.json"

with open(klant_bestand) as f:
    data = json.load(f)

# Inject GroeiTeam CSS
st.markdown(GROEI_TEAM_CSS, unsafe_allow_html=True)

# Accent kleur
accent = data.get("accent_kleur", "#10b981")
st.markdown(
    f"<style>:root{{--primary:{accent};}}</style>",
    unsafe_allow_html=True,
)

# Haal GroeiTeam data
gt = data.get("groei_team", {})
pakket = gt.get("pakket", "—")
health = gt.get("health_score") or bereken_health_score(data)

# === HEADER ===
cols = st.columns([1, 3, 1])
with cols[0]:
    st.markdown(render_health_ring(health), unsafe_allow_html=True)
with cols[1]:
    st.markdown("<h1 style='margin:0;'>Mijn GroeiTeam</h1>", unsafe_allow_html=True)
    st.markdown(
        f"{render_pakket_badge(pakket)} "
        f"<span style='color:#94a3b8;font-size:0.78rem;margin-left:8px;'>"
        f"Sinds {gt.get('sinds','—')} &middot; "
        f"{gt.get('contact_frequentie','wekelijks').capitalize()} contact</span>",
        unsafe_allow_html=True,
    )
with cols[2]:
    status = gt.get("status", "actief")
    if status == "actief":
        st.markdown(
            f'<div style="text-align:right;">'
            f'<span style="color:#10b981;font-size:0.78rem;">&#9679; Actief</span>'
            f'<br><span style="color:#64748b;font-size:0.68rem;">Volgende check-in: {gt.get("volgende_checkin","—")}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("<hr class='gt-divider'>", unsafe_allow_html=True)

# === WORKFLOWS ===
st.markdown("<div class='gt-section-title'>&#9881;&#65039; Actieve Workflows</div>", unsafe_allow_html=True)
workflows = gt.get("workflows", [])
if workflows:
    wf_cols = st.columns(min(len(workflows), 3))
    for i, wf in enumerate(workflows):
        with wf_cols[i % len(wf_cols)]:
            st.markdown(render_workflow_card(wf), unsafe_allow_html=True)
else:
    st.info("Nog geen workflows ingesteld. Neem contact op met je accountmanager.")

# === HITL SAMENVATTING + CHECK-IN ===
cols2 = st.columns(2)
with cols2[0]:
    st.markdown("<div class='gt-section-title'>&#9989; Human-in-the-Loop</div>", unsafe_allow_html=True)
    hitl = gt.get("hitl_samenvatting", {})
    st.markdown(render_hitl_samenvatting(hitl), unsafe_allow_html=True)

with cols2[1]:
    st.markdown("<div class='gt-section-title'>&#128197; Check-in Historie</div>", unsafe_allow_html=True)
    checkins = gt.get("checkin_historie", [
        {"datum": "2026-04-28", "type": "wekelijkse check-in",
         "notities": "Lead opvolging loopt goed. KPI's op groen.", "status": "groen"},
        {"datum": "2026-04-21", "type": "wekelijkse check-in",
         "notities": "Nieuwe workflow kandidaatopvolging gestart.", "status": "groen"},
        {"datum": "2026-04-14", "type": "wekelijkse check-in",
         "notities": "Kostenbesparing zichtbaar. Doel &euro;3.000 gehaald.", "status": "groen"},
    ])
    checkin_html = '<div style="background:var(--card);border:1px solid var(--border);border-radius:12px;padding:0.8rem 1rem;">'
    kleur_map = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}
    for ci in checkins:
        c = kleur_map.get(ci.get("status", "groen"), "#10b981")
        checkin_html += f"""
        <div class="checkin-item">
            <div class="checkin-dot" style="background:{c};"></div>
            <div>
                <div class="checkin-date">{ci.get('datum','')} &middot; {ci.get('type','')}</div>
                <div class="checkin-text">{ci.get('notities','')}</div>
            </div>
        </div>"""
    checkin_html += "</div>"
    st.markdown(checkin_html, unsafe_allow_html=True)

# === KPI KOPPELING ===
st.markdown("<hr class='gt-divider'>", unsafe_allow_html=True)
st.markdown("<div class='gt-section-title'>&#128202; Hoe presteert jouw GroeiTeam?</div>", unsafe_allow_html=True)

kpi_koppeling = gt.get("kpi_koppeling", {})
if kpi_koppeling and data.get("periodes"):
    periodes = data["periodes"]
    huidige_periode = list(periodes.keys())[-1] if isinstance(periodes, dict) else None
    if huidige_periode:
        pd = periodes[huidige_periode]
        kpis = pd.get("kpis", {})
        koppel_items = [
            (
                "&#9201; Opvolging binnen 24u",
                kpi_koppeling.get("opvolging_binnen_24u"),
                "snelheid van reactie op nieuwe leads/kandidaten",
            ),
            (
                "&#127919; Gemiste kansen hersteld",
                kpi_koppeling.get("gemiste_kansen"),
                "aantal dat zonder GroeiTeam was blijven liggen",
            ),
            (
                "&#128200; Conversie uit opvolging",
                kpi_koppeling.get("conversie"),
                "percentage dat leidt tot gesprek of plaatsing",
            ),
        ]

        koppel_cols = st.columns(3)
        for i, (label, kpi_key, uitleg) in enumerate(koppel_items):
            with koppel_cols[i]:
                if kpi_key and kpi_key in kpis:
                    ki = kpis[kpi_key]
                    w = ki.get("waarde", "—")
                    doel = ki.get("doel", "—")
                    eenheid = ki.get("eenheid", "")
                    st.markdown(
                        f"""
                    <div class="kpi-box" style="text-align:center;">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-val" style="font-size:1.8rem;">{w}{eenheid}</div>
                        <div style="font-size:0.72rem;color:#64748b;">Doel: {doel}{eenheid}</div>
                        <div style="font-size:0.68rem;color:#64748b;margin-top:4px;padding-top:4px;border-top:1px solid var(--border);">{uitleg}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                    <div class="kpi-box" style="text-align:center;opacity:0.5;">
                        <div class="kpi-label">{label}</div>
                        <div style="font-size:1.2rem;color:#64748b;padding:10px 0;">Nog niet ingesteld</div>
                        <div style="font-size:0.68rem;color:#64748b;">{uitleg}</div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

# === LINKEDIN OUTREACH (alleen Pro) ===
if pakket == "Pro":
    st.markdown("<hr class='gt-divider'>", unsafe_allow_html=True)
    st.markdown("<div class='gt-section-title'>&#128279; LinkedIn Outreach</div>", unsafe_allow_html=True)

    # Probeer data uit linkedin db
    linkedin_db = Path(__file__).parent.parent / "linkedin-outreach" / "data" / "linkedin.db"
    li_stats = {}
    if linkedin_db.exists():
        try:
            conn = sqlite3.connect(str(linkedin_db))
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM prospects")
            li_stats["totaal"] = c.fetchone()[0]
            c.execute("SELECT status, COUNT(*) FROM prospects GROUP BY status")
            li_stats["per_status"] = dict(c.fetchall())
            c.execute("SELECT COUNT(*) FROM actions WHERE action_date >= date('now', '-7 days')")
            li_stats["acties_7d"] = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM messages WHERE reply_received = 1")
            li_stats["replies"] = c.fetchone()[0]
            conn.close()
        except Exception:
            li_stats = {}

    if li_stats:
        li_cols = st.columns(4)
        with li_cols[0]:
            st.markdown(f'<div class="kpi-box" style="text-align:center;"><div class="kpi-label">Prospects</div><div class="kpi-val" style="font-size:1.6rem;">{li_stats.get("totaal", 0)}</div></div>', unsafe_allow_html=True)
        with li_cols[1]:
            connected = li_stats.get("per_status", {}).get("connected", 0)
            st.markdown(f'<div class="kpi-box" style="text-align:center;"><div class="kpi-label">Verbonden</div><div class="kpi-val" style="font-size:1.6rem;">{connected}</div></div>', unsafe_allow_html=True)
        with li_cols[2]:
            st.markdown(f'<div class="kpi-box" style="text-align:center;"><div class="kpi-label">Reacties</div><div class="kpi-val" style="font-size:1.6rem;">{li_stats.get("replies", 0)}</div></div>', unsafe_allow_html=True)
        with li_cols[3]:
            st.markdown(f'<div class="kpi-box" style="text-align:center;"><div class="kpi-label">Acties (7d)</div><div class="kpi-val" style="font-size:1.6rem;">{li_stats.get("acties_7d", 0)}</div></div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;margin-top:0.3rem;">'
            '<a href="/pages/3_LinkedIn" target="_blank" style="color:#10b981;font-size:0.78rem;text-decoration:none;">'
            '&#8599; Open volledig LinkedIn overzicht</a></div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("LinkedIn outreach nog niet gestart. De cronjob draait automatisch op werkdagen.")

# === RAPPORTAGE KNOP ===
st.markdown("<hr class='gt-divider'>", unsafe_allow_html=True)
col_rapport = st.columns([1, 2, 1])
with col_rapport[1]:
    st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
    if st.button(
        "&#128196; Genereer GroeiTeam Rapport",
        use_container_width=True,
        type="primary",
    ):
        st.success(
            "Rapport wordt gegenereerd... (functionaliteit komt binnenkort beschikbaar)"
        )
    st.markdown("</div>", unsafe_allow_html=True)
