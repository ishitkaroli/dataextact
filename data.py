import csv
import requests
from bs4 import BeautifulSoup

# Function to fetch raw HTML from a URL
def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve {url} (Status Code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to parse the HTML and extract name, email, and phone
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract name
    name_tag = soup.find('h3', class_='card-title')
    name = name_tag.get_text(strip=True) if name_tag else 'N/A'
    
    # Extract email
    email = 'N/A'
    for p_tag in soup.find_all('p', class_='card-text mb-1'):
        if '@' in p_tag.get_text(strip=True):
            email = p_tag.get_text(strip=True)
            break  # Found the email, exit the loop
    
    # Extract phone
    phone = 'N/A'
    for p_tag in soup.find_all('p', class_='card-text mb-1'):
        if '+91' in p_tag.get_text(strip=True):
            phone = p_tag.get_text(strip=True)
            break  # Found the phone, exit the loop
    
    return name, email, phone

# Read the CSV file and filter relevant URLs
def read_csv_and_extract_links(csv_file):
    links = []
    with open(csv_file, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0].startswith('https://www.startinup.up.gov.in/crm/Welcome/startup_user_details/'):
                links.append(row[0])
    return links

# Write the extracted data to a CSV file
def write_to_csv(data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Startup Name', 'Email', 'Phone'])
        writer.writerows(data)

# Main function to orchestrate the process
def main(input_csv, output_csv):
    links = read_csv_and_extract_links(input_csv)
    scraped_data = []
    
    for link in links:
        print(f"Processing: {link}")
        html = fetch_html(link)
        if html:
            name, email, phone = parse_html(html)
            scraped_data.append([name, email, phone])
    
    write_to_csv(scraped_data, output_csv)
    print(f"Data saved to {output_csv}")

# Input and output file paths
input_csv = '/Users/ishitkaroli/Desktop/Test/all_links.csv'
output_csv = 'output_data.csv'

if __name__ == "__main__":
    main(input_csv, output_csv)
