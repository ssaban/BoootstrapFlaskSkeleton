from pprint import pprint
import sys
import os
from shutil import copyfile
import pwd
from datetime import datetime
import csv
import re
import importlib

importlib.reload(sys)

header = '''
google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var container = document.getElementById('timeline');
    var chart = new google.visualization.Timeline(container);
    var dataTable = new google.visualization.DataTable();


    dataTable.addColumn({ type: 'string', id: 'Project' });
    dataTable.addColumn({ type: 'string', id: 'Event' });
    dataTable.addColumn({ type: 'date', id: 'Start' });
    dataTable.addColumn({ type: 'date', id: 'End' });

    dataTable.addRows([
'''

footer = '''
]);


    var options = {
      timeline: {    colorByRowLabel : 'True',
                     groupByRowLabel : 'True',
                     rowLabelStyle: {fontName: 'Helvetica', fontSize: 8, color: '#603913' },
                     barLabelStyle: { fontName: 'Garamond', fontSize: 8 } }
    };

     chart.draw(dataTable, options);
    }
'''

footer_1 = '''
]);


    var options = {
      timeline: {    colorByRowLabel : 'True',
                     groupByRowLabel : 'True',
                     rowLabelStyle: {fontName: 'Helvetica', fontSize: 8, color: '#603913' },
                     barLabelStyle: { fontName: 'Garamond', fontSize: 8 } }
    };

     chart.draw(dataTable, options);

     nowLine('test_tl');

     google.visualization.events.addListener(chart, 'onmouseover', function(obj){
  	    if(obj.row == 0){
    	   $('.google-visualization-tooltip').css('display', 'none');
		}
        nowLine('test_tl');
     })

     google.visualization.events.addListener(chart, 'onmouseout', function(obj){
  	   nowLine('test_tl');
     })

}

function nowLine(div){
//get the height of the timeline div
	var height;
    $('#' + div + ' rect').each(function(index){
  	  var x = parseFloat($(this).attr('x'));
      var y = parseFloat($(this).attr('y'));

      if(x == 0 && y == 0) {height = parseFloat($(this).attr('height'))}
  })

'''

'''
work_dir is name of temp dir storing generated results 
'''


