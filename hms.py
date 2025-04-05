import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import datetime
import os
from PIL import Image, ImageTk
import webbrowser
import csv

class HMSApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "English"
        
        # Language dictionaries
        self.languages = {
            "English": {
                # Main window
                "title": "Hospital Management System",
                "status_ready": "Ready",
                "welcome": "Welcome to Hospital Management System",
                
                # Menu items
                "menu_file": "File",
                "menu_modules": "Modules",
                "menu_patient": "Patient Registration",
                "menu_medical": "Medical Records",
                "menu_doctor": "Doctor Management",
                "menu_billing": "Billing",
                "menu_report": "Reports",
                "menu_lang": "Language",
                "menu_exit": "Exit",
                
                # Common buttons
                "button_save": "Save",
                "button_clear": "Clear",
                "button_back": "Back",
                "button_register": "Register",
                "button_calculate": "Calculate",
                "button_generate": "Generate Report",
                "button_export": "Export to CSV",
                
                # Patient registration
                "patient_registration": "Patient Registration",
                "full_name": "Full Name:",
                "dob": "Date of Birth:",
                "gender": "Gender:",
                "male": "Male",
                "female": "Female",
                "other": "Other",
                "address": "Address:",
                "phone": "Phone:",
                "email": "Email:",
                "id_type": "ID Type:",
                "id_number": "ID Number:",
                "insurance_type": "Insurance Type:",
                "insurance_number": "Insurance Number:",
                "registered_patients": "Registered Patients",
                "bpjs_number": "BPJS Number:",
                "faskes_level": "Faskes Level:",
                "referral_letter": "Referral Letter:",
                "policy_number": "Policy Number:",
                "member_since": "Member Since:",
                "plan_type": "Plan Type:",
                
                # Medical records
                "medical_records": "Medical Records",
                "patient": "Patient:",
                "visit_date": "Visit Date:",
                "doctor": "Doctor:",
                "diagnosis": "Diagnosis:",
                "treatment": "Treatment:",
                "notes": "Notes:",
                "records_list": "Medical Records",
                
                # Doctor management
                "doctor_management": "Doctor Management",
                "name": "Name:",
                "specialization": "Specialization:",
                "schedule": "Schedule:",
                "doctors_list": "Doctors List",
                
                # Billing
                "billing": "Billing",
                "medical_visit": "Medical Visit:",
                "total_amount": "Total Amount (IDR):",
                "insurance_coverage": "Insurance Coverage (IDR):",
                "patient_payment": "Patient Payment (IDR):",
                "payment_status": "Payment Status:",
                "pending": "Pending",
                "paid": "Paid",
                "insurance_claim": "Insurance Claim",
                "payment_method": "Payment Method:",
                "cash": "Cash",
                "credit_card": "Credit Card",
                "debit_card": "Debit Card",
                "bank_transfer": "Bank Transfer",
                "payment_date": "Payment Date:",
                "billing_records": "Billing Records",
                
                # Reports
                "reports": "Reports",
                "select_report": "Select Report Type:",
                "start_date": "Start Date:",
                "end_date": "End Date:",
                "report_types": ["Patient List", "Doctor List", "Medical Visits", "Billing Summary", "Insurance Claims"],
                
                # Messages
                "error": "Error",
                "success": "Success",
                "database_error": "Database Error",
                "required_fields": "Please fill in all required fields",
                "invalid_numbers": "Please enter valid numbers",
                "invalid_date": "Please enter dates in YYYY-MM-DD format",
                "patient_registered": "Patient registered successfully",
                "record_saved": "Record saved successfully",
                "doctor_saved": "Doctor information saved successfully",
                "billing_saved": "Billing record saved successfully",
                "report_exported": "Report exported successfully",
                "no_report": "No report to export",
                
                # Insurance calculators
                "bpjs_calculator": "BPJS Kesehatan Contribution Calculator",
                "salary": "Monthly Salary (IDR):",
                "family_members": "Number of Family Members:",
                "calculate_contribution": "Calculate Contribution",
                "allianz_calculator": "Allianz Insurance Coverage Calculator",
                "prudential_calculator": "Prudential Insurance Coverage Calculator",
                "age": "Age:",
                "payment_frequency": "Payment Frequency:",
                "monthly": "Monthly",
                "quarterly": "Quarterly",
                "semesterly": "Semesterly",
                "yearly": "Yearly",
                "calculate_premium": "Calculate Premium",
                "premium_details": "Premium Details",
                "estimated_premium": "Estimated Premium:",
                "plan_features": "Plan Features:"
            },
            "Indonesia": {
                # Main window
                "title": "Sistem Manajemen Rumah Sakit",
                "status_ready": "Siap",
                "welcome": "Selamat datang di Sistem Manajemen Rumah Sakit",
                
                # Menu items
                "menu_file": "File",
                "menu_modules": "Modul",
                "menu_patient": "Pendaftaran Pasien",
                "menu_medical": "Rekam Medis",
                "menu_doctor": "Manajemen Dokter",
                "menu_billing": "Pembayaran",
                "menu_report": "Laporan",
                "menu_lang": "Bahasa",
                "menu_exit": "Keluar",
                
                # Common buttons
                "button_save": "Simpan",
                "button_clear": "Bersihkan",
                "button_back": "Kembali",
                "button_register": "Daftar",
                "button_calculate": "Hitung",
                "button_generate": "Buat Laporan",
                "button_export": "Ekspor ke CSV",
                
                # Patient registration
                "patient_registration": "Pendaftaran Pasien",
                "full_name": "Nama Lengkap:",
                "dob": "Tanggal Lahir:",
                "gender": "Jenis Kelamin:",
                "male": "Laki-laki",
                "female": "Perempuan",
                "other": "Lainnya",
                "address": "Alamat:",
                "phone": "Telepon:",
                "email": "Email:",
                "id_type": "Jenis ID:",
                "id_number": "Nomor ID:",
                "insurance_type": "Jenis Asuransi:",
                "insurance_number": "Nomor Asuransi:",
                "registered_patients": "Pasien Terdaftar",
                "bpjs_number": "Nomor BPJS:",
                "faskes_level": "Level Faskes:",
                "referral_letter": "Surat Rujukan:",
                "policy_number": "Nomor Polis:",
                "member_since": "Anggota Sejak:",
                "plan_type": "Jenis Plan:",
                
                # Medical records
                "medical_records": "Rekam Medis",
                "patient": "Pasien:",
                "visit_date": "Tanggal Kunjungan:",
                "doctor": "Dokter:",
                "diagnosis": "Diagnosa:",
                "treatment": "Perawatan:",
                "notes": "Catatan:",
                "records_list": "Rekam Medis",
                
                # Doctor management
                "doctor_management": "Manajemen Dokter",
                "name": "Nama:",
                "specialization": "Spesialisasi:",
                "schedule": "Jadwal:",
                "doctors_list": "Daftar Dokter",
                
                # Billing
                "billing": "Pembayaran",
                "medical_visit": "Kunjungan Medis:",
                "total_amount": "Total Pembayaran (IDR):",
                "insurance_coverage": "Cover Asuransi (IDR):",
                "patient_payment": "Pembayaran Pasien (IDR):",
                "payment_status": "Status Pembayaran:",
                "pending": "Menunggu",
                "paid": "Lunas",
                "insurance_claim": "Klaim Asuransi",
                "payment_method": "Metode Pembayaran:",
                "cash": "Tunai",
                "credit_card": "Kartu Kredit",
                "debit_card": "Kartu Debit",
                "bank_transfer": "Transfer Bank",
                "payment_date": "Tanggal Pembayaran:",
                "billing_records": "Catatan Pembayaran",
                
                # Reports
                "reports": "Laporan",
                "select_report": "Pilih Jenis Laporan:",
                "start_date": "Tanggal Mulai:",
                "end_date": "Tanggal Akhir:",
                "report_types": ["Daftar Pasien", "Daftar Dokter", "Kunjungan Medis", "Ringkasan Pembayaran", "Klaim Asuransi"],
                
                # Messages
                "error": "Error",
                "success": "Sukses",
                "database_error": "Error Database",
                "required_fields": "Harap isi semua bidang yang diperlukan",
                "invalid_numbers": "Harap masukkan angka yang valid",
                "invalid_date": "Harap masukkan tanggal dalam format YYYY-MM-DD",
                "patient_registered": "Pasien berhasil didaftarkan",
                "record_saved": "Rekam medis berhasil disimpan",
                "doctor_saved": "Informasi dokter berhasil disimpan",
                "billing_saved": "Catatan pembayaran berhasil disimpan",
                "report_exported": "Laporan berhasil diekspor",
                "no_report": "Tidak ada laporan untuk diekspor",
                
                # Insurance calculators
                "bpjs_calculator": "Kalkulator Iuran BPJS Kesehatan",
                "salary": "Gaji Bulanan (IDR):",
                "family_members": "Jumlah Anggota Keluarga:",
                "calculate_contribution": "Hitung Iuran",
                "allianz_calculator": "Kalkulator Premi Allianz",
                "prudential_calculator": "Kalkulator Premi Prudential",
                "age": "Usia:",
                "payment_frequency": "Frekuensi Pembayaran:",
                "monthly": "Bulanan",
                "quarterly": "Triwulan",
                "semesterly": "Semester",
                "yearly": "Tahunan",
                "calculate_premium": "Hitung Premi",
                "premium_details": "Detail Premi",
                "estimated_premium": "Perkiraan Premi:",
                "plan_features": "Fitur Plan:"
            }
        }
        
        # Initialize UI
        self.root.title(self._tr("title"))
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Set theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Database setup
        self.setup_database()
        
        # Create UI
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        
        # Show welcome screen
        self.show_welcome()
    
    def _tr(self, key):
        """Helper method to get translated text"""
        return self.languages[self.current_lang].get(key, key)
    
    def setup_database(self):
        self.conn = sqlite3.connect('hms.db')
        self.cursor = self.conn.cursor()
        
        # Create tables if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            dob TEXT,
                            gender TEXT,
                            address TEXT,
                            phone TEXT,
                            email TEXT,
                            id_type TEXT,
                            id_number TEXT,
                            insurance_type TEXT,
                            insurance_number TEXT,
                            registration_date TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS medical_records (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_id INTEGER,
                            visit_date TEXT,
                            doctor_id INTEGER,
                            diagnosis TEXT,
                            treatment TEXT,
                            notes TEXT,
                            FOREIGN KEY(patient_id) REFERENCES patients(id),
                            FOREIGN KEY(doctor_id) REFERENCES doctors(id))''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            specialization TEXT,
                            phone TEXT,
                            email TEXT,
                            schedule TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS billing (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            patient_id INTEGER,
                            visit_id INTEGER,
                            amount REAL,
                            insurance_amount REAL,
                            patient_amount REAL,
                            payment_status TEXT,
                            payment_date TEXT,
                            payment_method TEXT,
                            FOREIGN KEY(patient_id) REFERENCES patients(id),
                            FOREIGN KEY(visit_id) REFERENCES medical_records(id))''')
        
        self.conn.commit()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label=self._tr("menu_exit"), command=self.root.quit)
        menubar.add_cascade(label=self._tr("menu_file"), menu=file_menu)
        
        # Modules menu
        modules_menu = tk.Menu(menubar, tearoff=0)
        modules_menu.add_command(label=self._tr("menu_patient"), command=self.show_patient_registration)
        modules_menu.add_command(label=self._tr("menu_medical"), command=self.show_medical_records)
        modules_menu.add_command(label=self._tr("menu_doctor"), command=self.show_doctor_management)
        modules_menu.add_command(label=self._tr("menu_billing"), command=self.show_billing)
        modules_menu.add_command(label=self._tr("menu_report"), command=self.show_reports)
        menubar.add_cascade(label=self._tr("menu_modules"), menu=modules_menu)
        
        # Language menu
        lang_menu = tk.Menu(menubar, tearoff=0)
        for lang in self.languages:
            lang_menu.add_command(label=lang, command=lambda l=lang: self.change_language(l))
        menubar.add_cascade(label=self._tr("menu_lang"), menu=lang_menu)
        
        self.root.config(menu=menubar)
    
    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set(self._tr("status_ready"))
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def change_language(self, lang):
        self.current_lang = lang
        self.root.title(self._tr("title"))
        self.status_var.set(self._tr("status_ready"))
        self.create_menu()  # Refresh menu with new language
        
        # Refresh current page
        if hasattr(self, 'current_page'):
            self.current_page()
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_welcome(self):
        self.current_page = self.show_welcome
        self.clear_main_frame()
        
        welcome_label = ttk.Label(self.main_frame, 
                                text=self._tr("welcome"), 
                                font=('Helvetica', 18, 'bold'))
        welcome_label.pack(pady=50)
        
        # Add hospital logo (placeholder)
        try:
            img = Image.open("hospital_logo.png")
            img = img.resize((200, 200), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(img)
            logo_label = ttk.Label(self.main_frame, image=self.logo)
            logo_label.pack(pady=20)
        except:
            pass
        
        # Quick access buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text=self._tr("menu_patient"), 
                  command=self.show_patient_registration).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text=self._tr("menu_medical"), 
                  command=self.show_medical_records).grid(row=0, column=1, padx=10)
        ttk.Button(btn_frame, text=self._tr("menu_doctor"), 
                  command=self.show_doctor_management).grid(row=0, column=2, padx=10)
        ttk.Button(btn_frame, text=self._tr("menu_billing"), 
                  command=self.show_billing).grid(row=0, column=3, padx=10)
    
    def show_patient_registration(self):
        self.current_page = self.show_patient_registration
        self.clear_main_frame()
        
        # Patient Registration Form
        form_frame = ttk.LabelFrame(self.main_frame, text=self._tr("patient_registration"))
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Form fields
        ttk.Label(form_frame, text=self._tr("full_name")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_name = ttk.Entry(form_frame, width=40)
        self.p_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("dob")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_dob = ttk.Entry(form_frame, width=40)
        self.p_dob.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("gender")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_gender = ttk.Combobox(form_frame, values=[
            self._tr("male"),
            self._tr("female"),
            self._tr("other")
        ], width=37)
        self.p_gender.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("address")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_address = tk.Text(form_frame, width=30, height=3)
        self.p_address.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("phone")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_phone = ttk.Entry(form_frame, width=40)
        self.p_phone.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("email")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_email = ttk.Entry(form_frame, width=40)
        self.p_email.grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("id_type")).grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_id_type = ttk.Combobox(form_frame, values=["KTP", "Passport", "Driver License"], width=37)
        self.p_id_type.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("id_number")).grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_id_number = ttk.Entry(form_frame, width=40)
        self.p_id_number.grid(row=7, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("insurance_type")).grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.p_insurance_type = ttk.Combobox(form_frame, 
                                           values=["None", "BPJS Kesehatan", "Allianz", "Prudential", self._tr("other")], 
                                           width=37)
        self.p_insurance_type.grid(row=8, column=1, padx=5, pady=5)
        self.p_insurance_type.bind("<<ComboboxSelected>>", self.show_insurance_fields)
        
        # Insurance specific fields (initially hidden)
        self.insurance_frame = ttk.Frame(form_frame)
        self.insurance_frame.grid(row=9, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self._tr("button_register"), command=self.register_patient).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_clear"), command=self.clear_patient_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_back"), command=self.show_welcome).pack(side=tk.LEFT, padx=5)
        
        # Patient list
        list_frame = ttk.LabelFrame(self.main_frame, text=self._tr("registered_patients"))
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "name", "dob", "gender", "insurance")
        self.patient_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        self.patient_tree.heading("id", text="ID")
        self.patient_tree.heading("name", text=self._tr("name"))
        self.patient_tree.heading("dob", text=self._tr("dob"))
        self.patient_tree.heading("gender", text=self._tr("gender"))
        self.patient_tree.heading("insurance", text=self._tr("insurance_type"))
        
        self.patient_tree.column("id", width=50)
        self.patient_tree.column("name", width=150)
        self.patient_tree.column("dob", width=100)
        self.patient_tree.column("gender", width=80)
        self.patient_tree.column("insurance", width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.patient_tree.yview)
        self.patient_tree.configure(yscroll=scrollbar.set)
        
        self.patient_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.patient_tree.bind("<Double-1>", self.load_patient_data)
        
        self.load_patient_list()
    
    def show_insurance_fields(self, event=None):
        # Clear insurance frame
        for widget in self.insurance_frame.winfo_children():
            widget.destroy()
        
        insurance_type = self.p_insurance_type.get()
        
        if insurance_type == "BPJS Kesehatan":
            ttk.Label(self.insurance_frame, text=self._tr("bpjs_number")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            self.p_insurance_number = ttk.Entry(self.insurance_frame, width=30)
            self.p_insurance_number.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.insurance_frame, text=self._tr("faskes_level")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
            self.p_faskes_level = ttk.Combobox(self.insurance_frame, 
                                             values=["Faskes 1", "Faskes 2", "Faskes 3"], 
                                             width=27)
            self.p_faskes_level.grid(row=1, column=1, padx=5, pady=2)
            
            ttk.Label(self.insurance_frame, text=self._tr("referral_letter")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
            self.p_referral = ttk.Entry(self.insurance_frame, width=30)
            self.p_referral.grid(row=2, column=1, padx=5, pady=2)
            
            ttk.Button(self.insurance_frame, text=self._tr("calculate_contribution"), 
                      command=self.calculate_bpjs_contribution).grid(row=3, column=0, columnspan=2, pady=5)
            
        elif insurance_type in ["Allianz", "Prudential"]:
            ttk.Label(self.insurance_frame, text=self._tr("policy_number")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            self.p_insurance_number = ttk.Entry(self.insurance_frame, width=30)
            self.p_insurance_number.grid(row=0, column=1, padx=5, pady=2)
            
            ttk.Label(self.insurance_frame, text=self._tr("member_since")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
            self.p_member_since = ttk.Entry(self.insurance_frame, width=30)
            self.p_member_since.grid(row=1, column=1, padx=5, pady=2)
            
            if insurance_type == "Allianz":
                ttk.Label(self.insurance_frame, text=self._tr("plan_type")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
                self.p_plan_type = ttk.Combobox(self.insurance_frame, 
                                              values=["SmartHealth Maxi Violet", "Life Secure PASTI", "LegacyPro"], 
                                              width=27)
                self.p_plan_type.grid(row=2, column=1, padx=5, pady=2)
                
                ttk.Button(self.insurance_frame, text=self._tr("calculate_premium"), 
                          command=self.calculate_allianz_coverage).grid(row=3, column=0, columnspan=2, pady=5)
            
            elif insurance_type == "Prudential":
                ttk.Label(self.insurance_frame, text=self._tr("plan_type")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
                self.p_plan_type = ttk.Combobox(self.insurance_frame, 
                                              values=["PRUSolusi Sehat", "PRUPrime Healthcare", "PRUCritical Benefit"], 
                                              width=27)
                self.p_plan_type.grid(row=2, column=1, padx=5, pady=2)
                
                ttk.Button(self.insurance_frame, text=self._tr("calculate_premium"), 
                          command=self.calculate_prudential_coverage).grid(row=3, column=0, columnspan=2, pady=5)
    
    def calculate_bpjs_contribution(self):
        # Create a new window for BPJS calculation
        bpjs_window = tk.Toplevel(self.root)
        bpjs_window.title(self._tr("bpjs_calculator"))
        bpjs_window.geometry("500x400")
        
        ttk.Label(bpjs_window, text=self._tr("bpjs_calculator"), font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Input fields
        input_frame = ttk.Frame(bpjs_window)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text=self._tr("salary")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.salary_entry = ttk.Entry(input_frame, width=20)
        self.salary_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text=self._tr("family_members")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.family_members = ttk.Spinbox(input_frame, from_=1, to=20, width=18)
        self.family_members.grid(row=1, column=1, padx=5, pady=5)
        self.family_members.set(1)
        
        # Calculate button
        ttk.Button(bpjs_window, text=self._tr("calculate_contribution"), command=self.calculate_bpjs).pack(pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(bpjs_window, text=self._tr("premium_details"))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.bpjs_result = tk.Text(result_frame, height=10, width=60)
        self.bpjs_result.pack(padx=5, pady=5)
        self.bpjs_result.insert(tk.END, self._tr("premium_details") + "...")
        self.bpjs_result.config(state=tk.DISABLED)
    
    def calculate_bpjs(self):
        try:
            salary = float(self.salary_entry.get())
            family_members = int(self.family_members.get())
            
            # BPJS calculation logic
            max_salary = 12000000  # Maximum salary for BPJS calculation
            min_salary = 2000000   # Example minimum salary (UMK)
            
            if salary < min_salary:
                salary = min_salary
            elif salary > max_salary:
                salary = max_salary
            
            # Base contribution (for up to 5 family members)
            total_contribution = 0.05 * salary
            company_share = 0.04 * salary
            employee_share = 0.01 * salary
            
            # Additional members (beyond 5)
            additional_members = max(0, family_members - 5)
            additional_contribution = additional_members * (0.01 * salary)
            
            # Update result text
            self.bpjs_result.config(state=tk.NORMAL)
            self.bpjs_result.delete(1.0, tk.END)
            
            self.bpjs_result.insert(tk.END, f"{self._tr('bpjs_calculator')}:\n\n")
            self.bpjs_result.insert(tk.END, f"{self._tr('salary')}: IDR {salary:,.2f}\n")
            self.bpjs_result.insert(tk.END, f"{self._tr('family_members')}: {family_members}\n\n")
            
            self.bpjs_result.insert(tk.END, f"Base Contribution (5% of salary): IDR {total_contribution:,.2f}\n")
            self.bpjs_result.insert(tk.END, f"  - Company Share (4%): IDR {company_share:,.2f}\n")
            self.bpjs_result.insert(tk.END, f"  - Employee Share (1%): IDR {employee_share:,.2f}\n")
            
            if additional_members > 0:
                self.bpjs_result.insert(tk.END, f"\nAdditional Members ({additional_members}): IDR {additional_contribution:,.2f}\n")
                self.bpjs_result.insert(tk.END, f"\nTotal Contribution: IDR {total_contribution + additional_contribution:,.2f}\n")
            
            self.bpjs_result.config(state=tk.DISABLED)
            
        except ValueError:
            messagebox.showerror(self._tr("error"), self._tr("invalid_numbers"))
    
    def calculate_allianz_coverage(self):
        # Create a new window for Allianz calculation
        allianz_window = tk.Toplevel(self.root)
        allianz_window.title(self._tr("allianz_calculator"))
        allianz_window.geometry("500x400")
        
        ttk.Label(allianz_window, text=self._tr("allianz_calculator"), font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Plan selection
        plan_frame = ttk.Frame(allianz_window)
        plan_frame.pack(pady=10)
        
        ttk.Label(plan_frame, text=self._tr("plan_type")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.allianz_plan = ttk.Combobox(plan_frame, 
                                       values=["SmartHealth Maxi Violet", "Life Secure PASTI", "LegacyPro"], 
                                       width=25)
        self.allianz_plan.grid(row=0, column=1, padx=5, pady=5)
        
        # Payment frequency
        ttk.Label(plan_frame, text=self._tr("payment_frequency")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.allianz_frequency = ttk.Combobox(plan_frame, 
                                            values=[
                                                self._tr("monthly"),
                                                self._tr("quarterly"),
                                                self._tr("semesterly"),
                                                self._tr("yearly")
                                            ], 
                                            width=25)
        self.allianz_frequency.grid(row=1, column=1, padx=5, pady=5)
        self.allianz_frequency.set(self._tr("monthly"))
        
        # Calculate button
        ttk.Button(allianz_window, text=self._tr("calculate_premium"), command=self.calculate_allianz).pack(pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(allianz_window, text=self._tr("premium_details"))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.allianz_result = tk.Text(result_frame, height=10, width=60)
        self.allianz_result.pack(padx=5, pady=5)
        self.allianz_result.insert(tk.END, self._tr("premium_details") + "...")
        self.allianz_result.config(state=tk.DISABLED)
    
    def calculate_allianz(self):
        plan = self.allianz_plan.get()
        frequency = self.allianz_frequency.get()
        
        if not plan:
            messagebox.showerror(self._tr("error"), f"{self._tr('required_fields')}")
            return
        
        # Sample premium data (in reality, this would come from a database or API)
        plan_data = {
            "SmartHealth Maxi Violet": {
                "monthly": 500000,
                "quarterly": 1350000,
                "semesterly": 2500000,
                "yearly": 4500000
            },
            "Life Secure PASTI": {
                "monthly": 300000,
                "quarterly": 810000,
                "semesterly": 1560000,
                "yearly": 3000000
            },
            "LegacyPro": {
                "monthly": 750000,
                "quarterly": 2100000,
                "semesterly": 4000000,
                "yearly": 7500000
            }
        }
        
        if plan not in plan_data:
            messagebox.showerror(self._tr("error"), "Invalid plan selected")
            return
        
        # Get frequency key (reverse translation)
        freq_map = {
            self._tr("monthly"): "monthly",
            self._tr("quarterly"): "quarterly",
            self._tr("semesterly"): "semesterly",
            self._tr("yearly"): "yearly"
        }
        freq_key = freq_map.get(frequency, "monthly")
        
        premium = plan_data[plan].get(freq_key, 0)
        
        # Update result text
        self.allianz_result.config(state=tk.NORMAL)
        self.allianz_result.delete(1.0, tk.END)
        
        self.allianz_result.insert(tk.END, f"{self._tr('allianz_calculator')}:\n\n")
        self.allianz_result.insert(tk.END, f"{self._tr('plan_type')}: {plan}\n")
        self.allianz_result.insert(tk.END, f"{self._tr('payment_frequency')}: {frequency}\n\n")
        self.allianz_result.insert(tk.END, f"{self._tr('estimated_premium')}: IDR {premium:,.2f}\n\n")
        
        # Add plan features
        if plan == "SmartHealth Maxi Violet":
            self.allianz_result.insert(tk.END, f"{self._tr('plan_features')}:\n")
            self.allianz_result.insert(tk.END, "- No claims bonus (20% return if no claims)\n")
            self.allianz_result.insert(tk.END, "- Comprehensive hospitalization coverage\n")
            self.allianz_result.insert(tk.END, "- Worldwide emergency coverage\n")
        elif plan == "Life Secure PASTI":
            self.allianz_result.insert(tk.END, f"{self._tr('plan_features')}:\n")
            self.allianz_result.insert(tk.END, "- Basic hospitalization coverage\n")
            self.allianz_result.insert(tk.END, "- Critical illness protection\n")
            self.allianz_result.insert(tk.END, "- Affordable premiums\n")
        elif plan == "LegacyPro":
            self.allianz_result.insert(tk.END, f"{self._tr('plan_features')}:\n")
            self.allianz_result.insert(tk.END, "- High coverage limits\n")
            self.allianz_result.insert(tk.END, "- Long-term protection\n")
            self.allianz_result.insert(tk.END, "- Investment component\n")
        
        self.allianz_result.config(state=tk.DISABLED)
    
    def calculate_prudential_coverage(self):
        # Create a new window for Prudential calculation
        prudential_window = tk.Toplevel(self.root)
        prudential_window.title(self._tr("prudential_calculator"))
        prudential_window.geometry("500x400")
        
        ttk.Label(prudential_window, text=self._tr("prudential_calculator"), font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        # Plan selection
        plan_frame = ttk.Frame(prudential_window)
        plan_frame.pack(pady=10)
        
        ttk.Label(plan_frame, text=self._tr("plan_type")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.prudential_plan = ttk.Combobox(plan_frame, 
                                          values=["PRUSolusi Sehat", "PRUPrime Healthcare", "PRUCritical Benefit"], 
                                          width=25)
        self.prudential_plan.grid(row=0, column=1, padx=5, pady=5)
        
        # Age input
        ttk.Label(plan_frame, text=self._tr("age")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.prudential_age = ttk.Spinbox(plan_frame, from_=1, to=70, width=28)
        self.prudential_age.grid(row=1, column=1, padx=5, pady=5)
        self.prudential_age.set(30)
        
        # Calculate button
        ttk.Button(prudential_window, text=self._tr("calculate_premium"), command=self.calculate_prudential).pack(pady=10)
        
        # Result frame
        result_frame = ttk.LabelFrame(prudential_window, text=self._tr("premium_details"))
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.prudential_result = tk.Text(result_frame, height=10, width=60)
        self.prudential_result.pack(padx=5, pady=5)
        self.prudential_result.insert(tk.END, self._tr("premium_details") + "...")
        self.prudential_result.config(state=tk.DISABLED)
    
    def calculate_prudential(self):
        plan = self.prudential_plan.get()
        age = int(self.prudential_age.get())
        
        if not plan:
            messagebox.showerror(self._tr("error"), f"{self._tr('required_fields')}")
            return
        
        # Sample premium data based on age and plan (simplified)
        base_premiums = {
            "PRUSolusi Sehat": 270000,
            "PRUPrime Healthcare": 500000,
            "PRUCritical Benefit": 750000
        }
        
        # Age adjustment factor (in reality, this would be more complex)
        if age < 18:
            age_factor = 0.8
        elif age <= 30:
            age_factor = 1.0
        elif age <= 40:
            age_factor = 1.2
        elif age <= 50:
            age_factor = 1.5
        else:
            age_factor = 2.0
        
        base_premium = base_premiums.get(plan, 0)
        estimated_premium = base_premium * age_factor
        
        # Update result text
        self.prudential_result.config(state=tk.NORMAL)
        self.prudential_result.delete(1.0, tk.END)
        
        self.prudential_result.insert(tk.END, f"{self._tr('prudential_calculator')}:\n\n")
        self.prudential_result.insert(tk.END, f"{self._tr('plan_type')}: {plan}\n")
        self.prudential_result.insert(tk.END, f"{self._tr('age')}: {age}\n\n")
        self.prudential_result.insert(tk.END, f"{self._tr('estimated_premium')}: IDR {estimated_premium:,.2f}\n\n")
        
        # Add plan features
        if plan == "PRUSolusi Sehat":
            self.prudential_result.insert(tk.END, f"{self._tr('plan_features')}:\n")
            self.prudential_result.insert(tk.END, "- Basic hospitalization coverage\n")
            self.prudential_result.insert(tk.END, "- Affordable premiums\n")
            self.prudential_result.insert(tk.END, "- Covers ages 1 month to 70 years\n")
        elif plan == "PRUPrime Healthcare":
            self.prudential_result.insert(tk.END, f"{self._tr('plan_features')}:\n")
            self.prudential_result.insert(tk.END, "- Comprehensive medical coverage\n")
            self.prudential_result.insert(tk.END, "- Private hospital rooms\n")
            self.prudential_result.insert(tk.END, "- Specialist doctor coverage\n")
        elif plan == "PRUCritical Benefit":
            self.prudential_result.insert(tk.END, f"{self._tr('plan_features')}:\n")
            self.prudential_result.insert(tk.END, "- Critical illness protection\n")
            self.prudential_result.insert(tk.END, "- Lump sum payment for diagnosis\n")
            self.prudential_result.insert(tk.END, "- Additional hospital benefits\n")
        
        self.prudential_result.config(state=tk.DISABLED)
    
    def register_patient(self):
        # Get form data
        name = self.p_name.get()
        dob = self.p_dob.get()
        gender = self.p_gender.get()
        address = self.p_address.get("1.0", tk.END).strip()
        phone = self.p_phone.get()
        email = self.p_email.get()
        id_type = self.p_id_type.get()
        id_number = self.p_id_number.get()
        insurance_type = self.p_insurance_type.get()
        insurance_number = self.p_insurance_number.get() if hasattr(self, 'p_insurance_number') else ""
        
        # Validate required fields
        if not name or not dob or not gender or not phone:
            messagebox.showerror(self._tr("error"), self._tr("required_fields"))
            return
        
        # Insert into database
        registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            self.cursor.execute('''INSERT INTO patients 
                              (name, dob, gender, address, phone, email, id_type, id_number, 
                              insurance_type, insurance_number, registration_date)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (name, dob, gender, address, phone, email, id_type, id_number, 
                               insurance_type, insurance_number, registration_date))
            self.conn.commit()
            
            messagebox.showinfo(self._tr("success"), self._tr("patient_registered"))
            self.clear_patient_form()
            self.load_patient_list()
            
        except sqlite3.Error as e:
            messagebox.showerror(self._tr("database_error"), f"Failed to register patient: {e}")
    
    def clear_patient_form(self):
        self.p_name.delete(0, tk.END)
        self.p_dob.delete(0, tk.END)
        self.p_gender.set('')
        self.p_address.delete("1.0", tk.END)
        self.p_phone.delete(0, tk.END)
        self.p_email.delete(0, tk.END)
        self.p_id_type.set('')
        self.p_id_number.delete(0, tk.END)
        self.p_insurance_type.set('None')
        
        # Clear insurance specific fields
        for widget in self.insurance_frame.winfo_children():
            widget.destroy()
    
    def load_patient_list(self):
        # Clear current list
        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)
        
        # Fetch patients from database
        self.cursor.execute("SELECT id, name, dob, gender, insurance_type FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        
        # Add to treeview
        for patient in patients:
            self.patient_tree.insert('', tk.END, values=patient)
    
    def load_patient_data(self, event):
        # Get selected item
        selected_item = self.patient_tree.focus()
        if not selected_item:
            return
        
        # Get patient ID
        patient_id = self.patient_tree.item(selected_item)['values'][0]
        
        # Fetch patient data
        self.cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        patient = self.cursor.fetchone()
        
        if not patient:
            return
        
        # Fill form with patient data
        self.clear_patient_form()
        
        self.p_name.insert(0, patient[1])
        self.p_dob.insert(0, patient[2])
        self.p_gender.set(patient[3])
        self.p_address.insert("1.0", patient[4])
        self.p_phone.insert(0, patient[5])
        self.p_email.insert(0, patient[6])
        self.p_id_type.set(patient[7])
        self.p_id_number.insert(0, patient[8])
        self.p_insurance_type.set(patient[9])
        
        # Show insurance fields if applicable
        if patient[9] and patient[9] != "None":
            self.show_insurance_fields()
            if hasattr(self, 'p_insurance_number'):
                self.p_insurance_number.insert(0, patient[10])
    
    def show_medical_records(self):
        self.current_page = self.show_medical_records
        self.clear_main_frame()
        
        # Medical Records Form
        form_frame = ttk.LabelFrame(self.main_frame, text=self._tr("medical_records"))
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Patient selection
        ttk.Label(form_frame, text=self._tr("patient")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.mr_patient = ttk.Combobox(form_frame, width=40)
        self.mr_patient.grid(row=0, column=1, padx=5, pady=5)
        
        # Load patient names
        self.cursor.execute("SELECT id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        self.patient_dict = {f"{p[1]} (ID: {p[0]})": p[0] for p in patients}
        self.mr_patient['values'] = list(self.patient_dict.keys())
        
        # Visit date
        ttk.Label(form_frame, text=self._tr("visit_date")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.mr_visit_date = ttk.Entry(form_frame, width=40)
        self.mr_visit_date.grid(row=1, column=1, padx=5, pady=5)
        self.mr_visit_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        # Doctor selection
        ttk.Label(form_frame, text=self._tr("doctor")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.mr_doctor = ttk.Combobox(form_frame, width=40)
        self.mr_doctor.grid(row=2, column=1, padx=5, pady=5)
        
        # Load doctor names
        self.cursor.execute("SELECT id, name, specialization FROM doctors ORDER BY name")
        doctors = self.cursor.fetchall()
        self.doctor_dict = {f"{d[1]} ({d[2]}) (ID: {d[0]})": d[0] for d in doctors}
        self.mr_doctor['values'] = list(self.doctor_dict.keys())
        
        # Diagnosis
        ttk.Label(form_frame, text=self._tr("diagnosis")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.mr_diagnosis = tk.Text(form_frame, width=30, height=3)
        self.mr_diagnosis.grid(row=3, column=1, padx=5, pady=5)
        
        # Treatment
        ttk.Label(form_frame, text=self._tr("treatment")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.mr_treatment = tk.Text(form_frame, width=30, height=3)
        self.mr_treatment.grid(row=4, column=1, padx=5, pady=5)
        
        # Notes
        ttk.Label(form_frame, text=self._tr("notes")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.mr_notes = tk.Text(form_frame, width=30, height=3)
        self.mr_notes.grid(row=5, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self._tr("button_save"), command=self.save_medical_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_clear"), command=self.clear_medical_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_back"), command=self.show_welcome).pack(side=tk.LEFT, padx=5)
        
        # Medical records list
        list_frame = ttk.LabelFrame(self.main_frame, text=self._tr("records_list"))
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "patient", "visit_date", "doctor", "diagnosis")
        self.medical_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        self.medical_tree.heading("id", text="ID")
        self.medical_tree.heading("patient", text=self._tr("patient"))
        self.medical_tree.heading("visit_date", text=self._tr("visit_date"))
        self.medical_tree.heading("doctor", text=self._tr("doctor"))
        self.medical_tree.heading("diagnosis", text=self._tr("diagnosis"))
        
        self.medical_tree.column("id", width=50)
        self.medical_tree.column("patient", width=150)
        self.medical_tree.column("visit_date", width=100)
        self.medical_tree.column("doctor", width=150)
        self.medical_tree.column("diagnosis", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.medical_tree.yview)
        self.medical_tree.configure(yscroll=scrollbar.set)
        
        self.medical_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.medical_tree.bind("<Double-1>", self.load_medical_data)
        
        self.load_medical_list()
    
    def save_medical_record(self):
        # Get form data
        patient_key = self.mr_patient.get()
        patient_id = self.patient_dict.get(patient_key)
        visit_date = self.mr_visit_date.get()
        doctor_key = self.mr_doctor.get()
        doctor_id = self.doctor_dict.get(doctor_key)
        diagnosis = self.mr_diagnosis.get("1.0", tk.END).strip()
        treatment = self.mr_treatment.get("1.0", tk.END).strip()
        notes = self.mr_notes.get("1.0", tk.END).strip()
        
        # Validate required fields
        if not patient_id or not visit_date or not doctor_id or not diagnosis:
            messagebox.showerror(self._tr("error"), self._tr("required_fields"))
            return
        
        # Insert into database
        try:
            self.cursor.execute('''INSERT INTO medical_records 
                              (patient_id, visit_date, doctor_id, diagnosis, treatment, notes)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                              (patient_id, visit_date, doctor_id, diagnosis, treatment, notes))
            self.conn.commit()
            
            messagebox.showinfo(self._tr("success"), self._tr("record_saved"))
            self.clear_medical_form()
            self.load_medical_list()
            
        except sqlite3.Error as e:
            messagebox.showerror(self._tr("database_error"), f"Failed to save medical record: {e}")
    
    def clear_medical_form(self):
        self.mr_patient.set('')
        self.mr_visit_date.delete(0, tk.END)
        self.mr_visit_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.mr_doctor.set('')
        self.mr_diagnosis.delete("1.0", tk.END)
        self.mr_treatment.delete("1.0", tk.END)
        self.mr_notes.delete("1.0", tk.END)
    
    def load_medical_list(self):
        # Clear current list
        for item in self.medical_tree.get_children():
            self.medical_tree.delete(item)
        
        # Fetch medical records from database with patient and doctor names
        self.cursor.execute('''SELECT mr.id, p.name, mr.visit_date, d.name, mr.diagnosis
                           FROM medical_records mr
                           JOIN patients p ON mr.patient_id = p.id
                           JOIN doctors d ON mr.doctor_id = d.id
                           ORDER BY mr.visit_date DESC''')
        records = self.cursor.fetchall()
        
        # Add to treeview
        for record in records:
            self.medical_tree.insert('', tk.END, values=record)
    
    def load_medical_data(self, event):
        # Get selected item
        selected_item = self.medical_tree.focus()
        if not selected_item:
            return
        
        # Get record ID
        record_id = self.medical_tree.item(selected_item)['values'][0]
        
        # Fetch record data
        self.cursor.execute('''SELECT mr.*, p.name, d.name
                           FROM medical_records mr
                           JOIN patients p ON mr.patient_id = p.id
                           JOIN doctors d ON mr.doctor_id = d.id
                           WHERE mr.id=?''', (record_id,))
        record = self.cursor.fetchone()
        
        if not record:
            return
        
        # Fill form with record data
        self.clear_medical_form()
        
        # Find patient key
        patient_name = record[8]  # p.name
        patient_id = record[1]    # mr.patient_id
        patient_key = f"{patient_name} (ID: {patient_id})"
        
        # Find doctor key
        doctor_name = record[9]   # d.name
        doctor_id = record[3]     # mr.doctor_id
        doctor_specialization = ""
        
        # Get doctor specialization
        self.cursor.execute("SELECT specialization FROM doctors WHERE id=?", (doctor_id,))
        doctor_data = self.cursor.fetchone()
        if doctor_data:
            doctor_specialization = doctor_data[0]
        
        doctor_key = f"{doctor_name} ({doctor_specialization}) (ID: {doctor_id})"
        
        self.mr_patient.set(patient_key)
        self.mr_visit_date.delete(0, tk.END)
        self.mr_visit_date.insert(0, record[2])
        self.mr_doctor.set(doctor_key)
        self.mr_diagnosis.insert("1.0", record[4])
        self.mr_treatment.insert("1.0", record[5])
        self.mr_notes.insert("1.0", record[6])
    
    def show_doctor_management(self):
        self.current_page = self.show_doctor_management
        self.clear_main_frame()
        
        # Doctor Management Form
        form_frame = ttk.LabelFrame(self.main_frame, text=self._tr("doctor_management"))
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Form fields
        ttk.Label(form_frame, text=self._tr("name")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.d_name = ttk.Entry(form_frame, width=40)
        self.d_name.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("specialization")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.d_specialization = ttk.Entry(form_frame, width=40)
        self.d_specialization.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("phone")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.d_phone = ttk.Entry(form_frame, width=40)
        self.d_phone.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("email")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.d_email = ttk.Entry(form_frame, width=40)
        self.d_email.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text=self._tr("schedule")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.d_schedule = tk.Text(form_frame, width=30, height=3)
        self.d_schedule.grid(row=4, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self._tr("button_save"), command=self.save_doctor).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_clear"), command=self.clear_doctor_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_back"), command=self.show_welcome).pack(side=tk.LEFT, padx=5)
        
        # Doctor list
        list_frame = ttk.LabelFrame(self.main_frame, text=self._tr("doctors_list"))
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "name", "specialization", "phone", "schedule")
        self.doctor_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        self.doctor_tree.heading("id", text="ID")
        self.doctor_tree.heading("name", text=self._tr("name"))
        self.doctor_tree.heading("specialization", text=self._tr("specialization"))
        self.doctor_tree.heading("phone", text=self._tr("phone"))
        self.doctor_tree.heading("schedule", text=self._tr("schedule"))
        
        self.doctor_tree.column("id", width=50)
        self.doctor_tree.column("name", width=150)
        self.doctor_tree.column("specialization", width=150)
        self.doctor_tree.column("phone", width=100)
        self.doctor_tree.column("schedule", width=200)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.doctor_tree.yview)
        self.doctor_tree.configure(yscroll=scrollbar.set)
        
        self.doctor_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.doctor_tree.bind("<Double-1>", self.load_doctor_data)
        
        self.load_doctor_list()
    
    def save_doctor(self):
        # Get form data
        name = self.d_name.get()
        specialization = self.d_specialization.get()
        phone = self.d_phone.get()
        email = self.d_email.get()
        schedule = self.d_schedule.get("1.0", tk.END).strip()
        
        # Validate required fields
        if not name or not specialization:
            messagebox.showerror(self._tr("error"), self._tr("required_fields"))
            return
        
        # Insert into database
        try:
            self.cursor.execute('''INSERT INTO doctors 
                              (name, specialization, phone, email, schedule)
                              VALUES (?, ?, ?, ?, ?)''',
                              (name, specialization, phone, email, schedule))
            self.conn.commit()
            
            messagebox.showinfo(self._tr("success"), self._tr("doctor_saved"))
            self.clear_doctor_form()
            self.load_doctor_list()
            
        except sqlite3.Error as e:
            messagebox.showerror(self._tr("database_error"), f"Failed to save doctor information: {e}")
    
    def clear_doctor_form(self):
        self.d_name.delete(0, tk.END)
        self.d_specialization.delete(0, tk.END)
        self.d_phone.delete(0, tk.END)
        self.d_email.delete(0, tk.END)
        self.d_schedule.delete("1.0", tk.END)
    
    def load_doctor_list(self):
        # Clear current list
        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)
        
        # Fetch doctors from database
        self.cursor.execute("SELECT id, name, specialization, phone, schedule FROM doctors ORDER BY name")
        doctors = self.cursor.fetchall()
        
        # Add to treeview
        for doctor in doctors:
            self.doctor_tree.insert('', tk.END, values=doctor)
    
    def load_doctor_data(self, event):
        # Get selected item
        selected_item = self.doctor_tree.focus()
        if not selected_item:
            return
        
        # Get doctor ID
        doctor_id = self.doctor_tree.item(selected_item)['values'][0]
        
        # Fetch doctor data
        self.cursor.execute("SELECT * FROM doctors WHERE id=?", (doctor_id,))
        doctor = self.cursor.fetchone()
        
        if not doctor:
            return
        
        # Fill form with doctor data
        self.clear_doctor_form()
        
        self.d_name.insert(0, doctor[1])
        self.d_specialization.insert(0, doctor[2])
        self.d_phone.insert(0, doctor[3])
        self.d_email.insert(0, doctor[4])
        self.d_schedule.insert("1.0", doctor[5])
    
    def show_billing(self):
        self.current_page = self.show_billing
        self.clear_main_frame()
        
        # Billing Form
        form_frame = ttk.LabelFrame(self.main_frame, text=self._tr("billing"))
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Patient selection
        ttk.Label(form_frame, text=self._tr("patient")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_patient = ttk.Combobox(form_frame, width=40)
        self.b_patient.grid(row=0, column=1, padx=5, pady=5)
        
        # Load patient names
        self.cursor.execute("SELECT id, name FROM patients ORDER BY name")
        patients = self.cursor.fetchall()
        self.b_patient_dict = {f"{p[1]} (ID: {p[0]})": p[0] for p in patients}
        self.b_patient['values'] = list(self.b_patient_dict.keys())
        self.b_patient.bind("<<ComboboxSelected>>", self.load_patient_visits)
        
        # Visit selection
        ttk.Label(form_frame, text=self._tr("medical_visit")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_visit = ttk.Combobox(form_frame, width=40)
        self.b_visit.grid(row=1, column=1, padx=5, pady=5)
        
        # Amount
        ttk.Label(form_frame, text=self._tr("total_amount")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_amount = ttk.Entry(form_frame, width=40)
        self.b_amount.grid(row=2, column=1, padx=5, pady=5)
        
        # Insurance coverage
        ttk.Label(form_frame, text=self._tr("insurance_coverage")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_insurance = ttk.Entry(form_frame, width=40)
        self.b_insurance.grid(row=3, column=1, padx=5, pady=5)
        self.b_insurance.insert(0, "0")
        
        # Patient payment
        ttk.Label(form_frame, text=self._tr("patient_payment")).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_patient_payment = ttk.Entry(form_frame, width=40)
        self.b_patient_payment.grid(row=4, column=1, padx=5, pady=5)
        
        # Payment status
        ttk.Label(form_frame, text=self._tr("payment_status")).grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_status = ttk.Combobox(form_frame, values=[
            self._tr("pending"),
            self._tr("paid"),
            self._tr("insurance_claim")
        ], width=37)
        self.b_status.grid(row=5, column=1, padx=5, pady=5)
        self.b_status.set(self._tr("pending"))
        
        # Payment method
        ttk.Label(form_frame, text=self._tr("payment_method")).grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_method = ttk.Combobox(form_frame, 
                                   values=[
                                       self._tr("cash"),
                                       self._tr("credit_card"),
                                       self._tr("debit_card"),
                                       "BPJS", 
                                       "Allianz", 
                                       "Prudential",
                                       self._tr("bank_transfer")
                                   ], 
                                   width=37)
        self.b_method.grid(row=6, column=1, padx=5, pady=5)
        
        # Payment date
        ttk.Label(form_frame, text=self._tr("payment_date")).grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        self.b_date = ttk.Entry(form_frame, width=40)
        self.b_date.grid(row=7, column=1, padx=5, pady=5)
        self.b_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self._tr("button_calculate"), command=self.calculate_payment).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_save"), command=self.save_billing).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_clear"), command=self.clear_billing_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_back"), command=self.show_welcome).pack(side=tk.LEFT, padx=5)
        
        # Billing list
        list_frame = ttk.LabelFrame(self.main_frame, text=self._tr("billing_records"))
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("id", "patient", "visit_date", "amount", "status", "method")
        self.billing_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        self.billing_tree.heading("id", text="ID")
        self.billing_tree.heading("patient", text=self._tr("patient"))
        self.billing_tree.heading("visit_date", text=self._tr("visit_date"))
        self.billing_tree.heading("amount", text=self._tr("total_amount"))
        self.billing_tree.heading("status", text=self._tr("payment_status"))
        self.billing_tree.heading("method", text=self._tr("payment_method"))
        
        self.billing_tree.column("id", width=50)
        self.billing_tree.column("patient", width=150)
        self.billing_tree.column("visit_date", width=100)
        self.billing_tree.column("amount", width=100)
        self.billing_tree.column("status", width=100)
        self.billing_tree.column("method", width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.billing_tree.yview)
        self.billing_tree.configure(yscroll=scrollbar.set)
        
        self.billing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.billing_tree.bind("<Double-1>", self.load_billing_data)
        
        self.load_billing_list()
    
    def load_patient_visits(self, event=None):
        # Get selected patient
        patient_key = self.b_patient.get()
        patient_id = self.b_patient_dict.get(patient_key)
        
        if not patient_id:
            return
        
        # Clear visit combobox
        self.b_visit.set('')
        self.b_visit['values'] = []
        
        # Fetch patient's medical visits
        self.cursor.execute('''SELECT mr.id, mr.visit_date, d.name, mr.diagnosis
                           FROM medical_records mr
                           JOIN doctors d ON mr.doctor_id = d.id
                           WHERE mr.patient_id=?
                           ORDER BY mr.visit_date DESC''', (patient_id,))
        visits = self.cursor.fetchall()
        
        # Create visit dictionary and set values
        self.visit_dict = {}
        visit_values = []
        
        for visit in visits:
            visit_id = visit[0]
            visit_date = visit[1]
            doctor_name = visit[2]
            diagnosis = visit[3]
            
            key = f"Visit on {visit_date} with {doctor_name} - {diagnosis[:30]}..."
            self.visit_dict[key] = visit_id
            visit_values.append(key)
        
        self.b_visit['values'] = visit_values
        
        # Get patient's insurance info
        self.cursor.execute("SELECT insurance_type, insurance_number FROM patients WHERE id=?", (patient_id,))
        patient_data = self.cursor.fetchone()
        
        if patient_data and patient_data[0] and patient_data[0] != "None":
            self.b_method.set(patient_data[0])
            self.b_status.set(self._tr("insurance_claim"))
    
    def calculate_payment(self):
        # Get amount and insurance coverage
        try:
            amount = float(self.b_amount.get())
            insurance_coverage = float(self.b_insurance.get())
            
            if insurance_coverage > amount:
                messagebox.showerror(self._tr("error"), "Insurance coverage cannot be greater than total amount")
                return
            
            patient_payment = amount - insurance_coverage
            self.b_patient_payment.delete(0, tk.END)
            self.b_patient_payment.insert(0, f"{patient_payment:,.2f}")
            
        except ValueError:
            messagebox.showerror(self._tr("error"), self._tr("invalid_numbers"))
    
    def save_billing(self):
        # Get form data
        patient_key = self.b_patient.get()
        patient_id = self.b_patient_dict.get(patient_key)
        visit_key = self.b_visit.get()
        visit_id = self.visit_dict.get(visit_key)
        amount = self.b_amount.get()
        insurance_amount = self.b_insurance.get()
        patient_amount = self.b_patient_payment.get()
        status = self.b_status.get()
        method = self.b_method.get()
        payment_date = self.b_date.get()
        
        # Validate required fields
        if not patient_id or not visit_id or not amount:
            messagebox.showerror(self._tr("error"), self._tr("required_fields"))
            return
        
        try:
            amount = float(amount)
            insurance_amount = float(insurance_amount) if insurance_amount else 0
            patient_amount = float(patient_amount) if patient_amount else amount - insurance_amount
        except ValueError:
            messagebox.showerror(self._tr("error"), self._tr("invalid_numbers"))
            return
        
        # Insert into database
        try:
            self.cursor.execute('''INSERT INTO billing 
                              (patient_id, visit_id, amount, insurance_amount, patient_amount, 
                               payment_status, payment_date, payment_method)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                              (patient_id, visit_id, amount, insurance_amount, patient_amount, 
                               status, payment_date, method))
            self.conn.commit()
            
            messagebox.showinfo(self._tr("success"), self._tr("billing_saved"))
            self.clear_billing_form()
            self.load_billing_list()
            
        except sqlite3.Error as e:
            messagebox.showerror(self._tr("database_error"), f"Failed to save billing record: {e}")
    
    def clear_billing_form(self):
        self.b_patient.set('')
        self.b_visit.set('')
        self.b_visit['values'] = []
        self.b_amount.delete(0, tk.END)
        self.b_insurance.delete(0, tk.END)
        self.b_insurance.insert(0, "0")
        self.b_patient_payment.delete(0, tk.END)
        self.b_status.set(self._tr("pending"))
        self.b_method.set('')
        self.b_date.delete(0, tk.END)
        self.b_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
    
    def load_billing_list(self):
        # Clear current list
        for item in self.billing_tree.get_children():
            self.billing_tree.delete(item)
        
        # Fetch billing records from database with patient names and visit dates
        self.cursor.execute('''SELECT b.id, p.name, mr.visit_date, b.amount, b.payment_status, b.payment_method
                           FROM billing b
                           JOIN patients p ON b.patient_id = p.id
                           JOIN medical_records mr ON b.visit_id = mr.id
                           ORDER BY b.id DESC''')
        bills = self.cursor.fetchall()
        
        # Add to treeview
        for bill in bills:
            self.billing_tree.insert('', tk.END, values=bill)
    
    def load_billing_data(self, event):
        # Get selected item
        selected_item = self.billing_tree.focus()
        if not selected_item:
            return
        
        # Get billing ID
        billing_id = self.billing_tree.item(selected_item)['values'][0]
        
        # Fetch billing data
        self.cursor.execute('''SELECT b.*, p.name, mr.visit_date, d.name, mr.diagnosis
                           FROM billing b
                           JOIN patients p ON b.patient_id = p.id
                           JOIN medical_records mr ON b.visit_id = mr.id
                           JOIN doctors d ON mr.doctor_id = d.id
                           WHERE b.id=?''', (billing_id,))
        bill = self.cursor.fetchone()
        
        if not bill:
            return
        
        # Fill form with billing data
        self.clear_billing_form()
        
        # Find patient key
        patient_name = bill[9]   # p.name
        patient_id = bill[1]     # b.patient_id
        patient_key = f"{patient_name} (ID: {patient_id})"
        
        # Find visit key
        visit_date = bill[10]    # mr.visit_date
        doctor_name = bill[11]   # d.name
        diagnosis = bill[12]     # mr.diagnosis
        visit_id = bill[2]       # b.visit_id
        
        visit_key = f"Visit on {visit_date} with {doctor_name} - {diagnosis[:30]}..."
        
        self.b_patient.set(patient_key)
        self.load_patient_visits()  # This will populate the visit combobox
        self.b_visit.set(visit_key)
        self.b_amount.insert(0, f"{bill[3]:,.2f}")
        self.b_insurance.insert(0, f"{bill[4]:,.2f}")
        self.b_patient_payment.insert(0, f"{bill[5]:,.2f}")
        self.b_status.set(bill[6])
        self.b_method.set(bill[8])
        self.b_date.delete(0, tk.END)
        self.b_date.insert(0, bill[7])
    
    def show_reports(self):
        self.current_page = self.show_reports
        self.clear_main_frame()
        
        # Reports Frame
        report_frame = ttk.LabelFrame(self.main_frame, text=self._tr("reports"))
        report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Report type selection
        ttk.Label(report_frame, text=self._tr("select_report")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.report_type = ttk.Combobox(report_frame, 
                                      values=[self._tr(rt) for rt in self._tr("report_types")],
                                      width=40)
        self.report_type.grid(row=0, column=1, padx=5, pady=5)
        
        # Date range
        ttk.Label(report_frame, text=self._tr("start_date")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.report_start = ttk.Entry(report_frame, width=40)
        self.report_start.grid(row=1, column=1, padx=5, pady=5)
        self.report_start.insert(0, datetime.datetime.now().strftime("%Y-%m-01"))
        
        ttk.Label(report_frame, text=self._tr("end_date")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.report_end = ttk.Entry(report_frame, width=40)
        self.report_end.grid(row=2, column=1, padx=5, pady=5)
        self.report_end.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        # Buttons
        btn_frame = ttk.Frame(report_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text=self._tr("button_generate"), command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_export"), command=self.export_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text=self._tr("button_back"), command=self.show_welcome).pack(side=tk.LEFT, padx=5)
        
        # Report display
        self.report_text = tk.Text(report_frame, height=20, width=100)
        self.report_text.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(report_frame, orient=tk.VERTICAL, command=self.report_text.yview)
        self.report_text.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky='ns')
    
    def generate_report(self):
        report_type = self.report_type.get()
        start_date = self.report_start.get()
        end_date = self.report_end.get()
        
        if not report_type:
            messagebox.showerror(self._tr("error"), f"{self._tr('required_fields')}")
            return
        
        try:
            # Validate dates
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror(self._tr("error"), self._tr("invalid_date"))
            return
        
        self.report_text.config(state=tk.NORMAL)
        self.report_text.delete(1.0, tk.END)
        
        # Reverse translation for report type
        report_map = {self._tr(rt): rt for rt in self._tr("report_types")}
        original_report_type = report_map.get(report_type, report_type)
        
        if original_report_type == "Patient List":
            self.generate_patient_report(start_date, end_date)
        elif original_report_type == "Doctor List":
            self.generate_doctor_report()
        elif original_report_type == "Medical Visits":
            self.generate_visits_report(start_date, end_date)
        elif original_report_type == "Billing Summary":
            self.generate_billing_report(start_date, end_date)
        elif original_report_type == "Insurance Claims":
            self.generate_insurance_report(start_date, end_date)
        
        self.report_text.config(state=tk.DISABLED)
    
    def generate_patient_report(self, start_date, end_date):
        lang = self.current_lang
        self.cursor.execute('''SELECT id, name, dob, gender, insurance_type, registration_date 
                            FROM patients 
                            WHERE registration_date BETWEEN ? AND ?
                            ORDER BY registration_date''', (start_date, end_date))
        patients = self.cursor.fetchall()
        
        self.report_text.insert(tk.END, f"{self._tr('report_types')[0].upper()}\n")
        self.report_text.insert(tk.END, f"{self._tr('from')} {start_date} {self._tr('to')} {end_date}\n\n")
        self.report_text.insert(tk.END, 
            f"{'ID':<5} {self._tr('name'):<30} {self._tr('dob'):<12} {self._tr('gender'):<8} "
            f"{self._tr('insurance_type'):<15} {'Reg Date'}\n")
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        
        for patient in patients:
            self.report_text.insert(tk.END, 
                f"{patient[0]:<5} {patient[1]:<30} {patient[2]:<12} {patient[3]:<8} "
                f"{patient[4]:<15} {patient[5]}\n")
        
        self.report_text.insert(tk.END, f"\n{self._tr('from')} {len(patients)} {self._tr('patient').lower()}\n")
    
    def generate_doctor_report(self):
        lang = self.current_lang
        self.cursor.execute('''SELECT id, name, specialization, phone, schedule 
                            FROM doctors 
                            ORDER BY name''')
        doctors = self.cursor.fetchall()
        
        self.report_text.insert(tk.END, f"{self._tr('report_types')[1].upper()}\n\n")
        self.report_text.insert(tk.END, 
            f"{'ID':<5} {self._tr('name'):<25} {self._tr('specialization'):<20} "
            f"{self._tr('phone'):<15} {self._tr('schedule')}\n")
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        
        for doctor in doctors:
            self.report_text.insert(tk.END, 
                f"{doctor[0]:<5} {doctor[1]:<25} {doctor[2]:<20} "
                f"{doctor[3]:<15} {doctor[4][:30]}...\n")
        
        self.report_text.insert(tk.END, f"\n{self._tr('from')} {len(doctors)} {self._tr('doctor').lower()}\n")
    
    def generate_visits_report(self, start_date, end_date):
        lang = self.current_lang
        self.cursor.execute('''SELECT mr.id, p.name, mr.visit_date, d.name, mr.diagnosis
                            FROM medical_records mr
                            JOIN patients p ON mr.patient_id = p.id
                            JOIN doctors d ON mr.doctor_id = d.id
                            WHERE mr.visit_date BETWEEN ? AND ?
                            ORDER BY mr.visit_date''', (start_date, end_date))
        visits = self.cursor.fetchall()
        
        self.report_text.insert(tk.END, f"{self._tr('report_types')[2].upper()}\n")
        self.report_text.insert(tk.END, f"{self._tr('from')} {start_date} {self._tr('to')} {end_date}\n\n")
        self.report_text.insert(tk.END, 
            f"{'ID':<5} {self._tr('patient'):<25} {self._tr('visit_date'):<12} "
            f"{self._tr('doctor'):<25} {self._tr('diagnosis')}\n")
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        
        for visit in visits:
            self.report_text.insert(tk.END, 
                f"{visit[0]:<5} {visit[1]:<25} {visit[2]:<12} "
                f"{visit[3]:<25} {visit[4][:30]}...\n")
        
        self.report_text.insert(tk.END, f"\n{self._tr('from')} {len(visits)} {self._tr('visit').lower()}\n")
    
    def generate_billing_report(self, start_date, end_date):
        lang = self.current_lang
        self.cursor.execute('''SELECT b.id, p.name, mr.visit_date, b.amount, 
                            b.insurance_amount, b.patient_amount, b.payment_status, b.payment_method
                            FROM billing b
                            JOIN patients p ON b.patient_id = p.id
                            JOIN medical_records mr ON b.visit_id = mr.id
                            WHERE b.payment_date BETWEEN ? AND ?
                            ORDER BY b.payment_date''', (start_date, end_date))
        bills = self.cursor.fetchall()
        
        total_amount = sum(bill[3] for bill in bills)
        total_insurance = sum(bill[4] for bill in bills)
        total_patient = sum(bill[5] for bill in bills)
        
        self.report_text.insert(tk.END, f"{self._tr('report_types')[3].upper()}\n")
        self.report_text.insert(tk.END, f"{self._tr('from')} {start_date} {self._tr('to')} {end_date}\n\n")
        self.report_text.insert(tk.END, 
            f"{'ID':<5} {self._tr('patient'):<25} {self._tr('visit_date'):<12} "
            f"{self._tr('total_amount'):>10} {self._tr('insurance_coverage'):>10} "
            f"{self._tr('patient_payment'):>10} {self._tr('payment_status'):<15} "
            f"{self._tr('payment_method')}\n")
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        
        for bill in bills:
            self.report_text.insert(tk.END, 
                f"{bill[0]:<5} {bill[1]:<25} {bill[2]:<12} "
                f"{bill[3]:>10,.2f} {bill[4]:>10,.2f} {bill[5]:>10,.2f} "
                f"{bill[6]:<15} {bill[7]}\n")
        
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        self.report_text.insert(tk.END, 
            f"{'Total:':<42} {total_amount:>10,.2f} {total_insurance:>10,.2f} "
            f"{total_patient:>10,.2f}\n")
        self.report_text.insert(tk.END, f"\n{self._tr('from')} {len(bills)} {self._tr('bill').lower()}\n")
    
    def generate_insurance_report(self, start_date, end_date):
        lang = self.current_lang
        self.cursor.execute('''SELECT b.id, p.name, p.insurance_type, p.insurance_number,
                            mr.visit_date, b.amount, b.insurance_amount, b.payment_method
                            FROM billing b
                            JOIN patients p ON b.patient_id = p.id
                            JOIN medical_records mr ON b.visit_id = mr.id
                            WHERE b.payment_date BETWEEN ? AND ? 
                            AND b.payment_method IN ('BPJS', 'Allianz', 'Prudential')
                            ORDER BY p.insurance_type''', (start_date, end_date))
        claims = self.cursor.fetchall()
        
        # Group by insurance type
        insurance_totals = {}
        for claim in claims:
            ins_type = claim[2]
            insurance_totals[ins_type] = insurance_totals.get(ins_type, 0) + claim[6]
        
        self.report_text.insert(tk.END, f"{self._tr('report_types')[4].upper()}\n")
        self.report_text.insert(tk.END, f"{self._tr('from')} {start_date} {self._tr('to')} {end_date}\n\n")
        self.report_text.insert(tk.END, 
            f"{'ID':<5} {self._tr('patient'):<25} {self._tr('insurance_type'):<15} "
            f"{self._tr('insurance_number'):<15} {self._tr('visit_date'):<12} "
            f"{self._tr('total_amount'):>10} {self._tr('insurance_coverage'):>10} "
            f"{self._tr('payment_method')}\n")
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        
        for claim in claims:
            self.report_text.insert(tk.END, 
                f"{claim[0]:<5} {claim[1]:<25} {claim[2]:<15} {claim[3]:<15} "
                f"{claim[4]:<12} {claim[5]:>10,.2f} {claim[6]:>10,.2f} {claim[7]}\n")
        
        self.report_text.insert(tk.END, "-" * 90 + "\n")
        self.report_text.insert(tk.END, f"{self._tr('insurance_type')} {self._tr('from')}:\n")
        for ins_type, total in insurance_totals.items():
            self.report_text.insert(tk.END, f"{ins_type}: {total:,.2f}\n")
        
        self.report_text.insert(tk.END, f"\n{self._tr('from')} {len(claims)} {self._tr('claim').lower()}\n")
    
    def export_report(self):
        report_text = self.report_text.get("1.0", tk.END)
        if not report_text.strip():
            messagebox.showerror(self._tr("error"), self._tr("no_report"))
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")],
            title=self._tr("export_report"))
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                # For CSV, we need to parse the text into rows and columns
                if file_path.endswith('.csv'):
                    writer = csv.writer(file)
                    
                    # Simple parsing - split lines and then split by multiple spaces
                    lines = report_text.split('\n')
                    for line in lines:
                        if line.strip():  # Skip empty lines
                            # Split by 2+ spaces to get columns
                            row = [col.strip() for col in line.split('  ') if col.strip()]
                            writer.writerow(row)
                else:
                    file.write(report_text)
            
            messagebox.showinfo(self._tr("success"), f"{self._tr('report_exported')} {file_path}")
        except Exception as e:
            messagebox.showerror(self._tr("error"), f"Failed to export report: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HMSApp(root)
    root.mainloop()