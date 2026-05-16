# Gedeelde sidebar voor alle dashboard pagina's
import streamlit as st
from groei_team_ui import render_pakket_badge

def render_sidebar(data, kn, gt, periodes=None, periode_lijst=None):
    """Render de sidebar met logo, navigatie, periode selector, klant info en uitloggen.
    Aanroepen vanuit elke pagina: render_sidebar(data, kn, gt, periodes, periode_lijst)
    """
    # CSS om Streamlit's auto-navigatie te verbergen op alle pagina's
    # Ook: ongedaan maken van login pagina's sidebar hide
    st.markdown("""<style>
section[data-testid="stSidebar"] ul.st-emotion-cache-1gczx66 {
    display: none !important;
}
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
/* Sidebar toggle knop — vast pijltje rechtsboven in de sidebar */
.sidebar-toggle-collapse {
    position: absolute !important;
    top: 0.5rem !important;
    right: 0.5rem !important;
    z-index: 999 !important;
    width: 28px !important;
    height: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 6px !important;
    color: #ffffff !important;
    font-size: 1rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.sidebar-toggle-collapse:hover {
    background: rgba(255,255,255,0.2) !important;
    border-color: rgba(255,255,255,0.3) !important;
}
/* Floating open-knop als sidebar collapsed is */
.sidebar-toggle-open {
    position: fixed !important;
    top: 0.5rem !important;
    left: 0.5rem !important;
    z-index: 9999 !important;
    width: 32px !important;
    height: 32px !important;
    display: none !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(45, 27, 105, 0.9) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-size: 1.1rem !important;
    cursor: pointer !important;
    backdrop-filter: blur(8px) !important;
    transition: all 0.2s ease !important;
}
.sidebar-toggle-open:hover {
    background: rgba(45, 27, 105, 1) !important;
    border-color: rgba(255,255,255,0.4) !important;
}
/* Toon open-knop altijd — JS verstopt hem als sidebar open is */
.sidebar-toggle-open {
    display: flex !important;
}
</style>""", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-logo" style="position:relative;">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)

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

    # Toggle JS — maakt collapse/open knoppen aan in de DOM en koppelt click handlers
    st.markdown("""<script>
(function() {
    if (document.getElementById('bw-sidebar-toggle')) return;
    // Collapse knop (◀) — in de sidebar header
    var sbHeader = parent.document.querySelector('[data-testid="stSidebar"] .sidebar-logo');
    if (sbHeader) {
        sbHeader.style.position = 'relative';
        var collBtn = document.createElement('span');
        collBtn.id = 'bw-collapse-btn';
        collBtn.className = 'sidebar-toggle-collapse';
        collBtn.textContent = '◀';
        sbHeader.appendChild(collBtn);
        collBtn.onclick = function() {
            var sb = parent.document.querySelector('[data-testid="stSidebar"]');
            if (sb) { sb.style.width='0'; sb.style.minWidth='0'; sb.style.overflow='hidden'; sb.style.padding='0'; sb.style.border='none'; sb.setAttribute('aria-expanded','false'); }
            if (openBtn) openBtn.style.display='flex';
        };
    }
    // Open knop (☰) — floating linksboven
    var openBtn = document.createElement('div');
    openBtn.id = 'bw-open-btn';
    openBtn.className = 'sidebar-toggle-open';
    openBtn.textContent = '☰';
    document.body.appendChild(openBtn);
    openBtn.onclick = function() {
        var sb = parent.document.querySelector('[data-testid="stSidebar"]');
        if (sb) { sb.style.width=''; sb.style.minWidth=''; sb.style.overflow=''; sb.style.padding=''; sb.style.border=''; sb.setAttribute('aria-expanded','true'); }
        openBtn.style.display='none';
    };
    // Monitor sidebar breedte voor open knop
    function check() {
        var sb = parent.document.querySelector('[data-testid="stSidebar"]');
        if (!sb) return;
        var hidden = sb.getBoundingClientRect().width < 10;
        openBtn.style.display = hidden ? 'flex' : 'none';
    }
    check();
    setInterval(check, 500);
})();
</script>""", unsafe_allow_html=True)
