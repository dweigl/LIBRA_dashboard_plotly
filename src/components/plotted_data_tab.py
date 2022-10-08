from dash import Dash, dcc, html
from . import ids

from . import line_plot, line_plot_2


def render(app: Dash) -> dcc.Tab:
    return dcc.Tab(
        id=ids.PLOTTED_DATA_TAB,
        label="Plotted data",
        children=[
            html.H4("Plotted data.", style=dict(
                textAlign="center", fontWeight="bold", color="#047cc4")),
            html.Div(
                className="plot-and-dropdown-container",
                children=[
                    line_plot.render(app),
                    line_plot_2.render(app)
                ]
            ),
        ]
    )
