import subprocess
import sys
from datetime import datetime, timedelta
from falconpy import APIHarness
 
# Do not hardcode API credentials!
falcon = APIHarness(client_id="YOUR_CLIENT_ID",
                    client_secret="YOUR_SECRET_ID"
                    )
 
def get_ad_computers():
    command = """
    Get-ADComputer -Filter * -Properties PasswordLastSet |
    Where {$_.Passwordlastset -ge (Get-date).AddDays(-45)} |
    Select-Object Name |
    Format-Table -HideTableHeaders
    """
    result = subprocess.run(["powershell", "-Command", command], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')
 
def cs_get_hostids(filter = ""):
    PARAMS = {
        'offset': 0,
        'limit': 500,
        'sort': "hostname.asc",
        'filter': filter
    }
 
    response = falcon.command('QueryDevicesByFilter', parameters=PARAMS)
    return response['body']['resources']
 
def cs_get_hostdetails(host_ids):
    response = falcon.command("GetDeviceDetails", ids=host_ids)
    return response['body']['resources']
 
def check_rogues(ad_computers, host_details):
    # Normalize and extract hostnames from host_details
    hostnames_in_details = [item['hostname'].strip().lower() for item in host_details]
 
    # Normalize ad_computers
    ad_computers_normalized = [hostname.strip().lower() for hostname in ad_computers]
 
    # Finding hostnames that are in ad_computers but not in hostnames_in_details
    rogue_hostnames = [hostname for hostname in ad_computers_normalized if hostname not in hostnames_in_details]
 
    return rogue_hostnames
 
 
# Define optional FQL filter to find hosts in environment
today = datetime.today()
filter_date = today - timedelta(days=30)
filter_date = filter_date.strftime("%Y-%m-%d")
filter = f"last_seen:>='{filter_date}'"
 
# Get a list of computer accounts from AD
ad_computers = get_ad_computers()
if len(ad_computers) == 0:
    print("No computers found in AD, exiting")
    sys.exit()
else:
    print(f"Found {len(ad_computers)} computers in AD")
 
# Get a list of host_ids , optionally pass a filter to cs_get_hostids function
target_hosts = cs_get_hostids()
if len(target_hosts) == 0:
    print("No CrowdStrike hosts found, exiting")
    sys.exit()
else:
    print(f"Found {len(target_hosts)} hosts in CrowdStrike \n")
 
# Create a list of dictionaries with full details for each host
host_details = cs_get_hostdetails(target_hosts)
 
# Check for hosts seen in AD that are not seen in CrowdStrike
rogue_hostnames = check_rogues(ad_computers, host_details)
print(f"Found {len(rogue_hostnames)} rogue hosts")
for rogue in rogue_hostnames:
    print(rogue)
    