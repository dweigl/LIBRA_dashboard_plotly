from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from datetime import date
from typing import Any
from src.plotting_functions.plotting_functions_plotly import make_comparative_lineplots
from src.plotting_functions.plot_parameters import LinePlotParameters, StyleParameters
from . import ids
import pandas as pd
import re

def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.COMPARATIVE_LINE_PLOT_TWO, "children"),
        Input(ids.STELLA_RUN_NAMES_DROPDOWN, "value"),
        Input(ids.MODULE_DROPDOWN_TWO, "value"),
        Input(ids.VARIABLE_DROPDOWN_TWO, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_TWO_1, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_TWO_2, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_TWO_3, "value"),
        Input(ids.TITLE_INPUT_TWO, "value"),
        Input(ids.YLABEL_INPUT_TWO, "value"),
        Input(ids.MAX_YVAL_INPUT_TWO, "value"),
        Input(ids.DECIMAL_POINT_RADIOITEMS_TWO, "value"),
        Input(ids.EXOGENOUS_INPUT_RADIOITEMS_TWO, "value"),
        Input(ids.SCENARIO_NAME_INPUT, "value"),
        Input(ids.GITHUB_COMMIT_INPUT, "value"),
        State(ids.DATA_STORAGE, "data")
    )
    def update_line_plot(
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
        scenario_name: str,
        github_commit: str,
        data: dict[Any],
    ) -> html.Div:
        placeholder_title = f"{module}.{variable}"+"["+ \
            ", ".join([val for val in [array_val_1, array_val_2, array_val_3] if val != "None"]) + "]"
        placeholder_ylabel = f"{module}.{variable}"

        tag = None
        if scenario_name and github_commit:
            tag = f"{scenario_name}_{github_commit}_"+re.sub("-", "", str(date.today()))

        try:
            plot_params = LinePlotParameters(
                module=module,
                variable=variable,
                array_vals=[val for val in [array_val_1, array_val_2, array_val_3] if val != "None"],
                title=placeholder_title if title != placeholder_title else title,
                y_label=placeholder_ylabel if y_label != placeholder_ylabel else y_label,
                max_yval=max_yval if max_yval != 0 else None,
                decimal=decimal,
                is_exogenous_input=is_exogenous_input,
                tag=tag if tag else None
            )
            df = pd.DataFrame.from_records(data, index="Years")
            style_params = StyleParameters(stella_run_names=stella_run_names, compare=False)
            
            fig = make_comparative_lineplots(df, plot_params, style_params)
            return html.Div(
                children=[
                    html.Div(
                        className="comparative-line-plot", 
                        children=[
                            dcc.Graph(
                                figure=fig,
                                config=dict(
                                    toImageButtonOptions=dict(
                                        format="png", 
                                        width=325*len(style_params.stella_run_names),
                                        height=400,
                                        scale=3.0)
                            )
                        )]),
                ],
                id=ids.COMPARATIVE_LINE_PLOT_TWO)
        except Exception as e:
            return html.Div([str(e)])
        
    return html.Div(id=ids.COMPARATIVE_LINE_PLOT_TWO)