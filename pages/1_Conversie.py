# BigWaves Conversie Pagina — Conversie-overzicht & inzichten
import streamlit as st

st.set_page_config(page_title="Conversie — BigWaves", page_icon="📈", layout="wide")

from shared_css import setup_subpage
setup_subpage()

data = st.session_state.data
klant_naam = st.session_state.klant_naam

# Pagina-specifieke extra CSS
st.markdown("""
<style>
.conv-card {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; padding: 1.2rem !important;
    box-shadow: var(--shadow) !important; margin-bottom: 0.8rem !important;
}
.conv-card .big-number { font-size: 2rem; font-weight: 700; color: var(--text); letter-spacing: -0.02em; }
.conv-card .label { font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.3px; font-weight: 500; }
.conv-metric {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; padding: 0.8rem 1rem !important;
    text-align: center; box-shadow: var(--shadow-sm) !important;
}
.conv-metric .val { font-size: 1.6rem; font-weight: 700; color: var(--text); }
.conv-metric .lbl { font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.4px; }
.conv-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.6rem 0; border-bottom: 1px solid var(--border);
    font-size: 0.85rem;
}
@media screen and (max-width: 768px) {
    .conv-card { padding: 0.8rem !important; }
    .conv-metric .val { font-size: 1.2rem !important; }
}
</style>
""", unsafe_allow_html=True)

st.title("📈 Conversie")
st.caption(f"{klant_naam} • Conversie-overzicht en kanaalprestaties")

# ─── Conversie KPI's uit data ───────────────────────────
kpis = data.get("kpis", {})
kanalen = data.get("kanalen", {})

# Bepaal conversie-gerelateerde KPI's
conversie_kpis = {}
for name, info in kpis.items():
    name_lower = name.lower()
    if any(kw in name_lower for kw in ["conversie", "nauwkeurig", "verwerkt", "respons", "hitl", "kosten"]):
        conversie_kpis[name] = info

# ─── 1. Conversie KPI's in een grid ─────────────────────
if conversie_kpis:
    st.markdown('<div class="sec-head">🎯 Conversie KPI\'s</div>', unsafe_allow_html=True)
    cols = st.columns(min(len(conversie_kpis), 3))
    for i, (name, info) in enumerate(conversie_kpis.items()):
        w = info.get("waarde", 0)
        e = info.get("eenheid", "")
        dsp = f"€{w:,}" if e == "euro" else f"{w}{'s' if e == 'seconden' else '%' if e == '%' else ''}"
        if e not in ("euro", "seconden", "%"):
            dsp = f"{w:,}" if isinstance(w, int) else str(w)
        sts = info.get("status", "groen")
        clr = {"groen": "#22c55e", "oranje": "#f59e0b", "rood": "#ef4444"}.get(sts, "#22c55e")
        with cols[i % len(cols)]:
            st.markdown(
                f'<div class="conv-metric">'
                f'<div class="lbl">{name}</div>'
                f'<div class="val" style="color:{clr};">{dsp}</div>'
                f'<div style="font-size:0.72rem;color:var(--text-muted);">Doel: {info.get("doel", "")} | {info.get("trend", "")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ─── 2. Kanaal per kanaal breakdown ─────────────────────
if kanalen:
    st.markdown('<div class="sec-head">📬 Kanaalprestaties</div>', unsafe_allow_html=True)
    icoon_map = {"website": "🌐", "mail": "📧", "whatsapp": "💬", "telefoon": "📞"}
    for kanaal, info in sorted(kanalen.items()):
        verwerkt = info.get("verwerkt", 0)
        bestellingen = info.get("bestellingen", 0)
        conversie_pct = round(bestellingen / verwerkt * 100, 1) if verwerkt > 0 else 0
        icoon = icoon_map.get(kanaal.lower(), "📨")
        st.markdown(
            f'<div class="conv-card">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;">'
            f'<div><span style="font-size:1.5rem;">{icoon}</span> <strong style="font-size:1rem;color:var(--text);">{kanaal.capitalize()}</strong></div>'
            f'<div style="text-align:right;">'
            f'<span style="font-size:1.2rem;font-weight:700;color:#5273ff;">{conversie_pct}%</span>'
            f'<span style="color:var(--text-muted);font-size:0.72rem;margin-left:4px;">conversie</span>'
            f'</div>'
            f'</div>'
            f'<div class="conv-row"><span>Verwerkt</span><span style="font-weight:600;">{verwerkt:,}</span></div>'
            f'<div class="conv-row"><span>Bestellingen</span><span style="font-weight:600;">{bestellingen:,}</span></div>'
            f'<div class="conv-row" style="border-bottom:none;"><span>Conversieratio</span>'
            f'<span style="font-weight:700;color:#5273ff;">{conversie_pct}%</span></div>'
            f'</div>',
            unsafe_allow_html=True
        )

# ─── 3. Totale conversie ────────────────────────────────
totaal_verwerkt = sum(v.get("verwerkt", 0) for v in kanalen.values())
totaal_bestellingen = sum(v.get("bestellingen", 0) for v in kanalen.values())
totale_conversie = round(totaal_bestellingen / totaal_verwerkt * 100, 1) if totaal_verwerkt > 0 else 0

st.markdown('<div class="sec-head">📊 Totaaloverzicht</div>', unsafe_allow_html=True)
tc = st.columns(3)
with tc[0]:
    st.markdown(
        f'<div class="conv-metric"><div class="lbl">Totaal verwerkt</div>'
        f'<div class="val">{totaal_verwerkt:,}</div></div>',
        unsafe_allow_html=True
    )
with tc[1]:
    st.markdown(
        f'<div class="conv-metric"><div class="lbl">Totaal bestellingen</div>'
        f'<div class="val">{totaal_bestellingen:,}</div></div>',
        unsafe_allow_html=True
    )
with tc[2]:
    st.markdown(
        f'<div class="conv-metric"><div class="lbl">Totale conversie</div>'
        f'<div class="val" style="color:#5273ff;">{totale_conversie}%</div></div>',
        unsafe_allow_html=True
    )

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
