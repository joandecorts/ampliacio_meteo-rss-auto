"""
CONFIGURACIÓ BANNER NEWS CHANNEL - VERSIÓ DADES REALS
Configuració per al sistema de banner meteorològic amb dades reals de Meteocat
"""

import os
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURACIÓ DE LES 15 ESTACIONS (codis verificats)
# ============================================================================
STATIONS = [
    # 20 Estacions
    {'code': 'XJ', 'name': 'GIRONA', 'display_name': 'GIRONA'},
    {'code': 'UO', 'name': 'FORNELLS', 'display_name': 'FORNELLS DE LA SELVA'},
    {'code': 'D4', 'name': 'ROSES', 'display_name': 'ROSES'},
    {'code': 'CD', 'name': 'SEU_URGELL', 'display_name': 'LA SEU D\'URGELL - BELLESTAR'},
    {'code': 'YP', 'name': 'PALAFRUGELL', 'display_name': 'PALAFRUGELL'},
    {'code': 'XL', 'name': 'PRAT_LLOBREGAT', 'display_name': 'EL PRAT DE LLOBREGAT'},
    {'code': 'DJ', 'name': 'BANYOLES', 'display_name': 'BANYOLES'},
    {'code': 'DP', 'name': 'DAS', 'display_name': 'DAS - AERÒDROM'},
    {'code': 'X4', 'name': 'BARCELONA_RAVAL', 'display_name': 'BARCELONA - EL RAVAL'},
    {'code': 'VK', 'name': 'LLEIDA_RAIMAT', 'display_name': 'LLEIDA - RAIMAT'},
    {'code': 'XE', 'name': 'TARRAGONA', 'display_name': 'TARRAGONA - COMPLEX EDUCATIU'},
    {'code': 'DG', 'name': 'QUERALBS_NURIA', 'display_name': 'QUERALBS - NÚRIA (1.971 m)'},
    {'code': 'ZC', 'name': 'SETCASES_ULLDETER', 'display_name': 'SETCASES - ULLDETER (2.413 m)'},
    {'code': 'UN', 'name': 'CASSÀ DE LA SELVA', 'display_name': 'CASSÀ DE LA SELVA'},
    {'code': 'X5', 'name': 'PN DELS PORTS', 'display_name': 'ROQUETES - PN DELS PORTS'},
    {'code': 'YB', 'name': 'OLOT', 'display_name': 'OLOT'},
    {'code': 'CI', 'name': 'SANT PAU DE SEGÚRIES', 'display_name': 'SANT PAU DE SEGÚRIES'},
    {'code': 'XK', 'name': 'PUIG SESOLLES', 'display_name': 'PUIG SESOLLES (1.668 M)'},  
    {'code': 'VS', 'name': 'LAC REDON', 'display_name': 'LAC REDON (2.247 M)'}, 
    {'code': 'DN', 'name': 'ANGLÈS', 'display_name': 'ANGLÈS'}
]

# ============================================================================
# VARIABLES METEOROLÒGIQUES A CAPTURAR
# ============================================================================
VARIABLES = {
    'TX': 'Temperatura màxima (°C)',
    'TN': 'Temperatura mínima (°C)', 
    'PPT': 'Precipitació (mm)'
}

# ============================================================================
# CONFIGURACIÓ DE RUTES
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Fitxers de dades
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

LATEST_DATA_FILE = os.path.join(DATA_DIR, 'latest_weather.json')
HISTORICAL_DIR = os.path.join(DATA_DIR, 'historical')
os.makedirs(HISTORICAL_DIR, exist_ok=True)

# Fitxers HTML
HTML_TEMPLATE = os.path.join(BASE_DIR, 'banner_news_channel.html')
OUTPUT_HTML = os.path.join(BASE_DIR, 'banner_output.html')  # Aquest usarà OBS

# ============================================================================
# CONFIGURACIÓ API METEOCAT (COMENTADA - NO LA NECESSITEM ARA)
# ============================================================================
METEOcat_CONFIG = {
    'api_base': 'https://api.meteo.cat/v1',
    'timeout': 30,
    'max_retries': 3,
    'backoff_factor': 2
}

# MODIFICACIÓ: No comprovem la clau API, no la necessitem per a web scraping
# Si en un futur vols utilitzar l'API, descomenta això:
# API_KEY = os.environ.get('METEOcat_API_KEY', '')
# if not API_KEY:
#     print("⚠️  MODE WEB SCRAPING: No s'ha trobat clau API.")

API_KEY = None  # El deixem com a None per no causar errors

# ============================================================================
# CONFIGURACIÓ DE TEMPS
# ============================================================================
# Període de dades (avui)
TODAY = datetime.now().date()
YESTERDAY = TODAY - timedelta(days=1)

# Scroll del banner
SCROLL_CONFIG = {
    'transition_duration': 0.8,
    'display_duration': 15,
    'stations_per_view': 2  # Quantes estacions es mostren alhora
}

# ============================================================================
# FUNCIONS UTILS
# ============================================================================
def get_current_datetime():
    """Retorna la data i hora actual formatejada"""
    now = datetime.now()
    return {
        'time': now.strftime('%H:%M'),
        'date': now.strftime('%d/%m/%Y'),
        'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
        'timestamp': int(now.timestamp())
    }

def get_update_text():
    """Retorna el text d'actualització per al peu del banner"""
    current = get_current_datetime()
    return f"Actualitzat: {current['time']} - Data: {current['date']}"

def get_station_file_path(station_code):
    """Retorna la ruta del fitxer històric per una estació"""
    return os.path.join(HISTORICAL_DIR, f"{station_code}.json")

# ============================================================================
# VALORS PER DEFECTE (si no hi ha dades)
# ============================================================================
DEFAULT_VALUES = {
    'TX': '--',  # Temperatura màxima
    'TN': '--',  # Temperatura mínima
    'PPT': '--'  # Precipitació
}
