from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from . import ids

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.TITLE_INPUT_TWO, 'value'),
        Input(ids.MODULE_DROPDOWN_TWO, 'value'),
        Input(ids.VARIABLE_DROPDOWN_TWO, 'value'),
        Input(ids.ARRAYVAL_DROPDOWN_TWO_1, 'value'),
        Input(ids.ARRAYVAL_DROPDOWN_TWO_2, 'value'),
        Input(ids.ARRAYVAL_DROPDOWN_TWO_3, 'value')
    )
    def update_title(
        module: str,
        variable: str,
        array_val_1: str,
        array_val_2: str,
        array_val_3: str,
    ) -> str:
        title = f"{module}.{variable}"
        if array_val_1 != "None":
            title = title+"["+", ".join([val for val in [array_val_1, array_val_2, array_val_3]\
                 if val != "None"]) + "]"
        return title 
    
    @app.callback(
        Output(ids.YLABEL_INPUT_TWO, 'value'),
        Input(ids.MODULE_DROPDOWN_TWO, 'value'),
        Input(ids.VARIABLE_DROPDOWN_TWO, 'value')
    )
    def update_ylabel(
        module: str,
        variable: str
    ) -> str:
        return f"{module}.{variable}" 

    return html.Div(
        children=[
            html.H6("Line plot title (Press Enter to submit)."),
            dcc.Input(
                id=ids.TITLE_INPUT_TWO,
                type="text",
                required=True,
                debounce=True,
                value='None',
                className="title-and-ylabel-input"),
            html.H6("Y-axis label (Press Enter to submit)."),
            dcc.Input(
                id=ids.YLABEL_INPUT_TWO,
                type="text",
                required=True,
                debounce=True,
                value='None',
                className="title-and-ylabel-input"),
            html.H6("Maximum value for Y-axis."),
            dcc.Input(
                id=ids.MAX_YVAL_INPUT_TWO,
                type="number",
                min=0,
                max=100_000_000_000,
                step=0.01,
                value=0,
                size="300",
                className="max-yval-input"),
            html.H6("Decimal point for Y-axis labels?"),
            dcc.RadioItems(
                    id=ids.DECIMAL_POINT_RADIOITEMS_TWO,
                    className="radio-items",
                    options=[
                        dict(label="Yes\t\t\t\t\t\t.", value=True),
                        dict(label="No\t\t\t\t\t\t.", value=False)
                    ],
                    inline=True,
                    value=False),
            html.H6("Is the variable an exogenous input?"),
            dcc.RadioItems(
                    id=ids.EXOGENOUS_INPUT_RADIOITEMS_TWO,
                    className="radio-items",
                    options=[
                        dict(label="Yes\t\t\t\t\t\t.", value=True),
                        dict(label="No\t\t\t\t\t\t.", value=False)
                    ],
                    inline=True,
                    value=False)
        ],
    )