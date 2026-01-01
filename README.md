# 🛡️ Local Vulnerability Scanner (Python + Nmap)

A lightweight local network vulnerability scanner built using Python and Nmap.  
It scans a local subnet or target IP, detects risky services, assigns CVSS‑style severity, and generates HTML & PDF reports.

## 📌 Features

* Scan local network or custom target
* Detect:
  * Open ports
  * Weak / risky services
  * Outdated service versions
  * Potential default credential risks
* CVSS-style scoring & severity levels
* CLI-based tool
* Generates:
  * HTML report
  * PDF report (optional)
* Clean project structure (reports/ directory)

  ## 📌  Why This Tool Exists
-------------------
Most vulnerability scanners are heavy, commercial, or cloud-based.
This tool focuses on:
- Local environments
- Fast visibility
- Clear prioritization
- Offline report generation


## 🧱 Tech Stack

* Python 3.x
* Nmap
* python-nmap
* pdfkit
* wkhtmltopdf

## 📁 Project Structure

```
vuln-scanner/
├── scanner.py        # Main scanner logic
├── reports/          # Generated scan reports
│   ├── *.html
│   └── *.pdf
└── README.md

```

## ⚙️ Requirements

### 1️⃣ Install Nmap (System)
Download and install Nmap from:  
https://nmap.org/download.html  
Verify:

```bash
nmap --version
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Python Dependencies

```bash
pip install python-nmap pdfkit
```

### 4️⃣ Install wkhtmltopdf (For PDF)
Download from:  
https://wkhtmltopdf.org/downloads.html  
Default install path used in code:

```
wkhtmltopdf Configuration
-------------------------
The tool assumes wkhtmltopdf is available in system PATH.
If installed elsewhere, update the path inside scanner.py.

Tested on:
- Windows
- Linux (Ubuntu)

```

## 🚀 Usage

### Basic Scan (HTML report only)

```bash
python scanner.py
```

Scans local /24 subnet and generates:

```
reports/scan_report.html
```

### Scan with PDF Report

```bash
python scanner.py --pdf
```

Generates:

```
reports/scan_report.html
reports/scan_report.pdf
```

### Scan Custom Target

```bash
python scanner.py --target 192.168.0.10
```

or subnet:

```bash
python scanner.py --target 192.168.0.0/26
```

### Custom Output Name

```bash
python scanner.py --output office_scan --pdf
```

Output:

```
reports/office_scan.html
reports/office_scan.pdf
```

## 🧠 How It Works

1. Detects local subnet automatically (default /24)
2. Uses Nmap for:
   * Host discovery
   * Port scanning
   * Service version detection
3. Applies rule-based logic:
   * Weak services (FTP, Telnet, SMB, etc.)
   * Default credential risk ports
   * Outdated software versions
4. Calculates CVSS-style score
5. Assigns severity:
   * Low
   * Medium
   * High
   * Critical
6. Generates professional reports

## Default behavior scans:
```
192.168.1.0/24
```

## Sample Report
-------------
Generated reports include:
- Target summary
- Open ports & services
- Risk explanation
- Severity classification

Example:
reports/scan_report.html
reports/scan_report.pdf


## 📊 Severity Levels

### Note on CVSS Scoring
-------------------
This tool uses a simplified, rule-based CVSS-style scoring system.
It is NOT a full CVSS v3.1 implementation.

| CVSS Score | Severity  |
|------------|-----------|
| 9.0 – 10   | Critical |
| 7.0 – 8.9  | High     |
| 4.0 – 6.9  | Medium   |
| < 4.0      | Low      |

Scores are calculated based on:
- Service type risk
- Port exposure
- Known weak protocols
- Version age indicators

The goal is prioritization, not formal compliance.

## 🔒 Legal Disclaimer
This tool is intended only for educational purposes and authorized testing.  
Do NOT scan networks you do not own or have permission to test.

## 📌 Future Enhancements

* JSON export
* Severity filtering
* NSE vulnerability scripts
* Banner grabbing
* OS detection
* Web dashboard
