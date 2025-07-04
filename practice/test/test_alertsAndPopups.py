import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_AlertsAndPopups import AlertsPopupsLocatorsPage
from practice.utils import config

def test_ver_simple_alert(set_up_byText):
    page= set_up_byText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    apl= AlertsPopupsLocatorsPage(page)
    
    #fg.verificar_alerta_visible("verificar_alerta_visible_simple_alert", config.SCREENSHOT_DIR, "I am an alert box!")
    fg.verificar_alerta_simple_con_on(apl.botonSimpleAlert, "I am an alert box!", "verificar_alerta_simple_boton_simple_alert", config.SCREENSHOT_DIR)
    
def test_ver_confirmation_alert(set_up_byText):
    page= set_up_byText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    apl= AlertsPopupsLocatorsPage(page)
    
    fg.validar_elemento_no_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_no_visible_mensaje_Confirmación_De_Accion", config.SCREENSHOT_DIR)
    fg.verificar_confirmacion_on_dialog(apl.botonConfirmationAlert, "Press a button!", "accept", "verificar_confirmación_on_dialog_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, "You pressed OK!", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    fg.verificar_confirmacion_on_dialog(apl.botonConfirmationAlert, "Press a button!", "dismiss", "verificar_confirmación_dismiss_on_dialog_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, "You pressed Cancel!", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    
def test_ver_prompt_alert_con_on(set_up_byText):
    page= set_up_byText
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    apl= AlertsPopupsLocatorsPage(page)
    
    texto_a_ingresar = "Playwright User On"
    resultado_mensaje_esperado = f"Hello {texto_a_ingresar}! How are you today?"
    
    fg.verificar_prompt_on_dialog(apl.botonPromptAlert, "Please enter your name:", texto_a_ingresar, "accept", "verificar_prompt_on_dialog_botón_Prompt_Alert", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, resultado_mensaje_esperado, "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    
    fg.verificar_prompt_on_dialog(apl.botonPromptAlert, "Please enter your name:", texto_a_ingresar, "dismiss", "verificar_prompt_on_dialog_botón_Prompt_Alert", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, "User cancelled the prompt.", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)