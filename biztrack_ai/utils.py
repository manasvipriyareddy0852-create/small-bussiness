"""
Utility functions for BizTrack AI
Handles theming, formatting, and helper functions
"""

import pandas as pd
from datetime import datetime

def format_currency(amount):
    """Format number as currency"""
    if amount is None:
        return "$0.00"
    return f"${amount:,.2f}"

def format_number(num):
    """Format number with commas"""
    if num is None:
        return "0"
    return f"{num:,}"

def format_percentage(value):
    """Format as percentage"""
    if value is None:
        return "0%"
    return f"{value:.1f}%"

def format_date(date_str):
    """Format date string"""
    if date_str is None:
        return ""
    try:
        if isinstance(date_str, str):
            return datetime.fromisoformat(date_str.replace('Z', '')).strftime('%Y-%m-%d %H:%M')
        return date_str.strftime('%Y-%m-%d %H:%M')
    except:
        return str(date_str)

def get_time_ago(timestamp):
    """Get human-readable time ago"""
    if timestamp is None:
        return "Unknown"

    try:
        if isinstance(timestamp, str):
            dt = datetime.fromisoformat(timestamp.replace('Z', ''))
        else:
            dt = timestamp

        now = datetime.now()
        diff = now - dt

        if diff.days > 365:
            return f"{diff.days // 365}y ago"
        elif diff.days > 30:
            return f"{diff.days // 30}mo ago"
        elif diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "Just now"
    except:
        return str(timestamp)

# ---------------------------------------------------------------------------
# Premium Design System
# ---------------------------------------------------------------------------

_COMMON_CSS = """
<style>
    /* ===== Google Font ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ===== Keyframes ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 8px rgba(99,102,241,.15); }
        50%      { box-shadow: 0 0 20px rgba(99,102,241,.30); }
    }
    @keyframes gradientSlide {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%      { transform: translateY(-6px); }
    }

    /* ===== Global Reset ===== */
    *, *::before, *::after { box-sizing: border-box; }

    html, body, .stApp,
    .stApp [data-testid="stAppViewContainer"],
    .stApp [data-testid="stHeader"],
    .stApp header {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
    .stDeployButton { display: none !important; }

    /* ===== Custom Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(99,102,241,.25);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,.45); }

    /* ===== Responsive — Tablet (≤1024px) ===== */
    @media screen and (max-width: 1024px) {
        .block-container {
            padding-left: 16px !important;
            padding-right: 16px !important;
            max-width: 100% !important;
        }
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.25rem !important; }
        [data-testid="metric-container"] {
            padding: 16px 14px;
        }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-size: 22px !important;
        }
    }

    /* ===== Responsive — Mobile (≤768px) ===== */
    @media screen and (max-width: 768px) {
        .block-container {
            padding-left: 12px !important;
            padding-right: 12px !important;
            padding-top: 16px !important;
        }
        h1 { font-size: 1.35rem !important; }
        h2 { font-size: 1.1rem !important; }
        h3 { font-size: 1rem !important; }

        /* Stack columns vertically */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        /* Metric cards - 2-up grid on mobile */
        [data-testid="metric-container"] {
            padding: 14px 12px;
            border-radius: 12px;
        }
        [data-testid="metric-container"] label {
            font-size: 10px !important;
        }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-size: 18px !important;
        }

        /* Buttons — touch-friendly */
        .stButton > button {
            padding: 12px 20px !important;
            font-size: 14px !important;
            min-height: 44px;
        }

        /* Form inputs — touch-friendly */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {
            padding: 14px 14px !important;
            font-size: 16px !important;  /* prevents iOS zoom on focus */
            min-height: 44px;
        }

        /* Tabs — scroll on small screens */
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
        }
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 18px !important;
            font-size: 13px !important;
            white-space: nowrap;
        }

        /* Sidebar — overlay on mobile */
        section[data-testid="stSidebar"] {
            min-width: 260px !important;
            max-width: 280px !important;
        }
        section[data-testid="stSidebar"][aria-expanded="false"] {
            margin-left: -280px !important;
        }

        /* Form containers */
        [data-testid="stForm"] {
            padding: 18px 14px !important;
            border-radius: 14px;
        }

        /* Dataframes — horizontal scroll */
        .stDataFrame > div {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
        }

        /* Download buttons */
        .stDownloadButton > button {
            padding: 12px 16px !important;
            font-size: 13px !important;
        }
    }

    /* ===== Responsive — Small Mobile (≤480px) ===== */
    @media screen and (max-width: 480px) {
        .block-container {
            padding-left: 8px !important;
            padding-right: 8px !important;
        }
        h1 { font-size: 1.2rem !important; }
        h2 { font-size: 1rem !important; }

        [data-testid="metric-container"] {
            padding: 12px 10px;
        }
        [data-testid="metric-container"] [data-testid="stMetricValue"] {
            font-size: 16px !important;
        }
        [data-testid="metric-container"] label {
            font-size: 9px !important;
            letter-spacing: 0.04em !important;
        }

        /* Tabs — compact */
        .stTabs [data-baseweb="tab"] {
            padding: 8px 14px !important;
            font-size: 12px !important;
        }
    }
</style>
"""

