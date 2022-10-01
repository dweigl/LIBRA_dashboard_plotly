from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Any
from . import ids
from src.data.LIBRAOutputNamesParser import LIBRAOutputNamesParser

import pandas as pd

def render(app: Dash) -> html.Div:

    @app.callback(
        Output(ids.VARIABLE_DROPDOWN_TWO, "options"),
        Output(ids.VARIABLE_DROPDOWN_TWO, "value"),
        Input(ids.MODULE_DROPDOWN_TWO, "value"),
        State(ids.VARIABLE_DICT_STORAGE, "data"),
    )
    def update_variable_dropdown(module: str, variable_dict: dict[str, list[str]]) -> \
        tuple[list[dict[str, str]], str]:
        if module == "None":
            return [dict(value="None", label="None")], "None"
        print()
        try:
            variable_list = variable_dict[module]
        except KeyError:
            variable_list = ["None"]
        return [dict(label=variable, value=variable) for variable in sorted(variable_list)], \
            variable_list[0]

    return html.Div(
        children=[
            html.H6("Select name of LIBRA variable."),
            dcc.Dropdown(
                id=ids.VARIABLE_DROPDOWN_TWO,
                options=[dict(value="None", label="None")],
                value="None"
            ) 
        ]
    )