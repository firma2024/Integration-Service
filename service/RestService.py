from typing import Optional, Union
import requests
from fastapi import HTTPException
from datetime import datetime
from model.model import Actuacion, Proceso, PreProceso
import requests
import json

import constants.constants as const


class RestService:

    def get_process_info(self, file_number: str) -> PreProceso:
        """Get process information by CPNU.

        Args:
            file_number (str): File number of the process.

        Raises:
            HTTPException 503: When the CPNU rest API is down.
            HTTPException 404: When the process does not exit in the CPNU.
            HTTPException 400: When the process is private.

        Returns:
            PreProceso: Process information.
        """
        url_cpnu_file_number = f"{const.URL_CPNU}{file_number}&SoloActivos=false"
        res = requests.get(url_cpnu_file_number)
        if res.status_code == 503:
            raise HTTPException(status_code=503, detail="Pagina no disponible")

        res_json = json.loads(res.text)
        if not res_json["procesos"]:
            raise HTTPException(status_code=404, detail="Proceso no encontrado.")
        if res_json["procesos"][0]["esPrivado"]:
            raise HTTPException(status_code=400, detail="Proceso privado.")

        subjects = res_json["procesos"][0]["sujetosProcesales"]
        res_data = res_json["procesos"][0]
        department = res_data["departamento"]
        office = res_data["despacho"]
        process_id = res_data["idProceso"]
        date_filed = res_data.pop("fechaProceso")

        # Get process type
        url_cpnu_single_process_id = (
            f"{const.URL_CPNU_SINGLE}Detalle/{res_data['idProceso']}"
        )
        try:
            res = requests.get(url_cpnu_single_process_id)
        except requests.exceptions.ConnectTimeout:
            raise HTTPException(status_code=503, detail="Pagina no disponible")
        res_json = json.loads(res.text)

        process = PreProceso(
            idProceso=process_id,
            numeroRadicado=file_number,
            despacho=office,
            departamento=department,
            sujetos=subjects,
            fechaRadicacion=date_filed,
            tipoProceso=res_json["tipoProceso"],
            ubicacionExpediente=res_json["ubicacion"],
        )

        return process

    def get_all_process_info(self, file_number: str) -> Proceso:
        """Get process information and actions by CPNU.

        Args:
            file_number (str): File number of the process.

        Raises:
            HTTPException 503: When the CPNU rest API is down.
            HTTPException 404: When the process does not exit in the CPNU.

        Returns:
            Proceso: Process information with actions.
        """
        url_cpnu_file_number = f"{const.URL_CPNU}{file_number}&SoloActivos=false"
        res = requests.get(url_cpnu_file_number)

        if res.status_code == 503:
            raise HTTPException(status_code=503, detail="Pagina no disponible")

        res_json = json.loads(res.text)
        if not res_json["procesos"]:
            raise HTTPException(status_code=404, detail="Proceso no encontrado.")

        subjects = res_json["procesos"][0]["sujetosProcesales"]
        res_data = res_json["procesos"][0]
        department = res_data["departamento"]
        office = res_data["despacho"]
        process_id = res_data["idProceso"]
        date_filed = res_data.pop("fechaProceso")

        # Get actions
        url_cpnu_single_actions = (
            f"{const.URL_CPNU_SINGLE}Actuaciones/{res_data['idProceso']}?pagina=1"
        )
        try:
            res = requests.get(url_cpnu_single_actions)
        except requests.exceptions.ConnectTimeout:
            raise HTTPException(status_code=503, detail="Pagina no disponible")
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
                    fechaActuacion=datetime.strptime(
                        action["fechaActuacion"], "%Y-%m-%dT%H:%M:%S"
                    ),
                    fechaRegistro=datetime.strptime(
                        action["fechaRegistro"], "%Y-%m-%dT%H:%M:%S"
                    ),
                    existDocument=(
                        True
                        if action["fechaInicial"] is not None
                        and action["fechaFinal"] is not None
                        else False
                    ),
                    fechaInicia=action["fechaInicial"],
                    fechaFinaliza=action["fechaFinal"],
                    proceso=None,
                )
            )

        # Get process type
        url_cpnu_single_process_id = (
            f"{const.URL_CPNU_SINGLE}Detalle/{res_data['idProceso']}"
        )
        try:
            res = requests.get(url_cpnu_single_process_id)
        except requests.exceptions.ConnectTimeout:
            raise HTTPException(status_code=503, detail="Pagina no disponible")
        res_json = json.loads(res.text)

        process = Proceso(
            idProceso=process_id,
            numeroRadicado=file_number,
            despacho=office,
            departamento=department,
            sujetos=subjects,
            fechaRadicacion=date_filed,
            actuaciones=actuaciones,
            tipoProceso=res_json["tipoProceso"],
            ubicacionExpediente=res_json["ubicacion"],
        )

        return process

    def new_actuacion_process(
        self, file_number: str, date_actuacion_str: str
    ) -> Optional[Union[bool, None]]:
        """Validate if a process has an action.

        Args:
            file_number (str): File number of the process.
            date_actuacion_str (str): Date of the actual action detected.

        Raises:
            HTTPException: 503 When the CPNU rest API is down.

        Returns:
            Optional[Union[bool, None]]: True if action exists, else None.
        """
        url_cpnu_file_number = f"{const.URL_CPNU}{file_number}&SoloActivos=false"
        try:
            response = requests.get(url_cpnu_file_number)
            response.raise_for_status()
            data = response.json()
            procesos = data.get("procesos")
            last_date_actuacion_str = procesos[0].get("fechaUltimaActuacion")
            last_date_actuacion = datetime.fromisoformat(last_date_actuacion_str)
            date_actuacion = datetime.fromisoformat(date_actuacion_str)

            if last_date_actuacion > date_actuacion:
                print("Nueva actuacion ", last_date_actuacion)
                return True

            return None

        except requests.exceptions.RequestException as e:
            raise HTTPException(503, detail=f"Error al realizar la consulta: {e}")

    def get_last_actuacion(
        self, number_process: int, date_actuacion_str: str
    ) -> list[Actuacion]:
        """Get last action of a process.

        Args:
            number_process (int): Process number.
            last_date_actuacion (datetime): Last date action had an update.

        Raises:
            HTTPException: 503 When the CPNU rest API is down.

        Returns:
            List[Actuacion]: Action details.
        """
        url_cpnu_actuaciones = f"{const.URL_CPNU_ACTUACIONES}{number_process}?pagina=1"
        try:
            list_new_actuaciones = []
            response = requests.get(url_cpnu_actuaciones)
            response.raise_for_status()
            data = response.json()
            actuaciones_list = data.get("actuaciones", [])
            date_actuacion = datetime.fromisoformat(date_actuacion_str)

            for actuacion in reversed(actuaciones_list):
                actuacion_date = datetime.fromisoformat(actuacion.get("fechaActuacion"))
                if actuacion_date > date_actuacion:
                    print("Actuacion encontrada  ", actuacion_date)
                    actuacion_name = actuacion.get("actuacion")
                    anotacion = actuacion.get("anotacion")
                    registro_date = datetime.fromisoformat(
                        actuacion.get("fechaRegistro")
                    )
                    proceso = actuacion.get("llaveProceso")

                    existDocument = (
                        True
                        if actuacion["fechaInicial"] is not None
                        and actuacion["fechaFinal"] is not None
                        else False
                    )

                    new_actuacion = Actuacion(
                        nombreActuacion=actuacion_name,
                        anotacion=anotacion,
                        fechaActuacion=actuacion_date,
                        fechaRegistro=registro_date,
                        proceso=proceso,
                        fechaInicia=actuacion["fechaInicial"],
                        fechaFinaliza=actuacion["fechaFinal"],
                        existDocument=existDocument,
                    )
                    list_new_actuaciones.append(new_actuacion)

            return list_new_actuaciones

        except requests.exceptions.RequestException as e:
            raise HTTPException(503, detail=f"Error al realizar la consulta: {e}")
