from config import ENROLLMENT_URL
from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from seleniumbase import SB
from flask_cors import CORS

# Importing the extraction function
from utils.table_extractor import extract_course_data_from_table, identify_main_table

app = Flask(__name__)
CORS(app)


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
    with SB(uc=True) as sb:
        sb.open(ENROLLMENT_URL)
        handle_cloudflare_challenge(sb)
        input_user_details(sb, user_id)
        input_course_code(sb, course_code)
        page_html = sb.get_page_source()

    soup = BeautifulSoup(page_html, 'html.parser')
    raw_table = identify_main_table(soup)
    return jsonify(extract_course_data_from_table(str(raw_table)))


def handle_cloudflare_challenge(sb):
    """
    Handle the cloudflare challenge on the page.

    Args:
        sb (SB): SeleniumBase instance.
    """
    if sb.is_element_present("#challenge-stage"):
        # This waits for the cloudflare challenge to complete.
        # Adjust timeout as per your observation of how long it usually takes.
        sb.wait_for_element(
            "/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table/tbody/tr/td[2]/input",
            timeout=60)


def input_user_details(sb, user_id):
    """
    Input user details into the appropriate fields.

    Args:
        sb (SB): SeleniumBase instance.
        user_id (str): User identifier.
    """
    sb.update_text(
        "/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table/tbody/tr/td[2]/input",
        user_id, by="xpath")
    sb.click("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/center/input[1]",
             by="xpath")
    sb.wait_for_element(
        "/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table[2]/tbody/tr/td[2]/input",
        timeout=10)


def input_course_code(sb, course_code):
    """
    Input course code into the appropriate field.

    Args:
        sb (SB): SeleniumBase instance.
        course_code (str): Code of the course to fetch details for.
    """
    sb.update_text(
        "/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table[2]/tbody/tr/td[2]/input",
        course_code, by="xpath")
    sb.click("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/center/input[1]",
             by="xpath")


if __name__ == '__main__':
    app.run()
