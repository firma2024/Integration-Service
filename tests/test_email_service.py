import unittest
from parameterized import parameterized
from utils.utils import *
from service.EmailService import EmailService

class TestEmailService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.utility_instance = EmailService()
    def test_send_email(self):
        pass