import imaplib  # Para conectarse al servidor de correo usando IMAP
import email  # Para manejar el contenido de los correos electrónicos
import re  # Para utilizar expresiones regulares en la limpieza de texto
from bs4 import BeautifulSoup  # Para procesar y limpiar contenido HTML
from email.header import decode_header  # Para decodificar encabezados codificados


# --- Cache para guardar correos ya clasificados ---
emails_cache = []

# --- Funciones auxiliares ---
def limpiar_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def limpiar_texto(texto):
    texto = re.sub(r'http\S+|www\S+', '', texto)
    texto = re.sub(r'(?i)-- ?\n.*', '', texto)
    texto = re.sub(r'(?i)el .*escribió:', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def get_emails_imap(user, app_password, max_emails=10):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, app_password)
    mail.select("inbox")

    status, messages = mail.search(None, 'X-GM-RAW "category:primary"')
    if status != "OK":
        return []

    email_ids = messages[0].split()[-max_emails:]
    correos = []

    for eid in reversed(email_ids):
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        subject, _ = decode_header(msg["Subject"] or "")[0]
        if isinstance(subject, bytes):
            subject = subject.decode(errors="ignore")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True).decode(errors="ignore")
                    body = limpiar_html(html_body)
                    break
        else:
            content_type = msg.get_content_type()
            payload = msg.get_payload(decode=True)
            if payload:
                if content_type == "text/html":
                    body = limpiar_html(payload.decode(errors="ignore"))
                else:
                    body = payload.decode(errors="ignore")

        body = limpiar_texto(body)
        correos.append((subject, body))

    mail.logout()
    return correos