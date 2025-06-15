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

def get_emails_imap(user, app_password, max_emails=5):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, app_password)
        mail.select("inbox")

        # 🔍 Búsqueda sin filtro para probar
        status, messages = mail.search(None, "ALL")
        print("🔍 Estado de búsqueda:", status)
        # print("🔍 IDs de mensajes encontrados:", messages)

        if status != "OK":
            print("❌ No se pudieron obtener los mensajes.")
            return []

        email_ids = messages[0].split()[-max_emails:]
        correos = []

        for eid in reversed(email_ids):
            print(f"\n📩 Procesando correo ID: {eid.decode()}")
            _, msg_data = mail.fetch(eid, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            subject, _ = decode_header(msg["Subject"] or "")[0]
            if isinstance(subject, bytes):
                subject = subject.decode(errors="ignore")
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    payload = part.get_payload(decode=True)
                    if payload:
                        if content_type == "text/plain":
                            body = payload.decode(errors="ignore")
                            break  # Prioridad a texto plano
                        elif content_type == "text/html" and not body:
                            html_body = payload.decode(errors="ignore")
                            body = limpiar_html(html_body)
            else:
                content_type = msg.get_content_type()
                payload = msg.get_payload(decode=True)
                if payload:
                    if content_type == "text/html":
                        body = limpiar_html(payload.decode(errors="ignore"))
                    else:
                        body = payload.decode(errors="ignore")

            body = limpiar_texto(body)
            print(f"📝 Asunto: {subject}")
            print(f"📄 Cuerpo (preview): {body[:100]}...\n")
            correos.append((subject, body))

        return correos

    except imaplib.IMAP4.error as e:
        print(f"❌ Error al conectar al servidor IMAP: {e}")
        return []