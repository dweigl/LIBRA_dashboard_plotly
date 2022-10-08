from dash import Dash, html, dcc
from src.components import (
    comparative_line_plot_tab,
    file_uploader,
    plot_settings_tab,
    plotted_data_tab
)


def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, style=dict(textAlign="center",
                    fontWeight="bold", color="#047cc4")),
            html.Hr(),
            file_uploader.render(app),
            dcc.Tabs(
                [
                    plotted_data_tab.render(app),
                    comparative_line_plot_tab.render(app),
                    plot_settings_tab.render(app)
                ]
            )
        ]
    )
