import customtkinter as ctk
from welcome_screen import WelcomeScreen
from login import LoginPage
from recon_tool import ReconTools, VulnerabilityAssessment
import json
import xml.etree.ElementTree as ET
import subprocess
import logging

# Set up logging for error tracking
logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VulRec")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Global style settings
        ctk.set_appearance_mode("Dark")  # Dark mode for a modern look
        ctk.set_default_color_theme("blue")  # Use a cool color theme

        # Create a container frame for all pages
        self.container = ctk.CTkFrame(self, fg_color="#121212")
        self.container.pack(fill="both", expand=True)

        self.current_page = None
        self.show_welcome_screen()

    def switch_page(self, new_page_class):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = new_page_class(self.container, self.show_main_page)
        self.current_page.pack(fill="both", expand=True)

    def show_welcome_screen(self):
        self.switch_page(lambda parent, _: WelcomeScreen(parent, self.show_login_page))

    def show_login_page(self):
        self.switch_page(lambda parent, _: LoginPage(parent, self.show_main_page))

    def show_main_page(self):
        self.current_page.pack_forget()
        self.current_page = MainPage(self.container)
        self.current_page.pack(fill="both", expand=True)


class MainPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1E1E2F")

        # Horizontal Layout
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#2C2C3A", corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.result_display = ctk.CTkTextbox(self, fg_color="#262626", corner_radius=10, font=("Consolas", 12))
        self.result_display.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Sidebar Content
        ctk.CTkLabel(
            self.sidebar,
            text="Tools",
            font=("Helvetica", 20, "bold"),
            text_color="#FFFFFF",
        ).pack(pady=20)

        # Buttons with updated style and spacing
        ctk.CTkButton(
            self.sidebar,
            text="Vulnerability Assessment",
            command=self.show_vuln_assessment,
            font=("Helvetica", 14),
            corner_radius=5,
            hover_color="#3B3B4B",
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.sidebar,
            text="Recon Tools",
            command=self.show_recon_tools,
            font=("Helvetica", 14),
            corner_radius=5,
            hover_color="#3B3B4B",
        ).pack(pady=10, padx=20)

        ctk.CTkButton(
            self.sidebar,
            text="Install Tools",
            command=self.show_tool_installer,
            font=("Helvetica", 14),
            corner_radius=5,
            hover_color="#3B3B4B",
        ).pack(pady=10, padx=20)

        # Report Generation
        self.report_frame = ctk.CTkFrame(self)
        self.report_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.report_format = ctk.StringVar(value="JSON")
        ctk.CTkOptionMenu(self.report_frame, values=["JSON", "XML"], variable=self.report_format).pack(side="left", padx=(10, 10))
        ctk.CTkButton(self.report_frame, text="Generate Report", command=self.generate_report).pack(side="left", padx=(5, 0))

        self.active_tool_frame = None

    def show_vuln_assessment(self):
        if self.active_tool_frame:
            self.active_tool_frame.pack_forget()
        self.active_tool_frame = VulnerabilityAssessment(self, self.result_display)
        self.active_tool_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def show_recon_tools(self):
        if self.active_tool_frame:
            self.active_tool_frame.pack_forget()
        self.active_tool_frame = ReconTools(self, self.result_display)
        self.active_tool_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def show_tool_installer(self):
        if self.active_tool_frame:
            self.active_tool_frame.pack_forget()
        self.active_tool_frame = ToolInstaller(self, self.result_display)
        self.active_tool_frame.pack(fill="both", expand=True, padx=10, pady=10)

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
                logging.error(f"Error generating JSON report: {e}")
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
                logging.error(f"Error generating XML report: {e}")
                ctk.messagebox.showerror("Error", f"Failed to save report: {str(e)}")


class ToolInstaller(ctk.CTkFrame):
    def __init__(self, parent, display):
        super().__init__(parent)
        self.display = display
        self.configure(fg_color="#1E1E2F")

        ctk.CTkLabel(
            self, text="Tool Installer", font=("Helvetica", 20, "bold"), text_color="#FFFFFF"
        ).pack(pady=10)

        tools = {
            "PyHunter": "pip install pyhunter",
            "Nmap": "sudo apt-get install -y nmap",
            "Bandit": "pip install bandit",
            "Nikto": "sudo apt-get install -y nikto",
            "IP2Location.io": "pip install ip2location"
        }

        for tool, command in tools.items():
            frame = ctk.CTkFrame(self, fg_color="#2C2C3A", corner_radius=5)
            frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(
                frame, text=tool, font=("Helvetica", 14), text_color="#FFFFFF"
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                frame,
                text="Install",
                command=lambda cmd=command, name=tool: self.install_tool(cmd, name),
                font=("Helvetica", 12),
                corner_radius=5,
                hover_color="#3B3B4B",
            ).pack(side="right", padx=10)

    def install_tool(self, command, tool_name):
        try:
            self.display.insert(ctk.END, f"Installing {tool_name}...\n")
            subprocess.check_call(command.split())  # Avoid shell=True
            self.display.insert(ctk.END, f"{tool_name} installed successfully!\n")
        except subprocess.CalledProcessError as e:
            self.display.insert(ctk.END, f"Error installing {tool_name}: {e}\n")
            logging.error(f"Error installing {tool_name}: {e}")
        except Exception as e:
            self.display.insert(ctk.END, f"Unexpected error: {e}\n")
            logging.error(f"Unexpected error while installing {tool_name}: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
