
from . import ids
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import Dash, dcc, html
from src.data.LIBRAOutputNamesParser import LIBRAOutputNamesParser
from src.data.preprocess_data import preprocess_data
from typing import Any
import pandas as pd

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.DATA_STORAGE, "data"),
        Input(ids.FILE_UPLOADER, "contents")
    )
    def update_data_storage(contents: bytes) -> dict[Any]:
        try:
            if not contents:
                return dict()
            df = preprocess_data(contents)
            df.reset_index(inplace=True)

        except Exception as e:
            print(e)
            return dict()
        return df.to_dict("records")

    return html.Div([
        dcc.Upload(
            id=ids.FILE_UPLOADER,
            children=html.Div([
                "Drag and drop a LIBRA output CSV file (of size < 2 MB) or ",
                html.A("Select CSV file")
            ]),
            style=dict(
                width="100%",
                height="60px",
                lineHeight="60px",
                borderWidth="1px",
                borderStyle="dashed",
                borderRadius="5px",
                textAlign="center",
                margin="10px"
            )
        ),
        dcc.Store(
            id=ids.DATA_STORAGE, data=dict(), storage_type="memory"),  
        html.Button(
            id=ids.FILE_UPLOAD_BUTTON,
            className="file-upload-button",
            children=["Upload"],
            n_clicks=0
        )
    ])
