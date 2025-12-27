"""
Genera el fitxer HTML amb el banner meteorològic
"""

import json
from datetime import datetime
import os

def round_catalan_style(value, decimals=1):
    """
    Arrodoneix un número a 'decimals' decimals.
    Si el segon decimal TROBAT és >= 5, augmenta el primer decimal en 1.
    
    Args:
        value: El número a arrodonir (int, float o string)
        decimals: Nombre de decimals desitjats (per defecte: 1)
    
    Returns:
        float: El valor arrodonit amb 'decimals' decimals
    """
    try:
        num = float(value)
        if num == 0:
            return 0.0
            
        # Multipliquem per moure els decimals
        factor = 10 ** (decimals + 1)  # Un decimal extra per veure el segon
        multiplied = abs(num) * factor
        
        # Separem parts enteres i decimals
        integer_part = int(multiplied)
        fractional = multiplied - integer_part
        
        # Mirem el SEGON decimal (primer decimal després del que volem)
        second_decimal_digit = int((fractional * 10) % 10)
        
        # Si el segon decimal és >= 5, sumem 1 a la part entera
        if second_decimal_digit >= 5:
            integer_part += 1
        
        # Ara dividim eliminant el decimal extra
        result = integer_part / (10 ** decimals)
        
        # Restaurem el signe
        if num < 0:
            result = -result
            
        # Arrodonim per eliminar errors de coma flotant
        return round(result, decimals)
        
    except (ValueError, TypeError):
        return 0.0


def format_temperature(temp):
    """Formata temperatura amb símbol °C"""
    if temp is None:
        return "-"
    try:
        rounded = round_catalan_style(temp, 1)
        return f"{rounded}°c"
    except:
        return "-"


def format_rain(rain):
    """Formata pluja acumulada"""
    if rain is None:
        return "-"
    try:
        rounded = round_catalan_style(rain, 1)
        return f"{rounded} mm"
    except:
        return "-"


def generate_banner_html(weather_data, output_file="banner_output.html"):
    """
    Genera el fitxer HTML del banner
    
    Args:
        weather_data: Diccionari amb les dades meteorològiques
        output_file: Nom del fitxer de sortida
    """
    # Llegir les dades
    try:
        if isinstance(weather_data, str):
            with open(weather_data, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = weather_data
    except Exception as e:
        print(f"❌ Error llegint dades: {e}")
        return
    
    stations = data.get('estacions', {})
    update_time = data.get('ultima_actualitzacio', '')
    update_date = data.get('data_actualitzacio', '')
    
    # HTML template
    html_template = """<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MeteoCat Banner</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #000;
            color: #fff;
            font-family: 'Arial', sans-serif;
            width: 1920px;
            overflow: hidden;
        }}
        
        .banner-container {{
            display: flex;
            flex-wrap: nowrap;
            padding: 10px;
            background: linear-gradient(90deg, #1a237e, #0d47a1);
            border-bottom: 3px solid #ff9800;
        }}
        
        .station {{
            flex: 0 0 auto;
            width: 320px;
            padding: 15px;
            margin-right: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            border-left: 4px solid #ff9800;
        }}
        
        .station-name {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ff9800;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .data-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-size: 16px;
        }}
        
        .data-label {{
            color: #bbdefb;
        }}
        
        .data-value {{
            font-weight: bold;
            color: #fff;
        }}
        
        .footer {{
            position: absolute;
            bottom: 5px;
            right: 10px;
            font-size: 12px;
            color: #90a4ae;
        }}
    </style>
</head>
<body>
    <div class="banner-container">
        {stations_html}
    </div>
    <div class="footer">
        Actualitzat: {update_time} - Data: {update_date} | Font: MeteoCat
    </div>
</body>
</html>"""
    
    # Generar HTML per a cada estació
    stations_html = ""
    for station_name, station_data in stations.items():
        tmx = format_temperature(station_data.get('tmx'))
        tmn = format_temperature(station_data.get('tmn'))
        ppt = format_rain(station_data.get('ppt'))
        
        station_html = f"""
        <div class="station">
            <div class="station-name">{station_name}</div>
            <div class="data-row">
                <span class="data-label">Temp. màx:</span>
                <span class="data-value">{tmx}</span>
            </div>
            <div class="data-row">
                <span class="data-label">Temp. mín:</span>
                <span class="data-value">{tmn}</span>
            </div>
            <div class="data-row">
                <span class="data-label">Pluja:</span>
                <span class="data-value">{ppt}</span>
            </div>
        </div>"""
        
        stations_html += station_html
    
    # Generar HTML final
    html_content = html_template.format(
        stations_html=stations_html,
        update_time=update_time,
        update_date=update_date
    )
    
    # Guardar fitxer
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Banner generat: {output_file}")
    return output_file


def main():
    """Funció principal"""
    print("🎨 Generant banner meteorològic...")
    
    # Ruta al fitxer de dades
    data_file = "data/latest_weather.json"
    
    # Verificar que el fitxer existeix
    if not os.path.exists(data_file):
        print(f"❌ El fitxer {data_file} no existeix")
        print("   Executa primer meteo_scraper.py per obtenir dades")
        return
    
    # Generar el banner
    output_file = generate_banner_html(data_file)
    
    if output_file:
        print(f"🏁 Banner creat correctament a: {output_file}")
        print(f"   Obre {output_file} al navegador per visualitzar-lo")


if __name__ == "__main__":
    main()