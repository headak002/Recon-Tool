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

Insert a screenshot of the welcome screen here.

#### Login Page

Insert a screenshot of the login page here.

#### Main Tool Interface

Insert screenshots of the "Vulnerability Assessment" and "Recon Tools" tabs here.

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

## Contact

For any queries or feedback, contact us at: [support@reconvapt.com](mailto\:support@reconvapt.com)

---

**Disclaimer:** This tool is intended for ethical use only. Unauthorized usage is strictly prohibited.

