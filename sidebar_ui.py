# sidebar_ui.py — Gedeelde sidebar voor BigWaves dashboard
import streamlit as st

def render_sidebar(data: dict, kn: str, gt: dict, periodes: dict = None, periode_lijst: list = None):
    """Render de consistente sidebar voor alle dashboard pagina's."""
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.7rem;color:#64748b;margin:-8px 0 12px 0;letter-spacing:0.3px;">Conversiebureau</p>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-sect">NAVIGATIE</div>', unsafe_allow_html=True)
        st.page_link("dashboard.py", label="📊  Dashboard", width="stretch")
        st.page_link("pages/1_GroeiTeam.py", label="🌱  GroeiTeam", width="stretch")
        st.page_link("pages/1_Inzichten.py", label="📈  Inzichten", width="stretch")
        st.page_link("pages/2_Admin.py", label="🔐  Admin", width="stretch")

        # LinkedIn Outreach alleen voor Pro pakket
        pakket_naam = gt.get("pakket", "") if gt else ""
        if pakket_naam == "Pro":
            st.page_link("pages/3_LinkedIn.py", label="🔗  LinkedIn Outreach", use_container_width=True)
        else:
            st.markdown(
                f'<div style="padding:0.3rem 0.8rem;background:linear-gradient(135deg,rgba(16,185,129,0.08),rgba(16,185,129,0.02));'
                f'border:1px solid rgba(16,185,129,0.2);border-radius:10px;margin:0.2rem 0;font-size:0.78rem;">'
                f'<div style="color:#64748b;font-size:0.72rem;">🔗 LinkedIn Outreach</div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:2px;">'
                f'<span style="color:#94a3b8;">Alleen in Pro</span>'
                f'<span style="color:#10b981;font-weight:600;font-size:0.7rem;">⬆ Upgrade</span>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sect">KLANT</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='padding:0.3rem 0;font-size:0.85rem;color:var(--text);font-weight:500;'>{data.get('logo','🌊')} {kn}</div>", unsafe_allow_html=True)
        st.caption(f"Periode: {data.get('periode','—')} · Update: {data.get('laatste_update','—')}")

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if st.button("🚪 Uitloggen", width="stretch"):
            for k in ["ingelogd", "klant_naam", "data"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.65rem;color:#475569;text-align:center;margin-top:8px;">🌊 BigWaves — datagedreven · menselijk gecheckt</p>', unsafe_allow_html=True)
