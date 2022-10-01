from dataclasses import dataclass, field
import pandas as pd
import re

@dataclass(kw_only=True)
class LIBRAOutputNamesParser:
    """
    Parser for run-names, module, variable and array-value names from a LIBRA outputs dataframe.
    """
    variable_dict: dict[str, set[str]] = field(default_factory=dict)
    array_val_dict: dict[str, list[str]] = field(default_factory=dict)

    def parse_names_from_dataframe(self, df: pd.DataFrame) -> None:
        """Update variable and arrayvalue dictionaries based on names parsed from input dataframe."""
        for col in df.columns:
            variable_name = self._update_variable_dict_from_single_column_name(col)
            self._update_array_val_dict_from_single_column_name(col, variable_name)
        for module in self.variable_dict.keys():
            self.variable_dict[module] = list(self.variable_dict[module])

    def _update_variable_dict_from_single_column_name(self, col: str) -> str:
        """
        Parse new variable, module and run names from a column name in the LIBRA outputs pandas dataframe.
        """

        rootname_pattern = re.compile(r"([\w\s$%/-]+):\s([\w\s$%/-]+)\.([\w\s$%/-]+)\[?") 
        for match in rootname_pattern.findall(col):
            if match[1] not in self.variable_dict.keys():
                self.variable_dict[match[1]] = set([match[2]])
            else:
                self.variable_dict[match[1]].add(match[2])
        return f"{match[1]}.{match[2]}"
        
    def _update_array_val_dict_from_single_column_name(self, col: str, variable_name: str) -> None:
        """
        Parse variables and corresponding array values from a column name of the LIBRA output pandas dataframe.
        """
        assert variable_name in col, f"Variable name \"{variable_name}\" is not in column \"{col}\"."

        arrayval_pattern = re.compile(r"\[(\w+|\w+(,\s\w+){0,3})\]")
        for match in arrayval_pattern.findall(col):
            if variable_name not in self.array_val_dict.keys():
                self.array_val_dict[variable_name] = [array_val.strip() \
                                for array_val in match[0].split(",") if array_val != ""]