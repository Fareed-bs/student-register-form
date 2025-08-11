from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Define the path for the JSON file
JSON_FILE = 'details.json'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Collect form data into a dictionary
        new_entry = {
            "student_name": request.form.get('student_name'),
            "email_id": request.form.get('email_id'),
            "contact_no": request.form.get('contact_no'),
            "address": request.form.get('address'),
            "institution": request.form.get('institution'),
            "branch": request.form.get('branch'),
            "percentage": request.form.get('percentage')
        }

        # Read existing data, append new entry, and write back
        data = []
        # Check if file exists and is not empty to avoid errors
        if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
            with open(JSON_FILE, 'r') as f:
                data = json.load(f)

        data.append(new_entry)
        with open(JSON_FILE, 'w') as f:
            json.dump(data, f, indent=4)

        return redirect(url_for('success'))

    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/viewdetails')
def view_details():
    # Read the JSON file and pass the data to the template
    students = []
    try:
        with open(JSON_FILE, 'r') as f:
            students = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, it means no students are registered yet.
        pass
    except json.JSONDecodeError:
        # If the file is empty or corrupted, treat it as if there are no students.
        pass

    return render_template('viewdetails.html', students=students)


if __name__ == '__main__':
    # Enable debug mode for development for auto-reloading and better error pages
    # Add port number while running the app
    app.run(debug=True)
