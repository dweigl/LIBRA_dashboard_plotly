"""
Plotting functions for LIBRA outputs
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import textwrap

from plot_parameters import LinePlotParameters, StackPlotParameters, StyleParameters, ArrayType
from typing import Optional
from matplotlib import ticker

stylesheet_path = os.path.join(os.path.dirname(__file__), "LIBRA_plots.mplstyle")
plt.style.use(["seaborn-whitegrid", "seaborn-paper",
              "seaborn-colorblind", stylesheet_path])

def make_lineplot(
        df: pd.DataFrame,
        plot_parameters: LinePlotParameters,
        style_parameters: StyleParameters,
        start_year: int = 2020,
        end_year: int = 2050) -> None:
    """
    Helper function to make line plots.
    """
    colnames = [f"{run_name}: {plot_parameters._full_variable_name}"
                for run_name in style_parameters.stella_run_names]

    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes()
    for col, style_idx in zip(colnames, np.arange(len(style_parameters.stella_run_names))):
        ax.plot(np.arange(start_year, end_year+1),
                df.loc[start_year:end_year, col],
                label=style_parameters.stella_run_names[style_idx],
                linestyle=style_parameters.line_styles[style_idx],
                color=style_parameters.colors[style_idx])

    ax.set_title(textwrap.fill(plot_parameters.title, width=30, break_long_words=True))
    if plot_parameters.is_exogenous_input:
        ax.set_title(textwrap.fill(f"LIBRA input: {plot_parameters.title}", 
            width=30, break_long_words=True))
    ax.set_ylabel(textwrap.fill(plot_parameters.y_label, width=20, break_long_words=True))

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, pos: '{:0,d}'.format(int(x))))
    if plot_parameters.decimal:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # 5 x axis ticks
    ax.tick_params(axis='x', labelrotation=-45)
    if plot_parameters.max_yval is not None:
        ax.set_ylim(0, plot_parameters.max_yval)

    if plot_parameters.tag is not None:
        ax.annotate(plot_parameters.tag,
                    xy=(1.0, -0.45),
                    xycoords='axes fraction',
                    ha='right',
                    va="center",
                    fontsize=14)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -.35), ncol=2)
    if plot_parameters.max_yval is not None:
        ax.set_ylim(0, plot_parameters.max_yval)
    plt.show()

def make_comparative_lineplots(
        input_df: pd.DataFrame,
        plot_parameters: LinePlotParameters,
        style_parameters: StyleParameters,
        start_year: Optional[int] = 2020,
        end_year: Optional[int] = 2050) -> None:
    """
    Helper function to make comparative subplots.
    """
    ax: list = [0]*len(style_parameters.stella_run_names)

    fig = plt.figure(figsize=(5*len(style_parameters.stella_run_names), 3))
    fig.suptitle(plot_parameters.title, fontsize=16)
    if plot_parameters.is_exogenous_input:
        fig.suptitle(f"LIBRA input : {plot_parameters.title}", fontsize=16)
    fig.subplots_adjust(top=0.80, bottom=0.10)

    for i, stella_run in enumerate(style_parameters.stella_run_names):
        col_name = f"{stella_run}: {plot_parameters._full_variable_name}"
        if i > 0:
            ax[i] = plt.subplot(
                1, len(style_parameters.stella_run_names), i+1, sharey=ax[0])
            plt.tick_params('y', labelleft=False)
        elif i == 0:
            ax[i] = plt.subplot(1, len(style_parameters.stella_run_names), i+1)
        plt.plot(input_df.loc[start_year:end_year,
                 col_name], linewidth=1.0, color='b')
        if style_parameters.highlight:
            if style_parameters.highlight[i]:
                plt.plot(input_df.loc[start_year:2030,
                         col_name], linewidth=1.0, color='b')
                plt.plot(input_df.loc[2030:end_year,
                         col_name], linewidth=3.0, color='k')
        plt.title(textwrap.fill(stella_run, width=30, break_long_words=True))
        ax[i].set_xlim([start_year, end_year])
        if plot_parameters.max_yval is not None:
            ax[i].set_ylim([0, plot_parameters.max_yval])

        ax[i].tick_params(axis="both", which="both", length=5)
        ax[i].grid(visible=False)
        ax[i].xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax[i].spines['top'].set_color('white')
        ax[i].spines['right'].set_color('white')
    ax[0].locator_params(nbins=5, axis='y')

    ax[0].yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, pos: f"{int(x):0,d}"))
    if plot_parameters.decimal:
        ax[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    if plot_parameters.tag is not None:
        plt.annotate(plot_parameters.tag,
                     xy=(1.0, -0.25),
                     xycoords='axes fraction',
                     ha='right',
                     va="center",
                     fontsize=14)
    ax[0].set_ylabel(textwrap.fill(plot_parameters.y_label, width=20, break_long_words=True))
    plt.show()

def make_stackplot(df: pd.DataFrame,
                   plot_params: StackPlotParameters,
                   run_name: str,
                   start_year: Optional[int] = 2020,
                   end_year: Optional[int] = 2050) -> None:
    """
    Makes a stack plot of given variables.
    """
    CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                      '#f781bf', '#a65628', '#984ea3',
                      '#999999', '#b7121f', '#dede00', '#600FFF']

    stack_list = ArrayType.enumerate_array_type(
        plot_params.array_vals[-1].data_type)
    col_names = [
        f"{run_name}: {variable_name}" for variable_name in plot_params._stack_variable_names]

    plt.figure(figsize=(12, 6))
    ax = plt.axes()
    ax.stackplot(np.arange(start_year, end_year+1),
                 *[df.loc[start_year:end_year, col] for col in col_names],
                 labels=stack_list, colors=CB_color_cycle, alpha=0.8)


    if plot_params.max_yval is not None:
        ax.set_ylim([0, plot_params.max_yval])
    if plot_params.is_exogenous_input:
        ax.set_title(textwrap.fill(f"LIBRA input : {plot_params.title}: {run_name}", 
            width=30, break_long_words=True))
    ax.set_title(textwrap.fill(f"{plot_params.title}: {run_name}", width=30, break_long_words=True))
    if plot_params.x_label is not None:
        ax.set_xlabel(plot_params.x_label)
    ax.set_ylabel(plot_params.y_label)

    ax.tick_params(axis='x', labelrotation=-45)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, pos: '{:0,d}'.format(int(x))))
    if plot_params.decimal:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

    if plot_params.tag is not None:
        ax.annotate(plot_params.tag,
                    xy=(1.0, -0.45),
                    xycoords='axes fraction',
                    ha='right',
                    va="center",
                    fontsize=14)
    plt.legend(loc='lower center', bbox_to_anchor=(.5, -.4), ncol=5)
    plt.show()

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
                plot_params=plot_params,
                run_name=stella_run
            )

def make_barplot(df: pd.DataFrame,
        plot_parameters: LinePlotParameters,
        style_parameters: StyleParameters,
        start_year: int = 2020,
        end_year: int = 2050) -> None:
        """Makes a barplot for given input bar plot parameters and style parameters."""

        colnames = [f"{run_name}: {plot_parameters._full_variable_name}"
                for run_name in style_parameters.stella_run_names]

        fig = plt.figure(figsize=(12, 6))
        ax = plt.axes()
        width = 1/len(style_parameters.stella_run_names)-0.1
        for col, style_idx in zip(colnames, np.arange(len(style_parameters.stella_run_names))):
            middle_idx = int(len(style_parameters.stella_run_names)/2)+1 \
                if len(style_parameters.stella_run_names)%2 else len(style_parameters.stella_run_names)/2
            ax.bar(x=np.arange(start_year, end_year+1)+\
                width*int(style_idx+1),
                    height=df.loc[start_year:end_year, col],
                    width=width,
                    label=style_parameters.stella_run_names[style_idx],
                    color=style_parameters.colors[style_idx])
            ax.set_title(textwrap.fill(plot_parameters.title, width=30, break_long_words=True))
        if plot_parameters.is_exogenous_input:
            ax.set_title(textwrap.fill(f"LIBRA input: {plot_parameters.title}", 
                width=30, break_long_words=True))
        ax.set_ylabel(textwrap.fill(plot_parameters.y_label, width=20, break_long_words=True))

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(
            lambda x, pos: '{:0,d}'.format(int(x))))
        if plot_parameters.decimal:
            ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

        ax.xaxis.set_major_locator(ticker.MultipleLocator(5))  # 5 x axis ticks
        ax.tick_params(axis='x', labelrotation=-45)
        if plot_parameters.max_yval is not None:
            ax.set_ylim(0, plot_parameters.max_yval)

        if plot_parameters.tag is not None:
            ax.annotate(plot_parameters.tag,
                        xy=(1.0, -0.45),
                        xycoords='axes fraction',
                        ha='right',
                        va="center",
                        fontsize=14)
        plt.legend(loc='lower center', bbox_to_anchor=(0.5, -.35), ncol=2)
        if plot_parameters.max_yval is not None:
            ax.set_ylim(0, plot_parameters.max_yval)
        plt.show()

def fix_col_names(df:pd.DataFrame) -> None:
    """
    Removes "=" and " that are inserted into the names of some LIBRA variables.
    """
    col_names_to_change = df.columns[df.columns.str.startswith("=")].tolist()
    changed_col_names = [col.replace("=", "") for col in col_names_to_change]
    changed_col_names = [col.replace("\"", "") for col in changed_col_names]
    df.rename(columns=dict(zip(col_names_to_change, changed_col_names)), inplace=True)
