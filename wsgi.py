"""
WSGI configuration for PythonAnywhere

Questo file va configurato in PythonAnywhere nella sezione Web > WSGI configuration file
"""
import sys
import os
from dotenv import load_dotenv

# Aggiungi il path del progetto
project_home = '/home/TUOUSERNAME/myAriel'  # IMPORTANTE: Cambia TUOUSERNAME con il tuo username PythonAnywhere
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Carica variabili d'ambiente
dotenv_path = os.path.join(project_home, '.env')
load_dotenv(dotenv_path)

# Importa l'applicazione Flask
from app import app as application
