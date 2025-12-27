"""
Genera el fitxer HTML amb el banner meteorològic - FORMAT SIMPLE I NET
Com la imatge que has compartit
"""

import json
from datetime import datetime, timezone, timedelta
import os

def generate_banner_simple():
    """Genera el banner en format simple (com la teva imatge)"""
    
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
            tx_display = f"{tx}°c" if tx != '-' else "-"
            tn_display = f"{tn}°c" if tn != '-' else "-"
            ppt_display = f"{ppt} mm" if ppt != '-' else "-"
            
            # Hora local (Catalunya, UTC+1)
            utc_time = datetime.now(timezone.utc)
            local_time = utc_time + timedelta(hours=1)  # UTC+1 per Catalunya
            hora_actual = local_time.strftime("%H:%M")
            data_actual = local_time.strftime("%d/%m/%Y")
            
            # HTML de l'estació (format simple)
            station_html = f"""
            <div style="margin: 20px; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h1 style="color: #c00; text-align: center; margin-bottom: 20px;">{station_name}</h1>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 25px;">
                    <div style="text-align: center; flex: 1;">
                        <h3 style="color: #333; margin-bottom: 10px;">Temperatura máxima del día</h3>
                        <div style="font-size: 48px; font-weight: bold; color: #c00;">{tx_display}</div>
                    </div>
                    
                    <div style="text-align: center; flex: 1;">
                        <h3 style="color: #333; margin-bottom: 10px;">Temperatura mínima del día</h3>
                        <div style="font-size: 48px; font-weight: bold; color: #c00;">{tn_display}</div>
                    </div>
                    
                    <div style="text-align: center; flex: 1;">
                        <h3 style="color: #333; margin-bottom: 10px;">Pluja acumulada</h3>
                        <div style="font-size: 48px; font-weight: bold; color: #c00;">{ppt_display}</div>
                    </div>
                </div>
                
                <hr style="border: none; border-top: 2px solid #eee; margin: 25px 0;">
                
                <div style="text-align: center; color: #666; font-size: 14px;">
                    <p><strong>Actualitzat: {hora_actual} - Data: {data_actual}</strong></p>
                    <p>Font: https://www.meteo.cat/</p>
                </div>
            </div>
            """
            
            stations_html += station_html
    
    # 3. Si no hi ha dades
    if not stations_html:
        hora_actual = datetime.now().strftime("%H:%M")
        data_actual = datetime.now().strftime("%d/%m/%Y")
        
        stations_html = f"""
        <div style="margin: 20px; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
            <h1 style="color: #c00; margin-bottom: 20px;">SENSE DADES DISPONIBLES</h1>
            <p style="font-size: 18px; color: #666;">Esperant actualització de dades meteorològiques...</p>
            
            <hr style="border: none; border-top: 2px solid #eee; margin: 25px 0;">
            
            <div style="text-align: center; color: #666; font-size: 14px;">
                <p><strong>Actualitzat: {hora_actual} - Data: {data_actual}</strong></p>
                <p>Font: https://www.meteo.cat/</p>
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
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            h1 {{ font-size: 24px; }}
            h3 {{ font-size: 16px; }}
            div[style*="font-size: 48px"] {{
                font-size: 36px !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {stations_html}
    </div>
</body>
</html>"""
    
    return html

def main():
    """Funció principal"""
    print("🎨 Generant banner meteorològic (format simple)...")
    
    html = generate_banner_simple()
    
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
