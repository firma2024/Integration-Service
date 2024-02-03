from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from service.WebScraperService import WebScraperService
import constants.constants as const
from utils.utils import split_list

from typing import List
import time
import queue
import pandas as pd
import threading
from fastapi import HTTPException


class SeleniumService:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.driver = None
        self.df = pd.read_csv('Data/offices.csv')
        self.lock = threading.Lock()

    def close(self):
        """Close instance of driver Chrome.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None  # Establece el driver a None después de cerrarlo

    def open(self):
        """Create instance of Chrome.
        """
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.chrome_options)

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

    def get_office_url_df(self, office_name):
        with self.lock:
            res = self.df[self.df["Nombre_despacho"] == office_name]
            if res.empty:
                raise HTTPException(
                    status_code=404, detail="Juzgado no encontrado")
            return res["Link_Despacho"].iloc[0]

    async def get_offices(self):
        """Get office links from page interactions using selenium.
        """
        web_scraper_service = WebScraperService()

        dict_offices = web_scraper_service.get_court_offices()
        list_offices = [value for value in dict_offices.values()]

        num_threads = 1
        # Split the list into the number of threads to be used to update the df
        for office in split_list(list_offices, num_threads):
            # Get name of the office and url of the sub-offices
            t = ScrapeThread(office, self.df, self.lock)
            t.start()


class ScrapeThread(threading.Thread):
    def __init__(self, list_offices, df, lock):
        threading.Thread.__init__(self)
        self.list_offices = list_offices
        self.df = df
        self.lock = lock
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')

    def run(self):
        """Update dataframe while checking for duplicates and delete them.
        """
        # Create chrome driver instance
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.chrome_options)
        for office in self.list_offices:
            # Iterate in the list of urls and get the name of the office
            self.driver.get(office)
            # Get city list
            div_principales_mapa = self.driver.find_element(
                By.CLASS_NAME, 'principalesMapa')
            lista_items = div_principales_mapa.find_elements(By.TAG_NAME, 'li')
            for item in lista_items:
                item.click()
                time.sleep(3)
                # Obtain name of the city
                ciudad_mapa = self.driver.find_element(By.ID, 'titleD')

                div = self.driver.find_element(By.ID, 'selected')
                lista_items = div.find_elements(By.TAG_NAME, 'li')
                for li in lista_items:
                    a_tag = li.find_elements(By.TAG_NAME, 'a')
                    with self.lock:
                        self.df = pd.concat([self.df, pd.DataFrame(
                            {"Ciudad_Mapa": [ciudad_mapa.text], "Nombre_despacho": [
                                a_tag[0].text], "Link_Despacho": [a_tag[0].get_attribute("href")]}
                        )], ignore_index=True)
                        self.df.drop_duplicates()
                go_back = self.driver.find_element(By.ID, 'atras')
                go_back.click()
                time.sleep(3)
        self.driver.close()
