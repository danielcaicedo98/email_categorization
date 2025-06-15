# Importación de librerías necesarias
import os  # Para acceder a variables de entorno del sistema
from dotenv import load_dotenv  # Para cargar variables desde un archivo .env
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification  # Para usar el modelo NLP

# --- Configuración inicial ---

# Cargar las variables de entorno desde un archivo .env (como EMAIL_USER y EMAIL_PASSWORD)
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")  # Usuario del correo
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Contraseña (o app password) del correo

# Cargar el modelo multilingüe de clasificación de textos (compatible con español)
model_name = "joeddav/xlm-roberta-large-xnli"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Crear un clasificador de tipo zero-shot (sin entrenamiento previo en las categorías)
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# Etiquetas en español que se usarán para clasificar los correos
labels_en = [
    "Este correo está relacionado con el trabajo, negocios o comunicación profesional",
    "Este correo es un mensaje personal de un amigo o familiar",
    "Este correo trata sobre una cita, evento o reunión programada",
    "Este correo contiene una transacción, factura, recibo, comprobante de pago o confirmación",
    "Este correo está relacionado con cuentas bancarias, servicios financieros o inversiones",
    "Este correo es spam, una estafa o un anuncio no deseado",
    "Este correo es un mensaje general que no entra en categorías específicas",
    "Este correo está relacionado con la escuela, universidad o temas académicos"
]


label_map = {
    "Este correo está relacionado con el trabajo, negocios o comunicación profesional": "Profesional",
    "Este correo es un mensaje personal de un amigo o familiar": "Personal",
    "Este correo trata sobre una cita, evento o reunión programada": "Citas",
    "Este correo contiene una transacción, factura, recibo, comprobante de pago o confirmación": "Factura",
    "Este correo está relacionado con cuentas bancarias, servicios financieros o inversiones": "Finanzas",
    "Este correo es spam, una estafa o un anuncio no deseado": "Spam",
    "Este correo es un mensaje general que no entra en categorías específicas": "General",
    "Este correo está relacionado con la escuela, universidad o temas académicos": "Académico"
}
# --- Funciones auxiliares para limpieza de texto ---

# --- Función de clasificación de texto usando zero-shot ---
def clasificar_correo(texto):
    resultado = classifier(texto, labels_en)  # Clasifica el texto según las etiquetas definidas
    return resultado['labels'][0]  # Retorna la etiqueta más probable