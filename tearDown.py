######
# To run in Python3:
# python3 -m pip install pytz
# python3 -m pip install requests
# Should also run in Default Python 2.7!
######
import requests
import datetime
import time
import pytz
import sys

#--------------------------------------------------------------------------------------------------
# EDIT THESE FOR YOUR SERVICES
defaultUser = 'pagerduty_account_email'
token = "token_here"
# END: EDIT THESE FOR YOUR SERVICES
#--------------------------------------------------------------------------------------------------

#Set up the default headers for your environment
headers = {'Content-Type': 'application/json',   "Accept": "application/vnd.pagerduty+json;version=2", 'Authorization': "Token token=" + token}
#--------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------
#Delete Services
r = requests.get('https://api.pagerduty.com/services?time_zone=UTC&sort_by=name', headers=headers)

for servicename in r.json()['services']:
    print("Deleting: " + servicename['id'])
    requests.delete('https://api.pagerduty.com/services/' + servicename['id'], headers=headers)
    

#--------------------------------------------------------------------------------------------------
#Delete EPs
r = requests.get('https://api.pagerduty.com/escalation_policies', headers=headers)

for EPName in r.json()['escalation_policies']:
    print("Deleting (EP): " + EPName['id'])
    requests.delete('https://api.pagerduty.com/escalation_policies/' + EPName['id'], headers=headers)


#--------------------------------------------------------------------------------------------------
#Delete EPs
r = requests.get('https://api.pagerduty.com/teams', headers=headers)

for team in r.json()['teams']:
    print("Deleting (Team): " + team['id'])
    requests.delete('https://api.pagerduty.com/teams/' + team['id'], headers=headers)