import unittest
from unittest.mock import patch
from parameterized import parameterized
from service.RestService import RestService
from datetime import datetime
class TestRestService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rest_service = RestService()

    @parameterized.expand(
        [
            [   "has_action",
                "2023-10-22",
                "2024-11-02"
            ],
            [
                "no_action",
                "2024-11-02",
                "2023-10-22"
            ]
        ],
    )
    @patch('requests.get')
    def test_new_actuacion_process(self,name,last_action,expected,mock_get):
        mock_response = {
            "procesos": [
                {"fechaUltimaActuacion": expected}
            ]
        }
        mock_get.return_value.json.return_value = mock_response
        result = self.rest_service.new_actuacion_process("file_number", last_action)
        if name in "no_action":
            assert result is None
        else:
            assert result == datetime.fromisoformat(expected)
