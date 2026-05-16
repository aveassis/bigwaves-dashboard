# pages/3_LinkedIn.py — LinkedIn Outreach overzicht (schone versie)
import streamlit as st
st.set_page_config(page_title="LinkedIn — BigWaves", page_icon="🔗", layout="wide")
from sidebar_ui import render_sidebar
from pathlib import Path
import sqlite3
from datetime import date

# Check login
if "ingelogd" not in st.session_state or not st.session_state.ingelogd:
    st.warning("Log eerst in via het dashboard.")
    st.stop()

# Laad data voor sidebar
kn = st.session_state.get("klant_naam", "")
data = st.session_state.get("data", {})
gt = data.get("groei_team", {}) if data else {}
periodes = data.get("periodes", None)
render_sidebar(data, kn, gt, periodes, list(periodes.keys()) if periodes else None)

# LinkedIn DB pad
linkedin_db = Path(__file__).parent.parent / "linkedin-outreach" / "data" / "linkedin.db"
if not linkedin_db.exists():
    st.warning("LinkedIn database nog niet beschikbaar.")
    st.stop()

def get_stats(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    stats = {}

    # Totalen
    c.execute("SELECT COUNT(*) as total FROM prospects")
    stats["totaal"] = c.fetchone()["total"]

    c.execute("SELECT status, COUNT(*) as count FROM prospects GROUP BY status")
    stats["per_status"] = {row["status"]: row["count"] for row in c.fetchall()}

    # Acties vandaag
    vandaag = date.today().isoformat()
    c.execute("SELECT action_type, COUNT(*) as count FROM actions WHERE date(created_at) = ? GROUP BY action_type", (vandaag,))
    stats["acties_vandaag"] = {row["action_type"]: row["count"] for row in c.fetchall()}

    # Inbound replies
    c.execute("SELECT COUNT(*) as count FROM messages WHERE direction = 'inbound'")
    stats["replies"] = c.fetchone()["count"]

    # Meetings
    c.execute("SELECT COUNT(*) as count FROM messages WHERE message_type LIKE '%meeting%' OR message_type LIKE '%positive%'")
    stats["meetings"] = c.fetchone()["count"]

    # Connecties vandaag
    c.execute("SELECT COUNT(*) as count FROM actions WHERE action_type = 'connect_request' AND date(created_at) = ?", (vandaag,))
    stats["connecties_vandaag"] = c.fetchone()["count"]

    # Recente acties
    c.execute("""SELECT a.action_type, a.created_at AS actie_datum,
                      (COALESCE(p.voornaam,'') || ' ' || COALESCE(p.achternaam,'')) AS naam,
                      p.bedrijf AS bedrijf
               FROM actions a JOIN prospects p ON a.prospect_id = p.id
               WHERE a.created_at >= date('now', '-7 days')
               ORDER BY a.created_at DESC LIMIT 20""")
    stats["recente_acties"] = [dict(row) for row in c.fetchall()]

    # Prospect lijst
    c.execute("""SELECT id, (COALESCE(voornaam,'') || ' ' || COALESCE(achternaam,'')) AS naam,
                      titel AS functie, bedrijf, '' AS locatie,
                      status, created_at AS toegevoegd, updated_at AS laatste_actie
               FROM prospects ORDER BY updated_at DESC NULLS LAST, created_at DESC LIMIT 50""")
    stats["prospects"] = [dict(row) for row in c.fetchall()]

    conn.close()
    return stats

# === UI ===
st.set_page_config(page_title="LinkedIn Outreach", page_icon="🔗", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3 { color: #f1f5f9 !important; }
    .metric-card {
        background: #1e293b; border: 1px solid #334155;
        border-radius: 12px; padding: 1rem 1.2rem; text-align: center;
    }
    .metric-val { font-size: 2rem; font-weight: 700; color: #10b981; line-height: 1.2; }
    .metric-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
    .prospect-row {
        background: #1e293b; border: 1px solid #334155;
        border-radius: 8px; padding: 0.6rem 1rem; margin-bottom: 4px; font-size: 0.85rem;
    }
    .status-badge {
        display: inline-block; padding: 2px 8px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 600;
    }
    .status-new { background: #1e3a5f; color: #60a5fa; }
    .status-warming { background: #5b3a1a; color: #fbbf24; }
    .status-warmed { background: #1a3d1a; color: #34d399; }
    .status-connecting { background: #3b1a5e; color: #c084fc; }
    .status-connected { background: #1a3d3d; color: #2dd4bf; }
    .status-replied { background: #1a3d1a; color: #10b981; }
    .status-meeting { background: #1a5e1a; color: #4ade80; }
    .status-rejected { background: #3d1a1a; color: #f87171; }
    .activity-item {
        display: flex; gap: 8px; align-items: center;
        border-bottom: 1px solid #1e293b; padding: 6px 0; font-size: 0.82rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔗 LinkedIn Outreach")

try:
    stats = get_stats(linkedin_db)
except Exception as e:
    st.error(f"Fout bij laden data: {e}")
    st.stop()

# Metrics
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{stats['totaal']}</div><div class='metric-label'>Totaal Prospects</div></div>", unsafe_allow_html=True)
with c2:
    connected = stats["per_status"].get("connected", 0)
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{connected}</div><div class='metric-label'>Verbonden</div></div>", unsafe_allow_html=True)
with c3:
    replied = stats["per_status"].get("replied", 0)
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{replied}</div><div class='metric-label'>Reacties</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{stats.get('meetings', 0)}</div><div class='metric-label'>Gesprekken</div></div>", unsafe_allow_html=True)
with c5:
    vandaag = sum(stats["acties_vandaag"].values())
    st.markdown(f"<div class='metric-card'><div class='metric-val'>{vandaag}</div><div class='metric-label'>Acties Vandaag</div></div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#334155; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# Recente activiteit + status
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("#### 📋 Recente Activiteit (7 dagen)")
    if stats["recente_acties"]:
        icon_map = {"visit": "👁️", "like": "👍", "comment": "💬", "connect_request": "🔗", "message": "✉️", "followup": "🔄"}
        for a in stats["recente_acties"][:15]:
            icon = icon_map.get(a["action_type"], "•")
            st.markdown(f"<div class='activity-item'><span>{icon}</span><span><strong>{a.get('naam','?')}</strong> ({a.get('bedrijf','')})</span><span style='color:#64748b;font-size:0.75rem;'>{a.get('actie_datum','')[:16]}</span></div>", unsafe_allow_html=True)
    else:
        st.info("Nog geen activiteit.")

with col_right:
    st.markdown("#### 📊 Status Verdeling")
    status_kleuren = {
        "new": "#60a5fa", "warming": "#fbbf24", "warmed": "#34d399",
        "connecting": "#c084fc", "connected": "#2dd4bf",
        "replied": "#10b981", "meeting": "#4ade80", "rejected": "#f87171",
    }
    for status in ["new", "warming", "warmed", "connecting", "connected", "replied", "meeting", "rejected"]:
        count = stats["per_status"].get(status, 0)
        if count > 0:
            kleur = status_kleuren.get(status, "#64748b")
            st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:4px;'><span style='color:#94a3b8;font-size:0.82rem;'><span style='color:{kleur};'>●</span> {status.capitalize()}</span><span style='color:#f1f5f9;font-weight:600;'>{count}</span></div>", unsafe_allow_html=True)

    st.markdown("#### 🔧 Limieten Vandaag")
    limieten = [
        ("Connecties", stats["connecties_vandaag"], 25),
        ("Visits", stats["acties_vandaag"].get("visit", 0), 50),
        ("Likes", stats["acties_vandaag"].get("like", 0), 30),
    ]
    for label, used, max_l in limieten:
        pct = min(used / max_l, 1.0)
        bar_kleur = "#10b981" if pct < 0.8 else ("#fbbf24" if pct < 1.0 else "#ef4444")
        st.markdown(f"<div style='margin-bottom:6px;'><div style='display:flex;justify-content:space-between;font-size:0.78rem;'><span style='color:#94a3b8;'>{label}</span><span style='color:#f1f5f9;'>{used}/{max_l}</span></div><div style='background:#1e293b;border-radius:10px;height:6px;'><div style='background:{bar_kleur};width:{pct*100:.0f}%;height:6px;border-radius:10px;'></div></div></div>", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#334155; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# Prospect lijst
st.markdown("#### 🎯 Prospects Overzicht")
status_filter = st.selectbox("Filter op status", ["Alle", "new", "warming", "warmed", "connecting", "connected", "replied", "meeting", "rejected"], label_visibility="collapsed")

for p in stats["prospects"]:
    if status_filter != "Alle" and p["status"] != status_filter:
        continue
    s_class = f"status-{p['status']}" if p["status"] in status_kleuren else "status-new"
    st.markdown(
        f"<div class='prospect-row'><div style='display:flex;justify-content:space-between;align-items:center;'>"
        f"<div><strong style='color:#f1f5f9;'>{p.get('naam','?')}</strong>"
        f"<span style='color:#94a3b8;font-size:0.78rem;'> — {p.get('functie','')} bij {p.get('bedrijf','')}</span></div>"
        f"<div style='display:flex;gap:6px;align-items:center;'>"
        f"<span class='status-badge {s_class}'>{p['status']}</span>"
        f"<span style='color:#64748b;font-size:0.7rem;'>{p.get('laatste_actie','')[:10] if p.get('laatste_actie') else ''}</span>"
        f"</div></div></div>",
        unsafe_allow_html=True,
    )

if not stats["prospects"]:
    st.info("Nog geen prospects in de database.")

if st.button("🔄 Ververs Data", use_container_width=True):
    st.rerun()
