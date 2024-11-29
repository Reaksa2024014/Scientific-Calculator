from tkinter import Tk, Entry, Button, StringVar, Frame
from tkinter import messagebox
from tkinter import Toplevel, Text, Label
import math


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Scientific Calculator")
        master.geometry('430x900+0+0')  # Adjusted height
        master.config(bg='#2c2f33')
        master.resizable(True, True)

        self.equation = StringVar()
        self.entry_value = ""
        self.is_radian = True  # Default to radians
        self.is_dark_mode = True  # Default to dark mode

        # Colors for modes
        self.colors = {
            "dark": {"bg": "#2c2f33", "fg": "white", "button_bg": "#7289da", "button_fg": "white"},
            "light": {"bg": "#ffffff", "fg": "black", "button_bg": "#d3d3d3", "button_fg": "black"},
        }

        # Stylish Entry Widget
        self.entry = Entry(master, width=22, bg=self.colors["dark"]["bg"], fg=self.colors["dark"]["fg"],
                           font=("Arial", 24), textvariable=self.equation, bd=5, highlightthickness=0, justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, ipady=10, padx=10, pady=10, sticky="nsew")

        # Create a Frame for buttons
        self.button_frame = Frame(master, bg=self.colors["dark"]["bg"])
        self.button_frame.place(x=10, y=80, width=410, height=550)

        # Configure grid weights for uniform distribution
        for i in range(8):  # Updated to 8 rows
            self.button_frame.rowconfigure(i, weight=1)
        for j in range(4):  # 4 columns
            self.button_frame.columnconfigure(j, weight=1)

        # Button configuration
        buttons = [
            ['C', '(', ')', '%'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['.', '0', '=', '/'],
            ['sin', 'cos', 'tan', '√'],
            ['!', 'log', 'ln', '^'],
            ['10^', 'e^', 'π', 'e'],
        ]

        self.button_widgets = []  # Store button widgets for color toggle

        for i, row in enumerate(buttons):
            for j, btn in enumerate(row):
                button = Button(self.button_frame, text=btn, font=("Arial", 18), bg=self.colors["dark"]["button_bg"],
                                fg=self.colors["dark"]["button_fg"], activebackground=self.colors["dark"]["button_bg"],
                                activeforeground=self.colors["dark"]["fg"], relief='flat', height=2, width=6,
                                command=lambda b=btn: self.on_button_click(b))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.button_widgets.append(button)

        # Usage History Button
        self.usage_history_button = Button(self.master, text="Usage History", font=("Arial", 14), 
                                   bg=self.colors["dark"]["button_bg"], fg=self.colors["dark"]["button_fg"], 
                                   command=self.show_usage_history)
        self.usage_history_button.place(x=250, y=645)


        # Toggle radian/degree mode button
        self.toggle_mode_button = Button(self.master, text="Rad", font=("Arial", 14), bg=self.colors["dark"]["button_bg"],
                                          fg=self.colors["dark"]["button_fg"], command=self.toggle_mode)
        self.toggle_mode_button.place(x=50, y=645)

        # Toggle Dark/Light Mode Button
        self.mode_button = Button(self.master, text="Light Mode", font=("Arial", 14),
                                  bg=self.colors["dark"]["button_bg"], fg=self.colors["dark"]["button_fg"],
                                  command=self.toggle_theme)
        self.mode_button.place(x=120, y=645)

    def toggle_theme(self):
        """Toggles between dark mode and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        mode = "dark" if self.is_dark_mode else "light"
        self.master.config(bg=self.colors[mode]["bg"])
        self.button_frame.config(bg=self.colors[mode]["bg"])
        self.entry.config(bg=self.colors[mode]["bg"], fg=self.colors[mode]["fg"])

        # Update button colors
        for button in self.button_widgets:
            button.config(bg=self.colors[mode]["button_bg"], fg=self.colors[mode]["button_fg"],
                          activebackground=self.colors[mode]["button_bg"], activeforeground=self.colors[mode]["fg"])

        # Update other buttons
        self.toggle_mode_button.config(bg=self.colors[mode]["button_bg"], fg=self.colors[mode]["button_fg"])
        self.mode_button.config(bg=self.colors[mode]["button_bg"], fg=self.colors[mode]["button_fg"])
        self.usage_history_button.config(bg=self.colors[mode]["button_bg"], fg=self.colors[mode]["button_fg"])


        # Change the toggle button text
        self.mode_button.config(text="Dark Mode" if mode == "light" else "Light Mode")

    def on_button_click(self, button):
        try:
            if button == "C":
                self.clear()
            elif button == "=":
                self.solve()
            elif button == "^":
                self.entry_value += "**"
                self.equation.set(self.entry_value)
            elif button == "√":
                self.solve_advanced("sqrt")
            elif button == "log":
                self.solve_advanced("log")
            elif button == "ln":
                self.solve_advanced("ln")
            elif button == "rad":
                self.set_mode("rad")
            elif button == "deg":
                self.set_mode("deg")
            elif button == "π":
                self.entry_value += str(math.pi)
                self.equation.set(self.entry_value)
            elif button == "e":
                self.entry_value += str(math.e)
                self.equation.set(self.entry_value)
            elif button in ["sin", "cos", "tan"]:
                self.solve_advanced(button)
            elif button == "!":
                self.solve_advanced("factorial")
            else:
                self.show(button)
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Operation: {str(e)}")

    def set_mode(self, mode):
        """Sets the mode to either radian or degree."""
        if mode == "rad":
            self.is_radian = True
            self.toggle_mode_button.config(text="Rad")
        elif mode == "deg":
            self.is_radian = False
            self.toggle_mode_button.config(text="Deg")
        
    def toggle_mode(self):
        """Toggles between radian and degree modes."""
        if self.is_radian:
            self.set_mode("deg")
        else:
            self.set_mode("rad")

    def add_10_power(self):
        """Adds 10^ to the equation."""
        self.entry_value += "10**"
        self.equation.set(self.entry_value)

    def add_e_power(self):
        """Adds e^ to the equation."""
        self.entry_value += "math.e**"
        self.equation.set(self.entry_value)

    def solve_advanced(self, operation):
        try:
            if self.entry_value == "":
                raise ValueError("Empty Input")
            value = float(self.entry_value)

            if operation == "sqrt":
                result = math.sqrt(value)
            elif operation == "log":
                result = math.log10(value)
            elif operation == "ln":
                result = math.log(value)  # Natural log
            elif operation == "factorial":
                if not value.is_integer() or value < 0:
                    raise ValueError("Factorial undefined for non-integer or negative values")
                result = math.factorial(int(value))
            elif operation == "sin":
                result = math.sin(math.radians(value)) if not self.is_radian else math.sin(value)
            elif operation == "cos":
                result = math.cos(math.radians(value)) if not self.is_radian else math.cos(value)
            elif operation == "tan":
                result = math.tan(math.radians(value)) if not self.is_radian else math.tan(value)

            self.equation.set(result)
            self.entry_value = str(result)

            # Save to history
            self.save_to_history(f"{operation}({value}) = {result}")
        except ValueError:
            self.equation.set("Error")
            self.entry_value = ""

    def show(self, value):
        self.entry_value += str(value)
        self.equation.set(self.entry_value)

    def clear(self):
        self.entry_value = ""
        self.equation.set(self.entry_value)

    def solve(self):
        try:
            # First, check for 10^ and e^ and convert them properly for evaluation
            if "10^" in self.entry_value:
                self.entry_value = self.entry_value.replace("10^", "10**")
            if "e^" in self.entry_value:
                self.entry_value = self.entry_value.replace("e^", "math.e**")


            result = eval(self.entry_value)
            self.equation.set(result)

            # Save to history
            self.save_to_history(f"{self.entry_value} = {result}")
            self.entry_value = str(result)
        except Exception as e:
            self.equation.set(f"Error: {str(e)}")
            self.entry_value = ""

    def save_to_history(self, operation):
        """Saves the operation to a file"""
        with open("usage_history.txt", "a") as file:
            file.write(operation + "\n")

    def clear_history(self):
        """Clears the usage history"""
        with open("usage_history.txt", "w") as file:
            file.truncate()
        messagebox.showinfo("History Cleared", "Usage history has been cleared!")

    def show_usage_history(self):
        """Displays the usage history in a new window with editing functionality"""
        history_window = Toplevel(self.master)
        history_window.title("Usage History")
        history_window.geometry("400x300")
        history_window.config(bg="#2c2f33")

        Label(history_window, text="Usage History (Click to Use)", font=("Arial", 16), bg="#2c2f33", fg="white").pack(pady=10)

        history_box = Text(history_window, height=15, width=40, font=("Arial", 14), bg="#23272a", fg="white")
        history_box.pack(pady=10)

        # Load history from the file
        try:
            with open("usage_history.txt", "r") as file:
                history_content = file.readlines()
                for line in history_content:
                    history_box.insert("end", line)
        except FileNotFoundError:
            history_box.insert("1.0", "No history found.")

        # Enable single-click functionality
        def on_history_click(event):
            selected_line = history_box.get("insert linestart", "insert lineend").strip()
            if selected_line:
                # Extract calculation part from history line if formatted as "calculation = result"
                if "=" in selected_line:
                    selected_line = selected_line.split("=")[0].strip()
                self.entry_value = selected_line
                self.equation.set(selected_line)
                history_window.destroy()

        history_box.bind("<Button-1>", on_history_click)
        history_box.config(state="normal", cursor="hand2")

root = Tk()
calculator = Calculator(root)
root.mainloop()
