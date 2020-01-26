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


@app.route('/t-menue-2')
def t_2():
    #return render_template('home.html',team = team_1)
    return render_template('test_timeline_fixed_ranges.html')



@app.route('/GTimeline',methods = ['POST', 'GET'])
def SetTimeline():

    print ("in SetTimeLine\n")
    if request.method == 'POST':
        print ("in SetTimeline - POST\n")

        timelineCmd = request.form


        if not 'RadioForBlackoutEventUpdate' in timelineCmd.keys():
            print ("no need to set CalEvent\n")
            set_cal_event = 'off'
        else:
            set_cal_event = timelineCmd['RadioForBlackoutEventUpdate']


        print ("???????????????????????????     DATA PASSED FOR SetTimeline")
        pprint(timelineCmd)



        store_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + "static/js/timeline"
        result_file = store_dir + os.sep + "timeline.js"
        #header = "timeline  Log Generated on: {}".format(time.ctime(os.path.getctime(result_file)))

        print ("1========================================= before TimelineBuilder\n")
        tlb = TimelineBuilder(store_dir)


        print ("2========================================= before getCachedTimeline\n")
        tlb.getCachedTimeline("timeline")

        tlb.processTimelineOp(timelineCmd['RadioForTimeLineLaneUpdate'],
                              timelineCmd['LaneName'],
                              timelineCmd['Event'],
                              timelineCmd['EventStartDate'],
                              timelineCmd['EventEndDate'],
                              set_cal_event,
                              timelineCmd['BlackoutEvent'],
                              timelineCmd['BlackOutStart'],
                              timelineCmd['BlackOutEnd'])






        print ("3=========================================== FlushTimeLineCacheToFile\n")
        tlb.flushTimelineCacheToFile("timeline")



    return render_template('bs_setTimeline.html',title = 'GTimeline')






if __name__=='__main__':
    app.run(debug=True)