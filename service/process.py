from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
import json
from typing import Dict

import constants.constants as const
from utils.utils import get_defendant_and_plaintiff

class ProcessService:
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

    def get_office_url(self, officeName: str)->str:
        """Get office url given name of the office.

        Args:
            officeName (str): Office name.

        Returns:
            str: url of the office.
        """
        self.open()
        words_list = officeName.split()
        city = words_list[-1]

        self.driver.get(const.URL_JUZGADO)

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

    def get_process_info(self, file_number: str) -> Dict[str, any]:
        """Get process informatio by CPNU.

        Args:
            file_number (str): File number of the process.

        Returns:
            Dict[str, any]: Process informatio.
        """
        url_cpnu_file_number = f"{const.URL_CPNU}{file_number}&SoloActivos=true"
        res = requests.get(url_cpnu_file_number)
        res_json = json.loads(res.text)
        process = res_json["procesos"][0]

        process["demandante"],process["demandado"] = get_defendant_and_plaintiff(res_json["procesos"][0]["sujetosProcesales"])

        to_delete = ["idConexion", "esPrivado", "cantFilas","sujetosProcesales","llaveProceso"]
        for key in to_delete:
            if key in process:
                del process[key]

        url_cpnu_single_process_id = f"{const.URL_CPNU_SINGLE}{process['idProceso']}"
        res = requests.get(url_cpnu_single_process_id)
        res_json = json.loads(res.text)
        process["tipoProceso"] = res_json["tipoProceso"]
        return process
