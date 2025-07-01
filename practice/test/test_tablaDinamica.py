import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_tablaDinamica import TablaDinamicaLocatorsPage
from practice.utils import config

def test_visibilidad_tabla_y_valores(set_up_manejodDeTabla):
    page= set_up_manejodDeTabla
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'TablaDinamicaLocatorsPage'
    tdl= TablaDinamicaLocatorsPage(page)
    
    fg.validar_elemento_visible(tdl.tablaDinamica, "validar_elemento_visible_tabla_dinamica", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(tdl.listaValores, "validar_elemento_visible_lista_valores_dinamicos", config.SCREENSHOT_DIR)
    
def test_verificar_dimension_tabla(set_up_manejodDeTabla):
    page= set_up_manejodDeTabla
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'TablaDinamicaLocatorsPage'
    tdl= TablaDinamicaLocatorsPage(page)
    
    fg.obtener_dimensiones_tabla(tdl.tablaDinamica, "obtener_dimension_tabla_dinamica", config.SCREENSHOT_DIR)
    
def test_comparar_valor_texto_y_tabla(set_up_manejodDeTabla):
    page= set_up_manejodDeTabla
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'TablaDinamicaLocatorsPage'
    tdl= TablaDinamicaLocatorsPage(page)
    
    fg.busqueda_estricta_imprimir_fila(tdl.tablaDinamica, fg.obtener_valor_elemento(tdl.textoCPU, "obtener_valor_elemento_texto_cpu", config.SCREENSHOT_DIR), "busqueda_estricta_imprimir_fila_tabla_dinamica", config.SCREENSHOT_DIR)
    fg.busqueda_estricta_imprimir_fila(tdl.tablaDinamica, fg.obtener_valor_elemento(tdl.textoMemoria, "obtener_valor_elemento_texto_memoria", config.SCREENSHOT_DIR), "busqueda_estricta_imprimir_fila_tabla_dinamica", config.SCREENSHOT_DIR)
    fg.busqueda_estricta_imprimir_fila(tdl.tablaDinamica, fg.obtener_valor_elemento(tdl.textoRed, "obtener_valor_elemento_texto_red", config.SCREENSHOT_DIR), "busqueda_estricta_imprimir_fila_tabla_dinamica", config.SCREENSHOT_DIR)
    fg.busqueda_estricta_imprimir_fila(tdl.tablaDinamica, fg.obtener_valor_elemento(tdl.textoDisco, "obtener_valor_elemento_texto_disco", config.SCREENSHOT_DIR), "busqueda_estricta_imprimir_fila_tabla_dinamica", config.SCREENSHOT_DIR)