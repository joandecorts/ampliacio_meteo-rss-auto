#!/usr/bin/env python3
"""
meteo_scraper.py - Versió adaptada del daily_weather_scraper.py
Fa web scraping directe de Meteocat igual que l'altre projecte
AMB ARRODONIMENT CORREGIT (sense multiplicar per 100)
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import sys
import re

import config_banner as cfg

def round_catalan_style(value, decimals=1):
    """
    Arrodoneix un número a 'decimals' decimals.
    Si el segon decimal TROBAT és >= 5, augmenta el primer decimal en 1.
    
    Args:
        value: El número a arrodonir (int, float, string o None)
        decimals: Nombre de decimals desitjats (per defecte: 1)
    
    Returns:
        float: El valor arrodonit amb 'decimals' decimals
    """
    try:
        # Si el valor és None, buit o 'None', retorna 0.0
        if value in [None, 'None', '', 'null']:
            return 0.0
            
        num = float(value)
        if num == 0:
            return 0.0
        
        # MÈTODE CORRECTE:
        # 1. Desplacem el decimal que volem mantenir a la posició d'unitats
        factor = 10 ** decimals
        shifted = abs(num) * factor
        
        # 2. Mirem la part decimal d'aquest número desplaçat
        integer_part = int(shifted)
        fractional_part = shifted - integer_part
        
        # 3. Mirem el PRIMER decimal després dels que volem mantenir
        first_decimal_after = int(fractional_part * 10)
        
        # 4. Si aquest decimal és >= 5, sumem 1 a la part entera
        if first_decimal_after >= 5:
            integer_part += 1
        
        # 5. Restaurem la posició decimal original
        result = integer_part / factor
        
        # 6. Restaurem el signe
        if num < 0:
            result = -result
            
        return result
        
    except (ValueError, TypeError):
        return 0.0

def write_log(message):
    """Escriu un missatge i també el mostra per pantalla"""
    print(message)

def convertir_a_numero(text, default=None):
    """Converteix text a número, retorna None si no és vàlid"""
    if not text or text in ['(s/d)', '-', '', 'n/d', 'N/D']:
        return None
    try:
        # Netejar possibles símbols
        text = text.replace(',', '.').replace('°', '').replace('mm', '').replace('hPa', '').replace('W/m²', '')
        # APLIQUEM ARRODONIMENT DIRECTAMENT
        return round_catalan_style(float(text.strip()), 1)
    except:
        return None

def scrape_station_data(station_code, station_name):
    """
    Extreu les dades d'una estació (versió simplificada per al banner)
    Retorna: {'TX': valor, 'TN': valor, 'PPT': valor} o None
    """
    url = f"https://www.meteo.cat/observacions/xema/dades?codi={station_code}"
    
    try:
        write_log(f"  📡 Connectant a {station_name} ({station_code})...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'tblperiode'})
        
        if not table:
            write_log("  ❌ No s'ha trobat la taula tblperiode")
            return None
        
        rows = table.find_all('tr')
        
        # Variables per emmagatzemar les dades del dia
        temp_max_values = []
        temp_min_values = []
        rain_values = []
        
        # Recórrer totes les files per acumular dades del dia
        for i, row in enumerate(rows):
            cells = row.find_all(['td', 'th'])
            
            if len(cells) < 6:  # Necessitem almenys 6 columnes
                continue
            
            periode = cells[0].get_text(strip=True)
            
            # Verificar si és un període vàlid (hh:mm - hh:mm)
            if re.match(r'\d{1,2}:\d{2}\s*[-–]\s*\d{1,2}:\d{2}', periode):
                # Extreure dades
                tx = convertir_a_numero(cells[2].get_text(strip=True)) if len(cells) > 2 else None
                tn = convertir_a_numero(cells[3].get_text(strip=True)) if len(cells) > 3 else None
                ppt = convertir_a_numero(cells[5].get_text(strip=True)) if len(cells) > 5 else None
                
                # Acumular per a càlculs
                if tx is not None:
                    temp_max_values.append(tx)
                if tn is not None:
                    temp_min_values.append(tn)
                if ppt is not None:
                    rain_values.append(ppt)
        
        # Calcular màxims, mínims i acumulats
        values = {}
        
        if temp_max_values:
            values['TX'] = max(temp_max_values)
        else:
            values['TX'] = cfg.DEFAULT_VALUES['TX']
            
        if temp_min_values:
            values['TN'] = min(temp_min_values)
        else:
            values['TN'] = cfg.DEFAULT_VALUES['TN']
            
        if rain_values:
            values['PPT'] = sum(rain_values)
        else:
            values['PPT'] = cfg.DEFAULT_VALUES['PPT']
        
        # APLIQUEM ARRODONIMENT FINAL (per si hi ha errors de coma flotant)
        values['TX'] = round_catalan_style(values['TX'], 1)
        values['TN'] = round_catalan_style(values['TN'], 1)
        values['PPT'] = round_catalan_style(values['PPT'], 1)
        
        write_log(f"  ✅ {station_name}: TX={values['TX']}°C, TN={values['TN']}°C, PPT={values['PPT']}mm")
        return values
        
    except Exception as e:
        write_log(f"  ❌ Error consultant {station_name}: {str(e)[:50]}")
        return None

def main():
    """Funció principal"""
    print("=" * 60)
    print("METEOCAT WEB SCRAPER - Versió igual que l'altre projecte")
    print("=" * 60)
    
    print("\n[1] Comprovant estacions configurades...")
    print(f"   Estacions a consultar: {len(cfg.STATIONS)}")
    for station in cfg.STATIONS:
        print(f"   • {station['display_name']} ({station['code']})")
    
    # Diccionari per emmagatzemar totes les dades
    all_data = {
        'metadata': {
            'last_updated': datetime.now().isoformat(),
            'source': 'meteocat_web_scraping',
            'stations_count': len(cfg.STATIONS)
        },
        'stations': {}
    }
    
    print("\n[2] Obtenint dades de les estacions...")
    
    for station in cfg.STATIONS:
        station_code = station['code']
        display_name = station['display_name']
        
        # Obtenir dades de l'estació
        raw_values = scrape_station_data(station_code, display_name)
        
        if raw_values:
            station_data = {
                'success': True,
                'values': {
                    'TX': raw_values.get('TX', cfg.DEFAULT_VALUES['TX']),
                    'TN': raw_values.get('TN', cfg.DEFAULT_VALUES['TN']),
                    'PPT': raw_values.get('PPT', cfg.DEFAULT_VALUES['PPT'])
                },
                'metadata': {
                    'name': display_name,
                    'last_fetched': datetime.now().isoformat(),
                    'url': f"https://www.meteo.cat/observacions/xema/dades?codi={station_code}"
                }
            }
        else:
            station_data = {
                'success': False,
                'values': cfg.DEFAULT_VALUES,
                'metadata': {
                    'name': display_name,
                    'error': 'No s\'han pogut obtenir dades',
                    'last_attempt': datetime.now().isoformat()
                }
            }
        
        all_data['stations'][station_code] = station_data
    
    # Guardar dades
    try:
        with open(cfg.LATEST_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Dades guardades a: {cfg.LATEST_DATA_FILE}")
        print(f"   Estacions processades: {len(all_data['stations'])}")
        print(f"   Última actualització: {datetime.now().strftime('%H:%M:%S')}")
        
        # Mostrar resum
        print("\n📊 RESUM DE DADES OBTINGUDES:")
        for station_code, station_data in all_data['stations'].items():
            name = next((s['display_name'] for s in cfg.STATIONS if s['code'] == station_code), station_code)
            if station_data['success']:
                vals = station_data['values']
                print(f"   {name}: TX={vals['TX']}°C, TN={vals['TN']}°C, PPT={vals['PPT']}mm")
            else:
                print(f"   {name}: ❌ Sense dades")
        
        return all_data
        
    except Exception as e:
        print(f"❌ Error guardant dades: {e}")
        return None

if __name__ == "__main__":
    try:
        result = main()
        if result:
            print("\n" + "=" * 60)
            print("✅ PROCÉS COMPLETAT AMB ÈXIT")
            print("=" * 60)
        else:
            print("\n❌ PROCÉS COMPLETAT AMB ERRORS")
    except KeyboardInterrupt:
        print("\n\n⏹️  Execució cancel·lada per l'usuari")
    except Exception as e:
        print(f"\n💥 ERROR CRÍTIC: {e}")