import os, time, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class Bet365Scraper:
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
        about_us_url = "https://help.bet365.com/en/about-us"
        try:
            self.driver.get(about_us_url)
            time.sleep(5)

            about_text = self.driver.find_element(By.XPATH, "//div[@class='sa__singleaccordion__section__body']").text

            products = []
            if "Sports" in about_text:
                products.append("Sports")
            if "Casino" in about_text:
                products.append("Casino")
            if "Live Casino" in about_text:
                products.append("Live Casino")
            if "Poker" in about_text:
                products.append("Poker")
            if "Bingo" in about_text:
                products.append("Bingo")
            
            if "Gibraltar" in about_text:
                country_hq = "Gibraltar"

            licensing = []
            if "Government of Gibraltar" in about_text:
                licensing.append("Government of Gibraltar")
            if "Gibraltar Gambling Commissioner" in about_text:
                licensing.append("Gibraltar Gambling Commissioner")
            if "UK Gambling Commission" in about_text or "UKGC" in about_text:
                licensing.append("UKGC")

            if "eCOGRA" in about_text:
                affiliates ="eCOGRA"
            
            if "Thawte SSL" in about_text:
                security_certifications = "Thawte SSL Web Server Certificate"

            match = re.search(r"employs over ([\d,]+) people", about_text)
            if match:
                num_of_employees = match.group(1) + '+'
            
            match = re.search(r"over ([\d,]+) million customers worldwide", about_text)
            if match:
                customer_base = match.group(1) + ' M+'

            data = {
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

            return data

        except Exception as e:
            print(f"[SCRAPING FAILED] error for Bet365: {e}")
            return None

        finally:
            self.driver.quit()
