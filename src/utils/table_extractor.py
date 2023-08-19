from bs4 import BeautifulSoup

def identify_main_table(soup):
    """
    Identifies the primary table of interest in the provided soup object.
    Parameters:
    - soup (BeautifulSoup): The parsed HTML content.
    Returns:
    - BeautifulSoup Tag: The largest table found in the soup.
    """
    tables = soup.find_all('table')
    return max(tables, key=lambda t: len(t.find_all('tr')), default=None)

def extract_course_data_from_table(html_table):
    """
    Extracts course offering data from the given HTML table.
    Parameters:
    - html_table (str): The HTML content of the table.
    Returns:
    - list: A list of dictionaries containing course offering details.
    """
    try:
        soup = BeautifulSoup(html_table, 'html.parser')
        offerings = []
        current_offering = None
        current_class_nbr = None

        for tr in soup.find_all('tr')[1:]:
            columns = tr.find_all('td')
            if len(columns) < 9:
                continue
            class_nbr = columns[0].text.strip()
            if class_nbr.isdigit():
                if class_nbr != current_class_nbr:
                    if current_offering:
                        offerings.append(current_offering)
                    current_offering = create_new_course_offering(columns)
                    current_class_nbr = class_nbr

            if current_offering:
                session = extract_session_data(tr, columns)
                current_offering["classes"].append(session)

        if current_offering:
            offerings.append(current_offering)

        return offerings

    except Exception as e:
        print(f"Error extracting offerings: {e}")
        return []

def create_new_course_offering(columns):
    """
    Creates a new course offering dictionary from the provided columns.
    Parameters:
    - columns (list): List of BeautifulSoup Tags representing table columns.
    Returns:
    - dict: Dictionary containing course offering details.
    """
    course_code = columns[1].text.strip()
    subject_code = course_code[:2]
    catalog_nbr = course_code[2:]
    is_closed = True if columns[1].find('font', {'color': '#0099CC'}) else False
    return {
        "subjectCode": subject_code,
        "catalogNbr": catalog_nbr,
        "classNbr": columns[0].text.strip(),
        "Section": columns[2].text.strip(),
        "isClosed": is_closed,
        "scheduleDayRemarks": columns[8].text.strip(),
        "classes": []
    }

def extract_session_data(tr, columns):
    """
    Extracts session data from the given row and columns.
    Parameters:
    - tr (BeautifulSoup Tag): The table row.
    - columns (list): List of BeautifulSoup Tags representing table columns.
    Returns:
    - dict: Dictionary containing session details.
    """
    next_row = tr.find_next_sibling()
    instructor = ''
    if next_row and len(next_row.find_all('td')) == 1:
        instructor = next_row.text.strip()
    room = columns[5].text.strip() if columns[5].text.strip() else "N/A"
    return {
        "instructor": instructor,
        "room": room,
        "scheduleDayCode": columns[3].text.strip(),
        "scheduleDayTime": columns[4].text.strip()
    }
