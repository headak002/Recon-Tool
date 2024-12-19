import subprocess
import requests
from bs4 import BeautifulSoup
import customtkinter as ctk
import threading
import re
import time
import ipaddress
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pyhunter import PyHunter
import json
import xml.etree.ElementTree as ET
from tkinter import ttk  # For the loading bar
from tkinter import messagebox  # For error and info dialogs

# Utility functions
def remove_dup(x):
    return list(dict.fromkeys(x))

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_url(url):
    return re.match(r'http(s)?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url) is not None

def get_email(html):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)
    return remove_dup(email)

def get_phone(html):
    phone = re.findall(r"\+?\d[\d\s-]{9,}\d", html)
    return remove_dup(phone)

def run_nikto(target, callback):
    try:
        cmd = f'nikto -host {target}'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if error:
            callback(f"Error: {error}")
        else:
            callback(output)
    except Exception as e:
        callback(f"Exception occurred: {str(e)}")

def run_nmap(target, callback):
    try:
        cmd = f'nmap -sS {target}'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        if error:
            callback(f"Error: {error}")
        else:
            callback(output)
    except Exception as e:
        callback(f"Exception occurred: {str(e)}")

def query_ip_geolocation(ip_address, api_key=None):
    command = ["ip2locationio"]
    if api_key:
        command.append("-k")
        command.append(api_key)
    command.append(ip_address)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        raw_output = result.stdout.strip()
        if raw_output.startswith("{") and raw_output.endswith("}"):  # Basic check for JSON
            data = json.loads(raw_output)
            return data
        else:
            return {"error": "Non-JSON response received", "raw_response": raw_output}
    except subprocess.CalledProcessError as e:
        return {"error": f"Error executing command: {e}"}

