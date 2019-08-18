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
from oauth2client.service_account import ServiceAccountCredentials

#cgitb.enable()

credentials = ServiceAccountCredentials.from_json_keyfile_dict({
  "type": "service_account",
  "project_id": "realtime-analytics-224018",
  "private_key_id": "fa58579719a2d0a3c1171bcbeb47fe77f33c6c7d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCeY5O6WvFMyppS\nWFoHitFi2DysoAsBsewP672LBi2tM4CuEyb+06u3EAfFbybRqk9HIgOAdiiTytUq\nfl0gbc7hW+UqNUDeu9BEAyakdO8sNuHmoMahtgK2MggXplMVsKe8f1+2TddXPJP5\n36D+gJsEDCJUg35L8q343qcZSxNB1BGqux8n+aI0Big7dRF0LjQEcyfYMiLdWItO\nJ2q9gXJWo4q96xMoxeaKboea05ASOivp6P364jNatFgIX2X8fUbhkZ6UznxlJ7G0\nxF5TVoR00evJQYfCzpJSy4V1shTBas/vBkOX60xg3Q/aetD7fFlUtBpx7PIXRxK5\nwNKBc3QtAgMBAAECggEABebb+FOvLhdWjL7yC9nmV3KLQDtubY+9phI4q9d9GDkV\nEGdySoiEm3ujbn3nymQ4NARWcRD2Dhu+uaifu7ebv9X2wg3d7u68oewkInig+NrK\nrBdNj3UCwNs4Zfkym1pLxcBRRq+72GpPcT4d952/KPVyygdkS1wtk1poi466lvdK\n8P8hhn0WmCx2OWJjYfTIPABf18MvEKzONS5K73j2KZYrZSyKrFPwpEv5TsnfirF8\nNrwIyMeY/jZJJrvaz5/7NVKEDcUJfM41XejSvO55eHvIH9/vhMzDi1Vc2Xs56EUs\nXWkI+3YnLHCUtDIqpkYvK4EYw3v6Ot9KMpQS6IbewQKBgQDVgMgEGvSDc4fIOoRT\nS7MzMfeZQyi/9QU87TH8fo+YR0VIDDNuuqxsF4WMTkLO/9ZIfiwDAUMpVc48D0yc\nqaG6rB3OgbrFmQLA6r9i4G38jOzvRDQ1YVD9cFQDkh5bNM0sTvqRevmc4kWn4kTq\nBD8fW/K/q/P5J32xWsIoZuAVWQKBgQC96mnuOPwzYFtRwzwkOn6MKq/9RUGzA5hn\nHtytls4JmKnYrEXPh51BZTelrRjKqDFDojmSRG5rvhuj8Cl6VbW4hV0GWP2RSLd6\nUQX2cVBFwty+6hqYHzUAbqMZLZSgpuuRUr4ULxDb4ZQkKqX74tB4EKEJyDN/qWPK\nbTk272h29QKBgCDUDW08K86ui/lIriIUqLg9faHORszFQwnsOtxlJXU3uDpszde/\n0lVIhJtfSTyE8BDzfZb0sbwAWpa3j4MjPh/y6R5gqjRJ47eAIO92LNNBZAkiRpjS\nnt5pUDHAXPSPOOEQP8zwyMLLtAQtcYU+I+qRe9DnAruTy+riVqpZryj5AoGBAIXw\n5qbxn8VoRt+Cb08pxgh7LsXUa4KinYDU/lSbUFLqTZeX4GB+R8VQao+5Zgu/1Yba\nyfnDs5DfckUL42T5QAGUZUhNyQAHJgfpTuhBgJjC1sb6+qihEdNtNDBUukcXknpa\nvd4kV6KMFNvxDEF69QZIzBrHDLMTt2KT5887yBRlAoGAAcipRc03kU9Y7OVimV80\n0PLzFhsgCZwmJZL7leHO9q13O1D9AGMVuq4l6CSPfJoqyZLIKinIEoAbWr9OaYf1\nEBclACW/aayzP+GIMBTIPuqkbrjroGuJFTz6peRg40ssON5evYWD/aUpJhLE9EiR\n7sFUu/YBHFTSmvAjbJy7b7s=\n-----END PRIVATE KEY-----\n",
  "client_email": "ptm-hue@realtime-analytics-224018.iam.gserviceaccount.com",
  "client_id": "112492768590743802019",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ptm-hue@realtime-analytics-224018.iam.gserviceaccount.com"
}, scopes=['https://www.googleapis.com/auth/analytics.readonly'])

# Create requests session object (avoids need to pass in headers with every request)
session = requests.Session()
session.headers= {'Authorization': 'Bearer ' + credentials.get_access_token().access_token}

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


def printit():
  threading.Timer(15, printit).start()
  response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs))
  response.raise_for_status()

  print response.raise_for_status()  

  result = response.json() 
  print result

  activeUsers = result['totalsForAllResults']['rt:activeUsers']
  hueIP = '192.168.86.41'
  
  print 'activeUsers: ' + activeUsers

  if activeUsers == '0':
    requests.put('http://'+hueIP+'/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":false}')
  else:
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

getToken()
printit()
