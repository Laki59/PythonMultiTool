import customtkinter as ctk
import os, shutil, requests, pyqrcode
from tkinter import messagebox
import psutil
import GPUtil
import requests
import tempfile


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🧠 My Tools Collection")
app.geometry("600x600")

tabview = ctk.CTkTabview(app)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

# -------------------------------------------------------
# 🧮 TAB 1 — Kalkulator
# -------------------------------------------------------
tab_calc = tabview.add("Kalkulator")

def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        op = operation_var.get()

        if op == "+": res = num1 + num2
        elif op == "-": res = num1 - num2
        elif op == "*": res = num1 * num2
        elif op == "/":
            if num2 == 0: raise ZeroDivisionError
            res = num1 / num2
        else:
            messagebox.showerror("Greška", "Nepoznata operacija")
            return

        result_label.configure(text=f"Rezultat: {res}")
    except ValueError:
        messagebox.showerror("Greška", "Unesite brojeve!")
    except ZeroDivisionError:
        messagebox.showerror("Greška", "Deljenje nulom nije dozvoljeno!")

ctk.CTkLabel(tab_calc, text="🧮 Kalkulator", font=("Arial", 22, "bold")).pack(pady=10)
entry_num1 = ctk.CTkEntry(tab_calc, placeholder_text="Prvi broj"); entry_num1.pack(pady=5)
entry_num2 = ctk.CTkEntry(tab_calc, placeholder_text="Drugi broj"); entry_num2.pack(pady=5)
operation_var = ctk.StringVar(value="+")
ctk.CTkOptionMenu(tab_calc, variable=operation_var, values=["+", "-", "*", "/"]).pack(pady=5)
ctk.CTkButton(tab_calc, text="Izračunaj", command=calculate).pack(pady=10)
result_label = ctk.CTkLabel(tab_calc, text="Rezultat:", font=("Arial", 16))
result_label.pack(pady=5)

# -------------------------------------------------------
# 🗂️ TAB 2 — File Organizer
# -------------------------------------------------------
tab_org = tabview.add("File Organizer")

def organize_files():
    path = path_entry.get().strip()
    if not os.path.exists(path):
        messagebox.showerror("Greška", "Putanja ne postoji!")
        return
    try:
        files = os.listdir(path)
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext[1:]
            if not ext: continue
            folder = os.path.join(path, ext)
            os.makedirs(folder, exist_ok=True)
            shutil.move(os.path.join(path, file), os.path.join(folder, file))
        messagebox.showinfo("Uspeh", "Fajlovi su organizovani po ekstenzijama!")
    except Exception as e:
        messagebox.showerror("Greška", str(e))

ctk.CTkLabel(tab_org, text="🗂️ Organizator fajlova", font=("Arial", 22, "bold")).pack(pady=10)
path_entry = ctk.CTkEntry(tab_org, placeholder_text="Unesite putanju (npr. C:\\Users\\User\\Desktop)")
path_entry.pack(pady=10, fill="x", padx=20)
ctk.CTkButton(tab_org, text="Organizuj fajlove", command=organize_files).pack(pady=10)

# -------------------------------------------------------
# 🧾 TAB 3 — QR Code Generator
# -------------------------------------------------------
tab_qr = tabview.add("QR Kod")

def generate_qr():
    title = qr_title.get().strip()
    text = qr_text.get().strip()
    save_path = fr"C:\Users\User\OneDrive\Desktop\qrkodovi\{title}"
    try:
        if not title or not text:
            messagebox.showerror("Greška", "Popunite sva polja!")
            return
        os.makedirs(save_path, exist_ok=True)
        file_name = f"{title}.png"
        qr = pyqrcode.create(text)
        qr.png(file_name, scale=8)
        shutil.move(file_name, save_path)
        messagebox.showinfo("Uspeh", f"Sacuvano na:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Greška", str(e))

ctk.CTkLabel(tab_qr, text="🔳 QR Kod Generator", font=("Arial", 22, "bold")).pack(pady=10)
qr_title = ctk.CTkEntry(tab_qr, placeholder_text="Naziv QR koda"); qr_title.pack(pady=5, padx=20, fill="x")
qr_text = ctk.CTkEntry(tab_qr, placeholder_text="Tekst ili link za QR kod"); qr_text.pack(pady=5, padx=20, fill="x")
ctk.CTkButton(tab_qr, text="Generiši QR Kod", command=generate_qr).pack(pady=15)

# -------------------------------------------------------
# 🌦️ TAB 4 — Weather Info
# -------------------------------------------------------
tab_weather = tabview.add("Vremenska prognoza")

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Greška", "Unesite grad!")
        return
    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url).json()
        weather = data["current_condition"][0]["weatherDesc"][0]["value"]
        temp = data["current_condition"][0]["temp_C"]
        feels = data["current_condition"][0]["FeelsLikeC"]
        country = data["nearest_area"][0]["country"][0]["value"]
        moon = data["weather"][0]["astronomy"][0]["moon_phase"]
        weather_label.configure(
            text=f"{city}, {country}\n{weather}\nTemp: {temp}°C (oseća se kao {feels}°C)\nFaza meseca: {moon}"
        )
    except Exception as e:
        messagebox.showerror("Greška", f"Nije moguće dohvatiti podatke: {e}")

