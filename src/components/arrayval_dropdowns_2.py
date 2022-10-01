from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from typing import Any
from . import ids
from src.data.LIBRAOutputNamesParser import LIBRAOutputNamesParser

import pandas as pd

from src.plotting_functions.basedatatypes import ArrayValue, ArrayType, InvalidArrayTypeError
from . import ids

def render(app: Dash) -> html.Div:
    def create_options_and_value(
                            module: str, 
                            variable: str,
                            array_val_dict: dict[str, list[str]],
                            i: int) -> tuple[list[dict[str, str]], str]:
        if module == "None" or variable == "None":
            return [dict(value="None", label="None")], "None"
        arrayvals = []
        try:
            arrayvals = [ArrayValue(val) for val in array_val_dict[f"{module}.{variable}"] if val]
        except Exception as e:
            print(e)
            return [dict(value="None", label="None")], "None"
        if not arrayvals or i >= len(arrayvals):
            return [dict(value="None", label="None")], "None"
        options = [dict(label=val, value=val) 
                    for val in sorted(ArrayType.enumerate_array_type(arrayvals[i].data_type))] 
        value = sorted(ArrayType.enumerate_array_type(arrayvals[i].data_type))[0]
        return options, value

    @app.callback(
        Output(ids.ARRAYVAL_DROPDOWN_TWO_1, "options"),
        Output(ids.ARRAYVAL_DROPDOWN_TWO_1, "value"),
        Input(ids.MODULE_DROPDOWN_TWO, "value"),
        Input(ids.VARIABLE_DROPDOWN_TWO, "value"),
        State(ids.ARRAYVAL_DICT_STORAGE, "data")
    )
    def update_arrayval_dropdown_1(
                            module: str, 
                            variable: str,
                            array_val_dict: dict[str, list[str]]) -> tuple[list[dict[str, str]], str]:
        options, value = create_options_and_value(module, variable, array_val_dict, 0)
        return options, value
    
    @app.callback(
        Output(ids.ARRAYVAL_DROPDOWN_TWO_2, "options"),
        Output(ids.ARRAYVAL_DROPDOWN_TWO_2, "value"),
        Input(ids.MODULE_DROPDOWN_TWO, "value"),
        Input(ids.VARIABLE_DROPDOWN_TWO, "value"),
        State(ids.ARRAYVAL_DICT_STORAGE, "data")
    )
    def update_arrayval_dropdown_2(
                            module: str, 
                            variable: str,
                            array_val_dict: dict[str, list[str]]) -> tuple[list[dict[str, str]], str]:
        options, value = create_options_and_value(module, variable, array_val_dict, 1)
        return options, value

    @app.callback(
        Output(ids.ARRAYVAL_DROPDOWN_TWO_3, "options"),
        Output(ids.ARRAYVAL_DROPDOWN_TWO_3, "value"),
        Input(ids.MODULE_DROPDOWN_TWO, "value"),
        Input(ids.VARIABLE_DROPDOWN_TWO, "value"),
        State(ids.ARRAYVAL_DICT_STORAGE, "data")
    )
    def update_arrayval_dropdown_3(
                            module: str, 
                            variable: str,
                            array_val_dict: dict[str, list[str]]) -> tuple[list[dict[str, str]], str]:
        options, value = create_options_and_value(module, variable, array_val_dict, 2)
        return options, value

    return html.Div([
            html.Div(
                children=[html.H6(f"Select array value 1."),
                    dcc.Dropdown(
                            id=ids.ARRAYVAL_DROPDOWN_TWO_1,
                            options=[dict(label="None", value="None")],
                            value="None",
                        ),
                    html.H6(f"Select array value 2."),
                    dcc.Dropdown(
                            id=ids.ARRAYVAL_DROPDOWN_TWO_2,
                            options=[dict(label="None", value="None")],
                            value="None",
                        ),
                    html.H6(f"Select array value 3."),
                    dcc.Dropdown(
                            id=ids.ARRAYVAL_DROPDOWN_TWO_3,
                            options=[dict(label="None", value="None")],
                            value="None",
                        )
                    ]
                )
    ])