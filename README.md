# Payslip System Fullstack
## Self-Service Payslip System
A full-stack web application for managing employee payslips.

Employee can securely view and download their payslips while administrators can upload monthly payroll data through Excel files.

## Features
- Login using Citizen ID and Password
- View monthly payslips
- View payslip details
- Download payslip as PDF

### Administrator
- Login with role-based access control
- Upload monthly payslip Excel file
- View upload history
- View upload detail
- Excel format validation
- Duplicate payslip protection

### Security
- JWT Authentication
- Role-based Authorization
- Protected API Endpoints

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Pandas
- ReportLab

### Frontend
- Vue 3
- Vue Router
- Axios

### Development Tools
- Git
- GitHub

## Architecture

Frontend (Vue 3) -> Backend (FastAPI) -> MySQL Database

## Database Design

Main Tables:

- users
- payslips
- upload_histories

## API Endpoints

### Authentication

- POST /auth/register
- POST /auth/login

### User

- GET /users/me

### Payslips

- GET /payslips
- GET /payslips/{id}
- GET /payslips/{id}/pdf

### Admin

- POST /admin/upload-payslip
- GET /admin/upload-history
- GET /admin/upload-history/{upload-history_id}

## Excel Validation

Required Columns:

- เลขรหัส / ID
- ชื่อ-สกุล / Name
- ID Card
- เงินเดือน / Salary
- รายรับทั้งหมด / Total Income
- รวมรายการหัก
- รวมทั้งหมด / Total Payment

The system will reject file with missing required columns.

## Run Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload

## Run Frontend

cd frontend

npm install

npm run dev

## Database ER Diagram

```mermaid
erDiagram

    USERS ||--o{ PAYSLIPS : owns
    UPLOAD_HISTORIES ||--o{ PAYSLIPS : creates

    USERS {
        int id PK
        string citizen_id
        string full_name
        string role
    }

    PAYSLIPS {
        int id PK
        int user_id FK
        int upload_history_id FK
        string employee_code
        string citizen_id
        int salary_month
        int salary_year
        decimal total_income
        decimal total_deduction
        decimal net_salary
    }

    UPLOAD_HISTORIES {
        int id PK
        string file_name
        int uploaded_by_user_id
        int salary_month
        int salary_year
        string status
    }