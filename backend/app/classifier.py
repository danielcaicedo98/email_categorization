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
labels = ["Profesional", "Personal", "Finanzas", "Citas", "Spam", "Facturas", "General", "Académico"]

# --- Funciones auxiliares para limpieza de texto ---

# --- Función de clasificación de texto usando zero-shot ---
def clasificar_correo(texto):
    resultado = classifier(texto, labels)  # Clasifica el texto según las etiquetas definidas
    return resultado['labels'][0]  # Retorna la etiqueta más probable