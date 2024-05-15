import unittest
from parameterized import parameterized
from utils.utils import *
from service.WebScraperService import SeleniumService, BeatifulSoupService
from unittest.mock import MagicMock, patch
from selenium import webdriver
from fastapi import HTTPException


class TestSeleniumService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium_service = SeleniumService()


    @parameterized.expand(
        [
            [
                "exist_in_df",
                "JUZGADO 030 ADMINISTRATIVO  DE LA SECCIÓN SEGUNDA  DE BOGOTÁ ",
                "https://portalhistorico.ramajudicial.gov.co/web/juzgado-30-administrativo-de-bogota",
            ],
            [
                "not_in_df",
                "JUZGADO 030 ADMINISTRATIVO  DE LA SECCIÓN SEGUNDA  DE ESTADOS UNIDOS",
                None,
            ],
        ],
    )
    def test_get_office_url(self, name, office_name, expected_url):
        if name == "exist_in_df":
            assert self.selenium_service.get_office_url_df(office_name) == expected_url
        else:
            with self.assertRaises(HTTPException):
                self.selenium_service.get_office_url_df(office_name)


class TestBeaitfulSoupService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.beatiful_soup_service = BeatifulSoupService()

    def test_get_url_estados(self):
        office_url = (
            "https://portalhistorico.ramajudicial.gov.co/web/juzgado-30-administrativo-de-bogota"
        )
        expected_url = f"{office_url}/181"

        assert self.beatiful_soup_service.get_url_estados(office_url,"2024") == expected_url

    @patch("requests.get")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_get_court_offices_success(self, mock_open, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><a href='url1'>Juzgados</a><a href='url2'>Tribunales</a></html>"
        )
        mock_get.return_value = mock_response

        result = self.beatiful_soup_service.get_court_offices()

        mock_open.assert_called_once_with("Data/offices.json", "w")

        expected_result = {"Juzgados": "url1"}
        assert result == expected_result
