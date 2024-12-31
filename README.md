# Detection of Lumbar Spondylolisthesis

This is a Django-based web application designed to detect Lumbar Spondylolisthesis from medical images such as X-rays. The application utilizes machine learning, specifically a Convolutional Neural Network (CNN), to accurately classify and grade the severity of the condition. It provides separate user and admin portals for effective management of tasks and diagnostics.

---

## Features

- **Medical Diagnosis**: Upload X-ray images for automated detection of Lumbar Spondylolisthesis.
- **Severity Classification**: The system classifies and grades the severity of the condition using trained CNN models.
- **User-Friendly Interface**: Includes separate portals for administrators and users for streamlined workflows.
- **Django Backend**: Robust backend system with secure handling of user data.
- **Static and Template Management**: Organized static assets and HTML templates for seamless frontend integration.

---

## Project Structure

```
├── lum_spond/
│   ├── settings.py        # Django settings configuration
│   ├── __init__.py        # Package initializer
│   ├── urls.py            # URL routing and mapping
│   ├── asgi.py            # ASGI configuration
│   ├── views.py           # View logic for handling requests
│   ├── wsgi.py            # WSGI configuration
│   └── __pycache__/       # Compiled Python files
├── manage.py              # Entry point for Django commands
├── templates/             # HTML templates for the frontend
│   ├── index.html         # Landing page
│   ├── adminLogin.html    # Admin login portal
│   ├── userLogin.html     # User login portal
│   ├── adminPortal.html   # Admin dashboard
│   ├── userPortal.html    # User dashboard
│   └── basic_templates/   # Reusable base templates
│       └── login_basic.html
├── static/                # Static files (e.g., images)
│   └── images/
```

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/nehalms-Detection-of-Lumbar-Spondylolisthesis.git
   cd nehalms-Detection-of-Lumbar-Spondylolisthesis
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open a browser and go to `http://127.0.0.1:8000/`

---

## Usage

- **Admin Portal**: Log in via `adminLogin.html` to manage users and view diagnostic reports.
- **User Portal**: Log in via `userLogin.html` to upload images and access diagnostic results.

---

## Technical Details

- **Framework**: Django
- **Database**: MySQL (for data storage and management)
- **Frontend**: HTML, CSS
- **Machine Learning**: CNN for medical image classification

---

## Future Enhancements

- Implementing advanced data visualization for diagnostic results.
- Extending support for additional medical conditions.
- Adding a feedback system for user experience improvement.
