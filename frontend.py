import streamlit as st
import base64
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import shap

def get_base64_of_bin_file(bin_file):
    """Reads a local file and converts it to base64 for CSS/HTML injection."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

def apply_custom_css():
    # ══════════════════════════════════════════════════════════════════════
    # GLASSMORPHISM DESIGN SYSTEM — futuristic AI financial terminal.
    #   STACK:
    #     -1  = background video (fixed, viewport-wide, clearly visible)
    #     0   = navy/purple tint + glow (fixed, light)
    #     1   = glass application shell (block container, translucent)
    #     10  = content panels / cards (dark translucent glass)
    #     20  = sidebar + sticky top monitor bar
    #     30  = dropdowns / modals
    #   The background stays clearly visible through every glass surface.
    # ══════════════════════════════════════════════════════════════════════
    video_base64 = get_base64_of_bin_file("now_change_the_text_into_FINA (1).mp4")

    video_tag = ""
    if video_base64:
        video_tag = f"""
        <video autoplay loop muted playsinline id="bg-video">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """
    st.markdown(
        f"""{video_tag}
        <div id="bg-tint"></div>
        """,
        unsafe_allow_html=True
    )

    # ── Technical fonts (falls back gracefully offline) ──────────────────────
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* ═══════════════════════════════════════════════════════════════════
           GLASS DESIGN SYSTEM — single source of truth
           Dark navy · indigo · violet · cyan · coral · glassmorphism
        ═══════════════════════════════════════════════════════════════════ */

        /* ── DESIGN TOKENS ─────────────────────────────────────────────── */
        :root {
            --shell-gap: 0.9rem;
            --ticker-h: 42px;
            --sidebar-w: 232px;

            /* Layered surface hierarchy (background → shell → cards) */
            --bg-base:      #070A2A;                     /* deep navy base */
            --bg-nav:       #0A0D35;                     /* dark navy/purple */

            --glass-shell:   rgba(12, 15, 48, 0.58);     /* main terminal window */
            --glass-sidebar: rgba(8, 10, 38, 0.78);      /* floating sidebar */
            --glass-ticker:  rgba(7, 9, 32, 0.84);       /* top monitor bar */
            --glass-card:    rgba(10, 13, 42, 0.62);     /* telemetry / panels */
            --glass-card-strong: rgba(10, 13, 42, 0.78); /* important cards */
            --glass-input:   rgba(10, 13, 42, 0.82);     /* dropdown / inputs */

            --border-glass:        rgba(120, 100, 255, 0.32);
            --border-glass-strong: rgba(150, 120, 255, 0.46);
            --border-card:         rgba(110, 100, 200, 0.28);

            --glass-shadow:  0 10px 36px rgba(0, 0, 0, 0.42);
            --shell-shadow:  0 22px 90px rgba(0, 0, 0, 0.45), inset 0 0 44px rgba(100, 70, 255, 0.05);

            --accent-purple: #8B5CFF;
            --accent-violet: #7C4DFF;
            --accent-indigo: #5B6CFF;
            --accent-blue:   #3B82F6;
            --accent-cyan:   #24CFFF;
            --accent-red:    #FF4D5A;
            --accent-coral:  #FF5964;
            --accent-green:  #20E88A;
            --accent-amber:  #F59E0B;

            --text-primary:   #F2F3FF;
            --text-secondary: #A7ABC8;
            --text-muted:     #6D739A;
            --text-label:     #9FA6D6;

            --radius-lg: 20px;
            --radius:    14px;
            --radius-sm: 10px;
        }

        /* ══ LAYER -1 / 0 — FIXED BACKGROUND STACK (video + tint) ══ */
        /* The video container is a descendant of the shell, so the shell can
           NOT use backdrop-filter (it would become the containing block for
           this fixed video). We keep the video fixed at z-index:-1 so it paints
           below every translucent glass surface while covering the viewport. */
        [data-testid="stElementContainer"]:has(#bg-video) {
            position: fixed !important;
            inset: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            pointer-events: none !important;
            z-index: -1 !important;
            overflow: hidden !important;
        }
        #bg-video {
            position: absolute !important;
            inset: 0 !important;
            width: 100% !important;
            height: 100% !important;
            object-fit: cover !important;
            pointer-events: none !important;
            filter: blur(4px) saturate(1.05) brightness(0.92) !important;
            transform: scale(1.06) !important;
            z-index: 0 !important;
        }
        #bg-tint {
            position: absolute !important;
            inset: 0 !important;
            z-index: 1 !important;
            pointer-events: none !important;
            background:
                radial-gradient(1100px 520px at 78% -8%, rgba(139, 92, 255, 0.16), transparent 62%),
                radial-gradient(900px 460px at 8% 112%, rgba(36, 207, 255, 0.10), transparent 60%),
                linear-gradient(160deg,
                    rgba(5, 7, 30, 0.42) 0%,
                    rgba(8, 10, 42, 0.50) 100%);
        }

        /* ══ LAYER 1 — GLASS APPLICATION SHELL (main terminal window) ══ */
        [data-testid="stMainBlockContainer"],
        [data-testid="block-container"] {
            position: relative;
            max-width: none !important;
            margin: calc(var(--ticker-h) + 1.35rem) 1.3rem 2.2rem 1.3rem !important;
            padding: 0.9rem 1.5rem 1.9rem !important;
            background: var(--glass-shell);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-lg);
            box-shadow: var(--shell-shadow);
        }

        /* ══ TRANSPARENT CHROME — background video visible everywhere ══ */
        .stApp,
        .stApp > header,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stMain"],
        section.main,
        [data-testid="stVerticalBlock"],
        [data-testid="stHorizontalBlock"],
        html, body, #root {
            background: transparent !important;
            background-color: transparent !important;
        }
        [data-testid="stDecoration"] { display: none !important; }
        #MainMenu { visibility: hidden; }
        footer     { visibility: hidden; }
        header     { visibility: hidden; }

        /* ══ LAYER 10 — CONTENT SITS ABOVE THE GLASS ══ */
        [data-testid="stElementContainer"] {
            position: relative !important;
            z-index: 10 !important;
        }
        [data-testid="stElementContainer"]:has(#bg-video) {
            position: fixed !important;
            z-index: -1 !important;
        }
        [data-testid="block-container"] {
            padding-top: calc(var(--shell-gap) + 0.2rem) !important;
        }

        /* ══ LAYER 20 — SIDEBAR (floating glass command panel) ══
           Desktop (>=1024px): TWO REAL COLUMNS. The app container is forced
           into an in-flow flex row:
             column 1 = sidebar  (position: sticky; reserves its width via
                                  flex-basis 232px; stays visible on scroll)
             column 2 = main     (flex: 1 1 auto; min-width: 0)
           Because the sidebar remains IN FLOW, the layout engine reserves its
           horizontal space — main content can never slide under it, so no
           fixed-position compensation or random margins are needed. */
        [data-testid="stSidebar"] {
            border-radius: 14px !important;
            background: var(--glass-sidebar) !important;
            backdrop-filter: blur(20px) saturate(135%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(135%) !important;
            border: 1px solid var(--border-glass) !important;
            box-shadow: 0 14px 46px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        }
        @media (min-width: 1024px) {
            /* Parent = two real columns */
            [data-testid="stAppViewContainer"] {
                display: flex !important;
                flex-direction: row !important;
                align-items: stretch !important;
                width: 100% !important;
            }
            /* Column 2 — the header+main wrapper takes the remaining space */
            [data-testid="stAppViewContainer"] > div {
                flex: 1 1 auto !important;
                min-width: 0 !important;
            }
            [data-testid="stMain"],
            [data-testid="stMainBlockContainer"] {
                width: 100% !important;
                min-width: 0 !important;
            }
            /* Column 1 — sidebar stays in flow (sticky) and reserves its width */
            [data-testid="stSidebar"] {
                position: sticky !important;
                top: 12px !important;
                align-self: flex-start !important;
                flex: 0 0 var(--sidebar-w) !important;
                width: var(--sidebar-w) !important;
                min-width: var(--sidebar-w) !important;
                max-width: var(--sidebar-w) !important;
                height: calc(100vh - 24px) !important;
                margin: 12px 0 12px 12px !important;
                display: flex !important;
                flex-direction: column !important;
                visibility: visible !important;
                opacity: 1 !important;
                transform: none !important;
                overflow: hidden auto !important;
                z-index: 20 !important;
            }
            /* Sidebar content fills the panel so SYSTEM STATUS pins to bottom */
            [data-testid="stSidebarContent"],
            [data-testid="stSidebarUserContent"] {
                height: 100% !important;
            }
            [data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }
        }
        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding: 0.5rem 0.5rem 0.75rem !important;
        }
        /* Push SYSTEM STATUS card to the bottom of the sidebar panel */
        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] > div {
            display: flex !important;
            flex-direction: column !important;
            min-height: 100% !important;
        }
        [data-testid="stSidebar"] .system-status-card {
            margin-top: auto !important;
        }
        [data-testid="stSidebar"] h2 {
            font-family: 'IBM Plex Mono', 'Consolas', monospace !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            letter-spacing: 0.14em !important;
            color: var(--accent-purple) !important;
            margin: 0.2rem 0 0.9rem !important;
        }
        [data-testid="stSidebar"] .stRadio > label,
        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] p {
            font-family: 'IBM Plex Mono', 'Consolas', monospace !important;
            font-size: 11px !important;
            font-weight: 500 !important;
            letter-spacing: 0.1em !important;
            color: var(--text-secondary) !important;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] > div {
            gap: 4px !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            display: flex !important;
            align-items: center !important;
            gap: 9px !important;
            padding: 9px 12px !important;
            border-radius: 10px !important;
            border: 1px solid transparent !important;
            color: rgba(240, 240, 255, 0.88) !important;
            font-size: 13.5px !important;
            transition: background 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease !important;
        }
        [data-testid="stSidebar"] .stRadio label:hover {
            background: rgba(124, 92, 255, 0.16) !important;
            border-color: rgba(150, 120, 255, 0.26) !important;
        }
        [data-testid="stSidebar"] .stRadio label:has(input:checked) {
            background: rgba(124, 92, 255, 0.34) !important;
            border-color: rgba(150, 120, 255, 0.46) !important;
            border-radius: 10px !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 18px rgba(124, 92, 255, 0.28) !important;
        }

        /* ══ LAYER 20 — TOP MONITORING TICKER (floating sticky glass bar) ══ */
        /* The ticker floats ABOVE the shell: it is pulled up out of the shell's
           flow with a negative margin so it reads as a separate monitor bar over
           the background, with a visible gap below it before the shell starts. */
        [data-testid="stElementContainer"]:has(.hud-ticker-wrap) {
            position: sticky !important;
            top: 0.9rem !important;
            z-index: 20 !important;
            margin-top: calc(-1 * (var(--ticker-h) + 1.35rem)) !important;
            margin-bottom: 1.1rem !important;
        }
        .hud-ticker-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
            background: var(--glass-ticker);
            backdrop-filter: blur(16px) saturate(135%);
            -webkit-backdrop-filter: blur(16px) saturate(135%);
            border: 1px solid rgba(100, 80, 220, 0.30);
            border-radius: 12px;
            box-shadow: 0 6px 26px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.05);
            padding: 6px 14px;
            min-height: var(--ticker-h);
            overflow: hidden;
        }
        .hud-status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding-right: 14px;
            border-right: 1px solid rgba(120, 100, 255, 0.22);
            flex-shrink: 0;
        }
        .hud-status-label {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: rgba(160, 170, 220, 0.85);
        }
        .hud-status-online {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.14em;
            color: var(--accent-green);
        }
        .hud-online-dot {
            display: inline-block;
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 9px rgba(32, 232, 138, 0.75);
            flex-shrink: 0;
        }
        .hud-ticker-overflow { overflow: hidden; flex: 1; }
        .hud-ticker-scroll {
            display: inline-block;
            white-space: nowrap;
            padding-left: 20px;
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 11px;
            letter-spacing: 0.07em;
            color: rgba(165, 175, 220, 0.62);
            animation: hud-scroll 40s linear infinite;
        }
        .hud-ticker-scroll b {
            color: rgba(210, 220, 255, 0.85);
            font-weight: 600;
        }
        @keyframes hud-scroll {
            0%   { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        /* Right-side futuristic equalizer icon */
        .hud-ticker-wrap::after {
            content: "";
            display: flex;
            align-items: flex-end;
            gap: 2.5px;
            height: 18px;
            width: 24px;
            flex-shrink: 0;
            padding: 0 2px;
        }
        .hud-ticker-wrap::after {
            background:
                linear-gradient(180deg, var(--accent-cyan) 0 35%, transparent 36%) 0 0/4px 100% no-repeat,
                linear-gradient(180deg, var(--accent-purple) 0 55%, transparent 56%) 7px 0/4px 100% no-repeat,
                linear-gradient(180deg, var(--accent-cyan) 0 25%, transparent 26%) 14px 0/4px 100% no-repeat,
                linear-gradient(180deg, var(--accent-purple) 0 70%, transparent 71%) 21px 0/4px 100% no-repeat;
            animation: hud-eq 1.6s ease-in-out infinite;
        }
        @keyframes hud-eq {
            0%, 100% { transform: translateY(0); opacity: 0.75; }
            50%      { transform: translateY(1px); opacity: 1; }
        }

        /* ══ GLASS CARD LANGUAGE — dark translucent glass cards ══ */
        .pt-glass-panel,
        .pt-data-feed,
        .hud-warning-box,
        .slider-card,
        .crisis-indicator-card,
        .system-status-card {
            background: var(--glass-card);
            backdrop-filter: blur(14px) saturate(130%);
            -webkit-backdrop-filter: blur(14px) saturate(130%);
            border: 1px solid var(--border-card);
            border-radius: var(--radius-sm);
            box-shadow: var(--glass-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.05);
        }
        .pt-glass-panel      { padding: 1.1rem 1.3rem 0.9rem;  margin: 0.5rem 0 1rem; }
        .pt-data-feed        { display: flex; align-items: flex-start; gap: 14px; padding: 14px 18px; margin: 0.5rem 0 1.1rem; border-left: 3px solid rgba(36, 207, 255, 0.55); }
        .hud-warning-box     { display: flex; align-items: flex-start; gap: 14px; padding: 14px 18px; border-left: 3px solid rgba(59, 130, 246, 0.70); margin: 1rem 0; }
        .slider-card         { padding: 10px 12px 6px; margin-bottom: 10px; }
        .crisis-indicator-card { padding: 12px 14px; margin-bottom: 10px; border-left: 3px solid var(--status-color, var(--accent-purple)); }
        .system-status-card  { padding: 14px; margin-top: 1rem; }

        .hud-risk-card {
            border-radius: var(--radius-sm);
            box-shadow: var(--glass-shadow);
        }
        .hud-risk-card b {
            font-family: 'Inter', sans-serif !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
        }

        /* ── Section / telemetry labels ─────────────────────────────────── */
        .hud-section-label {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: var(--accent-purple);
            margin: 0.5rem 0 0.8rem;
        }
        .pt-data-feed-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(34, 211, 238, 0.65);
            flex-shrink: 0;
            margin-top: 5px;
        }
        .pt-data-feed-label {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent-cyan);
            margin-bottom: 4px;
        }
        .pt-data-feed-body {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: rgba(243, 244, 247, 0.90);
        }
        .hud-warning-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            background: var(--accent-blue);
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.60);
            flex-shrink: 0;
            margin-top: 4px;
        }
        .hud-warning-title {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--accent-blue);
            margin-bottom: 4px;
        }
        .hud-warning-body {
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            color: rgba(243, 244, 247, 0.75);
        }
        .crisis-indicator-label {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 9px;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: rgba(150, 175, 230, 0.62);
            margin-bottom: 6px;
        }
        .crisis-indicator-value {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 22px;
            font-weight: 600;
            color: rgba(230, 240, 255, 0.95);
            margin-bottom: 4px;
        }
        .crisis-indicator-status { display: flex; align-items: center; gap: 8px; }
        .crisis-indicator-status-tag {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 9.5px;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--status-color, var(--accent-purple));
        }
        .crisis-indicator-delta {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 9.5px;
            color: rgba(160, 180, 230, 0.50);
        }
        .system-status-label {
            font-family: 'IBM Plex Mono', 'Consolas', monospace;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.11em;
            color: var(--accent-purple);
            margin-bottom: 14px;
        }
        .system-status-line {
            color: #E7E4F6;
            font-size: 12px;
        }
        .system-status-line span {
            display: inline-block;
            width: 9px; height: 9px;
            margin: 0 10px 0 1px;
            border-radius: 50%;
            background: #22E77E;
            box-shadow: 0 0 8px #22E77E;
            vertical-align: middle;
        }

        /* ── TYPOGRAPHY ─────────────────────────────────────────────────── */
        .stApp { color: var(--text-primary); }
        h1 {
            font-family: 'Inter', sans-serif !important;
            font-size: 36px !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
            color: var(--text-primary) !important;
            margin: 0.1rem 0 0.2rem !important;
        }
        h1 + p {
            color: var(--text-secondary) !important;
            font-size: 15px !important;
            margin: 0 0 1rem !important;
        }
        h2 {
            font-family: 'Inter', sans-serif !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            color: var(--accent-purple) !important;
        }
        h3 {
            font-family: 'Inter', sans-serif !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            color: rgba(190, 200, 240, 0.85) !important;
        }
        .stCaptionContainer p,
        [data-testid="stCaptionContainer"] {
            font-family: 'IBM Plex Mono', 'Consolas', monospace !important;
            font-size: 11px !important;
            letter-spacing: 0.03em !important;
            color: var(--text-muted) !important;
        }

        /* ── CONTROLS — SLIDERS (dark track, coral active, visible thumb) ── */
        [data-testid="stSlider"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        [data-testid="stSlider"] label {
            color: var(--text-secondary) !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {
            background: rgba(255, 255, 255, 0.13) !important;
            height: 5px !important;
            border-radius: 3px !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div > div {
            background: var(--accent-red) !important;
            box-shadow: 0 0 12px rgba(255, 77, 90, 0.55) !important;
        }
        [data-testid="stSlider"] div[role="slider"] {
            background-color: var(--accent-coral) !important;
            border: 2px solid rgba(255, 255, 255, 0.85) !important;
            box-shadow: 0 0 14px rgba(255, 89, 100, 0.8), inset 0 0 4px rgba(255, 255, 255, 0.5) !important;
            width: 17px !important;
            height: 17px !important;
            border-radius: 50% !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] div {
            color: #F3F4F7 !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }

        /* ── CONTROLS — SELECT BOX (dark translucent glass) ─────────────── */
        [data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
            background: var(--glass-input) !important;
            border: 1px solid var(--border-glass) !important;
            backdrop-filter: blur(12px) saturate(130%) !important;
            -webkit-backdrop-filter: blur(12px) saturate(130%) !important;
            color: var(--text-primary) !important;
            border-radius: 10px !important;
            min-height: 52px !important;
        }
        [data-testid="stSelectbox"] > div[data-baseweb="select"] > div:focus-within {
            border-color: var(--accent-purple) !important;
            box-shadow: 0 0 0 1px rgba(139, 92, 255, 0.30) !important;
        }
        [data-testid="stSelectbox"] label {
            color: var(--text-secondary) !important;
            font-size: 11.5px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            margin-bottom: 8px !important;
        }
        [data-testid="stSelectbox"] span,
        [data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"],
        [data-testid="stSelectbox"] * {
            color: rgba(242, 243, 255, 0.95) !important;
        }

        /* ── CONTROLS — BUTTONS (purple → indigo gradient + glow) ───────── */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #8B5CFF 0%, #7C4DFF 100%) !important;
            border: 1px solid rgba(150, 120, 255, 0.45) !important;
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            letter-spacing: 0.08em !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            box-shadow: 0 0 22px rgba(139, 92, 255, 0.38), 0 4px 18px rgba(0, 0, 0, 0.35) !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #9B6CFF 0%, #8B5CFF 100%) !important;
            box-shadow: 0 0 30px rgba(139, 92, 255, 0.55), 0 4px 18px rgba(0, 0, 0, 0.35) !important;
            transform: translateY(-1px) !important;
        }
        .stDownloadButton > button {
            background: linear-gradient(135deg, #8B5CFF 0%, #7C4DFF 100%) !important;
            border: 1px solid rgba(150, 120, 255, 0.45) !important;
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.6rem !important;
            box-shadow: 0 0 18px rgba(139, 92, 255, 0.30) !important;
        }

        /* ── ALERTS / DATAFRAME — dark translucent glass ─────────────────── */
        div[data-testid="stAlert"] {
            background: var(--glass-card) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius-sm) !important;
            backdrop-filter: blur(12px) saturate(130%) !important;
            -webkit-backdrop-filter: blur(12px) saturate(130%) !important;
            box-shadow: var(--glass-shadow) !important;
        }
        [data-testid="stDataFrameResizable"] {
            background: var(--glass-card-strong) !important;
            border: 1px solid var(--border-glass) !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: var(--glass-shadow) !important;
        }

        /* ── LAYER 30 — DROPDOWNS / MODALS ──────────────────────────────── */
        [data-testid="stPopover"],
        [data-baseweb="popover"],
        [data-baseweb="menu"] {
            z-index: 30 !important;
        }
        [data-baseweb="popover"] [role="option"],
        [data-baseweb="menu"] [role="option"],
        [data-baseweb="menu"] li {
            background: rgba(10, 13, 42, 0.96) !important;
            color: var(--text-primary) !important;
        }
        [data-baseweb="popover"] [role="option"]:hover,
        [data-baseweb="menu"] li:hover {
            background: rgba(139, 92, 255, 0.35) !important;
            color: #FFFFFF !important;
        }

        /* ── SUBTLE TERMINAL SCROLLBAR ──────────────────────────────────── */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: rgba(8, 10, 30, 0.35); }
        ::-webkit-scrollbar-thumb { background: rgba(139, 92, 255, 0.35); border-radius: 8px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 255, 0.55); }
    </style>
    """, unsafe_allow_html=True)


