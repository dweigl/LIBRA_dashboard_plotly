from dash import Dash, html
from src.components import (
    file_uploader,
    stella_run_names_dropdown,
    module_dropdown,
    variable_dropdown,
    arrayval_dropdowns, 
    title_and_ylabel_input, 
    line_plot,
    comparative_line_plot,
    module_dropdown_2,
    variable_dropdown_2,
    arrayval_dropdowns_2, 
    title_and_ylabel_input_2, 
    line_plot_2,
    comparative_line_plot_2,
    tag_input
)

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div", 
        children=[
            html.H1(app.title, style=dict(textAlign="center", fontWeight="bold")),
            html.Hr(),
            file_uploader.render(app),
            stella_run_names_dropdown.render(app),
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
                            title_and_ylabel_input_2.render(app)
                        ]
                    ),
                ]
            ),
            tag_input.render(app),
            html.H4("Plotted data.", style=dict(textAlign="center", fontWeight="bold")),
            html.Div(
                className="plot-and-dropdown-container",
                children=[
                    line_plot.render(app),
                    line_plot_2.render(app)
                ]
            ),
            html.H4("Comparison across scenarios.", style=dict(textAlign="center", fontWeight="bold")),
            html.Div(
                className="comparative-line-plot-container",
                children=[
                    comparative_line_plot.render(app),
                    comparative_line_plot_2.render(app)
                ]
            ),
        ]
    )