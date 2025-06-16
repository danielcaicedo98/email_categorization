from flask import Blueprint, jsonify
from .email_utils import get_emails_imap
from .classifier import clasificar_correo
from .config import EMAIL_USER, EMAIL_PASSWORD

main = Blueprint("main", __name__)

@main.route("/correos")
def obtener_correos():
    emails = get_emails_imap(EMAIL_USER, EMAIL_PASSWORD, max_emails=100)
    resultado = []
    for subject, body in emails:
        texto = f"{subject}\n{body[:500]}"
        categoria = clasificar_correo(texto)
        resultado.append({
            "asunto": subject,
            "cuerpo": body,
            "categoria": categoria
        })
    return jsonify(resultado)
