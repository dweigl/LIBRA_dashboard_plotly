""" 
Plotting functions for LIBRA outputs, using plotly
"""

import pandas as pd
import os
import numpy as np
import textwrap
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .basedatatypes import ArrayType
from .plot_parameters import LinePlotParameters, StackPlotParameters, StyleParameters

def make_lineplot(
    df: pd.DataFrame,
    plot_parameters: LinePlotParameters,
    style_parameters: StyleParameters,
    start_year: int = 2020,
    end_year: int = 2050) -> go.Figure:
    """
    Helper function to make line plots.
    """
    col_names = [f"{run_name}: {plot_parameters._full_variable_name}" \
        for run_name in style_parameters.stella_run_names]

    fig = go.Figure()
    for i, col in enumerate(col_names):
        fig.add_trace(
            go.Scatter(
                x=np.arange(start_year, end_year+1),
                y=df.loc[start_year:end_year+1, col],
                mode="lines",
                line=dict(
                    color=style_parameters.colors[i],
                    width=3
                ),
                name=style_parameters.stella_run_names[i]
            )
        )
    fig.update_layout(
        template="simple_white",
        width=700,
        height=700,
        font=dict(
            family="Arial",
            size=14,
            color="rgb(82, 82, 82)"
        ),
        title=dict(
            text="<br>".join(textwrap.wrap(f"LIBRA input: {plot_parameters.title}", 
            width=50)) if plot_parameters.is_exogenous_input \
            else "<br>".join(textwrap.wrap(plot_parameters.title, width=50)),                  
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top'
        ),
        yaxis_title="<br>".join(textwrap.wrap(plot_parameters.y_label, width=30)),
        xaxis=dict(showgrid=True),
        yaxis=dict(
            showgrid=True,
            tickformat=".2f" if plot_parameters.decimal else "",
            title=dict(standoff=5),
            range=[0.0, np.max(df.loc[start_year:end_year+1, col_names].values)]
        ),
        legend_title_text=None,
        legend=dict(
            yanchor="bottom",
            y=-0.35,
            xanchor="left",
            x=0.25
        )
    )
    if plot_parameters.tag:
        fig.add_annotation(
                    x=1.1, y=-0.38, xref="paper", yref="paper", 
                    text=plot_parameters.tag, showarrow=False, align="center")

    if plot_parameters.max_yval:
        fig.update_layout(yaxis=dict(range=[0.0, plot_parameters.max_yval]))

    return fig

def make_comparative_lineplots(
        df: pd.DataFrame,
        plot_parameters: LinePlotParameters,
        style_parameters: StyleParameters,
        start_year:int = 2020,
        end_year:int = 2050) -> go.Figure:
    """
    Helper function to make comparative subplots.
    """

    fig = make_subplots(
        rows=1, 
        cols=len(style_parameters.stella_run_names), 
        shared_yaxes=True,
        subplot_titles=["<br>".join(textwrap.wrap(run_name, width=30)) \
            for run_name in style_parameters.stella_run_names]
    )

    col_names = [f"{stella_run}: {plot_parameters._full_variable_name}" \
        for stella_run in style_parameters.stella_run_names]
    for i, col in enumerate(col_names):
        fig.add_trace(
            go.Scatter(
                x=np.arange(start_year, end_year+1),
                y=df.loc[start_year:end_year+1, col],
                mode="lines",
                line=go.scatter.Line(color="black", width=3),
                name=style_parameters.stella_run_names[i]
            ),
            row=1, col=i+1
        )
        fig.update_xaxes(showgrid=False, row=1, col=i+1)
        fig.update_yaxes(
            showgrid=False, 
            range=[0.0, np.max(df.loc[start_year:end_year+1, col_names].values)],
            row=1, col=i+1)
        if plot_parameters.max_yval:
            fig.update_yaxes(range=[0.0, plot_parameters.max_yval])
    
    fig.update_layout(
        template="simple_white",
        width=300*len(style_parameters.stella_run_names),
        height=400,
        font=dict(
            family="Arial",
            size=14,
            color="rgb(82, 82, 82)"
        ),
        title=dict(
            text="<br>".join(textwrap.wrap(f"LIBRA input: {plot_parameters.title}", width=50)) \
                if plot_parameters.is_exogenous_input \
                else "<br>".join(textwrap.wrap(plot_parameters.title, width=50)),                  
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top'
        ),
        yaxis=dict(
            title=dict(
                text="<br>".join(textwrap.wrap(plot_parameters.y_label, width=30)),
                standoff=5),
            tickformat=".2f" if plot_parameters.decimal else ""),
        showlegend=False
    )
    if plot_parameters.tag:
        fig.add_annotation(
                    x=1.0, y=-0.3, xref="paper", yref="paper", 
                    text=plot_parameters.tag, showarrow=False, align="center")
    return fig

