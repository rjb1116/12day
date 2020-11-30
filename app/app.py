from flask import Flask, render_template, request, redirect

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
	return render_template('plot.html', stock=app.vars['stock_ticker'])



if __name__ == '__main__':
  app.run(port=33507)
