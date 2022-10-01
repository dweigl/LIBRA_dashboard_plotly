"""
Parser for LIBRA inputs and constants
"""

import re
import pprint
from basedatatypes import Variable

pp = pprint.PrettyPrinter()
modules = [
        "Battery_Market", 
        "Minerals_Market", 
        "RIRA",  
        "Cathode", 
        "Manufacturing", 
        "HydroPyro", 
        "DirectRecycle", 
        "LDV", 
        "LCV", 
        "MHDV", 
        "EBus",
        "BES"
    ]

all_parsed_data = dict.fromkeys(modules)

input_file_path = "./Equations.txt"

with open(input_file_path, "r") as f:
    module_pattern = re.compile(r"[a-zA-Z\_]+:") 
    variable_pattern = re.compile(r"([\w\s$%/-]+)(\[[\w\s,]+\])? = ([0-9\.]+|GRAPH\(TIME\))\n") 
    lines = iter(f.readlines())
    line = next(lines)
    while (line):
        finds = module_pattern.findall(line)
        vars = variable_pattern.findall(line)
        if len(finds) == 1 and finds[0][:-1] in modules:
            module = finds[0][:-1]
            all_parsed_data[module] = []
        if vars and not("INIT " in vars[0][0]):
            parsed_var = Variable(
                    module=re.sub(r"_", " ", module), 
                    variable=vars[0][0].strip(), 
                    array_vals=[array_val.strip() for array_val in vars[0][1][1:-1].split(",")]\
                        if vars[0][1] else "",
                    value=float(vars[0][2]) if vars[0][2] != "GRAPH(TIME)" else 0.0)
            if vars[0][2] == "GRAPH(TIME)":
                line = next(lines)
                tuple_pattern = re.compile(f"\([\d\.]+, [\d\.]+\)")
                parsed_var.value = [(float(value[1:-1].split(",")[0].strip()), \
                    float(value[1:-1].split(",")[1].strip())) for value in tuple_pattern.findall(line)]
            all_parsed_data[module].append(parsed_var) 
        try:
            line = next(lines)
        except StopIteration as e:
            break

for module in modules:
    print(module)
    print()
    pp.pprint(all_parsed_data[module])
    print("\n\n")
        
    
