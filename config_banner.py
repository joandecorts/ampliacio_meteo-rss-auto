"""
CONFIGURACIÓ BANNER NEWS CHANNEL - VERSIÓ DADES REALS
Configuració per al sistema de banner meteorològic amb dades reals de Meteocat
Fitxer generat automàticament: 2026-01-07 01:01:18
Total estacions: 189 (Actives: 25, Comentades: 164)
"""

import os
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURACIÓ DE LES ESTACIONS (189 estacions) - ORDENADES ALFABÈTICAMENT
# Les estacions comentades (COM) tenen un # al davant
# ============================================================================
STATIONS = [
    # {'code': 'WB', 'name': 'ALBESA_[WB]_WB', 'display_name': 'Albesa [wb]'},  # COM
    # {'code': 'XY', 'name': 'ALCARRAS_[XY]_XY', 'display_name': 'Alcarràs [xy]'},  # COM
    # {'code': 'U7', 'name': 'ALDOVER_[U7]_U7', 'display_name': 'Aldover [u7]'},  # COM
    # {'code': 'WK', 'name': 'ALFARRAS_[WK]_WK', 'display_name': 'Alfarràs [wk]'},  # COM
    # {'code': 'WG', 'name': 'ALGERRI_[WG]_WG', 'display_name': 'Algerri [wg]'},  # COM
    # {'code': 'X3', 'name': 'ALGUAIRE_[X3]_X3', 'display_name': 'Alguaire [x3]'},  # COM
    # {'code': 'ZB', 'name': 'ALINS___SALORIA_2451_M_[ZB]_ZB', 'display_name': 'Alins - Salòria (2.451 m) [zb]'},  # COM
    # {'code': 'YT', 'name': 'ALT_ANEU___BONABE_1693_M_[YT]_YT', 'display_name': 'Alt Àneu - Bonabé (1.693 m) [yt]'},  # COM
    # {'code': 'Z1', 'name': 'ALT_ANEU___BONAIGUA_2266_M_[Z1]_Z1', 'display_name': 'Alt Àneu - Bonaigua (2.266 m) [z1]'},  # COM
    # {'code': 'UU', 'name': 'AMPOSTA_[UU]_UU', 'display_name': 'Amposta [uu]'},  # COM
    # {'code': 'XX', 'name': 'ANGLESOLA___TORNABOUS_[XX]_XX', 'display_name': 'Anglesola - Tornabous [xx]'},  # COM
    {'code': 'DN', 'name': 'ANGLES_DN', 'display_name': 'ANGLÈS [DN]'},
    # {'code': 'Z6', 'name': 'ARRES___SASSEUVA_2228_M_[Z6]_Z6', 'display_name': 'Arres - Sasseuva (2.228 m) [z6]'},  # COM
    # {'code': 'X6', 'name': 'ARTESA_DE_SEGRE___BALDOMAR_[X6]_X6', 'display_name': 'Artesa de Segre - Baldomar [x6]'},  # COM
    # {'code': 'WW', 'name': 'ARTES_[WW]_WW', 'display_name': 'Artés [ww]'},  # COM
    # {'code': 'VA', 'name': 'ASCO_[VA]_VA', 'display_name': 'Ascó [va]'},  # COM
    # {'code': 'WU', 'name': 'BADALONA___MUSEU_[WU]_WU', 'display_name': 'Badalona - Museu [wu]'},  # COM
    {'code': 'DJ', 'name': 'BANYOLES_DJ', 'display_name': 'BANYOLES [DJ]'},
    {'code': 'X4', 'name': 'BARCELONA_RAVAL', 'display_name': 'BARCELONA - EL RAVAL'},
    # {'code': 'D5', 'name': 'BARCELONA_FABRA', 'display_name': 'BARCELONA - OBSERVATORI FABRA'},  # COM
    # {'code': 'X8', 'name': 'BARCELONA___ZONA_UNIVERSITARIA_[X8]_X8', 'display_name': 'Barcelona - Zona Universitària [x8]'},  # COM
    # {'code': 'YX', 'name': 'BATEA_[YX]_YX', 'display_name': 'Batea [yx]'},  # COM
    # {'code': 'UF', 'name': 'BEGUES___PN_DEL_GARRAF___EL_RASCLER_[UF]_UF', 'display_name': 'Begues - Pn del Garraf - el Rascler [uf]'},  # COM
    # {'code': 'VB', 'name': 'BENISSANET_[VB]_VB', 'display_name': 'Benissanet [vb]'},  # COM
    # {'code': 'WM', 'name': 'BERGA___SANTUARI_DE_QUERALT_[WM]_WM', 'display_name': 'Berga - Santuari de Queralt [wm]'},  # COM
    # {'code': 'W8', 'name': 'BLANCAFORT_[W8]_W8', 'display_name': 'Blancafort [w8]'},  # COM
    # {'code': 'YS', 'name': 'CABANES_[YS]_YS', 'display_name': 'Cabanes [ys]'},  # COM
    # {'code': 'UP', 'name': 'CABRILS_[UP]_UP', 'display_name': 'Cabrils [up]'},  # COM
    # {'code': 'X9', 'name': 'CALDES_DE_MONTBUI_[X9]_X9', 'display_name': 'Caldes de Montbui [x9]'},  # COM
    # {'code': 'WX', 'name': 'CAMARASA_[WX]_WX', 'display_name': 'Camarasa [wx]'},  # COM
    # {'code': 'XU', 'name': 'CANYELLES_[XU]_XU', 'display_name': 'Canyelles [xu]'},  # COM
    # {'code': 'MQ', 'name': 'CARDONA_[MQ]_MQ', 'display_name': 'Cardona [mq]'},  # COM
    {'code': 'UN', 'name': 'CASSA_SELVA', 'display_name': 'CASSÀ DE LA SELVA [UN]'},
    # {'code': 'DO', 'name': 'CASTELL_DARO_PLATJA_DARO_I_SAGARO___CASTELL_DARO_[', 'display_name': 'Castell D\'aro, Platja D\'aro i S\'agaró - Castell D\'aro [do]'},  # COM
    {'code': 'MS', 'name': 'CASTELLAR_NHUG_CLOT', 'display_name': 'CASTELLAR DE N\'HUG - EL CLOT DEL MORO [MS]'},
    # {'code': 'XC', 'name': 'CASTELLBISBAL_[XC]_XC', 'display_name': 'Castellbisbal [xc]'},  # COM
    # {'code': 'U4', 'name': 'CASTELLNOU_DE_BAGES_[U4]_U4', 'display_name': 'Castellnou de Bages [u4]'},  # COM
    # {'code': 'C6', 'name': 'CASTELLNOU_DE_SEANA_[C6]_C6', 'display_name': 'Castellnou de Seana [c6]'},  # COM
    # {'code': 'W1', 'name': 'CASTELLO_DEMPURIES_[W1]_W1', 'display_name': 'Castelló D\'empúries [w1]'},  # COM
    # {'code': 'C8', 'name': 'CERVERA_[C8]_C8', 'display_name': 'Cervera [c8]'},  # COM
    # {'code': 'VQ', 'name': 'CONSTANTI_[VQ]_VQ', 'display_name': 'Constantí [vq]'},  # COM
    # {'code': 'MR', 'name': 'CORNUDELLA_DE_MONTSANT___PANTA_DE_SIURANA_[MR]_MR', 'display_name': 'Cornudella de Montsant - Pantà de Siurana [mr]'},  # COM
    # {'code': 'WZ', 'name': 'CUNIT_[WZ]_WZ', 'display_name': 'Cunit [wz]'},  # COM
    {'code': 'DP', 'name': 'DAS_AERODROM', 'display_name': 'DAS - AERÒDROM [DP]'},
    # {'code': 'UQ', 'name': 'DOSRIUS___PN_MONTNEGRE_CORREDOR_[UQ]_UQ', 'display_name': 'Dosrius - Pn Montnegre Corredor [uq]'},  # COM
    # {'code': 'WJ', 'name': 'EL_MASROIG___EL_MASROIG_[WJ]_WJ', 'display_name': 'El Masroig - el Masroig [wj]'},  # COM
    # {'code': 'UH', 'name': 'EL_MONTMELL___EL_MONTMELL_[UH]_UH', 'display_name': 'El Montmell - el Montmell [uh]'},  # COM
    # {'code': 'DB', 'name': 'EL_PERELLO___EL_PERELLO_[DB]_DB', 'display_name': 'El Perelló - el Perelló [db]'},  # COM
    # {'code': 'V8', 'name': 'EL_POAL___EL_POAL_[V8]_V8', 'display_name': 'El Poal - el Poal [v8]'},  # COM
    # {'code': 'CT', 'name': 'EL_PONT_DE_SUERT___EL_PONT_DE_SUERT_[CT]_CT', 'display_name': 'El Pont de Suert - el Pont de Suert [ct]'},  # COM
    # {'code': 'Y7', 'name': 'EL_PRAT_DE_LLOBREGAT___PORT_DE_BARCELONA___BOCANA_', 'display_name': 'El Prat de Llobregat - Port de Barcelona - Bocana Sud [y7]'},  # COM
    # {'code': 'YQ', 'name': 'EL_PRAT_DE_LLOBREGAT___PORT_DE_BARCELONA___ZAL_PRA', 'display_name': 'El Prat de Llobregat - Port de Barcelona - Zal Prat [yq]'},  # COM
    {'code': 'XL', 'name': 'PRAT_LLOBREGAT_XL', 'display_name': 'EL PRAT DE LLOBREGAT [XL]'},
    # {'code': 'D9', 'name': 'EL_VENDRELL___EL_VENDRELL_[D9]_D9', 'display_name': 'El Vendrell - el Vendrell [d9]'},  # COM
    # {'code': 'XM', 'name': 'ELS_ALAMUS___ELS_ALAMUS_[XM]_XM', 'display_name': 'Els Alamús - els Alamús [xm]'},  # COM
    # {'code': 'CE', 'name': 'ELS_HOSTALETS_DE_PIEROLA___ELS_HOSTALETS_DE_PIEROL', 'display_name': 'Els Hostalets de Pierola - els Hostalets de Pierola [ce]'},  # COM
    # {'code': 'VD', 'name': 'ELS_PLANS_DE_SIO___EL_CANOS_[VD]_VD', 'display_name': 'Els Plans de Sió - el Canós [vd]'},  # COM
    # {'code': 'VZ', 'name': 'ESPOLLA_[VZ]_VZ', 'display_name': 'Espolla [vz]'},  # COM
    # {'code': 'Z7', 'name': 'ESPOT_2519_M_[Z7]_Z7', 'display_name': 'Espot (2.519 m) [z7]'},  # COM
    # {'code': 'X1', 'name': 'FALSET_[X1]_X1', 'display_name': 'Falset [x1]'},  # COM
    # {'code': 'KP', 'name': 'FOGARS_DE_LA_SELVA_[KP]_KP', 'display_name': 'Fogars de la Selva [kp]'},  # COM
    # {'code': 'DI', 'name': 'FONT_RUBI_[DI]_DI', 'display_name': 'Font-rubí [di]'},  # COM
    {'code': 'UO', 'name': 'FORNELLS_SELVA', 'display_name': 'FORNELLS DE LA SELVA [UO]'},
    # {'code': 'Y4', 'name': 'FIGOLS_I_ALINYA___ALINYA_[Y4]_Y4', 'display_name': 'Fígols i Alinyà - Alinyà [y4]'},  # COM
    # {'code': 'XP', 'name': 'GANDESA_[XP]_XP', 'display_name': 'Gandesa [xp]'},  # COM
    # {'code': 'VH', 'name': 'GIMENELLS_I_EL_PLA_DE_LA_FONT___GIMENELLS_[VH]_VH', 'display_name': 'Gimenells i el Pla de la Font - Gimenells [vh]'},  # COM
    {'code': 'XJ', 'name': 'GIRONA_XJ', 'display_name': 'GIRONA [XJ]'},
    # {'code': 'UI', 'name': 'GISCLARENY_[UI]_UI', 'display_name': 'Gisclareny [ui]'},  # COM
    # {'code': 'WC', 'name': 'GOLMES_[WC]_WC', 'display_name': 'Golmés [wc]'},  # COM
    # {'code': 'YM', 'name': 'GRANOLLERS_[YM]_YM', 'display_name': 'Granollers [ym]'},  # COM
    # {'code': 'WV', 'name': 'GUARDIOLA_DE_BERGUEDA_[WV]_WV', 'display_name': 'Guardiola de Berguedà [wv]'},  # COM
    # {'code': 'MV', 'name': 'GUIXERS___VALLS_[MV]_MV', 'display_name': 'Guixers - Valls [mv]'},  # COM
    # {'code': 'D8', 'name': 'HORTA_DE_SANT_JOAN_[D8]_D8', 'display_name': 'Horta de Sant Joan [d8]'},  # COM
    # {'code': 'CP', 'name': 'ISONA_I_CONCA_DELLA___SANT_ROMA_DABELLA_[CP]_CP', 'display_name': 'Isona i Conca Dellà - Sant Romà D\'abella [cp]'},  # COM
    # {'code': 'U9', 'name': 'LALDEA___LALDEA_[U9]_U9', 'display_name': 'L\'aldea - L\'aldea [u9]'},  # COM
    # {'code': 'UA', 'name': 'LAMETLLA_DE_MAR___LAMETLLA_DE_MAR_[UA]_UA', 'display_name': 'L\'ametlla de Mar - L\'ametlla de Mar [ua]'},  # COM
    # {'code': 'CW', 'name': 'LESPLUGA_DE_FRANCOLI___LESPLUGA_DE_FRANCOLI_[CW]_C', 'display_name': 'L\'espluga de Francolí - L\'espluga de Francolí [cw]'},  # COM
    # {'code': 'YU', 'name': 'LESQUIROL___CANTONIGROS_[YU]_YU', 'display_name': 'L\'esquirol - Cantonigròs [yu]'},  # COM
    # {'code': 'DF', 'name': 'LA_BISBAL_DEMPORDA___LA_BISBAL_DEMPORDA_[DF]_DF', 'display_name': 'La Bisbal D\'empordà - la Bisbal D\'empordà [df]'},  # COM
    # {'code': 'WO', 'name': 'LA_BISBAL_DEL_PENEDES___LA_BISBAL_DEL_PENEDES_[WO]', 'display_name': 'La Bisbal del Penedès - la Bisbal del Penedès [wo]'},  # COM
    # {'code': 'ZE', 'name': 'LA_COMA_I_LA_PEDRA___EL_PORT_DEL_COMTE_2290_M_[ZE]', 'display_name': 'La Coma i la Pedra - el Port del Comte (2.290 m) [ze]'},  # COM
    # {'code': 'UM', 'name': 'LA_GRANADELLA___LA_GRANADELLA_[UM]_UM', 'display_name': 'La Granadella - la Granadella [um]'},  # COM
    # {'code': 'XB', 'name': 'LA_LLACUNA___LA_LLACUNA_[XB]_XB', 'display_name': 'La Llacuna - la Llacuna [xb]'},  # COM
    # {'code': 'YC', 'name': 'LA_POBLA_DE_SEGUR___LA_POBLA_DE_SEGUR_[YC]_YC', 'display_name': 'La Pobla de Segur - la Pobla de Segur [yc]'},  # COM
    # {'code': 'CR', 'name': 'LA_QUAR___LA_QUAR_[CR]_CR', 'display_name': 'La Quar - la Quar [cr]'},  # COM
    # {'code': 'KX', 'name': 'LA_ROCA_DEL_VALLES___LA_ROCA_DEL_VALLES___ETAP_CAR', 'display_name': 'La Roca del Vallès - la Roca del Vallès - Etap Cardedeu [kx]'},  # COM
    # {'code': 'UW', 'name': 'LA_RAPITA___ELS_ALFACS_[UW]_UW', 'display_name': 'La Ràpita - els Alfacs [uw]'},  # COM
    {'code': 'CD', 'name': 'SEU_URGELL_BELLESTAR', 'display_name': 'LA SEU D\'URGELL - BELLESTAR'},
    # {'code': 'UB', 'name': 'LA_TALLADA_DEMPORDA___LA_TALLADA_DEMPORDA_[UB]_UB', 'display_name': 'La Tallada D\'empordà - la Tallada D\'empordà [ub]'},  # COM
    # {'code': 'ZD', 'name': 'LA_TOSA_DALP_2478_M_[ZD]_ZD', 'display_name': 'La Tosa D\'alp (2.478 m) [zd]'},  # COM
    # {'code': 'W9', 'name': 'LA_VALL_DEN_BAS___LA_VALL_DEN_BAS_[W9]_W9', 'display_name': 'La Vall D\'en Bas - la Vall D\'en Bas [w9]'},  # COM
    {'code': 'Z2', 'name': 'LA_VALL_DE_BOI', 'display_name': 'LA VALL DE BOÍ - BOÍ (2.535 M)'},
    {'code': 'VS', 'name': 'LAC_REDON', 'display_name': 'LAC REDON (2.247 m)'},
    # {'code': 'YD', 'name': 'LES_BORGES_BLANQUES___LES_BORGES_BLANQUES_[YD]_YD', 'display_name': 'Les Borges Blanques - Les Borges Blanques [yd]'},  # COM
    # {'code': 'US', 'name': 'LES_CASES_DALCANAR_[US]_US', 'display_name': 'Les Cases D\'alcanar [us]'},  # COM
    # {'code': 'Z5', 'name': 'LLADORRE___CERTASCAN_2400_M_[Z5]_Z5', 'display_name': 'Lladorre - Certascan (2.400 m) [z5]'},  # COM
    # {'code': 'VO', 'name': 'LLADURS_[VO]_VO', 'display_name': 'Lladurs [vo]'},  # COM
    # {'code': 'YJ', 'name': 'LLEIDA___LA_FEMOSA_[YJ]_YJ', 'display_name': 'Lleida - la Femosa [yj]'},  # COM
    {'code': 'VK', 'name': 'LLEIDA_RAIMAT', 'display_name': 'LLEIDA - RAIMAT'},
    # {'code': 'WI', 'name': 'MAIALS_[WI]_WI', 'display_name': 'Maials [wi]'},  # COM
    # {'code': 'WT', 'name': 'MALGRAT_DE_MAR_[WT]_WT', 'display_name': 'Malgrat de Mar [wt]'},  # COM
    # {'code': 'D1', 'name': 'MARGALEF_[D1]_D1', 'display_name': 'Margalef [d1]'},  # COM
    # {'code': 'C9', 'name': 'MAS_DE_BARBERANS_[C9]_C9', 'display_name': 'Mas de Barberans [c9]'},  # COM
    # {'code': 'YE', 'name': 'MASSOTERES_[YE]_YE', 'display_name': 'Massoteres [ye]'},  # COM
    # {'code': 'YV', 'name': 'MATARO_[YV]_YV', 'display_name': 'Mataró [yv]'},  # COM
    # {'code': 'WP', 'name': 'MEDIONA___CANALETES_[WP]_WP', 'display_name': 'Mediona - Canaletes [wp]'},  # COM
    {'code': 'Z3', 'name': 'MERANGES_MALNIU', 'display_name': 'MERANGES - MALNIU (2.230 m)'},
    # {'code': 'XI', 'name': 'MOLLERUSSA_[XI]_XI', 'display_name': 'Mollerussa [xi]'},  # COM
    # {'code': 'CG', 'name': 'MOLLO___FABERT_[CG]_CG', 'display_name': 'Molló - Fabert [cg]'},  # COM
    # {'code': 'WN', 'name': 'MONISTROL_DE_MONTSERRAT___MONTSERRAT___SANT_DIMES_', 'display_name': 'Monistrol de Montserrat - Montserrat - Sant Dimes [wn]'},  # COM
    # {'code': 'YF', 'name': 'MONT_ROIG_DEL_CAMP___MIAMI_PLATJA_[YF]_YF', 'display_name': 'Mont-roig del Camp - Miami Platja [yf]'},  # COM
    # {'code': 'Z9', 'name': 'MONTELLA_I_MARTINET___CADI_NORD_2143_M___PRAT_DAGU', 'display_name': 'Montellà i Martinet - Cadí Nord (2.143 m) - Prat D\'aguiló [z9]'},  # COM
    # {'code': 'V4', 'name': 'MONTESQUIU_[V4]_V4', 'display_name': 'Montesquiu [v4]'},  # COM
    # {'code': 'XA', 'name': 'MONTMANEU___LA_PANADELLA_[XA]_XA', 'display_name': 'Montmaneu - la Panadella [xa]'},  # COM
    # {'code': 'CY', 'name': 'MUNTANYOLA_[CY]_CY', 'display_name': 'Muntanyola [cy]'},  # COM
    # {'code': 'Y5', 'name': 'NAVATA_[Y5]_Y5', 'display_name': 'Navata [y5]'},  # COM
    # {'code': 'MW', 'name': 'NAVES_[MW]_MW', 'display_name': 'Navès [mw]'},  # COM
    # {'code': 'VY', 'name': 'NULLES_[VY]_VY', 'display_name': 'Nulles [vy]'},  # COM
    # {'code': 'W5', 'name': 'OLIANA_[W5]_W5', 'display_name': 'Oliana [w5]'},  # COM
    # {'code': 'WA', 'name': 'OLIOLA_[WA]_WA', 'display_name': 'Oliola [wa]'},  # COM
    {'code': 'YB', 'name': 'OLOT_YB', 'display_name': 'OLOT [YB]'},
    # {'code': 'CJ', 'name': 'ORGANYA_[CJ]_CJ', 'display_name': 'Organyà [cj]'},  # COM
    # {'code': 'CC', 'name': 'ORIS_[CC]_CC', 'display_name': 'Orís [cc]'},  # COM
    # {'code': 'UY', 'name': 'OS_DE_BALAGUER___EL_MONESTIR_DAVELLANES_[UY]_UY', 'display_name': 'Os de Balaguer - el Monestir D\'avellanes [uy]'},  # COM
    {'code': 'YP', 'name': 'PALAFRUGELL_YP', 'display_name': 'PALAFRUGELL [YP]'},
    {'code': 'J5', 'name': 'DARNIUS_BOADELLA', 'display_name': 'PANTÀ DE DARNIUS - BOADELLA [J5]'},
    # {'code': 'XG', 'name': 'PARETS_DEL_VALLES_[XG]_XG', 'display_name': 'Parets del Vallès [xg]'},  # COM
    # {'code': 'V5', 'name': 'PERAFITA_[V5]_V5', 'display_name': 'Perafita [v5]'},  # COM
    # {'code': 'VP', 'name': 'PINOS_[VP]_VP', 'display_name': 'Pinós [vp]'},  # COM
    # {'code': 'D6', 'name': 'PORTBOU___COLL_DELS_BELITRES_[D6]_D6', 'display_name': 'Portbou - Coll dels Belitres [d6]'},  # COM
    # {'code': 'XR', 'name': 'PRADES_[XR]_XR', 'display_name': 'Prades [xr]'},  # COM
    {'code': 'XK', 'name': 'PUIG_SESOLLES', 'display_name': 'PUIG SESOLLES (1.668 m)'},
    # {'code': 'YA', 'name': 'PUIGCERDA_[YA]_YA', 'display_name': 'Puigcerdà [ya]'},  # COM
    # {'code': 'YH', 'name': 'PUJALT_[YH]_YH', 'display_name': 'Pujalt [yh]'},  # COM
    {'code': 'DG', 'name': 'QUERALBS_NURIA', 'display_name': 'QUERALBS - NÚRIA (1.971 m)'},
    # {'code': 'VU', 'name': 'RELLINARS_[VU]_VU', 'display_name': 'Rellinars [vu]'},  # COM
    # {'code': 'VC', 'name': 'RIBA_ROJA_DEBRE___PANTA_DE_RIBA_ROJA_[VC]_VC', 'display_name': 'Riba-roja D\'ebre - Pantà de Riba-roja [vc]'},  # COM
    # {'code': 'YL', 'name': 'RIUDECANYES_[YL]_YL', 'display_name': 'Riudecanyes [yl]'},  # COM
    # {'code': 'X5', 'name': 'ROQUETES___PN_DELS_PORTS_[X5]_X5', 'display_name': 'Roquetes - Pn dels Ports [x5]'},  # COM
    {'code': 'D4', 'name': 'ROSES_D4', 'display_name': 'ROSES [D4]'},
    # {'code': 'XF', 'name': 'SABADELL___PARC_AGRARI_[XF]_XF', 'display_name': 'Sabadell - Parc Agrari [xf]'},  # COM
    # {'code': 'XV', 'name': 'SANT_CUGAT_DEL_VALLES___CAR_[XV]_XV', 'display_name': 'Sant Cugat del Vallès - Car [xv]'},  # COM
    # {'code': 'WQ', 'name': 'SANT_ESTEVE_DE_LA_SARGA___MONTSEC_DARES_1572_M_[WQ', 'display_name': 'Sant Esteve de la Sarga - Montsec D\'ares (1.572 m) [wq]'},  # COM
    # {'code': 'DL', 'name': 'SANT_JAUME_DENVEJA___ILLA_DE_BUDA_[DL]_DL', 'display_name': 'Sant Jaume D\'enveja - Illa de Buda [dl]'},  # COM
    # {'code': 'M6', 'name': 'SANT_JOAN_DE_LES_ABADESSES_[M6]_M6', 'display_name': 'Sant Joan de Les Abadesses [m6]'},  # COM
    # {'code': 'VV', 'name': 'SANT_LLORENC_SAVALL_[VV]_VV', 'display_name': 'Sant Llorenç Savall [vv]'},  # COM
    # {'code': 'WL', 'name': 'SANT_MARTI_DE_RIUCORB_[WL]_WL', 'display_name': 'Sant Martí de Riucorb [wl]'},  # COM
    # {'code': 'U3', 'name': 'SANT_MARTI_SARROCA_[U3]_U3', 'display_name': 'Sant Martí Sarroca [u3]'},  # COM
    {'code': 'CI', 'name': 'SANT_PAU_SEGURIES', 'display_name': 'SANT PAU DE SEGÚRIES [CI]'},
    # {'code': 'UK', 'name': 'SANT_PERE_DE_RIBES___PN_DEL_GARRAF_[UK]_UK', 'display_name': 'Sant Pere de Ribes - Pn del Garraf [uk]'},  # COM
    # {'code': 'U2', 'name': 'SANT_PERE_PESCADOR_[U2]_U2', 'display_name': 'Sant Pere Pescador [u2]'},  # COM
    # {'code': 'YO', 'name': 'SANT_SADURNI_DANOIA_[YO]_YO', 'display_name': 'Sant Sadurní D\'anoia [yo]'},  # COM
    # {'code': 'CL', 'name': 'SANT_SALVADOR_DE_GUARDIOLA_[CL]_CL', 'display_name': 'Sant Salvador de Guardiola [cl]'},  # COM
    # {'code': 'XS', 'name': 'SANTA_COLOMA_DE_FARNERS_[XS]_XS', 'display_name': 'Santa Coloma de Farners [xs]'},  # COM
    # {'code': 'UJ', 'name': 'SANTA_COLOMA_DE_QUERALT_[UJ]_UJ', 'display_name': 'Santa Coloma de Queralt [uj]'},  # COM
    # {'code': 'XN', 'name': 'SEROS_[XN]_XN', 'display_name': 'Seròs [xn]'},  # COM
    {'code': 'ZC', 'name': 'SETCASES_ULLDETER', 'display_name': 'SETCASES-ULLDETER (2.413 m)'},
    # {'code': 'XT', 'name': 'SOLSONA_[XT]_XT', 'display_name': 'Solsona [xt]'},  # COM
    {'code': 'XH', 'name': 'SORT_XH', 'display_name': 'SORT [XH]'},
    # {'code': 'VX', 'name': 'TAGAMANENT___PN_DEL_MONTSENY_[VX]_VX', 'display_name': 'Tagamanent - Pn del Montseny [vx]'},  # COM
    {'code': 'XE', 'name': 'TARRAGONA_XE', 'display_name': 'TARRAGONA - COMPLEX EDUCATIU'},
    # {'code': 'YK', 'name': 'TERRASSA_[YK]_YK', 'display_name': 'Terrassa [yk]'},  # COM
    # {'code': 'Y6', 'name': 'TIVISSA_[Y6]_Y6', 'display_name': 'Tivissa [y6]'},  # COM
    # {'code': 'DK', 'name': 'TORREDEMBARRA_[DK]_DK', 'display_name': 'Torredembarra [dk]'},  # COM
    # {'code': 'X7', 'name': 'TORRES_DE_SEGRE_[X7]_X7', 'display_name': 'Torres de Segre [x7]'},  # COM
    # {'code': 'XZ', 'name': 'TORROELLA_DE_FLUVIA_[XZ]_XZ', 'display_name': 'Torroella de Fluvià [xz]'},  # COM
    # {'code': 'UE', 'name': 'TORROELLA_DE_MONTGRI_[UE]_UE', 'display_name': 'Torroella de Montgrí [ue]'},  # COM
    # {'code': 'WR', 'name': 'TORROJA_DEL_PRIORAT_[WR]_WR', 'display_name': 'Torroja del Priorat [wr]'},  # COM
    # {'code': 'XQ', 'name': 'TREMP_[XQ]_XQ', 'display_name': 'Tremp [xq]'},  # COM
    # {'code': 'C7', 'name': 'TARREGA_[C7]_C7', 'display_name': 'Tàrrega [c7]'},  # COM
    # {'code': 'YG', 'name': 'TIRVIA_[YG]_YG', 'display_name': 'Tírvia [yg]'},  # COM
    # {'code': 'UX', 'name': 'ULLDECONA___ELS_VALENTINS_[UX]_UX', 'display_name': 'Ulldecona - els Valentins [ux]'},  # COM
    # {'code': 'XD', 'name': 'ULLDEMOLINS_[XD]_XD', 'display_name': 'Ulldemolins [xd]'},  # COM
    # {'code': 'D2', 'name': 'VACARISSES_[D2]_D2', 'display_name': 'Vacarisses [d2]'},  # COM
    # {'code': 'V1', 'name': 'VALLFOGONA_DE_BALAGUER_[V1]_V1', 'display_name': 'Vallfogona de Balaguer [v1]'},  # COM
    # {'code': 'D3', 'name': 'VALLIRANA_[D3]_D3', 'display_name': 'Vallirana [d3]'},  # COM
    {'code': 'XO', 'name': 'VIC_XO', 'display_name': 'VIC [XO]'},
    # {'code': 'YN', 'name': 'VIELHA_E_MIJARAN___VIELHA___ELIPORT_[YN]_YN', 'display_name': 'Vielha e Mijaran - Vielha - Elipòrt [yn]'},  # COM
    # {'code': 'DQ', 'name': 'VILA_RODONA_[DQ]_DQ', 'display_name': 'Vila-rodona [dq]'},  # COM
    # {'code': 'UG', 'name': 'VILADECANS_[UG]_UG', 'display_name': 'Viladecans [ug]'},  # COM
    # {'code': 'WS', 'name': 'VILADRAU_[WS]_WS', 'display_name': 'Viladrau [ws]'},  # COM
    # {'code': 'W4', 'name': 'VILAFRANCA_DEL_PENEDES___LA_GRANADA_[W4]_W4', 'display_name': 'Vilafranca del Penedès - la Granada [w4]'},  # COM
    # {'code': 'CQ', 'name': 'VILANOVA_DE_MEIA_[CQ]_CQ', 'display_name': 'Vilanova de Meià [cq]'},  # COM
    # {'code': 'KE', 'name': 'VILANOVA_DE_SAU___PANTA_DE_SAU_[KE]_KE', 'display_name': 'Vilanova de Sau - Pantà de Sau [ke]'},  # COM
    # {'code': 'VM', 'name': 'VILANOVA_DE_SEGRIA_[VM]_VM', 'display_name': 'Vilanova de Segrià [vm]'},  # COM
    # {'code': 'YR', 'name': 'VILANOVA_I_LA_GELTRU_[YR]_YR', 'display_name': 'Vilanova i la Geltrú [yr]'},  # COM
    # {'code': 'D7', 'name': 'VINEBRE_[D7]_D7', 'display_name': 'Vinebre [d7]'},  # COM
    # {'code': 'U6', 'name': 'VINYOLS_I_ELS_ARCS___CAMBRILS_[U6]_U6', 'display_name': 'Vinyols i els Arcs - Cambrils [u6]'},  # COM
    # {'code': 'H1', 'name': 'ODENA_[H1]_H1', 'display_name': 'Òdena [h1]'},  # COM
]

