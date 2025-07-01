import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByTitle import TitleLocatorsPage
from practice.utils import config

def test_visualiza_explicacion(set_up_byTitle):
    page= set_up_byTitle
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tl= TitleLocatorsPage(page)
    
    fg.verificar_texto_contenido(tl.explicacionText, "to see their titles:", "verificar_texto_contenido_explicacion_text", config.SCREENSHOT_DIR)
    
def test_mouse_sobre_home(set_up_byTitle):
    page= set_up_byTitle
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tl= TitleLocatorsPage(page)
    
    fg.hacer_hover_en_elemento(tl.homeLink, "hacer_hover_en_elemento_home_link", config.SCREENSHOT_DIR, "Home", 1)
    fg.hacer_click_en_elemento(tl.homeLink, "hacer_click_en_elemento_home_link", config.SCREENSHOT_DIR, None)
    
def test_mouse_sobre_html(set_up_byTitle):
    page= set_up_byTitle
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tl= TitleLocatorsPage(page)
    
    fg.scroll_pagina(0, 2550)
    fg.hacer_hover_en_elemento(tl.htmlText, "hacer_hover_en_elemento_html_text", config.SCREENSHOT_DIR, "HTML", 1)
    
def test_mouse_sobre_text_Tooltip(set_up_byTitle):
    page= set_up_byTitle
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tl= TitleLocatorsPage(page)
    
    fg.hacer_hover_en_elemento(tl.textTooltip, "hacer_hover_en_elemento_text_Tooltip", config.SCREENSHOT_DIR, "This text has a tooltip", 1)
    
def test_mouse_sobre_boton_save(set_up_byTitle):
    page= set_up_byTitle
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    tl= TitleLocatorsPage(page)
    
    fg.hacer_hover_en_elemento(tl.saveBoton, "hacer_hover_en_elemento_save_boton", config.SCREENSHOT_DIR, "Save", 1)
    fg.hacer_click_en_elemento(tl.saveBoton, "hacer_click_en_elemento_save_boton", config.SCREENSHOT_DIR, None)