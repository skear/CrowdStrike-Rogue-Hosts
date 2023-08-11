# CrowdStrike-Rogue-Hosts
Script to discover rogue hosts in a CrowdStrike environment

I created this script to automate the process demonstrated in the CrowdStrike support video Rogue Discovery with Real Time Response
https://supportportal.crowdstrike.com/s/article/Rogue-Discovery-with-RTR-Video

The script runs a powershell command to obtain a list of computers from active directory.  It then connects to the CrowdStrike hosts API ot obtain a list of all active Falcon sensors in the environment.  It then checks for "rogues" or hosts that exist in AD but are not found in the CrowdStrike Falcon console.

# How to use the script
To run the script you will need the FalconPy package.

https://pypi.org/project/crowdstrike-falconpy/

pip install crowdstrike-falconpy

You will also need to create a CrowdStrike API key

https://falcon.crowdstrike.com/api-clients-and-keys/

Then edit the script and replace YOUR_CLIENT_ID and YOUR_SECRET_ID with your API info.
