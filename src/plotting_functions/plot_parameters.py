"""
Data types used in LIBRA output plotting functions
"""
from .basedatatypes import ArrayValue, ArrayType, Module
from dataclasses import dataclass, field
from typing import Optional, ClassVar
from abc import ABC, abstractmethod, abstractclassmethod
import csv


@dataclass(kw_only=True, slots=True)
class PlotParameters(ABC):
    """
    Base class for plot parameters.
    """
    module: Module  # name of LIBRA module
    variable: str  # name of variable
    array_vals: list[ArrayValue]  # names of array values
    title: str  # Plot title
    y_label: str  # Y axis label
    max_yval: Optional[float] = None  # Maximum value of y axis ticks
    decimal: Optional[bool] = False  # Whether to use decimal point in y ticks
    # Whether variable is an exogenous input
    is_exogenous_input: Optional[bool] = False
    tag: Optional[str] = None  # Figure tag
    x_label: Optional[str] = None  # X axis label

    @abstractclassmethod
    def instantiate_from_csv(cls) -> None:
        """
        Loads pre-defined plot parameters from csv.
        """

    def _construct_full_variable_name(self, end_array_val: ArrayValue) -> str:
        """Construct full variable name from its parts."""
        full_variable_name = f"{self.module.value}.{self.variable}"
        if self.array_vals:
            full_variable_name += f"[{self.array_vals[0].value}"
            for val in self.array_vals[1:-1]:
                full_variable_name += f", {val.value}"
            if len(self.array_vals) > 1:
                if isinstance(end_array_val, str):
                    full_variable_name += f", {end_array_val}"
                else:
                    full_variable_name += f", {end_array_val.value}"
            full_variable_name += "]"
        return full_variable_name

    def _validate_plot_params(self) -> None:
        """Validates input values for plot parameters."""
        assert len(self.array_vals) > 0, "At least one valid array value must be supplied."
        assert len(self.array_vals) < 4, "Number of array values cannot exceed 3."
        assert len(self.variable.strip()) > 0, "Variable name cannot be empty."
        assert len(self.title.strip()) > 0, "Title cannot be empty."
        assert len(self.y_label.strip()) > 0, "Y label cannot be empty."
        assert isinstance(
            self.decimal, bool), f"\"decimal\" must be a boolean value."
        assert isinstance(self.is_exogenous_input,
                          bool), f"\"is_exogenous_input\" must be a boolean value."

    def _initialize_module(self) -> Module:
        """Initialize a module object from input."""
        return Module(str(self.module).strip())

    def _initialize_array_vals(self) -> list[ArrayValue]:
        """Initialize array value from input."""
        if isinstance(self.array_vals, str):
            return [ArrayValue(array_val.strip()) for array_val in self.array_vals.split(",") if array_val != ""]
        return [ArrayValue(str(array_val).strip()) for array_val in self.array_vals if array_val != ""]

    def __repr__(self) -> str:
        return f"\n{self.__class__.__name__}:\n\tmodule : {self.module}, \n\tvariable : {self.variable}, \
            \n\tarray_vals : {self.array_vals}, \n\ttitle : {self.title}, \n\tx_label : {self.x_label}, \
            \n\ty_label : {self.y_label}, \n\tmax_yval : {self.max_yval}, \n\tdecimal : {self.decimal}, \
            \n\tis_exogenous_input : {self.is_exogenous_input}, \n\ttag : {self.tag}"


@dataclass(kw_only=True, slots=True)
class LinePlotParameters(PlotParameters):
    """
    Class for line plot parameters.
    """
    _full_variable_name: str = field(init=False)
    __all: ClassVar[list] = []

    def __post_init__(self):
        self.module = self._initialize_module()
        self.array_vals = self._initialize_array_vals()
        self._validate_plot_params()
        self._full_variable_name = self._construct_full_variable_name(
            self.array_vals[-1].value)
        LinePlotParameters.__all.append(self)

    @classmethod
    def instantiate_from_csv(cls):
        """
        Loads pre-defined plot parameters from csv.
        """
        with open("definitions_lineplots.csv", "r") as f:
            reader = csv.DictReader(f)
            plot_params = list(reader)

        for plot_param in plot_params:
            LinePlotParameters(
                module=plot_param.get("module"),
                variable=plot_param.get("variable"),
                array_vals=plot_params.get("array_vals"),
                title=plot_param.get("title"),
                y_label=plot_param.get("y_label"),
                max_yval=float(plot_param.get("max_yval")) if plot_param.get(
                    "max_yval") else None,
                decimal=True if plot_param.get(
                    "decimal").upper() == "TRUE" else False,
                is_exogenous_input=True if plot_param.get(
                    "is_exogenous_input").upper() == "TRUE" else False
            )

    def __repr__(self) -> str:
        return f"\n{self.__class__.__name__}:\n\tmodule : {self.module}, \n\tvariable : {self.variable}, \
            \n\tarray_vals : {self.array_vals}, \n\ttitle : {self.title}, \n\tx_label : {self.x_label}, \
            \n\ty_label : {self.y_label}, \n\tmax_yval : {self.max_yval}, \n\tdecimal : {self.decimal}, \
            \n\tis_exogenous_input : {self.is_exogenous_input}, \n\ttag : {self.tag}, {self._full_variable_name}"

