"""
MeteoCat Web Scraper - VERSIÓ ACTUALITZADA
Extreu dades meteorològiques de https://www.meteo.cat/observacions/xema
AMB DETECCIÓ AUTOMÀTICA DE L'ESTRUCTURA HTML
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from datetime import datetime, timezone
import os
import sys
import re

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Importar configuració
try:
    import config_banner as cfg
    STATIONS = cfg.STATIONS
    logger.info(f"✅ Carregades {len(STATIONS)} estacions de config_banner.py")
except ImportError as e:
    logger.error(f"❌ Error important config_banner.py: {e}")
    sys.exit(1)
except AttributeError as e:
    logger.error(f"❌ Error: config_banner.py no té STATIONS: {e}")
    sys.exit(1)

def scrape_station_data(station_code, station_name, max_retries=3):
    """
    Extreu dades meteorològiques d'una estació
    
    Args:
        station_code: Codi de l'estació (ex: 'XJ')
        station_name: Nom de l'estació per logging
        max_retries: Intents màxims en cas d'error
    
    Returns:
        dict amb dades de l'estació o None si error
    """
    url = f"https://www.meteo.cat/observacions/xema/dades?codi={station_code}"
    
    for attempt in range(max_retries):
        try:
            # Headers per semblar un navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'ca,en-US;q=0.7,en;q=0.3',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            logger.info(f"Intent {attempt + 1}/{max_retries}: Scraping {station_code} - {station_name}")
            
            # Fer la petició amb timeout
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            # Verificar contingut
            if not response.content:
                logger.warning(f"Resposta buida per a {station_code}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
            
            # Analitzar HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # DEBUG: Guardar HTML per inspeccionar (opcional)
            if station_code in ['XJ', 'VK']:  # Per a debug
                with open(f'debug_{station_code}.html', 'w', encoding='utf-8') as f:
                    f.write(soup.prettify())
                logger.info(f"DEBUG: HTML guardat a debug_{station_code}.html")
            
            # INTENT 1: Buscar per múltiples patrons de taula
            table = None
            table_patterns = [
                {'class': 'table-dades'},
                {'class': 'taula-dades'},
                {'class': 'dades-table'},
                {'id': 'taula-dades'},
                {'id': 'table-dades'},
                {'class': 'table'},
                {'class': 'taula'}
            ]
            
            for pattern in table_patterns:
                table = soup.find('table', pattern)
                if table:
                    logger.debug(f"✅ Taula trobada amb patró: {pattern}")
                    break
            
            if table:
                values = extract_from_table(table)
            else:
                # INTENT 2: Buscar dades per text
                logger.warning(f"No s'ha trobat taula per {station_code}, buscant per text...")
                values = extract_from_text(soup.get_text())
            
            # Verificar que tenim algun valor
            if any(v != '-' for v in values.values()):
                logger.info(f"✅ {station_code}: TX={values.get('TX', '-')}°C, TN={values.get('TN', '-')}°C, PPT={values.get('PPT', '-')}mm")
                return {
                    'success': True,
                    'values': values,
                    'metadata': {
                        'name': station_name,
                        'last_fetched': datetime.now(timezone.utc).isoformat(),
                        'url': url
                    }
                }
            else:
                logger.warning(f"No s'han trobat dades per {station_code}")
                if attempt < max_retries - 1:
                    time.sleep(3)
                    continue
                return None
                
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout per a {station_code} (intent {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(3)
                continue
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de xarxa per a {station_code}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None
            
        except Exception as e:
            logger.error(f"Error inesperat scraping {station_code}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None
    
    return None

def extract_from_table(table):
    """Extreu dades d'una taula HTML"""
    values = {'TX': '-', 'TN': '-', 'PPT': '-'}
    
    try:
        # Buscar totes les files
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                # Text de la cel·la d'esquerra (variable)
                var_text = cells[0].get_text(strip=True).upper()
                val_text = cells[1].get_text(strip=True)
                
                # Buscar números amb regex
                numbers = re.findall(r'[-+]?\d*[.,]?\d+', val_text)
                if numbers:
                    try:
                        num = float(numbers[0].replace(',', '.'))
                        
                        # Assignar a la variable correcta
                        if 'MÀXIMA' in var_text or 'TX' in var_text or 'TEMPERATURA MÀXIMA' in var_text:
                            values['TX'] = round(num, 1)
                        elif 'MÍNIMA' in var_text or 'TN' in var_text or 'TEMPERATURA MÍNIMA' in var_text:
                            values['TN'] = round(num, 1)
                        elif 'ACUMULADA' in var_text or 'PPT' in var_text or 'PRECIPITACIÓ' in var_text or 'PLUJA' in var_text:
                            values['PPT'] = round(num, 1)
                    except ValueError:
                        pass
    except Exception as e:
        logger.debug(f"Error extreient de taula: {e}")
    
    return values