ctk.CTkLabel(tab_weather, text="🌤️ Vremenska prognoza", font=("Arial", 22, "bold")).pack(pady=10)
city_entry = ctk.CTkEntry(tab_weather, placeholder_text="Unesite grad")
city_entry.pack(pady=10, padx=20, fill="x")
ctk.CTkButton(tab_weather, text="Proveri vreme", command=get_weather).pack(pady=10)
weather_label = ctk.CTkLabel(tab_weather, text="", font=("Arial", 16), justify="center")
weather_label.pack(pady=10)

# -------------------------------------------------------
#  TAB 5 — Computer details
# -------------------------------------------------------
podaci = tabview.add("Podaci o kompijuteru")

def podaciOKompu():

    gpus = GPUtil.getGPUs()
    if not gpus:
        print("No NVIDIA GPUs found.")
        return
    virtual_mem = psutil.virtual_memory()
    #Computer only has one GPU,otherwies would need and if loop
    gpu=gpus[0]
    podaci_label.configure(
        text=f"GPU ime: {gpu.name}\nGPU Temperature: {gpu.temperature}\nGPU Memory total: {gpu.memoryTotal}GB\nGPU Memory used: {gpu.memoryUsed}GB\nGPU Memory free: {gpu.memoryFree}GB\n\nTotal RAM: {virtual_mem.total/1024**3:.2f}GB\nAvailable RAM: {virtual_mem.available/1024**3:.2f}\nUsed RAM: {virtual_mem.used/1024**3:.2f}\nRAM used percentage: {virtual_mem.percent:.2f}")


ctk.CTkLabel(podaci, text="Podaci o kompijuteru", font=("Arial", 22, "bold")).pack(pady=10)
ctk.CTkButton(podaci, text="Klikni za podatke", command=podaciOKompu).pack(pady=10)
podaci_label = ctk.CTkLabel(podaci, text="", font=("Arial", 16), justify="center")
podaci_label.pack(pady=10)

# -------------------------------------------------------
# 🔁 TAB 6 — Unit Converter
# -------------------------------------------------------
tab_convert = tabview.add("Konverter jedinica")

def convert_units():
    try:
        value = float(entry_value.get())
        option = conversion_type.get()
        if option == "Kilometri u milje":
            result = value * 0.621371
            result_label.configure(text=f"{value} km = {result:.2f} milja")
        elif option == "Milje u kilometre":
            result = value / 0.621371
            result_label.configure(text=f"{value} milja = {result:.2f} km")
        elif option == "C → F":
            result = (value * 9/5) + 32
            result_label.configure(text=f"{value}°C = {result:.2f}°F")
        elif option == "F → C":
            result = (value - 32) * 5/9
            result_label.configure(text=f"{value}°F = {result:.2f}°C")
        elif option == "Kg u funte":
            result = value * 2.20462
            result_label.configure(text=f"{value} kg = {result:.2f} lb")
        elif option == "Funte u kg":
            result = value / 2.20462
            result_label.configure(text=f"{value} lb = {result:.2f} kg")
    except ValueError:
        messagebox.showerror("Greška", "Unesite brojčanu vrednost!")

ctk.CTkLabel(tab_convert, text="🔁 Konverter jedinica", font=("Arial", 22, "bold")).pack(pady=10)
entry_value = ctk.CTkEntry(tab_convert, placeholder_text="Unesite vrednost")
entry_value.pack(pady=10, padx=20, fill="x")
conversion_type = ctk.StringVar(value="Kilometri u milje")
ctk.CTkOptionMenu(tab_convert, variable=conversion_type,
                  values=["Kilometri u milje", "Milje u kilometre", "C → F", "F → C", "Kg u funte", "Funte u kg"]).pack(pady=5)
ctk.CTkButton(tab_convert, text="Pretvori", command=convert_units).pack(pady=10)
result_label = ctk.CTkLabel(tab_convert, text="", font=("Arial", 16))
result_label.pack(pady=10)

# -------------------------------------------------------
# 🔁 TAB 7 — Temp file cleaner
# -------------------------------------------------------
tab_temp = tabview.add("Temp Cleaner")

progress_bar = ctk.CTkProgressBar(tab_temp, width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)

temp_label = ctk.CTkLabel(tab_temp, text="", font=("Arial", 16))
temp_label.pack(pady=5)

def clean_temp():
    import tempfile
    temp_dir = tempfile.gettempdir() 
    try:
        total_items = sum(len(files) + len(dirs) for _, dirs, files in os.walk(temp_dir))
        if total_items == 0:
            messagebox.showinfo("Info", "Nema ništa za brisanje u temp folderu!")
            return

        files_deleted = 0

        for root, dirs, files in os.walk(temp_dir):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                except Exception:
                    pass
                files_deleted += 1
                progress_bar.set(files_deleted / total_items)
                tab_temp.update_idletasks() 

            for d in dirs:
                try:
                    shutil.rmtree(os.path.join(root, d))
                except Exception:
                    pass
                files_deleted += 1
                progress_bar.set(files_deleted / total_items)
                tab_temp.update_idletasks()

        messagebox.showinfo("Uspeh", f"Obrisano {files_deleted} privremenih fajlova/foldera!")
        temp_label.configure(text=f"✅ Obrisano {files_deleted} fajlova/foldera!")
        progress_bar.set(0) 
    except Exception as e:
        messagebox.showerror("Greška", f"Došlo je do greške:\n{e}")


ctk.CTkLabel(tab_temp, text="🧹 Temp Cleaner", font=("Arial", 22, "bold")).pack(pady=10)
ctk.CTkButton(tab_temp, text="Očisti privremene fajlove", command=clean_temp).pack(pady=20)

# -------------------------------------------------------
# Pokretanje aplikacije
# -------------------------------------------------------
app.mainloop()
