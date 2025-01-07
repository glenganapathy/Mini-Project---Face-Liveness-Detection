from django.shortcuts import render, redirect
from django.http import JsonResponse
import subprocess
from pymongo import MongoClient
from django.contrib.auth import logout

# Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
db = client['user_database']
users_collection = db['users']

def login(request):
    error_message = None  # Initialize error message as None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if the user exists in the database
        user = users_collection.find_one({"username": username, "password": password})
        if user:
            request.session['username'] = username  # Save username in session
            return redirect('home')  # Redirect to home page
        else:
            error_message = "Invalid credentials. Please try again."

    return render(request, 'face_detection/login.html', {"error_message": error_message})

def logout_view(request):
    # Use Django's logout to clear session
    logout(request)
    
    # Clear cookies explicitly
    response = redirect('login')  # Redirect to the login page after logout
    for key in request.COOKIES:
        response.delete_cookie(key)
    
    return response

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        # Check if username or email already exists
        if users_collection.find_one({"username": username}):
            return render(request, 'face_detection/signup.html', {"error_message": "Username already exists."})
        if users_collection.find_one({"email": email}):
            return render(request, 'face_detection/signup.html', {"error_message": "Email already registered."})

        # Save the new user to the MongoDB collection
        new_user = {
            "name": name,
            "email": email,
            "username": username,
            "password": password  # Note: Use hashing for storing passwords securely
        }
        users_collection.insert_one(new_user)
        return redirect('login')  # Redirect to login page after successful signup

    return render(request, 'face_detection/signup.html')

def home(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')  # Redirect to login if session is not set

    # Retrieve user's name from MongoDB
    user = users_collection.find_one({"username": username})
    name = user["name"] if user else "Guest"
    return render(request, 'face_detection/home.html', {"name": name})

def detect(request):
    return render(request, 'face_detection/detect.html')

def result(request):
    return render(request, 'face_detection/result.html')

def run_test_script(request):
    """
    Runs the test.py script when the Start Detection button is clicked.
    """
    try:
        # Call the script using subprocess
        result = subprocess.run(
            ['python', 'test.py'],  # Update with the correct path to test.py
            capture_output=True,
            text=True
        )
        # Return output from the script as JSON
        return JsonResponse({
            "status": "success",
            "output": result.stdout,
            "error": result.stderr,
        })
    except Exception as e:
        return JsonResponse({"status": "error", "error": str(e)})

