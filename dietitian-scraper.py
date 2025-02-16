from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime


driver = None


def setup_driver():
    global driver
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)


def search_location(location):

    global driver
    driver.get("https://member.dietitiansaustralia.org.au/faapd")

    try:
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtLocationSearchField"))
        )
        search_field.clear()
        search_field.send_keys(location)
        time.sleep(2)  # Wait for the suggestions to appear
        search_field.send_keys(Keys.ARROW_DOWN)
        search_field.send_keys(Keys.RETURN)
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pseudoSearchbtn"))
        )
        # Wait for the button to be clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pseudoSearchbtn"))
        )
        search_button.click()

    except Exception as e:
        print(f"An error occurred: {e}")


def grab_data():
    global driver
    practitioners = []  # Initialize empty list at the start

    # Wait for the innerDiv to be present
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "innerDiv"))
        )

        # Find all practitioner cards
        cards = driver.find_elements(By.CLASS_NAME, "card-inner")

        for card in cards:
            practitioner = {}
            try:
                practitioner["Name"] = card.find_element(By.TAG_NAME, "h4").text
            except:
                practitioner["Name"] = "N/A"

            try:
                practitioner["Email"] = card.find_element(
                    By.CSS_SELECTOR, "a[href^='mailto:']"
                ).text
            except:
                practitioner["Email"] = "N/A"

            try:
                speciality_div = card.find_element(By.CLASS_NAME, "speciality")
                info_paragraphs = speciality_div.find_elements(By.TAG_NAME, "p")

                # Get location from map marker - modified selector
                try:
                    map_marker = card.find_element(
                        By.CSS_SELECTOR, "a[onclick*='callOpenGoogleMap']"
                    )
                    location = map_marker.get_attribute("title")
                    practitioner["Location"] = location
                    print(f"Found location: {location}")  # Debug print
                except Exception as e:
                    print(f"Failed to get location: {e}")  # Debug print
                    practitioner["Location"] = "N/A"

                for p in info_paragraphs:
                    text = p.text
                    if "Business Name:" in text:
                        practitioner["Business Name"] = text.replace(
                            "Business Name:", ""
                        ).strip()
                    elif "Phone:" in text:
                        practitioner["Phone"] = text.replace("Phone:", "").strip()
                    elif "Suburb:" in text:
                        practitioner["Suburb"] = text.replace("Suburb:", "").strip()
                    elif "Website:" in text:
                        practitioner["Website"] = text.replace("Website:", "").strip()
                    elif "Languages:" in text:
                        practitioner["Languages"] = text.replace(
                            "Languages:", ""
                        ).strip()
            except:
                pass

            print(practitioner)
            practitioners.append(practitioner)

    except Exception as e:
        print(f"Error in grab_data: {e}")

    return practitioners


def has_next_page():
    try:
        next_button = driver.find_element(
            By.CLASS_NAME, "mat-paginator-navigation-next"
        )
        is_disabled = next_button.get_attribute(
            "disabled"
        ) == "true" or "disabled" in next_button.get_attribute("class")
        return not is_disabled
    except:
        return False


def click_next_page():
    try:
        next_button = driver.find_element(
            By.CLASS_NAME, "mat-paginator-navigation-next"
        )
        next_button.click()
        time.sleep(2)  # Wait for the new page to load
        return True
    except:
        return False


def start_scraping(suburbs):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for suburb in suburbs:
        print(f"Searching for {suburb}")
        search_location(suburb)
        time.sleep(2)

        suburb_practitioners = []

        while True:
            practitioners = grab_data()  # Grab data from current page
            suburb_practitioners.extend(practitioners)

            if has_next_page():
                click_next_page()
            else:
                print(f"Finished scraping {suburb}")
                break

        # Write suburb data to its own CSV file
        if suburb_practitioners:
            filename = f"practitioners_{suburb}_{timestamp}.csv"
            fieldnames = [
                "Name",
                "Email",
                "Business Name",
                "Phone",
                "Suburb",
                "Website",
                "Languages",
                "Location",
            ]
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(suburb_practitioners)
            print(f"Data for {suburb} saved to {filename}")

        time.sleep(2)


def main():

    # Add new suburbs as needed
    suburbs = ["Sydney"]

    try:
        # Setup the driver with firefox
        setup_driver()
        start_scraping(suburbs)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
