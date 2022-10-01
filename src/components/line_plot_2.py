from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from typing import Any
from src.plotting_functions.plotting_functions_plotly import make_lineplot
from src.plotting_functions.plot_parameters import LinePlotParameters, StyleParameters
from . import ids
import pandas as pd

def render(app: Dash) -> html.Div:
    def make_selected_data(
        df: pd.DataFrame, 
        plot_params: LinePlotParameters, 
        style_params:StyleParameters) -> pd.DataFrame:

        selected_data = pd.DataFrame([])
        cols = [f"{run_name}: {plot_params._full_variable_name}" for run_name in style_params.stella_run_names]
        selected_data = df.loc[2020:2050, cols].transpose()
        selected_data.reset_index(inplace=True)
        return selected_data


    @app.callback(
        Output(ids.LINE_PLOT_TWO, "children"),
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
        data: dict[Any],
    ) -> html.Div:
        placeholder_title = f"{module}.{variable}"+"["+ \
            ", ".join([val for val in [array_val_1, array_val_2, array_val_3] if val != "None"]) + "]"
        placeholder_ylabel = f"{module}.{variable}"

        try:
            plot_params = LinePlotParameters(
                module=module,
                variable=variable,
                array_vals=[val for val in [array_val_1, array_val_2, array_val_3] if val != "None"],
                title=placeholder_title if title != placeholder_title else title,
                y_label=placeholder_ylabel if y_label != placeholder_ylabel else y_label,
                max_yval=max_yval if max_yval != 0 else None,
                decimal=decimal,
                is_exogenous_input=is_exogenous_input
            )
            df = pd.DataFrame.from_records(data, index="Years")
            style_params = StyleParameters(stella_run_names=stella_run_names, compare=False)

            selected_data = make_selected_data(df, plot_params, style_params)

            fig = make_lineplot(df, plot_params, style_params)

            return html.Div(
                className="line-plot-and-datatable-container",
                children=[
                    html.Div(className="data-table-div", children=[
                        dash_table.DataTable(
                            id=ids.DATATABLE_TWO,
                            data=selected_data.to_dict('records'), 
                            columns=[{"name": str(i), "id": str(i)} for i in selected_data.columns],    
                            style_table={'overflowX': 'auto'}),
                    ]),
                    html.Div(children=[dcc.Graph(className="line-plot", figure=fig)]),
                ],
                id=ids.LINE_PLOT_TWO)
        except Exception as e:
            return html.Div([str(e)])
        
    return html.Div(id=ids.LINE_PLOT_TWO)