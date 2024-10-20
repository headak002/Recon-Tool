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
from pyhunter import PyHunter  # Import PyHunter
import json

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

class ReconTool(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.initUI()
        self.driver = None  # Initialize the Selenium driver variable

    def initUI(self):
        self.target_label = ctk.CTkLabel(self, text='Enter URL or IP Address:')
        self.target_label.pack(pady=10)
        self.target_input = ctk.CTkEntry(self)
        self.target_input.pack(pady=5)

        self.scrape_btn = ctk.CTkButton(self, text='Scrape Emails and Phones (URLs only)', command=self.scrape_data)
        self.scrape_btn.pack(pady=10)

        self.pyhunter_btn = ctk.CTkButton(self, text='PyHunter Domain Search', command=self.pyhunter_recon)
        self.pyhunter_btn.pack(pady=10)

        self.result_display = ctk.CTkTextbox(self, width=400, height=150)
        self.result_display.pack(pady=10)

        self.nikto_btn = ctk.CTkButton(self, text='Run Nikto', command=self.run_nikto_scan)
        self.nikto_btn.pack(pady=5)

        self.nmap_btn = ctk.CTkButton(self, text='Run Nmap', command=self.run_nmap_scan)
        self.nmap_btn.pack(pady=5)

        self.geolocation_btn = ctk.CTkButton(self, text='Get Geolocation Info', command=self.query_ip_geolocation)
        self.geolocation_btn.pack(pady=10)

        # Add a loading progress bar
        self.loader = ctk.CTkProgressBar(self, mode="indeterminate", width=200)
        self.loader.pack(pady=10)
        self.loader.set(0)
        self.loader.stop()  # Initially stop the loader

        self.pack(padx=20, pady=20)

    def start_selenium_driver(self):
        """Start the Selenium Chrome driver."""
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service('/usr/local/bin/chromedriver-linux64')  # Path to your ChromeDriver
        self.driver = webdriver.Chrome(service=service, options=options)

    def stop_selenium_driver(self):
        """Stop the Selenium driver."""
        if self.driver:
            self.driver.quit()

    def show_loader(self):
        """Start showing the loading spinner"""
        self.loader.start()

    def hide_loader(self):
        """Stop and hide the loading spinner"""
        self.loader.stop()

    def append_result(self, text):
        self.result_display.insert(ctk.END, text + "\n")

    def scrape_data(self):
        target = self.target_input.get()
        if not target:
            self.append_result('Please enter a valid URL or IP address.')
            return

        self.show_loader()  # Show loader when the scrape begins

        def task():
            if is_valid_ip(target):
                self.append_result("Skipping email and phone scraping for IP addresses.")
            elif is_valid_url(target):
                try:
                    # Start the Selenium driver
                    self.start_selenium_driver()

                    # Use Selenium to get the page
                    self.driver.get(target)
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    emails = get_email(soup.get_text())
                    phones = get_phone(soup.get_text())

                    self.append_result(f"Scraped Data from {target}:")
                    self.append_result(f"Emails: {', '.join(emails) if emails else 'No emails found'}")
                    self.append_result(f"Phones: {', '.join(phones) if phones else 'No phones found'}")
                except Exception as e:
                    self.append_result(f"Error scraping {target}: {str(e)}")
                finally:
                    self.stop_selenium_driver()  # Ensure the driver is stopped
            else:
                self.append_result("Invalid URL or IP address format.")

            self.hide_loader()  # Hide loader when the scrape is done

        threading.Thread(target=task).start()

    def run_nikto_scan(self):
        target = self.target_input.get()
        if not target:
            self.append_result('Please enter a valid URL or IP address.')
            return

        self.show_loader()  # Show loader when Nikto starts

        def task():
            run_nikto(target, self.append_result)
            self.hide_loader()  # Hide loader when Nikto finishes

        threading.Thread(target=task).start()

    def run_nmap_scan(self):
        target = self.target_input.get()
        if not target:
            self.append_result('Please enter a valid URL or IP address.')
            return

        self.show_loader()  # Show loader when Nmap starts

        def task():
            run_nmap(target, self.append_result)
            self.hide_loader()  # Hide loader when Nmap finishes

        threading.Thread(target=task).start()

    def pyhunter_recon(self):
        domain = self.target_input.get()
        if not is_valid_url(domain):
            self.append_result('Please enter a valid domain URL (e.g., https://example.com).')
            return

        self.show_loader()  # Show loader when the PyHunter starts

        def task():
            # Initialize PyHunter with your Hunter.io API key
            hunter = PyHunter('3938d8875745e3e9e2b5b80117a802194b30be6d')  # Replace with your actual Hunter.io API key
            
            # Step 1: Search for emails tied to the domain
            response = hunter.domain_search(domain.replace("https://", "").replace("http://", ""))
            emails = [email['value'] for email in response['emails']]
            
            self.append_result(f"Emails found for {domain}:")
            self.append_result(f"Emails: {', '.join(emails) if emails else 'No emails found'}")
            
            # Step 2: Verify found email addresses
            for email in emails:
                result = hunter.email_verifier(email)
                self.append_result(f"Verification for {email}: {result['result']}")

            self.hide_loader()  # Hide loader when PyHunter finishes

    def query_ip_geolocation(self):
        target = self.target_input.get()
        if not is_valid_ip(target):
            self.append_result('Please enter a valid IP address.')
            return

        self.show_loader()

        def task():
            api_key = "E892DE0FDD9592F6F7D81CE9F5C08BAF"  # Replace with your IP2Location.io API key
            result = query_ip_geolocation(target, api_key)
            self.append_result(f"Geolocation info for {target}: {result}")
            self.hide_loader()

        threading.Thread(target=task).start()

if __name__ == "__main__":
    root =ctk.CTk()

