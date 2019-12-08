#!/usr/bin/env python
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for


top_menue_descriptor = [
    {
        'top_menue_item':'About',
        'help':'Activity to provide overall info about the app',
        'verbose':'text to describe the about menue item',
    },
    {
        'top_menue_item':'t-menue-1',
        'help':'Activity to provide overall info about t-menue-1 ',
        'verbose':'text to describe this menue item',
    },
    {
        'top_menue_item':'t-menue-2',
        'help':'Activity to provide overall info about t-menue-2',
        'verbose':'text to describe this menue item',
    },
    {
        'top_menue_item':'t-menue-3',
        'help':'Activity to provide overall info about t-menue-3',
        'verbose':'text to describe this menue item',
    }
]



app = Flask(__name__)


@app.route('/')
@app.route('/home',methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html',top_menue_items = top_menue_descriptor)


@app.route('/t-menue-1')
@app.route('/t-menue-2')
@app.route('/t-menue-3')
@app.route('/t-menue-4')
def menue_item():
    return render_template('menue_item.html',page_title = 'T-MENUE<>')




if __name__=='__main__':
    app.run(debug=True)