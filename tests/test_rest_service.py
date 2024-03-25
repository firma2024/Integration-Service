import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from model.model import Actuacion, PreProceso, Proceso
from service.RestService import RestService
from requests.exceptions import ConnectTimeout, HTTPError
from datetime import datetime
from fastapi import HTTPException
from requests.exceptions import RequestException
class TestRestService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rest_service = RestService()

    @parameterized.expand(
        [
            ["has_action", "2023-10-22", "2024-11-02"],
            ["no_action", "2024-11-02", "2023-10-22"],
        ],
    )
    @patch("requests.get")
    def test_new_actuacion_process(self, name, last_action, expected, mock_get):
        mock_response = {"procesos": [{"fechaUltimaActuacion": expected}]}
        mock_get.return_value.json.return_value = mock_response
        result = self.rest_service.new_actuacion_process("file_number", last_action)
        if name in "no_action":
            assert result is None
        else:
            assert result == True

    @patch("requests.get")
    def test_get_process_info_success(self, mock_get):
        file_number = "123456"

        # Mock response
        mock_response_CPNU = MagicMock()
        mock_response_CPNU.status_code = 200
        mock_response_CPNU.text = """{
            "procesos": [{
                "sujetosProcesales": [],
                "departamento": "Department",
                "despacho": "Office",
                "idProceso": "123",
                "fechaProceso": "2024-02-12",
                "esPrivado": false
                
            }]
        }"""

        mock_response_CPNU_Individual = MagicMock()
        mock_response_CPNU_Individual.text = """
            {
                "tipoProceso": "Penal",
                "ubicacion": "Bogota"
            }
        """

        mock_get.side_effect = [mock_response_CPNU, mock_response_CPNU_Individual]

        result = self.rest_service.get_process_info(file_number)

        # Assertions
        assert isinstance(result, PreProceso)
        assert result.idProceso == "123"
        assert result.numeroRadicado == file_number
        assert result.despacho == "Office"
        assert result.departamento == "Department"
        assert result.fechaRadicacion == "2024-02-12"

    @patch("requests.get")
    def test_get_process_info_connect_timeout(self, mock_get):

        file_number = "123456"

        # Mock response to raise ConnectTimeout
        mock_get.side_effect = ConnectTimeout()

        with self.assertRaises(ConnectTimeout):
            self.rest_service.get_process_info(file_number)

    @patch("requests.get")
    def test_get_process_info_process_not_found(self, mock_get):
        file_number = "123456"

        # Mock response with empty "procesos" list
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """{"procesos": []}"""
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPException):
            self.rest_service.get_process_info(file_number)

    @patch('requests.get')
    def test_get_last_actuacion_success(self, mock_get):
        number_process = "123456"
        last_date_actuacion = "2024-02-12"

        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "actuaciones": [{
                "fechaActuacion": "2024-02-13",
                "actuacion": "Test Action",
                "anotacion": "Test Annotation",
                "fechaRegistro": "2024-02-12",
                "llaveProceso": "Test Process Key",
                "fechaInicial": "2024-02-12",
                "fechaFinal": "2024-02-12"
            }]
        }
        mock_get.return_value = mock_response

        res = self.rest_service.get_last_actuacion(number_process, last_date_actuacion)

        # Assertions
        assert len(res) == 1
        assert isinstance(res[0], Actuacion)
        assert res[0].nombreActuacion == "Test Action"
        assert res[0].anotacion == "Test Annotation"
        assert res[0].fechaActuacion == datetime.fromisoformat("2024-02-13")
        assert res[0].fechaRegistro == datetime.fromisoformat("2024-02-12")
        assert res[0].proceso == "Test Process Key"
        assert res[0].fechaInicia == "2024-02-12"
        assert res[0].fechaFinaliza == "2024-02-12"
        assert res[0].existDocument == True

    @patch('requests.get')
    def test_get_last_actuacion_request_exception(self, mock_get):
        number_process = "123456"
        last_date_actuacion = "2024-02-12"

        # Mock response to raise RequestException
        mock_get.side_effect = RequestException()

        with self.assertRaises(HTTPException) as cm:
            self.rest_service.get_last_actuacion(number_process, last_date_actuacion)

        # Assertions
        self.assertEqual(cm.exception.status_code, 503)
        self.assertEqual(cm.exception.detail, "Error al realizar la consulta: ")
    
    @patch('requests.get')
    def test_get_all_process_info_success(self, mock_get):
        file_number = "123456"

        # Mock response
        mock_response_proceso = MagicMock()
        mock_response_proceso.status_code = 200
        mock_response_proceso.text = """{
            "procesos": [{
                "sujetosProcesales": [],
                "departamento": "Department",
                "despacho": "Office",
                "idProceso": "123",
                "fechaProceso": "2024-02-12"
            }]
        }"""
        mock_response_actions = MagicMock()
        mock_response_actions.status_code = 200
        mock_response_actions.text = """{
            "actuaciones": [{
                "actuacion": "Test Action",
                "anotacion": "Test Annotation",
                "fechaActuacion": "2024-02-12T10:00:00",
                "fechaRegistro": "2024-02-12T10:00:00",
                "fechaInicial": "2024-02-12T10:00:00",
                "fechaFinal": "2024-02-12T10:00:00"
            }]
        }"""
        mock_response_CPNU_Individual = MagicMock()
        mock_response_actions.status_code = 200
        mock_response_CPNU_Individual.text = """
            {
                "tipoProceso": "Penal",
                "ubicacion": "Bogota"
            }
        """
        mock_get.side_effect = [mock_response_proceso, mock_response_actions,mock_response_CPNU_Individual]

        res = self.rest_service.get_all_process_info(file_number)

        # Assertions
        assert isinstance(res, Proceso)
        assert res.idProceso == "123"
        assert res.numeroRadicado == file_number
        assert res.despacho == "Office"
        assert res.departamento == "Department"
        assert res.fechaRadicacion == "2024-02-12"

        assert len(res.actuaciones) == 1
        assert isinstance(res.actuaciones[0], Actuacion)
        assert res.actuaciones[0].nombreActuacion == "Test Action"
        assert res.actuaciones[0].anotacion == "Test Annotation"
        assert res.actuaciones[0].fechaActuacion == datetime.fromisoformat("2024-02-12T10:00:00")
        assert res.actuaciones[0].fechaRegistro == datetime.fromisoformat("2024-02-12T10:00:00")
        assert res.actuaciones[0].fechaInicia == "2024-02-12T10:00:00"
        assert res.actuaciones[0].fechaFinaliza == "2024-02-12T10:00:00"
        assert res.actuaciones[0].existDocument

    @patch('requests.get')
    def test_get_all_process_info_request_exception(self, mock_get):
        file_number = "123456"
        mock_response = MagicMock()
        mock_response.status_code = 503
        
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPException):
            self.rest_service.get_all_process_info(file_number)