def extract_from_text(full_text):
    """Extreu dades del text brut (fallback)"""
    values = {'TX': '-', 'TN': '-', 'PPT': '-'}
    
    try:
        # Buscar patrons amb regex
        # Temperatura màxima
        tx_match = re.search(r'(?:Temperatura|Temp\.?)\s*(?:[Mm]àxima|MAX)\s*[:=]?\s*([-+]?\d*[.,]?\d+)', full_text, re.IGNORECASE)
        if tx_match:
            try:
                values['TX'] = round(float(tx_match.group(1).replace(',', '.')), 1)
            except:
                pass
        
        # Temperatura mínima
        tn_match = re.search(r'(?:Temperatura|Temp\.?)\s*(?:[Mm]ínima|MIN)\s*[:=]?\s*([-+]?\d*[.,]?\d+)', full_text, re.IGNORECASE)
        if tn_match:
            try:
                values['TN'] = round(float(tn_match.group(1).replace(',', '.')), 1)
            except:
                pass
        
        # Precipitació
        ppt_match = re.search(r'(?:Precipitació|Pluja|PPT)\s*(?:[Aa]cumulada|ACUM)?\s*[:=]?\s*([-+]?\d*[.,]?\d+)', full_text, re.IGNORECASE)
        if ppt_match:
            try:
                values['PPT'] = round(float(ppt_match.group(1).replace(',', '.')), 1)
            except:
                pass
        
    except Exception as e:
        logger.debug(f"Error extreient de text: {e}")
    
    return values

def main():
    """Funció principal"""
    logger.info("=" * 60)
    logger.info("🚀 INICIANT METEO SCRAPER - VERSIÓ ACTUALITZADA")
    logger.info(f"📊 Estacions a processar: {len(STATIONS)}")
    logger.info("=" * 60)
    
    # Crear directori de dades
    os.makedirs('data', exist_ok=True)
    
    # Diccionari per dades
    all_data = {
        'metadata': {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'source': 'meteocat_web_scraping',
            'stations_count': len(STATIONS),
            'version': '2.0'
        },
        'stations': {}
    }
    
    # Processar estacions
    success_count = 0
    failed_stations = []
    
    for i, station in enumerate(STATIONS, 1):
        station_code = station['code']
        station_name = station['display_name']
        
        logger.info(f"[{i}/{len(STATIONS)}] Processant {station_code} - {station_name}")
        
        # Scraping
        station_data = scrape_station_data(station_code, station_name)
        
        if station_data and station_data['success']:
            all_data['stations'][station_code] = station_data
            success_count += 1
        else:
            # Estació fallida
            all_data['stations'][station_code] = {
                'success': False,
                'values': {'TX': '-', 'TN': '-', 'PPT': '-'},
                'metadata': {
                    'name': station_name,
                    'last_fetched': datetime.now(timezone.utc).isoformat(),
                    'url': f"https://www.meteo.cat/observacions/xema/dades?codi={station_code}",
                    'error': 'No s\'han pogut obtenir dades'
                }
            }
            failed_stations.append(station_code)
        
        # Esperar entre peticions
        time.sleep(2)  # Augmentat per evitar bloqueig
    
    # Guardar dades
    output_file = 'data/latest_weather.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Dades guardades a {output_file}")
        
        # Mostrar data actual
        file_time = datetime.fromtimestamp(os.path.getmtime(output_file))
        logger.info(f"📅 Data del fitxer: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        logger.error(f"❌ Error guardant fitxer: {e}")
        return
    
    # Resum
    logger.info("=" * 60)
    logger.info("📊 RESUM DE L'EXECUCIÓ")
    logger.info(f"✅ Estacions amb èxit: {success_count}/{len(STATIONS)}")
    logger.info(f"❌ Estacions fallides: {len(failed_stations)}")
    
    if failed_stations:
        logger.info("Llista d'estacions fallides:")
        for failed in failed_stations:
            station_name = next((s['display_name'] for s in STATIONS if s['code'] == failed), failed)
            logger.info(f"   - {failed}: {station_name}")
    
    logger.info("=" * 60)
    
    # Mostrar dades d'exemple
    if success_count > 0:
        logger.info("📈 DADES D'EXEMPLE (3 estacions):")
        sample_count = 0
        for station_code, data in all_data['stations'].items():
            if data['success'] and sample_count < 3:
                values = data['values']
                name = data['metadata']['name']
                logger.info(f"   {station_code} - {name}:")
                logger.info(f"     TX: {values.get('TX', '-')}°C | TN: {values.get('TN', '-')}°C | PPT: {values.get('PPT', '-')}mm")
                sample_count += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Execució interrompuda per l'usuari")
    except Exception as e:
        logger.error(f"❌ Error crític: {e}")
        import traceback
        traceback.print_exc()
