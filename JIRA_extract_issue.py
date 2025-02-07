from datetime import datetime
from jira import JIRA, JIRAError
import pandas as pd
import sys
from dotenv import dotenv_values


"""
Further packages required to pip install:
openpyxl
"""

""" Constants - General """

base_api_url = "https://api.skyway.porsche.com/jira"
base_frontend_url = "https://skyway.porsche.com/jira/"

user = 'oliver.balb@porsche.de'

secrets = dotenv_values("C:/Users/balbol/OneDrive - Dr. Ing. h.c. F. Porsche AG/Documents/_FIG3/P51/Automation/prg/JIRA/.env")
# To renew apkikey access token go to https://skyway.porsche.com/jira/plugins/servlet/desk/portal/1 > "Access Tokens" > on next screen "Create" > on next screen "JIRA"
# Update the apikey in the secrets file .env specified above:
# apikey=EnVN*************************VNOj
apikey = secrets['apikey']  # 16.01.2025, 09:00 

server = base_api_url

now = datetime.now()
FILEPATH = 'C:/Users/balbol/OneDrive - Dr. Ing. h.c. F. Porsche AG/Documents/_FIG3/P51/Automation/data/'
FILENAME = f"{now.strftime('%Y%m%d-%H%M%S')}_JIRAIssueExtraction.xlsx"
SEPARATOR = ";"

def convert_name_format(input_string):
    
    lastname = ""
    firstname = ""
    department = ""


    try:            
        # Split the input string by comma and space
        parts = input_string.split(', ')
        
        # Extract lastname and firstname
        lastname = parts[0].strip()
        firstname = parts[1].split(' (')[0].strip()
        department = parts[1].split('(')[1][:-1].strip()

    except:
        lastname = input_string
        
    return firstname, lastname, department


def convert_datestring(in_string, srcfmt, tgtfmt):

    formatted_date_str = None    
    
    if in_string:
        # Convert the string to a datetime object
        date_obj = datetime.strptime(in_string, srcfmt)

        # Convert the datetime object to the desired format
        formatted_date_str = date_obj.strftime(tgtfmt)

    return formatted_date_str

def cleanse_issue_assignee(issue_key, in_assignee):
    """ Check if there is an entry for assignee and extract display name"""
    out_assignee_displayName = ""
    out_assignee_emailAddress = ""
    out_assignee_firstname = ""
    out_assignee_lastname = ""
    out_assignee_department = ""
    if (in_assignee and in_assignee.displayName != "Deactivated account"):
        out_assignee_displayName = in_assignee.displayName
        out_assignee_emailAddress = in_assignee.emailAddress
        out_assignee_firstname, out_assignee_lastname, out_assignee_department = convert_name_format(in_assignee.displayName)
        return out_assignee_displayName, out_assignee_emailAddress, out_assignee_firstname, out_assignee_lastname, out_assignee_department
    else:
       print(f"{issue_key}|ERROR|Assignee is empty") 

def cleanse_issue_relatedpersons(issue_key, in_related_persons):
    """ Check if there is an entry for related person and extract display name"""
    out_related_persons_displayNames = None 
    out_related_persons_emailAddresses = None
    if in_related_persons:
        count = 0
        for related_person in in_related_persons:
            if related_person.displayName != "Deactivated account":
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
    if in_components: 
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

    try:
       jira = JIRA(options, token_auth=apikey)
    except JIRAError as e:
        if e.status_code == 401:
            print('Authentication error - renew apikey access token: Go to https://skyway.porsche.com/jira/plugins/servlet/desk/portal/1',
                  '> "Access Tokens" > on next screen "Create" > on next screen "JIRA"')
            sys.exit(1)  # Exit the program with a non-zero status code
        else:
            print(f"An error occurred: {e}")
            sys.exit(1)  # Exit the program with a non-zero status code

    # Provide valid JQL query here:
    
    # .. ITIKS Tickets 2025 Identifizierungskontrollen
    # jira_jql = 'labels = P51 and project = itiks and Lead =2025 and labels = P51 and issuekey != ITIKS-4273 and summary ~ Identifikation order by Department asc'
    
    # .. ITIKS Tickets 2025 Einhaltung der Hauptabteilungen, OHNEe Tickets mit Status COMPLETED
    jira_jql = 'labels = P51 and project = itiks and Lead =2025 and issuekey != ITIKS-4273 and status != Completed  order by Department asc' 
    
    # .. ITQM 1st Line Tickets - nur Hauptabteilungen
    # jira_jql = 'project = ITQM AND component = p51 AND labels in (2024) and labels in (Übereinkunft) and department not in (FDO, FDB, FDE, MA) order by Department ASC'
    
    # .. ITQM Status Tracking 1st Line - Reminder Emails:
    # jira_jql = 'project = ITQM AND status != Fixed AND component = p51 AND labels in (2024) and labels in (Übereinkunft) order by Department ASC'
    
    # .. Sonstige
    # jira_jql = 'project = ITQM AND component = p51'
    # jira_jql = 'project = ITQM AND component = p51 AND labels in (2024)'
    # jira_jql = 'key in (ITQM-204, ITQM-189)'
    # jira_jql = 'key in (ITQM-95, ITQM-101)'
    

    try: 
        issues = jira.search_issues(jira_jql)
    except JIRAError as e:
        if e.status_code == 401:
            print('Authentication error - renew apikey access token: Go to https://skyway.porsche.com/jira/plugins/servlet/desk/portal/1',
                  '> "Access Tokens" > on next screen "Create" > on next screen "JIRA"')
            sys.exit(1)  # Exit the program with a non-zero status code
        else:
            print(f"An error occurred: {e}")
            sys.exit(1)  # Exit the program with a non-zero status code


    df_issues = pd.DataFrame()

    for issue in issues:
        
        new_issue = {}
        """ Extract and Cleanse relevant issue data  """
        new_issue['key'] = issue.key
        new_issue['url'] = base_frontend_url + 'browse/' + issue.key
        new_issue['id'] = issue.id
        new_issue['issuetype'] = issue.fields.issuetype.name
        new_issue['priority'] = issue.fields.priority
        new_issue['duedate'] = convert_datestring(issue.fields.duedate, srcfmt = "%Y-%m-%d", tgtfmt="%d.%m.%Y")
        new_issue['created'] = issue.fields.created
        new_issue['updated'] = issue.fields.updated
        new_issue['summary'] = issue.fields.summary          
        result = cleanse_issue_assignee(issue.key, issue.fields.assignee)
        if result is not None:
            new_issue['assignee_displayname'], new_issue['assignee_emailaddress'], new_issue['assignee_firstname'], new_issue['assignee_lastname'], new_issue['assignee_department'] = result
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
            
        """
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
        """
        
    df_issues.to_excel(FILEPATH + FILENAME)
        
    print(df_issues)
       
def main():
    process_JIRA_issue()

if __name__ == "__main__":
    main()