LIGHT_THEME = _COMMON_CSS + """
<style>
    /* ===== App Background ===== */
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #faf5ff 35%, #fef3f2 65%, #f0fdf4 100%);
        background-attachment: fixed;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #3730a3 100%) !important;
        border-right: 1px solid rgba(255,255,255,.08);
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #e0e7ff !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,.1) !important;
    }
    /* Sidebar button */
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,.08) !important;
        border: 1px solid rgba(255,255,255,.15) !important;
        color: #e0e7ff !important;
        backdrop-filter: blur(8px);
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,.15) !important;
        border-color: rgba(255,255,255,.25) !important;
        transform: translateY(-1px);
    }

    /* ===== Typography ===== */
    h1 {
        color: #1e1b4b !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        font-size: 2rem !important;
    }
    h2 {
        color: #312e81 !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    h3 {
        color: #3730a3 !important;
        font-weight: 600 !important;
    }
    p, span, label, .stMarkdown {
        color: #374151 !important;
        line-height: 1.6;
    }

    /* ===== Metric Cards ===== */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,.72);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255,255,255,.85);
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow:
            0 1px 3px rgba(0,0,0,.04),
            0 4px 12px rgba(0,0,0,.06);
        transition: all .3s cubic-bezier(.4,0,.2,1);
        animation: fadeInUp .5s ease-out both;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow:
            0 8px 24px rgba(99,102,241,.12),
            0 2px 8px rgba(0,0,0,.06);
    }
    [data-testid="metric-container"] label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #6366f1 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #1e1b4b !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* ===== Buttons ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 28px !important;
        letter-spacing: 0.02em;
        transition: all .3s cubic-bezier(.4,0,.2,1) !important;
        box-shadow: 0 2px 8px rgba(99,102,241,.25);
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,.35) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    /* Primary variant */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        box-shadow: 0 2px 8px rgba(16,185,129,.25);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(16,185,129,.35) !important;
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    }

    /* ===== Form Inputs ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,.7) !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
        transition: all .25s ease !important;
        color: #1e1b4b !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
        background: white !important;
    }
    /* Select boxes */
    .stSelectbox > div > div {
        border-radius: 12px !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(255,255,255,.7) !important;
        border: 1.5px solid #e5e7eb !important;
        border-radius: 12px !important;
        transition: all .25s ease !important;
    }
    .stSelectbox [data-baseweb="select"] > div:hover,
    .stSelectbox [data-baseweb="select"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
    }

    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(255,255,255,.5);
        border-radius: 14px;
        padding: 4px;
        border: 1px solid rgba(0,0,0,.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #6b7280 !important;
        transition: all .25s ease !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #4f46e5 !important;
        background: rgba(99,102,241,.06) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(99,102,241,.3);
    }
    /* Hide tab underline */
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ===== Dataframes ===== */
    .stDataFrame {
        border-radius: 14px !important;
        overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,.06);
        border: 1px solid rgba(0,0,0,.06) !important;
    }

    /* ===== Alert Boxes ===== */
    .stAlert {
        border-radius: 12px !important;
        border-left-width: 4px !important;
        font-size: 14px !important;
    }

    /* ===== Dividers ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,.2), transparent) !important;
        margin: 24px 0 !important;
    }

    /* ===== Page animations ===== */
    .block-container {
        animation: fadeInUp .4s ease-out;
        max-width: 1200px;
    }

    /* ===== Download buttons ===== */
    .stDownloadButton > button {
        background: rgba(255,255,255,.65) !important;
        color: #4f46e5 !important;
        border: 1.5px solid #e0e7ff !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all .25s ease !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(99,102,241,.08) !important;
        border-color: #6366f1 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(99,102,241,.15) !important;
    }

    /* ===== Form container ===== */
    [data-testid="stForm"] {
        background: rgba(255,255,255,.55);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,.7);
        border-radius: 18px;
        padding: 28px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,.04);
    }

    /* ===== Checkbox ===== */
    .stCheckbox label span {
        font-weight: 500 !important;
    }

    /* ===== Date inputs ===== */
    .stDateInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid #e5e7eb !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ===== Number input buttons ===== */
    .stNumberInput button {
        background: transparent !important;
        border: none !important;
        color: #6366f1 !important;
    }
</style>
"""

