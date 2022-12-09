"""
Plotly Dash based LIBRA dashboard
"""
from dash import Dash
from dash_bootstrap_components import themes
from src.components.layout import create_layout

def main():
    app = Dash(external_stylesheets=[themes.SPACELAB])
    app.title = "LIBRA Dashboard (based on LIBRA v2.2)"
    app.layout = create_layout(app)
    app.run_server(debug=False, host='127.0.0.1', port=8050)

if __name__=="__main__":
    main()
