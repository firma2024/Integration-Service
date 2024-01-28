from service.SeleniumService import SeleniumService
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json
import time
import pandas as pd

URL = "https://www.ramajudicial.gov.co/portal/inicio"
offices = ["Juzgados", "Tribunales", "Tierras",
           "Justicia", "Jurisdiccion", "Centro"]

df = pd.read_csv("file.csv")


fila_deseada = df[df['Nombre_despacho'] =="JUZGADO 001 CIVIL MUNICIPAL DE BELLO"]
fila_deseada2 = df[df['Nombre_despacho'] == "JUZGADO 031 CIVIL MUNICIPAL DE BOGOTÁ"]
print(fila_deseada["Link_Despacho"].iloc[0])
print(fila_deseada2["Link_Despacho"].iloc[0])

"""
response = requests.get(URL, verify=False)
doc = BeautifulSoup(response.text, 'html.parser')
links = doc.find_all('a')
links_map={}
for link in links:
    href = link.get('href')
    text = link.get_text()
    links_map[text] = href
res = {}
for key in list(links_map.keys()):
    for office in offices:
        if office in key and not "Consulta" in key and not "Corte" in key and not "Guia" in key:
            res[key] = links_map[key]"""


"""
selenium_service = SeleniumService()
selenium_service.open()
with open("res.json", 'r') as archivo:
    res = json.load(archivo)
columns = ["Ciudad_Mapa", "Nombre_despacho", "Link_Despacho"]
df = pd.DataFrame(columns=columns)

for key in res.keys():
    selenium_service.driver.get(res[key])
    div_principales_mapa = selenium_service.driver.find_element(
        By.CLASS_NAME, 'principalesMapa')
    lista_items = div_principales_mapa.find_elements(By.TAG_NAME, 'li')
    for item in lista_items:
        item.click()
        time.sleep(3)
        # Obtain name of the city
        ciudad_mapa = selenium_service.driver.find_element(By.ID, 'titleD')

        div = selenium_service.driver.find_element(By.ID, 'selected')
        lista_items = div.find_elements(By.TAG_NAME, 'li')
        for li in lista_items:
            a_tag = li.find_elements(By.TAG_NAME, 'a')
            df = pd.concat([df, pd.DataFrame(
                {"Ciudad_Mapa": [ciudad_mapa.text], "Nombre_despacho": [
                    a_tag[0].text], "Link_Despacho": [a_tag[0].get_attribute("href")]}
            )], ignore_index=True)
        go_back = selenium_service.driver.find_element(By.ID, 'atras')
        go_back.click()
        df.to_csv('file.csv', index=False)"""
