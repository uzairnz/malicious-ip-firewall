import subprocess
import os
import importlib.util
import sys

# Directory where firewall scripts are stored
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Function to run a script by importing and calling its `main()` function
def execute_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"Script {script_name} not found.")
        return False

    try:
        print(f"Executing {script_name}...")
        # Dynamically load the script
        spec = importlib.util.spec_from_file_location("module.name", script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["module.name"] = module
        spec.loader.exec_module(module)

        # Call the main function of the script
        if hasattr(module, "main"):
            module.main()
            print(f"Successfully executed {script_name}.")
        else:
            print(f"Script {script_name} does not have a 'main()' function.")
            return False
    except Exception as e:
        print(f"Error executing {script_name}: {e}")
        return False
    return True

# Main function to manage and execute all scripts
def main():
    print("Starting firewall master script...")
    
    # List of scripts to execute (add new scripts here as needed)
    scripts_to_run = [
        "abuse_ch_firewall.py",
        "spamhaus_firewall.py"
    ]

    # Loop through and execute each script
    for script in scripts_to_run:
        success = execute_script(script)
        if not success:
            print(f"Execution failed for {script}. Continuing with the next script...")
    
    print("Firewall master script completed.")

if __name__ == "__main__":
    main()
