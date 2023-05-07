import os
import requests
from datetime import datetime, timedelta

# JIRA server information
JIRA_SERVER = "https://jira.iress.com"
JIRA_USERNAME = ""
JIRA_PASSWORD = ""  

# Set up date range for search
today = datetime.now().strftime("%Y-%m-%d")
three_month_ago = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

# JIRA search API endpoint
JIRA_API_SEARCH = f"{JIRA_SERVER}/rest/api/2/search"

# JQL query to search for TMGDL tickets created in the three month
jql_query = f"project = TMGDL and created >= {three_month_ago} and created <= {today}"

# Set up headers and authentication for JIRA REST API call
headers = {
    "Accept": "application/json"
}
auth = (JIRA_USERNAME, JIRA_PASSWORD)

# Make REST API call to JIRA to search for TMGDL tickets
response = requests.get(JIRA_API_SEARCH, headers=headers, auth=auth, params={"jql": jql_query})

# Check for successful response and save ticket keys to a text file
if response.status_code == 200:
    data = response.json()
    issues = data.get("issues", [])
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.expanduser('~'), 'Desktop', 'Python Scripts','JIRA TMGDL Reports')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save ticket keys to text file
    output_file_path = os.path.join(output_dir, 'tmgdl_tickets_3_months.txt')
    with open(output_file_path, 'w') as f:
            f.write('Ticket Key\tCreated Date\tResolved Date\tAssignee\treporter\tstatus\n')
            for issue in issues:
             ticket_key = issue["key"]
             created_date = issue["fields"]["created"]
             resolved_date = issue["fields"].get("resolutiondate", "N/A")
             # assignee = issue["fields"]["assignee"]  #This gives too much info
             assignee = issue['fields']['assignee']['name'] if issue['fields']['assignee'] is not None else "N/A"
             reporter = issue['fields']['reporter']['name'] if issue['fields']['reporter'] is not None else "N/A"
             status = issue["fields"]["status"]["name"]
             f.write(f"{ticket_key}\t{created_date}\t{resolved_date}\t{assignee}\t{reporter}\t{status}\n")

    print(f"Successfully saved ticket keys to file: {output_file_path}")
else:
    print(f"Error {response.status_code}: {response.text}")  
