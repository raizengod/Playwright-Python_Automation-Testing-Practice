import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByText import TextLocatorsPage
from practice.utils import config

def test_verificar_titulo_seccion_by_text(set_up_byText):
    page= set_up_byText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lt= TextLocatorsPage(page)
    

    fg.validar_elemento_visible(lt.tituloDos, "validar_elemento_visible_titulo_dos", config.SCREENSHOT_DIR, 1)
    fg.validar_elemento_visible(lt.descripcionByText, "validar_elemento_visible_descripción_by_text", config.SCREENSHOT_DIR, 1)
    
def test_verificar_explicaciones_by_text(set_up_byText):
    page= set_up_byText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lt= TextLocatorsPage(page)
    
    fg.validar_elemento_visible(lt.textExplicacion1, "validar_elemento_visible_explicación_1", config.SCREENSHOT_DIR, 1)
    fg.validar_elemento_visible(lt.textExplicacion2, "validar_elemento_visible_explicación_2", config.SCREENSHOT_DIR, 1)
    
def test_verificar_lista_by_text(set_up_byText):
    page= set_up_byText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lt= TextLocatorsPage(page)
    
    fg.validar_elemento_visible(lt.item1, "validar_elemento_visible_item_1", config.SCREENSHOT_DIR, 1)
    fg.validar_elemento_visible(lt.item2, "validar_elemento_visible_item_2", config.SCREENSHOT_DIR, 1)
    fg.hacer_click_en_elemento(lt.item2, "hacer_click_en_elemento_item_2", config.SCREENSHOT_DIR, None, 1)
    fg.scroll_pagina(0, 500)
    fg.validar_elemento_visible(lt.item3, "validar_elemento_visible_item_3", config.SCREENSHOT_DIR, 1)
    fg.hacer_click_en_elemento(lt.botonSubmit, "hacer_click_en_elemento_botón_submit", config.SCREENSHOT_DIR, None, 1)
    fg.validar_elemento_visible(lt.explicacionBoton, "validar_elemento_visible_explicación_botón_submit", config.SCREENSHOT_DIR, 1)