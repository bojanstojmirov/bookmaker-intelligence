# Bookmaker Intelligence Mini Project - Bojan Stojmirov

## Overview
Scrapes public data from online bookmakers Bet365 and Betsson then visualizes it via a Streamlit dashboard.

## How It Works
1. **Scraper Scripts**: `scraper/` folder scrapes websites Bet365 and Betsson using Selenium
2. **Database**: Data is stored in SQLite (`bookmakers.db`)
3. **Dashboard**: Run `dashboard.py` using Streamlit

## Setup
- visit **https://sites.google.com/chromium.org/driver/** and download the version that matches your installed version of Google Chrome - unzip the file - place the chromedriver executable inside the **scrapers/** folder in the project
```bash
pip install -r requirements.txt
python run_all.py - // - which runs the two scrapers and saves the scraped data in the DB
streamlit run dashboard.py - // - it will open a browser window at: http://localhost:8501
```

## Data Sources and Assumptions

The information shown in this project is collected using web scraping techniques from the official bookmaker websites:

- [Bet365 - About Us](https://help.bet365.com/en/about-us)
- [Betsson - Corporate Information](https://info.betsson.com/about/en/)

Some assumptions were made:
- Headquarters country was assumed based on context
- Products and services are identified from website public info
- Revenue estimates are approximated from publicly available data
- Licensing information is typically taken from the legal section of the website

## Challenges Encountered

- **Chromedriver Setup**: Automatic download using `webdriver-manager` was not reliable due to mismatched driver versions and unavailable URLs. The final workaround was to manually download the correct version of Chromedriver and place it in the `scrapers/` directory.

- **JavaScript loaded Websites**: Both Bet365 and Betsson use dynamic content loading, which required the use of `Selenium` instead of lightweight solutions like `requests` or `BeautifulSoup`.

- **Data Structures**: Each bookmaker website structures its information differently. This required writing scraper logic specific to each site, including handling differently formatted fields.

- **Data Normalization**: Since fields like `products`, `licensing`, and `revenue` varied in wording and availability, additional parsing and assumptions had to be made to keep the dataset consistent for visualization.
