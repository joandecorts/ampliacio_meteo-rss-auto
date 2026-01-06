"""
CONFIGURACIÓ BANNER NEWS CHANNEL - VERSIÓ DADES REALS
Configuració per al sistema de banner meteorològic amb dades reals de Meteocat
Fitxer generat automàticament: 2026-01-06 20:17:57
Total estacions: 25 (Actives: 25, Comentades: 0)
"""

import os
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURACIÓ DE LES ESTACIONS (25 estacions)
# ============================================================================
STATIONS = [
    {'code': 'DN', 'name': 'ANGLES', 'display_name': 'ANGLÈS'},
    {'code': 'DJ', 'name': 'BANYOLES', 'display_name': 'BANYOLES'},
    {'code': 'X4', 'name': 'BARCELONA_RAVAL', 'display_name': 'BARCELONA - EL RAVAL'},
    {'code': 'UN', 'name': 'CASSÀ_DE_LA_SELVA', 'display_name': 'CASSÀ DE LA SELVA'},
    {'code': 'MS', 'name': 'CASTELLAR_DE_NHUG', 'display_name': 'CASTELLAR DE N\'HUG'},
    {'code': 'J5', 'name': 'DARNIUS', 'display_name': 'DARNIUS - PANTÀ DE DARNIUS - BOADELLA'},
    {'code': 'DP', 'name': 'DAS', 'display_name': 'DAS - AERÒDROM'},
    {'code': 'XL', 'name': 'PRAT_LLOBREGAT', 'display_name': 'EL PRAT DE LLOBREGAT'},
    {'code': 'XK', 'name': 'PUIG_SESOLLES', 'display_name': 'PUIG SESOLLES (1.668 m)'},
    {'code': 'UO', 'name': 'FORNELLS', 'display_name': 'FORNELLS DE LA SELVA'},
    {'code': 'XJ', 'name': 'GIRONA', 'display_name': 'GIRONA'},
    {'code': 'CD', 'name': 'SEU_URGELL', 'display_name': 'LA SEU D\'URGELL - BELLESTAR'},
    {'code': 'VK', 'name': 'LLEIDA_RAIMAT', 'display_name': 'LLEIDA - RAIMAT'},
    {'code': 'Z3', 'name': 'MERANGES', 'display_name': 'MERANGES - MALNIU (2.230 m)'},
    {'code': 'YB', 'name': 'OLOT', 'display_name': 'OLOT'},
    {'code': 'YP', 'name': 'PALAFRUGELL', 'display_name': 'PALAFRUGELL'},
    {'code': 'DG', 'name': 'QUERALBS_NURIA', 'display_name': 'QUERALBS - NÚRIA (1.971 m)'},
    {'code': 'D4', 'name': 'ROSES', 'display_name': 'ROSES'},
    {'code': 'CI', 'name': 'SANT_PAU_SEGURIES', 'display_name': 'SANT PAU DE SEGÚRIES'},
    {'code': 'ZC', 'name': 'SETCASES_ULLDETER', 'display_name': 'SETCASES-ULLDETER (2.413 m)'},
    {'code': 'XH', 'name': 'SORT', 'display_name': 'SORT'},
    {'code': 'XE', 'name': 'TARRAGONA', 'display_name': 'TARRAGONA - COMPLEX EDUCATIU'},
    {'code': 'XO', 'name': 'VIC', 'display_name': 'VIC'},
    {'code': 'VS', 'name': 'LAC_REDON', 'display_name': 'LAC REDON (2.247 m)'},
    {'code': 'D7', 'name': 'VINEBRE', 'display_name': 'VINEBRE'},
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
OUTPUT_HTML = os.path.join(BASE_DIR, 'banner_output.html')

# ============================================================================
# CONFIGURACIÓ API METEOCAT
# ============================================================================
METEOcat_CONFIG = {
    'api_base': 'https://api.meteo.cat/v1',
    'timeout': 30,
    'max_retries': 3,
    'backoff_factor': 2
}

API_KEY = None  # Modo web scraping

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
    'stations_per_view': 2
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
# VALORS PER DEFECTE
# ============================================================================
DEFAULT_VALUES = {
    'TX': '--',
    'TN': '--',
    'PPT': '--'
}

# ============================================================================
# INFORMACIÓ DE GENERACIÓ
# ============================================================================
GENERATION_INFO = {
    'generated_at': '2026-01-06 20:17:57',
    'total_stations': 25,
    'active_stations': 25,
    'commented_stations': 0,
    'false_stations': 0,
    'config_banner_version': 'v2.0 - Lògica: Op+CERT+Activa',
    'generator': 'ConfiguradorEstacions v2.0'
}

# ============================================================================
# COMPROVACIÓ INICIAL
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print(f"CONFIG_BANNER.PY - VERSIÓ {GENERATION_INFO['config_banner_version']}")
    print("=" * 70)
    print(f"📊 Total estacions: {len(STATIONS)}")
    print(f"✅ Actives: {GENERATION_INFO['active_stations']}")
    print(f"💬 Comentades: {GENERATION_INFO['commented_stations']}")
    print(f"🗑️ Desmantellades: {GENERATION_INFO['false_stations']}")
    print("=" * 70)
    
    for i, station in enumerate(STATIONS, 1):
        if i <= GENERATION_INFO['active_stations']:
            status = "✅"
        elif i <= GENERATION_INFO['active_stations'] + GENERATION_INFO['commented_stations']:
            status = "💬"
        else:
            status = "🗑️"
        
        print(f"  {status} {i:2}. {station['code']} - {station['display_name']}")
    
    print("=" * 70)
    print(f"🚀 Configuració carregada correctament!")
    print(f"💾 Dades actualitzades: {GENERATION_INFO['generated_at']}")
    print("=" * 70)
