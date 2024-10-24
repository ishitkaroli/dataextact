import os
import subprocess
import urllib.request
import zipfile

def download_and_extract(url, extract_to='.'):
    filename = url.split('/')[-1]
    
    # Download the file
    urllib.request.urlretrieve(url, filename)

    # Check file type and extract
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    
    # Remove the downloaded file after extraction
    os.remove(filename)

def install_package(package_name, url):
    print(f"Downloading and installing {package_name}...")
    download_and_extract(url)

    # Change directory to the extracted package
    extracted_dir = package_name  # Adjust this if necessary based on the package structure
    os.chdir(extracted_dir)
    
    # Run the setup.py script to install the package
    subprocess.check_call([os.sys.executable, 'setup.py', 'install'])

    # Change back to the original directory
    os.chdir('..')

def main():
    # Define package names and their respective download URLs
    packages = {
        "requests": "https://github.com/psf/requests/archive/refs/tags/v2.28.1.zip",
        "beautifulsoup4": "https://github.com/wention/BeautifulSoup4/archive/refs/tags/4.10.0.zip",
        "selenium": "https://github.com/SeleniumHQ/selenium/archive/refs/tags/4.21.0.zip",
        "webdriver-manager": "https://github.com/SergeyPirogov/webdriver_manager/archive/refs/tags/3.8.6.zip",
        "Pillow": "https://github.com/python-pillow/Pillow/archive/refs/tags/10.0.0.zip",
        "pytesseract": "https://github.com/madmaze/pytesseract/archive/refs/tags/0.3.8.zip",
    }

    # Install each package
    for package_name, url in packages.items():
        install_package(package_name, url)

    print("All packages have been installed.")

if __name__ == "__main__":
    main()
