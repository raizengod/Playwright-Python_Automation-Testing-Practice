import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_mouseAction import MouseActionsLocatorsPage
from practice.utils import config

def test_ver_titulo_y_descripcion(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    
    fg.verificar_texto_contenido(mal.tituloMouseHover, "Mouse Hover", "verificar_texto_contenido_titulo_MouseHover", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(mal.descripcionMouseHover, "Move the mouse over the button to open the dropdown menu.", "verificar_texto_contenido_titulo_MouseHover", config.SCREENSHOT_DIR)
    
    
def test_hacer_mouse_hover(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    
    fg.validar_elemento_no_visible(mal.opcionMobil, "validar_elemento_no_visibleopcion_Mobil", config.SCREENSHOT_DIR)
    fg.validar_elemento_no_visible(mal.opcionLaptop, "validar_elemento_no_visibleopcion_Laptop", config.SCREENSHOT_DIR)
    fg.hacer_hover_en_elemento(mal.botonHover, "hacer_hover_en_elemento_boton_hover", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(mal.opcionMobil, "validar_elemento_visible_opcion_mobil", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(mal.opcionLaptop, "validar_elemento_visible_opcion_Laptop", config.SCREENSHOT_DIR)
    
def test_hacer_click_opcion_mobil(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    
    fg.hacer_hover_en_elemento(mal.botonHover, "hacer_hover_en_elemento_boton_hover", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(mal.opcionMobil, "hacer_click_en_elemento_opcion_Mobil", config.SCREENSHOT_DIR, "Mobiles")
    
def test_hacer_click_opcion_laptop(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    fg.scroll_pagina(0, 1100)
    fg.hacer_hover_en_elemento(mal.botonHover, "hacer_hover_en_elemento_boton_hover", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(mal.opcionLaptop, "hacer_click_en_elemento_opcion_Mobil", config.SCREENSHOT_DIR, "Laptops")
    
def test_hacer_doble_click(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    
    fg.scroll_pagina(0, 1100)
    
    fg.validar_elemento_visible(mal.tituloDobleClick, "validar_elemento_visible_titulo_Doble_Click", config.SCREENSHOT_DIR)
    fg.verificar_valor_campo(mal.campoUnoDobleClick, "Hello World!", "verificar_valor_campo_campo_Uno_Doble_Click", config.SCREENSHOT_DIR)
    fg.verificar_valor_campo(mal.campoDosDobleClick, "", "verificar_valor_campo_campo_Dos_Doble_Click", config.SCREENSHOT_DIR)
    
    fg.hacer_doble_click_en_elemento(mal.botonDobleClick, "hacer_doble_click_en_elemento_boton_Doble_Click", config.SCREENSHOT_DIR, "Copy Text")
    fg.verificar_valor_campo(mal.campoDosDobleClick, "Hello World!", "verificar_valor_campo_campo_Dos_Doble_Click", config.SCREENSHOT_DIR)
    
    fg.verificar_texto_contenido(mal.descripcionDobleClick, "Double click on button, the text from Field1 will be copied into Field2.", "verificar_texto_contenido_descripcion_Doble_Click", config.SCREENSHOT_DIR)
    
def test_hacer_Drag_and_Drop(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    
    fg.scroll_pagina(0, 600)
    fg.verificar_texto_contenido(mal.tituloDragAndDrop,"Drag and Drop", "verificar_texto_contenido_titulo_Drag_And_Drop", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(mal.objetoDragMe, "Drag me to my target", "verificar_texto_contenido_objeto_Drag_Me", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(mal.objetoDropHere, "Drop here", "verificar_texto_contenido_objeto_Drop_here", config.SCREENSHOT_DIR)
    
    fg.realizar_drag_and_drop(mal.objetoDragMe, mal.objetoDropHere, "realizar_drag_and_drop", config. SCREENSHOT_DIR)
    
def test_hacer_slider(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)
    
    fg.validar_elemento_visible(mal.tituloSlider, "validar_elemento_visible_titulo_slider", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(mal.subTituloPriceSlider, "validar_elemento_visible_sub_titulo_slider", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(mal.rangoPrecio, "validar_elemento_visible_rango_precio", config.SCREENSHOT_DIR)
    
    fg.mover_slider_rango(mal.puntoInicioSlider, mal.puntoFinalSlider, mal.barraSlider, 0.1, 0.5, "mover_slider_rango", config.SCREENSHOT_DIR)
    
    fg.verificar_valor_campo(mal.rangoPrecio, "$49 - $248", "verificar_valor_campo_rango_Precio", config.SCREENSHOT_DIR)
    
    fg.mover_slider_rango(mal.puntoInicioSlider, mal.puntoFinalSlider, mal.barraSlider, 0.13, 1.0, "mover_slider_rango", config.SCREENSHOT_DIR)
    
    fg.verificar_valor_campo(mal.rangoPrecio, "$64 - $498", "verificar_valor_campo_rango_Precio", config.SCREENSHOT_DIR)
    
    fg.mover_slider_rango(mal.puntoInicioSlider, mal.puntoFinalSlider, mal.barraSlider, 0.0, 1.0, "mover_slider_rango", config.SCREENSHOT_DIR)
    
    fg.verificar_valor_campo(mal.rangoPrecio, "$0 - $498", "verificar_valor_campo_rango_Precio", config.SCREENSHOT_DIR)
    
    fg.mover_slider_rango(mal.puntoInicioSlider, mal.puntoFinalSlider, mal.barraSlider, 0.4, 0.4, "mover_slider_rango", config.SCREENSHOT_DIR)
    
    fg.verificar_valor_campo(mal.rangoPrecio, "$198 - $198", "verificar_valor_campo_rango_Precio", config.SCREENSHOT_DIR)
    
    fg.mover_slider_rango(mal.puntoInicioSlider, mal.puntoFinalSlider, mal.barraSlider, 0.4, 0.7, "mover_slider_rango", config.SCREENSHOT_DIR)
    
    fg.verificar_valor_campo(mal.rangoPrecio, "$198 - $348", "verificar_valor_campo_rango_Precio", config.SCREENSHOT_DIR)
    
    fg.esperar_fijo(3)
    
def test_hacer_slider(set_up_mouseAction):
    page= set_up_mouseAction
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'MouseActionsLocatorsPage'
    mal= MouseActionsLocatorsPage(page)