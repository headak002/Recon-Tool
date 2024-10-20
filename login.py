import customtkinter as ctk

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, switch_to_main):
        super().__init__(master)
        self.switch_to_main = switch_to_main
        self.initUI()

    def initUI(self):
        self.username_label = ctk.CTkLabel(self, text='Username:')
        self.username_label.pack(pady=10)
        self.username_input = ctk.CTkEntry(self)
        self.username_input.pack(pady=5)

        self.password_label = ctk.CTkLabel(self, text='Password:')
        self.password_label.pack(pady=10)
        self.password_input = ctk.CTkEntry(self, show='*')
        self.password_input.pack(pady=5)

        self.login_btn = ctk.CTkButton(self, text='Login', command=self.check_credentials)
        self.login_btn.pack(pady=10)

        self.label_error = ctk.CTkLabel(self, text="")
        self.label_error.pack()

        self.pack(padx=20, pady=20)

    def check_credentials(self):
        username = self.username_input.get()
        password = self.password_input.get()

        # Hardcoded credentials (replace with a secure method in real applications)
        if username == 'admin' and password == 'password123':
            self.switch_to_main()  # Call the function to switch to the main tool
        else:
            # Use 'configure' instead of 'config'
            self.label_error.configure(text="Invalid credentials", text_color="red")

