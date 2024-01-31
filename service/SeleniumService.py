from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import constants.constants as const

from typing import List
import json
import time
import pandas as pd
import os
import threading

class SeleniumService:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = None

    def close(self):
        """Close instance of driver Chrome.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None  # Establece el driver a None después de cerrarlo

    def open(self):
        """Create instance of Chrome.
        """
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

    def get_offices(self):
        json_offices = os.path.join(os.pardir,"Integration-Service/offices.json")
        with open(json_offices, 'r') as file:
            dict_offices = json.load(file)
        threads = []
        for key,url_offices in dict_offices.items():
            # Get name of the office and url of the sub-offices
            t = ScrapeThread(url_offices,key)
            t.start()
            threads.append(t)
        for t in threads: 
            t.join()
            
class ScrapeThread(threading.Thread): 
    def __init__(self, list_offices,file_name): 
        threading.Thread.__init__(self) 
        self.list_offices = list_offices 
        self.file_name = file_name

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    def run(self): 
        if not os.path.exists("Offices"):
            os.makedirs("Offices")

        #Create empty dataframe
        columns = ["Ciudad_Mapa", "Nombre_despacho", "Link_Despacho"]
        df = pd.DataFrame(columns=columns)

        # Create chrome driver instance
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
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
                    df = pd.concat([df, pd.DataFrame(
                        {"Ciudad_Mapa": [ciudad_mapa.text], "Nombre_despacho": [
                            a_tag[0].text], "Link_Despacho": [a_tag[0].get_attribute("href")]}
                    )], ignore_index=True)
                go_back = self.driver.find_element(By.ID, 'atras')
                go_back.click()

        df.to_csv(os.path.join("Offices", f'{self.file_name}.csv'), index=False)
        self.driver.close()
        

        
         