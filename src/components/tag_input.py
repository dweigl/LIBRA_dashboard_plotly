from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
import re

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.TAG_INPUT_SUBMIT_BUTTON, "disabled"),
        Input(ids.SCENARIO_NAME_INPUT, "value"),
        Input(ids.GITHUB_COMMIT_INPUT, "value")
    )
    def update_submit_button(
        scenario_name: str,
        commit: str) -> bool:

        if re.findall(r"[\w\_]+", scenario_name) and re.findall(r"\w+", commit):
            return False
        return True

    return html.Div(
        children=[
            html.Div([
                html.H4(
                    "Inputs for GitHub commit tag.",
                    className="tag-input-header"
                ),
                html.H6("LIBRA scenario name. (Should be alphanumeric with no spaces (_ allowed), max 30 characters.)"),
                dcc.Input(
                    id=ids.SCENARIO_NAME_INPUT,
                    type="text",
                    required=True,
                    debounce=False,
                    minLength=5,
                    maxLength=30,
                    className="tag-input"
                ),
                html.H6("Github commit tag of LIBRA model (Should be alphanumeric, 7 characters long, with no spaces.)"),
                dcc.Input(
                    id=ids.GITHUB_COMMIT_INPUT,
                    type="text",
                    required=True,
                    debounce=False,
                    minLength=6,
                    maxLength=7,
                    className="tag-input"
                ),  
                html.Button(
                    id=ids.TAG_INPUT_SUBMIT_BUTTON,
                    className="tag-input",
                    children=["Submit"],
                    disabled=True,
                    n_clicks=0
                )
            ])
        ])