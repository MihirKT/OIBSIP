import requests
import json
import tkinter as tk
from tkinter import messagebox
import geocoder

# Function to fetch weather data from API using GPS coordinates
def fetch_weather_data_by_coordinates(latitude, longitude):
    api_key = "16358f07cbbd23e5f9e60f30acbf4362"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to fetch weather data from API using location name
def fetch_weather_data_by_location(location):
    api_key = "16358f07cbbd23e5f9e60f30acbf4362"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Function to convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Function to convert temperature from Kelvin to Fahrenheit
def kelvin_to_fahrenheit(kelvin):
    return kelvin * 9/5 - 459.67

# Function to display weather data for beginners
def display_weather_data(data, unit='Celsius'):
    if data['cod'] == 200:
        print(f"Weather in {data['name']}:")
        temperature = data['main']['temp']
        if unit == 'Celsius':
            temperature = kelvin_to_celsius(temperature)
            print(f"Temperature: {temperature:.2f}°C")
        else:
            temperature = kelvin_to_fahrenheit(temperature)
            print(f"Temperature: {temperature:.2f}°F")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Weather Condition: {data['weather'][0]['description']}")
    else:
        print("Error:", data['message'])

# Function to fetch and display weather data for advanced users using Tkinter
def show_weather_gui():
    def get_weather():
        if location_choice.get() == 1:  # Current Location
            latitude, longitude = get_gps_coordinates()
            data = fetch_weather_data_by_coordinates(latitude, longitude)
        else:  # Enter Location
            location = location_entry.get()
            data = fetch_weather_data_by_location(location)
            
        if data['cod'] == 200:
            temperature = data['main']['temp']
            if temperature_unit.get() == 'Celsius':
                temperature = kelvin_to_celsius(temperature)
                temperature_label.config(text=f"Temperature: {temperature:.2f}°C")
            else:
                temperature = kelvin_to_fahrenheit(temperature)
                temperature_label.config(text=f"Temperature: {temperature:.2f}°F")
            humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
            condition_label.config(text=f"Weather Condition: {data['weather'][0]['description']}")
        else:
            messagebox.showerror("Error", data['message'])

    def toggle_unit():
        if temperature_unit.get() == 'Celsius':
            temperature_unit.set('Fahrenheit')
        else:
            temperature_unit.set('Celsius')

    def enable_disable_entry():
        if location_choice.get() == 1:  # Current Location
            location_entry.config(state=tk.DISABLED)
        else:  # Enter Location
            location_entry.config(state=tk.NORMAL)

    def get_gps_coordinates():
        g = geocoder.ip('me')
        return g.latlng

    root = tk.Tk()
    root.title("Weather App")

    welcome_label = tk.Label(root, text="Welcome to Weather App")
    welcome_label.pack()

    location_label = tk.Label(root, text="Location:")
    location_label.pack()

    location_choice = tk.IntVar()
    current_location_radio = tk.Radiobutton(root, text="Current Location", variable=location_choice, value=1, command=enable_disable_entry)
    current_location_radio.pack()
    enter_location_radio = tk.Radiobutton(root, text="Enter Location", variable=location_choice, value=2, command=enable_disable_entry)
    enter_location_radio.pack()

    location_entry = tk.Entry(root)
    location_entry.pack()

    get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
    get_weather_button.pack()

    temperature_label = tk.Label(root, text="")
    temperature_label.pack()

    humidity_label = tk.Label(root, text="")
    humidity_label.pack()

    condition_label = tk.Label(root, text="")
    condition_label.pack()

    temperature_unit = tk.StringVar()
    temperature_unit.set('Celsius')
    unit_button = tk.Button(root, textvariable=temperature_unit, command=toggle_unit)
    unit_button.pack()

    enable_disable_entry()  # Initially disable entry for current location

    root.mainloop()

# Main function to choose mode
def main():
    print("Welcome to the Weather App!")
    print("Choose your mode:")
    print("[1] Beginner (Console)")
    print("[2] Advanced (GUI)")
    mode = input("Enter your choice: ")

    if mode == '1':
        location = input("Enter location: ")
        unit_choice = input("Choose unit: [1] Celsius [2] Fahrenheit: ")
        if unit_choice == '1':
            unit = 'Celsius'
        else:
            unit = 'Fahrenheit'
        data = fetch_weather_data_by_location(location)
        display_weather_data(data, unit)
    elif mode == '2':
        show_weather_gui()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
