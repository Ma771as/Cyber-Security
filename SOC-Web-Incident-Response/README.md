# Web Application Incident Response & SOC Triage Project

## Project Overview
This project simulates a real-world Web Application Attack scenario and performs full Blue Team triage on generated telemetry. Using a local lab environment (**DVWA** via Docker), attack traffic was captured at both the Application Layer (Layer 7) and Network Layer (Layers 3–7) to analyze exploitation vectors, establish root cause, and document GRC control recommendations.

---

## Threat Scenarios Investigated
1. **Command Injection (RCE):** Exploitation of web input fields to run arbitrary shell commands (`cat /etc/passwd`).
2. **SQL Injection (Exfiltration):** Union-based database query manipulation to extract credential hashes from local storage.

---

## Tools & Environment
- **Environment:** Kali Linux / Docker Sandbox
- **Traffic Capture:** Wireshark (`.pcapng`)
- **Proxy/Application Analysis:** Burp Suite Community Edition
- **Framework Mapping:** MITRE ATT&CK & NIST SP 800-53

---

## Repository Navigation

```text
SOC_Project/
├── captures/                 # Raw telemetry and HTTP stream evidence
│   ├── web_attack_capture.pcapng
│   ├── GET-Vulnerabilities-sqli.txt
│   └── POST-Vulnerabilities-exec.txt
├── reports/                  # Detailed SOC Incident Response Triage
│   └── SOC-Triage-Report.md
└── README.md                 # Project executive summary