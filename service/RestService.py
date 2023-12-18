import requests
import json
from typing import Dict

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