class TimelineBuilder():
    def __init__(self, work_dir):
        self.store_dir = work_dir
        print("store dir is {}".format(self.store_dir))

        self.timelineMap = {}  # empty map to keep time line for all event_lanes
        self.calendarEventMap = {}  # empty map to keep calendar events (holidays, WWDC ect)
        self.cached_timeline = False

    ''' 
    tlb.updateTimelinedata(timelineCmd['RadioForevent_laneUpdate'],
                           timelineCmd['event_lane'],
                           timelineCmd['event'],
                           timelineCmd['eventeventDate'])

    '''

    def parseDate(self, event_event_date):
        event_start = [0, 0, 0]
        # safari date provided in format MM/DD/YYYY
        # chrome date provided in format YYYY-MM-DD
        print("BEFORE RE")
        m = re.match(r'(\d*)\D*(\d*)\D*(\d*).*$', event_event_date)
        print("AFTER  RE")
        pprint(m)
        if len(m.group(1)) == 4:
            # process format YYYY-MM-DD
            mm = int(m.group(2))
            mm -= 1
            event_start = [str(m.group(1)), str(mm), str(m.group(3))]
        elif len(m.group(1)) == 2:
            # process format MM/DD/YYYY
            mm = int(m.group(1))
            mm -= 1
            event_start = [str(m.group(3)), str(mm), str(m.group(2))]
        else:
            print("PROCESSING DATE IN FORMAT >{}<".format(event_event_date))
            print("ERROR Group1 {}  is un supported length {} ".format(m.group(1), len(m.group(1))))
            return False, event_start

        return True, event_start

    def validDateRange(self, s, e):
        if int(e[0]) > int(s[0]):
            return True  # year e > year s
        if int(e[0]) < int(s[0]):
            return False  # year s > year e
        # check s, e on same year
        if int(e[1]) >= int(s[1]):
            return True
        if int(e[1]) < int(s[1]):
            return False
        if int(e[2]) >= int(s[2]):
            return True

        return False

    def b_mm_dd(self, b, mm, dd):
        month = int(mm) + 1
        t = "{} ({}/{})".format(b, str(month), dd)
        return t

    def processTimelineOp(self,
                          op_type,
                          timeline_lane,
                          tl_event,
                          event_start_date,
                          event_end_date,
                          setBlackoutEvent,
                          blackoutEvent,
                          blackoutEventStartDate,
                          blackoutEventEndDate ):




        print("HANDLE UPDATE / DELETE CALENDAR EVENT HERE ==================")
        if setBlackoutEvent == 'update':
            print("EVENT {}   START {}   END {}".format(blackoutEvent, blackoutEventStartDate, blackoutEventEndDate))

            valid_start_date, e_start = self.parseDate(blackoutEventStartDate)
            valid_end_date, e_end = self.parseDate(blackoutEventEndDate)
            if valid_start_date and valid_end_date:
                if self.validDateRange(e_start, e_end):
                    print("VALID EVENT DATE  - Processing \n")
                    # self.updateCalendarEventMap('EVENTS',
                    self.updateCalendarEventMap('\\0',
                                                blackoutEvent,
                                                e_start,
                                                e_end)
                else:
                    print("IGNORE - END DATE {} EARLIER TNEN START DATE {}\n".format(e_end, e_start))
            else:
                print("IGNORE - NON VALID END DATE >{}< OR START DATE >{}<\n".format(e_end, e_start))
        elif setBlackoutEvent == 'remove':
            print("REMOVE EVENT {}\n".format(blackoutEvent))
            # if 'EVENTS' in self.calendarEventMap.keys():
            if '\\0' in list(self.calendarEventMap.keys()):
                if blackoutEvent in self.calendarEventMap['\\0']:
                    # self.calendarEventMap['EVENTS'].pop(blackoutEvent)
                    self.calendarEventMap['\\0'].pop(blackoutEvent)

        else:
            print("NO CAL EVENT ACTION\n")

        print(">>>>>>>>>>>>>>>>>>>>>>>STORED EVENTS\n")
        pprint(self.calendarEventMap)
        print(">>>>>>>>>>>>>>>>>>>>>>>STORED EVENTS\n")

        print("process op <{}> for timeline_lane {} tl_event {} on event lane_event DATE {}".format(op_type, timeline_lane, tl_event,
                                                                                    event_start_date))

        op_type = str(op_type)
        timeline_lane = str(timeline_lane)


        tl_event = str(tl_event)
        valid_date, event_start = self.parseDate(event_start_date)
        valid_date, event_end = self.parseDate(event_end_date)

        print("CACHED TIMELINE")
        pprint(self.timelineMap)

        print("op type is <{}>".format(op_type))

        print(timeline_lane)
        print(event_start)

        if op_type in 'update':
            print("UPDATE")
            if valid_date:
                self.updateTimelineMap(timeline_lane, tl_event, event_start, event_end)
        if op_type in 'remove':
            print("REMOVE")
            if timeline_lane:
                if tl_event:
                    print("REMOVE ONLY tl_event FROM TIMELINE_LANE")
                    self.timelineMap[timeline_lane].pop(tl_event)
                else:
                    print("REMOVE timeline_lane")
                    timeline_lane = str(timeline_lane)
                    print("remove timeline_lane {}".format(timeline_lane))
                    pprint(self.timelineMap.pop)
                    print("REMOVE timeline_lane - MAP AFTER POP")
                    self.timelineMap.pop(timeline_lane)

                    pprint(self.timelineMap.pop)
            else:
                print("ADD ERROR CONDITION - DO NOT SUPPORT REMOVE ENTIER TIMELINE")

    '''
            updateTimelineMap
            add a tiemline record to the map
            dates are in format [yyyy,mm,dd]

        '''

    def updateCalendarEventMap(self, event,
                               event_name,
                               event_start,
                               event_end):

        event = str(event)
        event_name = str(event_name)

        print("IN updateCalendarEventMap for event <{}> event name<{}> ".format(event, event_name))

        if not event in list(self.calendarEventMap.keys()):
            self.calendarEventMap[event] = {}
            self.calendarEventMap[event][event_name] = {}
        else:
            event_map = self.calendarEventMap[event]
            if not event_name in list(event_map.keys()):
                self.calendarEventMap[event][event_name] = {}

        self.calendarEventMap[event][event_name]['event_start_date'] = event_start
        self.calendarEventMap[event][event_name]['event_end_date'] = event_end

        pprint(self.calendarEventMap)

    def updateTimelineMap(self, event_lane,
                          lane_event_name,
                          event_start,
                          event_end):

        event_lane = str(event_lane)
        lane_event_name = str(lane_event_name)

        # check if lane_event name is already in format of
        # {} ({}/{})".format(b,str(month),dd)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& >{}<\n".format(lane_event_name))
        m = re.match(r'(\S*)(.*$)', lane_event_name)
        lane_event_name = m.group(1)
        bd = m.group(2)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& >{}<  >{}<\n".format(lane_event_name, bd))

        # lane_event name might be in format lane_event_name(mm/dd)
        # hash only keep lane_event name
        # m = re.match(r'(.*)*\s\(.*\).*$', lane_event_name)
        # print m
        # lane_event_name = m.group(1)

        print("IN updateTimelineMap for event_lane <{}> lane_event name<{}> ".format(event_lane, lane_event_name))

        if not event_lane in list(self.timelineMap.keys()):
            self.timelineMap[event_lane] = {}
            self.timelineMap[event_lane][lane_event_name] = {}
        else:
            event_lane_map = self.timelineMap[event_lane]
            if not lane_event_name in list(event_lane_map.keys()):
                self.timelineMap[event_lane][lane_event_name] = {}

        self.timelineMap[event_lane][lane_event_name]['event_start_date'] = event_start
        self.timelineMap[event_lane][lane_event_name]['event_end_date'] = event_end

        event_date_suffix = self.b_mm_dd(lane_event_name, event_start[1], event_start[2])
        self.timelineMap[event_lane][lane_event_name]['date_sufix'] = event_date_suffix

    '''
        getCachedTimeLine
        read the existing cached timeline to a dictionary 
    '''

    def getCachedTimeline(self, chached_timeline_file):

        print("+++++++++++++++ EXTRACT TIMELINE CACHED IN {}".format(chached_timeline_file))

        body = ""
        i = 0

        fn = "{}.js".format(chached_timeline_file)
        fullpath_name = self.store_dir + os.sep + fn

        if os.path.isfile(fullpath_name):
            with open(fullpath_name, "r") as f:
                l = f.readline()
                cnt = 1

                while l:
                    # print("Line {}: {}".format(cnt, l.strip()))
                    m = re.match(
                        r'\s*\[\s*\'([^\']*)\'[^\']*\'([^\']*)\'\s*,\s*new\s* Date\s*\((\d*),\s*(\d*),\s*(\d*)\)\s*,\s*new\s*Date\s*\((\d*),\s*(\d*),\s*(\d*)\).*$',
                        l)
                    if m:
                        # print "FOUND MATCH ________"

                        # if m.group(1) == 'EVENTS' :
                        if m.group(1) == '\\0':
                            self.updateCalendarEventMap(m.group(1),  # event_lane
                                                        m.group(2),  # lane_event_name,
                                                        [m.group(3), m.group(4), m.group(5)],  # event start
                                                        [m.group(6), m.group(7), m.group(8)])
                        else:

                            self.updateTimelineMap(m.group(1),  # event_lane
                                                   m.group(2),  # lane_event_name,
                                                   [m.group(3), m.group(4), m.group(5)],  # event start
                                                   [m.group(6), m.group(7), m.group(8)])

                        # print m.groups()
                    l = f.readline()
                    cnt += 1

                print("========================================CACHED TIMELINE and Events\n")
                pprint(self.timelineMap)
                pprint(self.calendarEventMap)
                print("===================Clean Non Defined Dates from Cache\n")
                for p in list(self.timelineMap.keys()):
                    event_lane_map = self.timelineMap[p]
                    print("check event_lane {} in hash".format(p))
                    for b in list(event_lane_map.keys()):
                        print("check lane_event {} in hash".format(b))
                        event_map = event_lane_map[b]
                        print("event start key valeu {}   of b {}\n".format(event_map['event_start_date'], b))
                        if event_map['event_start_date'] == ['0', '0', '0']:
                            print("NOT VALID DATE - REMOVE")
                            self.timelineMap[p].pop(b)

                print("========== Clean Cacheed TIMELINE\n")
                pprint(self.timelineMap)








        else:
            print("Empty cache")

    def flushTimelineCacheToFile(self, chached_timeline_file):
        body = ""

        fn = "{}.js".format(chached_timeline_file)
        fn_cpy = "{}.backup.js".format(chached_timeline_file)
        fullpath_name = self.store_dir + os.sep + fn
        fullpath_cpy_name = self.store_dir + os.sep + fn_cpy

        if os.path.isfile(fullpath_name):
            os.remove(fullpath_name)
        else:
            copyfile(fullpath_name, fullpath_cpy_name)

        f = open(fullpath_name, "w")
        #f.write(header.encode("utf8"))
        f.write(header)


        print("START SAVING EVENTS\n")
        pprint(self.calendarEventMap)

        line = "[ '\\0','Now', new Date(), new Date() ],"
        line += "\n"
        body += line

        for eg in list(self.calendarEventMap.keys()):
            eg_map = self.calendarEventMap[eg]
            for e in list(eg_map.keys()):
                ms = eg_map[e]
                line = "[ '{}','{}', new Date({}, {}, {}), new Date({}, {}, {}) ],".format(eg,
                                                                                           e,
                                                                                           ms['event_start_date'][0],
                                                                                           ms['event_start_date'][1],
                                                                                           ms['event_start_date'][2],
                                                                                           ms['event_end_date'][0],
                                                                                           ms['event_end_date'][1],
                                                                                           ms['event_end_date'][2])
                line += "\n"
                body += line

        for p in list(self.timelineMap.keys()):
            p_map = self.timelineMap[p]
            for b in list(p_map.keys()):
                ms = p_map[b]
                # event_and_date = "{} {}/{}".format(b,str(int(ms['event_start_date'][1])+1),ms['event_start_date'][2])
                line = "[ '{}','{}', new Date({}, {}, {}), new Date({}, {}, {}) ],".format(p,
                                                                                           # b,
                                                                                           ms['date_sufix'],
                                                                                           ms['event_start_date'][0],
                                                                                           ms['event_start_date'][1],
                                                                                           ms['event_start_date'][2],
                                                                                           ms['event_end_date'][0],
                                                                                           ms['event_end_date'][1],
                                                                                           ms['event_end_date'][2])
                line += "\n"
                body += line

        body = body[:-2]
        #f.write(body.encode("utf8"))
        f.write(body)

        mf1 = re.sub(r"\btest_tl\b", chached_timeline_file, footer_1)
        #f.write(mf1.encode("utf8"))
        f.write(mf1)

        body = ""
        # get all the events defined
        print("calendarEventMap is :\n")
        pprint(self.calendarEventMap)
        for eg in list(self.calendarEventMap.keys()):
            eg_map = self.calendarEventMap[eg]
            # TODO - add NOW dynamically from GUI
            eg_map['Now'] = 1

            print("event group map is \n")
            pprint(eg_map)
            for e in list(eg_map.keys()):
                print("{} EVENT IS ".format(e))
                line = "var {}Word = $('#' + div + ' text:contains(\"{}\")');".format(e, e)
                print("{}".format(line))

                line += "\n"
                body += line

                line = "{}Word.prev().first().attr('height', height + 'px').attr('y', '0');   ".format(e)

                line += "\n"
                body += line

        body = body[:-2]

        #f.write(body.encode("utf8"))
        f.write(body)

        #f.write("\n}".encode("utf8"))
        f.write("\n}")

        f.close()





