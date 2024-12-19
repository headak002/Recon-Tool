# Recon-VAPT Tool

The Recon-VAPT Tool is a comprehensive and user-friendly application designed for security assessments and reconnaissance tasks. It provides utilities for vulnerability scanning, reconnaissance, and reporting.

---

## Features

### 1. Welcome Screen

The application greets users with an intuitive welcome screen, featuring a gradient background and options to proceed to the login page.

### 2. Login Page

Users can securely log in using valid credentials to access the application's features.

### 3. Vulnerability Assessment

The "Vulnerability Assessment" tab includes tools like:

- **Nikto**: For scanning web servers for known vulnerabilities.
- **Bandit**: For analyzing Python scripts for security issues.

### 4. Recon Tools

The "Recon Tools" tab provides options for:

- **Nmap**: Network scanning and port identification.
- **Geolocation**: IP-based geolocation lookup.
- **Email and Phone Scraping**: Extract emails and phone numbers from a webpage.
- **PyHunter**: Domain reconnaissance using Hunter.io.

### 5. Report Generation

Generate reports in either JSON or XML format based on findings.

---

## Installation

### Prerequisites

- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

### Tools and Libraries

Install the required tools and libraries using the following commands:

```bash
# Clone the repository
$ git clone https://github.com/your-repo/recon-vapt-tool.git
$ cd recon-vapt-tool

# Install Python dependencies
$ pip install -r requirements.txt

# Install Selenium WebDriver (for advanced web scraping, if applicable)
$ pip install selenium

# Other recommended tools
$ sudo apt install nmap
$ pip install pyhunter
```

---

## Usage

### Running the Application

Start the application by running the following command:

```bash
$ python app.py
```

### Screenshots

#### Welcome Screen

![image](https://github.com/user-attachments/assets/3bd39854-17af-4a60-b0d3-fdde9f1f7755)

#### Login Page

![image](https://github.com/user-attachments/assets/5175bdd1-d314-48e0-9c65-17bd52ceca71)

#### Main Tool Interface

Insert screenshots of the "Recon Tools" 
![image](https://github.com/user-attachments/assets/938393ea-ef37-4387-8cfd-c54c1e6f0af5)

and "Vulnerability Assessment" tabs here.
![image](https://github.com/user-attachments/assets/afdfb418-deb8-4519-822e-14bff9c26cb6)

Automated installation of tools
![image](https://github.com/user-attachments/assets/de28f6a2-b10f-4a2c-803c-666ecfad06cb)



---

## Examples

### Nikto Scan

1. Enter a valid URL or IP address.
2. Click "Run Nikto."
3. View results in the shared display box.

### Nmap Scan

1. Enter a valid URL or IP address.
2. Click "Run Nmap."
3. View results in the shared display box.

---

## Report Generation

1. Choose the desired format (JSON or XML).
2. Click "Generate Report."
3. Reports are saved in the project directory as `report.json` or `report.xml`.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.

---

**Disclaimer:** This tool is intended for ethical use only. Unauthorized usage is strictly prohibited.

