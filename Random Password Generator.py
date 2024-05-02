import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

# Function to generate a random password
def generate_password(length, use_letters, use_numbers, use_symbols):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Error", "Please select at least one character type.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to run the GUI password generator with Tkinter
def gui_password_generator():
    def generate():
        try:
            length = int(length_entry.get())
            use_letters = letters_var.get()
            use_numbers = numbers_var.get()
            use_symbols = symbols_var.get()

            password = generate_password(length, use_letters, use_numbers, use_symbols)
            if password:
                password_entry.delete(0, tk.END)
                password_entry.insert(0, password)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid password length.")

    def copy_to_clipboard():
        password = password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard.")

    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("400x300")
    root.configure(bg="#f0f0f0")

    title_label = tk.Label(root, text="Password Generator", font=("Arial", 20), bg="#f0f0f0", padx=10, pady=10)
    title_label.pack()

    length_label = tk.Label(root, text="Password Length:", font=("Arial", 12), bg="#f0f0f0")
    length_label.pack()

    length_entry = tk.Entry(root, font=("Arial", 12))
    length_entry.pack()

    letters_var = tk.BooleanVar()
    letters_check = tk.Checkbutton(root, text="Include Letters", variable=letters_var, font=("Arial", 12), bg="#f0f0f0")
    letters_check.pack()

    numbers_var = tk.BooleanVar()
    numbers_check = tk.Checkbutton(root, text="Include Numbers", variable=numbers_var, font=("Arial", 12), bg="#f0f0f0")
    numbers_check.pack()

    symbols_var = tk.BooleanVar()
    symbols_check = tk.Checkbutton(root, text="Include Symbols", variable=symbols_var, font=("Arial", 12), bg="#f0f0f0")
    symbols_check.pack()

    generate_button = tk.Button(root, text="Generate Password", command=generate, font=("Arial", 12), bg="#007bff", fg="white")
    generate_button.pack(pady=10)

    password_entry = tk.Entry(root, width=30, font=("Arial", 12))
    password_entry.pack()

    copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 12), bg="#28a745", fg="white")
    copy_button.pack(pady=10)

    root.mainloop()

# Main function to choose mode
def main():
    print("Choose your mode:")
    print("[1] Beginner (Command Line)")
    print("[2] Advanced (GUI)")
    mode = input("Enter your choice: ")

    if mode == '1':
        command_line_password_generator()  # Beginner Part
    elif mode == '2':
        gui_password_generator()  # Advanced Part
    else:
        print("Invalid choice.")

# Function to run the command-line password generator
def command_line_password_generator():
    length = int(input("Enter the length of the password: "))
    use_letters = input("Include letters? (yes/no): ").lower() == 'yes'
    use_numbers = input("Include numbers? (yes/no): ").lower() == 'yes'
    use_symbols = input("Include symbols? (yes/no): ").lower() == 'yes'

    password = generate_password(length, use_letters, use_numbers, use_symbols)
    if password:
        print("Generated Password:", password)

# Call the Function to Choose Mode
main()
