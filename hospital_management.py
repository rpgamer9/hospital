import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Setup
def setup_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        insurance TEXT,
                        faskes TEXT)''')
    conn.commit()
    conn.close()

setup_db()

# Language Dictionary
translations = {
    "ID": {"title": "Sistem Manajemen Rumah Sakit", "register": "Daftar Pasien", "view": "Lihat Data", "name": "Nama", "age": "Usia", "insurance": "Asuransi", "faskes": "Faskes", "save": "Simpan", "success": "Pasien berhasil didaftarkan!", "error": "Mohon isi semua data!", "faskes_options": ["Faskes 1", "Faskes 2", "Faskes 3"]},
    "EN": {"title": "Hospital Management System", "register": "Register Patient", "view": "View Data", "name": "Name", "age": "Age", "insurance": "Insurance", "faskes": "Facility", "save": "Save", "success": "Patient registered successfully!", "error": "Please fill in all fields!", "faskes_options": ["Primary Facility", "Secondary Facility", "Tertiary Facility"]}
}

# Main GUI
class HospitalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("600x400")
        
        # Language Selection
        self.language = tk.StringVar(value="ID")
        self.language.trace_add("write", self.update_language)
        lang_frame = ttk.Frame(root)
        lang_frame.pack(pady=10)
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT)
        ttk.Combobox(lang_frame, textvariable=self.language, values=["ID", "EN"], width=5).pack(side=tk.LEFT)
        
        # Title
        self.title_label = ttk.Label(root, text="Sistem Manajemen Rumah Sakit", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # Buttons
        self.register_button = ttk.Button(root, text="Daftar Pasien", command=self.register_patient)
        self.register_button.pack(pady=5)
        
        self.view_button = ttk.Button(root, text="Lihat Data", command=self.view_patients)
        self.view_button.pack(pady=5)
    
    def update_language(self, *args):
        lang = self.language.get()
        self.title_label.config(text=translations[lang]["title"])
        self.register_button.config(text=translations[lang]["register"])
        self.view_button.config(text=translations[lang]["view"])
    
    def register_patient(self):
        lang = self.language.get()
        reg_window = tk.Toplevel(self.root)
        reg_window.title(translations[lang]["register"])
        reg_window.geometry("400x300")
        
        ttk.Label(reg_window, text=translations[lang]["name"]).pack()
        name_entry = ttk.Entry(reg_window)
        name_entry.pack()
        
        ttk.Label(reg_window, text=translations[lang]["age"]).pack()
        age_entry = ttk.Entry(reg_window)
        age_entry.pack()
        
        ttk.Label(reg_window, text=translations[lang]["insurance"]).pack()
        insurance_combo = ttk.Combobox(reg_window, values=["BPJS", "Allianz", "Prudential", "Mandiri"])
        insurance_combo.pack()
        
        ttk.Label(reg_window, text=translations[lang]["faskes"]).pack()
        faskes_combo = ttk.Combobox(reg_window, values=translations[lang]["faskes_options"])
        faskes_combo.pack()
        
        def save_patient():
            name = name_entry.get()
            age = age_entry.get()
            insurance = insurance_combo.get()
            faskes = faskes_combo.get()
            
            if name and age and insurance and faskes:
                conn = sqlite3.connect("hospital.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO patients (name, age, insurance, faskes) VALUES (?, ?, ?, ?)", (name, age, insurance, faskes))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", translations[lang]["success"])
                reg_window.destroy()
            else:
                messagebox.showwarning("Error", translations[lang]["error"])
        
        ttk.Button(reg_window, text=translations[lang]["save"], command=save_patient).pack(pady=10)
    
    def view_patients(self):
        lang = self.language.get()
        view_window = tk.Toplevel(self.root)
        view_window.title(translations[lang]["view"])
        view_window.geometry("500x300")
        
        tree = ttk.Treeview(view_window, columns=("ID", "Nama", "Usia", "Asuransi", "Faskes"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nama", text=translations[lang]["name"])
        tree.heading("Usia", text=translations[lang]["age"])
        tree.heading("Asuransi", text=translations[lang]["insurance"])
        tree.heading("Faskes", text=translations[lang]["faskes"])
        tree.pack(fill=tk.BOTH, expand=True)
        
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root)
    root.mainloop()

