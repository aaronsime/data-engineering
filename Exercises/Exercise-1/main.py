import requests
import os 
from os import remove
import zipfile
from concurrent.futures import ThreadPoolExecutor

# List of ZIP file URLs
download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

# Directory for downloads
downloads_dir = r'C:\Users\iron_\Desktop\repos\data-engineering-practice\Exercises\Exercise-1\Downloads'  # Relative path; adjust as needed

def ensure_directory_exists(directory):
    # Ensure the specified directory exists.
    os.makedirs(directory, exist_ok=True)
    print(f"Directory ensured: {directory}")

def download_zip(url, save_dir):
    # Download a ZIP file from a URL to the specified save directory.
    try:
        filename = url.split('/')[-1]
        output_path = os.path.join(save_dir, filename)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"File successfully downloaded and saved as {output_path}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

def download_files_concurrently(urls, save_dir):
    # Download files concurrently to the specified directory
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_zip, url, save_dir) for url in urls]
        for future in futures:
            future.result()

def unzip_files(downloads_dir):
    # UnZip downloaded files and delete the zip files.
    for filename in os.listdir(downloads_dir):
        file_path = os.path.join(downloads_dir, filename)
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(downloads_dir)
                print(f"Extracted contents of {filename}")
            remove(file_path)
    print(f"Finished extracting all .ZIP files from '{downloads_dir}'")


def main(download_uris, downloads_dir):
    # Ensure the download directory exists
    ensure_directory_exists(downloads_dir)
    
    # Download files concurrently
    download_files_concurrently(download_uris, downloads_dir)

    # unzipfiles and delete zip files are extraction
    unzip_files(downloads_dir)

if __name__ == "__main__":
    main(download_uris, downloads_dir)