def make_stackplot(df: pd.DataFrame,
                   plot_parameters: StackPlotParameters,
                   run_name: str,
                   start_year: int = 2020,
                   end_year: int = 2050,
                   alpha: float = 0.8) -> go.Figure:
    """
    Makes a stack plot of given variables.
    """
    CB_color_cycle_hex = ['#377eb8', '#ff7f00', '#4daf4a',
                      '#f781bf', '#a65628', '#984ea3',
                      '#999999', '#b7121f', '#dede00', '#600FFF']
    CB_color_cycle_rgb = [(55, 126, 184), (255, 127, 0), (77, 175, 74),
                        (247, 129, 191), (166, 86, 40), (152, 78, 163),
                        (153, 153, 153), (183, 18, 31), (222, 222, 0), (96, 15, 255)]

    stack_list = ArrayType.enumerate_array_type(
        plot_parameters.array_vals[-1].data_type)
    col_names = [
        f"{run_name}: {variable_name}" for variable_name in plot_parameters._stack_variable_names]

    fig = go.Figure()
    for i, col in enumerate(col_names):
        fig.add_trace(
            go.Scatter(
                x=np.arange(start_year, end_year+1),
                y=df.loc[start_year:end_year+1, col],
                line=dict(width=0, color=CB_color_cycle_hex[i]),
                fillcolor=f"rgba({CB_color_cycle_rgb[i][0]}, {CB_color_cycle_rgb[i][1]}, {CB_color_cycle_rgb[i][2]}, {alpha})" ,
                stackgroup="one",
                name=stack_list[i]
            )
        )
    
    fig.update_layout(
        template="simple_white",
        width=800,
        height=600,
        font=dict(
            family="Arial",
            size=14,
            color="rgb(82, 82, 82)"
        ),
        title=dict(
            text="<br>".join(textwrap.wrap(f"LIBRA input: {plot_parameters.title}", 
            width=50)) if plot_parameters.is_exogenous_input \
            else "<br>".join(textwrap.wrap(plot_parameters.title, width=50)),                  
            x=0.5,
            y=0.9,
            xanchor='center',
            yanchor='top'
        ),
        yaxis_title=plot_parameters.y_label,
        xaxis=dict(showgrid=True),
        yaxis=dict(
            showgrid=True,
            tickformat=".2f" if plot_parameters.decimal else "",
            title=dict(standoff=5)
        ),
        legend_title_text=None,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.25
        )
    )
    if plot_parameters.tag:
        fig.add_annotation(
                    x=1.0, y=-0.45, xref="paper", yref="paper", 
                    text=plot_parameters.tag, showarrow=False, align="center")
    
    return fig

def make_stackplots_from_list(df: pd.DataFrame,
                              plot_params_list: list[StackPlotParameters],
                              stella_run_names: list[str]) -> None:
    """
    Generates stack plots given dataframe, list of plot parameters and Stella run names.
    """
    for stella_run in stella_run_names:
        for plot_params in plot_params_list:
            make_stackplot(
                df=df,
                plot_parameters=plot_params,
                run_name=stella_run
            )

def fix_col_names(df:pd.DataFrame) -> None:
    """
    Removes "=" and " that are inserted into the names of some LIBRA variables.
    """
    col_names_to_change = df.columns[df.columns.str.startswith("=")].tolist()
    changed_col_names = [col.replace("=", "") for col in col_names_to_change]
    changed_col_names = [col.replace("\"", "") for col in changed_col_names]
    df.rename(columns=dict(zip(col_names_to_change, changed_col_names)), inplace=True)