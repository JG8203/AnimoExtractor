from bs4 import BeautifulSoup
import adaptive_extraction_script
from selenium.webdriver.chrome.options import Options
from seleniumbase import SB

def get_course_offerings_details():
    # Create a new SeleniumBase instance with undetected_chromedriver enabled
    with SB(uc=True) as sb:
        # Step 2: Visit the page
        sb.open("https://enroll.dlsu.edu.ph/dlsu/view_course_offerings")

        # Check for Cloudflare challenge
        if sb.is_element_present("#challenge-stage"):
            print("CloudFlare occurred! Waiting for verification")
            # Wait for the challenge to complete and the textbox for ID to be present
            sb.wait_for_element("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table/tbody/tr/td[2]/input", timeout=60)

        # Step 3: Enter ID
        user_id = input("Please enter your ID number: ")
        sb.update_text("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table/tbody/tr/td[2]/input", user_id, by="xpath")
        sb.click("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/center/input[1]", by="xpath")

        # Wait for the next expected element to appear
        sb.wait_for_element("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table[2]/tbody/tr/td[2]/input", timeout=10)

        # Step 4: Enter Course Code
        course_code = input("Please enter the course code: ")
        sb.update_text("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/table[2]/tbody/tr/td[2]/input", course_code, by="xpath")
        sb.click("/html/body/table[4]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td[2]/form/div/center/input[1]", by="xpath")

        # Step 5: Parse the resulting page
        page_html = sb.get_page_source()
        soup = BeautifulSoup(page_html, 'html.parser')
        raw_table = adaptive_extraction_script.adaptive_table_identification(soup)
        extracted_data = adaptive_extraction_script.adaptive_extraction_v2(raw_table)

        # Step 6: Output the extracted details
        print(extracted_data)

if __name__ == "__main__":
    get_course_offerings_details()
