import time
import requests
from jira import JIRA
import csv
import pandas as pd

"""
Further packages required to pip install:
openpyxl
"""

""" Constants - General """

base_api_url = "https://api.skyway.porsche.com/jira"
base_frontend_url = "https://skyway.porsche.com/jira/"

user = 'oliver.balb@porsche.de'
apikey = 'cmEHnoGP7wvsR1E8lR3TFpF6XYw2QafUqsFrHm'
server = base_api_url

FILEPATH = 'C:/Users/balbol/OneDrive - Dr. Ing. h.c. F. Porsche AG/Documents/_FIG3/P51/Automation/data/'
FILENAME = f"{time.strftime('%Y%m%d-%H%M%S')}_JIRAIssueExtraction.xlsx"
SEPARATOR = ";"

def cleanse_issue_assignee(issue_key, in_assignee):
    """ Check if there is an entry for assignee and extract display name"""
    out_assignee_displayName = None 
    out_assignee_emailAddress = None
    if in_assignee:
        out_assignee_displayName = in_assignee.displayName
        out_assignee_emailAddress = in_assignee.emailAddress
    else:
       print(f"{issue_key}|ERROR|Assignee is empty") 
    return out_assignee_displayName, out_assignee_emailAddress

def cleanse_issue_relatedpersons(issue_key, in_related_persons):
    """ Check if there is an entry for assignee and extract display name"""
    out_related_persons_displayNames = None 
    out_related_persons_emailAddresses = None
    count = 0
    for related_person in in_related_persons:
        if count != 0:
            out_related_persons_displayNames = out_related_persons_displayNames + SEPARATOR + related_person.displayName
            out_related_persons_emailAddresses = out_related_persons_emailAddresses + SEPARATOR + related_person.emailAddress
        else:
            out_related_persons_displayNames = related_person.displayName
            out_related_persons_emailAddresses = related_person.emailAddress
        count = count + 1
        
    return out_related_persons_displayNames, out_related_persons_emailAddresses

def cleanse_issue_reporter(issue_key, in_reporter):
    """ Check if there is an entry for assignee and extract display name"""
    out_reporter = None
    if in_reporter:
        out_reporter = in_reporter.displayName
    else:
       print(f"{issue_key}|ERROR|Reporter is empty") 
    return out_reporter

def cleanse_issue_organization(issue_key, in_organization):
    """ Extract organization from dictionary and check if Organization is populated """
    out_organization = None
    if in_organization:
        out_organization = in_organization[0].value
    else:
        print(f"{issue_key}|WARNING|Organization is empty")
    return out_organization

def cleanse_issue_components(issue_key, in_components):
    """ Extract components """
    out_components = None
    count = 0
    for component in in_components:
        if count != 0:
            out_components = out_components + SEPARATOR + component.name
        else:
            out_components = component.name
        count = count + 1
    return out_components
          
"""" Request JIRA issue and extract required data """
def process_JIRA_issue():

    options = {
    'server': server
    }

    jira = JIRA(options, token_auth=apikey)

    # jira_url = 'project = "PROD: IT Quality Assessment Center" AND issuetype = "Test Plan" and reporter=balbol'
    jira_url = 'key in (ITQM-204, ITQM-189)'
    # jira_url = 'key in (XSXO001LP2-530)'

    issues = jira.search_issues(jira_url)

    df_issues = pd.DataFrame()

    for issue in issues:
        
        new_issue = {}
        """ Extract and Cleanse relevant issue data  """
        new_issue['key'] = issue.key
        new_issue['url'] = base_frontend_url + 'browse/' + issue.key
        new_issue['id'] = issue.id
        new_issue['issuetype'] = issue.fields.issuetype.name
        new_issue['created'] = issue.fields.created
        new_issue['updated'] = issue.fields.updated
        new_issue['summary'] = issue.fields.summary          
        new_issue['assignee_displayname'], new_issue['assignee_emailaddress'] = cleanse_issue_assignee(issue.key, issue.fields.assignee)
        new_issue['stakeholder_displaynames'], new_issue['stakeholder_emailaddresses'] = cleanse_issue_relatedpersons(issue.key, issue.fields.customfield_11010)
        new_issue['participant_displaynames'], new_issue['participant_emailaddresses'] = cleanse_issue_relatedpersons(issue.key, issue.fields.customfield_12300)
        new_issue['reporter'] = cleanse_issue_reporter(issue.key, issue.fields.reporter)
        new_issue['status'] = issue.fields.status
        new_issue['resolution'] = issue.fields.resolution
        new_issue['resolutiondate'] = issue.fields.resolutiondate
        new_issue['components'] = cleanse_issue_components(issue.key, issue.fields.components)
        new_issue['organization'] = cleanse_issue_organization(issue.key,issue.fields.customfield_11011)
        #   new_issue['Issue Links'] = issue.fields.issuelinks

        df_new_issue = pd.DataFrame([new_issue])
        df_issues = pd.concat([df_issues, df_new_issue], ignore_index=True)        
            
        print(f"Key:\t\t\t{new_issue['key']}")
        print(f"ID:\t\t\t{new_issue['id']}")
        print(f"IssueType:\t\t{new_issue['issuetype']}") 
        print(f"Created:\t\t{new_issue['created']}")
        print(f"Updated:\t\t{new_issue['updated']}")
        print(f"Summary:\t\t{new_issue['summary']}")           
        print(f"Assignee:\t\t{new_issue['assignee_emailaddress']}")
        print(f"Reporter:\t\t{new_issue['reporter']}")  
        print(f"Status:\t\t\t{new_issue['status']}")
        print(f"Components:\t\t{new_issue['components']}") 
        print(f"Organization:\t\t{new_issue['organization']}")
        print(f"Resolution:\t\t{new_issue['resolution']}")
        print(f"Resolution Date:\t{new_issue['resolutiondate']}")
        print(f"Type of new_issue:\t{type(new_issue)}")

        print("---------------------")
        
    df_issues.to_excel(FILEPATH + FILENAME)
        
    print(df_issues)
       
def main():
    process_JIRA_issue()

if __name__ == "__main__":
    main()