DARK_THEME = _COMMON_CSS + """
<style>
    /* ===== App Background ===== */
    .stApp {
        background: linear-gradient(135deg, #0f0a1a 0%, #13111c 35%, #171321 65%, #0d1117 100%);
        background-attachment: fixed;
        color: #e2e8f0;
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c0a15 0%, #161229 50%, #1a1640 100%) !important;
        border-right: 1px solid rgba(99,102,241,.15);
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #c7d2fe !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(99,102,241,.15) !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: rgba(99,102,241,.1) !important;
        border: 1px solid rgba(99,102,241,.2) !important;
        color: #c7d2fe !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99,102,241,.2) !important;
        border-color: rgba(99,102,241,.35) !important;
        transform: translateY(-1px);
    }

    /* ===== Typography ===== */
    h1 {
        color: #e0e7ff !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        font-size: 2rem !important;
    }
    h2 {
        color: #c7d2fe !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }
    h3 {
        color: #a5b4fc !important;
        font-weight: 600 !important;
    }
    p, span, label, .stMarkdown {
        color: #cbd5e1 !important;
        line-height: 1.6;
    }

    /* ===== Metric Cards ===== */
    [data-testid="metric-container"] {
        background: rgba(30,27,75,.55);
        backdrop-filter: blur(16px) saturate(160%);
        -webkit-backdrop-filter: blur(16px) saturate(160%);
        border: 1px solid rgba(99,102,241,.15);
        border-radius: 16px;
        padding: 22px 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,.25);
        transition: all .3s cubic-bezier(.4,0,.2,1);
        animation: fadeInUp .5s ease-out both;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow:
            0 8px 24px rgba(99,102,241,.2),
            0 0 0 1px rgba(99,102,241,.25);
        border-color: rgba(99,102,241,.3);
    }
    [data-testid="metric-container"] label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #818cf8 !important;
        text-transform: uppercase;
        letter-spacing: 0.08em !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #e0e7ff !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }

    /* ===== Buttons ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 28px !important;
        transition: all .3s cubic-bezier(.4,0,.2,1) !important;
        box-shadow: 0 2px 12px rgba(99,102,241,.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(99,102,241,.45) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        box-shadow: 0 2px 12px rgba(16,185,129,.3);
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 24px rgba(16,185,129,.4) !important;
    }

    /* ===== Form Inputs ===== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30,27,75,.4) !important;
        border: 1.5px solid rgba(99,102,241,.2) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 14px !important;
        font-family: 'Inter', sans-serif !important;
        color: #e0e7ff !important;
        transition: all .25s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
        background: rgba(30,27,75,.6) !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
        background: rgba(30,27,75,.4) !important;
        border: 1.5px solid rgba(99,102,241,.2) !important;
        border-radius: 12px !important;
    }
    .stSelectbox [data-baseweb="select"] > div:hover,
    .stSelectbox [data-baseweb="select"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,.15) !important;
    }

    /* ===== Tabs ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(30,27,75,.35);
        border-radius: 14px;
        padding: 4px;
        border: 1px solid rgba(99,102,241,.1);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #94a3b8 !important;
        transition: all .25s ease !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #a5b4fc !important;
        background: rgba(99,102,241,.08) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        box-shadow: 0 2px 12px rgba(99,102,241,.35);
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ===== Dataframes ===== */
    .stDataFrame {
        border-radius: 14px !important;
        overflow: hidden;
        border: 1px solid rgba(99,102,241,.12) !important;
    }

    /* ===== Alert Boxes ===== */
    .stAlert {
        border-radius: 12px !important;
        border-left-width: 4px !important;
    }

    /* ===== Dividers ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,.25), transparent) !important;
        margin: 24px 0 !important;
    }

    /* ===== Page animations ===== */
    .block-container {
        animation: fadeInUp .4s ease-out;
        max-width: 1200px;
    }

    /* ===== Download buttons ===== */
    .stDownloadButton > button {
        background: rgba(99,102,241,.1) !important;
        color: #a5b4fc !important;
        border: 1.5px solid rgba(99,102,241,.2) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(99,102,241,.2) !important;
        border-color: rgba(99,102,241,.35) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(99,102,241,.2) !important;
    }

    /* ===== Form container ===== */
    [data-testid="stForm"] {
        background: rgba(30,27,75,.35);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(99,102,241,.12);
        border-radius: 18px;
        padding: 28px !important;
    }

    /* ===== Date inputs ===== */
    .stDateInput > div > div > input {
        border-radius: 12px !important;
        border: 1.5px solid rgba(99,102,241,.2) !important;
        background: rgba(30,27,75,.4) !important;
        color: #e0e7ff !important;
    }

    /* ===== Number input buttons ===== */
    .stNumberInput button {
        background: transparent !important;
        border: none !important;
        color: #818cf8 !important;
    }
</style>
"""

