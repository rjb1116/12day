import requests
import json
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure, show
from bokeh.resources import INLINE

def pretty_print_response(response):
	print(json.dumps(response, indent=2, sort_keys=True))

key = 'S0D1315IPQVMPSX0'
ticker = 'AAPL'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
response = requests.get(url).json()

df = pd.DataFrame(response["Time Series (Daily)"]).transpose().reset_index().rename(columns={'index':'date'})

df['date'] = pd.to_datetime(df['date'])

print(df['date'])

#Bokeh plot
TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
fig = figure(plot_width=600, plot_height=600, tools=TOOLS, x_axis_type="datetime")
fig.line(
	#x=df['4. close'].values.tolist(),
	#y=df['4. close'].values.tolist()
	x=df['date'],
	y=df['4. close']
)

show(fig)

