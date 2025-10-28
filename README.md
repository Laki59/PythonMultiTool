# 🧠 My Tools Collection
**A modern multi-tool Python desktop app built with `customtkinter`.** It combines seven mini utilities in one beautiful dark-themed GUI.

## 🚀 Features

### 🧮 Modern Calculator
- Clean and simple calculator supporting addition, subtraction, multiplication, and division
- Division-by-zero check included
- Input validation and instant result display

### 🗂️ File Organizer
- Automatically organizes files in a chosen folder by file extension
- Example structure:
C:\Desktop
┣━ .jpg
┣━ .pdf
┗━ .txt
- Keeps your folders clean and structured automatically

### 🔳 QR Code Generator
- Generate QR codes from text or links
- Saves generated codes as `.png` files
- Automatically creates a folder on your Desktop
- Perfect for sharing links, Wi-Fi passwords, or messages

### 🌦️ Weather Checker
- Fetches real-time weather data using the wttr.in API
- Displays: Temperature, Feels-like temperature, Weather description, Moon phase, Country information

### 💻 Computer Details
- Shows GPU info (name, temperature, memory usage)
- Displays RAM usage (total, available, used, percentage)
- Works with GPUs detected by GPUtil

### 🔁 Unit Converter
- Convert between Kilometers ↔ Miles, Celsius ↔ Fahrenheit, Kg ↔ Pounds
- Instant conversion with a dropdown for unit selection

### 🧹 Temp File Cleaner
- Cleans system temporary folder
- Deletes files and empty folders in temp directories
- Includes progress bar for real-time cleaning feedback
- Safe deletion with error handling

## ⚙️ Installation
1. Clone the repository
2. Install required dependencies:
pip install customtkinter pyqrcode pypng requests psutil gputil
3. Run the app:
python app.py

## 🧩 Tech Stack
- Python 3
- customtkinter – Modern, responsive UI
- requests – Weather API communication
- pyqrcode + pypng – QR code generation
- os + shutil + tempfile – File handling, organization, and temp cleaning
- psutil + GPUtil – System and GPU information

## 🌟 Future Improvements
- Add icons and better layout for each tool
- Include Light/Dark theme switcher
- Add YouTube downloader, currency converter, or unit converter enhancements
- Package into a single `.exe` with PyInstaller

## 💡 Author
**Lazar Ginić**

## 📜 License
Released under the MIT License — free to use, modify, and share.

⭐ If you like this project, consider giving it a star on GitHub!
