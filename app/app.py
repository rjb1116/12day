from flask import Flask, render_template, request, redirect
import requests
import json
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
import datetime

app = Flask(__name__)

app.vars = {}

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html', num=1)
	elif request.method == 'POST':
		app.vars['stock_ticker'] = request.form['stock_ticker_input']
		return redirect('/plot')

@app.route('/plot', methods=['GET','POST'])
def plot():

	

	key = 'S0D1315IPQVMPSX0'
	ticker = app.vars['stock_ticker']
	url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)
	response = requests.get(url).json()
	df = pd.DataFrame(response["Time Series (Daily)"]).transpose().reset_index().rename(columns={'index':'date'})
	df['date'] = pd.to_datetime(df['date'])

	#filter df
	df = df[df['date'] > datetime.datetime.now() - pd.to_timedelta("30day")]

	
	#Bokeh plot
	TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
	fig = figure(plot_width=600, plot_height=600, tools=TOOLS, x_axis_type="datetime")
	fig.line(
		#x=df['4. close'].values.tolist(),
		#y=df['4. close'].values.tolist()
		x=df['date'],
		y=df['5. adjusted close']
	)

	# grab the static resources
	js_resources = INLINE.render_js()
	css_resources = INLINE.render_css()

	# render template
	script, div = components(fig)
	html = render_template(
		'plot.html',
		stock=app.vars['stock_ticker'],
		plot_script=script,
		plot_div=div,
		js_resources=js_resources,
		css_resources=css_resources,
	)
	return html
	


if __name__ == '__main__':
  app.run(port=33507)
