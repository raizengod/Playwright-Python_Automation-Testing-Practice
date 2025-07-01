import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByAltText import AltLocatorsPage
from practice.utils import config

def test_visualizacion_de_imagen(set_up_byAtlText):
    page= set_up_byAtlText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    al= AltLocatorsPage(page)
    
    fg.validar_elemento_visible(al.logoPlaywright, "validar_elemento_visible_lo_playwright", config.SCREENSHOT_DIR)

def test_sub_descripcion_de_imagen(set_up_byAtlText):
    page= set_up_byAtlText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    al= AltLocatorsPage(page)
    
    fg.verificar_texto_contenido(al.subDescripcionImagen, "Logo", "verificar_texto_contenido_subdescripcion_Imagen", config.SCREENSHOT_DIR)

def test_texto_alt_imagen(set_up_byAtlText):
    page= set_up_byAtlText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    al= AltLocatorsPage(page)
    
    fg.verificar_alt_imagen(al.logoPlaywright, "logo image", "verificar_alt_imagen_logo_Playwright", config.SCREENSHOT_DIR)
    

"""Hay una contradicción en el ouput que se debe mejor y corregir, sigue mostrando .wait_for_response"""   
@pytest.mark.skip(reason= "No es perfecta la función")
def test_estatus_de_carga_de_imagen(set_up_byAtlText):
    page= set_up_byAtlText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    al= AltLocatorsPage(page)
    
    fg.verificar_carga_exitosa_imagen(al.logoPlaywright, "verificar_carga_exitosa_imagen_logo_playwright", config.SCREENSHOT_DIR)
    