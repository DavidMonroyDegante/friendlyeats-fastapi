
import os

from google.cloud import firestore

from app.core.config import settings


# Configurar el emulador local
if settings.FIRESTORE_EMULATOR_HOST:
    os.environ["FIRESTORE_EMULATOR_HOST"] = (
        settings.FIRESTORE_EMULATOR_HOST
    )

# Configurar el proyecto de prueba
os.environ["GCLOUD_PROJECT"] = settings.FIREBASE_PROJECT_ID

# Crear el cliente de Firestore para el emulador
db = firestore.Client(
    project=settings.FIREBASE_PROJECT_ID
)