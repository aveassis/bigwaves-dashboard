# groei_team_ui.py — GroeiTeam UI componenten voor Streamlit dashboard
import streamlit as st
from datetime import datetime, date
import json

def render_health_ring(score: int) -> str:
    """Genereer HTML voor een SVG health ring (donut chart)."""
    pct = min(score, 100)
    kleur = "#10b981" if pct >= 80 else "#f59e0b" if pct >= 60 else "#ef4444"
    straal = 36
    omtrek = 2 * 3.14159 * straal
    offset = omtrek - (pct / 100) * omtrek
    return f"""
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
        <svg width="90" height="90" viewBox="0 0 90 90">
            <circle cx="45" cy="45" r="{straal}" fill="none" stroke="#2a2e3d" stroke-width="6"/>
            <circle cx="45" cy="45" r="{straal}" fill="none" stroke="{kleur}" stroke-width="6"
                stroke-dasharray="{omtrek}" stroke-dashoffset="{offset}"
                stroke-linecap="round" transform="rotate(-90 45 45)"
                style="transition: stroke-dashoffset 0.5s ease;"/>
            <text x="45" y="45" text-anchor="middle" dominant-baseline="central"
                fill="#edf2f7" font-size="20" font-weight="700">{pct}%</text>
        </svg>
        <span style="color:#94a3b8;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.4px;">Health</span>
    </div>
    """

def render_pakket_badge(pakket: str) -> str:
    """Genereer HTML voor een pakket badge."""
    kleuren = {
        "Pilot": "#8b5cf6",
        "Start": "#3b82f6",
        "Groei": "#f59e0b",
        "Pro": "#10b981"
    }
    k = kleuren.get(pakket, "#64748b")
    return f'<span style="background:{k}20;color:{k};border:1px solid {k}40;border-radius:6px;padding:2px 10px;font-size:0.75rem;font-weight:600;">{pakket}</span>'


def render_workflow_card(wf: dict) -> str:
    """Genereer HTML voor een workflow card."""
    kleur_map = {"groen": "#10b981", "oranje": "#f59e0b", "rood": "#ef4444"}
    s_kleur = kleur_map.get(wf.get("status", "groen"), "#10b981")
    icoon = "🎯" if wf.get("type") == "lead" else "👤"
    return f"""
    <div class="wf-card">
        <div class="wf-header">
            <span class="wf-icon">{icoon}</span>
            <span class="wf-name">{wf['naam']}</span>
            <span class="wf-status-dot" style="background:{s_kleur};"></span>
        </div>
        <div class="wf-stats">
            <span class="wf-stat"><span class="wf-stat-val">{wf.get('items_verwerkt',0)}</span> verwerkt</span>
            <span class="wf-stat"><span class="wf-stat-val">{wf.get('opvolgmomenten',0)}</span> stappen</span>
        </div>
        <div class="wf-footer">
            <span class="wf-type-label">{wf.get('type','onbekend').capitalize()}</span>
            <span class="wf-date">Laatste: {wf.get('laatste_actie','—')}</span>
        </div>
    </div>
    """


def render_hitl_samenvatting(hitl: dict) -> str:
    """Genereer HTML voor HITL samenvatting."""
    totaal = hitl.get("deze_maand_goedgekeurd", 0) + hitl.get("deze_maand_geweigerd", 0)
    goedk_pct = round(hitl.get("deze_maand_goedgekeurd", 0) / totaal * 100, 1) if totaal > 0 else 0
    return f"""
    <div class="hitl-summary">
        <div class="hitl-row">
            <span>✅ Goedgekeurd</span>
            <span class="hitl-val">{hitl.get('deze_maand_goedgekeurd',0)}</span>
        </div>
        <div class="hitl-row">
            <span>❌ Geweigerd</span>
            <span class="hitl-val">{hitl.get('deze_maand_geweigerd',0)}</span>
        </div>
        <div class="hitl-row">
            <span>⏱ Gem. wachttijd</span>
            <span class="hitl-val">{hitl.get('wachttijd_gemiddeld','—')}</span>
        </div>
        <div class="hitl-row hitl-row-total">
            <span>Goedkeuringsratio</span>
            <span class="hitl-val">{goedk_pct}%</span>
        </div>
    </div>
    """


def bereken_health_score(data: dict) -> int:
    """Bereken health score uit KPI data en workflow status."""
    score = 80  # startpunt

    gt = data.get("groei_team", {})

    # Check workflow statussen
    for wf in gt.get("workflows", []):
        if wf.get("status") == "rood":
            score -= 15
        elif wf.get("status") == "oranje":
            score -= 8

    # Check bottlenecks in huidige periode
    periodes = data.get("periodes", {})
    if periodes:
        huidige = list(periodes.keys())[-1] if periodes else None
        if huidige and periodes[huidige].get("bottleneck", {}).get("prioriteit") in ["hoog", "medium"]:
            score -= 10

    # Recente check-in (binnen 7 dagen = bonus)
    laatste = gt.get("laatste_checkin", "")
    if laatste:
        try:
            dagen = (date.today() - datetime.strptime(laatste, "%Y-%m-%d").date()).days
            if dagen <= 7:
                score += 5
            elif dagen > 14:
                score -= 5
        except Exception:
            pass

    # Check KPI statussen
    if periodes:
        huidige = list(periodes.keys())[-1] if periodes else None
        if huidige:
            for kpi, info in periodes[huidige].get("kpis", {}).items():
                if info.get("status") == "rood":
                    score -= 10
                elif info.get("status") == "oranje":
                    score -= 5

    return max(0, min(100, score))


# CSS voor GroeiTeam componenten
GROEI_TEAM_CSS = """
<style>
.wf-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    transition: all 0.2s ease;
}
.wf-card:hover { border-color: var(--border-light); transform: translateY(-1px); }
.wf-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.wf-icon { font-size: 1.1rem; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; background: rgba(16,185,129,0.1); border-radius: 8px; }
.wf-name { font-size: 0.85rem; font-weight: 600; color: var(--text); flex: 1; }
.wf-status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.wf-stats { display: flex; gap: 16px; margin-bottom: 4px; }
.wf-stat { font-size: 0.72rem; color: var(--text-sec); }
.wf-stat-val { font-weight: 700; color: var(--text); }
.wf-footer { display: flex; justify-content: space-between; font-size: 0.68rem; }
.wf-type-label { color: var(--primary); font-weight: 500; }
.wf-date { color: var(--text-muted); }

.hitl-summary { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 0.8rem 1rem; }
.hitl-row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 0.78rem; color: var(--text-sec); }
.hitl-val { font-weight: 600; color: var(--text); }
.hitl-row-total { border-top: 1px solid var(--border); margin-top: 4px; padding-top: 8px; font-weight: 500; }

.gt-section-title { font-size: 0.85rem; font-weight: 600; color: var(--text); margin: 1rem 0 0.6rem 0; display: flex; align-items: center; gap: 6px; }
.gt-divider { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

.checkin-item { display: flex; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--border); }
.checkin-item:last-child { border-bottom: none; }
.checkin-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 4px; flex-shrink: 0; }
.checkin-date { font-size: 0.72rem; color: var(--text-muted); }
.checkin-text { font-size: 0.78rem; color: var(--text-sec); }

.gt-pakket-header { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.gt-pakket-naam { font-size: 1.2rem; font-weight: 700; color: var(--text); }
.gt-status-actief { font-size: 0.78rem; color: #10b981; }
.gt-status-inactief { font-size: 0.78rem; color: #ef4444; }
</style>
"""
