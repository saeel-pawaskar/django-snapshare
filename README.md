# Snapshare - Django Project

Snapshare is a social media platform built with Django, allowing users to post images, follow friends, send requests to private accounts, and receive notifications for likes, comments, and follow requests.

## Features

- User Authentication: Login, Registration, and Logout
- Image Uploading: Post images to share with friends
- Friend System: Follow users and send requests to private accounts
- Notifications: Get notifications for likes, comments, and follow requests

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.6 or higher
- Django 4.2.5
- pip for managing Python packages

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/snapshare.git
   cd snapshare
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Set your environment variables:

   Create a `.env` file in the project root and add the following values:

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   EMAIL_HOST=smtp.gmail.com
   EMAIL_USE_TLS=True
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

   **Note**: Replace the placeholders with your actual values.

2. Run database migrations:

   ```bash
   python manage.py migrate
   ```

3. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

   Your project will be running at `http://127.0.0.1:8000/`.

## Static and Media Files

- Static files (CSS, JavaScript, and Images) will be served from the `static/` directory.
- Media files (like uploaded images) will be saved in the `media/` directory.

## Requirements

- **Django 4.2.5**
- **django-crispy-forms 2.3**
- **crispy-bootstrap4 2024.10**
- **python-decouple 3.8**

To install the required dependencies, use the following command:

```bash
pip install -r requirements.txt
```

### Key Sections in the README:

1. **Project Overview**: A brief description of what the project does.
2. **Installation Instructions**: Steps to get the project up and running on a local machine.
3. **Configuration**: How to configure environment variables for secret keys and email settings.
4. **Running the Project**: Instructions to run the server and access the admin panel.
5. **Requirements**: The necessary dependencies and instructions to install them.

Let me know if you need any adjustments!
