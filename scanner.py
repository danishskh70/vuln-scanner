import nmap
import socket
import ipaddress
import argparse
from datetime import datetime
import os
import pdfkit

config = pdfkit.configuration(
    wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
)

# =============================
# CLI ARGUMENTS
# =============================
parser = argparse.ArgumentParser(
    description="Local Vulnerability Scanner using Python + Nmap"
)

parser.add_argument(
    "--target",
    help="Target IP / Subnet (default: local /24 subnet)",
    default=None
)

parser.add_argument(
    "--output",
    help="Output file name (without extension)",
    default="scan_report"
)

parser.add_argument(
    "--pdf",
    help="Generate PDF report",
    action="store_true"
)

args = parser.parse_args()

# =============================
# SUBNET DETECTION
# =============================
def get_local_subnet():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    network = ipaddress.ip_network(local_ip + "/24", strict=False)
    return str(network)

target = args.target if args.target else get_local_subnet()
output_name = args.output

# =============================
# RULE ENGINES
# =============================
WEAK_SERVICES = {
    21: ("FTP", 7.5),
    23: ("Telnet", 9.8),
    25: ("SMTP", 6.5),
    445: ("SMB", 8.5),
    3306: ("MySQL", 8.0),
    3389: ("RDP", 8.8),
}

DEFAULT_CRED_RISK = {
    21: 6.0,
    22: 5.5,
    80: 5.0,
    8080: 6.0
}

OUTDATED_VERSIONS = {
    "apache": ("2.4.50", 7.0),
    "nginx": ("1.18.0", 6.5),
    "mysql": ("8.0", 8.0)
}

def calculate_cvss(port, service_name, version):
    score = 2.0  # base low risk

    if port in WEAK_SERVICES:
        score = max(score, WEAK_SERVICES[port][1])

    if port in DEFAULT_CRED_RISK:
        score = max(score, DEFAULT_CRED_RISK[port])

    if service_name and version:
        service_name = service_name.lower()
        for s in OUTDATED_VERSIONS:
            if s in service_name:
                try:
                    if version < OUTDATED_VERSIONS[s][0]:
                        score = max(score, OUTDATED_VERSIONS[s][1])
                except:
                    pass

    return round(score, 1)

def severity_from_cvss(score):
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    else:
        return "Low"

# =============================
# SCANNING
# =============================
print(f"[+] Scanning target: {target}")

scanner = nmap.PortScanner()
scanner.scan(target, arguments="-sV --open")

results = []

for host in scanner.all_hosts():
    if scanner[host].state() != "up":
        continue

    for proto in scanner[host].all_protocols():
        for port in scanner[host][proto]:
            service = scanner[host][proto][port]

            service_name = service.get("name")
            version = service.get("version")

            cvss = calculate_cvss(port, service_name, version)
            severity = severity_from_cvss(cvss)

            results.append({
                "host": host,
                "port": port,
                "service": service_name,
                "version": version,
                "cvss": cvss,
                "severity": severity
            })

# =============================
# HTML REPORT
# =============================
html = f"""
<html>
<head>
<title>Vulnerability Scan Report</title>
<style>
body {{ font-family: Arial; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 8px; }}
th {{ background-color: #f2f2f2; }}
.Critical {{ background-color: #ff4d4d; }}
.High {{ background-color: #ffcccc; }}
.Medium {{ background-color: #fff0b3; }}
.Low {{ background-color: #e6ffe6; }}
</style>
</head>
<body>

<h2>Local Vulnerability Scan Report</h2>
<p><b>Target:</b> {target}</p>
<p><b>Date:</b> {datetime.now()}</p>

<table>
<tr>
<th>Host</th>
<th>Port</th>
<th>Service</th>
<th>Version</th>
<th>CVSS</th>
<th>Severity</th>
</tr>
"""

for r in results:
    html += f"""
<tr class="{r['severity']}">
<td>{r['host']}</td>
<td>{r['port']}</td>
<td>{r['service']}</td>
<td>{r['version']}</td>
<td>{r['cvss']}</td>
<td>{r['severity']}</td>
</tr>
"""

html += """
</table>
</body>
</html>
"""

html_file = f"{output_name}.html"
with open(html_file, "w") as f:
    f.write(html)

print(f"[+] HTML report generated: {html_file}")

# =============================
# PDF EXPORT
# =============================
if args.pdf:
    try:
        import pdfkit
        pdf_file = f"{output_name}.pdf"
        pdfkit.from_file("scan_report.html", "scan_report.pdf", configuration=config)
        print(f"[+] PDF report generated: {pdf_file}")
    except Exception as e:
        print("[-] PDF generation failed:", e)

print("[✓] Scan complete.")
