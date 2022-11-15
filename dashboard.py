import plotly.express as px
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input

df = pd.read_csv("WhatsgoodlyData-10.csv")
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Analysis of User Behavior", style={"textAlign": "center"}),
    html.Hr(),
    html.P("Scroll Down for Full Data Analysis or Choose Segment of interest:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Segment Type', clearable=False,
                     value="Mobile",
                     options=[{'label': x, 'value': x} for x in
                              df["Segment Type"].unique()]),
    ], className="two columns"), className="row"),

    html.Div(id="output-div", children=[]),
])


@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="Segment Type", component_property="value"), )
def make_graphs(segment_chosen):
    # Histogram
    df_hist = df[df["Segment Type"] == segment_chosen]
    fig_hist1 = px.histogram(df_hist, x="Answer", y="Count",
                             title=f"Answers of {segment_chosen} Segment Users",
                             color="Answer",)

    fig_hist2 = px.histogram(df_hist, x="Description Type", y="Count",
                             title=f"Distribution of {segment_chosen} Segment Participants",
                             color="Description Type",)
    # Pie CHART
    fig_pie1 = px.pie(data_frame=df_hist, names="Answer", values="Count",
                      title=f"Share of {segment_chosen} Segment Participants",
                      color="Answer",)  #width=900, height=800)

    fig_pie2 = px.pie(data_frame=df_hist, names="Description Type", values="Count",
                      title=f"Share of {segment_chosen} Segment Participants ",)
                      #width=900, height=800)
    fig_pie2.update_traces(textposition='inside', textinfo='percent+label')

    # # All Answers
    df_fig_all = df.dropna(subset=["Count"])
    fig_all = df_fig_all[df_fig_all["Segment Type"].isin(["Mobile", "Web"])]

    fig_hist_all = px.histogram(fig_all, x="Answer", y="Count",
                                title="Total Number of Each Answer", color="Answer")
    fig_pie_all = px.pie(fig_all, names="Answer", values="Count",
                         title="Share of Total Distribution of Answers", color="Answer")

    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist1)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_pie1)], className="five columns"),
            html.Div([dcc.Graph(figure=fig_hist2)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_pie2)], className="five columns"),
        ], className="row"),
        html.H2("All Answers", style={"textAlign": "center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist_all)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_pie_all)], className="five columns"),
        ], className="row"),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
