import os
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "spacex_launch_dash.csv"

df = pd.read_csv(DATA_FILE)
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

df["Resultado"] = df["class"].map({0: "Fallo", 1: "Éxito"})

MIN_PAYLOAD = int(df["Payload Mass (kg)"].min())
MAX_PAYLOAD = int(df["Payload Mass (kg)"].max())
SITES = sorted(df["Launch Site"].unique())

app = Dash(__name__)
server = app.server
app.title = "SpaceX Falcon 9 Dashboard"

CARD_STYLE = {
    "background": "#111827",
    "border": "1px solid #243047",
    "borderRadius": "16px",
    "padding": "18px 20px",
}

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "#070b14",
        "color": "#eef2ff",
        "fontFamily": "Inter, Arial, sans-serif",
        "padding": "28px",
    },
    children=[
        html.Div(
            style={"maxWidth": "1280px", "margin": "0 auto"},
            children=[
                html.Div([
                    html.Div("DATA SCIENCE · SPACEX", style={
                        "fontSize": "12px", "letterSpacing": "0.14em",
                        "color": "#38bdf8", "fontWeight": "700"
                    }),
                    html.H1("Falcon 9 Launch Dashboard", style={
                        "margin": "8px 0 4px", "fontSize": "38px"
                    }),
                    html.P(
                        "Explora los lanzamientos, la tasa de éxito y la relación entre carga útil y aterrizaje.",
                        style={"color": "#94a3b8", "marginTop": "0"},
                    ),
                ], style={"marginBottom": "22px"}),

                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "minmax(220px, 1fr) minmax(280px, 2fr)",
                        "gap": "16px",
                        "marginBottom": "18px",
                    },
                    children=[
                        html.Div([
                            html.Label("Centro de lanzamiento", style={
                                "display": "block", "fontSize": "12px",
                                "color": "#94a3b8", "marginBottom": "8px"
                            }),
                            dcc.Dropdown(
                                id="site-dropdown",
                                options=[{"label": "Todos los centros", "value": "ALL"}]
                                + [{"label": s, "value": s} for s in SITES],
                                value="ALL",
                                clearable=False,
                                style={"color": "#111827"},
                            ),
                        ], style=CARD_STYLE),

                        html.Div([
                            html.Div([
                                html.Label("Rango de carga útil", style={
                                    "fontSize": "12px", "color": "#94a3b8"
                                }),
                                html.Span(id="payload-label", style={
                                    "float": "right", "fontSize": "12px",
                                    "color": "#38bdf8", "fontWeight": "700"
                                }),
                            ]),
                            dcc.RangeSlider(
                                id="payload-slider",
                                min=MIN_PAYLOAD,
                                max=MAX_PAYLOAD,
                                step=250,
                                value=[MIN_PAYLOAD, MAX_PAYLOAD],
                                tooltip={"placement": "bottom", "always_visible": False},
                                marks={
                                    MIN_PAYLOAD: f"{MIN_PAYLOAD:,}",
                                    5000: "5,000",
                                    MAX_PAYLOAD: f"{MAX_PAYLOAD:,}",
                                },
                            ),
                        ], style=CARD_STYLE),
                    ],
                ),

                html.Div(
                    id="metric-cards",
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "repeat(4, 1fr)",
                        "gap": "14px",
                        "marginBottom": "18px",
                    },
                ),

                html.Div(
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "0.85fr 1.35fr",
                        "gap": "18px",
                    },
                    children=[
                        html.Div(
                            dcc.Graph(id="success-pie-chart", config={"displayModeBar": False}),
                            style=CARD_STYLE,
                        ),
                        html.Div(
                            dcc.Graph(id="payload-scatter-chart", config={"displayModeBar": False}),
                            style=CARD_STYLE,
                        ),
                    ],
                ),
            ],
        )
    ],
)


@app.callback(
    Output("metric-cards", "children"),
    Output("success-pie-chart", "figure"),
    Output("payload-scatter-chart", "figure"),
    Output("payload-label", "children"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def update_dashboard(site, payload_range):
    filtered = df[
        (df["Payload Mass (kg)"] >= payload_range[0])
        & (df["Payload Mass (kg)"] <= payload_range[1])
    ].copy()

    if site != "ALL":
        filtered = filtered[filtered["Launch Site"] == site]

    total = len(filtered)
    successes = int(filtered["class"].sum()) if total else 0
    failures = total - successes
    success_rate = (successes / total * 100) if total else 0
    avg_payload = filtered["Payload Mass (kg)"].mean() if total else 0

    metrics = [
        ("LANZAMIENTOS", f"{total}"),
        ("ÉXITOS", f"{successes}"),
        ("TASA DE ÉXITO", f"{success_rate:.1f}%"),
        ("CARGA MEDIA", f"{avg_payload:,.0f} kg"),
    ]
    cards = [
        html.Div([
            html.Div(label, style={
                "fontSize": "11px", "letterSpacing": "0.08em",
                "color": "#94a3b8", "fontWeight": "700"
            }),
            html.Div(value, style={
                "fontSize": "27px", "fontWeight": "800",
                "marginTop": "6px"
            }),
        ], style=CARD_STYLE)
        for label, value in metrics
    ]

    pie = px.pie(
        names=["Éxito", "Fallo"],
        values=[successes, failures],
        hole=0.62,
        title="Resultado de los lanzamientos",
    )
    pie.update_traces(
        marker={"colors": ["#22c55e", "#f97316"]},
        textinfo="percent+label",
    )
    pie.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="#e5e7eb",
        title_font_size=17,
        margin=dict(l=20, r=20, t=55, b=20),
        legend_title_text="",
    )

    scatter = px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="Resultado",
        color="Booster Version Category",
        hover_data=["Launch Site", "Flight Number", "Booster Version"],
        title="Carga útil y resultado del aterrizaje",
        labels={
            "Payload Mass (kg)": "Carga útil (kg)",
            "Resultado": "Resultado",
            "Booster Version Category": "Booster",
        },
    )
    scatter.update_traces(marker={"size": 11, "opacity": 0.82})
    scatter.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="#e5e7eb",
        title_font_size=17,
        margin=dict(l=20, r=20, t=55, b=20),
        legend_title_text="Booster",
    )
    scatter.update_xaxes(gridcolor="#243047")
    scatter.update_yaxes(gridcolor="#243047")

    label = f"{payload_range[0]:,.0f} – {payload_range[1]:,.0f} kg"
    return cards, pie, scatter, label


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
