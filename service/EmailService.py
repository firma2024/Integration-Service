import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from model.Actuacion import Actuacion
from utils.utils import replace_placeholders_email
class EmailService:
    def send_email(self, receiver: str, action:Actuacion):
        # Lee el contenido HTML desde el archivo
        with open('static/email.html', 'r') as file:
            html_content = file.read()
            html_content_formatted = replace_placeholders_email(html_content,action)


        # Crea un mensaje MIME multipart y establece el contenido HTML
        msg = MIMEMultipart()
        msg.attach(MIMEText(html_content_formatted, 'html'))

        msg['Subject'] = 'Prueba HTML'
        msg['From'] = 'firma.software.soporte@gmail.com'
        msg['To'] = receiver

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login('firma.software.soporte@gmail.com', "bwun nhzu xxet rpev")
            smtp_server.sendmail('firma.software.soporte@gmail.com', receiver, msg.as_string())

