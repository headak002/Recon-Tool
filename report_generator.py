import json

def save_report(report_data, filename='scan_report.json'):
    with open(filename, 'w') as json_file:
        json.dump(report_data, json_file, indent=4)

def generate_report(findings, recommendations, summary):
    report_data = {
        "report_metadata": {
            "report_id": "12345",  # You might want to generate unique IDs
            "report_title": "Reconnaissance Scan Report",
            "tool_used": "Recon-VAPT",
            "version": "1.0",
            "generated_on": "2024-10-09",
            "generated_by": "Akshat Goyal",
            "contact_email": "akshat.goyal@example.com"
        },
        "target_info": {
            "target_domain": "",  # Fill this with actual data
            "target_ip": "",      # Fill this with actual data
            "scan_duration": "",  # Duration can be calculated
            "scan_start_time": "", # Fill this with actual data
            "scan_end_time": "",  # Fill this with actual data
        },
        "findings": findings,
        "recommendations": recommendations,
        "summary": summary,
        "conclusion": "The reconnaissance scan has identified critical vulnerabilities that need to be addressed to enhance the security posture of the target system."
    }
    return report_data

