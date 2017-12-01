import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import datetime

# Requires the bitstamp.csv
print('Loading Data')
bitcoinData = pd.read_csv('../data/bitstamp.csv')
count = 0
time = []
closingPrice = []
# The data set has entries per minute, so lets trim that down to weekly:
for _, b in bitcoinData.iterrows():
    if count % (1440 * 7) == 0:
        time.append(datetime.datetime.fromtimestamp(b['Timestamp']).strftime('%Y-%m-%d'))
        closingPrice.append(b['Close'])
    count = count + 1
print('Data Loaded.')

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.H1('Bitcoin Price over Time'),
    dcc.Graph(
        id='bitcoin-graph',
        figure=go.Figure(
            data=[
                go.Scatter(
                    x=time,
                    y=closingPrice,
                    name='Closing Price',
                    mode = 'lines'
                )
            ],
            layout=go.Layout(
                title='Bitcoin Closing Price versus Volume',
                yaxis=dict(
                    title='Price in USD'
                )
            )
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)