# ============================================================================
# VARIABLES METEOROLÒGIQUES A CAPTURAR
# ============================================================================
VARIABLES = {
    'TX': 'Temperatura màxima (°C)',
    'TN': 'Temperatura mínima (°C)', 
    'PPT': 'Precipitació (mm)'
}

# ============================================================================
# CONFIGURACIÓ DE RUTES
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Fitxers de dades
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

LATEST_DATA_FILE = os.path.join(DATA_DIR, 'latest_weather.json')
HISTORICAL_DIR = os.path.join(DATA_DIR, 'historical')
os.makedirs(HISTORICAL_DIR, exist_ok=True)

# Fitxers HTML
HTML_TEMPLATE = os.path.join(BASE_DIR, 'banner_news_channel.html')
OUTPUT_HTML = os.path.join(BASE_DIR, 'banner_output.html')

# ============================================================================
# CONFIGURACIÓ API METEOCAT
# ============================================================================
METEOcat_CONFIG = {
    'api_base': 'https://api.meteo.cat/v1',
    'timeout': 30,
    'max_retries': 3,
    'backoff_factor': 2
}

API_KEY = None  # Modo web scraping

# ============================================================================
# CONFIGURACIÓ DE TEMPS
# ============================================================================
# Període de dades (avui)
TODAY = datetime.now().date()
YESTERDAY = TODAY - timedelta(days=1)

