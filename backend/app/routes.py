from flask import Blueprint, jsonify
from .email_utils import get_emails_imap
from .classifier import clasificar_correo
from .config import EMAIL_USER, EMAIL_PASSWORD

main = Blueprint("main", __name__)

@main.route("/correos")
def obtener_correos():
    global emails_cache
    if not emails_cache:
        print("⌛ Cargando correos y clasificando...")
        emails = get_emails_imap(EMAIL_USER, EMAIL_PASSWORD, max_emails=10)
        for subject, body in emails:
            texto = f"{subject}\n{body[:500]}"
            categoria = clasificar_correo(texto)
            emails_cache.append({
                "asunto": subject,
                "cuerpo": body,
                "categoria": categoria
            })
        print("✅ Correos cargados y clasificados.")
    else:
        print("⚡ Usando correos cacheados.")

    return jsonify(emails_cache)
