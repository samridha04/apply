from flask import Flask, request, render_template, redirect, url_for
import os
import mysql.connector

app = Flask(__name__)

# Directory to save uploaded resumes
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'srisam012345#',
    'host': 'localhost',
    'port' : 3306,
    'database': 'job_applications',
    'auth_plugin': 'mysql_native_password'

}

# Function to connect to the database
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    return 'Welcome to the job application portal!'

# Job application form
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        linkedin_profile = request.form['linkedin_profile']  # LinkedIn profile link
        
        # Check if the POST request has the file part (resume)
        if 'resume' not in request.files:
            return 'No file part'
        
        resume = request.files['resume']
        if resume.filename == '':
            return 'No selected file'

        # Save the resume file
        if resume:
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(resume_path)

            # Store the applicant's details in the database
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO applicants (name, email, linkedin_profile, resume_path)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, linkedin_profile, resume_path))
            conn.commit()
            cursor.close()
            conn.close()

            return f"Application received for {name}. Resume saved at {resume_path}, LinkedIn Profile: {linkedin_profile}"

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
