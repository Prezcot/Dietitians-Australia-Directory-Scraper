# Dietitians Australia Directory Scraper

A web scraping tool designed to extract practitioner information from the Dietitians Australia Find an Accredited Practising Dietitian directory.

## Features

- Scrapes practitioner information including:
  - Name
  - Email
  - Business Name
  - Phone
  - Suburb
  - Website
  - Languages
- Handles pagination automatically
- Exports data to CSV files organized by suburb
- Includes timestamp in filenames for version control

## Prerequisites

- Python 3.7 or higher
- Firefox browser installed
- pip (Python package installer)

## Installation

1. Clone this repository:

```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install required Python packages:

```bash
pip install selenium
```

3. Install Firefox WebDriver:
   - The script uses Firefox WebDriver (geckodriver)
   - Download geckodriver from [Mozilla's GitHub](https://github.com/mozilla/geckodriver/releases)
   - Add the geckodriver to your system's PATH

## Usage

1. Configure suburbs to scrape:
   - Open `dietitian-scraper.py`
   - Modify the `suburbs` list in the `main()` function:

```python
suburbs = ["Sydney", "Melbourne"]  # Add or modify suburbs as needed
```

2. Run the scraper:

```bash
python dietitian-scraper.py
```

3. Output:
   - The script will create separate CSV files for each suburb
   - Files are named in the format: `practitioners_[SUBURB]_[TIMESTAMP].csv`
   - Example: `practitioners_Sydney_20240319_143022.csv`

## How It Works

The scraper:

1. Opens the Dietitians Australia directory website
2. Searches for each suburb in the configured list
3. Extracts practitioner information from each page
4. Automatically navigates through all available pages
5. Saves the data to suburb-specific CSV files

## Error Handling

- The script includes error handling for:
  - Network issues
  - Missing elements
  - Invalid data
  - Pagination errors

## Limitations

- Requires stable internet connection
- May be affected by website changes
- Subject to website's terms of service
- Rate limited by built-in delays to prevent server overload

## Disclaimer

This tool is for educational purposes only. Please ensure you comply with Dietitians Australia's terms of service and data usage policies when using this scraper.
