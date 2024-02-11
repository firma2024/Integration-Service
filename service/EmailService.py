from model.model import ActuacionEmail
from utils.utils import replace_placeholders_email

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class EmailService:
    def send_email(self, receiver: str, action: ActuacionEmail)->bool:
        """Send email with the HTML format.

        Args:
            receiver (str): Email of the receiver.
            action (ActuacionEmail): Action to be replaced in the HTML.

        Returns:
            bool: Validation if the email was sent.
        """
        # Read HTML and replace placeholders.
        with open('static/email.html', 'r') as file:
            html_content = file.read()
            html_content_formatted = replace_placeholders_email(html_content, action)


        # Create MIME multipart message y and set HTML email.
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_content_formatted, 'html'))

        msg['Subject'] = 'Actuación generada proceso [{}]'.format(action.radicado)
        msg['From'] = 'firma.software.soporte@gmail.com'
        msg['To'] = receiver

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login('firma.software.soporte@gmail.com', "bwun nhzu xxet rpev")
                smtp_server.sendmail('firma.software.soporte@gmail.com', receiver, msg.as_string())
            print("El correo se envió correctamente a", receiver)
            return True

        except smtplib.SMTPException as e:
            print("Error al enviar el correo:", e)
            return False

