import requests
import json
from typing import Dict
from datetime import datetime

import constants.constants as const
from utils.utils import get_defendant_and_plaintiff

class RestService:
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