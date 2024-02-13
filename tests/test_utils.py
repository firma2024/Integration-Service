import unittest
from parameterized import parameterized
from utils.utils import *


class TestUtils(unittest.TestCase):
    @parameterized.expand(
        [
            [
                "no_modifications",
                "JUZGADO 001 CIVIL MUNICIPAL DE BELLO",
                "JUZGADO 001 CIVIL MUNICIPAL DE BELLO",
            ],
            [
                "with_modifications",
                "JUZGADO 030 ADMINISTRATIVO  DE LA SECCION SEGUNDA  DE BOGOTÁ ",
                "JUZGADO 030 ADMINISTRATIVO DE LA SECCION SEGUNDA DE BOGOTÁ",
            ],
        ],
    )
    def test_clean_string(self, name, office_name, expected):
        self.assertEqual(clean_string(office_name), expected)

    @parameterized.expand(
        [
            ["no_split", [1, 2, 3, 4], 1, [[1, 2, 3, 4]]],
            ["split", [1, 2, 3, 4], 2, [[1, 2], [3, 4]]],
        ],
    )
    def test_split_list(self, name, lst, n, expected):
        assert list(split_list(lst, n)) == expected

    def test_replace_placeholders_email(self):
        html = """{{ id }}, {{ actuacion }}, 
                  {{ radicado }}, {{ anotacion }}, 
                  {{ fechaActuacion }}, {{ emailAbogado }}, 
                  {{ nameAbogado }}, {{ link }}"""

        actuacion_email = ActuacionEmail(
            id=1,
            actuacion="Test1",
            radicado="Test2",
            anotacion="Test3",
            fechaActuacion="Test4",
            emailAbogado="Test5",
            nameAbogado="Juan",
            link="example.com",
        )
        res = replace_placeholders_email(html, actuacion_email)
        assert (
            res
            == """1, Test1, 
                  Test2, Test3, 
                  Test4, Test5, 
                  Juan, example.com"""
        )
