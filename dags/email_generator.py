import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#Inroducir aquí la contraseña de la cuenta de correo que se usará para enviar los correos electrónicos
password = 'XXXXXXXXXXXXX'
remitente = 'XXXXXX@mail.com'
destinatario_marketing = "YYYYYYYY@mail.com"
destinatario_analytics = "ZZZZZZZZ@mail.com"

def send_email_marketing(password=password, remitente=remitente, destinatario = destinatario_marketing, **context):

    filepath1 = '/tmp/spaceX_data/history_' + context['ds_nodash'] + '_' + context['execution_date'].strftime('%H%M%S') + '.json'

    # Configurar los parámetros del correo
    asunto = "Noticias de SpaceX listas"
    cuerpo = f"""\
            Estimado equipo de marketing,

            Las noticias de SpaceX ya están a vuestra disposición en el archivo .json adjunto.

            También pueden encontrar los archivos en la siguiente ubicación:

            {filepath1}

            Atentamente,
            
            El equipo de Platzi Space Project.
            """

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar el archivo al mensaje
    
    with open(filepath1, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath1))
        mensaje.attach(attachment)

    # Enviar el correo electrónico
    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remitente, password)
    servidor_smtp.sendmail(remitente, destinatario, mensaje.as_string())
    servidor_smtp.quit()

def send_email_data_team(password=password, remitente=remitente, destinatario = destinatario_analytics, **context):

    filepath1 = '/tmp/platzi_data/platzi_data_' + context['ds_nodash'] + '_' + context['execution_date'].strftime('%H%M%S') + '.csv'

    # Se supone que aquí iría el mail de data analytics, por simplificar dejo el mismo
    destinatario = "platzi-marketing@mail.com"
    asunto = "Archivos del satélite listos"
    cuerpo = f"""\
            Estimado equipo de data analytics,

            Los datos de los usuarios registrados en el satélite están a vuestra disposición en el archivo .csv adjunto.

            También pueden encontrar los archivos en la siguiente ubicación:

            {filepath1}

            Atentamente,
            
            El equipo de Platzi Space Project.
            """

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    # Adjuntar el archivo al mensaje
    
    with open(filepath1, "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="txt")
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath1))
        mensaje.attach(attachment)

    # Enviar el correo electrónico
    servidor_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remitente, password)
    servidor_smtp.sendmail(remitente, destinatario, mensaje.as_string())
    servidor_smtp.quit()