def apply_home_style():
    """Home page only: fully NATURAL background — the existing background video
    is shown clear and unblurred with NO tint, NO glass shell, NO dark overlay.
    The Global Macro Monitor bar stays at the top of the main area, and a large
    cinematic "FINANCIAL CRISIS" title is centered within the main content area
    (to the right of the sidebar), sitting directly over the natural background.
    Applies exclusively when the Home route is active, so the other pages keep
    their glassmorphism treatment exactly as-is."""
    st.markdown("""
    <style>
        /* Natural background: remove blur / saturation / brightness treatment */
        #bg-video {
            filter: none !important;
            transform: none !important;
        }
        /* Remove the navy/purple tint + dark gradient overlay */
        #bg-tint {
            display: none !important;
        }
        /* No glass shell on Home — fully transparent, keeps the normal spacing
           so the Global Macro Monitor bar floats at the top like other pages */
        [data-testid="stMainBlockContainer"],
        [data-testid="block-container"] {
            background: transparent !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            border: none !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }
        /* Cinematic hero — aligned toward the left/center of the main content */
        .home-hero {
            position: relative;
            min-height: calc(100vh - 150px);
            min-width: 0;
        }
        .home-title {
            position: absolute;
            left: 20%; /* <--- Shifted right to clear the sidebar */
            top: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: max-content;
            text-align: center;
            white-space: nowrap;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: clamp(50px, 4.5vw, 95px); /* <--- Slightly reduced to fit the gap perfectly */
            font-weight: 900;
            letter-spacing: 4px;
            line-height: 0.95;
            text-transform: uppercase;
            color: rgba(230, 232, 255, 0.28);
            text-shadow: 0 0 20px rgba(150, 100, 255, 0.12),
                         0 0 60px rgba(150, 100, 255, 0.08);
            pointer-events: none;
            z-index: 2;
        }
        .home-title span {
            display: block;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)


def render_ticker():
    """Render the top HUD monitoring status bar."""
    sep = "&nbsp;&nbsp;<b>|</b>&nbsp;&nbsp;"
    ticker_items = (
        f"VIX: <b>18.4</b> +1.2%{sep}"
        f"US TREASURY 10Y: <b>4.12%</b>{sep}"
        f"BRENT CRUDE: <b>$84.50</b>{sep}"
        f"SCANNING HISTORICAL CREDIT CYCLES{sep}"
        f"GLOBAL MACRO MONITOR ACTIVE{sep}"
        f"VIX: <b>18.4</b> +1.2%{sep}"
        f"US TREASURY 10Y: <b>4.12%</b>{sep}"
        f"BRENT CRUDE: <b>$84.50</b>{sep}"
        f"SCANNING HISTORICAL CREDIT CYCLES{sep}"
        f"GLOBAL MACRO MONITOR ACTIVE"
    )
    st.markdown(f"""
    <div class="hud-ticker-wrap">
        <div class="hud-status-pill">
            <span class="hud-status-label">GLOBAL MACRO MONITOR</span>
            <span class="hud-online-dot"></span>
            <span class="hud-status-online">ONLINE</span>
        </div>
        <div class="hud-ticker-overflow">
            <span class="hud-ticker-scroll">{ticker_items}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_warning_no_data():
    """Render the HUD-style system notification for empty telemetry state."""
    st.markdown("""
    <div class="hud-warning-box">
        <div class="hud-warning-dot"></div>
        <div>
            <div class="hud-warning-title">No Telemetry Data</div>
            <div class="hud-warning-body">Run a prediction in the Terminal first to populate this view.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def determine_risk_level(risk_score):
    if risk_score >= 60:
        return (
            "CRITICAL SYSTEMIC RISK",
            "#ef4444",
            """<div class='hud-risk-card' style='background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.26);border-left:2px solid rgba(239,68,68,0.70);'>
                <b style='color:rgba(240,100,100,0.95);'>&#9888; WARNING: HIGH PROBABILITY OF IMPENDING FINANCIAL COLLAPSE DETECTED</b>
            </div>"""
        )
    elif risk_score >= 30:
        return (
            "ELEVATED RISK DETECTED",
            "#f59e0b",
            """<div class='hud-risk-card' style='background:rgba(245,158,11,0.12);border:1px solid rgba(245,158,11,0.24);border-left:2px solid rgba(245,158,11,0.65);'>
                <b style='color:rgba(240,170,70,0.95);'>&#9888; CAUTION: MACROECONOMIC INSTABILITY RISING</b>
            </div>"""
        )
    else:
        return (
            "ECONOMY STABLE",
            "#10b981",
            """<div class='hud-risk-card' style='background:rgba(16,185,129,0.10);border:1px solid rgba(16,185,129,0.20);border-left:2px solid rgba(16,185,129,0.55);'>
                <b style='color:rgba(40,210,145,0.95);'>&#10003; STATUS NORMAL: METRICS WITHIN STABLE OPERATING RANGES</b>
            </div>"""
        )


def render_gauge(risk_score, gauge_color, risk_label):
    st.markdown(
        "<div class='hud-section-label'>PROBABILITY GAUGE</div>",
        unsafe_allow_html=True
    )
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        number={
            'suffix': "%",
            'font': {'size': 46, 'family': 'IBM Plex Mono', 'color': 'rgba(225,238,255,0.93)'}
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "rgba(160, 185, 240, 0.40)",
                'tickfont': {'family': 'IBM Plex Mono', 'size': 10, 'color': 'rgba(140,170,230,0.55)'}
            },
            'bar': {'color': gauge_color, 'thickness': 0.22},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 1,
            'bordercolor': "rgba(130, 100, 255, 0.20)",
            'steps': [
                {'range': [0, 30],   'color': "rgba(16, 185, 129, 0.08)"},
                {'range': [30, 60],  'color': "rgba(245, 158, 11, 0.08)"},
                {'range': [60, 100], 'color': "rgba(239, 68, 68, 0.08)"}
            ],
            'threshold': {
                'line': {'color': gauge_color, 'width': 2},
                'thickness': 0.75,
                'value': risk_score
            }
        }
    ))
    fig.update_layout(
        height=340,
        margin=dict(l=20, r=20, t=25, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "rgba(190,210,250,0.75)", 'family': 'IBM Plex Mono'}
    )
    st.plotly_chart(fig, width='stretch')
    st.markdown(
        f"""<div style='text-align:center;margin-top:-10px;'>
            <span style='font-family:"IBM Plex Mono",monospace;font-size:13px;font-weight:600;
            letter-spacing:0.12em;color:{gauge_color};text-shadow:0 0 12px {gauge_color}55;'>
            {risk_label}
            </span>
        </div>""",
        unsafe_allow_html=True
    )


def render_shap(shap_values):
    st.markdown(
        "<div class='hud-section-label'>AI LOGIC TELEMETRY</div>",
        unsafe_allow_html=True
    )
    st.caption("🟥 Risk-increasing factors  |  🟦 Risk-reducing factors")

    shap_values.feature_names = [
        "Interest Rate Gap", "Total Debt vs Economy", "Debt Growth Speed",
        "Abnormal Debt Spikes", "Abnormal Rate Shifts",
        "Inflation (Prices)", "Unemployment Rate", "Government Debt"
    ]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 8))
    shap.plots.waterfall(shap_values[0], show=False)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    st.pyplot(fig, transparent=True)
    plt.clf()

def render_world_map(risk_df):
    st.markdown(
        "<div class='hud-section-label'>GLOBAL MACRO RISK HEATMAP</div>",
        unsafe_allow_html=True
    )
    st.caption("Scanning latest telemetry across all monitored global economies...")

    fig = px.choropleth(
        risk_df,
        locations="country",
        locationmode="country names",
        color="Risk Score",
        hover_name="country",
        color_continuous_scale=[(0, "#10b981"), (0.5, "#f59e0b"), (1, "#ef4444")],
        range_color=[0, 100]
    )
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(120,155,220,0.18)",
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)',
            landcolor='rgba(255,255,255,0.04)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="rgba(190,210,250,0.75)",
        font={'family': 'IBM Plex Mono'},
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        coloraxis_colorbar=dict(
            title=dict(
                text="RISK",
                font=dict(family='IBM Plex Mono', size=10, color='rgba(150,180,240,0.65)')
            ),
            tickfont=dict(family='IBM Plex Mono', size=9, color='rgba(150,180,240,0.60)'),
            thickness=12,
            len=0.6,
            bgcolor='rgba(5,10,25,0.55)',
            bordercolor='rgba(100,130,220,0.15)',
            borderwidth=1
        )
    )
    st.plotly_chart(fig, width='stretch')


def render_financial_crisis(live_data):
    """Render the Financial Crisis Overview page — HUD-style indicator dashboard."""
    import plotly.graph_objects as go
    import streamlit as st

    # ── Section header ────────────────────────────────────────────────────────
    st.markdown(
        "<div class='hud-section-label'>LIVE CRISIS INDICATOR PANEL</div>",
        unsafe_allow_html=True
    )
    st.caption("Real-time macro stress signals monitored across global markets.")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── LIVE Dynamic Logic for Colors ─────────────────────────────────────────
    vix_val = live_data.get('VIX', 18.4)
    vix_color = "#ef4444" if vix_val > 30 else "#f59e0b" if vix_val > 20 else "#10b981"
    vix_stat = "CRITICAL" if vix_val > 30 else "ELEVATED" if vix_val > 20 else "STABLE"

    us10y_val = live_data.get('US_10Y', 4.12)
    us10y_color = "#ef4444" if us10y_val > 5.0 else "#f59e0b" if us10y_val > 4.0 else "#10b981"
    us10y_stat = "CRITICAL" if us10y_val > 5.0 else "ELEVATED" if us10y_val > 4.0 else "STABLE"

    # ── Indicator data (Mixing LIVE feed with static macro data) ──────────────
    indicators = [
        {"label": "VIX — Market Fear Index",   "value": vix_val,  "unit": "",   "status": vix_stat,   "color": vix_color, "delta": "LIVE"},
        {"label": "US 10Y Treasury Yield",       "value": us10y_val,  "unit": "%",  "status": us10y_stat, "color": us10y_color, "delta": "LIVE"},
        {"label": "Brent Crude Oil",             "value": live_data.get('BRENT', 84.50), "unit": "$",  "status": "TRACKING",   "color": "#10b981", "delta": "LIVE"},
        {"label": "USD/EUR Exchange Rate",       "value": live_data.get('EUR_USD', 1.082), "unit": "",   "status": "TRACKING",   "color": "#10b981", "delta": "LIVE"},
        {"label": "US CPI (YoY Inflation)",      "value": 3.4,   "unit": "%",  "status": "ELEVATED", "color": "#f59e0b", "delta": "-0.1"},
        {"label": "Yield Curve Slope (10Y-2Y)",  "value": -0.38, "unit": "%",  "status": "CRITICAL", "color": "#ef4444", "delta": "-0.05"},
        {"label": "Global Credit Spread (HY)",   "value": 382,   "unit": "bps","status": "ELEVATED", "color": "#f59e0b", "delta": "+12"},
        {"label": "US Unemployment Rate",        "value": 3.9,   "unit": "%",  "status": "STABLE",   "color": "#10b981", "delta": "+0.1"},
    ]

    # ── Render indicator cards in a 4-column grid ─────────────────────────────
    cols = st.columns(4)
    for i, ind in enumerate(indicators):
        col = cols[i % 4]
        with col:
            val_str = f"{ind['unit']}{ind['value']}" if ind["unit"] == "$" else f"{ind['value']}{ind['unit']}"
            st.markdown(f"""
            <div class="crisis-indicator-card" style="--status-color:{ind['color']};">
                <div class="crisis-indicator-label">{ind['label']}</div>
                <div class="crisis-indicator-value">{val_str}</div>
                <div class="crisis-indicator-status">
                    <span class="crisis-indicator-status-tag">{ind['status']}</span>
                    <span class="crisis-indicator-delta">{ind['delta']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Yield curve visualisation (Remains unchanged) ─────────────────────────
    st.markdown("<div class='hud-section-label'>US TREASURY YIELD CURVE</div>", unsafe_allow_html=True)
    maturities  = ["1M",  "3M",  "6M",  "1Y",  "2Y",  "5Y",  "10Y", "20Y", "30Y"]
    yields_pct  = [5.30,  5.32,  5.28,  5.10,  4.67,  4.35,  4.12,  4.42,  4.20]

    fig_yc = go.Figure()
    fig_yc.add_trace(go.Scatter(
        x=maturities, y=yields_pct, mode="lines+markers",
        line=dict(color="rgba(100,155,255,0.75)", width=2),
        marker=dict(size=5, color="rgba(120,175,255,0.90)", line=dict(width=1, color="rgba(80,130,220,0.60)")),
        fill="tozeroy", fillcolor="rgba(80,120,220,0.06)",
        hovertemplate="<b>%{x}</b><br>Yield: %{y:.2f}%<extra></extra>"
    ))
    fig_yc.update_layout(
        height=260, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono", color="rgba(160,185,235,0.65)", size=10),
        xaxis=dict(showgrid=False, showline=True, linecolor="rgba(100,130,220,0.15)", tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor="rgba(100,130,220,0.07)", showline=False, ticksuffix="%", tickfont=dict(size=9)),
    )
    st.plotly_chart(fig_yc, use_container_width=True)

    # ── System status footer ───────────────────────────────────────────────────
    st.markdown("<div class='hud-section-label'>SYSTEM STATUS</div>", unsafe_allow_html=True)
    st.info("Financial crisis monitoring active. Navigate to Prediction Terminal to run isolated economy stress tests.")

def render_data_feed_panel(latest_year: int, future_year: int):
    """Render the DATA FEED LOCKED status as a cinematic HUD panel."""
    st.markdown(f"""
    <div class="pt-data-feed">
        <div class="pt-data-feed-dot"></div>
        <div>
            <div class="pt-data-feed-label">Data Feed Locked</div>
            <div class="pt-data-feed-body">
                Using <strong style="color:rgba(140,160,255,0.90);">{latest_year}</strong> closing
                data as the base vector for the
                <strong style="color:rgba(140,160,255,0.90);">{future_year}</strong> projection.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_slider_section_label():
    """Render the Economic Health Sliders section heading in HUD style."""
    st.markdown(
        "<div class='hud-section-label' style='margin-top:0.6rem;'>Economic Health Telemetry — Adjust to Test Scenarios</div>",
        unsafe_allow_html=True
    )

def jump_to_terminal(selected_country):
    """Callback executed BEFORE rerun starts."""
    st.session_state.target_country = selected_country
    st.session_state.nav_radio = "2 ▸ Prediction Terminal (Diagnostics)"


def render_threat_matrix(top_risks):
    """Renders the top 3 highest risk economies in glowing HUD cards with diagnostic buttons."""
    st.markdown(
        "<div class='hud-section-label' style='margin-top: 1rem;'>ACTIVE THREAT MATRIX: CRITICAL WATCHLIST</div>", 
        unsafe_allow_html=True
    )

    cols = st.columns(3)
    for i, (index, row) in enumerate(top_risks.iterrows()):
        country = row['country']
        risk = row['Risk Score']
        
        # Determine color based on risk level
        if risk >= 60:
            color, glow = "#ef4444", "rgba(239, 68, 68, 0.4)"
        elif risk >= 30:
            color, glow = "#f59e0b", "rgba(245, 158, 11, 0.4)"
        else:
            color, glow = "#10b981", "rgba(16, 185, 129, 0.4)"
            
        with cols[i]:
            st.markdown(f"""
            <div style="background: rgba(15, 20, 35, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); border-top: 4px solid {color}; padding: 18px; border-radius: 10px; box-shadow: 0 10px 20px rgba(0,0,0,0.5), 0 0 15px {glow}; margin-bottom: 10px;">
                <div style="font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: {color}; letter-spacing: 2px;">PRIORITY TARGET {i+1}</div>
                <div style="font-family: 'Inter', sans-serif; font-size: 24px; font-weight: 700; color: white; margin: 8px 0 4px 0;">{country}</div>
                <div style="font-family: 'IBM Plex Mono', monospace; font-size: 16px; color: {color}; font-weight: 600;">{risk:.2f}% SYSTEMIC RISK</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Pass jump_to_terminal directly to on_click (DO NOT use 'if st.button(...)')
            st.button(
                f"⚡ DIAGNOSE {country}", 
                key=f"jump_{country}", 
                use_container_width=True,
                on_click=jump_to_terminal,
                args=(country,)
            )