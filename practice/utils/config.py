import os

# Obtiene la ruta absoluta del directorio donde se encuentra este archivo config.py
# Esto resultará en algo como '.../ATP/practice/utils'
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Navega un nivel arriba para llegar a la raíz de tu paquete principal 'practice'
# CURRENT_DIR = '.../ATP/practice/utils'
# os.path.dirname(CURRENT_DIR) = '.../ATP/practice'
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) 

# --- Configuración de URLs ---
BASE_URL = "https://testautomationpractice.blogspot.com"

# --- Rutas de Almacenamiento de Evidencias ---

# Directorio base donde se guardarán todas las evidencias.
# Construye la ruta absoluta para que apunte a '.../ATP/practice/test/reportes'
EVIDENCE_BASE_DIR = os.path.join(PROJECT_ROOT, "test", "reportes")

# Ruta para videos.
# Se creará '.../ATP/practice/test/reportes/video'
VIDEO_DIR = os.path.join(EVIDENCE_BASE_DIR, "video")

# Ruta para traceview.
# Se creará '.../ATP/practice/test/reportes/traceview'
TRACEVIEW_DIR = os.path.join(EVIDENCE_BASE_DIR, "traceview")

# Ruta para capturas de pantalla.
# Se creará '.../ATP/practice/test/reportes/imagen'
SCREENSHOT_DIR = os.path.join(EVIDENCE_BASE_DIR, "imagen")

# --- Nueva ruta para archivos fuente ---
# Se creará '.../ATP/practice/test/archivos_fuentes'
SOURCE_FILES_DIR = os.path.join(PROJECT_ROOT, "test", "archivos_fuentes")

# Función para asegurar que los directorios existan
def ensure_directories_exist():
    """
    Crea los directorios necesarios si no existen.
    """
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(TRACEVIEW_DIR, exist_ok=True)
    os.makedirs(SCREENSHOT_DIR, exist_ok=True) 
    os.makedirs(SOURCE_FILES_DIR, exist_ok=True) # Asegúrate de crear también este directorio

# Llama a la función para asegurar que los directorios se creen al importar este módulo
ensure_directories_exist()
