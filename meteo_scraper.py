#!/usr/bin/env python3
"""
METEOCAT SCRAPER - Captura dades meteorològiques reals
Versió inicial: 3 estacions
"""

import requests
import json
import time
from datetime import datetime, timedelta
import sys
import os

# Importem la nostra configuració
import config_banner as cfg

class MeteoCatScraper:
    """Classe per capturar dades de l'API de Meteocat"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or cfg.API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MeteoBanner/1.0 (joandecorts.github.io)',
            'Accept': 'application/json'
        })
        
        if self.api_key:
            self.session.headers.update({'X-Api-Key': self.api_key})
        else:
            print("⚠️  Atenció: S'està utilitzant l'API sense clau (limitacions)")
    
    def get_station_data(self, station_code, date=None):
        """
        Obté dades d'una estació per una data concreta
        Retorna les dades crues de l'API
        """
        if date is None:
            date = cfg.YESTERDAY  # Per defecte, dades d'ahir (màx/mín)
        
        date_str = date.strftime('%Y-%m-%d')
        url = f"{cfg.METEOcat_CONFIG['api_base']}/stations/{station_code}/measurements/{date_str}"
        
        try:
            print(f"  🔍 Sol·licitant dades: {station_code} ({date_str})...")
            
            response = self.session.get(
                url,
                timeout=cfg.METEOcat_CONFIG['timeout']
            )
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'success': True,
                'station': station_code,
                'date': date_str,
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Error obtenint dades {station_code}: {e}")
            return {
                'success': False,
                'station': station_code,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def extract_daily_values(self, raw_data):
        """
        Extreu els valors diaris (TX, TN, PPT) de les dades crues
        
        TX: Temperatura màxima del dia
        TN: Temperatura mínima del dia  
        PPT: Precipitació acumulada
        """
        if not raw_data.get('success') or 'data' not in raw_data:
            return cfg.DEFAULT_VALUES.copy()
        
        measurements = raw_data['data'].get('measurements', [])
        
        # Inicialitzar valors
        values = {
            'TX': None,  # Màxima
            'TN': None,  # Mínima
            'PPT': 0.0   # Acumulat precipitat
        }
        
        # Processar cada mesura
        for measurement in measurements:
            # Temperatura (variable 32)
            if measurement.get('codi_variable') == 32:
                temp_value = measurement.get('valor')
                if temp_value is not None:
                    # Actualitzar màxima i mínima
                    if values['TX'] is None or temp_value > values['TX']:
                        values['TX'] = temp_value
                    if values['TN'] is None or temp_value < values['TN']:
                        values['TN'] = temp_value
            
            # Precipitació (variable 35)
            elif measurement.get('codi_variable') == 35:
                ppt_value = measurement.get('valor')
                if ppt_value is not None:
                    values['PPT'] += ppt_value
        
        # Formatar valors finals
        result = cfg.DEFAULT_VALUES.copy()
        
        if values['TX'] is not None:
            result['TX'] = round(values['TX'], 1)
        if values['TN'] is not None:
            result['TN'] = round(values['TN'], 1)
        if values['PPT'] > 0:
            result['PPT'] = round(values['PPT'], 1)
        
        return result
    
    def scrape_all_stations(self, stations=None):
        """
        Captura dades de totes les estacions configurades
        """
        if stations is None:
            stations = cfg.STATIONS
        
        print(f"\n📡 Començant captura de {len(stations)} estacions...")
        print("=" * 50)
        
        all_data = {
            'metadata': {
                'last_updated': datetime.now().isoformat(),
                'date': cfg.TODAY.isoformat(),
                'station_count': len(stations)
            },
            'stations': {}
        }
        
        for station in stations:
            station_code = station['code']
            station_name = station['name']
            
            print(f"\n📍 {station['display_name']} [{station_code}]")
            
            # 1. Obtenir dades crues
            raw_data = self.get_station_data(station_code, cfg.YESTERDAY)
            
            # 2. Extreu valors diaris
            if raw_data['success']:
                daily_values = self.extract_daily_values(raw_data)
                
                # Guardar resultats
                all_data['stations'][station_code] = {
                    'name': station['display_name'],
                    'code': station_code,
                    'values': daily_values,
                    'raw_timestamp': raw_data['timestamp'],
                    'success': True
                }
                
                print(f"   ✅ TX: {daily_values['TX']}°C | TN: {daily_values['TN']}°C | PPT: {daily_values['PPT']}mm")
                
                # Guardar dades crues per històric
                self.save_historical_data(station_code, raw_data)
                
            else:
                print(f"   ❌ Error: {raw_data.get('error', 'Desconegut')}")
                all_data['stations'][station_code] = {
                    'name': station['display_name'],
                    'code': station_code,
                    'values': cfg.DEFAULT_VALUES.copy(),
                    'error': raw_data.get('error'),
                    'success': False
                }
            
            # Esperar una mica per no sobrecarregar l'API
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print(f"✅ Captura completada: {len([s for s in all_data['stations'].values() if s['success']])}/{len(stations)} estacions")
        
        return all_data
    
    def save_historical_data(self, station_code, raw_data):
        """Guarda dades crues per a l'històric"""
        if not raw_data['success']:
            return
        
        file_path = cfg.get_station_file_path(station_code)
        
        try:
            # Carregar històric existent
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    historical = json.load(f)
            else:
                historical = {'station': station_code, 'data': []}
            
            # Afegir nova entrada (només si no existeix ja)
            date_str = raw_data.get('date')
            existing = any(entry.get('date') == date_str for entry in historical['data'])
            
            if not existing:
                historical['data'].append(raw_data)
                
                # Mantenir només últims 365 dies
                if len(historical['data']) > 365:
                    historical['data'] = historical['data'][-365:]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(historical, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            print(f"  ⚠️  Error guardant històric {station_code}: {e}")
    
    def save_latest_data(self, all_data):
        """Guarda les dades més recents per al banner"""
        try:
            with open(cfg.LATEST_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Dades guardades: {cfg.LATEST_DATA_FILE}")
            return True
            
        except Exception as e:
            print(f"❌ Error guardant dades: {e}")
            return False

def main():
    """Funció principal"""
    print("=" * 60)
    print("SCRAPER METEOCAT - Captura dades per Banner News Channel")
    print("=" * 60)
    
    # Verificar API key
    if not cfg.API_KEY:
        print("\n⚠️  ADVERTÈNCIA: No s'ha configurat clau API de Meteocat")
        print("   Les peticions podran ser limitades")
        print("   Configura la variable d'entorn METEOcat_API_KEY")
        input("   Prem Enter per continuar sense clau API...")
    
    # Inicialitzar scraper
    scraper = MeteoCatScraper()
    
    # Capturar dades
    all_data = scraper.scrape_all_stations()
    
    # Guardar dades
    if scraper.save_latest_data(all_data):
        print("\n🎉 PROCÉS COMPLETAT AMB ÈXIT")
        print(f"   Dades actualitzades: {cfg.get_current_datetime()['datetime']}")
        print(f"   Estacions: {len(all_data['stations'])}")
        
        # Mostrar resum
        successful = sum(1 for s in all_data['stations'].values() if s['success'])
        print(f"   Correctes: {successful}/{len(all_data['stations'])}")
        
        return 0
    else:
        print("\n❌ PROCÉS FALLAT")
        return 1

if __name__ == "__main__":
    sys.exit(main())
