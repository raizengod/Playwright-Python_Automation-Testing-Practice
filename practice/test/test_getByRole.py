import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByRole import RoleLocatorsPage
from practice.locator.locator_barraMenu import MenuLocatorsPage
from practice.utils import config

def test_ir_a_opcion_playwright(set_up):
    page= set_up
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    #IMPORTANTE: Creamos un objeto de tipo función 'barraMenu'
    ml= MenuLocatorsPage(page)

    fg.validar_url_actual("https://testautomationpractice.blogspot.com")
    fg.hacer_click_en_elemento(ml.irAPlaywright, "Clic_PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
    #Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
    fg.esperar_fijo(1)
    fg.validar_url_actual(".*/p/playwrightpractice.html")
    #Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
    fg.esperar_fijo(1)
    
def test_verificar_titulo_seccion(set_up_ir_a):
    page= set_up_ir_a
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.validar_elemento_visible(lr.tituloUno, "validar_elemento_visible_Titulo_getByRole", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.tituloUno, "1. getByRole() Locators", "verificar_texto_contenido_Titulo_getByRole", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(lr.labelDescripcion, "validar_elemento_visible_Descripción_getByRole", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.labelDescripcion, "implicit ARIA roles.", "verificar_texto_contenido_Descripción", config.SCREENSHOT_DIR)
   
def test_clic_en_botones(set_up_ir_a):
    page= set_up_ir_a
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.validar_elemento_visible(lr.labelBoton, "validar_elemento_visible_label_buttons", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.labelBoton, "Buttons", "verificar_texto_contenido_label_buttons", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(lr.botonPrimario, "hacer_click_en_elemento_Primary_Action", config.SCREENSHOT_DIR, "Primary Action")
    fg.hacer_click_en_elemento(lr.botonToggle, "hacer_click_en_elemento_Toggle_Button", config.SCREENSHOT_DIR, "Toggle Button")
    fg.validar_elemento_visible(lr.botonRoleEnDive, "validar_elemento_visible_Div_with_button_role", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.botonRoleEnDive, "Div with button role", "verificar_texto_contenido_Div_with_button_role", config.SCREENSHOT_DIR)
    
def test_completar_seccion_username(set_up_ir_a):
    page= set_up_ir_a
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.validar_elemento_visible(lr.labelFormulario, "validar_elemento_visible_label_fomulario", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.labelFormulario, "Form Elements", "verificar_texto_contenido_label_formaulario", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(lr.labelUsuario, "validar_elemento_visible_label_usuario", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.labelUsuario, "Username:", "verificar_texto_contenido_label_usuario", config.SCREENSHOT_DIR)
    fg.rellenar_campo_de_texto(lr.campoTextoUsername, "prueba_test_user", "rellenar_campo_de_texto_campo_Texto_Username", config.SCREENSHOT_DIR)
    fg.rellenar_campo_de_texto(lr.campoTextoUsername, "", "rellenar_campo_de_texto_campo_Texto_Username", config.SCREENSHOT_DIR, 1)
    fg.rellenar_campo_de_texto(lr.campoTextoUsername, "prueba_test_user2", "rellenar_campo_de_texto_campo_Texto_Username", config.SCREENSHOT_DIR)
    fg.marcar_checkbox(lr.checkTerminosYCondiciones, "marcar_checkbox_Terminos_Y_Condiciones", config.SCREENSHOT_DIR)
    fg.desmarcar_checkbox(lr.checkTerminosYCondiciones, "desmarcar_checkbox_Terminos_Y_Condiciones", config.SCREENSHOT_DIR)
    fg.marcar_checkbox(lr.checkTerminosYCondiciones, "marcar_checkbox_Terminos_Y_Condiciones", config.SCREENSHOT_DIR)
    
def test_sección_nacigation(set_up_ir_a):
    page= set_up_ir_a
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.hacer_click_en_elemento(lr.linkHome, "hacer_click_en_elemento_link_HOME", config.SCREENSHOT_DIR,"Home")
    fg.validar_url_actual(".*/p/playwrightpractice.html")
    fg.hacer_click_en_elemento(lr.linkProductos, "hacer_click_en_elemento_link_PRODUCTS", config.SCREENSHOT_DIR,"Products")
    fg.validar_url_actual(".*/p/playwrightpractice.html")
    fg.hacer_click_en_elemento(lr.linkContactar, "hacer_click_en_elemento_link_CONTACT", config.SCREENSHOT_DIR,"Contact")
    fg.validar_elemento_visible(lr.mensajeAlerta, "validar_elemento_visible_mensaje_alerta", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(lr.mensajeAlerta,"This is an important alert", "verificar_texto_contenido_mensaje_aletar", config.SCREENSHOT_DIR)
    
def test_boton_dinamico(set_up_ir_a):
    page= set_up_ir_a
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
    lr= RoleLocatorsPage(page)
    
    fg.hacer_click_en_elemento(lr.botonDinamicoStart,"hacer_click_en_elemento_boton_dinamico_start", config.SCREENSHOT_DIR, "START")
    fg.hacer_click_en_elemento(lr.botonDinamicoStop,"hacer_click_en_elemento_boton_dinamico_stop", config.SCREENSHOT_DIR, "STOP")