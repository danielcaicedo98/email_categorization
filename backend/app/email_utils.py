import imaplib  # Para conectarse al servidor de correo usando IMAP
import email  # Para manejar el contenido de los correos electrónicos
import re  # Para utilizar expresiones regulares en la limpieza de texto
from bs4 import BeautifulSoup  # Para procesar y limpiar contenido HTML
from email.header import decode_header  # Para decodificar encabezados codificados


# Elimina etiquetas HTML y obtiene solo el texto visible
def limpiar_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# Limpia el texto de elementos innecesarios como URLs, firmas, respuestas anteriores, etc.
def limpiar_texto(texto):
    texto = re.sub(r'http\S+|www\S+', '', texto)  # Eliminar URLs
    texto = re.sub(r'(?i)-- ?\n.*', '', texto)  # Eliminar líneas de firma comunes
    texto = re.sub(r'(?i)el .*escribió:', '', texto)  # Eliminar encabezados de respuestas
    texto = re.sub(r'\s+', ' ', texto)  # Quitar exceso de espacios
    return texto.strip()

# --- Función principal para obtener correos usando IMAP ---

def get_emails_imap(user, app_password, max_emails=5):
    # Conectar con el servidor IMAP de Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(user, app_password)
    mail.select("inbox")  # Selecciona la bandeja de entrada

    # Buscar los correos de la categoría "Principal" en Gmail
    status, messages = mail.search(None, 'X-GM-RAW "category:primary"')
    if status != "OK":
        print("No se pudieron obtener los mensajes.")
        return []

    # Obtener los IDs de los últimos correos (limitado por max_emails)
    email_ids = messages[0].split()[-max_emails:]

    correos = []

    # Iterar sobre cada correo (de más reciente a más antiguo)
    for eid in reversed(email_ids):
        _, msg_data = mail.fetch(eid, "(RFC822)")  # Descargar el contenido del mensaje
        msg = email.message_from_bytes(msg_data[0][1])  # Convertir a objeto email

        # Obtener y decodificar el asunto
        subject, _ = decode_header(msg["Subject"] or "")[0]
        if isinstance(subject, bytes):
            subject = subject.decode(errors="ignore")

        body = ""

        # Si el correo tiene varias partes (HTML, texto plano, etc.)
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                # Si se encuentra texto plano
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
                # Si se encuentra HTML, se limpia
                elif content_type == "text/html":
                    html_body = part.get_payload(decode=True).decode(errors="ignore")
                    body = limpiar_html(html_body)
                    break
        else:
            # Si el correo no tiene múltiples partes
            content_type = msg.get_content_type()
            payload = msg.get_payload(decode=True)
            if payload:
                if content_type == "text/html":
                    body = limpiar_html(payload.decode(errors="ignore"))
                else:
                    body = payload.decode(errors="ignore")

        # Limpiar el cuerpo del correo antes de usarlo
        body = limpiar_texto(body)

        # Guardar el asunto y el cuerpo en la lista
        correos.append((subject, body))
    
    return correos