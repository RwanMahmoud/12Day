#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import os
from flask import Flask,render_template,request,redirect
import quandl

import pandas as pd
import requests
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components
from bokeh.embed import file_html
from bokeh.resources import CDN




app = Flask(__name__)

# Define a function that make a Bokeh plot
def build_plot(ticker,plot_type,month):

    


    api_key=#api_key
    url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES?ticker={}&api_key={}'.format(ticker,api_key)
    res = requests.get(url)
    x=res.json()
    columns_names=['ticker','date','open','high','low','close','volume','ex-dividend','split-ratio','adj_open','adj_high','adj_low','adj_close','adj_volume']

    months = {'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,
              'September':9,'October':10,'November':11,'December':12}


    df = pd.DataFrame(x['datatable']['data'])
    df.columns=columns_names
    df['date'] = pd.to_datetime(df['date']) #to change into pandas Date type
    df['year'] = pd.DatetimeIndex(df['date']).year 
    df['month'] = pd.DatetimeIndex(df['date']).month 

    df=df.sort_values(by=['date'],ascending=False)
    df=df[df['year']==2017]
    df=df[df['month']==months[month]]
        
        
    plotting=df[plot_type]
    date=df['date']

    #add plot
    p=figure(
        title='QUANDL WIKI EOD Stock Prices - {}, 2017'.format(month),
        x_axis_label='date',
        x_axis_type='datetime'
        )

        ##render glyph
    p.line(date,plotting,legend='{}:{}'.format(ticker,plot_type),line_width=2)


    return p
    


@app.route('/')
def index_ticker():
    return render_template('ticker_info.html')
    
        
   
@app.route('/next_ticker', methods = ['POST'])   
def next_ticker():
    ticker=request.form['ticker']
    plot_type=request.form['plot_type']
    month=request.form['month']
    
    

    plot = build_plot(ticker,plot_type,month)
    
    script, div = components(plot)
    
    return render_template("plot.html", script=script,div=div)
    

    



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
