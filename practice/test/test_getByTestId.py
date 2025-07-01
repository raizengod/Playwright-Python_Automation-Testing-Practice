import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByTestId import IdTestLocatorsPage
from practice.utils import config

def test_verificar_datos_jone_doe(set_up_byTestId):
    page= set_up_byTestId
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    til= IdTestLocatorsPage(page)
    
    fg.verificar_texto_contenido(til.nombreDoe, "John Doe", "verificar_texto_contenido_nombre_doe", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(til.correoJone, "john.doe@example.com", "verificar_texto_contenido_correp_jone", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(til.botonEditarPerfil, "hacer_click_en_elemento_editar_perfil", config.SCREENSHOT_DIR, "Edit Profile")
    
def test_verificar_dato_producto_a(set_up_byTestId):
    page= set_up_byTestId
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    til= IdTestLocatorsPage(page)
    
    fg.verificar_texto_contenido(til.productoANombre, "Product A", "verificar_texto_contenido_producto_a_nombre", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(til.productoAPrecio, "19.99", "verificar_texto_contenido_producto_a_nombre", config.SCREENSHOT_DIR)
    
def test_verificar_dato_producto_b(set_up_byTestId):
    page= set_up_byTestId
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    til= IdTestLocatorsPage(page)
    
    fg.verificar_texto_contenido(til.productoBNombre, "Product B", "verificar_texto_contenido_producto_b_nombre", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(til.productoBPrecio, ".99", "verificar_texto_contenido_producto_b_nombre", config.SCREENSHOT_DIR)
    
def test_verificar_dato_producto_c(set_up_byTestId):
    page= set_up_byTestId
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    til= IdTestLocatorsPage(page)
    
    fg.verificar_texto_contenido(til.productoCNombre, "Product C", "verificar_texto_contenido_producto_c_nombre", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(til.productoCPrecio, "$3", "verificar_texto_contenido_producto_c_nombre", config.SCREENSHOT_DIR)
    
def test_interaccion_con_links(set_up_byTestId):
    page= set_up_byTestId
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    til= IdTestLocatorsPage(page)
    
    fg.hacer_click_en_elemento(til.linkHombe, "hacer_click_en_elemento_link_home", config.SCREENSHOT_DIR, "Home")
    fg.hacer_click_en_elemento(til.linkProducts, "hacer_click_en_elemento_link_productos", config.SCREENSHOT_DIR, "Products")
    fg.hacer_click_en_elemento(til.linkContact, "hacer_click_en_elemento_link_contacto", config.SCREENSHOT_DIR, None)