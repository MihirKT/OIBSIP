import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt

# Function to calculate BMI for command-line version
def calculate_bmi_cli(weight, height):
    height_m = height / 100 if height_choice in ['cm', 'centimeter'] else height / 39.3701 if height_choice in ['in', 'inch'] else height / 3.28084 if height_choice in ['ft', 'feet'] else height
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category

# Function to calculate BMI for GUI version
def calculate_bmi_gui():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        height_choice = height_var.get()
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive numbers.")
    except ValueError as e:
        result_label.config(text=str(e))
        return

    # Convert height to meters
    if height_choice == 'cm':
        height_m = height / 100
    elif height_choice == 'in':
        height_m = height / 39.3701
    elif height_choice == 'ft':
        height_m = height / 3.28084
    else:
        height_m = height

    # Calculate BMI
    bmi = weight / (height_m ** 2)

    # Classify BMI category
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # Display BMI result
    result_label.config(text=f"BMI: {bmi:.2f} ({category})")

    # Store data in the database
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bmi_data (user_id INTEGER PRIMARY KEY, weight REAL, height REAL, bmi REAL, category TEXT)''')
    c.execute('''INSERT INTO bmi_data (weight, height, bmi, category) VALUES (?, ?, ?, ?)''', (weight, height, bmi, category))
    conn.commit()
    conn.close()

# Function to show BMI trends
def show_trends():
    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()
    c.execute('''SELECT bmi FROM bmi_data''')
    data = c.fetchall()
    conn.close()

    bmi_values = [record[0] for record in data]
    plt.plot(bmi_values)
    plt.xlabel('User')
    plt.ylabel('BMI')
    plt.title('BMI Trends')
    plt.show()

# Beginner Part: Command-Line BMI Calculator
def beginner_bmi_calculator():
    try:
        weight = float(input("Enter your weight in kilograms: "))
        height = float(input("Enter your height: "))
        global height_choice
        height_choice = input("Choose height unit (cm/in/ft/meter): ").lower()
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive numbers.")
    except ValueError as e:
        print("Error:", e)
        return

    bmi, category = calculate_bmi_cli(weight, height)
    print(f"Your BMI is: {bmi:.2f} ({category})")

# Advanced Part: Graphical BMI Calculator with Tkinter
def advanced_bmi_calculator():
    # GUI
    root = tk.Tk()
    root.title("BMI Calculator")

    weight_label = tk.Label(root, text="Weight (kg):")
    weight_label.grid(row=0, column=0)

    global weight_entry
    weight_entry = tk.Entry(root)
    weight_entry.grid(row=0, column=1)

    height_label = tk.Label(root, text="Height:")
    height_label.grid(row=1, column=0)

    global height_entry
    height_entry = tk.Entry(root)
    height_entry.grid(row=1, column=1)

    global height_var
    height_var = tk.StringVar()
    height_var.set("m")
    height_choices = ['m', 'cm', 'in', 'ft']
    height_optionmenu = tk.OptionMenu(root, height_var, *height_choices)
    height_optionmenu.grid(row=1, column=2)

    calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi_gui)
    calculate_button.grid(row=2, columnspan=3)

    global result_label
    result_label = tk.Label(root, text="")
    result_label.grid(row=3, columnspan=3)

    trends_button = tk.Button(root, text="Show BMI Trends", command=show_trends)
    trends_button.grid(row=4, columnspan=3)

    root.mainloop()

# Main function to choose mode
def main():
    print("Choose your mode:")
    print("[1] Beginner (Command Line)")
    print("[2] Advanced (Graphical with Tkinter)")
    mode = input("Enter your choice: ")

    if mode == '1':
        beginner_bmi_calculator()  # Beginner Part
    elif mode == '2':
        advanced_bmi_calculator()  # Advanced Part
    else:
        print("Invalid choice.")

# Call the Function to Choose Mode
if __name__ == "__main__":
    main()