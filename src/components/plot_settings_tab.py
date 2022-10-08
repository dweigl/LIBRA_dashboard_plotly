from dash import Dash, dcc, html
from . import ids

from . import (
    stella_run_names_dropdown,
    module_dropdown,
    variable_dropdown,
    arrayval_dropdowns,
    title_and_ylabel_input,
    module_dropdown_2,
    variable_dropdown_2,
    arrayval_dropdowns_2,
    title_and_ylabel_input_2,
    tag_input
)


def render(app: Dash) -> dcc.Tab:
    return dcc.Tab(
        id=ids.PLOT_SETTINGS_TAB,
        label="Plot settings",
        children=[
            stella_run_names_dropdown.render(app),
            html.Div(
                className="LIBRA-variable-input-header",
                children=[
                    html.H4("LIBRA variable inputs.",
                            style=dict(
                                fontWeight="bold", color="#047cc4")
                            )]
            ),
            html.Div(
                className="plot-and-dropdown-container",
                children=[
                    html.Div(
                        className="dropdown-container",
                        children=[
                            module_dropdown.render(app),
                            variable_dropdown.render(app),
                            arrayval_dropdowns.render(app),
                            title_and_ylabel_input.render(app)
                        ]
                    ),
                    html.Div(
                        className="dropdown-container",
                        children=[
                            module_dropdown_2.render(app),
                            variable_dropdown_2.render(app),
                            arrayval_dropdowns_2.render(app),
                            title_and_ylabel_input_2.render(
                                app)
                        ]
                    ),
                ]
            ),
            tag_input.render(app)
        ]
    )
