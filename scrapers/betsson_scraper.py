from selenium.webdriver.common.by import By
from .utils import init_driver, get_and_sleep, regex_match, append_if_found

class BetssonScraper:
    def __init__(self):
        self.driver = init_driver()

    def scrape(self):
        about_us_url = "https://info.betsson.com/about/en/"
        try:
            get_and_sleep(self.driver, about_us_url)

            about_text = self.driver.find_element(By.XPATH, "//h2[contains(., 'COMPANY INFORMATION')]/parent::span/parent::div/following-sibling::div/following-sibling::div/p").text
            hq_text = self.driver.find_element(By.XPATH, "//h2[contains(., 'BML Group')]/parent::span/parent::div/following-sibling::div/following-sibling::div/p/b").text
            licenses_url = self.driver.find_element(By.XPATH, "//h3[contains(., 'Licenses and Security')]/following-sibling::p/following-sibling::div/a").get_attribute('href')
            investors_url = self.driver.find_element(By.XPATH, "//h3[contains(., 'Investor Relations')]/following-sibling::p/following-sibling::div/a").get_attribute('href')

            products = []
            for product in ["sportsbook", "casino", "poker", "bingo", "scratch tickets"]:
                append_if_found(about_text, product, product, products)

            country_hq = "Malta" if "Malta" in hq_text else None
            
            get_and_sleep(self.driver, licenses_url)
            licensing_text = self.driver.find_element(By.XPATH, "//p[contains(., 'holds a license issued by')]").text

            licensing = []
            for license_ in ["MGA", "Malta Gaming Authority", "UK Gambling Commission", "UKGC"]:
                append_if_found(licensing_text, license_, license_, licensing)

            license_code = regex_match(licensing_text, r"employs over ([\d,]+) people", "+")
            if license_code:
                licensing.append(license_code)

            get_and_sleep(self.driver, investors_url)

            stats_box = self.driver.find_element(By.XPATH, "//div[contains(., 'About us')]/parent::div/parent::div/parent::div/following-sibling::div/div/div")
            revenue_estimate = stats_box.find_element(By.XPATH, ".//div/div/div").text + " MEUR REVENUE 2024"
            customer_base = stats_box.find_element(By.XPATH, ".//div/following-sibling::div/div/div").text + " ACTIVE CUSTOMERS Q4 2024"

            return {
                "bookmaker_name": "Betsson",
                "country": country_hq,
                "products": products,
                "licensing": licensing,
                "customer_base": customer_base,
                "revenue_estimate": revenue_estimate,
                "source_url": about_us_url,
            }

        except Exception as e:
            print(f"[SCRAPING FAILED] error for Bet365: {e}")
            return None

        finally:
            self.driver.quit()