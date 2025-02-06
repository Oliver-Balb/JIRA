JIRA Issue Extraction and Email Generator

## Table of Contents

1. [Installation](#installation)
2. [Project Summary](#summary)
3. [Files](#files)
4. [Execution](#execution)

# Installation <a name="installation"></a>

* Unzip the ZIP file
* Python 3.12.* or newer required
* MS Excel required
* MS Outlook (old) required

# Overview<a name="summary"></a>

This "solution" helps to generate personalized emails to recipients based on JIRA Issue data.

Using python program JIRA_extract_issue.py data from JIRA (skyway.porsche.com/jira) can be can be extracted resulting in XLSX file.
The Excel table in this file needs to be copied to DEV_JIRAIssueExtraction.xlsm, worksheet "JIRA data" (do not alter the structure). 
Based on Email-Body the email drafts can be generated. Currently the population of TO, CC and SUBJECT can be adjusted only directly in VBA.

# Files <a name="files"></a>

### Data Files

tbd. 

### Program Files

tbd. 

# Execution <a name="execution"></a>

In order to run JIRA data extraction a user specific API key needs to be added to the JIRA_extract_issue.py.

user = 'vorname.nameb@porsche.de'
apikey = '#####'

To get or renew this access token (API key) go to https://skyway.porsche.com/jira/plugins/servlet/desk/portal/1 > "Access Tokens" > on next screen "Create" > on next screen "JIRA"

tbd.