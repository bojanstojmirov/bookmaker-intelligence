from selenium.webdriver.common.by import By
from .utils import init_driver, get_and_sleep, regex_match, append_if_found

class Bet365Scraper:
    def __init__(self):
        self.driver = init_driver()

    def scrape(self):
        about_us_url = "https://help.bet365.com/en/about-us"
        try:
            get_and_sleep(self.driver, about_us_url)

            about_text = self.driver.find_element(By.XPATH, "//div[@class='sa__singleaccordion__section__body']").text

            products, licensing = [], []
            for product in ["Sports", "Casino", "Live Casino", "Poker", "Bingo"]:
                append_if_found(about_text, product, product, products)

            for license_ in ["Government of Gibraltar", "Gibraltar Gambling Commissioner", "UKGC"]:
                append_if_found(about_text, license_, license_, licensing)

            country_hq = "Gibraltar" if "Gibraltar" in about_text else None
            affiliates = "eCOGRA" if "eCOGRA" in about_text else None
            security_certifications = "Thawte SSL Web Server Certificate" if "Thawte SSL" in about_text else None
            customer_base = regex_match(about_text, r"over ([\d,]+) million customers worldwide", " M+")
            num_of_employees = regex_match(about_text, r"employs over ([\d,]+) people", "+")

            return {
                "bookmaker_name": "Bet365",
                "country": country_hq,
                "products": products,
                "licensing": licensing,
                "affiliates": affiliates,
                "customer_base": customer_base,
                "employees": num_of_employees,
                "security_certifications": security_certifications,
                "source_url": about_us_url
            }

        except Exception as e:
            print(f"[SCRAPING FAILED] error for Bet365: {e}")
            return None

        finally:
            self.driver.quit()