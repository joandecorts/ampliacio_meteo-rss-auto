"""
CONFIGURACIÓ BANNER - GENERAT AMB CONFIGURADOR
Data de generació: 2025-12-30 22:32:47
"""

STATIONS = [
    {'code': 'XJ', 'name': 'GIRONA', 'display_name': 'GIRONA'},
    {'code': 'UO', 'name': 'FORNELLS_DE_LA_SELVA', 'display_name': 'FORNELLS DE LA SELVA'},
    {'code': 'DJ', 'name': 'BANYOLES', 'display_name': 'BANYOLES'},
    {'code': 'X4', 'name': 'BARCELONA', 'display_name': 'BARCELONA - EL RAVAL'},
    {'code': 'MS', 'name': 'CASTELLAR_DE_NHUG', 'display_name': 'CASTELLAR DE N\'HUG - EL CLOT DEL MORO'},
    {'code': 'XL', 'name': 'EL_PRAT_DE_LLOBREGAT', 'display_name': 'EL PRAT DE LLOBREGAT'},
    {'code': 'CD', 'name': 'LA_SEU_DURGELL', 'display_name': 'LA SEU D\'URGELL - BELLESTAR'},
    {'code': 'VK', 'name': 'LLEIDA', 'display_name': 'LLEIDA - RAIMAT'},
    {'code': 'Z3', 'name': 'MERANGES', 'display_name': 'MERANGES - MALNIU (2.230 M)'},
    {'code': 'YB', 'name': 'OLOT', 'display_name': 'OLOT'},
    {'code': 'YP', 'name': 'PALAFRUGELL', 'display_name': 'PALAFRUGELL'},
    {'code': 'D4', 'name': 'ROSES', 'display_name': 'ROSES'},
    {'code': 'ZC', 'name': 'SETCASES', 'display_name': 'SETCASES - ULLDETER (2.413 M)'},
    {'code': 'XH', 'name': 'SORT', 'display_name': 'SORT'},
    {'code': 'XE', 'name': 'TARRAGONA', 'display_name': 'TARRAGONA - COMPLEX EDUCATIU'},
    {'code': 'XO', 'name': 'VIC', 'display_name': 'VIC'},
    {'code': 'VS', 'name': 'VIELHA_E_MIJARAN', 'display_name': 'VIELHA E MIJARAN - LAC REDON (2.247 M)'},
    {'code': 'D7', 'name': 'VINEBRE', 'display_name': 'VINEBRE'}
]

CONFIG = {
    'version': 'v2.0',
    'generated_date': '2025-12-30 22:32:47',
    'total_stations': 18
}

if __name__ == "__main__":
    print(f"Configuració carregada correctament")
    print(f"Total d'estacions: {len(STATIONS)}")
    print()
    print("Llista d'estacions:")
    for i, station in enumerate(STATIONS, 1):
        print(f"  {i:2d}. {station['code']} - {station['display_name']}")
