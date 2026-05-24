# Secure Smart Campus Services System (SSCSS)

This is a functional prototype developed for the IT Project Management (ITPM) Course - Milestone 3.
The system provides a unified platform for students, lecturers, and administrators to manage facility bookings with real-time conflict detection, and allows students to submit maintenance requests.

## Features
- **Role-Based Access Control (RBAC):** Distinct dashboards and access levels for Students, Lecturers, and Admins.
- **Facility Booking & Conflict Detection:** Prevents double-booking of classrooms and labs.
- **Maintenance Request Management:** Allows users to report hardware, software, or facility issues.

## Prerequisites
- Python 3.8+
- pip (Python Package Installer)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/C4L00S3/IDB30303-IT-PROJECT-MANAGEMENT---SCSS-Project.git
   cd IDB30303-IT-PROJECT-MANAGEMENT---SCSS-Project
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Environment Variables:**
   Create a `.env` file in the root directory. You can copy the template provided:
   ```bash
   cp .env.example .env
   ```
   Or manually create `.env` and add the following content:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   DATABASE=scss.db
   ```

4. **Run the application:**
   The SQLite database (`scss.db`) will be automatically generated with the default test accounts on the first run.
   ```bash
   python app.py
   ```

4. **Access the Web Portal:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## Test Accounts

The following accounts are pre-configured for testing purposes. All accounts share the same password.

**Password for all accounts:** `password123`

| Role | Email |
|------|-------|
| **Admin** | `admin@unikl.edu.my` |
| **Lecturer** | `lecturer@unikl.edu.my` |
| **Student 1** | `student@unikl.edu.my` |
| **Student 2** | `student2@unikl.edu.my` |

*(Note: Student 2 can be used to simulate a conflict detection scenario when trying to book a room already reserved by Student 1).*

## Project Details
- **Course:** IDB30303 IT Project Management
- **Developed by:** Louis GOUBEAUX & Noé COMBE
