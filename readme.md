
# Malicious IP Firewall Automation

## Overview

The **Malicious IP Firewall Automation** project is an open-source initiative aimed at building a robust tool for dynamically managing malicious IP addresses in Windows Firewall. This project consolidates data from trusted sources such as Spamhaus and Feodo Tracker to provide a unified, secure, and automated firewall configuration.

With the newly added **master script**, users can now manage and execute multiple firewall scripts seamlessly, making the system more scalable and maintainable.

---

## Features

- **Dynamic Updates**: Fetches malicious IP lists from trusted sources like Spamhaus and Feodo Tracker.
- **Master Script for Orchestration**: The `firewall_master.py` script executes all configured scripts in sequence, allowing for easy management of multiple sources.
- **Rule Management**: Automatically removes outdated firewall rules created by the scripts to avoid duplication.
- **Validation**: Ensures only valid IP addresses or CIDR ranges are applied.
- **Error Handling**: Logs any errors encountered during execution and continues with subsequent tasks.
- **Modularity**: Future scripts can be added easily without modifying the core functionality.

---

## Future Goals

- Integrate additional IP blocklists, such as:
  - Proofpoint Emerging Threats
  - FireHOL IP Threat Lists
  - Project Honeypot
- Expand support to other platforms:
  - **Linux**: Use `iptables` for firewall management.
  - **macOS**: Use `pfctl` for rule configuration.
- Build a GUI for easier management and visualization of sources and rules.
- Develop logging and reporting features to provide detailed insights into blocked IPs and system activity.

---

## Getting Started

### Prerequisites

- **Operating System**: Windows (for the current version).
- **Python**: Version 3.x.
- **Administrator Privileges**: Required to manage Windows Firewall rules.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/uzairnz/malicious-ip-firewall.git
   cd malicious-ip-firewall
   ```

2. **Install Required Python Libraries**:
   Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Master Script

The `firewall_master.py` script is the central tool for managing and executing all configured firewall scripts.

1. **Run the Master Script**:
   ```bash
   python firewall_master.py
   ```

2. **What Happens**:
   - Executes all listed scripts (e.g., `abuse_ch_firewall.py`, `spamhaus_firewall.py`).
   - Fetches IP blocklists and updates firewall rules dynamically.
   - Logs success and errors for each script.

3. **Add New Scripts**:
   - Place the new script in the same directory.
   - Ensure the script has a `main()` function.
   - Add the script name to the `scripts_to_run` list in `firewall_master.py`.

### Example Output

```plaintext
Starting firewall master script...
Executing abuse_ch_firewall.py...
Successfully executed abuse_ch_firewall.py.
Executing spamhaus_firewall.py...
Successfully executed spamhaus_firewall.py.
Firewall master script completed.
```

---

## Sources

### Currently Supported
- **Feodo Tracker**: [https://feodotracker.abuse.ch/](https://feodotracker.abuse.ch/)
- **Spamhaus DROP List**: [https://www.spamhaus.org/drop/drop_v4.json](https://www.spamhaus.org/drop/drop_v4.json)

### Future Integrations
- [Proofpoint Emerging Threats](https://rules.emergingthreats.net/blockrules/)
- [FireHOL IP Threat Lists](https://iplists.firehol.org/)
- [Project Honeypot](https://www.projecthoneypot.org/)

Have a trusted source to recommend? Open an issue or submit a PR!

---

## Contributing

We welcome contributions to make this project more robust and comprehensive.

### How to Contribute

1. **Fork the Repository**:
   - Click the "Fork" button on GitHub to create your copy of the repository.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/<your-username>/malicious-ip-firewall.git
   cd malicious-ip-firewall
   ```

3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/<your-feature-name>
   ```

4. **Make Your Changes**:
   - Write clear, concise code.
   - Add comments and documentation if needed.
   - Test your changes thoroughly.

5. **Submit a Pull Request (PR)**:
   - Push your changes:
     ```bash
     git push origin feature/<your-feature-name>
     ```
   - Open a PR on the main repository.

---

### Contribution Guidelines

- **Code Security**: Ensure all contributions are secure and follow best practices.
- **Testing**: Test changes locally before submitting.
- **Documentation**: Add or update documentation for new features.
- **Respect**: Collaborate respectfully and constructively with the community.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## Community and Support

Have ideas, feedback, or issues? Open a discussion or issue on GitHub.

Let’s build a **secure, crowd-powered firewall solution** together!

---
