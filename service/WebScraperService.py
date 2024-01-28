from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

import constants.constants as const

class WebScraperService:
    
    def get_url_juzgado(self, name_despacho):
        """Get url_juzgado given name of the despacho.

        Args:
            name_despacho (str): despacho name.

        Returns:
            str: url of the juzgado.
        """
        print("Inicio de búsqueda de enlace del juzgado")
        words_list = re.sub(r'\b\d+\b', '', name_despacho).split()
        tama = len(words_list)
        words_list = words_list[:tama - 2]
        links_map = {}

        response = requests.get(const.URL_RAMA_JUDICIAL, verify=False)
        doc = BeautifulSoup(response.text, 'html.parser')

        links = doc.find_all('a')

        for link in links:
            href = link.get('href')
            text = link.get_text()
            links_map[text] = href

        containsEjecucion = False
        containsPromiscuo = False

        for word in words_list:
            if "ejecución" in word.lower():
                containsEjecucion = True
            if "promiscuo" in word.lower():
                containsPromiscuo = True

            for key in list(links_map.keys()):
                if len(links_map) == 1:
                    break
                if word.lower() not in key.lower():
                    del links_map[key]

        if not containsEjecucion:
            for key in list(links_map.keys()):
                if "ejecución" in key.lower():
                    del links_map[key]

        if not containsPromiscuo:
            for key in list(links_map.keys()):
                if "promiscuo" in key.lower():
                    del links_map[key]

        if len(links_map) == 1:
            return list(links_map.values())[0]

        return None


    def get_url_estados(self, url_despacho):
        """Get url despchao given url despacho.

        Args:
            url_despacho (str): despacho url.

        Returns:
            str: url of the estados.
        """
        print("Inicio de búsqueda de enlace de estados")
        links = []
        
        print(url_despacho)
        response = requests.get(url_despacho, verify=False)
        doc = BeautifulSoup(response.content, 'html.parser')
        
        index_estados = 0
        year = str(datetime.now().year)
        
        elements = doc.find_all(class_="layouts level-1")
        for element in elements:
            i = 0
            titles = element.select("h4")
            for title in titles:
                text = title.get_text()
                if "Estados Electrónicos".lower() in text.lower():
                    index_estados = i
                i += 1
            
            a_links = element.select("a")
            for a in a_links:
                href = a.get("href")
                text = a.get_text()
                if year in text:
                    links.append(href)
        
        print("Enviando enlace de estados")
        return const.URL_RAMA_JUDICIAL_INICIO + links[index_estados - 1]