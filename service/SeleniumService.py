from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import constants.constants as const
import time

class SeleniumService:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = None

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None  # Establece el driver a None después de cerrarlo
    def open(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)

    def get_office_url(self, office_name, url_juzgado):
        print(url_juzgado)
        """Get office url given name of the office and url_juzgado.

        Args:
            officeName (str): Office name.
            url_juzgafo (str): juzgado url.

        Returns:
            str: url of the office.
        """
        print("Inicio de SeleniumService")
        self.open()
        words_list = office_name.split()
        city = words_list[-1]

        self.driver.get(url_juzgado)

        links = self.driver.find_elements(By.TAG_NAME, "a")

        for link in links:
            text = link.text
            if city.lower() in text.lower():
                link.click()
                break

        time.sleep(3)

        value_despacho = words_list[1]

        links = self.driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            text = link.text
            href = link.get_attribute("href")
            if value_despacho.lower() in text.lower():
                self.close()
                return href
        self.close()
        return None
    
    def get_regions_and_subregions(self):
        self.open()
        self.driver.get(const.URL_RAMA_JUDICIAL)

        links = self.driver.find_elements(By.TAG_NAME, "a")

        for link in links:
            text = link.text
            print(text)
