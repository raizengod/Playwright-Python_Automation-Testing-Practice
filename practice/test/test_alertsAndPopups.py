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

@pytest.mark.xfail(reason="A veces falla cuando se ejecutan todos los archivos de pruebas, pero funciona si se ejecuta unicamente test_alertsAndPopups.py")    
def test_ver_nueva_ventana(set_up_AlertsAndPopups):
    page_original = set_up_AlertsAndPopups # Guardamos la referencia a la página ORIGINAL

    fg = Funciones_Globales(page_original) # fg se inicializa con la página original
    apl_original = AlertsPopupsLocatorsPage(page_original) # Instancia para la página original

    # Definir nombre_base_test y directorio_capturas antes de usarlos
    nombre_base_test = "TestNuevaVentana"

    # --- Inicia el bloque principal de try-except ---
    try:
        # Paso 1: Realizar la acción que abre la(s) nueva(s) ventana(s)
        print("\n--- Ejecutando acción para abrir nueva(s) ventana(s) ---")
        todas_las_nuevas_ventanas = fg.hacer_clic_y_abrir_nueva_ventana(apl_original.botonNuevaVentana, "hacer_clic_y_abrir_nueva_ventana_boton_Nueva_Ventana", config.SCREENSHOT_DIR, nombre_paso="Clic para abrir PopUp Windows")

        # Paso 2: Si se abrieron ventanas, procesarlas
        if todas_las_nuevas_ventanas:
            print(f"\n✅ Se detectaron {len(todas_las_nuevas_ventanas)} nueva(s) ventana(s).")
            
            selenium_page_found = False
            playwright_page_found = False # Reset this flag for the Playwright check

            # Iterar una sola vez para buscar ambas páginas
            for page_obj in todas_las_nuevas_ventanas:
                try:
                    if "selenium.dev" in page_obj.url and not selenium_page_found: # Added flag check
                        print("\n--- Cambiando foco a la ventana de Selenium ---")
                        fg.cambiar_foco_entre_ventanas(nombre_base_test, config.SCREENSHOT_DIR, opcion_ventana=page_obj.url, nombre_paso="Cambio de foco a Ventana de Selenium")
                        apl_selenium_ventana = AlertsPopupsLocatorsPage(fg.page) 
                        fg.page.wait_for_load_state()
                        fg.verificar_texto_contenido(apl_selenium_ventana.tituloNuevaVenatana, "Selenium automates browsers. That's it!", "verificar_texto_contenido_ventana_selenium", config.SCREENSHOT_DIR) 
                        
                        print("✅ Aserciones en la nueva ventana de Selenium pasadas exitosamente.")
                        selenium_page_found = True
                        
                    if "playwright.dev" in page_obj.url and not playwright_page_found: # Added flag check
                        print("\n--- Cambiando foco a la ventana de Playwright ---")
                        fg.cambiar_foco_entre_ventanas("cambiar_foco_entre_ventanas_playwright", config.SCREENSHOT_DIR, opcion_ventana=page_obj.url, nombre_paso="Cambio de foco a Ventana de Playwright")
                                                
                        apl_playwright_ventana = AlertsPopupsLocatorsPage(fg.page)
                        fg.page.wait_for_load_state()

                        fg.verificar_texto_contenido(apl_playwright_ventana.tituloNuevaVenatana2, "Playwright enables reliable end-to-end testing for modern web apps.", "verificar_texto_contenido_ventana_playwright", config.SCREENSHOT_DIR)
                        print("\n✅ Aserciones en la nueva ventana de Playwright pasadas exitosamente.")
                        playwright_page_found = True
                        
                except Exception as e:
                    print(f"\n❌ Error procesando ventana: {page_obj.url if page_obj else 'N/A'}. Detalles: {e}")
                    # Continúa para intentar procesar otras ventanas

            if not selenium_page_found:
                print("\n❌ No se encontró la ventana de Selenium entre las nuevas pestañas.")
                raise ValueError("La ventana de Selenium no se abrió o no se encontró.")
            
            if not playwright_page_found:
                print("\n❌ No se encontró la ventana de Playwright entre las nuevas pestañas.")
                raise ValueError("La ventana de Playwright no se abrió o no se encontró.")

            # Paso 3: Cerrar todas las ventanas nuevas que no son la original
            print("\n--- Cerrando todas las ventanas nuevas (Selenium, Playwright, etc.) ---")
            # Hacer una copia de la lista para evitar problemas al modificarla mientras se itera
            all_current_browser_pages = list(fg.page.context.pages) 
            for page_obj in all_current_browser_pages:
                # Asegurarse de no intentar cerrar la página original si sigue en la lista
                if page_obj != page_original and not page_obj.is_closed(): 
                    try:
                        fg.cerrar_pestana_especifica(page_obj, "cerrar_pestana_especifica", config.SCREENSHOT_DIR, f"Ventana: {page_obj.title() if page_obj.title() else page_obj.url}")
                    except Exception as e:
                        print(f"\n⚠️ Error al intentar cerrar pestaña '{page_obj.title() if page_obj else 'N/A'}': {e}")
            
            # Después de cerrar las pestañas nuevas, reasigna explícitamente fg.page a la página original.
            fg.page = page_original

        else:
            print("\n⚠️ No se detectaron nuevas ventanas. El test continuará en la página original.")
            raise ValueError("El botón 'Nueva Ventana' no abrió ninguna nueva ventana como se esperaba.")

        # Paso 4: Después de cerrar las ventanas nuevas, fg.page debería haber vuelto a la página original.
        print("\n--- Verificando que el foco haya regresado a la página original ---")
        assert fg.page is page_original
        print("\n✅ Foco regresado exitosamente a la página original.")

        fg.validar_url_actual("testautomationpractice.blogspot.com/p/playwrightpractice.html")
        fg.validar_elemento_visible(apl_original.botonConfirmationAlert, "validar_elemento_visible_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
        fg.verificar_confirmacion_on_dialog(apl_original.botonConfirmationAlert, "Press a button!", "accept", "verificar_confirmación_on_dialog_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
        fg.validar_elemento_visible(apl_original.mensajeConfirmacionDeAccion, "validar_elemento_visible_mensaje_Confirmación_DeAccion", config.SCREENSHOT_DIR)
        fg.verificar_texto_contenido(apl_original.mensajeConfirmacionDeAccion, "You pressed OK!", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
        fg.verificar_confirmacion_on_dialog(apl_original.botonConfirmationAlert, "Press a button!", "dismiss", "verificar_confirmación_dismiss_on_dialog_boton_Confirmation_Alert", config.SCREENSHOT_DIR)
        fg.verificar_texto_contenido(apl_original.mensajeConfirmacionDeAccion, "You pressed Cancel!", "verificar_texto_contenido_mensaje_Confirmacion_De_Accion", config.SCREENSHOT_DIR)
        

        print("\n---------- Fin del escenario de prueba 'test_ver_nueva_ventana' ----------")

    except Exception as e:
        print(f"\n❌ El test falló: {e}")
        # Solo toma la captura si fg.page sigue siendo una página válida.
        # En este punto, fg.page ya debería ser page_original, que siempre está abierta
        # a menos que haya un error más grave.
        if fg.page and not fg.page.is_closed():
            fg.tomar_captura(f"{nombre_base_test}_FALLO_FINAL", config.SCREENSHOT_DIR)
        else:
            print("⚠️ No se pudo tomar la captura de pantalla final porque la página de referencia está cerrada o no válida.")
        raise # Re-lanzar la excepción para que el framework de testing la capture