class VulnerabilityAssessment(ctk.CTkFrame):
    def __init__(self, master, result_display):
        super().__init__(master)
        self.result_display = result_display
        self.configure(border_width=2, border_color="gray", corner_radius=10)

        ctk.CTkLabel(self, text="Vulnerability Assessment", font=("Arial", 18, "bold")).pack(pady=20)

        # Nikto
        self.target_nikto = ctk.StringVar()
        nikto_frame = ctk.CTkFrame(self)
        nikto_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkEntry(nikto_frame, textvariable=self.target_nikto, placeholder_text="Enter URL or IP for Nikto", height=40, border_width=2, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(nikto_frame, text="Run Nikto", command=self.run_nikto_scan, width=120).pack(side="right", padx=(5, 0))

        # Bandit
        self.file_path_bandit = ctk.StringVar()
        bandit_frame = ctk.CTkFrame(self)
        bandit_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkEntry(bandit_frame, textvariable=self.file_path_bandit, placeholder_text="Select a Python file for Bandit", height=40, border_width=2, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(bandit_frame, text="Browse", command=self.browse_bandit_file, width=100).pack(side="right", padx=(5, 0))
        ctk.CTkButton(bandit_frame, text="Run Bandit", command=self.run_bandit_scan, width=120).pack(side="right", padx=(5, 0))

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=200)
        self.progress.pack(pady=10)

    def append_result(self, text):
        self.result_display.insert(ctk.END, text + "\n")

    def run_nikto_scan(self):
        target = self.target_nikto.get()
        if not target:
            self.append_result('Please enter a valid URL or IP for Nikto.')
            return
        def task():
            self.progress.start()
            run_nikto(target, self.append_result)
            self.progress.stop()
        threading.Thread(target=task).start()

    def browse_bandit_file(self):
        file = ctk.filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file:
            self.file_path_bandit.set(file)

    def run_bandit_scan(self):
        file = self.file_path_bandit.get()
        if not file:
            self.append_result('Please select a Python file for Bandit.')
            return
        def task():
            self.progress.start()
            try:
                result = subprocess.run(
                    ["bandit", "-r", file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self.append_result(result.stdout or result.stderr)
            except FileNotFoundError:
                self.append_result("Bandit is not installed. Please install Bandit and try again.")
            self.progress.stop()
        threading.Thread(target=task).start()

class ReconTools(ctk.CTkFrame):
    def __init__(self, master, result_display):
        super().__init__(master)
        self.result_display = result_display
        self.configure(border_width=2, border_color="gray", corner_radius=10)

        ctk.CTkLabel(self, text="Recon Tools", font=("Arial", 18, "bold")).pack(pady=20)

        # Recon Buttons
        self.target_recon = ctk.StringVar()
        recon_frame = ctk.CTkFrame(self)
        recon_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkEntry(recon_frame, textvariable=self.target_recon, placeholder_text="Enter URL or IP for Recon", height=40, border_width=2, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(recon_frame, text="Run Nmap", command=self.run_nmap_scan, width=120).pack(side="left", padx=(5, 0), pady=(5, 0))
        ctk.CTkButton(recon_frame, text="Get Geolocation", command=self.run_geolocation, width=150).pack(side="left", padx=(5, 0), pady=(5, 0))

        # Email and Phone Scraping
        self.target_scrape = ctk.StringVar()
        scrape_frame = ctk.CTkFrame(self)
        scrape_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkEntry(scrape_frame, textvariable=self.target_scrape, placeholder_text="Enter URL to scrape emails & phones", height=40, border_width=2, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(scrape_frame, text="Scrape Emails & Phones", command=self.scrape_emails_phones, width=200).pack(side="right", padx=(5, 0))

        # PyHunter functionality
        self.target_hunter = ctk.StringVar()
        hunter_frame = ctk.CTkFrame(self)
        hunter_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkEntry(hunter_frame, textvariable=self.target_hunter, placeholder_text="Enter domain for PyHunter", height=40, border_width=2, corner_radius=10).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(hunter_frame, text="Run PyHunter", command=self.run_hunter_scan, width=120).pack(side="right", padx=(5, 0))

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=200)
        self.progress.pack(pady=10)

    def append_result(self, text):
        self.result_display.insert(ctk.END, text + "\n")

    def run_nmap_scan(self):
        target = self.target_recon.get()
        if not target:
            self.append_result('Please enter a valid URL or IP for Nmap.')
            return
        def task():
            self.progress.start()
            run_nmap(target, self.append_result)
            self.progress.stop()
        threading.Thread(target=task).start()

    def run_geolocation(self):
        target = self.target_recon.get()
        if not is_valid_ip(target):
            self.append_result('Please enter a valid IP for Geolocation.')
            return
        def task():
            self.progress.start()
            result = query_ip_geolocation(target, api_key="E892DE0FDD9592F6F7D81CE9F5C08BAF")
            self.append_result(json.dumps(result, indent=2))
            self.progress.stop()
        threading.Thread(target=task).start()

    def scrape_emails_phones(self):
        url = self.target_scrape.get()
        if not is_valid_url(url):
            self.append_result('Please enter a valid URL for scraping.')
            return
        def task():
            self.progress.start()
            try:
                response = requests.get(url)
                html = response.text
                emails = get_email(html)
                phones = get_phone(html)
                self.append_result(f"Emails found: {emails}")
                self.append_result(f"Phones found: {phones}")
            except Exception as e:
                self.append_result(f"Error: {str(e)}")
            self.progress.stop()
        threading.Thread(target=task).start()

    def run_hunter_scan(self):
        domain = self.target_hunter.get()
        if not domain:
            self.append_result('Please enter a valid domain for PyHunter.')
            return
        def task():
            self.progress.start()
            try:
                hunter = PyHunter("3938d8875745e3e9e2b5b80117a802194b30be6d")
                result = hunter.domain_lookup(domain)
                self.append_result(json.dumps(result, indent=2))
            except Exception as e:
                self.append_result(f"Error: {str(e)}")
            self.progress.stop()
        threading.Thread(target=task).start()

class ReconToolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Recon-VAPT Tool")
        self.geometry("900x700")

        # Tabs
        self.tab_control = ctk.CTkTabview(self)
        self.tab_control.pack(fill="both", expand=True, padx=20, pady=20)

        # Shared Result Display
        self.result_display = ctk.CTkTextbox(self, height=200, width=600)
        self.result_display.pack(fill="x", padx=20, pady=20)

        # Vulnerability Assessment Tab
        vuln_tab = self.tab_control.add("Vulnerability Assessment")
        self.vuln_tool = VulnerabilityAssessment(vuln_tab, self.result_display)
        self.vuln_tool.pack(fill="both", expand=True, padx=20, pady=20)

        # Recon Tools Tab
        recon_tab = self.tab_control.add("Recon Tools")
        self.recon_tool = ReconTools(recon_tab, self.result_display)
        self.recon_tool.pack(fill="both", expand=True, padx=20, pady=20)

        # Report Generation
        report_frame = ctk.CTkFrame(self)
        report_frame.pack(fill="x", padx=20, pady=10)
        self.report_format = ctk.StringVar(value="JSON")
        ctk.CTkOptionMenu(report_frame, values=["JSON", "XML"], variable=self.report_format).pack(side="left", padx=(10, 10))
        ctk.CTkButton(report_frame, text="Generate Report", command=self.generate_report).pack(side="left", padx=(5, 0))

    def generate_report(self):
        data = self.result_display.get("1.0", ctk.END).strip()
        if not data:
            ctk.messagebox.showwarning("No Data", "No findings to generate a report.")
            return

        if self.report_format.get() == "JSON":
            try:
                report_data = {"findings": data.split("\n")}
                with open("report.json", "w") as f:
                    json.dump(report_data, f, indent=4)
                ctk.messagebox.showinfo("Report Generated", "JSON report saved as 'report.json'.")
            except Exception as e:
                ctk.messagebox.showerror("Error", f"Failed to save report: {str(e)}")

        elif self.report_format.get() == "XML":
            try:
                root = ET.Element("Report")
                findings = ET.SubElement(root, "Findings")
                for line in data.split("\n"):
                    ET.SubElement(findings, "Finding").text = line
                tree = ET.ElementTree(root)
                tree.write("report.xml")
                ctk.messagebox.showinfo("Report Generated", "XML report saved as 'report.xml'.")
            except Exception as e:
                ctk.messagebox.showerror("Error", f"Failed to save report: {str(e)}")

