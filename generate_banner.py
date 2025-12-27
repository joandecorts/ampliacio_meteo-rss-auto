"""
Genera el fitxer HTML amb el banner meteorològic - VERSIÓ DEFINITIVA
Amb caixes individuals per cada dada (com la foto IMG_6531.PNG)
"""

import json
from datetime import datetime, timezone, timedelta
import os

def generate_banner_with_boxes():
    """Genera el banner amb caixes individuals (com la teva foto)"""
    
    # 1. Carregar dades
    data_file = "data/latest_weather.json"
    if not os.path.exists(data_file):
        print(f"❌ El fitxer {data_file} no existeix")
        return None
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error llegint dades: {e}")
        return None
    
    stations = data.get('stations', {})
    
    # 2. Generar HTML per a cada estació
    stations_html = ""
    
    for station_id, station_data in stations.items():
        if station_data.get('success'):
            metadata = station_data['metadata']
            values = station_data['values']
            
            station_name = metadata['name']
            tx = values.get('TX', '-')
            tn = values.get('TN', '-')
            ppt = values.get('PPT', '-')
            
            # Formatejar valors
            tx_display = f"{tx}°C" if tx != '-' else "-"
            tn_display = f"{tn}°C" if tn != '-' else "-"
            ppt_display = f"{ppt} mm" if ppt != '-' else "-"
            
            # Hora local (Catalunya, UTC+1)
            utc_time = datetime.now(timezone.utc)
            local_time = utc_time + timedelta(hours=1)  # UTC+1 per Catalunya
            hora_actual = local_time.strftime("%H:%M")
            data_actual = local_time.strftime("%d/%m/%Y")
            
            # HTML de l'estació (AMB CAIXES INDIVIDUALS)
            station_html = f"""
            <div style="margin: 15px auto; padding: 0; max-width: 800px; background: #fff; border-radius: 0; font-family: Arial, sans-serif;">
                <!-- TÍTOL -->
                <h1 style="color: #c00; text-align: center; margin: 0 0 20px 0; padding: 15px 0; background: #f8f8f8; border-bottom: 2px solid #ddd;">
                    {station_name}
                </h1>
                
                <!-- TRES CAIXES EN FILES SEPARADES -->
                <div style="padding: 15px;">
                    <!-- Fila 1: Temp. màx -->
                    <div style="margin-bottom: 15px; border: 2px solid #e0e0e0; border-radius: 8px; padding: 15px; background: #fafafa;">
                        <div style="font-weight: bold; font-size: 16px; color: #333; margin-bottom: 8px;">
                            Temperatura máxima del día
                        </div>
                        <div style="font-size: 36px; font-weight: bold; color: #c00; text-align: center;">
                            {tx_display}
                        </div>
                    </div>
                    
                    <!-- Fila 2: Temp. mín -->
                    <div style="margin-bottom: 15px; border: 2px solid #e0e0e0; border-radius: 8px; padding: 15px; background: #fafafa;">
                        <div style="font-weight: bold; font-size: 16px; color: #333; margin-bottom: 8px;">
                            Temperatura mínima del día
                        </div>
                        <div style="font-size: 36px; font-weight: bold; color: #c00; text-align: center;">
                            {tn_display}
                        </div>
                    </div>
                    
                    <!-- Fila 3: Pluja -->
                    <div style="margin-bottom: 20px; border: 2px solid #e0e0e0; border-radius: 8px; padding: 15px; background: #fafafa;">
                        <div style="font-weight: bold; font-size: 16px; color: #333; margin-bottom: 8px;">
                            Pluja acumulada
                        </div>
                        <div style="font-size: 36px; font-weight: bold; color: #c00; text-align: center;">
                            {ppt_display}
                        </div>
                    </div>
                </div>
                
                <!-- PEU DE PÀGINA -->
                <div style="background: #f8f8f8; padding: 12px; border-top: 2px solid #ddd; text-align: center;">
                    <div style="color: #333; font-weight: bold; margin-bottom: 4px;">
                        Actualitzat: {hora_actual} - Data: {data_actual}
                    </div>
                    <div style="color: #666; font-size: 14px;">
                        Font: https://www.meteo.cat/
                    </div>
                </div>
            </div>
            """
            
            stations_html += station_html
    
    # 3. Si no hi ha dades
    if not stations_html:
        hora_actual = datetime.now().strftime("%H:%M")
        data_actual = datetime.now().strftime("%d/%m/%Y")
        
        stations_html = f"""
        <div style="margin: 15px auto; padding: 0; max-width: 800px; background: #fff; font-family: Arial, sans-serif;">
            <h1 style="color: #c00; text-align: center; margin: 0; padding: 20px; background: #f8f8f8;">
                SENSE DADES DISPONIBLES
            </h1>
            <div style="padding: 30px; text-align: center; color: #666;">
                <p style="font-size: 18px;">Esperant actualització de dades meteorològiques...</p>
            </div>
            <div style="background: #f8f8f8; padding: 12px; border-top: 2px solid #ddd; text-align: center;">
                <div style="color: #333; font-weight: bold; margin-bottom: 4px;">
                    Actualitzat: {hora_actual} - Data: {data_actual}
                </div>
                <div style="color: #666; font-size: 14px;">
                    Font: https://www.meteo.cat/
                </div>
            </div>
        </div>
        """
    
    # 4. HTML complet
    html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meteorologia - Dades en Directe</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            div[style*="font-size: 36px"] {{
                font-size: 28px !important;
            }}
            h1 {{
                font-size: 22px !important;
            }}
        }}
        @media print {{
            body {{
                background: #fff !important;
            }}
        }}
    </style>
</head>
<body>
    {stations_html}
</body>
</html>"""
    
    return html

def main():
    """Funció principal"""
    print("🎨 Generant banner meteorològic (amb caixes)...")
    
    html = generate_banner_with_boxes()
    
    if html:
        # Guardar com a banner_output.html
        with open("banner_output.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ banner_output.html generat")
        
        # Guardar com a index.html (per GitHub Pages)
        with open("index.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ index.html actualitzat")
        
        # Comptar estacions
        try:
            with open("data/latest_weather.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            count = len([s for s in data.get('stations', {}).values() if s.get('success')])
            print(f"📊 Estacions processades: {count}")
        except:
            print("📊 No s'han pogut comptar les estacions")
    else:
        print("❌ No s'ha pogut generar el banner")

if __name__ == "__main__":
    main()
