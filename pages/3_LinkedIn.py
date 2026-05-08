# pages/3_LinkedIn.py — LinkedIn Outreach overzicht
import streamlit as st
from pathlib import Path
import json
import sqlite3
import sys
from datetime import datetime, date

sys.path.insert(0, str(Path(__file__).parent.parent))

# Check login (alleen voor beheerder)
if "ingelogd" not in st.session_state or not st.session_state.ingelogd:
    st.warning("Log eerst in via het dashboard.")
    st.stop()

# Alleen voor Pro pakket
data = st.session_state.get("data", {})
gt = data.get("groei_team", {})
pakket = gt.get("pakket", "")
if pakket != "Pro":
    st.set_page_config(page_title="LinkedIn Outreach", page_icon="🔗", layout="wide")
    st.markdown("""
    <style>
        .block-container { padding-top: 3rem; text-align: center; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("#### 🔗 LinkedIn Outreach")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="background:#1e293b;border:1px solid #334155;border-radius:14px;padding:3rem 2rem;max-width:500px;margin:0 auto;">'
        '<div style="font-size:3rem;margin-bottom:1rem;">⭐</div>'
        '<h3 style="color:#f1f5f9;margin-bottom:0.5rem;">Alleen beschikbaar in Pro</h3>'
        '<p style="color:#94a3b8;font-size:0.82rem;">LinkedIn outreach is een exclusieve functie van het GroeiTeam Pro pakket. '
        'Neem contact op met je accountmanager voor een upgrade.</p>'
        '<div style="margin-top:1.5rem;padding:0.8rem;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:10px;">'
        '<p style="color:#10b981;font-weight:600;margin:0;font-size:0.85rem;">Pro &euro;1.997/mnd</p>'
        '<p style="color:#94a3b8;font-size:0.72rem;margin:4px 0 0 0;">Alles + LinkedIn outreach + procesautomatisering</p>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.stop()

# LinkedIn DB pad
linkedin_db = Path(__file__).parent.parent / "linkedin-outreach" / "data" / "linkedin.db"
if not linkedin_db.exists():
    st.error("LinkedIn outreach database niet gevonden. Voer eerst 'python main.py setup' uit in /opt/data/bigwaves/linkedin-outreach/")
    st.stop()

def get_stats(db_path):
    """Haal outreach statistieken uit SQLite."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    stats = {}

    # Totalen
    c.execute("SELECT COUNT(*) as total FROM prospects")
    stats["totaal"] = c.fetchone()["total"]

    c.execute(
        "SELECT status, COUNT(*) as count FROM prospects GROUP BY status"
    )
    stats["per_status"] = {row["status"]: row["count"] for row in c.fetchall()}

    # Acties vandaag
    vandaag = date.today().isoformat()
    c.execute(
        "SELECT action_type, COUNT(*) as count FROM actions WHERE date(action_date) = ? GROUP BY action_type",
        (vandaag,),
    )
    stats["acties_vandaag"] = {row["action_type"]: row["count"] for row in c.fetchall()}

    # Replies (positief)
    c.execute(
        "SELECT COUNT(*) as count FROM messages WHERE reply_received = 1 AND reply_content != ''"
    )
    stats["replies"] = c.fetchone()["count"]

    # Meetings (positief geclassificeerd)
    c.execute(
        "SELECT COUNT(*) as count FROM messages WHERE reply_received = 1 AND IFNULL(details, '') LIKE '%positive%'"
    )
    stats["meetings"] = c.fetchone()["count"]

    # Connecties verstuurd vandaag
    c.execute(
        "SELECT COUNT(*) as count FROM actions WHERE action_type = 'connect_request' AND date(action_date) = ?",
        (vandaag,),
    )
    stats["connecties_vandaag"] = c.fetchone()["count"]

    # Recente activiteit (laatste 7 dagen)
    c.execute(
        """SELECT a.action_type, a.action_date, p.name, p.company
           FROM actions a JOIN prospects p ON a.prospect_id = p.id
           WHERE a.action_date >= date('now', '-7 days')
           ORDER BY a.action_date DESC LIMIT 20"""
    )
    stats["recente_acties"] = [dict(row) for row in c.fetchall()]

    # Prospect lijst
    c.execute(
        """SELECT id, name, title, company, location, status, date_added, last_action_date
           FROM prospects ORDER BY last_action_date DESC NULLS LAST, date_added DESC LIMIT 50"""
    )
    stats["prospects"] = [dict(row) for row in c.fetchall()]

    conn.close()
    return stats

# === DASHBOARD UI ===
st.set_page_config(page_title="LinkedIn Outreach", page_icon="🔗", layout="wide")

# Pas donker thema aan voor deze pagina
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    h1, h2, h3 { color: #f1f5f9 !important; }
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 700;
        color: #10b981;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .prospect-row {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 4px;
        font-size: 0.85rem;
    }
    .status-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
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
        display: flex;
        gap: 8px;
        align-items: center;
        border-bottom: 1px solid #1e293b;
        padding: 6px 0;
        font-size: 0.82rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔗 LinkedIn Outreach")

# Laad data
stats = get_stats(linkedin_db)

# === METRICS RIJ ===
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{stats['totaal']}</div>
        <div class="metric-label">Totaal Prospects</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    connected = stats["per_status"].get("connected", 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{connected}</div>
        <div class="metric-label">Verbonden</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    replied = stats["per_status"].get("replied", 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{replied}</div>
        <div class="metric-label">Reacties</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    meetings = stats.get("meetings", 0)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{meetings}</div>
        <div class="metric-label">Gesprekken</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    vandaag_acties = sum(stats["acties_vandaag"].values())
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{vandaag_acties}</div>
        <div class="metric-label">Acties Vandaag</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:#334155; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# === RECENTE ACTIVITEIT + STATUS ===
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("#### 📋 Recente Activiteit (7 dagen)")
    if stats["recente_acties"]:
        for actie in stats["recente_acties"][:15]:
            # Icoon per actie type
            icon_map = {
                "visit": "👁️",
                "like": "👍",
                "comment": "💬",
                "connect_request": "🔗",
                "message": "✉️",
                "followup": "🔄",
            }
            icon = icon_map.get(actie["action_type"], "•")
            st.markdown(
                f"<div class='activity-item'>"
                f"<span>{icon}</span>"
                f"<span><strong>{actie.get('name','?')}</strong> ({actie.get('company','')})</span>"
                f"<span style='color:#64748b;font-size:0.75rem;'>{actie.get('action_date','')[:16]}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("Nog geen activiteit. Start met 'python main.py run' of voeg prospects toe.")

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
            status_label = status.capitalize()
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>"
                f"<span style='color:#94a3b8;font-size:0.82rem;'><span style='color:{kleur};'>●</span> {status_label}</span>"
                f"<span style='color:#f1f5f9;font-weight:600;'>{count}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("#### 🔧 Limieten Vandaag")
    limieten = [
        ("Connecties", stats["connecties_vandaag"], 25),
        ("Visits", stats["acties_vandaag"].get("visit", 0), 50),
        ("Likes", stats["acties_vandaag"].get("like", 0), 30),
    ]
    for label, used, max_l in limieten:
        pct = min(used / max_l, 1.0)
        bar_kleur = "#10b981" if pct < 0.8 else ("#fbbf24" if pct < 1.0 else "#ef4444")
        st.markdown(
            f"<div style='margin-bottom:6px;'>"
            f"<div style='display:flex;justify-content:space-between;font-size:0.78rem;'>"
            f"<span style='color:#94a3b8;'>{label}</span>"
            f"<span style='color:#f1f5f9;'>{used}/{max_l}</span>"
            f"</div>"
            f"<div style='background:#1e293b;border-radius:10px;height:6px;'>"
            f"<div style='background:{bar_kleur};width:{pct*100:.0f}%;height:6px;border-radius:10px;'></div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("<hr style='border-color:#334155; margin: 1.5rem 0;'>", unsafe_allow_html=True)

# === PROSPECT LIJST ===
st.markdown("#### 🎯 Prospects Overzicht")
status_filter = st.selectbox(
    "Filter op status",
    ["Alle", "new", "warming", "warmed", "connecting", "connected", "replied", "meeting", "rejected"],
    label_visibility="collapsed",
)

for p in stats["prospects"]:
    if status_filter != "Alle" and p["status"] != status_filter:
        continue

    status_class = f"status-{p['status']}" if p["status"] in status_kleuren else "status-new"
    st.markdown(
        f"<div class='prospect-row'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
        f"<div><strong style='color:#f1f5f9;'>{p.get('name','?')}</strong>"
        f"<span style='color:#94a3b8;font-size:0.78rem;'> — {p.get('title','')} bij {p.get('company','')}</span></div>"
        f"<div style='display:flex;gap:6px;align-items:center;'>"
        f"<span class='status-badge {status_class}'>{p['status']}</span>"
        f"<span style='color:#64748b;font-size:0.7rem;'>{p.get('last_action_date','')[:10] if p.get('last_action_date') else ''}</span>"
        f"</div></div></div>",
        unsafe_allow_html=True,
    )

if not stats["prospects"]:
    st.info("Nog geen prospects in de database. Voeg ze toe via 'python main.py search'.")

# === REFRESH KNOP ===
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Ververs Data", use_container_width=True):
    st.rerun()
