import os, time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class BetssonScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        chrome_driver_path = os.path.join(current_dir, "chromedriver")

        self.driver = webdriver.Chrome(
            service=Service(chrome_driver_path),
            options=options
        )

    def scrape(self):
        about_us_url = "https://info.betsson.com/about/en/"
        try:
            self.driver.get(about_us_url)
            time.sleep(5)

            about_text = self.driver.find_element(By.XPATH, "//h2[contains(., 'COMPANY INFORMATION')]/parent::span/parent::div/following-sibling::div/following-sibling::div/p").text
            hq_text = self.driver.find_element(By.XPATH, "//h2[contains(., 'BML Group')]/parent::span/parent::div/following-sibling::div/following-sibling::div/p/b").text
            licenses_url = self.driver.find_element(By.XPATH, "//h3[contains(., 'Licenses and Security')]/following-sibling::p/following-sibling::div/a").get_attribute('href')
            investors_url = self.driver.find_element(By.XPATH, "//h3[contains(., 'Investor Relations')]/following-sibling::p/following-sibling::div/a").get_attribute('href')

            products = []
            if "sportsbook" in about_text:
                products.append("Sportsbook betting")
            if "casino" in about_text:
                products.append("Casino")
            if "poker" in about_text:
                products.append("Poker")
            if "bingo" in about_text:
                products.append("Bingo")
            if "scratch tickets" in about_text:
                products.append("Scratch tickets")

            if "Malta" in hq_text:
                country_hq = "Malta"
            
            self.driver.get(licenses_url)
            time.sleep(5)
            licensing_text = self.driver.find_element(By.XPATH, "//p[contains(., 'holds a license issued by')]").text

            licensing = []
            if "MGA" in licensing_text or "Malta Gaming Authority" in licensing_text:
                licensing.append("Malta Gaming Authority")
            if "UK Gambling Commission" in licensing_text or "UKGC" in licensing_text:
                licensing.append("UKGC")

            match = re.search(r"licen[cs]e\s+([A-Z]+\/[A-Z]+\/\d+\/\d+) issued by", licensing_text)
            if match:
                license_code = match.group(1)
                licensing.append(license_code)

            self.driver.get(investors_url)
            time.sleep(5)

            stats_box = self.driver.find_element(By.XPATH, "//div[contains(., 'About us')]/parent::div/parent::div/parent::div/following-sibling::div/div/div")
            revenue_estimate = stats_box.find_element(By.XPATH, ".//div/div/div").text + " MEUR REVENUE 2024"
            customer_base = stats_box.find_element(By.XPATH, ".//div/following-sibling::div/div/div").text + " ACTIVE CUSTOMERS Q4 2024"

            data = {
                "bookmaker_name": "Betsson",
                "country": country_hq,
                "products": products,
                "licensing": licensing,
                "customer_base": customer_base,
                "revenue_estimate": revenue_estimate,
                "source_url": about_us_url,
            }

            return data

        except Exception as e:
            print(f"[SCRAPING FAILED] error for Bet365: {e}")
            return None

        finally:
            self.driver.quit()
