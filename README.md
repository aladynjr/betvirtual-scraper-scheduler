
# BetVirtual Scraper Scheduler

This project is a Python-based web scraper designed to collect race results from BetVirtual's Portman Park virtual horse racing site. It runs on a 10-minute schedule, continuously updating a JSON file with the latest results.

**Note:** This scraper was custom-made for a specific client's needs. You may need to adjust it to fit your particular requirements.

## Features

- Scrapes Portman Park race results every 10 minutes
- Stores data for the top 3 finishers of each race in a single, continuously updated JSON file
- Implements robust error handling and comprehensive logging
- Uses rotating log files to manage log size

## Requirements

- Python 3.7+
- requests
- beautifulsoup4

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/betvirtual-scraper-scheduler.git
   cd betvirtual-scraper-scheduler
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scraper:
```bash
python main.py
```

The script will run continuously, scraping data every 10 minutes. To stop it, use Ctrl+C.

## Output

- **`portman_park_results.json`**: Contains the top 3 finishers for all scraped races, updated every 10 minutes.
- **`scraper.log`**: Log file containing information about the scraper's operation, errors, etc.

### **Example JSON Output**

The output is stored in `portman_park_results.json` and structured like the following:

```json
{
  "20230912_120530": [
    {
      "title": "12:05 - PORTMAN PARK, MAIDEN STAKES",
      "id": "1205",
      "info": "11:52 • R65 • Today",
      "results": [
        {
          "position": "1",
          "runner_name": "MISS SANE",
          "runner_number": "10",
          "odds": "9/2"
        },
        {
          "position": "2",
          "runner_name": "QUICK TUNE",
          "runner_number": "1",
          "odds": "5/1"
        },
        {
          "position": "3",
          "runner_name": "LOVE INTEREST",
          "runner_number": "8",
          "odds": "3/1"
        }
      ]
    }
  ]
}
```

For **a complete and detailed example** of the JSON output structure, please refer to the following link:  
👉 **[Full JSON Data Example](https://api.npoint.io/8ec9769eddfeb6aefbc3)**

Each key in the JSON object represents a timestamp of when the data was scraped, containing an array of race results from that scrape.

## Notes

- Ensure you comply with BetVirtual's terms of service and robots.txt file before deploying.
- The script uses rotating log files, keeping the last 5 log files of 5MB each.
- As this was custom-built for a specific use case, you might need to modify the code to suit your particular needs.

## License

[MIT License](LICENSE)

