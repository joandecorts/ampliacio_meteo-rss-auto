"""
MeteoCat Web Scraper - VERSIÓ DEFINITIVA
Extreu dades meteorològiques de https://www.meteo.cat/observacions/xema
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from datetime import datetime, timezone
import os
import sys

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
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
            
            logger.info(f"Intent {attempt + 1}/{max_retries}: Scraping {station_code} - {station_name}")
            
            # Fer la petició amb timeout
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()  # Llença excepció per a codis HTTP dolents
            
            # Verificar que la resposta tingui contingut
            if not response.content:
                logger.warning(f"Resposta buida per a {station_code}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Esperar abans de reintentar
                    continue
                return None
            
            # Analitzar HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar la taula de dades
            table = soup.find('table', {'class': 'table-dades'})
            if not table:
                logger.warning(f"No s'ha trobat la taula per a {station_code}")
                # Intentar trobar dades d'una altra manera
                return extract_data_fallback(soup, station_code, station_name)
            
            # Buscar files de dades
            rows = table.find_all('tr')
            
            # Diccionari per emmagatzemar valors
            values = {}
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    variable = cells[0].get_text(strip=True)
                    valor_cell = cells[1]
                    
                    # Extreure el valor numèric
                    valor_text = valor_cell.get_text(strip=True)
                    
                    # Netejar i convertir
                    if valor_text and valor_text != '-':
                        try:
                            # Eliminar unitats i espais
                            valor_net = valor_text.split()[0].replace(',', '.')
                            valor_float = float(valor_net)
                            
                            # Identificar la variable
                            if 'Màxima' in variable or 'TEMPERATURA MÀXIMA' in variable.upper():
                                values['TX'] = round(valor_float, 1)
                            elif 'Mínima' in variable or 'TEMPERATURA MÍNIMA' in variable.upper():
                                values['TN'] = round(valor_float, 1)
                            elif 'Acumulada' in variable or 'PPT' in variable.upper() or 'PRECIPITACIÓ' in variable.upper():
                                values['PPT'] = round(valor_float, 1)
                        except (ValueError, IndexError) as e:
                            logger.debug(f"Error convertint valor per {station_code}, variable {variable}: {e}")
            
            # Verificar que tenim les dades mínimes
            required_vars = ['TX', 'TN', 'PPT']
            missing = [var for var in required_vars if var not in values]
            
            if missing:
                logger.warning(f"Falten variables per {station_code}: {missing}")
                # Posar valors per defecte per a les que falten
                for var in missing:
                    values[var] = '-'
            
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
            
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout per a {station_code} (intent {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(3)  # Esperar més abans de reintentar
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

def extract_data_fallback(soup, station_code, station_name):
    """Intent alternatiu d'extreure dades si no es troba la taula normal"""
    try:
        values = {'TX': '-', 'TN': '-', 'PPT': '-'}
        
        # Buscar valors per altres mètodes
        all_text = soup.get_text()
        
        # Buscar temperatura màxima
        if 'Màxima' in all_text or 'TEMPERATURA MÀXIMA' in all_text.upper():
            # Intentar trobar el valor després de la paraula clau
            lines = all_text.split('\n')
            for i, line in enumerate(lines):
                if 'Màxima' in line or 'TEMPERATURA MÀXIMA' in line.upper():
                    # Buscar números a les línies següents
                    for j in range(i, min(i+5, len(lines))):
                        import re
                        numbers = re.findall(r'[-+]?\d*\.\d+|\d+', lines[j])
                        if numbers:
                            try:
                                values['TX'] = round(float(numbers[0].replace(',', '.')), 1)
                                break
                            except:
                                pass
        
        # Similar per temperatura mínima i precipitació
        # (podries afegir més lògica aquí)
        
        logger.info(f"⚠️  {station_code}: Dades fallback - TX={values['TX']}°C, TN={values['TN']}°C, PPT={values['PPT']}mm")
        
        return {
            'success': True if any(v != '-' for v in values.values()) else False,
            'values': values,
            'metadata': {
                'name': station_name,
                'last_fetched': datetime.now(timezone.utc).isoformat(),
                'url': f"https://www.meteo.cat/observacions/xema/dades?codi={station_code}",
                'note': 'Dades obtingudes amb mètode fallback'
            }
        }
        
    except Exception as e:
        logger.error(f"Error en mètode fallback per {station_code}: {e}")
        return None

def main():
    """Funció principal"""
    logger.info("=" * 60)
    logger.info("🚀 INICIANT METEO SCRAPER")
    logger.info(f"📊 Estacions a processar: {len(STATIONS)}")
    logger.info("=" * 60)
    
    # Crear directori de dades si no existeix
    os.makedirs('data', exist_ok=True)
    
    # Diccionari per emmagatzemar totes les dades
    all_data = {
        'metadata': {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'source': 'meteocat_web_scraping',
            'stations_count': len(STATIONS)
        },
        'stations': {}
    }
    
    # Processar cada estació
    success_count = 0
    failed_stations = []
    
    for i, station in enumerate(STATIONS, 1):
        station_code = station['code']
        station_name = station['display_name']
        
        logger.info(f"[{i}/{len(STATIONS)}] Processant {station_code} - {station_name}")
        
        # Scraping de l'estació
        station_data = scrape_station_data(station_code, station_name)
        
        if station_data and station_data['success']:
            all_data['stations'][station_code] = station_data
            success_count += 1
        else:
            # Estació fallida, afegir amb dades buides
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
        
        # Esperar entre peticions per no sobrecarregar el servidor
        time.sleep(1.5)
    
    # Guardar dades en fitxer JSON
    output_file = 'data/latest_weather.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Dades guardades a {output_file}")
    except Exception as e:
        logger.error(f"❌ Error guardant fitxer: {e}")
        return
    
    # Resum
    logger.info("=" * 60)
    logger.info("📊 RESUM DE L'EXECUCIÓ")
    logger.info(f"✅ Estacions amb èxit: {success_count}/{len(STATIONS)}")
    
    if failed_stations:
        logger.info(f"❌ Estacions fallides: {len(failed_stations)}")
        for failed in failed_stations:
            station_name = next((s['display_name'] for s in STATIONS if s['code'] == failed), failed)
            logger.info(f"   - {failed}: {station_name}")
    
    logger.info(f"💾 Fitxer de sortida: {output_file}")
    logger.info("=" * 60)
    
    # Mostrar algunes dades d'exemple
    if success_count > 0:
        logger.info("📈 DADES D'EXEMPLE (primeres 3 estacions amb èxit):")
        sample_count = 0
        for station_code, data in all_data['stations'].items():
            if data['success'] and sample_count < 3:
                values = data['values']
                name = data['metadata']['name']
                logger.info(f"   {station_code} - {name}: TX={values.get('TX', '-')}°C, TN={values.get('TN', '-')}°C, PPT={values.get('PPT', '-')}mm")
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
