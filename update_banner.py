#!/usr/bin/env python3
"""
UPDATE BANNER - Actualitza el banner HTML amb dades reals (VERSIÓ TOLERANT)
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

def create_station_html(station_config, station_data, index):
    """
    Crea el bloc HTML per una estació amb dades reals
    """
    code = station_config['code']
    display_name = station_config['display_name']
    
    if station_data and station_data.get('success'):
        values = station_data.get('values', cfg.DEFAULT_VALUES)
        tx = values.get('TX', '--')
        tn = values.get('TN', '--')
        ppt = values.get('PPT', '--')
    else:
        tx, tn, ppt = cfg.DEFAULT_VALUES['TX'], cfg.DEFAULT_VALUES['TN'], cfg.DEFAULT_VALUES['PPT']
    
    # Determinar classes CSS per al JavaScript corregit
    css_class = 'content-group next'
    if index == 0:
        css_class = 'content-group active'  # La primera és visible
    elif index == 1:
        css_class = 'content-group next'    # La següent en línia
    
    html = f'''
            <!-- GRUP: {display_name} -->
            <div class="{css_class}" id="station{index}">
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
    VERSIÓ TOLERANT: Substitueix tot entre scroll-container
    """
    template = read_html_template()
    if template is None:
        return None
    
    stations_data = weather_data.get('stations', {}) if weather_data else {}
    
    # Generar HTML de TOTES les estacions
    all_stations_html = ""
    for i, station_config in enumerate(cfg.STATIONS):
        station_code = station_config['code']
        station_data = stations_data.get(station_code, {})
        all_stations_html += create_station_html(station_config, station_data, i) + "\n\n"
    
    # --- PART CLAU: SUBSTITUIR DES DE '<div class="scroll-container">' FINS AL FINAL ---
    start_marker = '<div class="scroll-container">'
    
    # Trobar la posició inicial
    start_index = template.find(start_marker)
    if start_index == -1:
        print("❌ No s'ha trobat l'inici del scroll-container")
        return None
    
    # Buscar la posició on comença el tancament del contenidor scroll
    # Primer trobem el proper '</div>' després del nostre marcador
    end_search_start = start_index + len(start_marker)
    
    # Fem una cerca simple: trobar el primer '</div>' després del marcador
    end_index = template.find('</div>', end_search_start)
    
    if end_index == -1:
        print("❌ No s'ha trobat el final del contenidor")
        return None
    
    # Ara retrocedim per assegurar-nos que aquest és el tancament del scroll-container
    # Comptem quants '<div' hi ha entre start_index i end_index
    temp_section = template[start_index:end_index]
    div_count = temp_section.count('<div')
    
    # Si hi ha més d'un div obert, trobem el tancament corresponent
    if div_count > 1:
        # Busquem el tancament que iguala el nombre de divs oberts
        close_tags_needed = div_count
        current_pos = end_index
        close_tags_found = 0
        
        while close_tags_found < close_tags_needed:
            next_close = template.find('</div>', current_pos + 1)
            if next_close == -1:
                break
            current_pos = next_close
            close_tags_found += 1
        
        end_index = current_pos + len('</div>')
    
    # Crear el nou HTML
    new_html = (
        template[:start_index + len(start_marker)] +  # Tot fins on comença el scroll
        "\n" + all_stations_html.strip() + "\n" +     # Els nostres nous grups
        template[end_index:]                          # Des del final del scroll en endavant
    )
    
    return new_html

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
    
    print("\n[1] Carregant dades meteorològiques...")
    weather_data = load_latest_data()
    
    if weather_data is None:
        print("   ⚠️  Utilitzant dades de prova per desenvolupament")
        weather_data = {
            'metadata': {'last_updated': datetime.now().isoformat()},
            'stations': {}
        }
    
    print("\n[2] Generant HTML amb dades reals...")
    banner_html = generate_banner_html(weather_data)
    
    if banner_html is None:
        print("❌ Error generant HTML")
        return 1
    
    print("\n[3] Guardant banner actualitzat...")
    if save_banner_html(banner_html):
        print(f"\n🎉 BANNER ACTUALITZAT AMB ÈXIT")
        print(f"   Fitxer: {cfg.OUTPUT_HTML}")
        print(f"   Estacions: {len(cfg.STATIONS)}")
        print(f"   {cfg.get_update_text()}")
        return 0
    else:
        print("\n❌ ERROR ACTUALITZANT BANNER")
        return 1

if __name__ == "__main__":
    sys.exit(main())