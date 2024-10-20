import customtkinter as ctk
from login import LoginPage
from recon_tool import ReconTool
from welcome_screen import WelcomeScreen

class MainApplication(ctk.CTk):  # Ensure you are inheriting from CTk
    def __init__(self):
        super().__init__()
        self.title("Recon Tool Application")
        self.geometry("600x400")

        self.frames = {}

        print("Initializing Main Application")
        self.show_welcome_screen()

    def show_welcome_screen(self):
        print("Attempting to show Welcome Screen...")
        try:
            self.welcome_screen = WelcomeScreen(self, self.show_login_page)
            print("Welcome Screen initialized successfully.")
            self.welcome_screen.pack(fill="both", expand=True)
        except Exception as e:
            print(f"Error in initializing Welcome Screen: {e}")

    def show_login_page(self):
        for widget in self.winfo_children():
            widget.destroy()

        login_page = LoginPage(self, self.show_recon_tool)
        login_page.pack(fill="both", expand=True)

    def show_recon_tool(self):
        for widget in self.winfo_children():
            widget.destroy()

        recon_tool_page = ReconTool(self)
        recon_tool_page.pack(fill="both", expand=True)

if __name__ == '__main__':
    app = MainApplication()  # Initialize the application properly
    app.mainloop()           # Start the main loop to run the GUI

