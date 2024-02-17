from utils.utils import split_list, clean_string

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from typing import Dict
import constants.constants as const
import time
import pandas as pd
import threading
from fastapi import HTTPException
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
import json


class SeleniumService:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )
        self.driver = None
        self.df = pd.read_csv("Data/offices.csv")
        self.lock = threading.Lock()

    def close(self):
        """Close instance of driver Chrome."""
        if self.driver:
            self.driver.quit()
            self.driver = None  # Establece el driver a None después de cerrarlo

    def open(self):
        """Create instance of Chrome."""
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options,
        )

    def get_office_url_df(self, office_name):
        office_name = clean_string(office_name)
        with self.lock:
            res = self.df[self.df["Nombre_despacho"] == office_name]
            if res.empty:
                raise HTTPException(status_code=404, detail="Juzgado no encontrado")
            return res["Link_Despacho"].iloc[0]

    async def get_offices(self):
        """Get office links from page interactions using selenium."""
        web_scraper_service = BeatifulSoupService()

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
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

    def run(self):
        """Update dataframe while checking for duplicates and delete them."""
        # Create chrome driver instance
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options,
        )
        for office in self.list_offices:
            # Iterate in the list of urls and get the name of the office
            self.driver.get(office)
            # Get city list
            principal_div_map = self.driver.find_element(
                By.CLASS_NAME, "principalesMapa"
            )
            item_list = principal_div_map.find_elements(By.TAG_NAME, "li")
            for item in item_list:
                item.click()
                time.sleep(3)
                # Obtain name of the city
                city_map = self.driver.find_element(By.ID, "titleD")

                div = self.driver.find_element(By.ID, "selected")
                item_list = div.find_elements(By.TAG_NAME, "li")
                for li in item_list:
                    a_tag = li.find_elements(By.TAG_NAME, "a")
                    with self.lock:
                        self.df = pd.concat(
                            [
                                self.df,
                                pd.DataFrame(
                                    {
                                        "Ciudad_Mapa": [city_map.text],
                                        "Nombre_despacho": [a_tag[0].text],
                                        "Link_Despacho": [
                                            a_tag[0].get_attribute("href")
                                        ],
                                    }
                                ),
                            ],
                            ignore_index=True,
                        )
                        self.df.drop_duplicates()
                go_back = self.driver.find_element(By.ID, "atras")
                go_back.click()
                time.sleep(3)
        self.driver.close()


class BeatifulSoupService:

    def get_url_estados(self, url_despacho: str):
        """Get url of the electronic documents.

        Args:
            url_despacho (str): Office url.

        Returns:
            str: Url of electronic documents.
        """
        print("Inicio de búsqueda de enlace de estados")

        print(url_despacho)
        response = requests.get(url_despacho, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")

        year = str(datetime.now().year)

        h4_tags = soup.find_all('h4', text='Estados Electrónicos')
        next_div = h4_tags[0].find_next_sibling('div')
        a_tags = next_div.find_all('a')
        for a_tag in a_tags:
            if year in a_tag.text:
                return const.URL_RAMA_JUDICIAL_INICIO + a_tag.attrs["href"]

    def get_court_offices(self) -> Dict[str, str]:
        """Get each office name with the url.

        Returns:
            Dict[str,str]: office name : url of the office.
        """
        offices = [
            "Juzgados",
            "Tribunales",
            "Tierras",
            "Justicia",
            "Jurisdiccion",
            "Centro",
        ]
        try:
            response = requests.get(const.URL_RAMA_JUDICIAL, verify=False, timeout=15)
        except requests.exceptions.Timeout:
            # If requesting the page is taking so long, read the last json.
            with open("Data/offices.json", "r") as file:
                res = json.load(file)
                return res
        doc = BeautifulSoup(response.text, "html.parser")
        links = doc.find_all("a")
        links_map = {}
        for link in links:
            href = link.get("href")
            text = link.get_text()
            links_map[text] = href
        res = {}
        not_offices = [
            "Consulta",
            "Corte",
            "Guia",
            "Gu\u00eda",
            "Informaci\u00f3n",
            "Tribunales",
            "Portal",
            "Justicia",
        ]
        for key in list(links_map.keys()):
            for office in offices:
                if office in key and all(
                    substring not in key for substring in not_offices
                ):
                    res[key] = links_map[key]

        # Update the json file
        with open("Data/offices.json", "w") as file:
            json.dump(res, file)

        return res
