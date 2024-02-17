import unittest
from unittest.mock import patch, MagicMock
import smtplib
from model.model import ActuacionEmail
from service.EmailService import EmailService
import os

class TestEmailService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.email_service = EmailService()
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='<html><body>{{action}}</body></html>')
    @patch('smtplib.SMTP_SSL')
    def test_send_email_success(self, mock_smtp_ssl, mock_open):
        action =  ActuacionEmail(
            id=1,
            actuacion="Test1",
            radicado="Test2",
            anotacion="Test3",
            fechaActuacion="Test4",
            emailAbogado="Test5",
            nameAbogado="Juan",
            link="example.com",
        )
        receiver = "test@example.com"

        # Mock SMTP server and login
        smtp_instance = mock_smtp_ssl.return_value.__enter__.return_value
        smtp_instance.sendmail.return_value = {}
        
        # Mock os.getenv
        os.getenv = MagicMock(return_value="dummy_password")

        assert self.email_service.send_email(receiver, action)

        # Assertions
        mock_smtp_ssl.assert_called_once_with("smtp.gmail.com", 465)
        smtp_instance.login.assert_called_once_with('firma.software.soporte@gmail.com', 'dummy_password')
        smtp_instance.sendmail.assert_called_once()

        args, _ = smtp_instance.sendmail.call_args
        assert args[0] == 'firma.software.soporte@gmail.com'
        assert args[1] == receiver

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='<html><body>{{action}}</body></html>')
    @patch('smtplib.SMTP_SSL')
    def test_send_email_failure(self, mock_smtp_ssl, mock_open):
        
        action =  ActuacionEmail(
            id=1,
            actuacion="Test1",
            radicado="Test2",
            anotacion="Test3",
            fechaActuacion="Test4",
            emailAbogado="Test5",
            nameAbogado="Juan",
            link="example.com",
        )
        receiver = "test@example.com"

        # Mock SMTP server and login to raise exception
        smtp_instance = mock_smtp_ssl.return_value.__enter__.return_value
        smtp_instance.login.side_effect = smtplib.SMTPException("Dummy exception")

        # Mock os.getenv
        os.getenv = MagicMock(return_value="dummy_password")

        assert not self.email_service.send_email(receiver, action)

        # Assertions
        mock_smtp_ssl.assert_called_once_with("smtp.gmail.com", 465)
        smtp_instance.login.assert_called_once_with('firma.software.soporte@gmail.com', 'dummy_password')
        smtp_instance.sendmail.assert_not_called()