# sidebar_ui.py — Gedeelde sidebar voor BigWaves dashboard
import streamlit as st

def render_sidebar(data: dict, kn: str, gt: dict = None, periodes: dict = None, periode_lijst: list = None):
    """Render de consistente sidebar voor alle dashboard pagina's."""
    if not data:
        return
    # Forceer sidebar expanded bij elke pagina
    st.markdown("""
    <script>
    const sb = parent.document.querySelector('[data-testid="stSidebar"]');
    if (sb && sb.getAttribute('aria-expanded') === 'false') {
        const btn = parent.document.querySelector('[data-testid="stSidebarCollapsedControl"]');
        if (btn) btn.click();
    }
    </script>
    """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🌊 <span>BigWaves</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">datagedreven · menselijk gecheckt</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-sect">NAVIGATIE</div>', unsafe_allow_html=True)
        st.page_link("dashboard.py", label="📊  Dashboard", width="stretch")
        st.page_link("pages/1_GroeiTeam.py", label="🌱  GroeiTeam", width="stretch")
        st.page_link("pages/1_Inzichten.py", label="📈  Inzichten", width="stretch")
        st.page_link("pages/2_Admin.py", label="🔐  Admin", width="stretch")

        # LinkedIn Outreach alleen voor Pro pakket
        pkg = gt.get("pakket", "") if gt else ""
        if pkg == "Pro":
            st.page_link("pages/3_LinkedIn.py", label="🔗  LinkedIn Outreach", use_container_width=True)
        else:
            st.markdown(
                '<div style="padding:0.3rem 0.8rem;background:linear-gradient(135deg,rgba(16,185,129,0.08),rgba(16,185,129,0.02));'
                'border:1px solid rgba(16,185,129,0.2);border-radius:10px;margin:0.2rem 0;font-size:0.78rem;">'
                '<div style="color:#64748b;font-size:0.72rem;">🔗 LinkedIn Outreach</div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:2px;">'
                '<span style="color:#94a3b8;">Alleen in Pro</span>'
                '<span style="color:#10b981;font-weight:600;font-size:0.7rem;">⬆ Upgrade</span>'
                '</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

        # Health badge
        gt_data = gt or {}
        health = gt_data.get("health_score") or data.get("health_score")
        if health is not None:
            c = "#10b981" if health >= 80 else "#f59e0b" if health >= 60 else "#ef4444"
            st.markdown(
                f'<div class="health-badge">'
                f'<span class="health-dot" style="background:{c};"></span>'
                f'Groei Health: <strong style="color:{c};">{health}%</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown('<div class="sidebar-sect">KLANT</div>', unsafe_allow_html=True)
        logo = data.get('logo','🌊')
        st.markdown(f'<div class="client-name">{logo} {kn}</div>', unsafe_allow_html=True)
        periode = data.get('periode','—')
        update = data.get('laatste_update','—')
        st.markdown(f'<div class="client-meta">Periode: {periode}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="client-meta">Update: {update}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if st.button("🚪 Uitloggen", width="stretch"):
            for k in ["ingelogd", "klant_naam", "data"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.65rem;color:#475569;text-align:center;margin-top:8px;">🌊 BigWaves AI-bureau — datagedreven · menselijk gecheckt</p>', unsafe_allow_html=True)
