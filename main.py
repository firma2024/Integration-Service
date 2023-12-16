from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

print("Inicio de SeleniumService")

urlJuzgado = "https://www.ramajudicial.gov.co/juzgados-civiles-del-circuito"  # Reemplaza con tu cadena de texto
nameDespacho = "JUZGADO 017 CIVIL DEL CIRCUITO DE BOGOTÁ"  # Reemplaza con tu URL

wordsList = nameDespacho.split()
city = wordsList[-1]

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get(urlJuzgado)

links = driver.find_elements(By.TAG_NAME, "a")

for link in links:
    text = link.text
    if city.lower() in text.lower():
        link.click()
        break

time.sleep(3)

valueDespacho = wordsList[1]

links = driver.find_elements(By.TAG_NAME, "a")
for link in links:
    text = link.text
    href = link.get_attribute("href")
    if valueDespacho.lower() in text.lower():
        driver.quit()
        print(href)
        exit()

driver.quit()
print("No se encontró el enlace correspondiente.")
