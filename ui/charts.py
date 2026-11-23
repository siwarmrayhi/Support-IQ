"""Graphiques Plotly du tableau de bord."""

import plotly.graph_objects as go

TRANSPARENT = "rgba(0,0,0,0)"


def auto_rate_gauge(rate: int) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=rate,
            number={"suffix": " %", "font": {"size": 42, "color": "#0f172a"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#94a3b8"},
                "bar": {"color": "#2563eb", "thickness": 0.32},
                "bgcolor": "#e2e8f0",
                "borderwidth": 0,
            },
        )
    )
    fig.update_layout(
        height=240, margin={"l": 30, "r": 30, "t": 30, "b": 10}, paper_bgcolor=TRANSPARENT
    )
    return fig


def status_donut(stats: dict) -> go.Figure:
    fig = go.Figure(
        go.Pie(
            labels=["Terminé", "En cours", "À traiter"],
            values=[stats["resolved"], stats["in_progress"], stats["pending"]],
            hole=0.65,
            sort=False,
            textinfo="value",
            marker={"colors": ["#22c55e", "#38bdf8", "#f97316"]},
        )
    )
    fig.update_layout(
        height=240,
        margin={"l": 10, "r": 10, "t": 10, "b": 10},
        paper_bgcolor=TRANSPARENT,
        legend={"orientation": "h", "y": -0.05},
    )
    return fig