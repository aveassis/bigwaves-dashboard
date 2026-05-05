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
    st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
:root { --bg:#0f1117; --surface:#1a1d27; --card:#1e2231; --border:#2a2e3d; --text:#edf2f7; --text-sec:#94a3b8; --text-muted:#64748b; --primary:#10b981; }
.stApp { background: var(--bg) !important; }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--text) !important; font-weight: 600 !important; }
.stApp p { color: var(--text-sec) !important; }
.stButton button { border-radius: 10px !important; font-weight: 500 !important; }
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; color: #fff !important; }
.stTextInput input { background: var(--surface) !important; color: var(--text) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
.stTextInput input:focus { border-color: var(--primary) !important; }
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
st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { font-family: 'Inter', system-ui, -apple-system, sans-serif !important; }
:root { --bg:#0f1117; --surface:#1a1d27; --card:#1e2231; --border:#2a2e3d; --border-light:#363b4d; --text:#edf2f7; --text-sec:#94a3b8; --text-muted:#64748b; --primary:#10b981; --primary-light:rgba(16,185,129,0.1); --shadow:0 2px 8px rgba(0,0,0,0.2); --radius:14px; --radius-sm:10px; }
.stApp { background: var(--bg) !important; }
.stApp h1 { font-size: 1.4rem !important; font-weight: 700 !important; color: var(--text) !important; }
.stApp h2 { font-size: 1.1rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp h3 { font-size: 0.95rem !important; font-weight: 600 !important; color: var(--text) !important; }
.stApp p, .stApp li, .stApp span, .stApp label { color: var(--text-sec) !important; font-size: 0.82rem !important; }
.stApp .st-caption { color: var(--text-muted) !important; font-size: 0.72rem !important; }
.stTextInput input { background: var(--surface) !important; color: var(--text) !important; border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important; }
.stTextInput input:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 3px var(--primary-light) !important; }
.stButton button { border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; color: #fff !important; }
.stButton button[kind="primary"]:hover { background: #059669 !important; }
section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--border) !important; }
.stApp hr { border-color: var(--border) !important; }
.stApp .st-bq { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; }
.stApp .stAlert { background: var(--card) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }

/* Admin cards */
.admin-card { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; padding: 1.2rem !important; box-shadow: var(--shadow) !important; margin-bottom: 1rem !important; }
.admin-card strong { color: var(--text) !important; }
.admin-kpi { text-align: center; padding: 0.3rem; }
.admin-kpi .lbl { color: var(--text-muted); font-size: 0.65rem; text-transform: uppercase; }
.admin-kpi .val { color: var(--text); font-size: 1rem; font-weight: 600; }
.admin-kpi .tgt { color: var(--text-muted); font-size: 0.6rem; }
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
    from datetime import datetime
    return {
        "naam": naam,
        "wachtwoord": wachtwoord,
        "logo": "🌊",
        "periodes": {
            "Huidige maand": {
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
                "hitl_detail": {"totaal_acties": 0, "menselijke_check": 0, "geautomatiseerd": 0, "bespaarde_uren": 0, "categorieen": {}}
            }
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
        st.markdown(f"""<div class="admin-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="color:var(--text); font-size:1.05rem;">{data.get('logo','🌊')} {klant_naam}</strong>
                    <span style="color:var(--text-muted); font-size:0.78rem; margin-left:1rem;">wachtwoord: {data.get('wachtwoord','—')}</span>
                </div>
                <div>
                    <span style="color:var(--text-sec); font-size:0.78rem;">{data.get('periode','')}</span>
                    <span style="color:var(--text-muted); font-size:0.78rem; margin-left:1rem;">update: {data.get('laatste_update','—')}</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # KPI-overzichtje in de kaart
        kpis = data.get("kpis", {})
        if kpis:
            kpi_cols = st.columns(len(kpis))
            for i, (kpi_name, info) in enumerate(kpis.items()):
                with kpi_cols[i]:
                    st.markdown(f"""<div class="admin-kpi">
                        <div class="lbl">{kpi_name[:12]}</div>
                        <div class="val">{info['waarde']}{'%' if info.get('eenheid')=='%' else ''}</div>
                        <div class="tgt">doel: {info['doel']}</div>
                    </div>""", unsafe_allow_html=True)

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
    st.caption("Vul de gegevens in en klik op Opslaan. Trend is een tekst zoals '+8% vs vorige maand' of 'Gelijk'.")

    with st.form(key=f"form_{k}"):
        # Basis instellingen
        st.markdown("**Basis**")
        col1, col2 = st.columns(2)
        with col1:
            nieuwe_wachtwoord = st.text_input("Inlog wachtwoord voor klant", value=data.get("wachtwoord", ""),
                help="De klant gebruikt dit wachtwoord om in te loggen op het dashboard")
        with col2:
            nieuwe_periode = st.text_input("Periode (bv. 'Mei 2026')", value=data.get("periode", ""))

        st.markdown("**Prestatie KPI's**")
        st.caption("Vul bij elke KPI de huidige waarde, het streefdoel en een trend-omschrijving in.")

        kpi_cols = st.columns(3)
        kpi_keys = list(data.get("kpis", {}).keys())
        nieuwe_kpis = {}
        for i, kpi_name in enumerate(kpi_keys):
            info = data["kpis"][kpi_name]
            eenheid = info.get("eenheid", "")
            eenheid_label = {"items": "aantal", "euro": "euro (€)", "%": "procent", "seconden": "seconden"}.get(eenheid, eenheid)

            with kpi_cols[i % 3]:
                st.markdown(f"**{kpi_name}** ({eenheid_label})")

                huidige = info["waarde"]
                if isinstance(huidige, (int, float)):
                    standaard_waarde = float(huidige)
                else:
                    standaard_waarde = 0.0

                stap_grootte = 1.0 if eenheid in ["items", "euro"] else 0.1
                nieuwe_waarde = st.number_input(
                    f"Huidige waarde",
                    value=standaard_waarde,
                    step=stap_grootte,
                    format="%.0f" if eenheid in ["items", "euro"] else "%.1f",
                    key=f"w_{k}_{kpi_name}",
                    help=f"Wat is de actuele prestatie? (in {eenheid_label})"
                )

                doel = info["doel"]
                if isinstance(doel, (int, float)):
                    standaard_doel = float(doel)
                else:
                    standaard_doel = 0.0

                nieuw_doel = st.number_input(
                    f"Doel / streefwaarde",
                    value=standaard_doel,
                    step=stap_grootte,
                    format="%.0f" if eenheid in ["items", "euro"] else "%.1f",
                    key=f"d_{k}_{kpi_name}",
                    help=f"Wat is de target? (in {eenheid_label})"
                )

                trend = st.text_input(
                    f"Trend (bv. '+5% vs vorige maand')",
                    value=info.get("trend", ""),
                    key=f"t_{k}_{kpi_name}",
                    help="Bijv. '+8.3% vs vorige maand', '-0.4s', 'Gelijk', of leeg laten"
                )

                nieuwe_kpis[kpi_name] = {
                    "waarde": int(nieuwe_waarde) if eenheid in ["items", "euro"] else round(nieuwe_waarde, 1),
                    "doel": int(nieuw_doel) if eenheid in ["items", "euro"] else round(nieuw_doel, 1),
                    "eenheid": eenheid,
                    "trend": trend,
                    "status": "groen"
                }

        # Kostenbesparing
        st.markdown("**💰 Kostenbesparing**")
        st.caption("Hoeveel euro bespaart de klant deze maand door AI-automatisering?")
        col1, col2 = st.columns(2)
        with col1:
            kosten = st.number_input(
                "Kostenbesparing deze maand (€)",
                value=float(data.get("kosten_besparing", 0)),
                step=100.0,
                format="%.0f",
                key=f"kosten_{k}",
                help="Totaal bedrag dat de klant deze maand heeft bespaard"
            )
        with col2:
            vorige_kosten = st.number_input(
                "Vorige maand (€)",
                value=float(data.get("doelen_vorige_maand", {}).get("kosten_besparing", 0)),
                step=100.0,
                format="%.0f",
                key=f"vkosten_{k}",
                help="Vergelijkingsbedrag van vorige maand (toont + of - verschil)"
            )

        # Bottleneck
        st.markdown("**⚠️ Bottleneck / Knelpunt**")
        st.caption("Zijn er problemen of aandachtspunten deze periode?")
        bottleneck = data.get("bottleneck", {})
        bottleneck_tekst = st.text_area(
            "Beschrijving (of leeg laten als alles goed gaat)",
            value=bottleneck.get("tekst", ""),
            key=f"bn_{k}",
            help="Bijv. 'Servercapaciteit moet worden uitgebreid' of 'Geen knelpunten deze week'"
        )

        # Opslaan
        st.divider()
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
