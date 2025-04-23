import pandas as pd
import sqlite3
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

conexao = sqlite3.connect("db/loja.db")
script = "SELECT * FROM PRODUTOS"
dados = pd.read_sql(script, conexao)

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="dropdown-selecao",
                options=[{"label": i, "value": i} for i in dados["FORNECEDOR"].unique()],
                multi=True,
                className="dbc",
                style={"backgroundColor": "#222", "color": "#000"}
            ), width=4
        ),
        dbc.Col([dcc.Graph(id="fig_forn_por_qtd")], width=7, className="mb-2"),
        dbc.Col([dcc.Graph(id="fig_forn_por_vlr")], width=6, className="mb-2"),
    ]),
    dbc.Row(dbc.Col([dcc.Graph(id="fig_nome_por_qtd")]))
])

@app.callback(
    Output("fig_forn_por_qtd", "figure"),
    Output("fig_forn_por_vlr", "figure"),
    Output("fig_nome_por_qtd", "figure"),
    Input("dropdown-selecao", "value"),
    prevent_initial_call=True
)
def atualiza_dash(fornecedores): 
    
    # Filtro dos Fornecedores
    
    dados_forn = dados[dados["FORNECEDOR"].isin(fornecedores)]
    
    # Graficos de Barra

    forn_por_qtd = dados_forn.groupby("FORNECEDOR")["QTDPROD"].sum().reset_index()
    fig_forn_por_qtd = px.bar(forn_por_qtd, x="FORNECEDOR", y="QTDPROD", color="FORNECEDOR")
    fig_forn_por_qtd.update_layout(template="plotly_dark", showlegend=False)
    
    # Graficos de Pizza

    forn_por_vlr = dados_forn.groupby("FORNECEDOR")["VLRPROD"].sum().reset_index()
    fig_forn_por_vlr = px.pie(forn_por_vlr, names="FORNECEDOR", values="VLRPROD", hole=0.5)
    fig_forn_por_vlr.update_layout(template="plotly_dark")
    
    # Graficos de Barra

    nome_por_qtd = dados_forn.groupby("NOMEPROD")["QTDPROD"].sum().reset_index()
    fig_nome_por_qtd = px.bar(nome_por_qtd, x="NOMEPROD", y="QTDPROD", color="NOMEPROD")
    fig_nome_por_qtd.update_layout(template="plotly_dark", showlegend=False)

    return fig_forn_por_qtd, fig_forn_por_vlr, fig_nome_por_qtd

if __name__ == "__main__":
    app.run(debug=True)
