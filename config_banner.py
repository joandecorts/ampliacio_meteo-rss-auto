"""
CONFIGURACIÓ BANNER NEWS CHANNEL
Configuració per al sistema de banner meteorològic per OBS
"""

import os
from datetime import datetime

# ============================================================================
# CONFIGURACIÓ DE LES ESTACIONS
# ============================================================================
STATIONS = [
    {
        'id': 'XO',
        'name': 'GIRONA',
        'display_name': 'GIRONA',
        'meteocat_code': 'XO'
    },
    {
        'id': 'XL',
        'name': 'FORNELLS',
        'display_name': 'FORNELLS DE LA SELVA',
        'meteocat_code': 'XL'
    }
]

# ============================================================================
# CONFIGURACIÓ DE RUTES
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_TEMPLATE = os.path.join(BASE_DIR, 'banner_news_channel.html')
OUTPUT_HTML = os.path.join(BASE_DIR, 'banner_output.html')
DATA_FILE = os.path.join(BASE_DIR, 'weather_data.json')

# ============================================================================
# CONFIGURACIÓ VISUAL
# ============================================================================
STYLE_CONFIG = {
    'header_bg_color': '#c00',
    'header_text_color': '#ffffff',
    'box_border_color': '#e0e0e0',
    'box_shadow': '0 3px 8px rgba(0,0,0,0.08)',
    'text_color_primary': '#000000',
    'text_color_secondary': '#333333',
    'text_color_footer': '#666666'
}

# ============================================================================
# CONFIGURACIÓ DE TEMPS
# ============================================================================
SCROLL_CONFIG = {
    'transition_duration': 0.8,
    'display_duration': 15,
    'update_interval': 15
}

# ============================================================================
# CONFIGURACIÓ METEOcat API
# ============================================================================
METEOcat_CONFIG = {
    'api_base': 'https://api.meteo.cat/v1',
    'timeout': 10,
    'max_retries': 3
}

# ============================================================================
# MISSATGES I TEXTOS
# ============================================================================
TEXTS = {
    'max_temp': 'Temperatura màxima del dia',
    'min_temp': 'Temperatura mínima del dia', 
    'rainfall': 'Pluja acumulada',
    'updated': 'Actualitzat',
    'source': 'Font',
    'date_format': '%H:%M - Data: %d/%m/%Y'
}

# ============================================================================
# FUNCIONS UTILS
# ============================================================================
def get_current_time():
    """Retorna l'hora actual formatejada"""
    return datetime.now().strftime('%H:%M')

def get_current_date():
    """Retorna la data actual formatejada"""
    return datetime.now().strftime('%d/%m/%Y')

def get_update_text():
    """Retorna el text d'actualització complet"""
    return f"{TEXTS['updated']}: {get_current_time()} - Data: {get_current_date()}"
