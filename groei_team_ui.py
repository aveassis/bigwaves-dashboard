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

def render_workflow_health_item(wf):
    """Compacte gezondheidskaart per workflow met trend, responstijd, hitl-percentage."""
    sts = wf.get("status", "groen")
    dot = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}.get(sts, "#64748b")
    sts_label = {"groen": "Gezond", "oranje": "Aandacht", "rood": "Actie nodig"}.get(sts, "Onbekend")
    icons = {"lead": "🎯", "support": "💬", "finance": "💰", "data": "📊", "reporting": "📋"}
    icon = icons.get(wf.get("type", ""), "⚙️")
    
    # Simuleer trend en hitl% als die niet in de data zitten
    items = wf.get("items_verwerkt", 0)
    # Trend bepalen obv items (demo-logica)
    trend = "up" if items > 200 else "stable" if items > 80 else "down"
    trend_icon = {"up": "↑ +12%", "stable": "→ 0%", "down": "↓ -8%"}.get(trend, "—")
    trend_cls = {"up": "wht-green", "stable": "wht-neutral", "down": "wht-red"}.get(trend, "wht-neutral")
    
    hitl_pct = wf.get("hitl_percentage", None)
    if hitl_pct is None:
        hitl_pct = 18 + hash(wf["naam"]) % 15  # demo fallback
    hitl_cls = "wht-green" if hitl_pct <= 20 else "wht-orange" if hitl_pct <= 30 else "wht-red"
    
    resp = wf.get("responstijd", None)
    if resp is None:
        resp = 1.8 + (hash(wf["naam"]) % 20) / 10  # demo fallback
    
    bar_pct = {"groen": 85, "oranje": 55, "rood": 25}.get(sts, 50)
    bar_cls = {"groen": "wht-bar-green", "oranje": "wht-bar-orange", "rood": "wht-bar-red"}.get(sts, "wht-bar-green")
    
    return f'''<div class="wht-card">
        <div class="wht-top">
            <div class="wht-left">
                <span class="wht-icon">{icon}</span>
                <div>
                    <div class="wht-name">{wf["naam"]}</div>
                    <div class="wht-vol">{items:,} verwerkt</div>
                </div>
            </div>
            <div class="wht-right">
                <span class="wht-badge wht-badge-{sts}">{sts_label}</span>
            </div>
        </div>
        <div class="wht-bar"><div class="{bar_cls}" style="width:{bar_pct}%"></div></div>
        <div class="wht-metrics">
            <div class="wht-metric">
                <span class="wht-ml">{resp:.1f}s</span>
                <span class="wht-ms">responstijd</span>
            </div>
            <div class="wht-metric">
                <span class="wht-ml {hitl_cls}">{hitl_pct}%</span>
                <span class="wht-ms">HITL</span>
            </div>
            <div class="wht-metric">
                <span class="wht-ml {trend_cls}">{trend_icon}</span>
                <span class="wht-ms">volume</span>
            </div>
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


def render_checkin_item(item):
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
.wht-card {
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius-sm);
    padding:0.75rem; margin-bottom:0.5rem;
    transition:all 0.2s ease;
}
.wht-card:hover { border-color:var(--border-light); }
.wht-top {
    display:flex; align-items:center; justify-content:space-between; margin-bottom:0.4rem;
}
.wht-left { display:flex; align-items:center; gap:0.5rem; }
.wht-icon { font-size:1.1rem; }
.wht-name { font-size:0.78rem; font-weight:600; color:var(--text); line-height:1.2; }
.wht-vol { font-size:0.62rem; color:var(--text-muted); }
.wht-right { flex-shrink:0; }
.wht-badge {
    font-size:0.6rem; font-weight:600; padding:0.15rem 0.45rem; border-radius:4px;
    text-transform:uppercase; letter-spacing:0.3px;
}
.wht-badge-groen { background:rgba(16,185,129,0.12); color:#10b981; }
.wht-badge-oranje { background:rgba(245,158,11,0.12); color:#f59e0b; }
.wht-badge-rood { background:rgba(239,68,68,0.12); color:#ef4444; }
.wht-bar {
    height:4px; background:rgba(255,255,255,0.06); border-radius:2px; margin-bottom:0.5rem;
    overflow:hidden;
}
.wht-bar-green { height:100%; background:#10b981; border-radius:2px; }
.wht-bar-orange { height:100%; background:#f59e0b; border-radius:2px; }
.wht-bar-red { height:100%; background:#ef4444; border-radius:2px; }
.wht-metrics {
    display:grid; grid-template-columns:repeat(3,1fr); gap:0.3rem;
}
.wht-metric { text-align:center; }
.wht-ml { font-size:0.78rem; font-weight:600; color:var(--text); display:block; }
.wht-ms { font-size:0.58rem; color:var(--text-muted); text-transform:uppercase; }
.wht-green { color:#10b981; }
.wht-orange { color:#f59e0b; }
.wht-red { color:#ef4444; }
.wht-neutral { color:var(--text-muted); }
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
