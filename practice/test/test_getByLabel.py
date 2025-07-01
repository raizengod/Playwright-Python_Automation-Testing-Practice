import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByLabel import LabelLocatorsPage
from practice.utils import config

def test_rellenar_campo_por_label(set_up_byLabel):
    page= set_up_byLabel
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    ll= LabelLocatorsPage(page)
    
    fg.rellenar_campo_de_texto(ll.campoEmail, "prueba@prueba.com", "rellenar_campo_de_texto_email", config.SCREENSHOT_DIR, 1)
    fg.rellenar_campo_de_texto(ll.campoClave, "Clave.123", "rellenar_campo_de_texto_password", config.SCREENSHOT_DIR, 1)
    fg.rellenar_campo_numerico_positivo(ll.campoEdad, 5555, "rellenar_campo_numerico_positivo_edad", config.SCREENSHOT_DIR, 1)
    
def test_verificar_contenido_campo_por_label(set_up_byLabel):
    page= set_up_byLabel
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    ll= LabelLocatorsPage(page)
    
    fg.verificar_valor_campo(ll.campoEmail, "prueba@prueba.com", "verificar_texto_contenido_email", config.SCREENSHOT_DIR, 1)
    fg.verificar_valor_campo(ll.campoClave, "Clave.123", "verificar_valor_campo_password", config.SCREENSHOT_DIR, 1)
    fg.verificar_valor_campo_numerico_int(ll.campoEdad, 5555, "verificar_valor_campo_edad", config.SCREENSHOT_DIR, 1)
    
def test_seleccion_option(set_up_byLabel):
    page= set_up_byLabel
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    ll= LabelLocatorsPage(page)
    
    fg.marcar_checkbox(ll.optionStandar, "marcar_checkbox_option_standar", config.SCREENSHOT_DIR, 1)
    fg.marcar_checkbox(ll.optionExpress, "marcar_checkbox_option_express", config.SCREENSHOT_DIR, 1)