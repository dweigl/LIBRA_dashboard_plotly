from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from . import ids
from typing import Any
from src.data.LIBRAOutputNamesParser import LIBRAOutputNamesParser

import pandas as pd

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.MODULE_DROPDOWN, "options"),
        Output(ids.MODULE_DROPDOWN, "value"),
        Input(ids.FILE_UPLOAD_BUTTON, "n_clicks"),
        State(ids.DATA_STORAGE, "data")
    )
    def update_module_dropdown(_: int, data: dict[Any]) -> tuple[list[dict[str, str], str]]:
        try:
            if not data:
                raise PreventUpdate
                return dict()
            df = pd.DataFrame.from_records(data, index="Years")
            names_parser = LIBRAOutputNamesParser()
            names_parser.parse_names_from_dataframe(df)
            module_dropdown_options = [dict(value=module, label=module) for module in names_parser.variable_dict.keys()]
        except Exception as e:
            print(e)
            return [dict(value="None", label="None")], "None"

        return module_dropdown_options, list(names_parser.variable_dict.keys())[0]    
            
    return html.Div(
            children=[
                html.H6("Select LIBRA module name."),
                dcc.Dropdown(
                    id=ids.MODULE_DROPDOWN,
                    options=[dict(label="None", value="None")],
                    value="None"
                )
            ]
        )