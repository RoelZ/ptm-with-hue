"""
Using "requests" to access Google Analytics Realtime Reporting API from python service
NOTE on google docs: The realtime reporting docs have samples for google-api-python-client. 
**They do not work** at the time of this writing. The GA docs sample seems to refer to features that don't actually exist.
In any case, the new RR API is restfull and requests is a pleasent library so here is how to use it instead.
pip requirements: oauth2client, requests
"""
#import cgi
#import cgitb
import sys
import httplib2
import json
import requests
import threading
import datetime
from oauth2client.service_account import ServiceAccountCredentials

#cgitb.enable()

with open('credentials.json') as f:
    data = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(data, scopes=['https://www.googleapis.com/auth/analytics.readonly'])

# Create requests session object (avoids need to pass in headers with every request)
# session = requests.Session()
# session.headers= {'Authorization': 'Bearer ' + credentials.get_access_token().access_token}

def getToken():
  global session 
  session = requests.Session()
  session.headers= {'Authorization': 'Bearer ' + credentials.get_access_token().access_token}


# Enjoy!
url_kwargs = {
    # GA:PROD
    'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    #'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
# Interactions
url_kwargs_2 = {
    # GA:PROD
    'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    #'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers&dimensions=rt:goalid&filters=rt:goalid==2'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
url_kwargs_3 = {
    # GA:PROD
    'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    #'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers&dimensions=rt:goalid&filters=rt:goalid==3'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
url_kwargs_4 = {
    # GA:PROD
    'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    #'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers&dimensions=rt:goalid&filters=rt:goalid==4'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
url_kwargs_5 = {
    # GA:PROD
    'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    #'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers&dimensions=rt:goalid&filters=rt:goalid==5'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
url_kwargs_6 = {
    # GA:PROD
    'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    #'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers&dimensions=rt:goalid&filters=rt:goalid==6'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}

# class StoppableThread(threading.Thread):
#    def __init__(self):
# 	super(StoppableThread, self).__init__()
# 	self._stop_event = threading.Event()

#    def stop(self):
# 	self._stop_event.set()

#    def stopped(self):
# 	return self._stop_event.is_set()

def tijdCheck():
  datum = datetime.datetime.now()
  dag = datetime.date.today().weekday()
  print datum

  # let op dat de tijd 2 uur achterloopt op de raspberry pi
  if dag<5:
    # door de weekse dag
    if (datum.hour>5 and datum.hour<7 or datum.hour>15 and datum.hour<19):
      printit()
      print 'doordeweeksedag actief '
    else:
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":false}')
      threading.Timer(15, tijdCheck).start()
      print 'doordeweeksedag inactief '
  else: 
    # weekend
    if (datum.hour>7 and datum.hour<21):
      printit()
      print 'weekend actief '
    else:
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":false}')
      threading.Timer(15, tijdCheck).start()
      print 'weekend inactief '

def printit():  

  threading.Timer(15, tijdCheck).start()

  response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs))

  if response.status_code != 200 or response.raise_for_status(): 
    getToken()

  # print response.raise_for_status()  
  print response.status_code

  result = response.json() 
  print result

  activeUsers = result['totalsForAllResults']['rt:activeUsers']
  
  global hueIP
  hueIP = '192.168.86.41'
  
  print 'activeUsers: ' + activeUsers

  if activeUsers == '0':
    requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":false}')
  else:
    # Editor
    response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_2))  
    response.raise_for_status()
    result = response.json()   
    editorAction = result['totalsForAllResults']['rt:activeUsers']

    print 'editorAction: ' + editorAction
  
    # Add to Cart  
    response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_3))  
    response.raise_for_status()
    result = response.json()   
    AddtoCartAction = result['totalsForAllResults']['rt:activeUsers']

    print 'AddtoCartAction: ' + AddtoCartAction

    # Checkout  
    response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_5))  
    response.raise_for_status()
    result = response.json()   
    checkoutAction = result['totalsForAllResults']['rt:activeUsers']

    print 'checkoutAction: ' + checkoutAction

    # Payment
    response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_6))  
    response.raise_for_status()
    result = response.json()   
    paymentAction = result['totalsForAllResults']['rt:activeUsers']

    print 'paymentAction: ' + paymentAction

    # Order  
    response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_4))  
    response.raise_for_status()
    result = response.json()   
    orderAction = result['totalsForAllResults']['rt:activeUsers']
  
    print 'orderAction: ' + orderAction

# groen: 25500
# blauw: 46920
# geel:  8570
# paars: 48860
# roze:  55996
# rood:  0


    if editorAction != '0' and AddtoCartAction == '0' and checkoutAction == '0' and paymentAction == '0' and orderAction == '0':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":8570}')   # geel
  
    if AddtoCartAction != '0' and checkoutAction == '0' and paymentAction == '0' and orderAction == '0':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":48860}')   # paars

    if checkoutAction != '0' and paymentAction == '0' and orderAction == '0':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":55996}')   # roze
    
    if paymentAction != '0' and orderAction == '0':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":46920}')   # blauw

    if orderAction != '0':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":0}')       # rood


    # Default color
    if editorAction == '0' and AddtoCartAction == '0' and checkoutAction == '0' and paymentAction == '0' and orderAction == '0':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"hue":8597,"sat":121}') 


    if activeUsers == '1' or activeUsers == '2':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":50}')
    if activeUsers == '3' or activeUsers == '4':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":100}')
    if activeUsers == '5' or activeUsers == '6':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":150}')
    if activeUsers == '7' or activeUsers == '8':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":200}')
    if activeUsers != '0' and activeUsers != '1' and activeUsers != '2' and activeUsers != '3' and activeUsers != '4' and activeUsers != '5' and activeUsers != '6' and activeUsers != '7' and activeUsers != '8':
      requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":254}')

getToken()
printit()
# threading.Timer(15, tijdCheck).start()
