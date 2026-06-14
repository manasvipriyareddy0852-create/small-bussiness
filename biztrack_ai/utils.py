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

LIGHT_THEME = """
<style>
    /* Main app styling */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e3a5f !important;
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: white !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    [data-testid="metric-container"] label {
        font-size: 14px !important;
        color: #666 !important;
        font-weight: 500 !important;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #1e3a5f !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #1e3a5f;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #2d4a6f;
        box-shadow: 0 4px 12px rgba(30,58,95,0.3);
    }

    /* Primary buttons */
    .stButton button[kind="primary"] {
        background-color: #2ecc71;
    }

    .stButton button[kind="primary"]:hover {
        background-color: #27ae60;
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1e3a5f !important;
        font-weight: 700 !important;
    }

    /* Success message styling */
    .element-container .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 12px;
        border-radius: 4px;
    }

    /* Warning message styling */
    .element-container .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 12px;
        border-radius: 4px;
    }

    /* Error message styling */
    .element-container .stError {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 12px;
        border-radius: 4px;
    }

    /* Info message styling */
    .element-container .stInfo {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 12px;
        border-radius: 4px;
    }

    /* Card styling */
    .insight-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #1e3a5f;
    }

    .insight-card.success {
        border-left-color: #28a745;
    }

    .insight-card.warning {
        border-left-color: #ffc107;
    }

    .insight-card.danger {
        border-left-color: #dc3545;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #e8eef5;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1e3a5f !important;
        color: white !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0f4f8;
        border-radius: 8px;
        font-weight: 600;
    }

    /* Navigation menu */
    .nav-item {
        padding: 12px 16px;
        border-radius: 8px;
        margin: 4px 0;
        transition: all 0.3s ease;
    }

    .nav-item:hover {
        background-color: rgba(255,255,255,0.1);
    }

    .nav-item.active {
        background-color: rgba(255,255,255,0.2);
    }
</style>
"""

DARK_THEME = """
<style>
    /* Main app styling */
    .stApp {
        background-color: #0e1117;
        color: #f0f0f0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
    }

    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #f0f0f0 !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
    }

    [data-testid="metric-container"] label {
        font-size: 14px !important;
        color: #8b949e !important;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #58a6ff !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #30363d;
    }

    .stButton button:hover {
        background-color: #2ea043;
        border: 1px solid #238636;
    }

    /* Dataframes */
    .stDataFrame {
        background-color: #21262d;
    }

    /* Headers */
    h1, h2, h3 {
        color: #f0f6fc !important;
    }

    /* Text */
    .stMarkdown, p, span {
        color: #c9d1d9 !important;
    }

    /* Input fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
    }

    /* Cards */
    .insight-card {
        background: #21262d;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #58a6ff;
    }
</style>
"""

def apply_theme(is_dark=False):
    """Apply theme styling"""
    return DARK_THEME if is_dark else LIGHT_THEME

def get_sidebar_navigation():
    """Get sidebar navigation menu"""
    return """
    <div style="padding: 20px 0;">
        <div style="text-align: center; padding: 20px 0; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-size: 24px;">BizTrack AI</h1>
            <p style="color: #a0aec0; margin: 5px 0 0 0; font-size: 12px;">Smart Inventory & Bookkeeping</p>
        </div>
    </div>
    """