# Scroll del banner
SCROLL_CONFIG = {
    'transition_duration': 0.8,
    'display_duration': 15,
    'stations_per_view': 2
}

# ============================================================================
# FUNCIONS UTILS
# ============================================================================
def get_current_datetime():
    """Retorna la data i hora actual formatejada"""
    now = datetime.now()
    return {
        'time': now.strftime('%H:%M'),
        'date': now.strftime('%d/%m/%Y'),
        'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
        'timestamp': int(now.timestamp())
    }

def get_update_text():
    """Retorna el text d'actualització per al peu del banner"""
    current = get_current_datetime()
    return f"Actualitzat: {current['time']} - Data: {current['date']}"

def get_station_file_path(station_code):
    """Retorna la ruta del fitxer històric per una estació"""
    return os.path.join(HISTORICAL_DIR, f"{station_code}.json")

# ============================================================================
# VALORS PER DEFECTE
# ============================================================================
DEFAULT_VALUES = {
    'TX': '--',
    'TN': '--',
    'PPT': '--'
}

# ============================================================================
# INFORMACIÓ DE GENERACIÓ
# ============================================================================
GENERATION_INFO = {
    'generated_at': '2026-01-07 01:01:18',
    'total_stations': 189,
    'active_stations': 25,
    'comented_stations': 164,
    'false_stations': 0,
    'config_banner_version': 'v2.0 - Lògica: Op+CERT+Activa',
    'generator': 'ConfiguradorEstacions v2.0'
}

# ============================================================================
# COMPROVACIÓ INICIAL
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print(f"CONFIG_BANNER.PY - VERSIÓ {GENERATION_INFO['config_banner_version']}")
    print("=" * 70)
    print(f"📊 Total estacions: {len(STATIONS)}")
    print(f"✅ Actives: {GENERATION_INFO['active_stations']}")
    print(f"💬 Comentades: {GENERATION_INFO['comented_stations']}")
    print(f"🗑️ Desmantellades: {GENERATION_INFO['false_stations']}")
    print("=" * 70)
    
    active_count = 0
    commented_count = 0
    
    for i, station_line in enumerate(STATIONS, 1):
        # Determinar si l'estació està comentada
        if isinstance(station_line, str) and station_line.strip().startswith('#'):
            status = "💬"
            commented_count += 1
        else:
            status = "✅"
            active_count += 1
        
        # Mostrar la línia
        print(f"  {status} {i:2}. {station_line}")
    
    print("=" * 70)
    print(f"🚀 Configuració carregada correctament!")
    print(f"✅ Actives reals: {active_count}")
    print(f"💬 Comentades reals: {commented_count}")
    print(f"💾 Dades actualitzades: {GENERATION_INFO['generated_at']}")
    print("=" * 70)
