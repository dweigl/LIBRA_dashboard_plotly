"""
LIBRA variable base data types
"""

from dataclasses import dataclass, field
from enum import Enum, unique
from multiprocessing.dummy import Array

class InvalidArrayTypeError(Exception):
    """Exception raised when user inputs an invalid LIBRA array type."""

    def __init__(self, msg):
        super().__init__(msg)

class EmptyVariableError(Exception):
    """Exception raised when user does not input a variable name."""

    def __init__(self, msg):
        super().__init__(msg)

@unique
class Module(Enum):
    """
    Enumerated datatype for LIBRA modules.
    """
    RECYCLING_INVESTMENT_ATTRACTIVENESS = "RIRA"
    MINERALS_MARKETPLACE = "Minerals Market"
    HYDROPYRO = "HydroPyro"
    DIRECT_RECYCLING = "DirectRecycle"
    BATTERY_MARKETPLACE = "Battery Market"
    BATTERY_MANUFACTURING = "Manufacturing"
    CATHODE_MANUFACTURING = "Cathode"
    CONSUMER = "Consumer"
    BES = "BES"
    LDV = "LDV"
    LCV = "LCV"
    MHDV = "MHDV"
    TWO3WHEELER = "Two3Wheel"
    EBUS = "EBus"


@unique
class ArrayType(Enum):
    """Enumerated datatype for types of array variables."""
    REGION = "region"
    V_BATT_TYPE = "VBattType"
    BATTERY_CHEMISTRY = "chemistry"
    MINERAL = "mineral"
    PROCESS = "process"
    STORAGE_BATT_TYPE = "storage_batt_type"
    CONVERSION_POLICY = "ConversionPolicy"
    TECH_ATTRIBUTE = "techattribute"
    TRANSPORT = "transport"
    PROJECT_YEAR = "ProjectYear"

    @staticmethod
    def enumerate_array_type(input) -> list[str]:
        """Returns a list of possible values for a LIBRA array type."""
        input_arraytype = ArrayType(input)
        match ArrayType(input):
            case ArrayType.REGION:
                return ["US", "ROW"]
            case ArrayType.V_BATT_TYPE:
                return ["BEV", "PHEV"]
            case ArrayType.BATTERY_CHEMISTRY:
                return ["LCO", "LFP", "LMO", "NCA", "NMC111", "NMC442", "NMC532", "NMC622", "NMC811", "NMC955"]
            case ArrayType.MINERAL:
                return ["Ni", "Co", "Li"]
            case ArrayType.PROCESS:
                return ["Hydro", "Pyro"]
            case ArrayType.STORAGE_BATT_TYPE:
                return ["Grid"]
            case ArrayType.CONVERSION_POLICY:
                return ["Price", "Feedstock", "FCI", "Loan"]
            case ArrayType.TECH_ATTRIBUTE:
                return ["ProcessYield", "PSuccess", "InputCap", "CapitalCost", "Risk", "DebtFrac"]
            case ArrayType.TRANSPORT:
                return ["TrainRail", "Road"]
            case ArrayType.PROJECT_YEAR:
                return [f"D&C{i+1}" for i in range(3)]+[f"Yr{j+1}" for j in range(30+1)]
        return []


@dataclass(slots=True)
class ArrayValue:
    """Base data type for all array values."""
    value: str
    data_type: ArrayType = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.data_type = self._assign_data_type()

    def _assign_data_type(self) -> ArrayType:
        """Set the array data type based on array value."""
        match self.value:
            case "US" | "ROW" | "region":
                return ArrayType.REGION
            case "BEV" | "PHEV" | "VBattType":
                return ArrayType.V_BATT_TYPE
            case "Co" | "Li" | "Ni" | "mineral":
                return ArrayType.MINERAL
            case "Hydro" | "Pyro" | "process":
                return ArrayType.PROCESS
            case "LFP" | "LCO" | "NCA" | "LMO" | "NMC111" | "NMC442" | "NMC532" | "NMC622" | "NMC811" | "NMC955" | "chemistry":
                return ArrayType.BATTERY_CHEMISTRY
            case "Grid" | "storage_batt_type":
                return ArrayType.STORAGE_BATT_TYPE
            case "Price"| "Feedstock"| "FCI"| "Loan" | "ConversionPolicy":
                return ArrayType.CONVERSION_POLICY
            case "ProcessYield" | "PSuccess" | "InputCap" | "CapitalCost" | "Risk" | "DebtFrac" |"techattribute":
                return ArrayType.TECH_ATTRIBUTE
            case "TrainRail"| "Road"| "transport":
                return ArrayType.TRANSPORT
            case 'D&C1'|'D&C2'|'D&C3'|'Yr1'|'Yr2'|'Yr3'|'Yr4'|'Yr5'|'Yr6'|'Yr7'|'Yr8'|'Yr9'|'Yr10'|'Yr11'|'Yr12'|'Yr13'|'Yr14'|'Yr15'|'Yr16'|'Yr17'|'Yr18'|'Yr19'|'Yr20'|'Yr21'|'Yr22'|'Yr23'|'Yr24'|'Yr25'|'Yr26'|'Yr27'|'Yr28'|'Yr29'|'Yr30'|"ProjectYear":
                return ArrayType.PROJECT_YEAR
            case _:
                raise InvalidArrayTypeError(
                    f"{self.value} is not a valid LIBRA array variable.")

@dataclass(kw_only=True, slots=True)
class Variable:
    """
    Base data type for LIBRA variables.
    """
    module: Module
    variable: str
    array_vals: list[ArrayValue]
    value: list = field(default_factory=list)
    is_graphical_input: bool = False
    _full_variable_name: str = field(init=False, repr=False)

    def __post_init__(self):
        """
        Validation of input values.
        """
        if self.variable.isspace():
            raise EmptyVariableError("Variable name should be alphanumeric.")
        
        self.module = self._initialize_module()
        self.array_vals = self._initialize_array_vals()
  
        self._full_variable_name = self._construct_full_variable_name()
        if self.array_vals:
            self._full_variable_name = self._construct_full_variable_name(self.array_vals[-1])

    def _construct_full_variable_name(self, end_array_val: ArrayValue = None) -> str:
        """Construct full variable name from its parts."""
        full_variable_name = f"{self.module.value}.{self.variable}"
        if self.array_vals:
            full_variable_name += f"[{self.array_vals[0].value}"
            for val in self.array_vals[1:-1]:
                full_variable_name += f", {val.value}"
            if len(self.array_vals) > 1 and end_array_val is not None:
                if isinstance(end_array_val, str):
                    full_variable_name += f", {end_array_val}"
                else:
                    full_variable_name += f", {end_array_val.value}"
            full_variable_name += "]"
        return full_variable_name

    def _initialize_module(self) -> Module:
        """Initialize a module object from input."""
        return Module(str(self.module).strip())

    def _initialize_array_vals(self) -> list[ArrayValue]:
        """Initialize array value from input."""
        if isinstance(self.array_vals, str):
            return [ArrayValue(array_val.strip()) for array_val in self.array_vals.split(",") if array_val != ""]
        return [ArrayValue(str(array_val).strip()) for array_val in self.array_vals if array_val != ""]

    
