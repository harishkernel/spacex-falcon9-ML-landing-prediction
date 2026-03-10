"""
SpaceX Falcon 9 First Stage Landing Prediction — Interactive Dashboard
=======================================================================
Author : Harish M
Project: IBM Data Science Professional Certificate — Capstone

Dashboard features:
  • Launch site dropdown  — filter all charts by site
  • Pie chart             — success vs. failure distribution per site
  • Payload range slider  — filter scatter plot by payload mass
  • Scatter plot          — payload vs. outcome coloured by booster version
"""

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import os
import pandas as pd
import dash
from dash import html, dcc          # dash >= 2.0 (replaces deprecated packages)
from dash.dependencies import Input, Output
import plotly.express as px

# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------
# Prefer a local CSV; fall back to IBM Skills Network hosted file.
_LOCAL_CSV = os.path.join(os.path.dirname(__file__), "spacex_launch_dash.csv")
_REMOTE_CSV = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
)

if os.path.exists(_LOCAL_CSV):
    spacex_df = pd.read_csv(_LOCAL_CSV)
else:
    print("[INFO] Local CSV not found — downloading from IBM Skills Network ...")
    spacex_df = pd.read_csv(_REMOTE_CSV)

max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Derive unique launch sites for the dropdown
launch_sites = sorted(spacex_df["Launch Site"].unique().tolist())
site_options = [{"label": "All Sites", "value": "ALL"}] + [
    {"label": site, "value": site} for site in launch_sites
]

# ---------------------------------------------------------------------------
# App Initialisation
# ---------------------------------------------------------------------------
app = dash.Dash(__name__)
app.title = "SpaceX Launch Records"

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        # Header
        html.H1(
            "SpaceX Falcon 9 — Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 36},
        ),
        html.P(
            "Explore launch outcomes, success rates, and payload correlations "
            "across all SpaceX Falcon 9 launch sites.",
            style={"textAlign": "center", "color": "#6c757d", "fontSize": 16},
        ),
        html.Hr(),

        # Task 1: Launch Site Dropdown
        html.Div(
            [
                html.Label("Select Launch Site:", style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id="site-dropdown",
                    options=site_options,
                    value="ALL",
                    placeholder="Select a launch site ...",
                    searchable=True,
                    clearable=False,
                    style={"maxWidth": "500px"},
                ),
            ],
            style={"padding": "10px 20px"},
        ),
        html.Br(),

        # Task 2: Pie Chart
        html.Div(
            dcc.Graph(id="success-pie-chart"),
            style={"padding": "0 20px"},
        ),
        html.Br(),

        # Task 3: Payload Range Slider
        html.Div(
            [
                html.Label("Payload Range (kg):", style={"fontWeight": "bold"}),
                dcc.RangeSlider(
                    id="payload-slider",
                    min=0,
                    max=10000,
                    step=1000,
                    marks={i: f"{i:,}" for i in range(0, 11000, 2500)},
                    value=[min_payload, max_payload],
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={"padding": "10px 40px"},
        ),
        html.Br(),

        # Task 4: Scatter Chart
        html.Div(
            dcc.Graph(id="success-payload-scatter-chart"),
            style={"padding": "0 20px"},
        ),

        # Footer
        html.Hr(),
        html.P(
            "IBM Data Science Capstone — Harish M",
            style={"textAlign": "center", "color": "#aaa", "fontSize": 13},
        ),
    ]
)


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def render_pie_chart(selected_site):
    """
    Return a pie chart figure.
    - ALL sites : proportion of successful launches contributed by each site.
    - One site  : success vs. failure count for that site.
    """
    if selected_site == "ALL":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Successful Launches by Site",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        outcome_counts = (
            site_df.groupby("class")
            .size()
            .reset_index(name="count")
        )
        outcome_counts["Outcome"] = outcome_counts["class"].map(
            {1: "Success", 0: "Failure"}
        )
        fig = px.pie(
            outcome_counts,
            values="count",
            names="Outcome",
            title=f"Launch Outcomes — {selected_site}",
            color="Outcome",
            color_discrete_map={"Success": "#2ecc71", "Failure": "#e74c3c"},
        )

    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin={"t": 60, "b": 20})
    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def render_scatter_chart(selected_site, payload_range):
    """
    Return a scatter chart of Payload Mass (kg) vs. landing class.
    Points are coloured by Booster Version Category.
    Filtered by the payload range slider and optional site selection.
    """
    low, high = payload_range
    filtered = spacex_df[spacex_df["Payload Mass (kg)"].between(low, high)]

    if selected_site != "ALL":
        filtered = filtered[filtered["Launch Site"] == selected_site]
        title = f"Payload vs. Outcome — {selected_site}"
    else:
        title = "Payload vs. Outcome — All Sites"

    fig = px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=title,
        labels={"class": "Landing Outcome (1 = Success)"},
        hover_data=["Launch Site", "Payload Mass (kg)", "Booster Version Category"],
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_yaxes(tickvals=[0, 1], ticktext=["Failure", "Success"])
    fig.update_layout(margin={"t": 60, "b": 20})
    return fig


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
