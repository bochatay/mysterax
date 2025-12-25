from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Charger le fichier .env si présent
load_dotenv()

class Settings(BaseSettings):
    # Définir les variables d'environnement
    debug: bool = False  # Valeur par défaut si la variable n'est pas définie

    class Config:
        env_file = ".env"  # Charger les variables d'environnement depuis .env
        env_file_encoding = 'utf-8'

# Créer une instance de Settings
settings = Settings()

