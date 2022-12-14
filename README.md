# LIBRA_dashboard_plotly

A simple dashboard to visualize outputs from LIBRA (Lithium-Ion Battery Resource Assessment Model, https://www.nrel.gov/transportation/libra.html) simulations, made using Plotly and Dash. To use, download the executable (LIBRA-dashboard_x.x.x.exe for Windows and LIBRA-dashboard_x.x.x for MacOS/ Linux users) from https://www.github.com/dweigl/LIBRA_dashboard_plotly/releases.

Currently, the dashboard requires the user to upload a CSV file containing outputs from LIBRA simulations in the vertical layout format. An example of the vertical layout format is given below:

| Years | baseline: Minerals Market.time to have fun[ROW, LFP] | baseline: Minerals Market.time to have fun[US, LFP] |
| ----- | ---------------------------------------------------- | --------------------------------------------------- |
| 1998  | 1                                                    | -1                                                  |
| 1999  | 3.23716                                              | -0.52619                                            |
| 2000  | -0.11721                                             | 0.22196                                             |

To run the program, double click on the exe (for Windows users). You will first see a command prompt (or terminal) window open up, as shown below.
![image](https://user-images.githubusercontent.com/107583173/194936368-3e2183de-ef33-4bc6-a3b8-1ba8c56691c5.png)

In Mac OS, download the executable (the file called LIBRA-dashboard_x.x.x, not the one with the exe), open a terminal and run the following commands : 
```
cd folder/where/you/downloaded/the/executable
./LIBRA-dashboard_x.x.x
```
If running into errors with permissions while trying to run the executable, run the command `chmod +x ./LIBRA_dashboard_x.x.x` to modify the file permissions for the executable to add permission to run the executable to your user account.

To view the dashboard, open a browser of your choice and navigate to the URL shown in the command prompt (in this case, http://127.0.0.1:8050). You will be able to see the dashboard.

To visualize the results, just upload (or drag and drop) your CSV and click on "Upload". The plots can be viewed in the first and second tabs within the dashboard. The variables to plot can be selected from the "Plot settings" tab.


To exit the dashboard, close the browser tab and then close the command prompt (or terminal) that was first launched.

### Dependencies

```
numpy
pandas
plotly
dash
dash-bootstrap-components
```

### Dependencies

```
numpy
pandas
plotly
dash
dash-bootstrap-components
```

### Creating a virtual environment and installing dependencies

If using Anaconda 3 or Miniconda, navigate to the `environment` directory and execute the command
`conda env create --file environment.yml`.

If not using Anaconda, you can use `venv`. Navigate to the downloaded dashboard GitHub repo directory and execute `python -m venv .venv`. Then, if on Windows, execute `.venv\Scripts\activate.bat` to activate the environment (`source .venv/bin/activate` if you are on MacOS or Linux). Finally, navigate to the `environment` directory and execute `pip install -r requirements.txt` to install all dependencies.

Please email any feedback, comments or questions to Dustin.Weigl@nrel.gov or Debajyoti.Debnath@nrel.gov.
