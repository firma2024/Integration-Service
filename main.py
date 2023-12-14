from bs4 import BeautifulSoup
import requests
import json
from pprint import pprint

file_number="11001400305420210000800"

CPNU ="https://consultaprocesos.ramajudicial.gov.co:448/api/v2/Procesos"
CPNU_INDIVIDUAL = CPNU[:-1]


#Get data of the process
res=requests.get(f"{CPNU}/Consulta/NumeroRadicacion?numero={file_number}&SoloActivos=true&pagina=1")
process = json.loads(res.text)

#Get office (despacho)
office = process["procesos"][0]["despacho"]
print(f"Office: {office}")
office = office[:-1]
#Obtain process_id in the CPNU
process_id = process["procesos"][0]["idProceso"]
print(f"Process id: {process_id}")

#Obtain process details
res = requests.get(f"{CPNU_INDIVIDUAL}/Detalle/{process_id}")

#Obtain actions (actuaciones)
res = requests.get(f"{CPNU_INDIVIDUAL}/Actuaciones/{process_id}?pagina=1")
res_actions = json.loads(res.text)
actions=res_actions["actuaciones"]
actions_with_docs = [action for action in actions if action["fechaInicial"] != None or action["fechaFinal"] != None]

#Get docs
#This could be better with maybe if in, think more.

#TODO Think how hijueputas obtain the url of the office (despacho)
"""mapped_urls = {
    "JUZGADO 054 CIVIL MUNICIPAL DE BOGOTÁ" : "https://www.ramajudicial.gov.co/portal/inicio/mapa/juzgados-civiles-municipales"
    #...
}"""
res_html=requests.get("https://www.ramajudicial.gov.co/web/juzgado-054-civil-municipal-de-bogota", verify=False)

soup = BeautifulSoup(res_html.text,"html.parser")
autos_h4 = soup.find('h4', text='Autos')

if autos_h4:
    next_div = autos_h4.find_next('div')

    if next_div:
        print(next_div)
    else:
        print("No div found after 'Autos' h4")
        
