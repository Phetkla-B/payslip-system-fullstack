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

Frontend (Vue 3)

        |

        v

Backend (FastAPI)

        |

        v
        
MySQL Database

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

cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload

## Run Frontend

cd frontend

npm install

npm run dev