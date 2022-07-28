from pathlib import Path
import environ
from django.core.mail import EmailMultiAlternatives, send_mail

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

API_KEY = env('MJ_APIKEY_PUBLIC')
API_SECRET = env('MJ_APIKEY_PRIVATE')


def send_email(cert=None):
    try:
        message = '''
        Hola, {NAME}
        Se ha generado tu certificado, por haber completado la competencia {COMPETENCIA}, felicidades.
        Este certificado es único y solo para ti. 
        '''.format(
            NAME=cert.participante.usuario.nombre,
            COMPETENCIA=cert.competencia.titulo,
        )
        subject, from_email, to = 'Certificado EduTech', 'EduTech <'+env('API_EMAIL')+'>', cert.participante.usuario.email
        msg = EmailMultiAlternatives(subject, message, from_email, [to])
        msg.attach_file(cert.certificado.path)
        msg.send()
        return True
    except Exception as e:
        print("error send", e)
        return e
