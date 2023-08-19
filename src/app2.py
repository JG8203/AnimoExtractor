import logging
from config import ENROLLMENT_URL
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
from flask_cors import CORS
import subprocess
import json

# Importing the extraction function
from utils.table_extractor import extract_course_data_from_table, identify_main_table

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

FLARESOLVERR_ENDPOINT = 'http://localhost:8191/v1'  # Adjust the host and port if necessary

@app.route('/')
def index():
    """
    Serve the main landing page of the application.

    Returns:
        str: Rendered HTML template for the index page.
    """
    return render_template('index.html')

@app.route('/course_offerings', methods=['POST'])
def get_course_offerings_details():
    """
    Endpoint to fetch course details based on user input.

    Returns:
        JSON: Extracted course details.
    """
    user_id = request.form.get('user_id')
    course_code = request.form.get('course_code')
    return fetch_course_details(user_id, course_code)

@app.route('/listclasses/<course_id>', methods=['POST'])
def list_classes(course_id):
    """
    Endpoint to list classes based on course ID and user ID.

    Args:
        course_id (str): Course ID to fetch class details for.

    Returns:
        JSON: Extracted class details for the provided course ID.
    """
    user_id = request.form.get('user_id')
    return fetch_course_details(user_id, course_id)

def fetch_course_details(user_id, course_code):
    """
    Fetch course details from the enrollment site using provided user and course information.

    Args:
        user_id (str): User identifier.
        course_code (str): Code of the course to fetch details for.

    Returns:
        JSON: Extracted course details.
    """
    logging.debug(f"Fetching course details for User ID: {user_id}, Course Code: {course_code}")
    
    # Constructing the curl command
    curl_cmd = [
        "curl", "-L", "-X", "POST", 'http://localhost:8191/v1',
        "-H", "Content-Type: application/json",
        "--data-raw", json.dumps({
            "cmd": "request.post",
            "url": "https://enroll.dlsu.edu.ph/dlsu/view_course_offerings",
            "postData": f"p_course_code={course_code}&p_option=all&p_button=Search&p_id_no={user_id}&p_button=Submit",
            "maxTimeout": 60000
        })
    ]

    # Executing the curl command
    response = subprocess.check_output(curl_cmd)
    response_data = json.loads(response)
    
    logging.debug(f"Full FlareSolverr Response: {response_data}")
    
    page_html = response_data['solution']['response']
    
    soup = BeautifulSoup(page_html, 'html.parser')
    raw_table = identify_main_table(soup)
    return jsonify(extract_course_data_from_table(str(raw_table)))

if __name__ == '__main__':
    app.run()
