# SOP: Attack Simulation and Defense Analysis
A hands-on red team / blue team lab covering three core attack vectors: SMB brute force, OS command injection with a reverse shell, and a TCP SYN flood DoS.
This project was built to practice the full attack-to-defense lifecycle: executing a realistic technique, identifying the specific artifact it leaves in logs or traffic, and mapping that artifact to a concrete mitigation control. All activity was performed in an isolated, two-VM lab environment with no production systems or external targets involved.

## Table of contents
1. [Lab environment](#lab-environment)
2. [Exercise 1 — SMB reconnaissance & brute force](#exercise-1--smb-reconnaissance--brute-force)
3. [Exercise 2 — Command injection & reverse shell](#exercise-2--command-injection--reverse-shell)
4. [Exercise 3 — TCP SYN flood DoS](#exercise-3--tcp-syn-flood-dos)
5. [Key takeaways](#key-takeaways)
6. [Full procedure](#full-procedure)
7. [Repository Structure](#repository-structure)

## Lab environment

| | Attacker VM | Victim / defender VM |
|---|---|---|
| Host | KALI-ATK | WIN-DEF |
| OS | Kali Linux | Windows 11 / Server |
| IP | 192.168.0.5 | 192.168.0.2 |
| Key tools / services | Nmap, Enum4linux, Smbclient, Ncat, Msfconsole | SMB Server, XAMPP (Apache, MySQL), bWAPP, Event Viewer |

---

## Exercise 1 — SMB reconnaissance & brute force
**Objective**
SMB is one of the most commonly exposed internal services in enterprise networks, and weak or unthrottled authentication on it is still a leading initial-access vector in real breaches (it's how WannaCry and NotPetya spread laterally). This exercise simulates an attacker enumerating a Windows host's shares and brute-forcing SMB credentials, while measuring what that activity actually looks like from the defender's side.

**Mitigation**
Three controls close this off at different layers: account lockout policy stops the brute-force outright after N attempts, SMB signing prevents the relay/tampering attacks that often follow successful SMB access, and IP-based rate limiting on the firewall slows or blocks the scripted traffic pattern before it reaches the host at all. Lockout alone is the cheapest fix, but combined with signing it also closes the follow-on attack path, not just this one.
- ATT&CK Mapping: T1135 (Network Share Discovery), T1087.002 (Account Discovery: Domain Account), T1110.001 (Brute Force: Password Guessing), T1021.002 (Remote Services: SMB/Windows Admin Shares)

**Lessons learned**
The most interesting part wasn't the attack, it was how obvious the attack became once logging was baselined first. Clearing the log before the brute-force run made the spike undeniable in a way it wouldn't have been against months of noisy real-world logs. It reinforced that detection engineering is as much about establishing a clean baseline as it is about the rule itself.

---

## Exercise 2 — Command injection & reverse shell
**Objective**
Unsanitized input in a command-execution context is still one of the most damaging web vulnerability classes, a single unfiltered character can turn a form field into a full remote shell. This exercise simulates discovering and exploiting an OS command injection flaw in a vulnerable web app, then using it to establish a live reverse shell back to the attacker machine.

**Mitigation**
The root cause is trusting user input inside a shell context, so the primary fix is strict input validation using an allowlist rather than a blacklist of blocked characters, and avoiding shell-exec style functions in application code entirely where possible. As a second layer, restricting outbound (egress) traffic from the web server tier closes the exploitation path even if an injection flaw slips through, a web server that cannot open arbitrary outbound connections can't call back to an attacker's listener.
- ATT&CK Mapping: T1190 (Exploit Public-Facing Application), T1059.003 (Command and Scripting Interpreter: Windows Command Shell), T1095 (Non-Application Layer Protocol)

**Lessons learned**
Testing `&` and `&&` first and watching them get blocked was a useful reminder that most input filters are built against the obvious payloads, not against the full set of shell metacharacters. The pipe operator working on the third attempt showed how a single gap in a blacklist undoes the whole control, which is exactly why allowlisting beats blacklisting for this class of vulnerability.

---

## Exercise 3 — TCP SYN flood DoS
**Objective**
Denial-of-service attacks don't need to breach anything, they just need to exhaust a resource. This exercise simulates a TCP SYN flood against SMB, exploiting the fact that a half-open TCP handshake still consumes server memory while it waits for a response that never comes.

**Mitigation**
TCP SYN cookies are the standard fix, they let the server respond to a SYN without allocating a connection record until the handshake actually completes, so a flood of SYNs without ACKs can't exhaust memory. Rate limiting SYN packets at the firewall and basic stateful firewall inspection add defense in depth on top of that, catching the flood before it reaches the host's own TCP stack in the first place.
- ATT&CK Mapping: T1499.002 (Endpoint Denial of Service: Service Exhaustion Flood)

**Lessons learned**
Having a *socket-state* baseline mattered just as much as having a bandwidth baseline, the Ethernet throughput graph alone wouldn't have told me what kind of traffic was spiking, or why. Pairing a performance metric with a protocol-state metric gave a much clearer picture of what was actually happening than either one would have on its own.

---

## Key takeaways
Across all three exercises, the strongest defensive signal never came from a single log line or packet, it came from comparing activity against an established baseline. A clean baseline before the SMB brute force made the spike unmistakable; an outbound connection from a web server stood out because servers aren't supposed to behave that way; a socket-state baseline turned a bandwidth graph into an actual diagnosis. The practical lesson for defense is the same one each time: instrument and baseline *before* you need to detect something, not after.

## Full procedure
The complete step-by-step lab procedure, the exact commands, VM setup, and task-by-task instructions for reproducing all three exercises is available in [`docs/SOP.pdf`](docs/SOP.pdf).

## Repository Structure

```
.
├── docs/
│   └── SOP.pdf          # Full step-by-step procedural manual & step commands
├── scripts/
│   └── brute.sh         # Bash automation script for SMB authentication testing
├── LICENSE              # MIT Open-Source License
└── README.md            # Portfolio executive summary & project overview

```

_Last updated: 2026-10-09 — added MITRE ATT&CK technique mapping to the SOP and README._