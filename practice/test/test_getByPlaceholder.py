import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByPlaceholder import PlaceholderLocatorsPage
from practice.utils import config

def test_rellenar_campo_por_placeholder(set_up_byPlaceholder):
    page= set_up_byPlaceholder
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lp= PlaceholderLocatorsPage(page)
    
    fg.rellenar_campo_de_texto(lp.campoPlaceholderEmail, "test@test.com", "rellenar_campo_de_texto_campo_Placeholder_Email", config.SCREENSHOT_DIR, 1)
    fg.rellenar_campo_numerico_positivo(lp.campoPlaceholderTelefono, 1234567890, "rellenar_campo_numerico_positivo_campo_Placeholder_Email", config.SCREENSHOT_DIR, 1)
    fg.rellenar_campo_de_texto(lp.campoPlaceholderMensaje, "Esto es una prueba automatizada para locator placeholder", "rellenar_campo_de_texto_campo_Placeholdr_Mensaje", config.SCREENSHOT_DIR, 1)
    fg.rellenar_campo_de_texto(lp.campoPlaceholderBuscar, "Buscar por placeholcer", "rellenar_campo_de_texto_campo_placeholder_buscar", config.SCREENSHOT_DIR, 1)
    
def test_verificar_contenido_campo_por_placeholder(set_up_byPlaceholder):
    page= set_up_byPlaceholder
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lp= PlaceholderLocatorsPage(page)
    
    fg.verificar_valor_campo(lp.campoPlaceholderEmail, "test@test.com", "verificar_valor_campo_campo_Placeholder_Email", config.SCREENSHOT_DIR, 1)
    fg.verificar_valor_campo_numerico_int(lp.campoPlaceholderTelefono, 1234567890, "verificar_valor_campo_numerico_int_campo_Placeholder_Email", config.SCREENSHOT_DIR, 1)
    fg.verificar_valor_campo(lp.campoPlaceholderMensaje, "Esto es una prueba automatizada para locator placeholder", "verificar_valor_campo_campo_Placeholder_Mensaje", config.SCREENSHOT_DIR, 1)
    fg.verificar_valor_campo(lp.campoPlaceholderBuscar, "Buscar por placeholcer", "verificar_valor_campo_campo_placeholder_buscar", config.SCREENSHOT_DIR, 1)
    
def test_hacer_click_boton_buscar(set_up_byPlaceholder):
    page= set_up_byPlaceholder
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lp= PlaceholderLocatorsPage(page)

    fg.hacer_click_en_elemento(lp.botonBuscar, "hacer_click_en_elemento_botón_buscar", config.SCREENSHOT_DIR, None)
    