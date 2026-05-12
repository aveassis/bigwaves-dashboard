# GroeiTeam UI helpers — BigWaves Dashboard
import streamlit as st

# ─── Pakket config ────────────────────────────────────────
PAKKETTEN = {
    "Pilot": {"kleur": "#8b5cf6", "bg": "rgba(139,92,246,0.12)", "prijs_maand": 0, "prijs_jaar": 0, "setup": 0, "workflows": 1},
    "Start": {"kleur": "#3b82f6", "bg": "rgba(59,130,246,0.12)", "prijs_maand": 997, "prijs_jaar": 9970, "setup": 2500, "workflows": 1},
    "Groei": {"kleur": "#f59e0b", "bg": "rgba(245,158,11,0.12)", "prijs_maand": 1497, "prijs_jaar": 14970, "setup": 2500, "workflows": 2},
    "Pro":    {"kleur": "#10b981", "bg": "rgba(16,185,129,0.12)", "prijs_maand": 2499, "prijs_jaar": 24990, "setup": 2500, "workflows": 5},
}

def render_pakket_badge(pakket, groot=False):
    cfg = PAKKETTEN.get(pakket, PAKKETTEN["Start"])
    fs = "0.85rem" if groot else "0.72rem"
    return f'<span style="background:{cfg["bg"]};color:{cfg["kleur"]};font-size:{fs};font-weight:600;padding:0.2rem 0.55rem;border-radius:6px;border:1px solid {cfg["kleur"]}33;">{pakket}</span>'

def render_health_ring(score, size=80):
    # Kleur op basis van threshold
    clr = "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
    pct = min(max(score, 0), 100)
    # SVG donut
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 36 36" style="display:inline-block;">
        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="3"/>
        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none" stroke="{clr}" stroke-width="3" stroke-dasharray="{pct}, 100"
            stroke-linecap="round"/>
        <text x="18" y="20.5" text-anchor="middle" font-size="7" font-weight="700" fill="{clr}">{score}</text>
    </svg>'''

def render_workflow_card(wf):
    sts = wf.get("status", "groen")
    dot = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}.get(sts, "#64748b")
    icons = {"lead": "🎯", "support": "💬", "finance": "💰", "data": "📊", "reporting": "📋"}
    icon = icons.get(wf.get("type", ""), "⚙️")
    return f'''<div class="wf-card">
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.4rem;">
            <span style="font-size:1.2rem;">{icon}</span>
            <div style="flex:1;">
                <div style="font-size:0.82rem;font-weight:600;color:var(--text);">{wf["naam"]}</div>
                <div style="font-size:0.68rem;color:var(--text-muted);">{wf.get("items_verwerkt",0):,} verwerkt</div>
            </div>
            <span style="width:8px;height:8px;border-radius:50%;background:{dot};display:inline-block;"></span>
        </div>
        <div style="display:flex;gap:0.8rem;font-size:0.68rem;color:var(--text-sec);">
            <span>🔄 {wf.get("opvolgmomenten",0)} opvolgmomenten</span>
            <span>📅 {wf.get("laatste_actie","—")}</span>
        </div>
    </div>'''

def render_hitl_samenvatting(hitl):
    if not hitl:
        return ""
    total = hitl.get("deze_maand_goedgekeurd", 0) + hitl.get("deze_maand_geweigerd", 0)
    ratio = hitl.get("deze_maand_goedgekeurd", 0) / total * 100 if total > 0 else 0
    return f'''<div class="hitl-summary">
        <div class="hitl-stat"><span class="hitl-num">{hitl.get("deze_maand_goedgekeurd",0):,}</span><span class="hitl-lab">goedgekeurd</span></div>
        <div class="hitl-stat"><span class="hitl-num">{hitl.get("deze_maand_geweigerd",0)}</span><span class="hitl-lab">geweigerd</span></div>
        <div class="hitl-stat"><span class="hitl-num">{ratio:.0f}%</span><span class="hitl-lab">accuraatheid</span></div>
        <div class="hitl-stat"><span class="hitl-num">{hitl.get("wachttijd_gemiddeld","—")}</span><span class="hitl-lab">gem. wachttijd</span></div>
    </div>'''
def render_roi_card(maandprijs, besparing=None, vorige_besparing=None):
    """Prominente ROI-kaart: kosten vs besparing vs netto winst."""
    if besparing is None:
        return ""  # geen data, toon niets

    netto = besparing - maandprijs
    rendement = (besparing / maandprijs * 100) if maandprijs > 0 else 0
    trend_pct = None
    if vorige_besparing is not None and vorige_besparing > 0:
        trend_pct = ((besparing - vorige_besparing) / vorige_besparing) * 100

    netto_cls = "roi-positive" if netto >= 0 else "roi-negative"
    netto_icon = "▲" if netto >= 0 else "▼"
    trend_cls = "roi-positive" if trend_pct is not None and trend_pct >= 0 else ("roi-negative" if trend_pct is not None else "roi-neutral")
    trend_icon = "↑" if trend_pct is not None and trend_pct >= 0 else ("↓" if trend_pct is not None else "→")
    trend_txt = f"{trend_icon} {abs(trend_pct):.0f}% vs vorige maand" if trend_pct is not None else "—"

    return f'''<div class="roi-card">
    <div class="roi-grid">
        <div class="roi-item">
            <div class="roi-label">Investering</div>
            <div class="roi-value">€{maandprijs:,}</div>
            <div class="roi-spark">/maand</div>
        </div>
        <div class="roi-item">
            <div class="roi-label">Besparing</div>
            <div class="roi-value roi-positive">€{besparing:,}</div>
            <div class="roi-spark">deze maand</div>
        </div>
        <div class="roi-item roi-net">
            <div class="roi-label">Netto resultaat</div>
            <div class="roi-value {netto_cls}">{netto_icon} €{abs(netto):,}</div>
            <div class="roi-spark">{rendement:.0f}% rendement</div>
        </div>
        <div class="roi-item">
            <div class="roi-label">Trend</div>
            <div class="roi-value {trend_cls}">{trend_txt}</div>
            <div class="roi-spark">besparing</div>
        </div>
    </div>
