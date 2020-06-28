from flask import Flask, render_template, request, redirect
import pandas as pd
from bokeh.plotting import figure, output_file, output_notebook, show
# from bokeh.layouts import row,column
from bokeh.embed import components


app = Flask(__name__)

def buildplot(ticker,bdays,h=0,l=0,o=0,c=1):
    api="E63Q4X6XMEZL2UVL"
    ticker = ticker.upper()
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
    url += ticker+'&apikey='+api+"&datatype=csv"
    a=pd.read_csv(url)
    a.timestamp=pd.to_datetime(a.timestamp)
    if bdays>99:
        bdays=99
    x=a.timestamp[bdays:0:-1]
    yhigh=a.high[bdays:0:-1]
    ylow=a.low[bdays:0:-1]
    yopen=a.open[bdays:0:-1]
    yclose=a.close[bdays:0:-1]
    
    output_file("./templates/stockreport.html")
    p1 = figure(title=ticker+" Stock Price",x_axis_label="date",x_axis_type='datetime',y_axis_label="price")

    if h:
        p1.line(x,yhigh,legend_label="high",line_width=2, line_color="blue")
    if l:
        p1.line(x,ylow,legend_label="low",line_width=2, line_color="orange")#, line_dash="4 4")
    if o:
        p1.line(x,yopen,legend_label="open",line_width=2,line_color="green")
    if c:
        p1.line(x,yclose,legend_label="close",line_width=2, line_color="purple")
#     show(p1)
    return p1

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/',methods=['POST',"GET"])
# def my_form_post():
#     if request.method=="POST":
# #         print(request.form)
#         ticker=request.form['ticker']
#         try:
#             h=request.form['High']
#         except:
#             h=0
#         try:
#             l=request.form['Low']
#         except:
#             l=0
#         try:
#             o=request.form['Open']
#         except:
#             o=0
#         try:
#             c=request.form['Close']
#         except:
#             c=0

# #         h,l,o,c=request.form['High'],request.form()['Low'],request.form()['Open'],request.form()['Close']
# #         print(request.form)

#         buildplot(ticker,h,l,o,c)
# #         buildplot("TSLA",1,1,1,0)
#         return render_template('stockreport.html') 
    
# @app.route('/stockreport')
# def about():
#     return render_template('stockreport.html')

@app.route('/')
def index():
    
    ticker = request.args.get("ticker")
    if request.args.get("ticker") == None:
        ticker = "KO"
    
    bdays = request.args.get("bdays")
    if request.args.get("bdays") == None:
        bdays = 30
    else:
        bdays = int(bdays)
    
    h = request.args.get("High")
    if request.args.get("High") == None:
        h = 0
    l = request.args.get("Low")
    if request.args.get("Low") == None:
        l = 0
    o = request.args.get("Open")
    if request.args.get("Open") == None:
        o = 0
    c = request.args.get("Close")
    if request.args.get("Close") == None:
        c = 1
#     print(ticker,h,l,o,c)
    
    plot = buildplot(ticker,bdays,h,l,o,c)
    
    script,div=components(plot)

    return render_template('index.html',script=script,div=div,ticker=ticker,bdays=bdays,h=h,l=l,o=o,c=c)   

if __name__ == '__main__':
    app.run(port=33507)
