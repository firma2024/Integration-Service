import unittest
from parameterized import parameterized
from utils.utils import *

class TestUtils(unittest.TestCase):
    @parameterized.expand(
        [
            [   "no_modifications",
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
    def test_clean_string(self,name, office_name, expected):
        self.assertEqual(clean_string(office_name), expected)

    def test_get_defendant_and_plaintiff(self):
        subjects = "Demandante: Juan Paez | Demandado: Daniel Barreto"
        plaintiff, defendant = get_defendant_and_plaintiff(subjects)
        assert plaintiff == "Juan Paez"
        assert defendant == "Daniel Barreto"

    @parameterized.expand(
        [
            [   "no_split",
                [1,2,3,4],
                1,
                [[1,2,3,4]]
            ],
            [   "split",
                [1,2,3,4],
                2,
                [[1,2],[3,4]]
            ]
        ],
    )
    def test_split_list(self,name,lst,n,expected):
        assert list(split_list(lst, n)) == expected
