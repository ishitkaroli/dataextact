import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pytesseract
from PIL import Image
import time
import csv
import re

def google_search(query):
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a', href=True)
        
        if title and link:
            results.append({
                'title': title.text,
                'link': link['href'],
            })
    return results

def google_search_with_selenium(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Path to your unpacked extension or the .crx file
    extension_path = '/Users/ishitkaroli/Library/Application Support/Google/Chrome/Default/Extensions/bbdhfoclddncoaomddgkaaphcnddbpdh/0.1.0_0/'
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://www.google.com")
        search_box = driver.find_element("name", "q")
        search_box.send_keys(query + Keys.RETURN)

        time.sleep(5)

        results = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for g in soup.find_all('div', class_='g'):
            title = g.find('h3')
            link = g.find('a', href=True)

            if title and link:
                results.append({
                    'title': title.text,
                    'link': link['href'],
                })
        return results

    finally:
        driver.quit()

def handle_google_sorry_page(driver):
    try:
        # Check if the "Sorry" page is displayed
        if "sorry" in driver.current_url:
            print("Detected Google 'Sorry' page. Attempting to resolve CAPTCHA...")
            time.sleep(5)  # Wait for the page to load
            
            # Locate the checkbox element for CAPTCHA
            checkbox = driver.find_element(By.CSS_SELECTOR, 'div[role="checkbox"]')
            if checkbox:
                checkbox.click()  # Click the checkbox
                print("Clicked the 'I'm not a robot' checkbox. Please complete the CAPTCHA if necessary.")
                time.sleep(5)  # Wait for the user to complete the CAPTCHA
            
    except Exception as e:
        print("Error while handling the 'Sorry' page:", e)

def scroll_and_check(driver):
    scroll_pause_time = 2
    scroll_height = 500
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")
        time.sleep(scroll_pause_time)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        contact_section = soup.find(string="Email ID")
        if contact_section:
            parent_div = contact_section.find_parent("div")
            if parent_div:
                email = parent_div.find(string=lambda text: text and "@" in text)
                address = parent_div.get_text(separator="\n").strip()
                
                print("Email:", email)
                print("Address:", address)
                return email

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def take_screenshot_and_extract(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    try:
        driver.get(url)
        print("The browser has opened. Please complete the CAPTCHA verification if needed.")
        handle_google_sorry_page(driver)  # Handle the "Sorry" page if encountered
        
        time.sleep(15)  # Wait for the user to complete verification if needed
        
        email = scroll_and_check(driver)
        driver.save_screenshot("screenshot.png")
        
        return email
        
    finally:
        driver.quit()

def ocr_from_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    print("Extracted Text from Image:")
    print(extracted_text)
    return extracted_text

def extract_name_and_email(text):
    company_name = None
    email = None
    
    for line in text.splitlines():
        if "Current status of" in line:
            company_name = line.split("Current status of ")[-1].split(" is")[0]
        
        email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', line)
        if email_match:
            email = email_match.group()

    return company_name, email

def save_to_csv(company_name, email, csv_file_path="Mca.csv"):
    with open(csv_file_path, mode='a', newline='') as file:  # Append mode
        writer = csv.writer(file)
        writer.writerow([company_name, email])
    print(f"Data for {company_name} saved to {csv_file_path}")

def get_cins_from_csv(file_path):
    cin_list = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if there is one
        for row in reader:
            if row:  # Check if the row is not empty
                cin_list.append(row[0].strip())  # Get the first column
    return cin_list

def main():
    cin_list = get_cins_from_csv("MCA-Company.csv")

    for cin in cin_list:
        query = f"company information for {cin}"
        
        results = google_search_with_selenium(query)

        for result in results:
            if 'zaubacorp.com' in result['link']:
                email = take_screenshot_and_extract(result['link'])
                time.sleep(5)
                extracted_text = ocr_from_image("screenshot.png")
                company_name, extracted_email = extract_name_and_email(extracted_text)
                
                if extracted_email:
                    email = extracted_email
                
                if company_name and email:
                    save_to_csv(company_name, email)
                else:
                    print(f"Could not find the required information for {cin}.")
                break

if __name__ == "__main__":
    main()
