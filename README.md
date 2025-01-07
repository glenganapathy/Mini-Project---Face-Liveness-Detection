# Face Liveness Detection

## Overview
Liveness Detection System is a web application developed using Django that implements face liveness verification technology. It allows users to log in or sign up, verifying their identity with advanced detection methods.

## Features
- **User Authentication:** Sign up and log in with user credentials.
- **MongoDB Integration:** Stores user information securely.
- **Face Liveness Verification:** Users can perform real-time liveness detection.
- **Responsive Design:** Built with Bootstrap for a clean, modern interface.

## Technologies Used
- Django
- MongoDB
- Bootstrap
- JavaScript
- HTML/CSS
- Python


## Installation

### Prerequisites
- Python 3.x
- Django
- MongoDB
- Virtual Environment

### Steps to Run the Project
1. **Clone the repository:**
   - Open your terminal and run:
     ```bash
     git clone https://github.com/yourusername/liveness-detection.git
     cd liveness-detection
     ```

2. **Create and activate a virtual environment:**
   - Run the following command to create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

3. **Install the required packages:**
   - Use the following command to install the necessary packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set up your MongoDB database:**
   - Ensure MongoDB is running.
   - Update your database settings in `settings.py`.

5. **Run migrations (if any):**
   - Execute the following command:
     ```bash
     python manage.py migrate
     ```

6. **Start the development server:**
   - Start the server with:
     ```bash
     python manage.py runserver
     ```

   - Access the application at `http://127.0.0.1:8000/`.

## Usage
- Navigate to the home page to either log in or sign up.
- After logging in, you can access the liveness detection feature.
