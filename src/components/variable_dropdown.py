from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Any
from . import ids
from src.data.LIBRAOutputNamesParser import LIBRAOutputNamesParser

import pandas as pd

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.VARIABLE_DICT_STORAGE, "data"),
        Input(ids.FILE_UPLOAD_BUTTON, "n_clicks"),
        State(ids.DATA_STORAGE, "data")
    )
    def update_variable_dict_storage(_: int, data: dict[Any]) -> dict[str, list[str]]:
        names_parser = LIBRAOutputNamesParser()
        try:
            if not data:
                raise PreventUpdate
                return dict()
            df = pd.DataFrame.from_records(data, index="Years")
            names_parser.parse_names_from_dataframe(df)
        except Exception as e:
            print(e)
            return dict()
        return names_parser.variable_dict

    @app.callback(
        Output(ids.VARIABLE_DROPDOWN, "options"),
        Output(ids.VARIABLE_DROPDOWN, "value"),
        Input(ids.MODULE_DROPDOWN, "value"),
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
                id=ids.VARIABLE_DROPDOWN,
                options=[dict(value="None", label="None")],
                value="None"
            ),
            dcc.Store(
                id=ids.VARIABLE_DICT_STORAGE, data=dict(), storage_type="memory") 
        ]
    )