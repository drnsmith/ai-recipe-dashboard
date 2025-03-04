import dash
from dash import dcc, html, Input, Output
import pandas as pd
import sqlite3
from sql_generator import generate_sql_query

# Load dataset (assuming it's a CSV)
df = pd.read_csv("dataset/full_dataset.csv")

# Create an in-memory SQLite database
conn = sqlite3.connect(":memory:")
df.to_sql("recipes", conn, index=False, if_exists="replace")

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("AI-Powered Recipe Explorer"),
    dcc.Input(id="query_input", type="text", placeholder="Ask a question about recipes..."),
    html.Button("Search", id="search_btn"),
    html.Div(id="query_output")
])

@app.callback(
    Output("query_output", "children"),
    Input("search_btn", "n_clicks"),
    Input("query_input", "value")
)
def process_query(n_clicks, user_query):
    if n_clicks and user_query:
        sql_query = generate_sql_query(user_query)  # Convert natural text to SQL
        try:
            result = pd.read_sql_query(sql_query, conn)
            return html.Pre(result.to_string())  # Show results
        except Exception as e:
            return f"Error: {e}"
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
