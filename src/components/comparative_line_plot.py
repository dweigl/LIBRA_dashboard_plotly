from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from typing import Any
from src.plotting_functions.plotting_functions_plotly import make_comparative_lineplots
from src.plotting_functions.plot_parameters import LinePlotParameters, StyleParameters
from . import ids
import pandas as pd

def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.COMPARATIVE_LINE_PLOT, "children"),
        Input(ids.STELLA_RUN_NAMES_DROPDOWN, "value"),
        Input(ids.MODULE_DROPDOWN, "value"),
        Input(ids.VARIABLE_DROPDOWN, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_1, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_2, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_3, "value"),
        Input(ids.TITLE_INPUT, "value"),
        Input(ids.YLABEL_INPUT, "value"),
        Input(ids.MAX_YVAL_INPUT, "value"),
        Input(ids.DECIMAL_POINT_RADIOITEMS, "value"),
        Input(ids.EXOGENOUS_INPUT_RADIOITEMS, "value"),
        State(ids.DATA_STORAGE, "data")
    )
    def update_comparative_line_plot(
        stella_run_names: list[str],
        module: str,
        variable: str,
        array_val_1: str,
        array_val_2: str,
        array_val_3: str,
        title: str,
        y_label: str,
        max_yval: float,
        decimal: bool,
        is_exogenous_input: bool,
        data: dict[Any],
    ) -> html.Div:
        placeholder_title = f"{module}.{variable}"+"["+ \
            ", ".join([val for val in [array_val_1, array_val_2, array_val_3] if val != "None"]) + "]"
        placeholder_ylabel = f"{module}.{variable}"

        try:
            plot_params = LinePlotParameters(
                module=module,
                variable=variable,
                array_vals=[val for val in [array_val_1, array_val_2, array_val_3] if val != "None"],
                title=placeholder_title if title != placeholder_title else title,
                y_label=placeholder_ylabel if y_label != placeholder_ylabel else y_label,
                max_yval=max_yval if max_yval != 0 else None,
                decimal=decimal,
                is_exogenous_input=is_exogenous_input
            )
            df = pd.DataFrame.from_records(data, index="Years")
            style_params = StyleParameters(stella_run_names=stella_run_names, compare=False)
            
            fig = make_comparative_lineplots(df, plot_params, style_params)
            return html.Div(
                children=[
                    html.Div(className="comparative-line-plot", children=[dcc.Graph(figure=fig)]),
                ],
                id=ids.COMPARATIVE_LINE_PLOT)
        except Exception as e:
            print(e)
            return html.Div([str(e)])
        
    return html.Div(id=ids.COMPARATIVE_LINE_PLOT)