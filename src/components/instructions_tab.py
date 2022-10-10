from dash import Dash, dcc, html, dash_table
from . import ids
import pandas as pd
import numpy as np


def render(app: Dash) -> dcc.Tab:
    example_df = pd.DataFrame(
        np.array([[1998, 1, -1], [1999, 3.23716, -0.52619],
                 [2000, -0.11721, 0.22196]]),
        columns=["Years",
                 "baseline: Minerals Market.time to have fun[ROW, LFP]",
                 "baseline: Minerals Market.time to have fun[US, LFP]"]
    )
    return dcc.Tab(
        id=ids.INSTRUCTIONS_TAB,
        label="Instructions",
        children=[
            html.H4("Instructions.", style=dict(
                textAlign="center", fontWeight="bold", color="#047cc4")),
            html.Div(
                className="instructions-div",
                children=[
                    dcc.Markdown(
                        """
                        Currently, the dashboard requires the user to upload a CSV file containing outputs from LIBRA simulations in the vertical layout format. An example of the vertical layout format is given below:\n\n
                        """),
                    dash_table.DataTable(example_df.to_dict("records"), [
                                         {"name": i, "id": i} for i in example_df.columns]),
                    dcc.Markdown(
                        """
                        \n\n
                        To run the program, double click on the exe (or unix executable, for Mac OS users). You will first see a command prompt (or terminal) window open up, as shown below.
                        ![image](https://user-images.githubusercontent.com/107583173/194936368-3e2183de-ef33-4bc6-a3b8-1ba8c56691c5.png)

                        To view the dashboard, open a browser of your choice and navigate to the URL shown in the command prompt (in this case, http://127.0.0.1:8050). You will be able to see the dashboard.
                        To visualize the results, just upload (or drag and drop) your CSV and click on "Upload". The plots can be viewed in the first and second tabs within the app. The variables to plot can be selected from the "Plot settings" tab.

                        To exit the dashboard, close the browser tab and then close the command prompt (or terminal) that was first launched.

                        Please email any feedback, comments or questions to Debajyoti.Debnath@nrel.gov.

                        """
                    )
                ]
            ),
        ]
    )
