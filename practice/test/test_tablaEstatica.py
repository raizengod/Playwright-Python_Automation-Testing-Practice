import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_tablaEstatica import TablaEstaticaLocatorsPage
from practice.utils import config

def test_obtener_dimensión_tabla(set_up_manejodDeTabla):
    page= set_up_manejodDeTabla
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tsl= TablaEstaticaLocatorsPage(page)
    
    fg.validar_elemento_visible(tsl.tabla, "validar_elemento_visible_tabla_estatica", config.SCREENSHOT_DIR, 1)
    fg.obtener_dimensiones_tabla(tsl.tabla, "obtener_dimensiones_tabla_estatica", config.SCREENSHOT_DIR)
    
    fg.busqueda_coincidencia_e_imprimir_fila(tsl.tabla, "Python", "busqueda_coincidencia_e_imprimir_fila_de_tabla", config.SCREENSHOT_DIR, 1)
    
def test_buscar_dato_tabla_imprimir(set_up_manejodDeTabla):
    page= set_up_manejodDeTabla
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tsl= TablaEstaticaLocatorsPage(page)
    
    fg.busqueda_coincidencia_e_imprimir_fila(tsl.tabla, "300", "busqueda_coincidencia_e_imprimir_fila_de_tabla", config.SCREENSHOT_DIR, 1)
    fg.busqueda_estricta_imprimir_fila(tsl.tabla, "Java", "busqueda_estricta_imprimir_fila_de_tabla", config.SCREENSHOT_DIR, 1)
