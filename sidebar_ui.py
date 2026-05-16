# Gedeelde sidebar voor alle dashboard pagina's
import streamlit as st
from groei_team_ui import render_pakket_badge

def render_sidebar(data, kn, gt, periodes=None, periode_lijst=None):
    """Render de sidebar met logo, navigatie, periode selector, klant info en uitloggen.
    Aanroepen vanuit elke pagina: render_sidebar(data, kn, gt, periodes, periode_lijst)
    """
    # CSS om Streamlit's auto-navigatie te verbergen op alle pagina's
    st.markdown("""<style>
section[data-testid="stSidebar"] ul.st-emotion-cache-1gczx66 {
    display: none !important;
}
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
</style>""", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)

        # Pakket badge
        if gt:
            pakket = gt.get("pakket", "")
            if pakket:
                st.markdown(
                    f'<div style="padding:0 0 0.3rem 0;">{render_pakket_badge(pakket)}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<div class="sidebar-sec">Navigatie</div>', unsafe_allow_html=True)
        st.page_link("dashboard.py", label="📊 Dashboard", use_container_width=True)
        st.page_link("pages/1_Conversie.py", label="📈 Conversie", use_container_width=True)
        st.page_link("pages/1_Inzichten.py", label="📊 Inzichten", use_container_width=True)
        st.page_link("pages/2_Admin.py", label="🔧 Admin", use_container_width=True)
        pakket_naam = gt.get("pakket", "") if gt else ""
        if pakket_naam == "Pro":
            st.page_link("pages/3_LinkedIn.py", label="🔗 LinkedIn Outreach", use_container_width=True)
        else:
            st.markdown(
                f'<div style="padding:0.3rem 0.8rem;background:linear-gradient(135deg,rgba(82,115,255,0.08),rgba(82,115,255,0.02));'
                f'border:1px solid rgba(82,115,255,0.2);border-radius:10px;margin:0.2rem 0;font-size:0.78rem;">'
                f'<div style="color:var(--sidebar-text-muted);font-size:0.72rem;">🔗 LinkedIn Outreach</div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:2px;">'
                f'<span style="color:var(--sidebar-text-muted);">Alleen in Pro</span>'
                f'<span style="color:#5273ff;font-weight:600;font-size:0.7rem;">⬆ Upgrade</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-sec">Periode</div>', unsafe_allow_html=True)
        if periodes and periode_lijst:
            gekozen = st.selectbox("", periode_lijst,
                index=periode_lijst.index(st.session_state.huidige_periode) if st.session_state.huidige_periode in periode_lijst else 0,
                key="sidebar_periode_selector", label_visibility="collapsed")
            if gekozen != st.session_state.huidige_periode:
                st.session_state.huidige_periode = gekozen
                st.session_state.vergelijk_modus = False
                st.rerun()
            vergelijk_aan = st.toggle("🔁 Vergelijk", value=st.session_state.get("vergelijk_modus", False), key="sidebar_vergelijk_toggle")
            if vergelijk_aan != st.session_state.get("vergelijk_modus", False):
                st.session_state.vergelijk_modus = vergelijk_aan
                st.rerun()
            if vergelijk_aan and len(periode_lijst) > 1:
                st.selectbox("Vergelijk met", [p for p in periode_lijst if p != st.session_state.huidige_periode],
                    key="sidebar_vergelijk_periode")
        else:
            st.caption(f"Periode: {data.get('periode', '—')}")
        st.caption(f"Update: {data.get('laatste_update', '—')}")

        st.markdown('<div class="sidebar-sec">Klant</div>', unsafe_allow_html=True)
        st.markdown(
            f"<div style='padding:0.3rem 0;font-size:0.85rem;color:#ffffff;font-weight:500;'>{data.get('logo','🌊')} {kn}</div>",
            unsafe_allow_html=True,
        )
        st.divider()
        if st.button("🚪 Uitloggen", use_container_width=True):
            for k in ["ingelogd", "klant_naam", "data"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()
        st.divider()
        st.caption("🌊 BigWaves AI-bureau")
        st.caption("datagedreven · menselijk gecheckt")
