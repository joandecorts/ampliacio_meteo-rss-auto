#!/usr/bin/env python3
"""
UPDATE BANNER - Actualitza el banner HTML amb dades reals
"""

import json
import os
import sys
from datetime import datetime

import config_banner as cfg

def load_latest_data():
    """Carrega les dades més recents del fitxer JSON"""
    try:
        with open(cfg.LATEST_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ No es troba el fitxer de dades: {cfg.LATEST_DATA_FILE}")
        print("   Executa primer: python meteo_scraper.py")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error llegint JSON: {e}")
        return None

def read_html_template():
    """Llegeix la plantilla HTML"""
    try:
        with open(cfg.HTML_TEMPLATE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ No es troba la plantilla: {cfg.HTML_TEMPLATE}")
        return None

def create_station_html(station_config, station_data):
    """
    Crea el bloc HTML per una estació amb dades reals
    
    station_config: dict amb {code, name, display_name}
    station_data: dict amb {values: {TX, TN, PPT}}
    """
    code = station_config['code']
    display_name = station_config['display_name']
    
    # Obtenir valors (o defaults si no hi ha)
    if station_data and station_data.get('success'):
        values = station_data.get('values', cfg.DEFAULT_VALUES)
        tx = values.get('TX', '--')
        tn = values.get('TN', '--') 
        ppt = values.get('PPT', '--')
    else:
        tx, tn, ppt = cfg.DEFAULT_VALUES['TX'], cfg.DEFAULT_VALUES['TN'], cfg.DEFAULT_VALUES['PPT']
    
    # Crear HTML
    html = f'''
            <!-- GRUP: {display_name} -->
            <div class="content-group" id="group{code}">
                <div class="location-header">
                    <div class="location-name">{display_name}</div>
                </div>
                
                <div class="data-container">
                    <div class="data-box">
                        <div class="data-title br-2">Temperatura<br>màxima del dia</div>
                        <div class="data-value">{tx}<span class="data-unit">°C</span></div>
                    </div>
                    
                    <div class="data-box">
                        <div class="data-title br-2">Temperatura<br>mínima del dia</div>
                        <div class="data-value">{tn}<span class="data-unit">°C</span></div>
                    </div>
                    
                    <div class="data-box">
                        <div class="data-title">Pluja acumulada</div>
                        <div class="data-value">{ppt}<span class="data-unit">mm</span></div>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="update-info">{cfg.get_update_text()}</div>
                    <div class="source">Font: https://www.meteo.cat/</div>
                </div>
            </div>
    '''
    
    return html

def generate_banner_html(weather_data):
    """
    Genera l'HTML complet del banner amb totes les estacions
    """
    # Llegir plantilla
    template = read_html_template()
    if template is None:
        return None
    
    # Obtenir dades per estació
    stations_data = weather_data.get('stations', {}) if weather_data else {}
    
    # Generar contingut de totes les estacions
    all_stations_html = ""
    
    for i, station_config in enumerate(cfg.STATIONS):
        station_code = station_config['code']
        station_data = stations_data.get(station_code, {})
        
        station_html = create_station_html(station_config, station_data)
        all_stations_html += station_html + "\n\n"
    
    # Reemplaçar el contingut al template
    # Busquem el punt on comença el primer grup
    lines = template.split('\n')
    
    # Trobar l'inici del primer grup
    start_index = None
    end_index = None
    
    for i, line in enumerate(lines):
        if '<!-- GRUP: GIRONA -->' in line or '<!-- GRUP 1: GIRONA -->' in line:
            start_index = i
            # Buscar el següent comentari de grup o final
            for j in range(i+1, len(lines)):
                if '<!-- GRUP:' in lines[j] or '<!-- GRUP ' in lines[j]:
                    end_index = j
                    break
            if end_index is None:
                end_index = len(lines)
            break
    
    if start_index is not None and end_index is not None:
        # Reemplaçar
        new_lines = lines[:start_index] + [all_stations_html.strip()] + lines[end_index:]
        return '\n'.join(new_lines)
    else:
        print("⚠️  No s'ha trobat el marcador de grups al template")
        # Intentar reemplaçar de manera simple
        return template.replace(
            '<!-- GRUP 1: GIRONA -->',
            all_stations_html.strip()
        )

def save_banner_html(html_content):
    """Guarda l'HTML generat"""
    try:
        with open(cfg.OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Banner actualitzat: {cfg.OUTPUT_HTML}")
        return True
        
    except Exception as e:
        print(f"❌ Error guardant banner: {e}")
        return False

def main():
    """Funció principal"""
    print("=" * 50)
    print("ACTUALITZADOR DE BANNER - Dades reals Meteocat")
    print("=" * 50)
    
    # 1. Carregar dades
    print("\n[1] Carregant dades meteorològiques...")
    weather_data = load_latest_data()
    
    if weather_data is None:
        # Crear dades de prova per desenvolupament
        print("   ⚠️  Utilitzant dades de prova per desenvolupament")
        weather_data = {
            'metadata': {'last_updated': datetime.now().isoformat()},
            'stations': {}
        }
    
    # 2. Generar HTML
    print("\n[2] Generant HTML amb dades reals...")
    banner_html = generate_banner_html(weather_data)
    
    if banner_html is None:
        print("❌ Error generant HTML")
        return 1
    
    # 3. Guardar fitxer
    print("\n[3] Guardant banner actualitzat...")
    if save_banner_html(banner_html):
        print(f"\n🎉 BANNER ACTUALITZAT AMB ÈXIT")
        print(f"   Fitxer: {cfg.OUTPUT_HTML}")
        print(f"   Estacions: {len(cfg.STATIONS)}")
        print(f"   {cfg.get_update_text()}")
        print(f"\n🔧 Recorda canviar OBS a: {cfg.OUTPUT_HTML}")
        return 0
    else:
        print("\n❌ ERROR ACTUALITZANT BANNER")
        return 1

if __name__ == "__main__":
    sys.exit(main())
