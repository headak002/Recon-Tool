import customtkinter as ctk
import time

class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, show_login_page):
        super().__init__(parent)
        
        # Gradient Background colors
        self.gradient_colors = ["#007acc", "#000000"]  # Blue to Black gradient
        
        # Initial Setup
        self.configure(fg_color="#000000")
        
        # Title Label with modern styling
        self.title_label = ctk.CTkLabel(self, text="Welcome to Vul_Rec", font=("Arial", 35, "bold"), text_color="#FFFFFF")
        self.title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Subtitle with modern styling
        self.subtitle_label = ctk.CTkLabel(self, text="Your Ultimate Reconnaissance Tool", font=("Arial", 20), text_color="#BBBBBB")
        self.subtitle_label.place(relx=0.5, rely=0.35, anchor="center")
        
        # Start Button with hover effects
        self.start_button = ctk.CTkButton(self, text="Get Started", command=show_login_page, font=("Arial", 16, "bold"), 
                                          fg_color="#007acc", hover_color="#005999", corner_radius=10)
        self.start_button.place(relx=0.5, rely=0.6, anchor="center")
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.place(relx=0.5, rely=0.75, anchor="center")
        
        # Shadow label for version
        self.version_label = ctk.CTkLabel(self, text="ReconVapt v1.0", font=("Arial", 14, "italic"), text_color="#777")
        self.version_label.place(relx=0.5, rely=0.9, anchor="center")
        
        # Animation variables
        self.fade_in_step = 0
        self.progress_step = 0

        # Start the animations
        self.animate_fade_in()
        self.animate_progress_bar()
    
    def animate_fade_in(self):
        """Smooth fade-in effect for labels."""
        if self.fade_in_step <= 1:
            fade_color = f"#{int(255*self.fade_in_step):02x}{int(255*self.fade_in_step):02x}{int(255*self.fade_in_step):02x}"
            
            # Update color based on the step for a fade-in effect
            self.title_label.configure(text_color=fade_color)
            self.subtitle_label.configure(text_color=fade_color)
            
            # Update the fade_in_step and recall the method
            self.fade_in_step += 0.05
            self.after(50, self.animate_fade_in)
    
    def animate_progress_bar(self):
        """Progress bar animation to simulate loading."""
        if self.progress_step <= 1:
            self.progress_bar.set(self.progress_step)
            self.progress_step += 0.01
            self.after(50, self.animate_progress_bar)
        else:
            # Once the progress completes, display the login screen
            self.show_login_page()

if __name__ == "__main__":
    print("This script is part of the Recon Tool application and cannot be run directly.")
