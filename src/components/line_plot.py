from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output, State
from datetime import date
from typing import Any
from src.plotting_functions.plotting_functions_plotly import make_lineplot
from src.plotting_functions.plot_parameters import LinePlotParameters, StyleParameters
from . import ids
import pandas as pd
import re

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
        Output(ids.LINE_PLOT, "children"),
        Input(ids.STELLA_RUN_NAMES_DROPDOWN, "value"),
        Input(ids.MODULE_DROPDOWN, "value"),
        Input(ids.VARIABLE_DROPDOWN, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_1, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_2, "value"),
        Input(ids.ARRAYVAL_DROPDOWN_3, "value"),
        Input(ids.TITLE_INPUT, "value"),
        Input(ids.YLABEL_INPUT, "value"),
        Input(ids.MAX_YVAL_INPUT, "value"),
        Input(ids.DECIMAL_POINT_RADIOITEMS, "value"),
        Input(ids.EXOGENOUS_INPUT_RADIOITEMS, "value"),
        Input(ids.SCENARIO_NAME_INPUT, "value"),
        Input(ids.GITHUB_COMMIT_INPUT, "value"),
        Input(ids.TAG_INPUT_SUBMIT_BUTTON, "n_clicks"),
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
        scenario_name: str,
        github_commit: str,
        n_clicks: int,
        data: dict[Any],
    ) -> html.Div:
        placeholder_title = f"{module}.{variable}"+"["+ \
            ", ".join([val for val in [array_val_1, array_val_2, array_val_3] if val != "None"]) + "]"
        placeholder_ylabel = f"{module}.{variable}"

        tag = None
        if n_clicks:
            tag = f"{scenario_name}_{github_commit}_"+re.sub( "-", "", str(date.today()))

        try:
            plot_params = LinePlotParameters(
                module=module,
                variable=variable,
                array_vals=[val for val in [array_val_1, array_val_2, array_val_3] if val != "None"],
                title=placeholder_title if title != placeholder_title else title,
                y_label=placeholder_ylabel if y_label != placeholder_ylabel else y_label,
                max_yval=max_yval if max_yval != 0 else None,
                decimal=decimal,
                is_exogenous_input=is_exogenous_input,
                tag=tag if tag else None
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
                            id=ids.DATATABLE,
                            data=selected_data.to_dict('records'), 
                            columns=[dict(name=str(i), id=str(i)) for i in selected_data.columns],              
                            style_table=dict(height="300px", overflowX='auto', overflowY='auto'),
                            export_format="csv")
                    ]),
                    html.Div(children=[
                        dcc.Graph(
                            className="line-plot", 
                            figure=fig, 
                            config=dict(
                                toImageButtonOptions=dict(
                                    format="png", width=800, height=700, scale=3.0)
                            ))]),
                ],
                id=ids.LINE_PLOT)
        except Exception as e:
            return html.Div([
                html.Div(className="data-table-div", children=[html.P("Invalid data selection")]),
                html.Div(className="line-plot", children=[html.P(f"{placeholder_title} is not present in the uploaded data")])
            ])
        
    return html.Div(id=ids.LINE_PLOT)