def apply_theme(is_dark=False):
    """Apply theme styling"""
    return DARK_THEME if is_dark else LIGHT_THEME

def get_sidebar_navigation():
    """Get sidebar navigation header with branding"""
    return """
<div style="padding: 28px 16px 8px 16px; text-align: center;">
    <div style="
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 56px; height: 56px;
        background: linear-gradient(135deg, #6366f1 0%, #a78bfa 100%);
        border-radius: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(99,102,241,.35);
        font-size: 28px;
    ">📊</div>
    <h1 style="
        color: white !important;
        margin: 0;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.03em;
        font-family: 'Inter', sans-serif;
    ">BizTrack AI</h1>
    <p style="
        color: rgba(199,210,254,.7) !important;
        margin: 6px 0 0 0;
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    ">Smart Inventory & Bookkeeping</p>
    <div style="
        margin-top: 12px;
        display: inline-block;
        padding: 3px 10px;
        background: rgba(99,102,241,.2);
        border: 1px solid rgba(99,102,241,.25);
        border-radius: 20px;
        font-size: 10px;
        color: #a5b4fc;
        font-weight: 600;
    ">v1.0 ✨</div>
</div>
"""

def get_login_hero_html():
    """Get the hero section HTML for the login page"""
    return """
<div style="
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4c1d95 100%);
    border-radius: 24px;
    padding: 48px 36px;
    color: white;
    position: relative;
    overflow: hidden;
    min-height: 480px;
    display: flex;
    flex-direction: column;
    justify-content: center;
">
    <!-- Decorative circles -->
    <div style="
        position: absolute; top: -40px; right: -40px;
        width: 160px; height: 160px;
        background: rgba(99,102,241,.15);
        border-radius: 50%;
    "></div>
    <div style="
        position: absolute; bottom: -60px; left: -30px;
        width: 200px; height: 200px;
        background: rgba(139,92,246,.1);
        border-radius: 50%;
    "></div>
    <div style="
        position: absolute; top: 50%; right: 20%;
        width: 80px; height: 80px;
        background: rgba(167,139,250,.08);
        border-radius: 50%;
    "></div>

    <!-- Content -->
    <div style="position: relative; z-index: 1;">
        <div style="
            display: inline-flex; align-items: center; justify-content: center;
            width: 64px; height: 64px;
            background: linear-gradient(135deg, #6366f1, #a78bfa);
            border-radius: 18px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(99,102,241,.4);
            font-size: 32px;
        ">📊</div>

        <h1 style="
            font-size: 36px;
            font-weight: 900;
            margin: 0 0 8px 0;
            letter-spacing: -0.04em;
            color: white !important;
            line-height: 1.1;
            font-family: 'Inter', sans-serif;
        ">BizTrack AI</h1>

        <p style="
            color: rgba(199,210,254,.85) !important;
            font-size: 16px;
            font-weight: 400;
            margin: 0 0 32px 0;
            line-height: 1.5;
        ">Smart Inventory & Bookkeeping<br>for Small Businesses</p>

        <div style="display: flex; flex-direction: column; gap: 16px;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="
                    width: 40px; height: 40px;
                    background: rgba(99,102,241,.2);
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 18px; flex-shrink: 0;
                ">📦</div>
                <div>
                    <p style="color: white !important; font-weight: 600; margin: 0; font-size: 14px;">
                        Inventory Management</p>
                    <p style="color: rgba(199,210,254,.6) !important; margin: 0; font-size: 12px;">
                        Track stock, set reorder alerts</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="
                    width: 40px; height: 40px;
                    background: rgba(16,185,129,.2);
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 18px; flex-shrink: 0;
                ">💳</div>
                <div>
                    <p style="color: white !important; font-weight: 600; margin: 0; font-size: 14px;">
                        Sales & Expense Tracking</p>
                    <p style="color: rgba(199,210,254,.6) !important; margin: 0; font-size: 12px;">
                        Real-time revenue & cost insights</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="
                    width: 40px; height: 40px;
                    background: rgba(244,114,182,.2);
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 18px; flex-shrink: 0;
                ">🔮</div>
                <div>
                    <p style="color: white !important; font-weight: 600; margin: 0; font-size: 14px;">
                        AI-Powered Forecasting</p>
                    <p style="color: rgba(199,210,254,.6) !important; margin: 0; font-size: 12px;">
                        Demand prediction & smart restocking</p>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div style="
                    width: 40px; height: 40px;
                    background: rgba(251,191,36,.2);
                    border-radius: 12px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 18px; flex-shrink: 0;
                ">📊</div>
                <div>
                    <p style="color: white !important; font-weight: 600; margin: 0; font-size: 14px;">
                        Reports & Analytics</p>
                    <p style="color: rgba(199,210,254,.6) !important; margin: 0; font-size: 12px;">
                        Export CSV/Excel, profit trends</p>
                </div>
            </div>
        </div>
    </div>
</div>
"""

