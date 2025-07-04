import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_AlertsAndPopups import AlertsPopupsLocatorsPage
from practice.utils import config

def test_ver_simple_alert(set_up_AlertsAndPopups):
    page= set_up_AlertsAndPopups
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'AlertsPopupsLocatorsPage'
    apl= AlertsPopupsLocatorsPage(page)
    
    #fg.verificar_alerta_visible("verificar_alerta_visible_simple_alert", config.SCREENSHOT_DIR, "I am an alert box!")
    fg.verificar_alerta_simple_con_on(apl.botonSimpleAlert, "I am an alert box!", "verificar_alerta_simple_boton_simple_alert", config.SCREENSHOT_DIR)
    
def test_ver_confirmation_alert(set_up_AlertsAndPopups):
    page= set_up_AlertsAndPopups
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'AlertsPopupsLocatorsPage'
    apl= AlertsPopupsLocatorsPage(page)
    
    fg.validar_elemento_no_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_no_visible_mensaje_Confirmación_De_Accion", config.SCREENSHOT_DIR)
    fg.verificar_confirmacion_on_dialog(apl.botonConfirmationAlert, "Press a button!", "accept", "verificar_confirmación_on_dialog_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, "You pressed OK!", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    fg.verificar_confirmacion_on_dialog(apl.botonConfirmationAlert, "Press a button!", "dismiss", "verificar_confirmación_dismiss_on_dialog_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, "You pressed Cancel!", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    
def test_ver_prompt_alert_con_on(set_up_AlertsAndPopups):
    page= set_up_AlertsAndPopups
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'AlertsPopupsLocatorsPage'
    apl= AlertsPopupsLocatorsPage(page)
    
    texto_a_ingresar = "Playwright User On"
    resultado_mensaje_esperado = f"Hello {texto_a_ingresar}! How are you today?"
    
    fg.verificar_prompt_on_dialog(apl.botonPromptAlert, "Please enter your name:", texto_a_ingresar, "accept", "verificar_prompt_on_dialog_botón_Prompt_Alert", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, resultado_mensaje_esperado, "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    
    fg.verificar_prompt_on_dialog(apl.botonPromptAlert, "Please enter your name:", texto_a_ingresar, "dismiss", "verificar_prompt_on_dialog_botón_Prompt_Alert", config.SCREENSHOT_DIR)
    fg.validar_elemento_visible(apl.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
    fg.verificar_texto_contenido(apl.mensajeConfirmacionDeAccion, "User cancelled the prompt.", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
    
def test_ver_nuevo_tab(set_up_AlertsAndPopups):
    page_original = set_up_AlertsAndPopups # Guardamos la referencia a la página ORIGINAL

    fg = Funciones_Globales(page_original) # fg se inicializa con la página original
    apl = AlertsPopupsLocatorsPage(page_original) # Esta instancia 'apl' también se inicializa con la página original

    # 1. Realizar la acción que abre la nueva pestaña y cambiar el foco
    # Ahora, 'abrir_y_cambiar_a_nueva_pestana' manejará tanto el clic como la espera y el cambio de foco.
    nueva_pestana_page = fg.abrir_y_cambiar_a_nueva_pestana(apl.botonNewTab, "abrir_nueva_pestana", config.SCREENSHOT_DIR)

    # 2. VERIFICAR QUE SE HAYA CAMBIADO A LA NUEVA PESTAÑA
    if nueva_pestana_page:
        # IMPORTANTE: Re-instanciar AlertsPopupsLocatorsPage con la *nueva* página
        # Esto asegura que los locators dentro de apl_nueva_pestana apunten a la nueva pestaña
        apl_nueva_pestana = AlertsPopupsLocatorsPage(nueva_pestana_page)

        # Ahora puedes realizar validaciones en la nueva pestaña
        # fg.page ya apunta a la nueva pestaña gracias a 'abrir_y_cambiar_a_nueva_pestana'
        fg.validar_url_actual("https://www.pavantestingtools.com")
        fg.validar_titulo_de_web("SDET-QA Blog", "validar_titulo_de_web", config.SCREENSHOT_DIR)

        # Usa la nueva instancia de locators para verificar el texto en la nueva pestaña
        fg.verificar_texto_contenido(apl_nueva_pestana.tituloEncabezadoNuevatab1, "SDET-QA Blog", "verificar_texto_contenido_titulo_Encabezado_Nuevatab_1", config.SCREENSHOT_DIR)
        fg.scroll_pagina(0, 200)
        
        # 3. Cerrar la nueva pestaña después de todas las validaciones
        fg.cerrar_pestana_actual("cerrar_pestana_nueva", config.SCREENSHOT_DIR)

        # Opcional: Si necesitas volver a interactuar con la página original específica después de cerrar la nueva pestaña,
        # y cerrar_pestana_actual no te devolvió automáticamente a ella, puedes reasignar fg.page
        fg.page = page_original # Esto podría ser necesario si cerrar_pestana_actual no cambia al foco deseado
        print(f"\n🔄 Foco vuelto a la página original: URL = {fg.page.url}")

    else:
        pytest.fail("No se pudo abrir o cambiar a la nueva pestaña. La prueba falló.")
        
    fg.validar_url_actual(".*/p/playwrightpractice.html")
    fg.validar_titulo_de_web("Automation Testing Practice: PlaywrightPractice", "validar_titulo_de_web", config.SCREENSHOT_DIR)
    fg.esperar_fijo(2)