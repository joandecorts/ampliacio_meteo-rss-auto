#!/usr/bin/env python3
"""
GENERADOR DE BANNER NEWS CHANNEL
Script principal per generar l'HTML del banner meteorològic
"""

import json
import os
import sys
from datetime import datetime

# Configuració pròpia
import config_banner as cfg

def carregar_dades_simulades():
    """Carrega dades de prova per desenvolupament"""
    return {
        'GIRONA': {
            'max_temp': 14.5,
            'min_temp': 7.3,
            'rainfall': 2.8,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'FORNELLS': {
            'max_temp': 13.8,
            'min_temp': 6.5,
            'rainfall': 1.2,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    }

def llegir_plantilla_html():
    """Llegeix la plantilla HTML"""
    try:
        with open(cfg.HTML_TEMPLATE, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERROR: No es troba la plantilla {cfg.HTML_TEMPLATE}")
        sys.exit(1)

def generar_html_estacio(estacio, dades):
    """Genera el bloc HTML per una estació"""
    
    html = f'''
            <!-- GRUP: {estacio['name']} -->
            <div class="content-group" id="group{estacio['id']}">
                <div class="location-header">
                    <div class="location-name">{estacio['display_name']}</div>
                </div>
                
                <div class="data-container">
                    <div class="data-box">
                        <div class="data-title">{cfg.TEXTS['max_temp']}</div>
                        <div class="data-value">{dades['max_temp']}<span class="data-unit">°C</span></div>
                    </div>
                    
                    <div class="data-box">
                        <div class="data-title">{cfg.TEXTS['min_temp']}</div>
                        <div class="data-value">{dades['min_temp']}<span class="data-unit">°C</span></div>
                    </div>
                    
                    <div class="data-box">
                        <div class="data-title">{cfg.TEXTS['rainfall']}</div>
                        <div class="data-value">{dades['rainfall']}<span class="data-unit">mm</span></div>
                    </div>
                </div>
                
                <div class="footer">
                    <div class="update-info">{cfg.get_update_text()}</div>
                    <div class="source">{cfg.TEXTS['source']}: https://www.meteo.cat/</div>
                </div>
            </div>
    '''
    
    return html

def generar_html_complet(dades_meteo):
    """Genera l'HTML complet amb totes les estacions"""
    
    # Llegir plantilla
    html_template = llegir_plantilla_html()
    
    # Generar contingut dinàmic
    contingut_estacions = ""
    for i, estacio in enumerate(cfg.STATIONS):
        estacio_html = generar_html_estacio(estacio, dades_meteo[estacio['name']])
        contingut_estacions += estacio_html
    
    # Substituir al template
    html_final = html_template.replace(
        '<!-- GRUP 1: GIRONA -->\n            <div class="content-group active" id="group1">',
        contingut_estacions
    )
    
    # Ajustar classes per scroll (la primera activa, la resta ocultes)
    lines = html_final.split('\n')
    for i, line in enumerate(lines):
        if 'content-group' in line and 'id="group' in line:
            if 'GIRONA' in lines[i+2]:  # Primera estació
                lines[i] = lines[i].replace('content-group"', 'content-group active"')
            else:
                lines[i] = lines[i].replace('content-group"', 'content-group next"')
    
    return '\n'.join(lines)

def guardar_html(html_content):
    """Guarda l'HTML generat"""
    try:
        with open(cfg.OUTPUT_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML generat correctament: {cfg.OUTPUT_HTML}")
        return True
    except Exception as e:
        print(f"✗ Error guardant HTML: {e}")
        return False

def main():
    """Funció principal"""
    print("=" * 50)
    print("GENERADOR BANNER NEWS CHANNEL")
    print("=" * 50)
    
    # 1. Carregar dades
    print("\n[1] Carregant dades meteorològiques...")
    dades_meteo = carregar_dades_simulades()
    print(f"   ✓ Dades carregades per {len(dades_meteo)} estacions")
    
    # 2. Generar HTML
    print("\n[2] Generant HTML...")
    html_final = generar_html_complet(dades_meteo)
    
    # 3. Guardar fitxer
    print("\n[3] Guardant fitxer de sortida...")
    if guardar_html(html_final):
        print(f"\n✅ PROCÉS COMPLETAT")
        print(f"   Fitxer: {cfg.OUTPUT_HTML}")
        print(f"   Estacions: {len(cfg.STATIONS)}")
        print(f"   Actualitzat: {cfg.get_update_text()}")
    else:
        print("\n❌ PROCÉS FALLAT")
        sys.exit(1)

if __name__ == "__main__":
    main()
