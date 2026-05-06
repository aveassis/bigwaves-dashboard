# BigWaves Admin Paneel — JSON Wizard
import streamlit as st
import json
from pathlib import Path
from datetime import datetime

ADMIN_PASS = "bigwaves2026"
DATA_DIR = Path(__file__).parent.parent / "data"

# ─── Helpers ───────────────────────────────────────────────
def laad_klanten():
    kl = {}
    if DATA_DIR.exists():
        for f in sorted(DATA_DIR.glob("*.json")):
            with open(f) as fh: d = json.load(fh); kl[d["naam"]] = (d, f.name)
    return kl

def opslaan_klant(data, bestand_naam=None):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not bestand_naam:
        bestand_naam = data["naam"].lower().replace(" ", "-") + ".json"
    with open(DATA_DIR / bestand_naam, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return bestand_naam

def lege_periode():
    return {
        "laatste_update": datetime.now().strftime("%Y-%m-%d"),
        "kpis": {},
        "kosten_besparing": 0,
        "doelen_vorige_maand": {"kosten_besparing": 0},
        "grafieken": {},
        "bottleneck": {"tekst": "Geen knelpunten.", "prioriteit": "laag"},
        "hitl_detail": {"totaal_acties": 0, "menselijke_check": 0, "geautomatiseerd": 0, "bespaarde_uren": 0, "categorieen": {}}
    }

def lege_klant(naam, ww):
    return {
        "naam": naam, "wachtwoord": ww, "logo": "🌊", "accent_kleur": "#10b981",
        "periodes": {"Huidige maand": lege_periode()}
    }

# ─── Admin CSS ─────────────────────────────────────────────
def admin_styling():
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
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { background: var(--surface) !important; color: var(--text) !important; border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--primary) !important; box-shadow: 0 0 0 3px var(--primary-light) !important; }
.stButton button { border-radius: var(--radius-sm) !important; font-weight: 500 !important; }
.stButton button[kind="primary"] { background: var(--primary) !important; border: 1px solid var(--primary) !important; color: #fff !important; }
.stButton button[kind="primary"]:hover { background: #059669 !important; }
.stApp hr { border-color: var(--border) !important; }
.stApp .stAlert { background: var(--card) !important; border: 1px solid var(--border) !important; color: var(--text) !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
.admin-card { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; padding: 1.2rem !important; box-shadow: var(--shadow) !important; margin-bottom: 0.8rem !important; }
.admin-card strong { color: var(--text) !important; }
.admin-sectie { font-size:0.9rem; font-weight:600; color:var(--text); margin:1rem 0 0.5rem 0; }
.admin-label { color: var(--text-muted); font-size:0.68rem; text-transform:uppercase; letter-spacing:0.3px; margin-bottom:0.2rem; }
</style>""", unsafe_allow_html=True)

# ─── Login ─────────────────────────────────────────────────
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.set_page_config(page_title="Admin — BigWaves", page_icon="🔐")
    admin_styling()
    st.title("🔐 BigWaves Admin")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        ww = st.text_input("Admin wachtwoord", type="password", placeholder="Voer admin wachtwoord in")
        if st.button("Inloggen", type="primary", use_container_width=True):
            if ww == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Onjuist wachtwoord.")
    st.stop()

st.set_page_config(page_title="Admin — BigWaves", page_icon="🔐", layout="wide")
admin_styling()

# ─── Session state init ────────────────────────────────────
if "admin_tab" not in st.session_state:
    st.session_state.admin_tab = "overzicht"

# ─── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔐 Admin Paneel")
    st.caption("BigWaves beheeromgeving")
    st.divider()
    tabs = ["📋 Overzicht", "✏️ Bewerken", "➕ Nieuwe klant", "📦 JSON Editor"]
    for t in tabs:
        if st.button(t, use_container_width=True, key=f"tab_{t}"):
            st.session_state.admin_tab = t
            st.rerun()
    st.divider()
    if st.button("← Dashboard", use_container_width=True):
        st.switch_page("dashboard.py")
    if st.button("🚪 Uitloggen", use_container_width=True):
        for k in ["admin_logged_in", "edit_klant", "admin_tab"]:
            st.session_state.pop(k, None)
        st.rerun()

# ─── Tab routing ───────────────────────────────────────────
tab = st.session_state.admin_tab
klanten = laad_klanten()

if tab == "📋 Overzicht":
    st.title("📋 Klantenoverzicht")
    st.caption(f"{len(klanten)} klant(en) geregistreerd")
    if not klanten:
        st.info("Nog geen klanten.")
        st.stop()
    for nm, (data, fn) in klanten.items():
        periodes = list(data.get("periodes", {}).keys())
        kpi_count = sum(len(p.get("kpis", {})) for p in data.get("periodes", {}).values())
        with st.container():
            st.markdown(f"""<div class="admin-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div><strong>{data.get('logo','🌊')} {nm}</strong>
                        <span style="color:var(--text-muted);font-size:0.78rem;margin-left:1rem;">{len(periodes)} periode(s)</span>
                        <span style="color:var(--text-muted);font-size:0.78rem;margin-left:0.5rem;">{kpi_count} KPI's</span>
                    </div>
                    <div style="display:flex;gap:0.5rem;">
                        <span style="color:var(--text-muted);font-size:0.7rem;">{fn}</span>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            if st.button("✏️ Bewerken", key=f"ov_edit_{nm}"):
                st.session_state.edit_klant = nm
                st.session_state.admin_tab = "✏️ Bewerken"
                st.rerun()
        with c2:
            if st.button("📦 JSON", key=f"ov_json_{nm}"):
                st.session_state.edit_klant = nm
                st.session_state.admin_tab = "📦 JSON Editor"
                st.rerun()
        with c3:
            if st.button("🗑️ Verwijderen", key=f"ov_del_{nm}"):
                (DATA_DIR / fn).unlink()
                st.success(f"'{nm}' verwijderd.")
                st.rerun()
        st.divider()

elif tab == "➕ Nieuwe klant":
    st.title("➕ Nieuwe klant aanmaken")
    c1, c2 = st.columns(2)
    with c1:
        nm = st.text_input("Klantnaam", placeholder="Bijv. 'Bouwbedrijf X'")
        ww = st.text_input("Wachtwoord", type="password", placeholder="Kies wachtwoord")
    with c2:
        logo = st.text_input("Logo (emoji)", value="🌊")
        accent = st.color_picker("Accentkleur", value="#10b981")
    if st.button("✅ Aanmaken", type="primary", use_container_width=True):
        if nm and ww:
            if nm in klanten:
                st.error(f"Klant '{nm}' bestaat al!")
            else:
                k = lege_klant(nm, ww)
                k["logo"] = logo
                k["accent_kleur"] = accent
                opslaan_klant(k)
                st.success(f"✅ '{nm}' aangemaakt!")
                st.rerun()
        else:
            st.warning("Vul naam en wachtwoord in.")

elif tab == "✏️ Bewerken":
    if "edit_klant" not in st.session_state or st.session_state.edit_klant not in klanten:
        st.info("Selecteer een klant om te bewerken via het overzicht.")
        st.stop()
    nm = st.session_state.edit_klant
    data, fn = klanten[nm]
    periodes = data.setdefault("periodes", {"Huidige maand": lege_periode()})
    periode_namen = list(periodes.keys())

    st.title(f"✏️ {data.get('logo','🌊')} {nm}")
    st.caption(f"Bestand: {fn}")

    # ─── Basis instellingen ────────────────────────────────
    with st.expander("⚙️ Basis instellingen", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1: data["logo"] = st.text_input("Logo", value=data.get("logo","🌊"), key="b_logo")
        with c2: data["wachtwoord"] = st.text_input("Wachtwoord", value=data.get("wachtwoord",""), key="b_ww")
        with c3: data["accent_kleur"] = st.color_picker("Accentkleur", value=data.get("accent_kleur","#10b981"), key="b_accent")
        with c4: st.markdown("<br>", unsafe_allow_html=True); st.caption(f"Update: {data.get('laatste_update','—')}")

    # ─── Periode selector ──────────────────────────────────
    st.markdown('<div class="admin-sectie">📅 Periodes</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        if periode_namen:
            gekozen_periode = st.selectbox("Selecteer periode om te bewerken", periode_namen,
                key="periode_selector_edit")
        else:
            st.warning("Geen periodes. Voeg er een toe.")
            gekozen_periode = None
    with c2:
        nieuwe_pn = st.text_input("Nieuwe periode naam", placeholder="Mei 2026", key="nieuwe_periode_input", label_visibility="collapsed")
        if st.button("➕ Toevoegen", use_container_width=True) and nieuwe_pn:
            if nieuwe_pn not in periodes:
                periodes[nieuwe_pn] = lege_periode()
                st.success(f"Periode '{nieuwe_pn}' toegevoegd!")
                st.rerun()
    with c3:
        if gekozen_periode and st.button("🗑️ Verwijder", use_container_width=True, key="del_periode"):
            if len(periodes) > 1:
                del periodes[gekozen_periode]
                st.rerun()
            else:
                st.error("Minimaal 1 periode nodig.")

    if not gekozen_periode:
        st.stop()

    pd = periodes[gekozen_periode]
    pd.setdefault("laatste_update", datetime.now().strftime("%Y-%m-%d"))
    pd.setdefault("kpis", {})
    pd.setdefault("grafieken", {})
    pd.setdefault("bottleneck", {"tekst": "", "prioriteit": "laag"})
    pd.setdefault("hitl_detail", {"totaal_acties": 0, "menselijke_check": 0, "geautomatiseerd": 0, "bespaarde_uren": 0, "categorieen": {}})
    pd.setdefault("kosten_besparing", 0)
    pd.setdefault("doelen_vorige_maand", {"kosten_besparing": 0})

    st.markdown(f'<div class="admin-sectie">📊 KPI\'s — {gekozen_periode}</div>', unsafe_allow_html=True)
    st.caption("Elke KPI heeft: waarde, doel, eenheid, trend, status, uitleg (optioneel).")

    kpi_namen = list(pd["kpis"].keys())

    # Bestaande KPI's
    for kpi_name in list(kpi_namen):
        info = pd["kpis"][kpi_name]
        st.markdown(f"""<div class="admin-card" style="padding:0.8rem 1rem;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <strong style="font-size:0.9rem;">{kpi_name}</strong>
                <span style="color:var(--text-muted);font-size:0.7rem;">{info.get('eenheid','')}</span>
            </div></div>""", unsafe_allow_html=True)
        cols = st.columns([1, 1, 1, 1, 1, 3, 1, 1])
        with cols[0]:
            info["waarde"] = st.number_input("Waarde", value=float(info.get("waarde",0)), key=f"kw_{nm}_{kpi_name}", label_visibility="collapsed", placeholder="Waarde")
        with cols[1]:
            info["doel"] = st.number_input("Doel", value=float(info.get("doel",0)), key=f"kd_{nm}_{kpi_name}", label_visibility="collapsed", placeholder="Doel")
        with cols[2]:
            info["eenheid"] = st.selectbox("Eenheid", ["items","%","euro","seconden","minuten","uren","aantal"], index=["items","%","euro","seconden","minuten","uren","aantal"].index(info.get("eenheid","items")), key=f"ke_{nm}_{kpi_name}", label_visibility="collapsed")
        with cols[3]:
            info["status"] = st.selectbox("Status", ["groen","oranje","rood"], index=["groen","oranje","rood"].index(info.get("status","groen")), key=f"ks_{nm}_{kpi_name}", label_visibility="collapsed")
        with cols[4]:
            info["trend"] = st.text_input("Trend", value=info.get("trend",""), key=f"kt_{nm}_{kpi_name}", label_visibility="collapsed", placeholder="+8% vs vorige maand")
        with cols[5]:
            info["uitleg"] = st.text_input("Uitleg", value=info.get("uitleg",""), key=f"ku_{nm}_{kpi_name}", label_visibility="collapsed", placeholder="Wat betekent deze KPI voor de klant?")
        with cols[6]:
            info.setdefault("drempel_oranje", 10)
            info["drempel_oranje"] = st.number_input("⚠️ Drempel %", value=float(info["drempel_oranje"]), key=f"kdor_{nm}_{kpi_name}", label_visibility="collapsed", placeholder="Oranje %")
        with cols[7]:
            info.setdefault("drempel_rood", 25)
            info["drempel_rood"] = st.number_input("🔴 Drempel %", value=float(info["drempel_rood"]), key=f"kdrd_{nm}_{kpi_name}", label_visibility="collapsed", placeholder="Rood %")
        if st.button("✕", key=f"kpi_del_{nm}_{kpi_name}"):
            del pd["kpis"][kpi_name]
            st.rerun()

    # Nieuwe KPI
    with st.expander("➕ KPI toevoegen"):
        c1, c2, c3, c4 = st.columns(4)
        with c1: n_kpi = st.text_input("Naam", key="nk_name", placeholder="Bijv. 'Doorlooptijd'")
        with c2: n_kpi_waarde = st.number_input("Waarde", value=0.0, key="nk_val")
        with c3: n_kpi_doel = st.number_input("Doel", value=0.0, key="nk_tgt")
        with c4: n_kpi_eenheid = st.selectbox("Eenheid", ["items","%","euro","seconden","minuten","uren","aantal"], key="nk_unit")
        if st.button("✅ KPI toevoegen", use_container_width=True, key="add_kpi") and n_kpi:
            pd["kpis"][n_kpi] = {"waarde": int(n_kpi_waarde) if n_kpi_eenheid in ["items","euro","aantal"] else round(n_kpi_waarde,1), "doel": int(n_kpi_doel) if n_kpi_eenheid in ["items","euro","aantal"] else round(n_kpi_doel,1), "eenheid": n_kpi_eenheid, "trend": "", "status": "groen", "uitleg": ""}
            st.rerun()

    # ─── Grafieken ─────────────────────────────────────────
    st.markdown(f'<div class="admin-sectie">📈 Grafieken — {gekozen_periode}</div>', unsafe_allow_html=True)
    for gk, gr in list(pd["grafieken"].items()):
        with st.container():
            st.markdown(f"""<div class="admin-card" style="padding:0.8rem 1rem;">
                <strong style="font-size:0.9rem;">{gr.get('titel',gk)}</strong></div>""", unsafe_allow_html=True)
            c1, c2 = st.columns([3, 1])
            with c1:
                labels_str = st.text_input("Labels (komma-gescheiden)", value=",".join(gr.get("labels",[])), key=f"gl_{nm}_{gk}", label_visibility="collapsed", placeholder="Ma,Di,Wo,Do,Vr")
                waarden_str = st.text_input("Waarden (komma-gescheiden)", value=",".join(str(v) for v in gr.get("waarden",[])), key=f"gw_{nm}_{gk}", label_visibility="collapsed", placeholder="100,120,110,130")
            with c2:
                gr["doel"] = st.number_input("Doellijn (optioneel)", value=float(gr.get("doel",0)), key=f"gd_{nm}_{gk}", label_visibility="collapsed")
                if st.button("✕", key=f"graf_del_{nm}_{gk}"):
                    del pd["grafieken"][gk]
                    st.rerun()
            gr["titel"] = st.text_input("Titel", value=gr.get("titel",""), key=f"gt_{nm}_{gk}", placeholder="Verwerkte items per dag")
            if labels_str:
                gr["labels"] = [x.strip() for x in labels_str.split(",") if x.strip()]
            if waarden_str:
                try:
                    gr["waarden"] = [float(x.strip()) for x in waarden_str.split(",") if x.strip()]
                except: pass

    with st.expander("➕ Grafiek toevoegen"):
        c1, c2 = st.columns(2)
        with c1:
            ng_key = st.text_input("Sleutel (bv. 'verwerkte_items_per_dag')", key="ng_key", placeholder="unieke-sleutel")
            ng_titel = st.text_input("Titel", key="ng_titel", placeholder="Verwerkte items per dag")
            ng_labels = st.text_input("Labels (komma)", key="ng_labels", placeholder="Ma,Di,Wo,Do,Vr")
        with c2:
            ng_waarden = st.text_input("Waarden (komma)", key="ng_waarden", placeholder="100,120,110,130")
            ng_doel = st.number_input("Doellijn (0 = uit)", value=0.0, key="ng_doel")
        if st.button("✅ Grafiek toevoegen", use_container_width=True, key="add_graf") and ng_key and ng_titel:
            try:
                pd["grafieken"][ng_key] = {
                    "titel": ng_titel,
                    "labels": [x.strip() for x in ng_labels.split(",") if x.strip()],
                    "waarden": [float(x.strip()) for x in ng_waarden.split(",") if x.strip()],
                    "doel": ng_doel
                }
                st.rerun()
            except: st.error("Ongeldige waarden.")

    # ─── HITL Detail ────────────────────────────────────────
    st.markdown(f'<div class="admin-sectie">👤 HITL Detail — {gekozen_periode}</div>', unsafe_allow_html=True)
    hitl = pd["hitl_detail"]
    c1, c2, c3, c4 = st.columns(4)
    with c1: hitl["totaal_acties"] = st.number_input("Totaal acties", value=int(hitl.get("totaal_acties",0)), key=f"ht_{nm}_{gekozen_periode}")
    with c2: hitl["menselijke_check"] = st.number_input("Menselijke checks", value=int(hitl.get("menselijke_check",0)), key=f"hm_{nm}_{gekozen_periode}")
    with c3: hitl["geautomatiseerd"] = st.number_input("Geautomatiseerd", value=int(hitl.get("geautomatiseerd",0)), key=f"ha_{nm}_{gekozen_periode}")
    with c4: hitl["bespaarde_uren"] = st.number_input("Bespaarde uren", value=float(hitl.get("bespaarde_uren",0)), key=f"hu_{nm}_{gekozen_periode}")

    st.markdown('<div class="admin-label">Categorieën</div>', unsafe_allow_html=True)
    cats = hitl.setdefault("categorieen", {})
    for cat_name in list(cats.keys()):
        ci = cats[cat_name]
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: st.markdown(f"**{cat_name}**")
        with c2: ci["totaal"] = st.number_input("Totaal", value=int(ci.get("totaal",0)), key=f"hct_{nm}_{cat_name}", label_visibility="collapsed")
        with c3: ci["hitl"] = st.number_input("HITL", value=int(ci.get("hitl",0)), key=f"hch_{nm}_{cat_name}", label_visibility="collapsed")
        ci["percentage"] = round(ci["hitl"] / ci["totaal"] * 100, 0) if ci["totaal"] else 0
        if st.button("✕", key=f"cat_del_{nm}_{cat_name}"):
            del cats[cat_name]
            st.rerun()

    with st.expander("➕ Categorie toevoegen"):
        c1, c2, c3 = st.columns(3)
        with c1: nc_naam = st.text_input("Naam", key=f"nc_name_{nm}_{gekozen_periode}", placeholder="Klantinteractie")
        with c2: nc_totaal = st.number_input("Totaal", value=0, key=f"nc_tot_{nm}_{gekozen_periode}")
        with c3: nc_hitl = st.number_input("HITL", value=0, key=f"nc_hitl_{nm}_{gekozen_periode}")
        if st.button("✅ Toevoegen", key=f"add_cat_{nm}") and nc_naam:
            pct = round(nc_hitl / nc_totaal * 100, 0) if nc_totaal else 0
            cats[nc_naam] = {"totaal": nc_totaal, "hitl": nc_hitl, "percentage": pct}
            st.rerun()

    # ─── Kosten en bottleneck ──────────────────────────────
    st.markdown(f'<div class="admin-sectie">💰 Kosten & Bottleneck — {gekozen_periode}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        pd["kosten_besparing"] = st.number_input("Kostenbesparing deze maand (€)", value=float(pd.get("kosten_besparing",0)), step=100.0, key=f"kb_{nm}_{gekozen_periode}", format="%.0f")
    with c2:
        vm = pd.setdefault("doelen_vorige_maand", {"kosten_besparing": 0})
        vm["kosten_besparing"] = st.number_input("Vorige maand (€)", value=float(vm.get("kosten_besparing",0)), step=100.0, key=f"vkb_{nm}_{gekozen_periode}", format="%.0f")

    bn = pd["bottleneck"]
    bn["tekst"] = st.text_area("Bottleneck beschrijving", value=bn.get("tekst",""), key=f"bn_{nm}_{gekozen_periode}", placeholder="Geen knelpunten deze maand.")
    bn["prioriteit"] = st.selectbox("Prioriteit", ["laag","medium","hoog"], index=["laag","medium","hoog"].index(bn.get("prioriteit","laag")), key=f"bnp_{nm}_{gekozen_periode}")

    # ─── Update & opslaan ──────────────────────────────────
    st.divider()
    pd["laatste_update"] = datetime.now().strftime("%Y-%m-%d")
    if st.button("💾 Alles opslaan", type="primary", use_container_width=True):
        opslaan_klant(data, fn)
        st.success(f"✅ '{nm}' opgeslagen!")
        st.rerun()
    if st.button("❌ Annuleren"):
        st.session_state.pop("edit_klant", None)
        st.session_state.admin_tab = "📋 Overzicht"
        st.rerun()

elif tab == "📦 JSON Editor":
    if "edit_klant" not in st.session_state or st.session_state.edit_klant not in klanten:
        st.info("Selecteer een klant via het overzicht.")
        st.stop()
    nm = st.session_state.edit_klant
    data, fn = klanten[nm]
    st.title(f"📦 JSON: {nm}")
    st.caption("Directe JSON-bewerking — alleen voor gevorderden.")
    json_str = st.text_area("JSON inhoud", value=json.dumps(data, indent=2, ensure_ascii=False), height=500, key="json_editor")
    c1, c2, c3 = st.columns([1, 1, 8])
    with c1:
        if st.button("💾 Opslaan", type="primary", use_container_width=True):
            try:
                parsed = json.loads(json_str)
                opslaan_klant(parsed, fn)
                st.success("✅ Opgeslagen!")
                st.rerun()
            except json.JSONDecodeError as e:
                st.error(f"JSON fout: {e}")
    with c2:
        if st.button("❌ Sluiten"):
            st.session_state.pop("edit_klant", None)
            st.session_state.admin_tab = "📋 Overzicht"
            st.rerun()
