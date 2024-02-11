from urllib.parse import urljoin
import requests
# import pandas
from bs4 import BeautifulSoup 


url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
modified = '2024-01-19 09:47'

def scrape_site(url, modified):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all the links in the page
    table = soup.find('table')
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        for cell in cells:
            cell_text = cell.get_text().strip()
            # print(cell_text)  # Debug: Print each cell text
            if modified in cell_text:
                a_tag = row.find('a')
                if a_tag:
                    file_url = urljoin(url, a_tag['href'])
                    file_response = requests.get(file_url)
                    filename = file_url.split('/')[-1]
                    with open(filename, 'wb') as f:
                        f.write(file_response.content)
                    print(f"file downloaded: {filename}")
                return



        

def main(url, modified):
    # your code here
    scrape_site(url, modified)


if __name__ == "__main__":
    main(url, modified)
