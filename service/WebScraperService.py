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

        url_rama_judicial = const.URL_RAMA_JUDICIAL
        response = requests.get(url_rama_judicial, verify=False)
        doc = BeautifulSoup(response.text, 'html.parser')

        links = doc.find_all('a')

        for link in links:
            href = link.get('href')
            text = link.get_text()
            links_map[text] = href

        contains_ejecucion = False
        contains_promiscuo = False

        for word in words_list:
            if "ejecución" in word.lower():
                contains_ejecucion = True
            if "promiscuo" in word.lower():
                contains_promiscuo = True

            keys_to_remove = [key for key in links_map.keys() if word.lower() not in key.lower()]
            for key in keys_to_remove:
                links_map.pop(key, None)

        if not contains_ejecucion:
            links_map = {key: value for key, value in links_map.items() if "ejecución" not in key.lower()}

        if not contains_promiscuo:
            links_map = {key: value for key, value in links_map.items() if "promiscuo" not in key.lower()}

        if len(links_map) == 1:
            return next(iter(links_map.values()))

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
        return const.URL_RAMA_JUDICIAL_INICIO + links[index_estados]