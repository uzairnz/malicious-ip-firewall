import requests
import subprocess
import json
import ipaddress

# URL for the Spamhaus DROP list in NDJSON format
DROP_LIST_URL = "https://www.spamhaus.org/drop/drop_v4.json"

# Function to validate IP ranges
def is_valid_ip_range(ip_range):
    try:
        ipaddress.ip_network(ip_range, strict=False)
        return True
    except ValueError:
        return False

# Function to fetch and parse the DROP list
def fetch_drop_list():
    try:
        response = requests.get(DROP_LIST_URL)
        response.raise_for_status()
        ip_ranges = []
        for line in response.text.splitlines():
            try:
                data = json.loads(line)
                if "cidr" in data and is_valid_ip_range(data["cidr"]):
                    ip_ranges.append(data["cidr"])
                else:
                    print(f"Skipping invalid IP range: {data.get('cidr', 'N/A')}")
            except json.JSONDecodeError as e:
                print(f"Skipping invalid line: {line} - Error: {e}")
        return ip_ranges
    except requests.RequestException as e:
        print(f"Error fetching the Spamhaus DROP list: {e}")
        return None

# Function to delete rules created by this script
def delete_existing_rules():
    for direction in ["In", "Out"]:
        print(f"Deleting existing {direction.lower()} rules created by the script...")
        # Use PowerShell to list existing rules
        list_rules_cmd = f'Get-NetFirewallRule -DisplayName "Spamhaus_Drop_{direction}_*" | Remove-NetFirewallRule'
        result = subprocess.run(["Powershell", "-Command", list_rules_cmd], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error deleting {direction.lower()} rules: {result.stderr.strip()}")
        else:
            print(f"Deleted existing {direction.lower()} rules successfully.")

# Function to split the list into smaller chunks
def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Function to add new firewall rules
def apply_firewall_rules(ip_ranges):
    if not ip_ranges:
        print("No IP ranges to block.")
        return

    chunk_size = 500  # Adjust chunk size to avoid netsh command limits

    for direction in ["In", "Out"]:
        print(f"Adding {direction.lower()} rules...")
        for idx, chunk in enumerate(chunk_list(ip_ranges, chunk_size)):
            ip_list = ",".join(chunk)
            rule_name = f"Spamhaus_Drop_{direction}_{idx}"  # Unique rule name for each chunk
            add_rule_cmd = f"netsh advfirewall firewall add rule name='{rule_name}' Dir={direction} Action=Block RemoteIP={ip_list}"
            result = subprocess.run(["Powershell", "-Command", add_rule_cmd], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Error adding {direction.lower()} rule {idx}: {result.stderr.strip()}")
            else:
                print(f"Applied {direction.lower()} rule {idx} to block {len(chunk)} IP ranges.")

# Main function
def main():
    print("Fetching Spamhaus DROP list...")
    ip_ranges = fetch_drop_list()

    if not ip_ranges:
        print("Failed to fetch the DROP list.")
        return

    print(f"Found {len(ip_ranges)} valid IP ranges to block.")
    delete_existing_rules()
    apply_firewall_rules(ip_ranges)

if __name__ == "__main__":
    main()
