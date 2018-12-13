# 1. Create and Execute a Real Time Report
# An application can request real-time data by calling the get method on the Analytics service object.
# The method requires an ids parameter which specifies from which view (profile) to retrieve data.
# For example, the following code requests real-time data for view (profile) ID 56789.

 # Authorize server-to-server interactions from Google Compute Engine.
#  import httplib2
#  from oauth2client.contrib import gce

#  credentials = gce.AppAssertionCredentials(
#    scope='https://www.googleapis.com/auth/devstorage.read_write')
#  http = credentials.authorize(httplib2.Http())
"""A simple example of how to access the Google Analytics API."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


# def get_results(service, profile_id):
#     # Use the Analytics Service Object to query the Core Reporting API
#     # for the number of sessions within the past seven days.
#     return service.data().ga().get(
#             ids='ga:' + profile_id,
#             start_date='7daysAgo',
#             end_date='today',
#             metrics='ga:sessions').execute()


# def print_results(results):
#     # Print data nicely for the user.
#     if results:
#         print 'View (Profile):', results.get('profileInfo').get('profileName')
#         print 'Total Sessions:', results.get('rows')[0][0]

#     else:
#         print 'No results found'


def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = 'client_secrets.json'

    # Authenticate and construct service.
    service = get_service(
            api_name='analytics',
            api_version='v3',
            scopes=[scope],
            key_file_location=key_file_location)

    profile_id = get_first_profile_id(service)
    print_results(get_results(service, profile_id))


if __name__ == '__main__':
    main()


def get_results(service, profile_id):
try:
  service.data().realtime().get(
      ids='ga:183761831',
      metrics='rt:activeUsers',
      dimensions='rt:medium').execute()

except TypeError, error:
  # Handle errors in constructing a query.
  print ('There was an error in constructing your query : %s' % error)

# except HttpError, error:
#   # Handle API errors.
#   print ('Arg, there was an API error : %s : %s' %
#          (error.resp.status, error._get_reason()))


# 2. Print out the Real-Time Data
# The components of the report can be printed out as follows:

def print_realtime_report(results):
  print '**Real-Time Report Response**' 
  print_report_info(results)
  print_query_info(results.get('query'))
  print_profile_info(results.get('profileInfo'))
  print_column_headers(results.get('columnHeaders'))
  print_data_table(results)
  print_totals_for_all_results(results)

def print_data_table(results):
  print 'Data Table:'
  # Print headers.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%30s' % header.get('name'))
  print ''.join(output)
  # Print rows.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
        output.append('%30s' % cell)
      print ''.join(output)
  else:
    print 'No Results Found'

def print_column_headers(headers):
  print 'Column Headers:'
  for header in headers:
    print 'Column name           = %s' % header.get('name')
    print 'Column Type           = %s' % header.get('columnType')
    print 'Column Data Type      = %s' % header.get('dataType')

def print_query_info(query):
  if query:
    print 'Query Info:'
    print 'Ids                   = %s' % query.get('ids')
    print 'Metrics:              = %s' % query.get('metrics')
    print 'Dimensions            = %s' % query.get('dimensions')
    print 'Sort                  = %s' % query.get('sort')
    print 'Filters               = %s' % query.get('filters')
    print 'Max results           = %s' % query.get('max-results')

def print_profile_info(profile_info):
  if profile_info:
    print 'Profile Info:'
    print 'Account ID            = %s' % profile_info.get('accountId')
    print 'Web Property ID       = %s' % profile_info.get('webPropertyId')
    print 'Profile ID            = %s' % profile_info.get('profileId')
    print 'Profile Name          = %s' % profile_info.get('profileName')
    print 'Table Id              = %s' % profile_info.get('tableId')

def print_report_info(results):
  print 'Kind                    = %s' % results.get('kind')
  print 'ID                      = %s' % results.get('id')
  print 'Self Link               = %s' % results.get('selfLink')
  print 'Total Results           = %s' % results.get('totalResults')

def print_totals_for_all_results(results):
  totals = results.get('totalsForAllResults')
  for metric_name, metric_total in totals.iteritems():
    print 'Metric Name  = %s' % metric_name
    print 'Metric Total = %s' % metric_total