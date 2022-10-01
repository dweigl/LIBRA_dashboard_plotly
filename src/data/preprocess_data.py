import io
import base64
import pandas as pd
from src.plotting_functions.plotting_functions_plotly import fix_col_names

def preprocess_data(contents: bytes) -> pd.DataFrame:
    decoded = base64.b64decode(contents.split(',')[1])
    df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), index_col=0)
    fix_col_names(df)
    return df