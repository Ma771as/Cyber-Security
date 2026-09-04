# SOC Incident Triage Report: Web Application Exploitation

## 1. Executive Summary
- **Incident Date/Time:** Thu, 03 Sep 2026 17:24:44 GMT
- **Severity Level:** High
- **Target IP / Asset:** `127.0.0.1` (DVWA Web Application)
- **Summary:** During routine security monitoring, HTTP telemetry revealed successful exploitation of local web application vulnerabilities. An external actor successfully executed arbitrary system commands via Command Injection and exfiltrated local database hashes using SQL Injection.

---

## 2. Technical Evidence & PCAP Analysis

### Vector 1: Command Injection
- **URI Requested:** `/vulnerabilities/exec/`
- **HTTP Method:** `POST`
- **Payload:** `127.0.0.1; cat /etc/passwd`
- **HTTP Response Status:** `HTTP/1.1 200 OK`
- **Impact Verification:** Local system user accounts revealed via web response.

### Vector 2: Union-Based SQL Injection
- **URI Requested:** `/vulnerabilities/sqli/`
- **HTTP Method:** `GET`
- **Payload:** `1' UNION SELECT user, password FROM users #`
- **HTTP Response Status:** `HTTP/1.1 200 OK`
- **Impact Verification:** Database credentials exfiltrated (`admin:5f4dcc3b5aa765d61d8327deb882cf99`).

---

## 3. Threat Mapping (MITRE ATT&CK)
| Attack Type | Tactic | Technique | ID |
| :--- | :--- | :--- | :--- |
| Command Injection | Execution / Discovery | Command & Scripting Interpreter | T1059.004 |
| SQL Injection | Credential Access | Exploit Public-Facing Application | T1190 |

---

## 4. Remediation & GRC Recommendations
1. **Parameterized Queries:** Enforce parameterized inputs across all database connectors to remediate SQLi.
2. **Input Validation:** Implement strict allow-listing on inputs accepted by system-level commands.
3. **NIST SP 800-53 Alignment:** Enforce **SI-10 (Information Input Validation)** and **AC-6 (Least Privilege)**.
