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
defaultUser = 'tchinchen@pagerduty.com'
serviceIDs = []

#servicenamenames = ['eCommerce-frontend', 'eCommerce-search', 'eCommerce-payment']
#TeamName = 'eCommerce Support'
#EPName = "eCommerce Engineering"
#token = "M8EKhymNqYr8n6pi_Rfi"
#teamName = "eCommerce Engineering"


servicenamenames = ['Infra-windows', 'Infra-Linux', 'Infra-DB']
TeamName = 'Infra Support'
EPName = "Infra Support"
token = "M8EKhymNqYr8n6pi_Rfi"
teamName = "Infrastructure"

# END: EDIT THESE FOR YOUR SERVICES
#--------------------------------------------------------------------------------------------------




#Set up the default headers for your environment
headers = {'Content-Type': 'application/json',   "Accept": "application/vnd.pagerduty+json;version=2", 'Authorization': "Token token=" + token}
#--------------------------------------------------------------------------------------------------






#--------------------------------------------------------------------------------------------------
#Create a Team for your Service
teamPayload = {
  "team": {
    "type": "team",
    "name": teamName,
    "description": "The team for " + TeamName
  }
}

teamUrl = "https://api.pagerduty.com/teams"

r = requests.post(teamUrl, json=teamPayload, headers=headers)
r.raise_for_status()
teamID = r.json()['team']['id']
print ("Services Created:")
print(teamID)
#--------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------
# Get the default Escalation Policy for your instance
r = requests.get('https://api.pagerduty.com/users?query=' + defaultUser, headers=headers)
userID = r.json()['users'][0]['id']
print(userID)
#--------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------
escPolicyPayload = {
  "escalation_policy": {
    "type": "escalation_policy",
    "name": EPName + " (EP)",
    "escalation_rules": [
      {
        "escalation_delay_in_minutes": 30,
        "targets": [
          {
            "id": userID,
            "type": "user_reference"
          }
        ]
      }
    ],
    "num_loops": 2,
    "teams": [
      {
        "id": teamID,
        "type": "team_reference"
      }
    ],
    "description": "Here is the ep for the engineering team."
  }
}

EPUrl = "https://api.pagerduty.com/escalation_policies"

r = requests.post(EPUrl, json=escPolicyPayload, headers=headers)
r.raise_for_status()
escalationPolicy = r.json()['escalation_policy']['id']
print ("EP Created:")
print(escalationPolicy)
#--------------------------------------------------------------------------------------------------


# Add an Escalation Policy to the Team created - REMOVED as we will add the EP to the Team when created
#r = requests.put("https://api.pagerduty.com/teams/" + teamID + "/escalation_policies/" + escalationPolicy, headers=headers)
#r.raise_for_status()


# Get the default Escalation Policy for your instance
#r = requests.get('https://api.pagerduty.com/escalation_policies?query=default&sort_by=name', headers=headers)
#escalationPolicy = r.json()['escalation_policies'][0]['id']


#--------------------------------------------------------------------------------------------------
for servicename in servicenamenames:
    payload = {"service": {
        "type": "service",
        "name": servicename,
        "description": "Microservice supporting" + servicename,
        "auto_resolve_timeout": 14400,
        "acknowledgement_timeout": 600,
        "status": "active",
        "escalation_policy": {
            "id": escalationPolicy,
            "type": "escalation_policy_reference"
        },
        "team":
        {
            "id": teamID,
            "type": "team_reference"
        },
        "incident_urgency_rule": {
        "type": "use_support_hours",
        "during_support_hours": {
            "type": "constant",
            "urgency": "high"
        },
        "outside_support_hours": {
            "type": "constant",
            "urgency": "low"
        }
        },
        "support_hours": {
        "type": "fixed_time_per_day",
        "time_zone": "Europe/Madrid",
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "days_of_week": [
            1,
            2,
            3,
            4,
            5
        ]
        },
        "scheduled_actions": [
        {
            "type": "urgency_change",
            "at": {
            "type": "named_time",
            "name": "support_hours_start"
            },
            "to_urgency": "high"
        }
        ],
        "alert_creation": "create_alerts_and_incidents",
        "alert_grouping": "time",
        "alert_grouping_timeout": 2
    }
    }

    url = "https://api.pagerduty.com/services"

    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    serviceIDs.append(r.json()['service']['id'])








print ("Services Created:")
print (serviceIDs)
print("Environment Ready")