</div>'''



    sts = item.get("status", "groen")
    dot = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}.get(sts, "#64748b")
    return f'''<div class="checkin-item">
        <div style="display:flex;align-items:flex-start;gap:0.6rem;">
            <span style="width:10px;height:10px;border-radius:50%;background:{dot};margin-top:4px;flex-shrink:0;"></span>
            <div>
                <div style="font-size:0.78rem;font-weight:600;color:var(--text);">{item["type"]}</div>
                <div style="font-size:0.65rem;color:var(--text-muted);">{item["datum"]}</div>
                <div style="font-size:0.72rem;color:var(--text-sec);margin-top:2px;">{item.get("notities","")}</div>
            </div>
        </div>
    </div>'''

GROEI_TEAM_CSS = """
<style>
.gt-header {
    display:flex; align-items:center; gap:1.5rem;
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius);
    padding:1.2rem 1.5rem; margin-bottom:1rem;
}
.gt-header-info { flex:1; }
.gt-header-info h2 { margin:0 0 0.2rem 0 !important; }
.gt-header-info p { margin:0; font-size:0.78rem; color:var(--text-muted); }
.gt-stats {
    display:grid; grid-template-columns:repeat(auto-fit, minmax(90px, 1fr)); gap:0.5rem;
}
.gt-stat {
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius-sm);
    padding:0.7rem; text-align:center;
}
.gt-stat-num {
    font-size:1.1rem; font-weight:700; color:var(--text); line-height:1.2;
}
.gt-stat-lab {
    font-size:0.62rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px;
}
.wf-card {
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius-sm);
    padding:0.8rem; margin-bottom:0.5rem;
    transition:all 0.2s ease;
}
.wf-card:hover { border-color:var(--border-light); }
.hitl-summary {
    display:grid; grid-template-columns:repeat(2,1fr); gap:0.6rem;
}
.hitl-stat {
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius-sm);
    padding:0.6rem; text-align:center;
}
.hitl-num { font-size:1rem; font-weight:700; color:var(--text); display:block; }
.hitl-lab { font-size:0.62rem; color:var(--text-muted); text-transform:uppercase; }
.checkin-item {
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius-sm);
    padding:0.7rem; margin-bottom:0.4rem;
}
.roi-card {
    background:var(--card);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem 1.2rem;
    margin-bottom:1.2rem;
}
.roi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
}
.roi-item { text-align: center; }
.roi-item .roi-label {
    font-size:0.62rem; color:var(--text-muted);
    text-transform:uppercase; letter-spacing:0.5px;
    margin-bottom:0.15rem;
}
.roi-item .roi-value {
    font-size:1.1rem; font-weight:700; line-height:1.3;
}
.roi-item .roi-trend { font-size:0.68rem; margin-top:0.1rem; }
.roi-positive { color:#10b981; }
.roi-negative { color:#ef4444; }
.roi-neutral  { color:var(--text-muted); }
.roi-net {
    border-left:1px solid var(--border);
    padding-left:0.8rem;
}
.roi-spark { font-size:0.68rem; color:var(--text-muted); }
@media (max-width:600px) {
    .roi-grid { grid-template-columns:repeat(2,1fr); }
    .roi-net { border-left:none; padding-left:0; }
}
.gt-footer {
    text-align:center; margin-top:1.5rem;
    font-size:0.7rem; color:var(--text-muted);
}
</style>
"""
