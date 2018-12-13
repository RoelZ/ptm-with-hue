"""
Using "requests" to access Google Analytics Realtime Reporting API from python service
NOTE on google docs: The realtime reporting docs have samples for google-api-python-client. 
**They do not work** at the time of this writing. The GA docs sample seems to refer to features that don't actually exist.
In any case, the new RR API is restfull and requests is a pleasent library so here is how to use it instead.
pip requirements: oauth2client, requests
"""
import httplib2
import json
import requests
# import urllib2
import threading 
from oauth2client.service_account import ServiceAccountCredentials

credentials = ServiceAccountCredentials.from_json_keyfile_dict({
  "type": "service_account",
  "project_id": "realtime-analytics-224018",
  "private_key_id": "",
  "private_key": "",
  "client_email": "ptm-hue@realtime-analytics-224018.iam.gserviceaccount.com",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ptm-hue@realtime-analytics-224018.iam.gserviceaccount.com"
}, scopes=['https://www.googleapis.com/auth/analytics.readonly'])

# Create requests session object (avoids need to pass in headers with every request)
session = requests.Session()
session.headers= {'Authorization': 'Bearer ' + credentials.get_access_token().access_token}

# Enjoy!
url_kwargs = {
    # GA:PROD
    #'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:activeUsers'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}
# Interactions
url_kwargs_2 = {
    # GA:PROD
    #'view_id': 162569474,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'view_id': 183761831,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
    'get_args': 'metrics=rt:totalEvents&dimensions=rt:eventCategory,rt:eventAction'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
}


# print result['totalResults']

# payload = '{"on":true}'

# if result['totalResults'] > 0:
#   requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/1/state', data=payload)

# r.content

def printit():
  threading.Timer(5, printit).start()
  response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs))
  response.raise_for_status()
  result = response.json() 
  activeUsers = result['totalsForAllResults']['rt:activeUsers']
  
  print 'activeUsers: ' + activeUsers

  if activeUsers == '0':
    requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":false}')
  if activeUsers == '1':
    requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":50}')
  if activeUsers == '2':
    requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":100}')
  if activeUsers == '3':
    requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":150}')
  if activeUsers == '4':
    requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":200}')
  if activeUsers != '0' and activeUsers != '1' and activeUsers != '2' and activeUsers != '3' and activeUsers != '4':
    requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"on":true,"bri":254}')


  response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs_2))  
  response.raise_for_status()
  result = response.json()   
  
  
  totalActions = True if "rows" in result else False
  
  
  if totalActions == True:
    for dest in result['rows']:
      addToCart = True if 'Add to Cart' in dest else False
      
    print addToCart
    if addToCart == True:
      requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":46920}')      
    else:
      requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"hue":8597,"sat":121}')

      # editor = True if 'Editor' in dest else False
      # if editor == True:
      #   requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":25500}')
      # payment = True if 'Checkout step 2' in dest else False
      # if payment == True:    
      #   requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"sat":254,"hue":0}')
  
  # print editor
  # print payment

  # if editor in locals() and addToCart in locals() and payment in locals():
    # requests.put('http://192.168.1.11/api/f2u4vQ3e-79Zh8iYoUJthdGBmmGeMG2B98fmKXx7/lights/4/state', data='{"hue":8597,"sat":121}')



printit()


# 0 = UIT
# 1 = 50
# 2 = 100
# 3 = 150
# 4 = 200
# 5 - 254