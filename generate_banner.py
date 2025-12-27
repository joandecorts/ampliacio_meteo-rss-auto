"""
Genera el fitxer HTML amb el banner meteorològic - VERSIÓ DEFINITIVA
Utilitza banner_news_channel.html com a template
AMB HORA LOCAL I DATA dd/mm/yyyy
"""

import json
from datetime import datetime, timezone, timedelta
import os

def load_template(template_file="banner_news_channel.html"):
    """Carrega el template HTML"""
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error carregant template: {e}")
        return None

def generate_station_html(station_data):
    """
    Genera el HTML per una estació individual
    """
    if not station_data.get('success'):
        return ""
    
    metadata = station_data['metadata']
    values = station_data['values']
    
    station_name = metadata['name']
    tx = values.get('TX', '-')
    tn = values.get('TN', '-')
    ppt = values.get('PPT', '-')
    
    # Formatejar valors (ja venen arrodonits del scraper)
    tx_display = f"{tx}" if tx != '-' else "-"
    tn_display = f"{tn}" if tn != '-' else "-"
    ppt_display = f"{ppt}" if ppt != '-' else "-"
    
    # HORA LOCAL (Catalunya, UTC+1) i DATA dd/mm/yyyy
    utc_time = datetime.now(timezone.utc)
    local_time = utc_time + timedelta(hours=1)  # UTC+1 per Catalunya
    hora_local = local_time.strftime("%H:%M")
    data_local = local_time.strftime("%d/%m/%Y")
    
    return f"""
            <div class="content-group">
                <div class="location-header">
                    <div class="location-name">{station_name}</div>
                </div>
                <div class="data-container">
                    <div class="data-box">
                        <div class="data-title">Temp. màxima</div>
                        <div class="data-value">{tx_display}<span class="data-unit">°C</span></div>
                    </div>
                    <div class="data-box">
                        <div class="data-title">Temp. mínima</div>
                        <div class="data-value">{tn_display}<span class="data-unit">°C</span></div>
                    </div>
                    <div class="data-box">
                        <div class="data-title">Pluja acumulada</div>
                        <div class="data-value">{ppt_display}<span class="data-unit">mm</span></div>
                    </div>
                </div>
                <!-- CANVIS AQUÍ: Hora local i data dd/mm/yyyy -->
                <div class="footer">
                    <div class="update-info">Actualitzat: {hora_local} - Data: {data_local}</div>
                    <div class="source">Font: https://www.meteo.cat/</div>
                </div>
            </div>
    """

def main():
    """Funció principal"""
    print("🎨 Generant banner meteorològic...")
    
    # 1. Carregar template
    template = load_template()
    if not template:
        return
    
    # 2. Carregar dades meteorològiques
    data_file = "data/latest_weather.json"
    if not os.path.exists(data_file):
        print(f"❌ El fitxer {data_file} no existeix")
        print("   Executa primer meteo_scraper.py per obtenir dades")
        return
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error llegint dades: {e}")
        return
    
    stations = data.get('stations', {})
    
    # 3. Generar HTML per a cada estació
    stations_html = ""
    station_count = 0
    
    for station_id, station_data in stations.items():
        if station_data.get('success'):
            station_html = generate_station_html(station_data)
            if station_html:
                stations_html += station_html
                station_count += 1
    
    # 4. Si no hi ha dades, mostrar missatge (AMB HORA LOCAL)
    if station_count == 0:
        # Hora local també per a sense dades
        utc_time = datetime.now(timezone.utc)
        local_time = utc_time + timedelta(hours=1)
        hora_local = local_time.strftime("%H:%M")
        data_local = local_time.strftime("%d/%m/%Y")
        
        stations_html = f"""
            <div class="content-group active">
                <div class="location-header">
                    <div class="location-name">SENSE DADES</div>
                </div>
                <div class="data-container">
                    <div class="data-box">
                        <div class="data-title">Temperatura màxima</div>
                        <div class="data-value">-<span class="data-unit">°C</span></div>
                    </div>
                    <div class="data-box">
                        <div class="data-title">Temperatura mínima</div>
                        <div class="data-value">-<span class="data-unit">°C</span></div>
                    </div>
                    <div class="data-box">
                        <div class="data-title">Pluja acumulada</div>
                        <div class="data-value">-<span class="data-unit">mm</span></div>
                    </div>
                </div>
                <!-- CANVIS AQUÍ també -->
                <div class="footer">
                    <div class="update-info">Actualitzat: {hora_local} - Data: {data_local}</div>
                    <div class="source">Font: https://www.meteo.cat/</div>
                </div>
            </div>
        """
    
    # 5. Injectar stations_html al template
    # Buscar el div.scroll-container i reemplaçar el seu contingut
    start_marker = '<div class="scroll-container">'
    end_marker = '</div>\n    </div>'  # Tancament de .scroll-container + .weather-container
    
    start_idx = template.find(start_marker)
    end_idx = template.find(end_marker, start_idx)
    
    if start_idx != -1 and end_idx != -1:
        # Mantenir el div.scroll-container obert i tancat
        new_content = f'{start_marker}\n            {stations_html}\n        </div>'
        updated_template = template[:start_idx] + new_content + template[end_idx:]
    else:
        # Fallback: reemplaçar manualment
        placeholder = '<!-- EL CONTINGUT D\'AQUÍ ES REEMPLAÇARÀ COMPLETAMENT PER update_banner.py -->'
        updated_template = template.replace(placeholder, stations_html)
    
    # 6. Guardar fitxer
    output_file = "banner_output.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_template)
    
    print(f"✅ Banner generat amb {station_count} estacions")
    print(f"🏁 Fitxer: {output_file}")
    
    # 7. També generar index.html (per GitHub Pages)
    with open("index.html", 'w', encoding='utf-8') as f:
        f.write(updated_template)
    print("📄 index.html actualitzat")

if __name__ == "__main__":
    main()
