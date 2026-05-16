# BigWaves Het Weer Pagina — Weerdata & omgevingsinvloeden
import streamlit as st

st.set_page_config(page_title="Het Weer — BigWaves", page_icon="🌤️", layout="wide")

from shared_css import setup_subpage
setup_subpage()

data = st.session_state.data
klant_naam = st.session_state.klant_naam

# Pagina-specifieke extra CSS
st.markdown("""
<style>
.weather-card {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important; padding: 1.2rem !important;
    box-shadow: var(--shadow) !important; margin-bottom: 0.8rem !important;
}
.weather-card .big-temp {
    font-size: 3rem; font-weight: 700; color: var(--text);
    letter-spacing: -0.03em; line-height: 1;
}
.weather-card .label {
    font-size: 0.72rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.3px; font-weight: 500;
}
.weather-stat {
    background: var(--card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important; padding: 0.8rem 1rem !important;
    text-align: center; box-shadow: var(--shadow-sm) !important;
}
.weather-stat .val { font-size: 1.4rem; font-weight: 700; color: var(--text); }
.weather-stat .lbl { font-size: 0.68rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.3px; }
.insight-tag {
    display: inline-block; background: var(--primary-light);
    color: var(--primary); font-size: 0.7rem; font-weight: 600;
    padding: 0.2rem 0.6rem; border-radius: 999px; margin: 0.15rem;
}
@media screen and (max-width: 768px) {
    .weather-card .big-temp { font-size: 2.2rem !important; }
    .weather-stat .val { font-size: 1.1rem !important; }
}
</style>
""", unsafe_allow_html=True)

st.title("🌤️ Het Weer")
st.caption(f"{klant_naam} • Weerdata en omgevingsinvloeden")

# ─── Huidig weer (statisch voor demo) ───────────────────
weer_data = data.get("weer", {})
if not weer_data:
    # Demo data als er nog geen weer veld in de JSON zit
    weer_data = {
        "temperatuur": 18,
        "conditie": "Zonnig",
        "wind": "12 km/h",
        "luchtvochtigheid": "62%",
        "icoon": "☀️",
        "locatie": "Nederland",
        "verwachting": [
            {"dag": "Vandaag", "icoon": "☀️", "temp_hoog": 18, "temp_laag": 10, "conditie": "Zonnig"},
            {"dag": "Morgen", "icoon": "⛅", "temp_hoog": 16, "temp_laag": 9, "conditie": "Half bewolkt"},
            {"dag": "Overmorgen", "icoon": "🌧️", "temp_hoog": 14, "temp_laag": 8, "conditie": "Regenachtig"},
            {"dag": "Woensdag", "icoon": "☁️", "temp_hoog": 15, "temp_laag": 9, "conditie": "Bewolkt"},
            {"dag": "Donderdag", "icoon": "⛅", "temp_hoog": 17, "temp_laag": 10, "conditie": "Half bewolkt"},
        ]
    }

# ─── Huidige weersituatie ──────────────────────────────
icoon = weer_data.get("icoon", "🌤️")
temp = weer_data.get("temperatuur", "--")
conditie = weer_data.get("conditie", "--")
locatie = weer_data.get("locatie", "Nederland")
wind = weer_data.get("wind", "--")
luchtvochtigheid = weer_data.get("luchtvochtigheid", "--")

wc = st.columns([1, 1])
with wc[0]:
    st.markdown(
        f'<div class="weather-card">'
        f'<div style="display:flex;align-items:center;gap:1rem;">'
        f'<span style="font-size:4rem;">{icoon}</span>'
        f'<div>'
        f'<div class="big-temp">{temp}°C</div>'
        f'<div style="font-size:1rem;color:var(--text-sec);font-weight:500;">{conditie}</div>'
        f'<div style="font-size:0.78rem;color:var(--text-muted);">{locatie}</div>'
        f'</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )
with wc[1]:
    ws_cols = st.columns(2)
    with ws_cols[0]:
        st.markdown(
            f'<div class="weather-stat"><div class="lbl">Wind</div>'
            f'<div class="val">{wind}</div></div>',
            unsafe_allow_html=True
        )
    with ws_cols[1]:
        st.markdown(
            f'<div class="weather-stat"><div class="lbl">Luchtvochtigheid</div>'
            f'<div class="val">{luchtvochtigheid}</div></div>',
            unsafe_allow_html=True
        )

# ─── 5-daagse verwachting ───────────────────────────────
verwachting = weer_data.get("verwachting", [])
if verwachting:
    st.markdown('<div class="sec-head">📅 5-daagse verwachting</div>', unsafe_allow_html=True)
    vc = st.columns(len(verwachting))
    for i, dag in enumerate(verwachting):
        with vc[i]:
            st.markdown(
                f'<div class="weather-stat">'
                f'<div class="lbl">{dag.get("dag", "")}</div>'
                f'<div style="font-size:2rem;margin:0.3rem 0;">{dag.get("icoon", "")}</div>'
                f'<div style="font-size:0.85rem;color:var(--text-sec);">{dag.get("conditie", "")}</div>'
                f'<div style="font-size:0.82rem;color:var(--text);font-weight:600;margin-top:2px;">'
                f'{dag.get("temp_hoog", "")}° / {dag.get("temp_laag", "")}°</div>'
                f'</div>',
                unsafe_allow_html=True
            )

# ─── Invloed op bedrijfsprocessen ──────────────────────
st.markdown('<div class="sec-head">🔍 Invloed op processen</div>', unsafe_allow_html=True)
invloed = weer_data.get("invloed_op_processen", {})
if not invloed:
    invloed = {
        "binnenkomst_verkeer": "Normaal",
        "bestellingen_piek": "Geen",
        "opmerking": "Geen bijzondere weersinvloeden deze periode."
    }

cols_inv = st.columns(3)
with cols_inv[0]:
    st.markdown(
        f'<div class="weather-stat"><div class="lbl">Binnenkomst verkeer</div>'
        f'<div class="val" style="font-size:1rem;color:#22c55e;">{invloed.get("binnenkomst_verkeer", "—")}</div></div>',
        unsafe_allow_html=True
    )
with cols_inv[1]:
    st.markdown(
        f'<div class="weather-stat"><div class="lbl">Bestellingen piek</div>'
        f'<div class="val" style="font-size:1rem;color:var(--text-sec);">{invloed.get("bestellingen_piek", "—")}</div></div>',
        unsafe_allow_html=True
    )
with cols_inv[2]:
    st.markdown(
        f'<div class="weather-stat"><div class="lbl">Bijzonderheden</div>'
        f'<div class="val" style="font-size:0.82rem;color:var(--text-sec);">{invloed.get("opmerking", "—")}</div></div>',
        unsafe_allow_html=True
    )

st.markdown('<div class="sec-head">💡 Inzichten</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="weather-card">'
    f'<div style="font-size:0.85rem;color:var(--text-sec);">'
    f'Het weer heeft invloed op bezoekersgedrag en conversie. Bij regenachtig weer zien we vaak een '
    f'daling in fysieke bezoeken maar een stijging in online verkeer. Gebruik deze inzichten om '
    f'je marketing en bezetting aan te passen.'
    f'</div>'
    f'<div style="margin-top:0.8rem;display:flex;gap:0.4rem;flex-wrap:wrap;">'
    f'<span class="insight-tag">☀️ Zonnig = meer conversie</span>'
    f'<span class="insight-tag">🌧️ Regen = meer online</span>'
    f'<span class="insight-tag">❄️ Koud = daling bezoek</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

st.divider()
st.caption("🌊 BigWaves — datagedreven, menselijk gecheckt | www.bigwaves.ai")
