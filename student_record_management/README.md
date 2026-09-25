# Student Record Management System (Python & MySQL)

A production-grade, human-designed institutional native desktop and mobile application for managing student academic records, daily attendance roll calls, examination grading, department structures, and official ReportLab PDF reports.

Built with **Python 3.11+**, **MySQL**, and **Kivy**, following clean architecture, separation of concerns, parameterized SQL queries, robust transaction management, and an institutional theme (Navy Blue `#1E3A8A` + Teal `#0D9488`).

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Project Directory Architecture](#project-directory-architecture)
5. [Prerequisites & Python Installation](#prerequisites--python-installation)
6. [Step-by-Step Installation Guide](#step-by-step-installation-guide)
   - [1. Clone / Extract Repository](#1-clone--extract-repository)
   - [2. Create Python Virtual Environment](#2-create-python-virtual-environment)
   - [3. Install Dependencies](#3-install-dependencies)
7. [MySQL Database Setup (Free Cloud & Local)](#mysql-database-setup-free-cloud--local)
   - [Recommended Free Hosted MySQL Providers](#recommended-free-hosted-mysql-providers)
   - [Importing schema.sql and seed.sql](#importing-schemasql-and-seedsql)
   - [Configuring .env](#configuring-env)
8. [Running the Application](#running-the-application)
9. [Operational Modules Guide](#operational-modules-guide)
   - [Executive Dashboard](#executive-dashboard)
   - [Student Registry & Search](#student-registry--search)
   - [Student Profile & Academic Dossier](#student-profile--academic-dossier)
   - [Attendance Roll Call & Audit](#attendance-roll-call--audit)
   - [Marks & Gradebook](#marks--gradebook)
   - [Department & Class Hierarchy](#department--class-hierarchy)
   - [Official PDF & CSV Reports](#official-pdf--csv-reports)
10. [Offline Demonstration & Resilient Fallback](#offline-demonstration--resilient-fallback)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Packaging & Distribution](#packaging--distribution)
   - [Desktop Executable (PyInstaller)](#desktop-executable-pyinstaller)
   - [Android APK (Buildozer)](#android-apk-buildozer)

---

## Project Overview

The **Student Record Management System** is engineered specifically for academic and institutional record administrators. Unlike toy scripts or fragile web scrapers, this system provides:
- **Zero Raw SQL String Concatenation**: Complete parameterized queries preventing SQL injection vulnerabilities.
- **Connection Pooling & Auto-Reconnect**: Thread-safe database connection pool with transaction rollbacks on failure.
- **Graceful Error Handling**: Technical stack traces are logged to `logs/app.log` with rotation, while end-users receive clean, actionable notices.
- **Responsive Geometry**: Seamlessly scales from desktop monitors (1920x1080, 1440x900) down to compact laptops (1180x740), tablets (768x1024), and mobile viewport aspect ratios.
- **Institutional Aesthetics**: Clean surfaces, high-contrast dark navy primary theme, clear visual hierarchy, and tactile buttons without flashy AI gradients.

---

## Key Features

- **Executive Analytics Dashboard**: Instant KPI cards for Total Students, Active Students, Male/Female ratios, Active Departments, and quick links to recently registered students.
- **Comprehensive Student Management**:
  - Full CRUD: Add, Search, Filter, View Details, Edit, and Delete records.
  - Multi-Criteria Search: Instant case-insensitive matching across Student ID, Admission Number, Name, Phone Number, and Department.
  - Granular Filters: By Department, Status (Active, Inactive, Suspended, Graduated), Gender, and Academic Year (1 to 4).
  - Validation: Strict verification of email syntax, phone format, ISO dates (`YYYY-MM-DD`), unique admission numbers, and valid department references.
- **Academic Dossier (Student Profile)**:
  - 360-degree view containing Personal, Contact, Academic, Guardian, and Admission dates.
  - Live attendance percentage summary badge.
  - Academic transcript table showing subject scores, percentages, and letter grades.
- **Attendance Roll Call**:
  - Daily date-based roll call table with one-click toggles (`Present`, `Absent`, `Late`).
  - "Mark All Present" convenience action for fast attendance entry.
  - Audit trail with remarks and attendance percentage calculations.
- **Marks & Examination Evaluation**:
  - Subject score entries with dynamic grade preview.
  - Automated percentage computation and standard letter grade assignment (`A+`, `A`, `B`, `C`, `D`, `F`).
  - Validation ensuring scores never exceed maximum marks and cannot be negative.
- **Department Administration**:
  - Add and update academic faculties, codes, descriptions, and statuses.
  - Integrity safeguards: Prevents accidental deletion of departments that have active enrolled students.
- **Printable Reports & Data Export**:
  - Generates formal landscape **ReportLab PDF** directories with institutional headers and page numbers.
  - One-click exports of Students, Daily Attendance, and Examination Gradebooks to **CSV** format for Microsoft Excel and Google Sheets.
- **Diagnostics & Connectivity**:
  - Built-in Diagnostic view to test MySQL round-trip latency, inspect `.env` parameters (passwords masked), and review application log files.

---

## Technology Stack

- **Programming Language**: Python 3.11+
- **GUI Framework**: Kivy 2.3+ / KivyMD
- **Database Engine**: MySQL 5.7+ / 8.0+
- **Database Connector**: `mysql-connector-python>=8.3.0`
- **Environment Management**: `python-dotenv>=1.0.1`
- **Document Generation**: `reportlab>=4.1.0`
- **Image Processing**: `pillow>=10.2.0`

---

## Project Directory Architecture

```text
student_record_management/
│
├── main.py                     # Native Kivy application entry point & ScreenManager
├── init_database.py            # Automated free online MySQL database initializer (No Workbench needed!)
├── requirements.txt           # Production dependencies specification
├── README.md                  # Comprehensive technical and setup documentation
├── .env.example               # Database configuration template
├── .gitignore                 # Version control exclusions
│
├── database/
│   ├── schema.sql             # Complete DDL: tables, foreign keys, indexes, constraints
│   └── seed.sql               # Realistic sample data (12 students, 4 depts, marks, attendance)
│
├── app/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Environment variables, color palette, rotating logger
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py      # Connection pooling, auto-init schema, transaction management
│   │   └── queries.py         # Parameterized SQL statements (%s placeholders)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py         # Student entity dataclass
│   │   ├── attendance.py      # Attendance entity dataclass
│   │   ├── marks.py           # Marks & exam results dataclass
│   │   └── department.py      # Department entity dataclass
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py     # Student business logic & validation
│   │   ├── attendance_service.py  # Roll call & attendance calculations
│   │   ├── marks_service.py       # Score validation & grade computing
│   │   ├── department_service.py  # Department integrity & enrollment counts
│   │   └── report_service.py      # ReportLab PDF building & CSV export
│   │
│   ├── screens/
│   │   ├── __init__.py
│   │   ├── dashboard.py       # ScholarPulse KPI dashboard
│   │   ├── students.py        # Student directory, search & filters
│   │   ├── student_form.py    # Add & Edit student form
│   │   ├── student_details.py # 360-degree student profile
│   │   ├── attendance.py      # Daily attendance roll call
│   │   ├── marks.py           # Marks recording & results list
│   │   ├── departments.py     # Academic departments management
│   │   ├── reports.py         # PDF & CSV generation center
│   │   └── settings_screen.py # Connection diagnostics & logging
│   │
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── statistic_card.py  # KPI summary card
│   │   ├── student_card.py    # Directory student item card
│   │   ├── nav_drawer.py      # Responsive sidebar navigation & top bar
│   │   └── dialogs.py         # ConfirmDialog and InfoDialog popups
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py      # Input validation routines
│       ├── helpers.py         # Grade calculations & CSV writers
│       └── constants.py       # Academic scales, subjects, statuses
│
├── logs/
│   └── app.log                # Rotating technical execution logs
│
├── reports_export/            # Output folder for generated PDFs and CSVs
│
└── assets/
    ├── icons/
    └── images/
```

---

## Prerequisites & Python Installation

Ensure you have **Python 3.11** or newer installed:

- **Windows**: Download from [python.org](https://www.python.org/downloads/). During installation, check the box: **"Add Python to PATH"**.
- **macOS**: Install via Homebrew:
  ```bash
  brew install python@3.11
  ```
- **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv libgl1-mesa-dev
  ```

---

## Step-by-Step Installation Guide

### 1. Clone / Extract Repository
Extract `student_record_management.zip` or open the project folder in Visual Studio Code:
```bash
cd student_record_management
```

### 2. Create Python Virtual Environment

Creating an isolated virtual environment ensures clean dependency isolation:

- **Windows (Command Prompt / PowerShell)**:
  ```cmd
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

Upon activation, your terminal prompt will prefix with `(.venv)`.

### 3. Install Dependencies
Install all required libraries from `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Free Online MySQL Database Setup (No Workbench Required)

The application communicates over standard MySQL wire protocol. You **do not need to install MySQL Workbench or any desktop software**! You can use any free online cloud MySQL database service.

### Recommended 100% Free Online Cloud MySQL Providers

You can get a free online cloud MySQL database up and running in 2 minutes:

1. **Aiven.io (Recommended Free Tier)**:
   - Provides free managed MySQL 8.0 cloud instance.
   - Sign up at [aiven.io](https://aiven.io) (no credit card required on free plan).
   - In your Aiven web dashboard, note:
     - **Host** (e.g., `mysql-yourname.aivencloud.com`)
     - **Port** (e.g., `12345`)
     - **User** (e.g., `avnadmin`)
     - **Password** (your secret password)
     - **Database** (e.g., `defaultdb`)

2. **TiDB Cloud Serverless (Free Forever MySQL 8.0)**:
   - Instant serverless MySQL-compatible database at [tidbcloud.com](https://tidbcloud.com).
   - Provides direct credentials and an interactive web SQL editor.

3. **Clever Cloud / Alwaysdata / db4free**:
   - Provide free MySQL cloud hosting with browser-based web dashboards and phpMyAdmin.

---

### Step 1: Configure Your `.env` File

Copy the configuration template:
```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` in VS Code and fill in your free online MySQL credentials:
```ini
DB_HOST=mysql-instance-yourdomain.aivencloud.com
DB_PORT=12345
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=your_secure_password_here

# Connection pool settings (optional)
DB_POOL_NAME=student_pool
DB_POOL_SIZE=5
DB_CONNECT_TIMEOUT=10
```

---

### Step 2: 1-Click Database Provisioning (Zero Workbench Needed!)

You don't need MySQL Workbench or command-line SQL imports. Choose either of these hassle-free methods:

#### Method A: Automated Python Initializer (Recommended)
Run the built-in database provisioner script:
```bash
python init_database.py
```
This script connects to your remote free online MySQL server, executes `database/schema.sql` to build the tables, indexes, and relations, and seeds initial data from `database/seed.sql`.

#### Method B: Automatic On-Launch Provisioning
Simply launch the application:
```bash
python main.py
```
The application checks your remote online database upon connection; if the tables do not exist yet, it automatically provisions the complete schema and seed data!

#### Method C: Online Web SQL Console / phpMyAdmin (Optional)
If your free online cloud host provides an in-browser SQL console (such as phpMyAdmin or Cloud Query Editor):
1. Copy the contents of `database/schema.sql` and run it in the web editor.
2. Copy the contents of `database/seed.sql` and run it to populate sample data.

---

## Running the Application

Launch the native desktop interface:
```bash
python main.py
```

VS Code Users: Press `F5` or select **Run Without Debugging** (`Ctrl + F5`) in the `main.py` tab.

---

## Operational Modules Guide

### ScholarPulse Dashboard
- Visualizes real-time counts of enrolled students, active status ratio, gender breakdown, and active academic faculties.
- Offers direct shortcuts to "+ Add Student", "Mark Attendance", and "Generate Reports".
- Lists the 5 most recently admitted students with direct "View" shortcuts.

### Student Registry & Search
- Type into the search field to filter in real-time across Student ID, Admission Number, Name, Phone, and Department.
- Use dropdowns to filter by Department and Account Status (`Active`, `Inactive`, `Suspended`, `Graduated`).
- Click "Reset" to instantly restore all records.
- Each student card displays admission badge, contact information, and action buttons (`View Profile`, `Edit`, `Delete`).

### Student Profile & Academic Dossier
- Displays complete student records organized into logical sections:
  - Personal Details (Name, Gender, DOB)
  - Contact Details (Email, Phone, Address)
  - Academic Details (Department, Year, Admission Date, Status)
  - Guardian Information (Name, Emergency Phone)
- Highlights live attendance percentage.
- Lists the student's examination history and assigned grades.

### Attendance Roll Call & Audit
- Select any calendar date (`YYYY-MM-DD`) and click "Load Records".
- Toggle `Present`, `Absent`, or `Late` for each student.
- Click "Mark All Present" to quickly default the entire cohort.
- Add optional notes/reasons for absence or tardiness.
- Click "Save All Attendance" to record transactions to the database.

### Marks & Gradebook
- Select student, subject, and exam type (`Sem Exam`, `Final Exam`, `Quiz 1`, etc.).
- Input marks obtained and maximum marks.
- Live preview computes percentage and letter grade automatically:
  - `90%+` → **A+**
  - `80% - 89%` → **A**
  - `70% - 79%` → **B**
  - `60% - 69%` → **C**
  - `50% - 59%` → **D**
  - `< 50%` → **F**
- Click "Record Score" to persist the score.
- Review existing score sheets with options to delete or adjust records.

### Department & Class Hierarchy
- Manage academic departments and study programs.
- Displays live headcount of active students enrolled in each department.
- Safety check prevents deleting departments with active students.

### Official PDF & CSV Reports
- **Official Student Directory (PDF)**: Formatted landscape document generated with ReportLab containing institutional headers, column widths, and page numbers.
- **Student Registry (CSV)**: Full data export suitable for Excel or data imports.
- **Attendance Audit (CSV)**: Daily attendance audit log for any chosen date.
- **Examination Transcript (CSV)**: Scores, percentages, and grades across all subjects.
- All files are automatically saved to `reports_export/`.

---

## Offline Demonstration & Resilient Fallback

If you run the application before configuring `.env`, or if your internet connection temporarily drops:
- **The application does NOT crash.**
- It automatically initializes in **Local Demonstration Mode** with sample records preloaded.
- A notification informs the user of demonstration mode.
- You can explore, add, edit, test searches, and mark attendance in demo mode.
- Once your `.env` is configured, visit the **Database / Settings** screen and click **"Test Connection & Reconnect"** to connect to MySQL without restarting.

---

## Troubleshooting Guide

### 1. `mysql-connector-python` or `kivy` fails to import
Ensure your virtual environment is active (`(.venv)`) and run:
```bash
pip install -r requirements.txt
```

### 2. Kivy Window does not open on Linux
Ensure required OpenGL and X11 development headers are installed:
```bash
sudo apt install libgl1-mesa-dev libgles2-mesa-dev xorg-dev
```

### 3. Remote MySQL Connection Timeout / Access Denied
- Double check `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD` in `.env`.
- Ensure your cloud MySQL provider allows connections from your IP (e.g. `0.0.0.0/0` in firewall/allowlist settings).
- Review `logs/app.log` for sanitized technical connection errors.

### 4. PDF Generation fails with `ModuleNotFoundError: No module named 'reportlab'`
Install ReportLab into your virtual environment:
```bash
pip install reportlab
```

---

## Packaging & Distribution

### Desktop Executable (PyInstaller)
To create a standalone `.exe` (Windows) or executable binary (macOS/Linux) that does not require Python on the target machine:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "StudentRecordManager" main.py
```
The compiled executable will be located in the `dist/` directory.

### Android APK (Buildozer)
Kivy applications can be packaged into Android APKs using Buildozer:
1. Initialize Buildozer specification:
   ```bash
   buildozer init
   ```
2. In `buildozer.spec`, configure:
   ```ini
   requirements = python3,kivy,kivymd,mysql-connector-python,python-dotenv,reportlab,pillow
   orientation = portrait,landscape
   ```
3. Build debug APK:
   ```bash
   buildozer android debug
   ```
The output APK will be placed in the `bin/` directory.

---

## License & Attribution
Created for educational, institutional, and production administrative deployment. Clean, modular, and ready to run.