@dataclass(kw_only=True, slots=True)
class StackPlotParameters(PlotParameters):
    """
    Class for stack plot parameters.
    """
    _stack_variable_names: list[str] = field(init=False)
    _stack_list: list[str] = field(init=False)
    __all: ClassVar[list] = []

    def __post_init__(self) -> None:
        self.module = self._initialize_module()
        self.array_vals = self._initialize_array_vals()
        self._validate_plot_params()
        self._stack_list =  self._construct_stack_list()
        self._stack_variable_names = self._construct_stack_variable_names()
        StackPlotParameters.__all.append(self)

    def _construct_stack_list(self) -> list[str]:
        """Creates a list of array values to be plotted from the last array value supplied."""
        return ArrayType.enumerate_array_type(
            self.array_vals[-1].data_type)

    def _construct_stack_variable_names(self) -> list[str]:
        """Creates a list of variable names for stack plots."""
        return [self._construct_full_variable_name(ArrayValue(stack)) for stack in self._stack_list]

    @classmethod
    def instantiate_from_csv(cls):
        """
        Loads pre-defined plot parameters from csv.
        """
        with open("definitions_stackplots.csv", "r") as f:
            reader = csv.DictReader(f)
            plot_params = list(reader)

        for plot_param in plot_params:
            StackPlotParameters(
                module=plot_param.get("module"),
                variable=plot_param.get("variable"),
                array_vals=plot_params.get("array_vals"),
                title=plot_param.get("title"),
                y_label=plot_param.get("y_label"),
                max_yval=float(plot_param.get("max_yval")) if plot_param.get(
                    "max_yval") else None,
                decimal=True if plot_param.get(
                    "decimal").upper() == "TRUE" else False,
                is_exogenous_input=True if plot_param.get(
                    "is_exogenous_input").upper() == "TRUE" else False
            )

    def __repr__(self) -> str:
        return f"\n{self.__class__.__name__}:\n\tmodule : {self.module}, \n\tvariable : {self.variable}, \
            \n\tarray_vals : {self.array_vals}, \n\ttitle : {self.title}, \n\tx_label : {self.x_label}, \
            \n\ty_label : {self.y_label}, \n\tmax_yval : {self.max_yval}, \n\tdecimal : {self.decimal}, \
            \n\tis_exogenous_input : {self.is_exogenous_input}, \n\ttag : {self.tag}, {self._stack_variable_names}"

@dataclass(kw_only=True, slots=True)
class StyleParameters:
    """
    Class for style parameters.
    """

    stella_run_names: list[str]
    compare: bool
    line_styles: Optional[list[str]] = field(default_factory=list[str])
    colors: Optional[list[str]] = field(default_factory=list[str])
    highlight: Optional[list[bool]] = field(default_factory=list[bool])

    # Color-blind friendly for line plots: https://gist.github.com/thriveth/8560036
    _CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a',
                       '#f781bf', '#a65628', '#984ea3',
                       '#999999', '#b7121f', '#dede00', '#600FFF']

    def __post_init__(self) -> None:
        """
        Assign colors and linestyles if not initialized. Also, validate datatypes.
        """
        assert isinstance(
            self.compare, bool), f"{self.compare} is not a boolean!"
        assert len(self.stella_run_names) != 0, f"Scenario names cannot be empty!"
        assert isinstance(
            self.stella_run_names[0], str), "Scenario names must be strings!"

        self._validate_highlights()
        self._validate_colors()
        self._validate_linestyles()

    def _validate_colors(self) -> None:
        """Validate the colors variable."""
        if not self.colors:
            self._set_colors()
        else:
            assert len(self.colors) == len(
                self.stella_run_names), "Number of colors should match the number of Stella run names."

    def _validate_linestyles(self) -> None:
        """Validate the linestyles variable."""
        if not self.line_styles:
            self._set_line_styles()
        else:
            assert len(self.line_styles) == len(
                self.stella_run_names), "Number of line-styles should match the number of Stella run names."

    def _validate_highlights(self) -> None:
        """Validate the highlights variable."""
        if self.highlight:
            assert len(self.highlight) == len(
                self.stella_run_names), "Number of lines to highlight should match the number of Stella run names."

    def _set_colors(self) -> None:
        """Set the colors variable."""
        self.colors = self._CB_color_cycle[:len(self.stella_run_names)]
        if self.compare:
            num_style_elems = int(len(self.stella_run_names)/2)
            self.colors = 2*self._CB_color_cycle[:num_style_elems]

    def _set_line_styles(self) -> None:
        """Set the linestyles variable."""
        self.line_styles = len(self.stella_run_names)*["solid"]
        if self.compare:
            num_style_elems = int(len(self.stella_run_names)/2)
            self.line_styles = num_style_elems * \
                ["solid"] + num_style_elems*["dashed"]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}:\n\tstella_run_names : {self.stella_run_names}, \
            \n\tline_styles : {self.line_styles}, \n\tcolors : {self.colors}, \
            \n\tcompare : {self.compare}"

