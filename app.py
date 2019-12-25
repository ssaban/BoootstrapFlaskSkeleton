#!/usr/bin/env python
from pprint import pprint
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap

from helper.timeline.timeline_builder import TimelineBuilder
from os import environ, path
import os
import time
import pwd
import sys


top_menue_descriptor = [
    {
        'top_menue_item':'About',
        'help':'Activity to provide overall info about the app',
        'verbose':'text to describe the about menue item',
    },
    {
        'top_menue_item':'SetTimeline',
        'help':'Use of Google Charts timeline widget to create project timeline',
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
bootstrap = Bootstrap(app)



#prevent caching
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
@app.route('/home',methods = ['POST', 'GET'])
def home():
    return render_template('bs_index.html')

@app.route('/about')
def about():
    return render_template('about.html',top_menue_items = top_menue_descriptor)

@app.route('/t-menue-3')
@app.route('/t-menue-4')
def menue_item():
    return render_template('menue_item.html',page_title = 'T-MENUE<>')



@app.route('/t-menue-2')
def t_2():
    #return render_template('home.html',team = team_1)
    return render_template('test_timeline_fixed_ranges.html')



@app.route('/SetTimeline',methods = ['POST', 'GET'])
def SetTimeline():

    print ("in SetTimeLine\n")
    if request.method == 'POST':
        print ("in SetTimeline - POST\n")

        timelineCmd = request.form

        if not 'RadioForEventUpdate' in timelineCmd.keys():
            print ("no need to set CalEvent\n")
            set_cal_event = 'off'
        else:
            set_cal_event = timelineCmd['RadioForEventUpdate']


        print ("???????????????????????????     DATA PASSED FOR SetTimeline")
        pprint(timelineCmd)


        store_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "static/js/timeline"
        result_file = store_dir + os.sep + "timeline.js"
        #header = "timeline  Log Generated on: {}".format(time.ctime(os.path.getctime(result_file)))

        print ("1========================================= before TimelineBuilder\n")
        tlb = TimelineBuilder(store_dir)


        print ("2========================================= before getCachedTimeline\n")
        tlb.getCachedTimeline("timeline")

        tlb.processTimelineOp(timelineCmd['RadioForProductUpdate'],
                           timelineCmd['Product'],
                           timelineCmd['Build'],
                           timelineCmd['SmtBuildDate'],
                           set_cal_event,
                           timelineCmd['Event'],
                           timelineCmd['EventStart'],
                           timelineCmd['EventEnd'],

                              )

        print ("3=========================================== FlushTimeLineCacheToFile\n")
        tlb.flushTimelineCacheToFile("timeline")



    return render_template('bs_setTimeline.html',title = 'Timeline')






if __name__=='__main__':
    app.run(debug=True)