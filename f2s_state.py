import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# Function to scrape table data
def scrape_table(blood_group, city, state, district, pin):
    try:
        donor_table = driver.find_element(By.ID, "dgBloodDonorResults")
        rows = donor_table.find_elements(By.XPATH, ".//tr")[2:]  # Skip header rows

        data = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 4:
                name = cols[0].text.strip()
                availability = cols[1].text.strip()
                mobile_no = cols[2].text.strip()

                data.append({
                    "Blood Group": blood_group,
                    "City": city,
                    "State": state,
                    "District": district,
                    "Pin": pin,
                    "Name": name,
                    "Availability": availability,
                    "Mobile No.": mobile_no
                })
        return data
    except Exception as e:
        print(f"Error while scraping table: {e}")
        return []


# Function to save data to CSV incrementally
def save_to_csv_incrementally(data, filename):
    if not data:  # Check if data is empty
        return
    keys = data[0].keys()
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        if file.tell() == 0:  # Check if file is empty
            writer.writeheader()
        writer.writerows(data)


# Function to handle pagination via links
def scrape_all_pages(blood_group, city, state, district, pin, csv_filename):
    all_data = []
    while True:
        # Scrape the current page
        data = scrape_table(blood_group, city, state, district, pin)
        all_data.extend(data)
        save_to_csv_incrementally(data, csv_filename)

        # Get pagination links
        try:
            pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
            links = pagination.find_elements(By.TAG_NAME, "a")
            link_texts = [link.text for link in links if link.text.isdigit()]  # Filter only digit links
        except Exception:
            break  # No pagination available

        # Extract and click each page link
        for page in link_texts:
            try:
                # Re-locate the pagination element (as DOM may have refreshed)
                pagination = driver.find_element(By.XPATH, "//td[@colspan='4']")
                link = pagination.find_element(By.LINK_TEXT, page)
                link.click()
                time.sleep(3)  # Wait for page to load

                # Scrape the current page after clicking
                data = scrape_table(blood_group, city, state, district, pin)
                all_data.extend(data)
                save_to_csv_incrementally(data, csv_filename)
            except Exception as e:
                print(f"Error navigating pagination: {e}")

        break  # Exit once all links have been clicked

    return all_data


# Main execution block
try:
    # Set up Selenium WebDriver
    driver = webdriver.Firefox()
    url = "https://www.friends2support.org/inner/news/searchresult.aspx"
    driver.get(url)
    time.sleep(5)

    # Define blood groups to search for
    blood_groups = ["B+","A+", "A-", "B-", "O+", "O-", "AB+", "AB-"]

    # First select a blood group (required for the website to work properly)
    blood_group_dropdown = Select(driver.find_element(By.ID, "dpBloodGroup"))
    blood_group_dropdown.select_by_visible_text(blood_groups[0])
    time.sleep(2)

    # Select "INDIA" as the country
    country_dropdown = Select(driver.find_element(By.ID, "dpCountry"))
    country_dropdown.select_by_visible_text("INDIA")
    time.sleep(2)

    # Let user select the state
    print("Please select the desired state from the dropdown.")
    state_dropdown = Select(driver.find_element(By.ID, "dpState"))
    time.sleep(5)  # Wait for the user to make the selection

    # Capture the selected state
    state = state_dropdown.first_selected_option.text

    # Create directory for state if it doesn't exist
    state_dir = state.replace(" ", "_")
    if not os.path.exists(state_dir):
        os.makedirs(state_dir)

    # Get all districts in the selected state
    district_dropdown = Select(driver.find_element(By.ID, "dpDistrict"))
    districts = [option.text for option in district_dropdown.options if option.text != "ALL"]

    for district in districts:
        # Select district
        district_dropdown = Select(driver.find_element(By.ID, "dpDistrict"))
        district_dropdown.select_by_visible_text(district)
        time.sleep(2)

        # Get all cities in the current district
        city_dropdown = Select(driver.find_element(By.ID, "dpCity"))
        cities = [option.text for option in city_dropdown.options if option.text != "ALL"]

        # Generate CSV filename for this district
        csv_filename = os.path.join(state_dir, f"{district}_blood_donors.csv".replace(" ", "_"))

        for blood_group in blood_groups:
            blood_group_dropdown = Select(driver.find_element(By.ID, "dpBloodGroup"))
            blood_group_dropdown.select_by_visible_text(blood_group)
            time.sleep(2)

            for city in cities:
                city_dropdown = Select(driver.find_element(By.ID, "dpCity"))
                city_dropdown.select_by_visible_text(city)
                time.sleep(2)

                driver.find_element(By.ID, "btnSearchDonor").click()
                time.sleep(5)

                scrape_all_pages(blood_group, city, state, district, "", csv_filename)

        print(f"Data for {district} saved to {csv_filename}")

    print(f"All data saved in {state_dir} directory")

finally:
    driver.quit()
