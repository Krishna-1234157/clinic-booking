# Clinic Booking System

## 1. Project Overview
This is a **Django-based web application** for managing doctor appointments.  
Users can register, log in, book appointments with available doctors, view their bookings, and cancel them.  
Admins can manage doctors, view all appointments, and monitor the clinic schedule.

**Key Features:**
- User registration and login
- Book appointments with available doctors
- Cancel booked appointments
- Admin dashboard to manage doctors and appointments

---

## 2. Technology Stack
- **Backend:** Python 3.x, Django 4.x  
- **Frontend:** HTML, CSS, Bootstrap  
- **Database:** SQLite (default, can switch to PostgreSQL/MySQL)  
- **Version Control:** Git & GitHub  

---

## 3. Installation & Setup

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/clinic-booking-system.git
cd clinic-booking-system
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open your browser at http://127.0.0.1:8000/

Log in as a user or admin to access different features.
