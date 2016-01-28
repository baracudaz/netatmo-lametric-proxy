# PythonAPI LaMetric REST data access
# coding=utf-8

import json
import urllib2

# Common definitions

_BASE_URL       = "https://developer.lametric.com/"
_PUSH_URL       = _BASE_URL + "api/V1/dev/widget/update/com.lametric."

class Setup(object):

    def __init__(self):
        self.data = {}
        self.data['frames'] = []
        self.index = 0

    def addTextFrame(self, icon, text):
        frame = {}
        frame['index'] = self.index
        frame['icon']  = icon
        frame['text']  = text
        self.data['frames'].append(frame)
        self.index += 1

    def addGoalFrame(self, icon, start, current, end, unit):
        frame = {}
        frame['index'] = self.index
        frame['icon']  = icon
        frame['goalData'] = {}
        frame['goalData']['start'] = start
        frame['goalData']['current'] = start
        frame['goalData']['end'] = start
        frame['goalData']['unit'] = unit
        self.data['frames'].append(frame)
        self.index += 1

    def addSparklineFrame(self, data):
        frame = {}
        frame['index'] = self.index
        frame['chartData'] = data
        self.data['frames'].append(frame)
        self.index += 1
    
    def push(self, app_id, access_token):
        #print json.dumps(self.data,ensure_ascii=False)
        opener = urllib2.build_opener();
        headers = { 'Accept': 'application/json', 'Cache-Control': 'no-cache', 'X-Access-Token': access_token };
        request = urllib2.Request(_PUSH_URL + app_id, json.dumps(self.data,ensure_ascii=False), headers);
        try:
            response = opener.open(request);
        except urllib2.HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
            print e.read()
        except urllib2.URLError as e:
            print('Failed to reach a server.')
            print('Reason: ', e.reason)
            print e.read()
        #else:
            # everything is fine

