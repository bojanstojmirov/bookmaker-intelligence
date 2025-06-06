from scrapers.bet365_scraper import Bet365Scraper
from scrapers.betsson_scraper import BetssonScraper
from data.database import create_table, insert_bookmaker

def main():
    create_table()

    print("[RUNNING] Bet365 Scraper!")
    bet365_data = Bet365Scraper().scrape()
    if bet365_data:
        insert_bookmaker(bet365_data)
        print("Bet365 data saved to DB\n")

    print("[RUNNING] Betsson Scraper!")
    betsson_data = BetssonScraper().scrape()
    if betsson_data:
        insert_bookmaker(betsson_data)
        print("Betsson data saved to DB\n")

if __name__ == "__main__":
    main()
