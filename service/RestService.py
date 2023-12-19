import requests
from fastapi import HTTPException
from datetime import datetime
from model.model import Proceso,Actuacion
import requests
import json
from datetime import datetime

from fastapi import HTTPException
import constants.constants as const
from utils.utils import get_defendant_and_plaintiff
from datetime import datetime

class RestService:
    def get_process_info(self, file_number: str) -> Proceso:
        """Get process information by CPNU.

        Args:
            file_number (str): File number of the process.

        Returns:
            Proceso: Process information.
        """
        # Get information of the process.
        url_cpnu_file_number = f"{const.URL_CPNU}{file_number}&SoloActivos=true"
        res = requests.get(url_cpnu_file_number)

        if res.status_code == 503:
            raise HTTPException(status_code=503, detail="Pagina no disponible")

        res_json = json.loads(res.text)
        if not res_json["procesos"]:
            raise HTTPException(status_code=404, detail="Proceso no encontrado.")

        defendant, plaintiff = get_defendant_and_plaintiff(
            res_json["procesos"][0]["sujetosProcesales"]
        )
        
        res_data = res_json["procesos"][0]
        department = res_data["departamento"]
        office = res_data["despacho"]
        last_date_action =  res_data["fechaUltimaActuacion"]
        process_id = res_data["idProceso"]
        date_filed = res_data.pop("fechaProceso")
        
       
        # Get actions
        url_cpnu_single_actions = (
            f"{const.URL_CPNU_SINGLE}Actuaciones/{res_data['idProceso']}?pagina=1"
        )
        res = requests.get(url_cpnu_single_actions)
        res_json = json.loads(res.text)
        actions = res_json["actuaciones"]
        last_actions = sorted(
            actions,
            key=lambda x: datetime.strptime(x["fechaActuacion"], "%Y-%m-%dT%H:%M:%S"),
            reverse=True,
        )
        last_actions = last_actions[:10]

        actuaciones = []
        for action in last_actions:
            actuaciones.append(
                Actuacion(
                    nombreActuacion=action["actuacion"],
                    anotacion=action["anotacion"],
                    fechaActuacion=datetime.strptime(action["fechaActuacion"], "%Y-%m-%dT%H:%M:%S"),
                    fechaRegistro=datetime.strptime(action["fechaRegistro"], "%Y-%m-%dT%H:%M:%S"),
                    proceso=None
                )
            )

        # Get process type
        url_cpnu_single_process_id = (
            f"{const.URL_CPNU_SINGLE}Detalle/{res_data['idProceso']}"
        )

        res = requests.get(url_cpnu_single_process_id)
        res_json = json.loads(res.text)
        
        process = Proceso(
            idProceso=process_id,
            numeroRadicado=file_number,
            fechaUltimaActuacion=last_date_action,
            despacho=office,
            departamento=department,
            demandante=plaintiff,
            demandado=defendant,
            fechaRadicacion=date_filed,
            actuaciones=actuaciones,
            tipoProceso=res_json["tipoProceso"],
            ubicacionExpediente=res_json["ubicacion"]
        )
        
        return process
    
    def new_actuacion_process(self, file_number: str, date_actuacion_str):
        url_cpnu_file_number = f"{const.URL_CPNU}{file_number}&SoloActivos=true"
        try:
            response = requests.get(url_cpnu_file_number)
            response.raise_for_status()
            data = response.json()
            procesos = data.get('procesos')
            last_date_actuacion_str = procesos[0].get('fechaUltimaActuacion')
            last_date_actuacion = datetime.fromisoformat(last_date_actuacion_str)
            date_actuacion = datetime.fromisoformat(date_actuacion_str)

            if last_date_actuacion > date_actuacion:
                print("Nueva actuacion")
                return True, last_date_actuacion
            
            return False

        except requests.exceptions.RequestException as e:
            print("Error al realizar la consulta:", e)
            return False

    def get_last_actuacion(self, number_process, last_date_actuacion):
        url_cpnu_actuaciones = f"{const.URL_CPNU_ACTUACIONES}{number_process}?pagina=1"
        try:
            response = requests.get(url_cpnu_actuaciones)
            response.raise_for_status()
            data = response.json()
            actuaciones_list = data.get("actuaciones", [])
            
            for actuacion in actuaciones_list:
                actuacion_date = datetime.fromisoformat(actuacion.get("fechaActuacion"))
                if (actuacion_date == last_date_actuacion):
                    print("Actuacion encontrada")
                    

                    break

        except requests.exceptions.RequestException as e:
            print("Error al realizar la consulta:", e)
