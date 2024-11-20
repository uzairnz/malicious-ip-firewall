import requests
import csv
import subprocess
import ipaddress

# Function to validate IP
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

# Fetch blocklist
try:
    response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv")
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching IP blocklist: {e}")
    exit()

# Clear previous rules
for direction in ["In", "Out"]:
    rule = f"netsh advfirewall firewall delete rule name='BadIP_{direction}'"
    subprocess.run(["Powershell", "-Command", rule])

# Parse CSV and collect valid IPs
valid_ips = []
mycsv = csv.reader(filter(lambda x: not x.startswith("#"), response.text.splitlines()))
for row in mycsv:
    if len(row) > 1:
        ip = row[1]
        if is_valid_ip(ip):
            valid_ips.append(ip)
        else:
            print(f"Invalid IP skipped: {ip}")

# Add rules for inbound and outbound traffic
if valid_ips:
    ip_list = ",".join(valid_ips)
    for direction in ["In", "Out"]:
        rule = f"netsh advfirewall firewall add rule name='BadIP_{direction}' Dir={direction} Action=Block RemoteIP={ip_list}"
        subprocess.run(["Powershell", "-Command", rule])
        print(f"Added {direction.lower()} rule blocking {len(valid_ips)} IPs.")
else:
    print("No valid IPs found to block.")
