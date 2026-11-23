"""Thème visuel clair : styles CSS, pastilles de statut, cartes d'indicateurs."""

import html

import streamlit as st

STATUS_STYLES = {
    "resolved": ("Terminé", "chip-green"),
    "in_progress": ("En cours", "chip-blue"),
    "pending_review": ("À traiter", "chip-orange"),
}

BRAND_HTML = (
    '<div class="brand"><div class="brand-badge">S</div>'
    '<div><div class="brand-name">SupportIQ</div>'
    '<div class="brand-sub">Copilote de support client</div></div></div>'
)

_CSS = """
<style>
.stApp { background: #f4f7fb; }
[data-testid="stMainBlockContainer"], .block-container { padding-top: 2.2rem; max-width: 1200px; }
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e2e8f0; }
header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

.brand { display: flex; align-items: center; gap: .7rem; }
.brand-badge {
    width: 40px; height: 40px; border-radius: 12px; color: #ffffff;
    font-size: 1.3rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    box-shadow: 0 6px 14px rgba(37, 99, 235, .35);
}
.brand-name { font-size: 1.25rem; font-weight: 800; color: #0f172a; line-height: 1.1; }
.brand-sub { font-size: .75rem; color: #64748b; }

.page-title { font-size: 1.9rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; }
.page-sub { color: #64748b; margin-bottom: 1.2rem; }

/* Navigation latérale en boutons */
[data-testid="stSidebar"] .stButton button,
[data-testid="stSidebar"] [data-testid="stButton"] button {
    width: 100%; justify-content: flex-start;
    padding: .65rem .9rem; border-radius: 12px; font-weight: 600; margin-bottom: .15rem;
}
[data-testid="stSidebar"] button[kind="secondary"],
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] {
    background: #f8fafc; border: 1px solid #e2e8f0; color: #334155;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover,
[data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover {
    background: #eff6ff; border-color: #93c5fd; color: #1d4ed8;
}
[data-testid="stSidebar"] button[kind="primary"],
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #2563eb, #0ea5e9); border: none; color: #ffffff;
    box-shadow: 0 6px 16px rgba(37, 99, 235, .28);
}

/* Pastilles de statut */
.chip {
    display: inline-block; padding: 2px 12px; border-radius: 999px;
    font-size: .8rem; font-weight: 600; border: 1px solid transparent;
}
.chip-green  { background: #dcfce7; color: #15803d; border-color: #86efac; }
.chip-blue   { background: #dbeafe; color: #1d4ed8; border-color: #93c5fd; }
.chip-orange { background: #ffedd5; color: #c2410c; border-color: #fdba74; }

/* Cartes d'indicateurs */
.kpi {
    display: flex; align-items: center; gap: 1rem;
    background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1rem 1.2rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, .04), 0 8px 24px rgba(15, 23, 42, .05);
}
.kpi-icon {
    width: 46px; height: 46px; border-radius: 14px; font-size: 1.4rem;
    display: flex; align-items: center; justify-content: center;
}
.kpi-blue .kpi-icon { background: #dbeafe; }
.kpi-green .kpi-icon { background: #dcfce7; }
.kpi-orange .kpi-icon { background: #ffedd5; }
.kpi-teal .kpi-icon { background: #cffafe; }
.kpi-label { font-size: .8rem; color: #64748b; font-weight: 600; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #0f172a; line-height: 1.1; }
</style>
"""


def apply_theme() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def status_label(status: str) -> str:
    return STATUS_STYLES.get(status, (status, ""))[0]


def chip(status: str) -> str:
    label, css_class = STATUS_STYLES.get(status, (status, "chip-blue"))
    return f'<span class="chip {css_class}">{html.escape(label)}</span>'


def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(
        f'<div class="page-title">{html.escape(title)}</div>'
        f'<div class="page-sub">{html.escape(subtitle)}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: int, icon: str, tone: str) -> str:
    return (
        f'<div class="kpi kpi-{tone}">'
        f'<div class="kpi-icon">{icon}</div>'
        f'<div><div class="kpi-label">{html.escape(label)}</div>'
        f'<div class="kpi-value">{int(value)}</div></div></div>'
    )
    
_CELL_STYLES = {
    "Terminé": "background-color: #dcfce7; color: #15803d; font-weight: 600",
    "En cours": "background-color: #dbeafe; color: #1d4ed8; font-weight: 600",
    "À traiter": "background-color: #ffedd5; color: #c2410c; font-weight: 600",
}


def status_cell_style(label: str) -> str:
    return _CELL_STYLES.get(label, "")
