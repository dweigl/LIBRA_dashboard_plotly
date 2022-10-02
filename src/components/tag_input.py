from dash import Dash, dcc, html
from . import ids

def render(app: Dash) -> html.Div:
    return html.Div(
        children=[
            html.Div([
                html.H6("LIBRA scenario name. (Should be alphanumeric with no spaces (_ allowed), max 30 characters. Press Enter to submit.)"),
                dcc.Input(
                    id=ids.SCENARIO_NAME_INPUT,
                    type="text",
                    required=True,
                    debounce=True,
                    minLength=5,
                    maxLength=30,
                    className="tag-input"
                ),
                html.H6("Github commit tag of LIBRA model (Should be alphanumeric, 7 characters long, with no spaces. Press Enter to submit)."),
                dcc.Input(
                    id=ids.GITHUB_COMMIT_INPUT,
                    type="text",
                    required=True,
                    debounce=True,
                    minLength=6,
                    maxLength=7,
                    className="tag-input"
                )
            ])
        ])