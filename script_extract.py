from bs4 import BeautifulSoup
import csv

# Function to read HTML from a file and append all href links to a CSV file
def fetch_and_append_all_links(html_file_path, csv_file_path):
    try:
        # Read the HTML content from the file
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all <a> tags and extract href links
        links = []
        a_tags = soup.find_all('a')
        for tag in a_tags:
            if 'href' in tag.attrs:
                links.append(tag['href'])
        
        # Append new links to the existing CSV file
        with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for link in links:
                writer.writerow([link])  # Append each new link
        
        print(f"New links successfully appended to: {csv_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the HTML file (raw HTML saved from the webpage)
html_file_path = './connect.html'  # Adjust this path if needed

# Path to append the CSV file
csv_file_path = '/Users/ishitkaroli/Desktop/Test/all_links2.csv'

# Call the function
fetch_and_append_all_links(html_file_path, csv_file_path)


# last fetched https://www.startinup.up.gov.in/crm/welcome/connect_network/12