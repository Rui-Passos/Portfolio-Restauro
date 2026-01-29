# Art Portfolio & Restoration Management System 🎨

A professional Full-Stack web application built for art restorers and artists to showcase their portfolio and manage content through a secure administrative dashboard.

## 🚀 Key Features

- **Custom CMS:** A secure, password-protected admin area to upload, edit, and delete projects without touching the code.
- **Dynamic Portfolio:** Real-time rendering of projects from a SQL database (SQLAlchemy ORM).
- **Scalable Architecture:** Migrated from JSON-based storage to a robust Relational Database (SQLite) for better data integrity.
- **NOC-Grade Security:** - Environment Variables (`.env`) for sensitive credential management.
  - Secure Session handling for Admin access.
  - Input sanitization and secure file upload handling.

## 🛠️ Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLite with SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, JavaScript
- **Environment:** Linux / PythonAnywhere / Mac Development

## 📂 Project Structure

```text
├── app.py              # Main application entry point & routes
├── utils.py            # Modular helper functions for file/JSON handling
├── models.py           # Database schemas and ORM definitions
├── templates/          # Jinja2 HTML templates
├── static/             # CSS, JS, and User Uploads
└── .env                # Environment variables (Hidden for security)