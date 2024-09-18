import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time
import os
import logging
from logging.handlers import RotatingFileHandler

# Set up logging
def setup_logging():
    logger = logging.getLogger('scraper')
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler (rotating log files, max 5MB each, keep 5 backup files)
    file_handler = RotatingFileHandler('scraper.log', maxBytes=5*1024*1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

def scrape_portman_park_results():
    url = "https://www.betvirtual.co/portman-park-results"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.select_one('body > section.content-page-center > div > div > div.col-md-8')
        
        if content_div:
            results = []
            for element in content_div.children:
                if element.name == 'h3':
                    current_race = {'title': element.text.strip(), 'id': element.get('id')}
                elif element.name == 'p' and 'text-muted' in element.get('class', []):
                    current_race['info'] = element.text.strip()
                elif element.name == 'div' and 'table-responsive' in element.get('class', []):
                    table = element.find('table', class_='results-table')
                    if table:
                        current_race['results'] = parse_table(table)[:3]  # Only keep top 3 finishers
                        results.append(current_race)
                        current_race = {}
            
            logger.info(f"Successfully scraped {len(results)} races")
            return results
        else:
            logger.error("Failed to find content div in the scraped page")
    except requests.RequestException as e:
        logger.error(f"Failed to retrieve the page: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while scraping: {str(e)}")
    return None

def parse_table(table):
    results = []
    try:
        for row in table.find_all('tr')[1:4]:  # Only parse first 3 rows after header
            columns = row.find_all('td')
            if len(columns) == 4:
                position = columns[0].find('img')['src'].split('-')[-1].split('.')[0]
                runner_info = columns[1].text.strip()
                runner_name = re.search(r'(.*) \((\d+)\)', runner_info)
                odds = columns[3].text.strip()
                
                results.append({
                    'position': position,
                    'runner_name': runner_name.group(1) if runner_name else runner_info,
                    'runner_number': runner_name.group(2) if runner_name else '',
                    'odds': odds
                })
        logger.debug(f"Parsed {len(results)} runners from table")
    except Exception as e:
        logger.error(f"Error parsing table: {str(e)}")
    return results

def save_to_json(data):
    filename = "portman_park_results.json"
    try:
        # Load existing data if file exists
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = {}
        
        # Add new data with timestamp as key
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        existing_data[timestamp] = data
        
        # Save updated data
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving results to JSON: {str(e)}")

def main():
    logger.info("Starting scraper")
    while True:
        try:
            logger.info(f"Initiating scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            results = scrape_portman_park_results()
            if results:
                save_to_json(results)
            else:
                logger.warning("No results to save from this scrape")
            
            # Wait for 10 minutes
            logger.info("Waiting for 10 minutes before next scrape")
            time.sleep(10 * 60)
        except KeyboardInterrupt:
            logger.info("Scraper stopped by user")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred in the main loop: {str(e)}")
            logger.info("Waiting for 1 minute before retrying")
            time.sleep(60)  # Wait for 1 minute before retrying in case of unexpected errors

if __name__ == "__main__":
    main()