def get_welcome_banner(user_name):
    """Get a styled welcome banner for the dashboard"""
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good Morning"
        icon = "☀️"
    elif hour < 17:
        greeting = "Good Afternoon"
        icon = "🌤️"
    else:
        greeting = "Good Evening"
        icon = "🌙"

    return f"""
<div style="
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
    border-radius: 20px;
    padding: 32px 36px;
    color: white;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(30,27,75,.25);
">
    <div style="
        position: absolute; top: -30px; right: -20px;
        width: 120px; height: 120px;
        background: rgba(99,102,241,.12);
        border-radius: 50%;
    "></div>
    <div style="
        position: absolute; bottom: -40px; right: 80px;
        width: 80px; height: 80px;
        background: rgba(139,92,246,.1);
        border-radius: 50%;
    "></div>
    <p style="
        font-size: 14px;
        color: rgba(199,210,254,.7) !important;
        margin: 0 0 4px 0;
        font-weight: 500;
    ">{icon} {greeting}</p>
    <h1 style="
        font-size: 28px;
        font-weight: 800;
        margin: 0;
        color: white !important;
        letter-spacing: -0.03em;
    ">{user_name}</h1>
    <p style="
        color: rgba(199,210,254,.6) !important;
        margin: 8px 0 0 0;
        font-size: 14px;
    ">Here's your business overview for today.</p>
</div>
"""

def get_section_header(icon, title, subtitle=""):
    """Get a styled section header"""
    sub_html = f'<p style="color: #9ca3af; margin: 4px 0 0 0; font-size: 13px;">{subtitle}</p>' if subtitle else ""
    return f"""
<div style="margin-bottom: 16px;">
    <h2 style="margin: 0; font-size: 20px;">
        <span style="margin-right: 8px;">{icon}</span>{title}
    </h2>
    {sub_html}
</div>
"""

def get_user_card(name, role):
    """Get styled user card for sidebar"""
    role_color = "#10b981" if role == "owner" else "#6366f1"
    role_bg = "rgba(16,185,129,.15)" if role == "owner" else "rgba(99,102,241,.15)"
    return f"""
<div style="
    padding: 14px 16px;
    background: rgba(255,255,255,.06);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 14px;
    margin-top: 16px;
">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="
            width: 38px; height: 38px;
            background: linear-gradient(135deg, #6366f1, #a78bfa);
            border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-size: 16px; font-weight: 700; color: white;
            flex-shrink: 0;
        ">{name[0].upper()}</div>
        <div>
            <p style="color: white !important; margin: 0; font-weight: 600; font-size: 14px;">
                {name}</p>
            <span style="
                display: inline-block;
                margin-top: 4px;
                padding: 2px 10px;
                background: {role_bg};
                border-radius: 20px;
                font-size: 11px;
                color: {role_color} !important;
                font-weight: 600;
            ">{role.title()}</span>
        </div>
    </div>
</div>
"""

def get_chart_colors():
    """Get premium chart color palette"""
    return {
        'primary': '#6366f1',
        'secondary': '#8b5cf6',
        'success': '#10b981',
        'danger': '#ef4444',
        'warning': '#f59e0b',
        'info': '#06b6d4',
        'sequence': ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe',
                      '#10b981', '#34d399', '#6ee7b7'],
        'revenue_color': '#10b981',
        'expense_color': '#ef4444',
        'bar_colorscale': 'Purples',
        'pie_colors': ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#818cf8',
                        '#10b981', '#34d399', '#f59e0b', '#f472b6', '#06b6d4'],
    }
