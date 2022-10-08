from dash import Dash, dcc, html
from . import ids

from . import comparative_line_plot, comparative_line_plot_2


def render(app: Dash) -> dcc.Tab:
    return dcc.Tab(
        id=ids.COMPARATIVE_LINEPLOT_TAB,
        label="Comparative line plots",
        children=[
            html.Div(
                className="comparative-line-plot-header",
                children=[
                    html.H4("Comparison across scenarios.",
                            style=dict(
                                fontWeight="bold", color="#047cc4")
                            )]
            ),
            html.Div(
                className="comparative-line-plot-container",
                children=[
                    comparative_line_plot.render(app),
                    comparative_line_plot_2.render(app)
                ]
            ),
        ]
    )
