from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from . import ids
from src.data.preprocess_data import preprocess_data
from typing import Any

import pandas as pd

def render(app: Dash) -> html.Div:
    def create_options_and_value(df: pd.DataFrame) -> tuple[list[dict[str, str]], list[str]]:
        values = sorted(list(set([col.split(":")[0] for col in df.columns])))
        return [dict(label=val, value=val) for val in values], values

    @app.callback(
        Output(ids.STELLA_RUN_NAMES_DROPDOWN, "options"),
        Output(ids.STELLA_RUN_NAMES_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_RUN_NAMES_BUTTON, "n_clicks"),
        Input(ids.FILE_UPLOAD_BUTTON, "n_clicks"),
        State(ids.DATA_STORAGE, "data")
    )
    def select_all_run_names(
            n_clicks_select_all: int, 
            n_clicks_file_upload: int, 
            data: dict[Any]) -> tuple[list[dict[str, str]], list[str]]:
        if not data:
            raise PreventUpdate
        df = pd.DataFrame.from_records(data, index="Years")
        options, value = create_options_and_value(df)
        return options, value

    return html.Div(
        children=[
            html.H6("Select LIBRA run names.", style=dict(textAlign="center", fontWeight="bold", color="#047cc4")),
            dcc.Dropdown(
                id=ids.STELLA_RUN_NAMES_DROPDOWN,
                options=[dict(label="None", value="None")],
                value=["None"],
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_RUN_NAMES_BUTTON,
                className="dropdown-button",
                children=["Select all"],
                n_clicks=0
            )
        ]
    )