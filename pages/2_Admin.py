# BigWaves Admin Paneel
# Alleen toegankelijk voor BigWaves beheerders
import streamlit as st
import json
from pathlib import Path
from datetime import datetime

ADMIN_USER = "admin"
ADMIN_PASS = "bigwaves2026"
DATA_DIR = Path(__file__).parent / "data"

# Controleer of admin is ingelogd
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Admin login
def admin_login():
    st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
        :root { --bw-surface: #171717; --bw-card: #1a1a1a; --bw-border: #2e2e2e; --bw-text: #fafafa; --bw-text-muted: #898989; --bw-primary: #0A4DA4; }
        .stApp { background: var(--bw-surface) !important; }
        .stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--bw-text) !important; font-weight: 500 !important; }
        .stApp p { color: var(--bw-text-muted) !important; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔐 BigWaves Admin")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-radius:16px; padding:2rem; text-align:center;">
                <h3 style="color:#fafafa; margin-bottom:0.3rem;">🔐 Admin</h3>
                <p style="color:#898989; margin-bottom:2rem;">Alleen voor BigWaves beheerders</p>
            </div>
            """, unsafe_allow_html=True)
            ww = st.text_input("Admin wachtwoord", type="password", placeholder="Voer admin wachtwoord in")
            if st.button("Inloggen", type="primary", use_container_width=True):
                if ww == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Onjuist wachtwoord.")

    # Terug naar dashboard
    st.divider()
    if st.button("← Terug naar dashboard", use_container_width=True):
        st.switch_page("dashboard.py")
    st.stop()

# ─── Admin panel ───────────────────────────────────────────
if not st.session_state.admin_logged_in:
    admin_login()

st.set_page_config(page_title="Admin — BigWaves", page_icon="🔐", layout="wide")

# ─── Styling ───────────────────────────────────────────────
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
    * { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
    :root { --bw-surface: #171717; --bw-card: #1a1a1a; --bw-border: #2e2e2e; --bw-border-light: #363636;
        --bw-text: #fafafa; --bw-text-secondary: #b4b4b4; --bw-text-muted: #898989;
        --bw-primary: #0A4DA4; --bw-accent: #00B4D8; --bw-green: #00C853; --bw-orange: #FF9100; --bw-red: #D50000; }
    .stApp { background: var(--bw-surface) !important; }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--bw-text) !important; font-weight: 500 !important; }
    .stApp p, .stApp li, .stApp span, .stApp label { color: var(--bw-text-secondary) !important; }
    .stApp .st-caption { color: var(--bw-text-muted) !important; }
    .stTextInput input { background: #0f0f0f !important; color: var(--bw-text) !important; border-color: var(--bw-border) !important; }
    .stTextInput input:focus { border-color: var(--bw-primary) !important; }
    .stButton button { border-radius: 9999px !important; font-weight: 500 !important; }
    .stButton button[kind="primary"] { background: var(--bw-primary) !important; border: 1px solid var(--bw-primary) !important; color: white !important; }
    section[data-testid="stSidebar"] { background: #0f0f0f !important; border-right: 1px solid var(--bw-border) !important; }
    hr { border-color: var(--bw-border) !important; }
    #MainMenu {visibility: hidden !important;} footer {visibility: hidden !important;} .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ─── Helper functies ───────────────────────────────────────
def laad_klanten():
    klanten = {}
    if not DATA_DIR.exists():
        return klanten
    for f in sorted(DATA_DIR.glob("*.json")):
        with open(f) as fh:
            data = json.load(fh)
            klanten[data["naam"]] = data
    return klanten

def opslaan_klant(klant_data, bestand_naam=None):
    """Sla klantdata op als JSON in de data directory"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not bestand_naam:
        bestand_naam = klant_data["naam"].lower().replace(" ", "-") + ".json"
    bestand = DATA_DIR / bestand_naam
    with open(bestand, "w") as f:
        json.dump(klant_data, f, indent=2, ensure_ascii=False)
    return bestand_naam

def maak_lege_klant(naam, wachtwoord):
    """Maak een nieuwe klant met standaard structuur"""
    return {
        "naam": naam,
        "wachtwoord": wachtwoord,
        "logo": "🌊",
        "periode": "Huidige maand",
        "laatste_update": datetime.now().strftime("%Y-%m-%d"),
        "kpis": {
            "Verwerkte items": {"waarde": 0, "doel": 0, "eenheid": "items", "trend": "Nieuw", "status": "groen"},
            "Uptime": {"waarde": 99.9, "doel": 99.0, "eenheid": "%", "trend": "Nieuw", "status": "groen"},
            "Gem. responstijd": {"waarde": 2.0, "doel": 3.0, "eenheid": "seconden", "trend": "Nieuw", "status": "groen"},
            "HITL-ratio": {"waarde": 15, "doel": 20, "eenheid": "%", "trend": "Nieuw", "status": "groen"},
            "Nauwkeurigheid": {"waarde": 95, "doel": 95, "eenheid": "%", "trend": "Nieuw", "status": "groen"},
            "Kostenbesparing": {"waarde": 0, "doel": 0, "eenheid": "euro", "trend": "Nieuw", "status": "groen"},
        },
        "kosten_besparing": 0,
        "doelen_vorige_maand": {"kosten_besparing": 0},
        "grafieken": {},
        "bottleneck": {"prioriteit": "laag", "tekst": "Nieuwe klant — nog geen data beschikbaar."},
        "hitl_detail": {
            "totaal_acties": 0,
            "menselijke_check": 0,
            "geautomatiseerd": 0,
            "bespaarde_uren": 0,
            "categorieen": {}
        }
    }

# ─── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔐 Admin Paneel")
    st.caption("BigWaves beheeromgeving")
    st.divider()
    st.page_link("pages/2_Admin.py", label="📋  Klanten beheren", use_container_width=True)
    st.divider()
    if st.button("← Naar dashboard", use_container_width=True):
        if "ingelogd" in st.session_state:
            del st.session_state.ingelogd
        st.switch_page("dashboard.py")
    if st.button("🚪 Uitloggen (admin)", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

# ─── Hoofdpagina ───────────────────────────────────────────
st.title("📋 Klanten beheren")
st.caption(f"BigWaves AI-bureau • {len(laad_klanten())} klant(en)")

klanten = laad_klanten()

# ─── Nieuwe klant toevoegen ────────────────────────────────
with st.expander("➕ Nieuwe klant toevoegen", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        nieuwe_naam = st.text_input("Klantnaam", placeholder="Bijv. 'Bouwbedrijf X'")
        nieuw_ww = st.text_input("Wachtwoord", type="password", placeholder="Kies een wachtwoord")
    with col2:
        nieuw_logo = st.text_input("Logo (emoji)", value="🌊", placeholder="🌊")
        nieuwe_periode = st.text_input("Periode", value="Huidige maand")

    if st.button("✅ Klant aanmaken", type="primary", use_container_width=True):
        if nieuwe_naam and nieuw_ww:
            if nieuwe_naam in klanten:
                st.error(f"Klant '{nieuwe_naam}' bestaat al!")
            else:
                klant = maak_lege_klant(nieuwe_naam, nieuw_ww)
                klant["logo"] = nieuw_logo
                klant["periode"] = nieuwe_periode
                bestand = opslaan_klant(klant)
                st.success(f"✅ Klant '{nieuwe_naam}' aangemaakt als `{bestand}`")
                st.rerun()
        else:
            st.warning("Vul zowel een naam als wachtwoord in.")

st.divider()

# ─── Klantenoverzicht ──────────────────────────────────────
if not klanten:
    st.info("Nog geen klanten. Maak er een aan via de knop hierboven.")
    st.stop()

for klant_naam in sorted(klanten.keys()):
    data = klanten[klant_naam]
    with st.container():
        st.markdown(f"""
        <div style="background:#1a1a1a; border:1px solid #2e2e2e; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="color:#fafafa; font-size:1.1rem;">{data.get('logo','🌊')} {klant_naam}</strong>
                    <span style="color:#898989; font-size:0.8rem; margin-left:1rem;">wachtwoord: {data.get('wachtwoord','—')}</span>
                </div>
                <div>
                    <span style="color:#b4b4b4; font-size:0.8rem;">{data.get('periode','')}</span>
                    <span style="color:#898989; font-size:0.8rem; margin-left:1rem;">update: {data.get('laatste_update','—')}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # KPI-overzichtje in de kaart
        kpis = data.get("kpis", {})
        if kpis:
            kpi_cols = st.columns(len(kpis))
            for i, (kpi_name, info) in enumerate(kpis.items()):
                with kpi_cols[i]:
                    st.markdown(f"""
                    <div style="text-align:center; padding:0.3rem;">
                        <div style="color:#898989; font-size:0.65rem; text-transform:uppercase;">{kpi_name[:12]}</div>
                        <div style="color:#fafafa; font-size:1rem; font-weight:600;">{info['waarde']}{'%' if info.get('eenheid')=='%' else ''}</div>
                        <div style="color:#898989; font-size:0.6rem;">doel: {info['doel']}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Bewerken knop
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button(f"✏️ Bewerken", key=f"edit_{klant_naam}", use_container_width=True):
                st.session_state.edit_klant = klant_naam
                st.rerun()
        with col2:
            if st.button(f"🗑️ Verwijderen", key=f"del_{klant_naam}", use_container_width=True):
                bestand = DATA_DIR / f"{klant_naam.lower().replace(' ', '-')}.json"
                if bestand.exists():
                    bestand.unlink()
                    st.success(f"Klant '{klant_naam}' verwijderd.")
                    st.rerun()

    st.divider()

# ─── Klant bewerken (modal-style) ──────────────────────────
if "edit_klant" in st.session_state and st.session_state.edit_klant in klanten:
    k = st.session_state.edit_klant
    data = klanten[k]

    st.markdown(f"## ✏️ Bewerken: {data.get('logo','🌊')} {k}")

    with st.form(key=f"form_{k}"):
        # Basis instellingen
        col1, col2 = st.columns(2)
        with col1:
            nieuwe_wachtwoord = st.text_input("Wachtwoord", value=data.get("wachtwoord", ""))
        with col2:
            nieuwe_periode = st.text_input("Periode", value=data.get("periode", ""))

        st.markdown("**KPI-waarden**")
        kpi_cols = st.columns(3)
        kpi_keys = list(data.get("kpis", {}).keys())
        nieuwe_kpis = {}
        for i, kpi_name in enumerate(kpi_keys):
            info = data["kpis"][kpi_name]
            with kpi_cols[i % 3]:
                waarde = st.number_input(f"{kpi_name} — waarde", value=float(info["waarde"]) if isinstance(info["waarde"], (int, float)) else 0.0, key=f"w_{k}_{kpi_name}", format="%f")
                doel = st.number_input(f"Doel", value=float(info["doel"]) if isinstance(info["doel"], (int, float)) else 0.0, key=f"d_{k}_{kpi_name}", format="%f")
                trend = st.text_input(f"Trend", value=info.get("trend", ""), key=f"t_{k}_{kpi_name}")
                nieuwe_kpis[kpi_name] = {
                    "waarde": int(waarde) if info.get("eenheid") in ["items", "euro"] else round(waarde, 1),
                    "doel": int(doel) if info.get("eenheid") in ["items", "euro"] else round(doel, 1),
                    "eenheid": info.get("eenheid", ""),
                    "trend": trend,
                    "status": "groen"  # auto
                }

        # Kostenbesparing
        st.markdown("**Kostenbesparing**")
        col1, col2 = st.columns(2)
        with col1:
            kosten = st.number_input("Kostenbesparing (€)", value=float(data.get("kosten_besparing", 0)), key=f"kosten_{k}")
        with col2:
            vorige_kosten = st.number_input("Vorige maand (€)", value=float(data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)), key=f"vkosten_{k}")

        # Bottleneck
        st.markdown("**Bottleneck**")
        bottleneck = data.get("bottleneck", {})
        bottleneck_tekst = st.text_area("Bottleneck tekst", value=bottleneck.get("tekst", ""), key=f"bn_{k}")

        # Opslaan
        if st.form_submit_button("💾 Opslaan", type="primary", use_container_width=True):
            data["wachtwoord"] = nieuwe_wachtwoord
            data["periode"] = nieuwe_periode
            data["kpis"] = nieuwe_kpis
            data["kosten_besparing"] = int(kosten)
            data["doelen_vorige_maand"] = {"kosten_besparing": int(vorige_kosten)}
            data["bottleneck"] = {"prioriteit": "laag", "tekst": bottleneck_tekst}
            data["laatste_update"] = datetime.now().strftime("%Y-%m-%d")

            opslaan_klant(data)
            st.success(f"✅ Klant '{k}' bijgewerkt!")
            del st.session_state.edit_klant
            st.rerun()

    if st.button("❌ Annuleren"):
        del st.session_state.edit_klant
        st.rerun()
