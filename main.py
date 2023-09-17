import requests
from bs4 import BeautifulSoup
import csv

# Function to extract data from an advisory page
def extract_advisory_data(advisory_url):
    advisory_response = requests.get(advisory_url)
    advisory_soup = BeautifulSoup(advisory_response.text, 'html.parser')
    
    # First extraction method (default)
    title_elem = advisory_soup.find('h4', class_='level-heading')
    impact_severity_elem = advisory_soup.find('span', class_='level')
    description_elem = advisory_soup.find('h5', text='Description')
    reporter_elem = advisory_soup.find('dt', text='Reporter')
    references_elem = advisory_soup.find_all('h5', text='References')
    
    title = title_elem.text.strip() if title_elem else 'N/A'
    impact_severity = impact_severity_elem.text.strip() if impact_severity_elem else 'N/A'
    description = description_elem.find_next('p').text.strip() if description_elem else 'N/A'
    reporter = reporter_elem.find_next('dd').text.strip() if reporter_elem else 'N/A'
    references = [ref.find_next('a')['href'] for ref in references_elem] if references_elem else 'N/A'

# Main function to scrape and save data
def scrape_and_save_data():
    base_url = 'https://www.mozilla.org/en-US/security/advisories/'
    csv_file = 'mozilla_security_advisories.csv'

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['date', 'title', 'impact/severity', 'description', 'references', 'reporter'])

        while True:
            main_response = requests.get(base_url)
            main_soup = BeautifulSoup(main_response.text, 'html.parser')

            for date_elem in main_soup.find_all('h2'):
                date = date_elem.text.strip()

                if date == 'January 21, 2005':
                    return

                advisory_links = date_elem.find_next('ul').find_all('a')

                for advisory_link in advisory_links:
                    advisory_url = 'https://www.mozilla.org' + advisory_link['href']
                    advisory_data = extract_advisory_data(advisory_url)
                    csv_writer.writerow([date] + advisory_data)

            # Find the link to the next page
            next_page_link = main_soup.find('a', class_='pagination__next')
            if next_page_link:
                base_url = 'https://www.mozilla.org' + next_page_link['href']
            else:
                break

if __name__ == '__main__':
    scrape_and_save_data()
