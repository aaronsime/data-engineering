from urllib.parse import urljoin
import requests
import pandas
from bs4 import BeautifulSoup 


url = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
modified = '2024-01-19 09:47'

def scrape_site(url, modified):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the table on the page
    table = soup.find('table')
    for row in table.find_all('tr'):
        # Find all the rows
        cells = row.find_all('td')
        for cell in cells:
            cell_text = cell.get_text().strip()
            # Find the row that contains the modified variable
            if modified in cell_text:
                a_tag = row.find('a')
                # Download the href csv file
                if a_tag:
                    file_url = urljoin(url, a_tag['href'])
                    file_response = requests.get(file_url)
                    filename = file_url.split('/')[-1]
                    with open(filename, 'wb') as f:
                        f.write(file_response.content)
                    print(f"file downloaded: {filename}")
                return filename

def open_in_pandas(filename):
    df = pandas.read_csv(filename)
    filtered_df = df[df.HourlyDryBulbTemperature == df.HourlyDryBulbTemperature.max()]
    return filtered_df


def main(url, modified):

    filename = scrape_site(url, modified)
    open_in_pandas(filename)
    print(open_in_pandas(filename).head())

# TOD
# Add error handling and change to a specific working directory

if __name__ == "__main__":
    main(url, modified)
