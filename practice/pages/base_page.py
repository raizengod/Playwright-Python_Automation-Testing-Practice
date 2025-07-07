import re
import time
import time
import random
from playwright.sync_api import Page, expect, Error , TimeoutError, sync_playwright, Response, Dialog 
from datetime import datetime
import os
from typing import Union, List, Dict

class Funciones_Globales:
    
    #1- Creamos una función incial 'Constructor'-----ES IMPORTANTE TENER ESTE INICIADOR-----
    def __init__(self, page):
        self.page = page
        self._alerta_detectada = False
        self._alerta_mensaje_capturado = ""
        self._alerta_tipo_capturado = ""
        self._alerta_input_capturado = ""
        self._dialog_handler_registered = False # <--- ¡Esta línea es crucial!

        # --- Nuevas variables para el manejo de pestañas (popups) ---
        self._popup_detectado = False
        self._popup_page = None # Para almacenar el objeto Page de la nueva pestaña
        self._popup_url_capturado = ""
        self._popup_title_capturado = ""  
        
        # Nueva lista para almacenar todas las nuevas páginas abiertas durante una interacción
        self._all_new_pages_opened_by_click: List[Page] = []
        
        # Registramos el manejador de eventos para nuevas páginas
        # Limpiamos la lista al registrar para evitar resagos de pruebas anteriores
        self.page.context.on("page", self._on_new_page)
        # Esto es importante: Si se va a usar _all_new_pages_opened_by_click,
        # necesitamos una forma de reiniciarla o asegurarnos de que solo contenga
        # las páginas relevantes para la acción actual.
        # Una estrategia es limpiar la lista antes de la acción que abre la nueva ventana,
        # y luego recopilar las páginas.
        
    #2- Función para generar el nombre de archivo con marca de tiempo
    def _generar_nombre_archivo_con_timestamp(self, prefijo):
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3] # Quita los últimos 3 dígitos para milisegundos más precisos
        return f"{timestamp}_{prefijo}"
    
    #3- Función para tomar captura de pantalla
    def tomar_captura(self, nombre_base, directorio):
        if not os.path.exists(directorio):
            os.makedirs(directorio) # Crea el directorio si no existe
        nombre_archivo = self._generar_nombre_archivo_con_timestamp(nombre_base)
        ruta_completa = os.path.join(directorio, f"{nombre_archivo}.jpg")
        self.page.screenshot(path=ruta_completa)
        print(f"📸 Captura guardada en: {ruta_completa}") # Para ver dónde se guardó
        
    #4- unción basica para tiempo de espera que espera recibir el parametro tiempo
    #En caso de no pasar el tiempo por parametro, el mismo tendra un valor de medio segundo
    def esperar_fijo(self, tiempo=0.5):
        time.sleep(tiempo)
        
    #5- unción para indicar el tiempo que se tardará en hacer el scroll
    def scroll_pagina(self, horz, vert, tiempo=0.5): 
        #Usamos 'self' ya que lo tenemos inicializada en __Init__ y para que la palabra page de la función funcione es necesaria
        self.page.mouse.wheel(horz, vert)
        time.sleep(tiempo)
        
    #6- Función para validar que un elemento es visible
    def validar_elemento_visible(self, selector, nombre_base, directorio, tiempo= 0.5, resaltar: bool = True) -> bool:
        print(f"\nValidando visibilidad del elemento con selector: '{selector}'")

        try:
            # Espera explícita para que el elemento sea visible.
            expect(selector).to_be_visible() # ¡Cambio clave aquí!
            
            if resaltar:
                selector.highlight() # Resaltar el elemento visible
                
            self.tomar_captura(f"{nombre_base}_visible", directorio)
            print(f"\n  --> ÉXITO: El elemento '{selector}' es visible en la página.")
            time.sleep(tiempo)
            
            return True

        except TimeoutError as e:
            error_msg = (
                f"\nFALLO (Timeout): El elemento con selector '{selector}' NO es visible "
                f"\ndespués de {tiempo} segundos.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            # Toma una captura de pantalla del estado actual de la página cuando el elemento no es visible
            self.tomar_captura(f"{nombre_base}_NO_visible_timeout", directorio)
            # En este caso, no relanzamos la excepción porque la función está diseñada para retornar False
            # Si el llamador necesita que la prueba falle, debe verificar el valor de retorno.
            return False

        except Error as e: 
            error_msg = (
                f"\nFALLO (Playwright): Error de Playwright al verificar la visibilidad de '{selector}'.\n"
                f"\nPosibles causas: Selector inválido, elemento desprendido del DOM.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            # Aquí sí relanzamos, ya que es un error inesperado de Playwright, no solo que no sea visible.
            raise 
        
        except Exception as e:
            error_msg = (
                f"\nFALLO (Inesperado): Ocurrió un error inesperado al validar la visibilidad de '{selector}'.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise

        finally:
            # Eliminamos el time.sleep() o self.esperar_fijo() final, ya que no es necesario para una validación de visibilidad.
            # El timeout de expect() ya maneja la espera.
            pass
    
    #7- Función para validar que un elemento NO es visible
    def validar_elemento_no_visible(self, selector, nombre_base, directorio, tiempo= 0.5):
        print(f"\nValidando que el elemento con selector '{selector}' NO es visible.")
        try:
            # Usamos to_be_hidden() con un timeout explícito para mayor robustez.
            # Playwright espera automáticamente por el elemento sin necesidad de time.sleep()
            expect(selector).to_be_hidden()
            print(f"\nEl elemento con selector '{selector}' NO es visible.")
            self.tomar_captura(f"{nombre_base}_fallo_no_visible", directorio)
            
            time.sleep(tiempo)
            
        except AssertionError as e:
            print(f"\nError: El elemento con selector '{selector}' aún es visible o no se ocultó a tiempo.")
            # Tomamos la captura solo si la aserción falla para depuración.
            self.tomar_captura(f"{nombre_base}_fallo_no_visible", directorio)
            raise e # Re-lanza la excepción para que el test falle.
        
        finally:
            # Puedes optar por tomar una captura de pantalla exitosa si lo deseas,
            # pero generalmente se toman en caso de fallo para depuración.
            # self.tomar_captura(nombre_base=f"{nombre_base}_exito_no_visible", directorio=directorio)
            pass
        
    #8- Función para verificar que un elemento (o elementos) localizado en una página web contiene un texto específico    
    def verificar_texto_contenido(self, selector, texto_esperado, nombre_base, directorio, tiempo= 0.5):
        try:
            # Esperar visibilidad y capturar antes de la verificación del texto
            # Usamos expect().to_be_visible() con un timeout específico.
            # El timeout de expect es más robusto que time.sleep().
            expect(selector).to_be_visible()
            print(f"\n✅ Elemento con selector '{selector}' es visible.")

            # Opcional: Resaltar el elemento solo si es necesario para depuración.
            # En un entorno de CI/CD, no siempre es práctico o visible.
            selector.highlight()

            self.tomar_captura(f"{nombre_base}_antes_verificacion", directorio)

            # Verificar que el elemento contenga el texto esperado
            # Playwright ya espera implícitamente a que el texto aparezca.
            # Usamos to_contain_text() para la verificación, también con timeout.
            expect(selector).to_contain_text(texto_esperado)
            print(f"\n✅ Elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # 4. Capturar después de la verificación exitosa
            self.tomar_captura(nombre_base=f"{nombre_base}_despues_verificacion", directorio=directorio)
            
            time.sleep(tiempo)

        except Exception as e:
            # Manejo de errores para capturar cualquier fallo durante la operación
            print(f"\n❌ Error al verificar el texto para el selector '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error", directorio)
            raise  # Re-lanzar la excepción para que el test falle
        
    #9- Función para rellenar campo de texto y hacer capture la imagen
    def rellenar_campo_de_texto(self, selector, texto, nombre_base, directorio, tiempo=0.5):
        try:
            # Resaltar el campo en azul para depuración visual
            selector.highlight()
            self.tomar_captura("Antes_de_rellenar", directorio)

            # Rellenar el campo de texto.
            # Playwright espera automáticamente a que el campo sea editable.
            selector.fill(texto) # Espera hasta 15 segundos para la operación de llenado
            print(f"\n  --> Campo '{selector}' rellenado con éxito con el texto: '{texto}'.")

            self.tomar_captura(nombre_base, directorio)

        except TimeoutError as e:
            # Captura errores cuando una aserción o una acción excede su tiempo de espera.
            error_msg = (
                f"\nERROR (Timeout): El tiempo de espera se agotó al interactuar con '{selector}'.\n"
                f"\nPosibles causas: El elemento no apareció, no fue visible/habilitado/editable a tiempo.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura("error_timeout", nombre_base, directorio)
            # Re-lanza la excepción para que el test principal falle y marque el paso como erróneo.
            raise Error(error_msg) from e

        except Error as e:
            # Captura otras excepciones generales de Playwright (ej., elemento desprendido, selector incorrecto).
            error_msg = (
                f"\nERROR (Playwright): Ocurrió un problema de Playwright al interactuar con '{selector}'.\n"
                f"\nVerifica la validez del selector y el estado del elemento en el DOM.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura("error_playwright", nombre_base, directorio)
            raise # Re-lanza la excepción

        except Exception as e:
            # Captura cualquier otra excepción inesperada que no sea de Playwright.
            error_msg = (
                f"\nERROR (Inesperado): Se produjo un error desconocido al interactuar con '{selector}'.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura("error_inesperado", nombre_base, directorio)
            raise

        finally:
            # Este bloque se ejecuta siempre, independientemente de si hubo un error o no.
            if tiempo > 0:
                print(f"\n  --> Realizando espera fija de {tiempo} segundos.")
                time.sleep(tiempo)
                
    #10- Función para rellenar campo numérico y hacer capture la imagen
    def rellenar_campo_numerico_positivo(self, selector, valor_numerico: int | float, nombre_base, directorio, tiempo= 0.5):
        print(f"\nIniciando intento de rellenar campo con selector '{selector}' con el valor numérico POSITIVO: '{valor_numerico}'")

        # --- VALIDACIÓN DE NÚMERO POSITIVO ---
        if not isinstance(valor_numerico, (int, float)):
            error_msg = f"\nERROR: El valor proporcionado '{valor_numerico}' no es un tipo numérico (int o float)."
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_valor_no_numerico", directorio)
            raise ValueError(error_msg)

        if valor_numerico < 0:
            error_msg = f"\nERROR: El valor numérico '{valor_numerico}' no es positivo. Se esperaba un número mayor o igual a cero."
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_valor_negativo", directorio)
            raise ValueError(error_msg)

        # Convertir el valor numérico a cadena para el método fill()
        valor_a_rellenar_str = str(valor_numerico)
        # --- FIN DE VALIDACIÓN ---

        try:
            # Resaltar el campo en azul para depuración visual
            selector.highlight()
            # Se usa f-string para incluir nombre_base en el nombre de la captura
            self.tomar_captura(f"{nombre_base}_antes_de_rellenar", directorio) 

            # Rellenar el campo de texto.
            selector.fill(valor_a_rellenar_str)
            print(f"\n  --> Campo '{selector}' rellenado con éxito con el valor: '{valor_a_rellenar_str}'.")

            self.tomar_captura(f"{nombre_base}_despues_de_rellenar", directorio)

        except TimeoutError as e:
            error_msg = (
                f"\nERROR (Timeout): El tiempo de espera se agotó al interactuar con '{selector}'.\n"
                f"\nPosibles causas: El elemento no apareció, no fue visible/habilitado/editable a tiempo.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_timeout", directorio)
            raise Error(error_msg) from e

        except Error as e:
            error_msg = (
                f"\nERROR (Playwright): Ocurrió un problema de Playwright al interactuar con '{selector}'.\n"
                f"\nVerifica la validez del selector y el estado del elemento en el DOM.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise # Re-lanza la excepción

        except TypeError as e:
            error_msg = (
                f"\nERROR (TypeError): El selector proporcionado no es un objeto Locator válido.\n"
                f"\nAsegúrate de pasar un objeto locator o una cadena para que sea convertido a locator.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_tipo_selector", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\nERROR (Inesperado): Se produjo un error desconocido al interactuar con '{selector}'.\n"
                f"\nDetalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise

        finally:
            if tiempo > 0:
                print(f"\n  --> Realizando espera fija de {tiempo} segundos.")
                time.sleep(tiempo)
                
    #11- Función para validar titulo de una página
    def validar_titulo_de_web(self, titulo_esperado, nombre_base, directorio, tiempo= 0.5):
        try:
            # Usa el 'expect' de Playwright con un timeout para una espera robusta
            expect(self.page).to_have_title(titulo_esperado)
            print(f"\n✅ Título de la página '{titulo_esperado}' validado exitosamente.")
           
            self.tomar_captura(nombre_base, directorio)
            
            time.sleep(tiempo)

        except Exception as e:
            print(f"\n❌ Error al validar el título o tomar la captura: {e}")
            # Opcionalmente, puedes relanzar la excepción si quieres que la prueba falle
            raise
    
    #12- Función para validar UR    
    def validar_url_actual(self, patron_url, tiempo= 1):
        try:
            # Usa 'expect' de Playwright con un timeout para una espera robusta.
            # to_have_url ya espera automáticamente y reintenta.
            expect(self.page).to_have_url(re.compile(patron_url))
            print(f"\n✅ URL '{self.page.url}' validada exitosamente con el patrón: '{patron_url}'.")
            time.sleep(tiempo)
            
        except Exception as e:
            print(f"\n❌ Error al validar la URL. URL actual: '{self.page.url}', Patrón esperado: '{patron_url}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle si la URL no coincide
            raise
        
    #13- Función para hacer click
    def hacer_click_en_elemento(self, selector, nombre_base, directorio, texto_esperado= None, tiempo= 1):
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validar texto solo si se proporciona
            if texto_esperado:
                expect(selector).to_have_text(texto_esperado)
                print(f"\n✅ El elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # Hacer click en el elemento
            selector.click()
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            print(f"\n✅ Click realizado exitosamente en el elemento con selector '{selector}'.")
            
            time.sleep(tiempo)

        except Exception as e:
            print(f"\n❌ Error al intentar hacer click en el elemento con selector '{selector}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle
            raise

    #14- Función para hacer doble click
    def hacer_doble_click_en_elemento(self, selector, nombre_base, directorio, texto_esperado= None, tiempo= 1):
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validar texto solo si se proporciona
            if texto_esperado:
                expect(selector).to_have_text(texto_esperado)
                print(f"\n✅ El elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # Realizar la acción de DOBLE CLICK
            selector.dblclick()
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            print(f"\n✅ Doble click realizado exitosamente en el elemento con selector '{selector}'.")
            
            time.sleep(tiempo)

        except Exception as e:
            print(f"\n❌ Error al intentar hacer click en el elemento con selector '{selector}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle
            raise
    
    #14- Función para hacer hover over
    def hacer_hover_en_elemento(self, selector, nombre_base, directorio, texto_esperado= None, tiempo= 1):
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validaciones robustas con Playwright's 'expect'
            # Playwright ya auto-espera por estas condiciones antes del hover.
            #expect(selector).to_be_enabled()

            # Validar texto solo si se proporciona (útil para asegurar que se hace hover sobre el elemento correcto)
            if texto_esperado:
                expect(selector).to_have_text(texto_esperado)
                print(f"\n✅ El elemento con selector '{selector}' contiene el texto esperado: '{texto_esperado}'.")

            # Realizar la acción de HOVER OVER
            selector.hover() # El hover también puede tener un timeout
            print(f"\n✅ Hover realizado exitosamente en el elemento con selector '{selector}'.")

            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            time.sleep(tiempo)

        except Exception as e:
            print(f"\n❌ Error al intentar hacer hover en el elemento con selector '{selector}'. Error: {e}")
            # Es buena práctica relanzar la excepción para que la prueba falle
            raise
        
    #15- Función para verificar si un elemento está habilitado o deshabilitado
    def verificar_elemento_habilitado(self, selector, nombre_base, directorio, tiempo= 1) -> bool:
        try:
            # Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # Validar si el elemento está habilitado usando expect de Playwright
            # Playwright espera automáticamente hasta que el elemento cumpla la condición
            expect(selector).to_be_enabled()
            print(f"\n✅ El elemento con selector '{selector}' está habilitado.")
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            time.sleep(tiempo)
            return True
        
        except Exception as e:
            print(f"\n❌ Error: El elemento con selector '{selector}' NO está habilitado o no se encontró dentro del tiempo esperado. Error: {e}")
            self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
            return False
        
    #16- Crear función para hacer click fuera de un campo
    def mouse_mueve_y_hace_clic_xy(self, x, y, nombre_base, directorio, tiempo= 0.5):
        self.page.mouse.click(x, y)
        self.tomar_captura(nombre_base, directorio) # Llama a la función de captura
        time.sleep(tiempo)
        
    #17 Función optimizada para marcar (o verificar que está marcado) un checkbox.
    def marcar_checkbox(self, selector, nombre_base, directorio, tiempo= 0.5):
        print(f"\nIntentando marcar/verificar el checkbox con selector: '{selector}'")

        try:
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_de_marcar", directorio)

            # Marcar el checkbox si no está ya marcado
            # Playwright's check() método espera automáticamente a que el elemento sea visible,
            # habilitado y cliqueable.
            # No se necesita un click explícito si el objetivo es "marcar" el checkbox.
            # check() solo marcará si no está ya marcado, y desmarcará con uncheck().
            selector.check() 
            print(f"\n✅ Checkbox '{selector}' marcado exitosamente (o ya lo estaba).")

            # Verificar que el checkbox está marcado después de la acción
            expect(selector).to_be_checked()
            print(f"\n✅ Checkbox '{selector}' verificado como marcado.")
            self.tomar_captura(f"{nombre_base}_despues_de_marcar_exito", directorio)

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): El checkbox con selector '{selector}' no pudo ser marcado "
                f"o verificado dentro de {tiempo} segundos.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_fallo_timeout", directorio)
            raise AssertionError(f"Checkbox no marcado/verificado: {selector}") from e

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright Error): Problema al interactuar con el checkbox '{selector}'.\n"
                f"Posibles causas: Selector inválido, elemento no interactuable.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_fallo_playwright_error", directorio)
            raise AssertionError(f"Error de Playwright con checkbox: {selector}") from e

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al manejar el checkbox '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_fallo_inesperado", directorio)
            raise AssertionError(f"Error inesperado con checkbox: {selector}") from e
        
    #18- Función optimizada para desmarcar un checkbox.
    def desmarcar_checkbox(self, selector, nombre_base, directorio, tiempo= 0.5):
        print(f"\nIntentando desmarcar/verificar el checkbox con selector: '{selector}'")

        try:
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_de_desmarcar", directorio)

            # Desmarcar el checkbox si está marcado
            # Playwright's uncheck() espera automáticamente a que el elemento sea visible,
            # habilitado y cliqueable.
            if selector.is_checked():
                print(f"\nEl checkbox '{selector}' está marcado. Procediendo a desmarcar...")
                selector.uncheck()
                print(f"\n✅ Checkbox '{selector}' desmarcado exitosamente.")
            else:
                print(f"\nEl checkbox '{selector}' ya está desmarcado. No se necesita acción.")

            # Verificar que el checkbox está desmarcado después de la acción
            expect(selector).not_to_be_checked()
            print(f"\n✅ Checkbox '{selector}' verificado como desmarcado.")
            self.tomar_captura(f"{nombre_base}_despues_de_desmarcar_exito", directorio)

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): El checkbox con selector '{selector}' no pudo ser desmarcado "
                f"o verificado dentro de {tiempo} segundos.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_fallo_timeout", directorio)
            raise AssertionError(f"Checkbox no desmarcado/verificado (Timeout): {selector}") from e

        except Error as e: # Playwright-specific errors
            error_msg = (
                f"\n❌ FALLO (Playwright Error): Problema al interactuar con el checkbox '{selector}'.\n"
                f"Posibles causas: Selector inválido, elemento no interactuable, DOM no estable.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_fallo_playwright_error", directorio)
            raise AssertionError(f"Error de Playwright con checkbox: {selector}") from e

        except Exception as e: # Catch-all for any other unexpected errors
            error_msg = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al manejar el checkbox '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_fallo_inesperado", directorio)
            raise AssertionError(f"\nError inesperado con checkbox: {selector}") from e

    #19- Función optimizada para verificar el valor de un campo de texto
    def verificar_valor_campo(self, selector, valor_esperado, nombre_base, directorio, tiempo=1):
        # Esta función se usaría específicamente para campos de entrada (input, textarea, select)
        try:
            expect(selector).to_be_visible()
            print(f"\n✅ Campo con selector '{selector}' es visible.")
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_verificacion", directorio)
            expect(selector).to_have_value(valor_esperado) # <<--- USAMOS TO_HAVE_VALUE AQUÍ
            print(f"✅ Campo '{selector}' tiene el valor esperado: '{valor_esperado}'")
        except AssertionError as e:
            print(f"\n❌ Falló la verificación de valor para '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_fallo_verificacion", directorio)
            raise
        except Exception as e:
            print(f"\n❌ Error inesperado al verificar valor para '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #20- Función optimizada para verificar el valor de un campo numérico int
    def verificar_valor_campo_numerico_int(self, selector, valor_esperado: int, nombre_base, directorio, tiempo=1):
        # Esta función se usaría específicamente para campos de entrada (input, textarea, select)
        try:
            expect(selector).to_be_visible(timeout=tiempo * 1000)
            print(f"\n✅ Campo con selector '{selector}' es visible.")
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_verificacion", directorio)

            # --- AJUSTE CLAVE AQUÍ: Lógica de conversión y comparación ---
            try:               
                # Intentar convertir el valor actual del campo a numérico
                actual_numeric = int(selector.input_value())

                # Comparar los valores numéricamente
                assert actual_numeric == valor_esperado, \
                    f"\nValor numérico esperado '{valor_esperado}' no coincide con el valor actual '{actual_numeric}'"
                
                print(f"\n✅ Campo '{selector}' tiene el valor numérico esperado: '{valor_esperado}'")

            except ValueError:
                # Si la conversión a numérico falla (es decir, no es un número),
                # entonces tratarlo como un string normal y usar to_have_value
                expect(selector).to_have_value(str(valor_esperado), tiempo)
                print(f"\n✅ Campo '{selector}' tiene el valor de texto esperado: '{valor_esperado}'")
            # --- FIN AJUSTE CLAVE ---

        except AssertionError as e:
            print(f"\n❌ Falló la verificación de valor para '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_fallo_verificacion", directorio)
            raise
        except Exception as e:
            print(f"\n❌ Error inesperado al verificar valor para '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise

    #21- Función optimizada para verificar el valor de un campo numérico float
    def verificar_valor_campo_numerico_int(self, selector, valor_esperado: float, nombre_base, directorio, tiempo=1):
        # Esta función se usaría específicamente para campos de entrada (input, textarea, select)
        try:
            expect(selector).to_be_visible(timeout=tiempo * 1000)
            print(f"\n✅ Campo con selector '{selector}' es visible.")
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_verificacion", directorio)

            # --- AJUSTE CLAVE AQUÍ: Lógica de conversión y comparación ---
            try:               
                # Intentar convertir el valor actual del campo a numérico
                actual_numeric = float(selector.input_value())

                # Comparar los valores numéricamente
                assert actual_numeric == valor_esperado, \
                    f"\nValor numérico esperado '{valor_esperado}' no coincide con el valor actual '{actual_numeric}'"
                
                print(f"\n✅ Campo '{selector}' tiene el valor numérico esperado: '{valor_esperado}'")

            except ValueError:
                # Si la conversión a numérico falla (es decir, no es un número),
                # entonces tratarlo como un string normal y usar to_have_value
                expect(selector).to_have_value(str(valor_esperado), tiempo)
                print(f"\n✅ Campo '{selector}' tiene el valor de texto esperado: '{valor_esperado}'")
            # --- FIN AJUSTE CLAVE ---

        except AssertionError as e:
            print(f"\n❌ Falló la verificación de valor para '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_fallo_verificacion", directorio)
            raise
        except Exception as e:
            print(f"\n❌ Error inesperado al verificar valor para '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise

    #22- Función para perifica que el atributo 'alt' de una imagen sea el texto esperado y esté correctamente asociado.
    def verificar_alt_imagen(self, selector, texto_alt_esperado, nombre_base, directorio, tiempo= 1) -> bool:
        try:
            print(f"\n⚙️ Verificando el texto 'alt' para la imagen con selector: '{selector}'")
            # Resaltar el elemento para depuración visual
            selector.highlight()

            # Esperar a que la imagen sea visible
            expect(selector).to_be_visible()
            print(f"\n✅ La imagen con selector '{selector}' es visible.")

            # Obtener el atributo 'alt' de la imagen
            alt_text_actual = selector.get_attribute("alt")

            # Validar que el atributo 'alt' no sea None y coincida con el texto esperado
            if alt_text_actual == texto_alt_esperado:
                print(f"\n✅ El texto 'alt' de la imagen es '{alt_text_actual}' y coincide con el esperado ('{texto_alt_esperado}').")
                self.tomar_captura(f"{nombre_base}_alt_ok", directorio)
                time.sleep(tiempo)
                return True
            else:
                print(f"\n❌ Error: El texto 'alt' actual es '{alt_text_actual}', pero se esperaba '{texto_alt_esperado}'.")
                self.tomar_captura(f"{nombre_base}_alt_error", directorio)
                return False

        except Exception as e:
            print(f"\n❌ Error al verificar el texto 'alt' de la imagen con selector '{selector}'. Error: {e}")
            self.tomar_captura(f"{nombre_base}_excepcion", directorio)
            return False
        
    #23- Función para Verifica que una imagen se cargue exitosamente (sin enlaces rotos).
    def verificar_carga_exitosa_imagen(self, selector, nombre_base, directorio, tiempo_espera_red= 10, tiempo= 1) -> bool:
        image_url = None
        try:
            print(f"\n⚙️ Verificando carga exitosa para la imagen con selector: '{selector}'")

            # 1. Resaltar el elemento (útil para depuración visual)
            selector.highlight()

            # 2. Esperar a que la imagen sea visible en el DOM
            expect(selector).to_be_visible(timeout=tiempo_espera_red * 1000)
            print(f"✅ La imagen con selector '{selector}' es visible.")

            # 3. Obtener la URL de la imagen
            image_url = selector.get_attribute("src")
            if not image_url:
                print(f"\n❌ Error: El atributo 'src' de la imagen con selector '{selector}' está vacío o no existe.")
                self.tomar_captura(f"{nombre_base}_src_vacio", directorio)
                return False

            print(f"\n🔍 URL de la imagen a verificar: {image_url}")

            # 4. Monitorear la carga de la imagen en la red
            # Usamos page.wait_for_response para esperar la respuesta HTTP de la imagen
            # Esto es más robusto que solo verificar la visibilidad, ya que asegura que el recurso fue descargado
            response: Response = self.page.wait_for_response(
                lambda response: response.url == image_url and response.request.resource_type == "image",
                timeout=tiempo_espera_red * 1000 # Playwright espera milisegundos
            )

            # 5. Verificar el código de estado de la respuesta HTTP
            if 200 <= response.status <= 299:
                print(f"\n✅ La imagen con URL '{image_url}' cargó exitosamente con estado {response.status}.")
                self.tomar_captura(f"{nombre_base}_carga_ok", directorio)
                time.sleep(tiempo)
                return True
            else:
                print(f"\n❌ Error: La imagen con URL '{image_url}' cargó con un estado de error: {response.status}.")
                self.tomar_captura(f"{nombre_base}_carga_fallida_status_{response.status}", directorio)
                return False

        except TimeoutError:
            print(f"\n❌ Error: La imagen con selector '{selector}' no se hizo visible a tiempo o su recurso '{image_url}' no respondió dentro de {tiempo_espera_red} segundos.")
            self.tomar_captura(f"{nombre_base}_timeout", directorio)
            return False
        except Exception as e:
            print(f"\n❌ Error inesperado al verificar la carga de la imagen con selector '{selector}'. Error: {e}")
            self.tomar_captura(f"{nombre_base}_excepcion", directorio)
            return False

    #24- Función para cargar archivo(s)
    def cargar_archivo(self, selector, nombre_base, directorio, base_dir, file_names: str | list[str], tiempo= 3):
        # Normalizar file_names a una lista si se pasa una sola cadena
        if isinstance(file_names, str):
            file_names = [file_names]

        # Construir las rutas completas de los archivos
        full_file_paths = []
        for name in file_names:
            full_path = os.path.join(base_dir, name)
            full_file_paths.append(full_path)

        # Verificar que todos los archivos existan antes de intentar la carga
        for path in full_file_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"\n❌ El archivo no existe en la ruta especificada: {path}")

        try:

            # Usar expect para asegurar que el elemento esté visible y habilitado
            expect(selector).to_be_visible()
            expect(selector).to_be_enabled()

            # Opcional: Resaltar el elemento para depuración (desactivar en producción si no es necesario)
            selector.highlight()

            # Usar set_input_files para cargar el archivo(s)
            # Playwright espera una lista de rutas completas
            selector.set_input_files(full_file_paths)

            # Construir mensaje de éxito basado en si es uno o varios archivos
            if len(file_names) == 1:
                print(f"\n✅ Archivo '{file_names[0]}' cargado exitosamente desde '{base_dir}' en el selector '{selector}'.")
                self.tomar_captura(f"{nombre_base}_archivos_cargados", directorio)
            else:
                print(f"\n✅ Archivos {file_names} cargados exitosamente desde '{base_dir}' en el selector '{selector}'.")
                self.tomar_captura(f"{nombre_base}_archivo_cargado", directorio)
            
            time.sleep(tiempo)

        except Exception as e:
            # Capturar los nombres de archivo para el mensaje de error
            error_files_info = file_names[0] if isinstance(file_names, list) and len(file_names) == 1 else file_names
            self.tomar_captura(f"{nombre_base}_Error_cargar_de_archivo", directorio)
            print(f"\n❌ Error al cargar el archivo(s) '{error_files_info}' desde '{base_dir}' en el selector '{selector}': {e}")
            raise # Re-lanza la excepción para que el test falle si ocurre un error
        
    #25- Función para remover carga de archivo(s)
    def remover_carga_de_archivo(self, selector, nombre_base, directorio, tiempo= 3):
        try:
            # Usar expect para asegurar que el elemento esté visible y habilitado
            expect(selector).to_be_visible()
            expect(selector).to_be_enabled()

            # Resaltar el elemento para depuración (desactivar en producción si no es necesario)
            selector.highlight()

            # Usar set_input_files con una lista vacía para remover el archivo
            selector.set_input_files([])

            print(f"\n✅ Carga de archivo removida exitosamente para el selector '{selector}'.")
            self.tomar_captura(f"{nombre_base}_remoción_completa", directorio)
            
            time.sleep(tiempo)

        except Exception as e:
            print(f"\n❌ Error al remover la carga del archivo para el selector '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error_en_remoción_completa", directorio)
            raise # Re-lanza la excepción para que el test falle si ocurre un error
        
    #26- Función para contar filas y columnas
    def obtener_dimensiones_tabla(self, selector, nombre_base, directorio, tiempo= 1) -> tuple[int, int]:
        print(f"\nObteniendo dimensiones de la tabla con selector: '{selector.get_attribute('id') or selector.text_content() if selector.text_content() else 'Tabla sin texto visible'}'")

        try:
            selector.highlight()

            # Contar el número de filas.
            # Excluye la fila de encabezado si hay una, contando solo las filas con celdas de datos (td).
            # O, si quieres contar todas las TRs (encabezado + datos):
            # num_filas = table_selector.locator("tr").count()
            # Una forma más precisa de contar las filas de datos:
            filas_datos = selector.locator("tbody tr")
            num_filas = filas_datos.count()

            # Contar el número de columnas.
            # Se hace tomando el número de celdas de encabezado (<th>) o las celdas de la primera fila de datos (<td>).
            num_columnas = 0
            headers = selector.locator("th")
            if headers.count() > 0:
                num_columnas = headers.count()
            else:
                # Si no hay thead/th, intenta contar td's de la primera fila de datos
                first_row_tds = selector.locator("tr").first.locator("td")
                if first_row_tds.count() > 0:
                    num_columnas = first_row_tds.count()
                else:
                    print("\n  --> ADVERTENCIA: No se pudieron encontrar encabezados (th) ni celdas (td) en la primera fila para contar columnas.")
                    # Si no hay th ni td en la primera fila, la tabla podría estar vacía o mal formada.
                    # En este caso, num_columnas seguirá siendo 0.

            self.tomar_captura(f"{nombre_base}_dimensiones_obtenidas", directorio)
            print(f"\n✅  --> ÉXITO: Dimensiones de la tabla obtenidas.")
            print(f"  --> Filas encontradas: {num_filas}")
            print(f"  --> Columnas encontradas: {num_columnas}")
            time.sleep(tiempo)

            return (num_filas, num_columnas)

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo obtener las dimensiones de la tabla con selector '{selector}'.\n"
                f"La tabla o sus elementos internos no estuvieron disponibles a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_dimensiones_timeout", directorio)
            return (-1, -1)

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al intentar obtener las dimensiones de la tabla con selector '{selector}'.\n"
                f"Posibles causas: Selector de tabla inválido, estructura de tabla inesperada.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_dimensiones_error_playwright", directorio)
            raise # Relanzar porque es un error de Playwright

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al obtener las dimensiones de la tabla con selector '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_dimensiones_error_inesperado", directorio)
            raise # Relanzar por ser un error inesperado

    #27- Función para buscar datos parcial e imprimir la fila
    def busqueda_coincidencia_e_imprimir_fila(self, table_selector, texto_buscado, nombre_base, directorio, tiempo= 1) -> bool:
        print(f"\nBuscando coincidencia parcial del texto '{texto_buscado}' en la tabla con selector: '{table_selector}'")
        
        try:
            # Obtener todas las filas de datos (tr) dentro del tbody de la tabla.
            # Usamos "tbody tr" para excluir explícitamente el thead si existe.
            filas = table_selector.locator("tbody tr")
            num_filas = filas.count()

            if num_filas == 0:
                print(f"\n  --> ADVERTENCIA: La tabla con selector '{table_selector}' no contiene filas de datos para buscar.")
                self.tomar_captura(f"{nombre_base}_tabla_sin_filas", directorio)

                return False

            print(f"  --> Se encontraron {num_filas} filas de datos en la tabla.")
            
            encontrado = False
            for i in range(num_filas):
                fila_actual = filas.nth(i)
                fila_texto_completo = fila_actual.text_content().strip() # Obtener todo el texto de la fila

                if texto_buscado in fila_texto_completo:
                    fila_actual.highlight() # Resaltar la fila encontrada   
                    print(f"\n✅  --> ÉXITO: Texto \"{texto_buscado}\" encontrado en la fila número: {i + 1}")              
                    print(f"  --> Contenido completo de la fila {i + 1}: '{fila_texto_completo}'")              
                            

                    self.tomar_captura(f"{nombre_base}_dato_encontrado_fila_{i+1}", directorio)                 
                    encontrado = True                   
                    time.sleep(tiempo) # Pequeña pausa para ver el resaltado
                    # Si solo necesitamos la primera ocurrencia, podemos salir aquí.                    
                    # Si necesitamos encontrar todas las ocurrencias, removemos el 'break'.                 
                    #break

            if not encontrado:
                print(f"\n❌  --> FALLO: El texto '{texto_buscado}' NO fue encontrado en ninguna fila de la tabla con selector '{table_selector}'.")
                self.tomar_captura(f"{nombre_base}_dato_no_encontrado", directorio)

            return encontrado
        
        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo buscar el texto EXACTO '{texto_buscado}' en la tabla con selector '{table_selector}'.\n"
                f"Posiblemente la tabla o sus filas no estuvieron disponibles a tiempo o la espera de visibilidad falló previamente.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_busqueda_exacta_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al intentar buscar el texto EXACTO '{texto_buscado}' en la tabla con selector '{table_selector}'.\n"
                f"Posibles causas: Selector de tabla inválido, estructura de tabla inesperada, o problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_busqueda_exacta_error_playwright", directorio)
            raise # Relanzar por ser un error de Playwright que podría indicar un problema mayor.

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al buscar el texto EXACTO '{texto_buscado}' en la tabla con selector '{table_selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_busqueda_exacta_error_inesperado", directorio)
            raise # Relanzar por ser un error inesperado.
        
    #28- Función para buscar datos exacto e imprimir la fila
    def busqueda_estricta_imprimir_fila(self, table_selector, texto_buscado, nombre_base, directorio, tiempo= 1) -> bool:
        print(f"\nBuscando coincidencia EXACTA del texto '{texto_buscado}' en la tabla con selector: '{table_selector}'")

        try:
            # Obtener todas las celdas (td o th) que contengan el texto buscado directamente.
            # Usamos :text-is() para una coincidencia exacta de texto dentro de cualquier celda.
            # Esto es más robusto que iterar fila por fila y luego el texto completo de la fila.
            # table_selector es el Locator de la tabla.
            celdas_con_texto = table_selector.locator(f"//td[text()='{texto_buscado}'] | //th[text()='{texto_buscado}']")
            num_celdas_encontradas = celdas_con_texto.count()

            if num_celdas_encontradas == 0:
                print(f"\n❌   --> FALLO: El texto EXACTO '{texto_buscado}' NO fue encontrado en ninguna celda de la tabla con selector '{table_selector}'.")
                self.tomar_captura(f"{nombre_base}_dato_no_encontrado_exacto", directorio)
                return False

            print(f"   --> Se encontraron {num_celdas_encontradas} celdas con el texto EXACTO '{texto_buscado}'.")
            encontrado = False

            for i in range(num_celdas_encontradas):
                celda_actual = celdas_con_texto.nth(i)
                # Obtenemos el Locator de la fila padre de la celda encontrada
                fila_actual = celda_actual.locator("xpath=ancestor::tr")
                fila_actual.highlight() # Resaltar la fila encontrada
                # Obtener todo el texto de la fila
                fila_texto_completo = fila_actual.text_content()

                # 1. Usar split() para dividir la cadena por cualquier secuencia de espacios en blanco
                #    (incluyendo saltos de línea). Esto generará una lista de los datos de cada <td>.
                # 2. Usar join() para unir esos datos con un solo espacio.
                fila_texto_formateado = " ".join(fila_texto_completo.split())

                print(f"\n✅  --> ÉXITO: Texto EXACTO \"{texto_buscado}\" encontrado en una celda de la fila número (estimado): {i + 1}")
                print(f"  --> Contenido completo de la fila: '{fila_texto_formateado}'") # Usamos el texto formateado

                self.tomar_captura(f"{nombre_base}_dato_encontrado_exacto_fila_{i+1}", directorio)
                encontrado = True
                time.sleep(tiempo) # Pequeña pausa para ver el resaltado
                # Si solo necesitamos la primera ocurrencia, podemos salir aquí.
                # Si necesitamos encontrar todas las ocurrencias, removemos el 'break'.
                # break

            return encontrado

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo buscar el texto EXACTO '{texto_buscado}' en la tabla con selector '{table_selector}'.\n"
                f"Posiblemente la tabla o sus filas no estuvieron disponibles a tiempo o la espera de visibilidad falló previamente.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_busqueda_exacta_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al intentar buscar el texto EXACTO '{texto_buscado}' en la tabla con selector '{table_selector}'.\n"
                f"Posibles causas: Selector de tabla inválido, estructura de tabla inesperada, o problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_busqueda_exacta_error_playwright", directorio)
            raise # Relanzar por ser un error de Playwright que podría indicar un problema mayor.

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al buscar el texto EXACTO '{texto_buscado}' en la tabla con selector '{table_selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_busqueda_exacta_error_inesperado", directorio)
            raise # Relanzar por ser un error inesperado.
        
    #29- Función para valida que todos los valores en una columna específica de una tabla sean numéricos
    def verificar_precios_son_numeros(self, tabla_selector, columna_nombre, nombre_base, directorio, tiempo_espera_celda: int = 5000,tiempo = 1) -> bool:
        try:
            print(f"\n⚙️ Verificando que todos los precios en la columna '{columna_nombre}' son números.")

            # No necesitamos volver a llamar a table_locator.to_be_visible() si ya se hizo antes de pasarla
            # Si se pasa como un selector string, entonces sí, el primer to_be_visible() es necesario.
            # Asumiendo que 'tabla_locator' ya es un Locator visible cuando se pasa.
            tabla_selector.highlight()


            # --- PASO CRÍTICO: Esperar a que el tbody exista y tenga contenido ---
            # Esperar a que al menos el tbody y la primera fila dentro de él sean visibles.
            # Esto maneja casos donde el tbody se carga dinámicamente o sus filas tardan en aparecer.
            tbody_locator = tabla_selector.locator("tbody")
            expect(tbody_locator).to_be_visible(timeout=15000) # Aumentamos el timeout para tbody
            print(f"✅ El tbody de la tabla es visible.")
            expect(tbody_locator.locator("tr").first).to_be_visible(timeout=10000) # Espera la primera fila dentro del tbody
            print(f"✅ Al menos la primera fila de datos en la tabla es visible.")


            # 2. Encontrar el índice de la columna "Price"
            # Nos aseguramos de que los headers también estén visibles si no lo estaban ya
            headers = tabla_selector.locator("th")
            expect(headers.first).to_be_visible(timeout=5000) # Espera que al menos un header sea visible

            col_index = -1
            header_texts = []
            for i in range(headers.count()):
                header_text = headers.nth(i).text_content().strip()
                header_texts.append(header_text)
                if header_text == columna_nombre:
                    col_index = i
            
            print(f"🔍 Cabeceras encontradas: {header_texts}")

            if col_index == -1:
                print(f"\n❌ Error: No se encontró la columna '{columna_nombre}' en la tabla.")
                self.tomar_captura(f"{nombre_base}_columna_no_encontrada", directorio)
                return False

            print(f"🔍 Columna '{columna_nombre}' encontrada en el índice: {col_index}")

            # 3. Obtener todas las filas de la tabla (excluyendo la cabecera)
            rows = tbody_locator.locator("tr") # Aseguramos que las filas se busquen dentro del tbody visible
            num_rows = rows.count()
            if num_rows == 0:
                print(f"\n⚠️ Advertencia: La tabla no contiene filas de datos.")
                self.tomar_captura(f"{nombre_base}_tabla_vacia", directorio)
                return True # Consideramos que no hay fallos si no hay datos que validar.

            print(f"🔍 Se encontraron {num_rows} filas de datos.")

            all_prices_are_numbers = True
            for i in range(num_rows):
                # Localizar la celda de precio en la fila actual
                row_locator = rows.nth(i)
                # Aquí también puedes añadir expect(row_locator).to_be_visible() si las filas individuales se "desvanecen"
                
                price_cell = row_locator.locator(f"td").nth(col_index)
                
                # --- AGREGAR UN EXPECT.TO_BE_VISIBLE() PARA LA CELDA ESPECÍFICA ---
                # Esto es crucial si las celdas se cargan de forma diferida.
                # El error indica que esta aserción falla porque el elemento no se encuentra.
                # Lo reubicamos y mejoramos la captura de error.
                expect(price_cell).to_be_visible(timeout=tiempo_espera_celda) 

                price_text = price_cell.text_content().strip()
                price_cell.highlight() # Resaltar la celda actual

                print(f"  Procesando fila {i+1}, precio: '{price_text}'")

                try:
                    float(price_text)
                    print(f"  ✅ '{price_text}' es un número válido.")
                except ValueError:
                    print(f"  ❌ Error: '{price_text}' en la fila {i+1} no es un número válido.")
                    self.tomar_captura(f"{nombre_base}_precio_invalido_fila_{i+1}", directorio)
                    all_prices_are_numbers = False
                    # Continuamos para encontrar todos los errores, no solo el primero.

            if all_prices_are_numbers:
                print(f"\n✅ Todos los precios en la columna '{columna_nombre}' son números válidos.")
                self.tomar_captura(f"{nombre_base}_precios_ok", directorio)
                time.sleep(tiempo) # Pausa si es necesaria para visualización
                return True
            else:
                print(f"\n❌ Se encontraron precios no numéricos en la columna '{columna_nombre}'.")
                raise
                return False

        except Exception as e:
            # Capturamos la excepción general y la tratamos.
            # El AssertionError de expect().to_be_visible() también será capturado aquí.
            print(f"\n❌ Error inesperado al verificar los precios en la tabla. Error: {type(e).__name__}: {e}")
            self.tomar_captura(f"{nombre_base}_excepcion_inesperada", directorio)
            raise
            return False
        
    #30- Función para extrae y retorna el valor de un elemento dado su selector.
    def obtener_valor_elemento(self, selector, nombre_base, directorio, tiempo= 0.5) -> str | None:
        print(f"\nExtrayendo valor del elemento '{selector}'")
        valor_extraido = None
        try:
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_extraccion_valor", directorio)

            # Usamos expect para asegurar que el elemento es visible y habilitado antes de intentar extraer
            expect(selector).to_be_visible(timeout=5000)
            expect(selector).to_be_enabled(timeout=5000)

            # Priorizamos input_value para campos de formulario (incluyendo <select>)
            try:
                # Playwright's input_value() es lo que necesitas para <select> 'value'
                valor_extraido = selector.input_value(timeout=1000)
                print(f"\n  > Valor extraído (input_value) de '{selector}': '{valor_extraido}'")
            except Error: # Usar Error para errores específicos de Playwright (e.g., no es un elemento de entrada)
                # Si falla input_value, intentamos con text_content o inner_text para otros elementos
                try:
                    valor_extraido = selector.text_content(timeout=1000)
                    if valor_extraido is not None:
                        # Si text_content devuelve solo espacios en blanco o es vacío,
                        # intentamos inner_text (que a veces es más preciso para texto visible)
                        if valor_extraido.strip() == "":
                            valor_extraido = selector.inner_text(timeout=1000)
                            print(f"\n  > Valor extraído (inner_text) de '{selector}': '{valor_extraido}'")
                        else:
                            print(f"\n  > Valor extraído (text_content) de '{selector}': '{valor_extraido}'")
                    else:
                        valor_extraido = selector.inner_text(timeout=1000)
                        print(f"\n  > Valor extraído (inner_text) de '{selector}': '{valor_extraido}'")
                except Error:
                    print(f"\n  > No se pudo extraer input_value, text_content ni inner_text de '{selector}'.")
                    valor_extraido = None # Asegurarse de que sea None si todo falla

            if valor_extraido is not None:
                # Stripping whitespace for cleaner results if it's a string
                valor_final = valor_extraido.strip() if isinstance(valor_extraido, str) else valor_extraido
                print(f"\n✅ Valor final obtenido del elemento '{selector}': '{valor_final}'")
                self.tomar_captura(f"{nombre_base}_valor_extraido_exito", directorio)
                return valor_final
            else:
                print(f"\n❌ No se pudo extraer ningún valor significativo del elemento '{selector}'.")
                self.tomar_captura(f"{nombre_base}_fallo_extraccion_valor_no_encontrado", directorio)
                return None

        except TimeoutError as e:
            mensaje_error = (
                f"\n❌ FALLO (Timeout): El elemento '{selector}' "
                f"no se volvió visible/habilitado a tiempo para extraer su valor.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_timeout_extraccion_valor", directorio)
            raise AssertionError(f"\nElemento no disponible para extracción de valor: {selector}") from e

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright): Ocurrió un error de Playwright al intentar extraer el valor de '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_playwright_error_extraccion_valor", directorio)
            raise AssertionError(f"\nError de Playwright al extraer valor: {selector}") from e

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al intentar extraer el valor de '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_inesperado_extraccion_valor", directorio)
            raise AssertionError(f"\nError inesperado al extraer valor: {selector}") from e
    
    #31- Función para verificar que los encabezados de las columnas de una tabla sean correctos y estén presentes.
    def verificar_encabezados_tabla(self, selector, encabezados_esperados: list[str], nombre_base, directorio, tiempo= 1) -> bool:
        print(f"\nVerificando encabezados de la tabla con selector '{selector}'...")

        try:
            # 1. Verificar la presencia de la tabla misma
            table_locator = selector
            # Esperar a que la tabla esté visible. Esto es crucial para evitar errores prematuros.
            #expect(table_locator).to_be_visible(timeout=5000) # Ajusta el timeout según necesidad

            # 2. Verificar la presencia del elemento thead dentro de la tabla
            # Usamos .locator().count() en vez de .to_have_count(0) para poder manejar el caso de no existencia
            # sin lanzar un error de expect, ya que queremos manejarlo explícitamente.
            thead_locator = table_locator.locator("thead") # Correcto: encadenamiento de Locators
            num_theads_actuales = thead_locator.count()

            if num_theads_actuales == 0:
                print(f"\n❌ --> FALLO: La tabla con selector '{selector}' no contiene un elemento '<thead>' (cabecera).")
                self.tomar_captura(f"{nombre_base}_no_thead_encontrado", directorio)
                return False

            # Si llegamos aquí, significa que thead existe. Ahora buscamos los th dentro de él.
            encabezados_actuales_locators = thead_locator.locator("th")
            encabezados_actuales_locators.highlight() # Resaltar la fila encontrada   
            num_encabezados_actuales = encabezados_actuales_locators.count()
            num_encabezados_esperados = len(encabezados_esperados)

            if num_encabezados_actuales == 0:
                # Este caso cubre que el thead existe, pero está vacío de th, o que los th no se encontraron
                # dentro del thead. Es una advertencia, pero se convierte en fallo si no coincide con los esperados.
                print(f"\n⚠️  --> ADVERTENCIA: Se encontró el '<thead>', pero no se encontraron elementos '<th>' dentro con el selector '{selector} thead th'.")
                self.tomar_captura(f"{nombre_base}_no_encabezados_th_encontrados", directorio)
                if num_encabezados_esperados > 0: # Si se esperaban encabezados pero no se encontraron th
                    print(f"\n❌ --> FALLO: Se esperaban {num_encabezados_esperados} encabezados, pero no se encontraron '<th>' dentro de la cabecera.")
                    return False
                else: # Si no se esperaban encabezados (lista vacía) y no hay th, entonces es un éxito.
                    print("\n✅ ÉXITO: No se esperaban encabezados y no se encontraron '<th>' dentro de la cabecera.")
                    self.tomar_captura(f"{nombre_base}_no_encabezados_esperados_y_no_th", directorio)
                    return True


            if num_encabezados_actuales != num_encabezados_esperados:
                print(f"\n❌ --> FALLO: El número de encabezados '<th>' encontrados ({num_encabezados_actuales}) "
                      f"no coincide con el número de encabezados esperados ({num_encabezados_esperados}).")
                self.tomar_captura(f"{nombre_base}_cantidad_encabezados_incorrecta", directorio)
                return False

            todos_correctos = True
            for i in range(num_encabezados_esperados):
                encabezado_locator = encabezados_actuales_locators.nth(i)
                # Usamos all_text_contents() si quieremos comparar sin espacios/newlines y en orden
                # O text_content().strip() si es uno a uno como lo tienes.
                texto_encabezado_actual = encabezado_locator.text_content().strip()
                encabezado_esperado = encabezados_esperados[i]

                if texto_encabezado_actual == encabezado_esperado:
                    print(f"\n  ✅ Encabezado {i+1}: '{texto_encabezado_actual}' coincide con el esperado '{encabezado_esperado}'.")
                    # encabezado_locator.highlight() # Opcional: resaltar el encabezado
                    time.sleep(tiempo) # Pausa para ver el resaltado
                else:
                    print(f"\n  ❌ FALLO: Encabezado {i+1} esperado era '{encabezado_esperado}', pero se encontró '{texto_encabezado_actual}'.")
                    encabezado_locator.highlight()
                    self.tomar_captura(f"{nombre_base}_encabezado_incorrecto_{i+1}", directorio)
                    todos_correctos = False
                    time.sleep(tiempo) # Pausa para ver el resaltado

            if todos_correctos:
                print("\n✅ ÉXITO: Todos los encabezados de columna son correctos y están en el orden esperado.")
                self.tomar_captura(f"{nombre_base}_encabezados_verificados_ok", directorio)
            else:
                print("\n❌ FALLO: Uno o más encabezados de columna son incorrectos o no están en el orden esperado.")
                self.tomar_captura(f"{nombre_base}_encabezados_verificados_fallo", directorio)

            return todos_correctos

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo encontrar la tabla o sus encabezados con el selector '{selector}'.\n"
                f"Posiblemente la tabla no estuvo disponible a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_verificar_encabezados_timeout", directorio)
            return False

        except Error as e: # Catch Playwright-specific errors
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al intentar verificar la tabla o sus encabezados con el selector '{selector}'.\n"
                f"Posibles causas: Selector inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_verificar_encabezados_error_playwright", directorio)
            raise # Relanzar por ser un error de Playwright que podría indicar un problema mayor.

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar los encabezados de la tabla con el selector '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_verificar_encabezados_error_inesperado", directorio)
            raise # Relanzar por ser un error inesperado.
        
    #32- Función para verificar los datos de las filas de una tabla
    def verificar_datos_filas_tabla(self, selector, datos_filas_esperados: list[dict], nombre_base, directorio, tiempo: int = 1) -> bool:
        print(f"\n--- Iniciando verificación de datos de las filas de la tabla con locator '{selector}' ---")
        self.tomar_captura(f"{nombre_base}_inicio_verificacion_datos_filas", directorio) # Renombrado para claridad

        try:
            # Asegurarse de que la tabla está visible y disponible
            expect(selector).to_be_visible(timeout=10000) # Ajusta el timeout si es necesario
            print("Tabla visible. Procediendo a verificar los datos.")

            # Obtener los encabezados para mapear los índices de las columnas
            header_locators = selector.locator("thead th")
            headers = [h.text_content().strip() for h in header_locators.all()]
            
            if not headers:
                print(f"\n❌ --> FALLO: No se encontraron encabezados en la tabla con locator '{selector}'. No se pueden verificar los datos de las filas.")
                self.tomar_captura(f"{nombre_base}_no_headers_para_datos_filas", directorio)
                return False

            # Obtener todas las filas del cuerpo de la tabla (excluyendo thead)
            row_locators = selector.locator("tbody tr")
            num_filas_actuales = row_locators.count()
            num_filas_esperadas = len(datos_filas_esperados)

            if num_filas_actuales == 0 and num_filas_esperadas == 0:
                print("\n✅ ÉXITO: No se esperaban filas y no se encontraron filas en la tabla.")
                self.tomar_captura(f"{nombre_base}_no_rows_expected_and_found", directorio)
                return True
            
            if num_filas_actuales != num_filas_esperadas:
                print(f"\n❌ --> FALLO: El número de filas encontradas ({num_filas_actuales}) "
                      f"no coincide con el número de filas esperadas ({num_filas_esperadas}).")
                self.tomar_captura(f"{nombre_base}_cantidad_filas_incorrecta", directorio)
                return False

            # --- Variable principal para el retorno ---
            todos_los_datos_correctos = True 

            for i in range(num_filas_esperadas):
                fila_actual_locator = row_locators.nth(i)
                datos_fila_esperada = datos_filas_esperados[i]
                print(f"\n  Verificando Fila {i+1} (ID esperado: {datos_fila_esperada.get('ID', 'N/A')})...")
                fila_actual_locator.highlight() # Resaltar la fila actual en la captura para debug.

                # Bandera para saber si la fila actual tiene algún fallo
                fila_actual_correcta = True 

                for col_name, expected_value in datos_fila_esperada.items():
                    try:
                        # Encontrar el índice de la columna por su nombre
                        if col_name not in headers:
                            print(f"\n  ❌ FALLO: Columna '{col_name}' esperada no encontrada en los encabezados de la tabla. Encabezados actuales: {headers}")
                            self.tomar_captura(f"{nombre_base}_columna_no_encontrada", directorio)
                            todos_los_datos_correctos = False # Falla general
                            fila_actual_correcta = False # Falla en esta fila
                            continue # Pasa a la siguiente columna esperada o fila

                        col_index = headers.index(col_name)
                        
                        # Localizar la celda específica (td) dentro de la fila por su índice
                        celda_locator = fila_actual_locator.locator("td").nth(col_index)
                        
                        if col_name == "Select": # Lógica específica para el checkbox
                            checkbox_locator = celda_locator.locator("input[type='checkbox']")
                            if checkbox_locator.count() == 0:
                                print(f"\n  ❌ FALLO: Checkbox no encontrado en la columna '{col_name}' de la Fila {i+1}.")
                                checkbox_locator.highlight()
                                self.tomar_captura(f"{nombre_base}_fila_{i+1}_no_checkbox", directorio)
                                todos_los_datos_correctos = False
                                fila_actual_correcta = False
                            elif isinstance(expected_value, bool): # Si se espera un estado específico (True/False)
                                if checkbox_locator.is_checked() != expected_value:
                                    print(f"\n  ❌ FALLO: El checkbox de la Fila {i+1}, Columna '{col_name}' estaba "
                                          f"{'marcado' if checkbox_locator.is_checked() else 'desmarcado'}, se esperaba {'marcado' if expected_value else 'desmarcado'}.")
                                    checkbox_locator.highlight()
                                    self.tomar_captura(f"{nombre_base}_fila_{i+1}_checkbox_estado_incorrecto", directorio)
                                    todos_los_datos_correctos = False
                                    fila_actual_correcta = False
                                else:
                                    print(f"  ✅ Fila {i+1}, Columna '{col_name}': Checkbox presente y estado correcto ({'marcado' if expected_value else 'desmarcado'}).")
                            else: # Si solo se espera que el checkbox exista, pero no se especificó un estado booleano
                                print(f"  ✅ Fila {i+1}, Columna '{col_name}': Checkbox presente (estado no verificado explícitamente).")
                        else: # Para otras columnas de texto
                            actual_value = celda_locator.text_content().strip()
                            # Aseguramos que expected_value también sea una cadena para la comparación
                            if actual_value != str(expected_value).strip(): 
                                print(f"\n  ❌ FALLO: Fila {i+1}, Columna '{col_name}'. Se esperaba '{expected_value}', se encontró '{actual_value}'.")
                                celda_locator.highlight()
                                self.tomar_captura(f"{nombre_base}_fila_{i+1}_col_{col_name}_incorrecta", directorio)
                                todos_los_datos_correctos = False
                                fila_actual_correcta = False
                            else:
                                print(f"  ✅ Fila {i+1}, Columna '{col_name}': '{actual_value}' coincide con lo esperado.")
                        
                    except Exception as col_e:
                        print(f"\n  ❌ ERROR INESPERADO al verificar la columna '{col_name}' de la Fila {i+1}: {col_e}")
                        self.tomar_captura(f"{nombre_base}_error_columna_inesperado", directorio)
                        todos_los_datos_correctos = False
                        fila_actual_correcta = False
                        # Podrías decidir si quieres continuar con el resto de las columnas/filas
                        # o si este error debe detener la verificación.

                # Pausa solo si la fila actual tuvo algún fallo para que la captura sea más útil
                if not fila_actual_correcta:
                    time.sleep(tiempo) 

            # --- Retorno final basado en el estado acumulado ---
            if todos_los_datos_correctos:
                print("\n✅ ÉXITO: Todos los datos de las filas y checkboxes son correctos y están presentes.")
                self.tomar_captura(f"{nombre_base}_datos_filas_verificados_ok", directorio)
                return True
            else:
                print("\n❌ FALLO: Uno o más datos de las filas o checkboxes son incorrectos o faltan.")
                self.tomar_captura(f"{nombre_base}_datos_filas_verificados_fallo", directorio)
                return False

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo encontrar la tabla o sus filas con el locator '{selector}'.\n"
                f"Posiblemente la tabla no estuvo disponible a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_verificar_datos_filas_timeout", directorio)
            return False

        except Error as e: # Captura errores específicos de Playwright
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al intentar verificar las filas con el locator '{selector}'.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_verificar_datos_filas_error_playwright", directorio)
            raise # Relanza por ser un error de Playwright que podría indicar un problema mayor.

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar los datos de las filas con el locator '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_verificar_datos_filas_error_inesperado", directorio)
            raise # Relanza por ser un error inesperado.
    
    #34- Función para seleccionar y verificar el estado de checkboxes de filas aleatorias.
    def seleccionar_y_verificar_checkboxes_aleatorios(self, selector_tabla, num_checkboxes_a_interactuar: int, nombre_base, directorio, tiempo: int = 1) -> bool:
        print(f"\nIniciando selección y verificación de {num_checkboxes_a_interactuar} checkbox(es) aleatorio(s) en la tabla con locator '{selector_tabla}'...")
        self.tomar_captura(f"{nombre_base}_inicio_seleccion_checkbox", directorio)

        try:
            # Asegurarse de que la tabla está visible
            expect(selector_tabla).to_be_visible(timeout=10000)
            
            # Obtener todos los locators de los checkboxes en las celdas de la tabla
            all_checkbox_locators = selector_tabla.locator("tbody tr td input[type='checkbox']")
            
            num_checkboxes_disponibles = all_checkbox_locators.count()

            if num_checkboxes_disponibles == 0:
                print(f"\n❌ --> FALLO: No se encontraron checkboxes en la tabla con locator '{selector_tabla.locator('tbody tr td input[type=\"checkbox\"]')}'.")
                self.tomar_captura(f"{nombre_base}_no_checkboxes_encontrados", directorio)
                return False
            
            if num_checkboxes_a_interactuar <= 0:
                print("\n⚠️  ADVERTENCIA: El número de checkboxes a interactuar es 0 o negativo. No se realizará ninguna acción.")
                return True # Consideramos éxito si no hay nada que hacer

            if num_checkboxes_a_interactuar > num_checkboxes_disponibles:
                print(f"\n❌ --> FALLO: Se solicitaron {num_checkboxes_a_interactuar} checkboxes, pero solo hay {num_checkboxes_disponibles} disponibles.")
                self.tomar_captura(f"{nombre_base}_no_suficientes_checkboxes", directorio)
                return False

            print(f"\nSe encontraron {num_checkboxes_disponibles} checkboxes. Seleccionando {num_checkboxes_a_interactuar} aleatoriamente...")

            # Seleccionar N índices de checkboxes aleatorios y únicos
            random_indices = random.sample(range(num_checkboxes_disponibles), num_checkboxes_a_interactuar)
            
            todos_correctos = True

            for i, idx in enumerate(random_indices):
                checkbox_to_interact = all_checkbox_locators.nth(idx)
                
                # Resaltar el checkbox actual para la captura/visualización
                checkbox_to_interact.highlight()
                self.tomar_captura(f"{nombre_base}_checkbox_{i+1}_seleccionado_idx_{idx}", directorio)
                time.sleep(tiempo)

                # Obtener el ID del producto asociado a esta fila (asumiendo ID en la primera columna)
                try:
                    row_locator = selector_tabla.locator("tbody tr").nth(idx)
                    product_id = row_locator.locator("td").nth(0).text_content().strip()
                except Exception:
                    product_id = "Desconocido"
                
                initial_state = checkbox_to_interact.is_checked()
                print(f"\n  Checkbox del Producto ID: {product_id} (Fila: {idx+1}): Estado inicial {'MARCADO' if initial_state else 'DESMARCADO'}.")

                # --- Lógica para asegurar que el click lo deje en estado 'seleccionado' ---
                if initial_state: # Si ya está marcado, lo desmarcamos primero con un clic
                    print(f"\n  El checkbox del Producto ID: {product_id} ya está MARCADO. Haciendo clic para desmarcar antes de seleccionar.")
                    checkbox_to_interact.uncheck()
                    time.sleep(0.5) # Pausa para que el DOM se actualice
                    if checkbox_to_interact.is_checked():
                        print(f"\n  ❌ FALLO: El checkbox del Producto ID: {product_id} no se desmarcó correctamente para la interacción.")
                        checkbox_to_interact.highlight()
                        self.tomar_captura(f"{nombre_base}_fila_{idx+1}_no_se_desmarco", directorio)
                        todos_correctos = False
                        continue # Pasa al siguiente checkbox aleatorio
                
                # Ahora el checkbox debería estar DESMARCADO (o siempre lo estuvo)
                print(f"\n  Haciendo clic en el checkbox del Producto ID: {product_id} para MARCARLO...")
                checkbox_to_interact.check()
                time.sleep(0.5) # Pausa para que el DOM se actualice

                final_state = checkbox_to_interact.is_checked()
                if not final_state: # Si no está marcado (seleccionado) después del clic
                    print(f"\n  ❌ FALLO: El checkbox del Producto ID: {product_id} no cambió a MARCADO después del clic. Sigue DESMARCADO.")
                    checkbox_to_interact.highlight()
                    self.tomar_captura(f"{nombre_base}_fila_{idx+1}_no_se_marco", directorio)
                    todos_correctos = False
                else:
                    print(f"\n  ✅ ÉXITO: El checkbox del Producto ID: {product_id} ahora está MARCADO (seleccionado).")
                    self.tomar_captura(f"{nombre_base}_fila_{idx+1}_marcado_ok", directorio)
                
                if not todos_correctos: # Si hubo un fallo en este checkbox, pausa antes del siguiente
                    time.sleep(tiempo)

            if todos_correctos:
                print(f"\n✅ ÉXITO: Todos los {num_checkboxes_a_interactuar} checkbox(es) aleatorio(s) fueron seleccionados y verificados correctamente.")
                self.tomar_captura(f"{nombre_base}_todos_seleccionados_ok", directorio)
            else:
                print(f"\n❌ FALLO: Uno o más checkbox(es) aleatorio(s) no pudieron ser seleccionados o verificados.")
                self.tomar_captura(f"{nombre_base}_fallo_general_seleccion", directorio)

            return todos_correctos

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo encontrar la tabla o los checkboxes con el locator '{selector_tabla}'.\n"
                f"Posiblemente los elementos no estuvieron disponibles a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_seleccion_checkbox_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al seleccionar y verificar checkboxes en la tabla '{selector_tabla}'.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_seleccion_checkbox_error_playwright", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al seleccionar y verificar checkboxes aleatorios.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_seleccion_checkbox_error_inesperado", directorio)
            raise
        
     # ---
    
    #35- Función para seleccionar y verificar el estado de checkboxes de filas CONSECUTIVAS.
    def seleccionar_y_verificar_checkboxes_consecutivos(self, selector_tabla, start_index: int, num_checkboxes_a_interactuar: int, nombre_base, directorio, tiempo= 1) -> bool:
        print(f"\nIniciando selección y verificación de {num_checkboxes_a_interactuar} checkbox(es) consecutivo(s) "
              f"a partir del índice {start_index} en la tabla con locator '{selector_tabla}'...")
        self.tomar_captura(f"{nombre_base}_inicio_seleccion_consecutiva_checkbox", directorio)

        try:
            # Asegurarse de que la tabla está visible
            expect(selector_tabla).to_be_visible(timeout=10000)
            
            # Obtener todos los locators de los checkboxes en las celdas de la tabla
            all_checkbox_locators = selector_tabla.locator("tbody tr td input[type='checkbox']")
            
            num_checkboxes_disponibles = all_checkbox_locators.count()

            if num_checkboxes_disponibles == 0:
                print(f"\n❌ --> FALLO: No se encontraron checkboxes en la tabla con locator '{selector_tabla.locator('tbody tr td input[type=\"checkbox\"]')}'.")
                self.tomar_captura(f"{nombre_base}_no_checkboxes_encontrados_consec", directorio)
                return False
            
            if num_checkboxes_a_interactuar <= 0:
                print("\n⚠️  ADVERTENCIA: El número de checkboxes a interactuar es 0 o negativo. No se realizará ninguna acción.")
                return True # Consideramos éxito si no hay nada que hacer

            if start_index < 0 or start_index >= num_checkboxes_disponibles:
                print(f"\n❌ --> FALLO: El 'posición de inicio' ({start_index}) está fuera del rango válido de checkboxes disponibles (0 a {num_checkboxes_disponibles - 1}).")
                self.tomar_captura(f"{nombre_base}_start_index_invalido_consec", directorio)
                return False
            
            if (start_index + num_checkboxes_a_interactuar) > num_checkboxes_disponibles:
                print(f"\n❌ --> FALLO: Se solicitaron {num_checkboxes_a_interactuar} checkboxes a partir del índice {start_index}, "
                      f"pero solo hay {num_checkboxes_disponibles} disponibles. El rango excede los límites de la tabla.")
                self.tomar_captura(f"{nombre_base}_rango_excedido_consec", directorio)
                return False

            print(f"\nInteractuando con {num_checkboxes_a_interactuar} checkbox(es) consecutivo(s) "
                  f"desde el índice {start_index} hasta el {start_index + num_checkboxes_a_interactuar - 1}...")
            
            todos_correctos = True

            for i in range(num_checkboxes_a_interactuar):
                current_idx = start_index + i
                checkbox_to_interact = all_checkbox_locators.nth(current_idx)
                
                # Resaltar el checkbox actual para la captura/visualización
                checkbox_to_interact.highlight()
                self.tomar_captura(f"{nombre_base}_checkbox_consecutivo_{i+1}_idx_{current_idx}", directorio)
                time.sleep(tiempo)

                # Obtener el ID del producto asociado a esta fila (asumiendo ID en la primera columna)
                try:
                    row_locator = selector_tabla.locator("tbody tr").nth(current_idx)
                    product_id = row_locator.locator("td").nth(0).text_content().strip()
                except Exception:
                    product_id = "Desconocido"
                
                initial_state = checkbox_to_interact.is_checked()
                print(f"  Checkbox del Producto ID: {product_id} (Fila: {current_idx+1}): Estado inicial {'MARCADO' if initial_state else 'DESMARCADO'}.")

                # --- Lógica para asegurar que el click lo deje en estado 'seleccionado' ---
                if initial_state: # Si ya está marcado, lo desmarcamos primero con un clic
                    print(f"\n  El checkbox del Producto ID: {product_id} ya está MARCADO. Haciendo clic para desmarcar antes de seleccionar.")
                    checkbox_to_interact.uncheck()
                    time.sleep(0.5) # Pausa para que el DOM se actualice
                    if checkbox_to_interact.is_checked():
                        print(f"  ❌ FALLO: El checkbox del Producto ID: {product_id} no se desmarcó correctamente para la interacción.")
                        checkbox_to_interact.highlight()
                        self.tomar_captura(f"{nombre_base}_fila_{current_idx+1}_no_se_desmarco_consec", directorio)
                        todos_correctos = False
                        continue # Pasa al siguiente checkbox consecutivo
                
                # Ahora el checkbox debería estar DESMARCADO (o siempre lo estuvo)
                print(f"  Haciendo clic en el checkbox del Producto ID: {product_id} para MARCARLO...")
                checkbox_to_interact.check()
                time.sleep(0.5) # Pausa para que el DOM se actualice

                final_state = checkbox_to_interact.is_checked()
                if not final_state: # Si no está marcado (seleccionado) después del clic
                    print(f"\n  ❌ FALLO: El checkbox del Producto ID: {product_id} no cambió a MARCADO después del clic. Sigue DESMARCADO.")
                    checkbox_to_interact.highlight()
                    self.tomar_captura(f"{nombre_base}_fila_{current_idx+1}_no_se_marco_consec", directorio)
                    todos_correctos = False
                else:
                    print(f"  ✅ ÉXITO: El checkbox del Producto ID: {product_id} ahora está MARCADO (seleccionado).")
                    self.tomar_captura(f"{nombre_base}_fila_{current_idx+1}_marcado_ok_consec", directorio)
                
                if not todos_correctos: # Si hubo un fallo en este checkbox, pausa antes del siguiente
                    time.sleep(tiempo)

            if todos_correctos:
                print(f"\n✅ ÉXITO: Todos los {num_checkboxes_a_interactuar} checkbox(es) consecutivo(s) fueron seleccionados y verificados correctamente.")
                self.tomar_captura(f"{nombre_base}_todos_seleccionados_ok_consec", directorio)
            else:
                print(f"\n❌ FALLO: Uno o más checkbox(es) consecutivo(s) no pudieron ser seleccionados o verificados.")
                self.tomar_captura(f"{nombre_base}_fallo_general_seleccion_consec", directorio)

            return todos_correctos

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo encontrar la tabla o los checkboxes con el locator '{selector_tabla}'.\n"
                f"Posiblemente los elementos no estuvieron disponibles a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_seleccion_consec_checkbox_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al seleccionar y verificar checkboxes consecutivos en la tabla '{selector_tabla}'.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_seleccion_consec_checkbox_error_playwright", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al seleccionar y verificar checkboxes consecutivos.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_seleccion_consec_checkbox_error_inesperado", directorio)
            raise
        
    #36- Función para deseleccionar un checkbox ya marcado y verificar su estado.
    def deseleccionar_y_verificar_checkbox_marcado_aleatorio(self, selector_tabla, nombre_base, directorio, tiempo= 1) -> bool:
        print(f"\nIniciando deselección y verificación de TODOS los checkboxes marcados "
              f"en la tabla con locator '{selector_tabla}'...")
        self.tomar_captura(f"{nombre_base}_inicio_deseleccion_todos_marcados", directorio)

        try:
            # Asegurarse de que la tabla está visible
            expect(selector_tabla).to_be_visible(timeout=10000)
            
            # Obtener todos los locators de los checkboxes en las celdas de la tabla
            all_checkbox_locators = selector_tabla.locator("tbody tr td input[type='checkbox']")
            
            num_checkboxes_disponibles = all_checkbox_locators.count()

            if num_checkboxes_disponibles == 0:
                print(f"\n❌ --> FALLO: No se encontraron checkboxes en la tabla con locator '{selector_tabla.locator('tbody tr td input[type=\"checkbox\"]')}'.")
                self.tomar_captura(f"{nombre_base}_no_checkboxes_encontrados_todos", directorio)
                return False
            
            # Recolectar todos los checkboxes que están actualmente marcados para deseleccionar
            checkboxes_to_deselect = []
            for i in range(num_checkboxes_disponibles):
                checkbox = all_checkbox_locators.nth(i)
                if checkbox.is_checked():
                    checkboxes_to_deselect.append({"locator": checkbox, "original_index": i})
            
            if not checkboxes_to_deselect:
                print("\n⚠️  ADVERTENCIA: No se encontró ningún checkbox actualmente MARCADO en la tabla para deseleccionar. Prueba completada sin acciones.")
                self.tomar_captura(f"{nombre_base}_no_marcados_para_deseleccionar", directorio)
                return True # Consideramos éxito si no hay nada que deseleccionar

            print(f"Se encontraron {len(checkboxes_to_deselect)} checkbox(es) marcado(s) para deseleccionar.")

            todos_deseleccionados_correctamente = True

            for i, checkbox_info in enumerate(checkboxes_to_deselect):
                checkbox_to_interact = checkbox_info["locator"]
                original_idx = checkbox_info["original_index"]
                
                # Resaltar el checkbox actual
                checkbox_to_interact.highlight()
                self.tomar_captura(f"{nombre_base}_deseleccion_actual_{i+1}_idx_{original_idx}", directorio)
                time.sleep(tiempo)

                # Obtener el ID del producto asociado a esta fila (asumiendo ID en la primera columna)
                try:
                    row_locator = selector_tabla.locator("tbody tr").nth(original_idx)
                    product_id = row_locator.locator("td").nth(0).text_content().strip()
                except Exception:
                    product_id = "Desconocido"
                
                print(f"\n  Procesando checkbox del Producto ID: {product_id} (Fila: {original_idx+1}). Estado inicial: MARCADO (esperado).")

                # --- Interacción: Clic para deseleccionar ---
                print(f"\n  Haciendo clic en el checkbox del Producto ID: {product_id} para DESMARCARLO...")
                checkbox_to_interact.click()
                time.sleep(0.5) # Pausa para que el DOM se actualice

                final_state = checkbox_to_interact.is_checked()
                if final_state: # Si sigue marcado después del clic
                    print(f"\n  ❌ FALLO: El checkbox del Producto ID: {product_id} no cambió a DESMARCADO después del clic. Sigue MARCADO.")
                    checkbox_to_interact.highlight()
                    self.tomar_captura(f"{nombre_base}_fila_{original_idx+1}_no_desmarcado", directorio)
                    todos_deseleccionados_correctamente = False
                else:
                    print(f"\n  ✅ ÉXITO: El checkbox del Producto ID: {product_id} ahora está DESMARCADO (deseleccionado).")
                    self.tomar_captura(f"{nombre_base}_fila_{original_idx+1}_desmarcado_ok", directorio)
                
                if not todos_deseleccionados_correctamente:
                    time.sleep(tiempo) # Pausa si hubo un fallo para visualización

            if todos_deseleccionados_correctamente:
                print(f"\n✅ ÉXITO: Todos los {len(checkboxes_to_deselect)} checkbox(es) marcados fueron deseleccionados y verificados correctamente.")
                self.tomar_captura(f"{nombre_base}_todos_deseleccionados_ok", directorio)
            else:
                print(f"\n❌ FALLO: Uno o más checkbox(es) marcados no pudieron ser deseleccionados o verificados.")
                self.tomar_captura(f"{nombre_base}_fallo_general_deseleccion_todos", directorio)

            return todos_deseleccionados_correctamente

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se pudo encontrar la tabla o los checkboxes con el locator '{selector_tabla}'.\n"
                f"Posiblemente los elementos no estuvieron disponibles a tiempo.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_deseleccion_todos_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al deseleccionar y verificar todos los checkboxes marcados en la tabla '{selector_tabla}'.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_deseleccion_todos_error_playwright", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al deseleccionar y verificar todos los checkboxes marcados.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_deseleccion_todos_error_inesperado", directorio)
            raise
    
    #37- Función para busca un 'texto_a_buscar' en todas las celdas de una tabla (tbody) y, si lo encuentra, intenta marcar el checkbox asociado en la misma fila..   
    def seleccionar_checkbox_por_contenido_celda(self, selector_tabla, texto_a_buscar: str, nombre_base, directorio, case_sensitive: bool = False, timeout: int = 10000, tiempo= 0.5) -> bool:
        print(f"\n--- Iniciando búsqueda de '{texto_a_buscar}' en la tabla {selector_tabla} para marcar checkboxes ---")
        self.tomar_captura(f"{nombre_base}_inicio_busqueda_celdas", directorio)

        try:
            # Asegurarse de que la tabla está visible y cargada
            expect(selector_tabla).to_be_visible(timeout=timeout)
            print("Tabla visible. Comenzando a iterar por filas y celdas.")

            # Obtener todas las filas del cuerpo de la tabla
            filas = selector_tabla.locator("tbody tr")
            num_filas = filas.count()

            if num_filas == 0:
                print(f"\n❌ --> FALLO: No se encontraron filas en el 'tbody' de la tabla con locator '{selector_tabla}'.")
                self.tomar_captura(f"{nombre_base}_no_filas_encontradas", directorio)
                return False

            print(f"Se encontraron {num_filas} filas en la tabla.")
            
            checkboxes_marcados_exitosamente = 0
            
            # Normalizar el texto de búsqueda si no es sensible a mayúsculas/minúsculas
            search_text_normalized = texto_a_buscar if case_sensitive else texto_a_buscar.lower()

            for i in range(num_filas):
                fila_actual = filas.nth(i)
                # Obtener todas las celdas (td) de la fila actual, excluyendo posibles celdas de encabezado (th) si las hubiera en tbody
                celdas = fila_actual.locator("td")
                num_celdas = celdas.count()

                if num_celdas == 0:
                    print(f"ADVERTENCIA: La fila {i+1} no contiene celdas (td). Saltando.")
                    continue

                celda_encontrada = False
                for j in range(num_celdas):
                    celda_actual = celdas.nth(j)
                    celda_texto = celda_actual.text_content().strip()
                    
                    # Normalizar el texto de la celda para la comparación
                    celda_texto_normalized = celda_texto if case_sensitive else celda_texto.lower()

                    if search_text_normalized in celda_texto_normalized:
                        print(f"✅ Coincidencia encontrada en Fila {i+1}, Celda {j+1}: '{celda_texto}' contiene '{texto_a_buscar}'.")
                        celda_encontrada = True
                        
                        # Buscar el checkbox dentro de la misma fila
                        checkbox_locator = fila_actual.locator("input[type='checkbox']")
                        
                        if checkbox_locator.count() > 0:
                            checkbox = checkbox_locator.first
                            checkbox.highlight()
                            self.tomar_captura(f"{nombre_base}_fila_{i+1}_coincidencia", directorio)
                            time.sleep(tiempo)

                            if not checkbox.is_checked():
                                print(f"  --> Marcando checkbox en Fila {i+1}...")
                                checkbox.check()
                                time.sleep(tiempo)
                                if checkbox.is_checked():
                                    print(f"  ✅ Checkbox en Fila {i+1} marcado correctamente.")
                                    checkboxes_marcados_exitosamente += 1
                                    self.tomar_captura(f"{nombre_base}_fila_{i+1}_checkbox_marcado", directorio)
                                else:
                                    print(f"  ❌ FALLO: No se pudo marcar el checkbox en Fila {i+1}.")
                                    self.tomar_captura(f"{nombre_base}_fila_{i+1}_checkbox_no_marcado", directorio)
                            else:
                                print(f"  ⚠️ Checkbox en Fila {i+1} ya estaba marcado. No se requiere acción.")
                                self.tomar_captura(f"{nombre_base}_fila_{i+1}_checkbox_ya_marcado", directorio)
                        else:
                            print(f"  ⚠️ ADVERTENCIA: No se encontró un checkbox en la Fila {i+1} a pesar de la coincidencia.")
                        break # Salir del bucle de celdas una vez encontrada la coincidencia en la fila

                if not celda_encontrada:
                    print(f"  No se encontró '{texto_a_buscar}' en la Fila {i+1}.")

            if checkboxes_marcados_exitosamente > 0:
                print(f"\n✅ ÉXITO: Se marcaron {checkboxes_marcados_exitosamente} checkbox(es) basados en la búsqueda de '{texto_a_buscar}'.")
                self.tomar_captura(f"{nombre_base}_busqueda_finalizada_exito", directorio)
                return True
            else:
                print(f"\n⚠️ ADVERTENCIA: No se encontraron coincidencias para '{texto_a_buscar}' o no se pudo marcar ningún checkbox.")
                self.tomar_captura(f"{nombre_base}_busqueda_finalizada_sin_marcados", directorio)
                return False

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): La tabla con el locator '{selector_tabla}' no estuvo visible a tiempo (timeout de {timeout}ms).\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_timeout_tabla", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error al interactuar con la tabla o los checkboxes.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado durante la búsqueda y marcado de checkboxes.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #38- Función para verifica que la página inicial esperada esté seleccionada y resaltada en un componente de paginación.
    def verificar_pagina_inicial_seleccionada(self, selector_paginado, texto_pagina_inicial: str, nombre_base, directorio, clase_resaltado: str = "active", timeout: int = 10000) -> bool:
        print(f"\n--- Iniciando verificación del estado inicial de la paginación ---")
        print(f"Contenedor de paginación locator: '{selector_paginado}'")
        print(f"Página inicial esperada: '{texto_pagina_inicial}'")
        self.tomar_captura(f"{nombre_base}_inicio_verificacion_paginacion", directorio)

        try:
            # Asegurarse de que el contenedor de paginación está visible
            expect(selector_paginado).to_be_visible(timeout=timeout)
            print("\nContenedor de paginación visible. Procediendo a verificar la página inicial.")

            # Intentar encontrar el elemento de la página inicial por su texto dentro del contenedor
            # Se usa text= para una coincidencia exacta del texto visible del número de página
            # Es importante asegurarse que este selector apunte al elemento clickable de la página (ej. un <a> o <span> dentro de un <li>)
            # Podría ser necesario ajustar el selector para ser más específico si el texto '1' aparece en otros lugares.
            # Por ejemplo: selector_contenedor_paginacion.locator(f"li a:has-text('{texto_pagina_inicial}')")
            pagina_inicial_locator = selector_paginado.locator(f"text='{texto_pagina_inicial}'").first

            # Esperar a que el elemento de la página inicial esté visible y sea interactuable
            expect(pagina_inicial_locator).to_be_visible(timeout=timeout)
            print(f"\nElemento para la página '{texto_pagina_inicial}' encontrado.")

            # 1. Verificar que la página inicial esperada esté seleccionada (marcada con la clase de resaltado)
            print(f"\nVerificando si la página '{texto_pagina_inicial}' tiene la clase de resaltado '{clase_resaltado}'...")
            pagina_inicial_locator.highlight() # Resaltar el elemento para la captura
            self.tomar_captura(f"{nombre_base}_pagina_inicial_encontrada", directorio)

            # --- CAMBIO CLAVE AQUÍ: Usar get_attribute("class") y verificar la subclase ---
            current_classes = pagina_inicial_locator.get_attribute("class")
            
            if current_classes and clase_resaltado in current_classes.split():
                print(f"\n  ✅ ÉXITO: La página '{texto_pagina_inicial}' está seleccionada y resaltada con la clase '{clase_resaltado}'.")
                self.tomar_captura(f"{nombre_base}_pagina_inicial_seleccionada_ok", directorio)
                return True
            else:
                print(f"\n  ❌ FALLO: La página '{texto_pagina_inicial}' no tiene la clase de resaltado esperada '{clase_resaltado}'.")
                print(f"  Clases actuales del elemento: '{current_classes}'")
                self.tomar_captura(f"{nombre_base}_pagina_inicial_no_resaltada", directorio)
                return False

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): El contenedor de paginación '{selector_paginado}' "
                f"o la página inicial '{texto_pagina_inicial}' no estuvieron visibles a tiempo "
                f"(timeout de {timeout}ms).\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_timeout_paginacion", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error al interactuar con el componente de paginación.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise # Relanzar la excepción para que el framework de pruebas la maneje

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar la paginación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise # Relanzar la excepción
        
    #39- Función para navega a un número de página específico en un componente de paginación
    def navegar_y_verificar_pagina(self, selector_paginado, numero_pagina_a_navegar: str, nombre_base, directorio, clase_resaltado: str = "active", timeout: int = 10000, tiempo= 0.5) -> bool:
        print(f"\n--- Iniciando navegación a la página '{numero_pagina_a_navegar}' y verificación de resaltado ---")
        print(f"Contenedor de paginación locator: '{selector_paginado}'")
        self.tomar_captura(f"{nombre_base}_inicio_navegacion_pagina_{numero_pagina_a_navegar}", directorio)

        try:
            # Asegurarse de que el contenedor de paginación está visible
            expect(selector_paginado).to_be_visible(timeout=timeout)
            print("\nContenedor de paginación visible.")

            # --- 1. Obtener el número total de páginas y la página actual ---
            # Asumimos que los elementos de paginación son 'li' dentro del contenedor y que el último 'li'
            # visible (que no sea "Siguiente" o "Última") contiene el número de la última página.
            # Podrías necesitar ajustar este selector si tu HTML es diferente.
            todos_los_botones_pagina = selector_paginado.locator("li")
            num_botones = todos_los_botones_pagina.count()
            
            # Este locator debería apuntar al elemento que realmente tiene la clase 'active'
            # Basado en tu HTML/JS, la clase 'active' está en el <a>
            pagina_actual_locator = selector_paginado.locator(f"a.{clase_resaltado}").first
            # O si el <li> es el que está marcado, pero necesitas obtener el texto del <a> dentro
            # pagina_actual_locator = selector_contenedor_paginacion.locator(f"li.{clase_resaltado} a").first
            pagina_actual_texto = pagina_actual_locator.text_content().strip() if pagina_actual_locator.is_visible() else "Desconocida"
            print(f"\nPágina actualmente seleccionada: {pagina_actual_texto}")

            # Calcular el número total de páginas (puede requerir un ajuste si hay botones "Siguiente", "Anterior", etc.)
            total_paginas = 0
            if num_botones > 0:
                # Filtrar elementos que son solo números o el último elemento numérico
                for i in range(num_botones - 1, -1, -1): # Iterar al revés para encontrar el último número
                    btn = todos_los_botones_pagina.nth(i)
                    btn_text = btn.text_content().strip()
                    if btn_text.isdigit(): # Si el texto es un número
                        total_paginas = int(btn_text)
                        break
            
            print(f"\nNúmero total de páginas detectadas: {total_paginas}")

            # --- Condicional 1: Página a ir es mayor que el total de páginas ---
            if total_paginas > 0 and int(numero_pagina_a_navegar) > total_paginas:
                print(f"\n⚠️ ADVERTENCIA: La página de destino '{numero_pagina_a_navegar}' es mayor que el número total de páginas disponibles '{total_paginas}'.")
                self.tomar_captura(f"{nombre_base}_pagina_destino_fuera_rango", directorio)
                return False # Considerar esto como un fallo o una advertencia, dependiendo del caso de prueba.

            # --- Condicional 2: La página a ir es la misma en la que ya está ubicado ---
            if pagina_actual_texto == numero_pagina_a_navegar:
                print(f"\n⚠️ ADVERTENCIA: Ya estás en la página '{numero_pagina_a_navegar}'. No se requiere navegación.")
                # Opcional: Podrías verificar que siga resaltada.
                self.tomar_captura(f"{nombre_base}_pagina_destino_actual", directorio)
                return True # Considerar esto un éxito, ya que el estado es el esperado.

            # 1. Encontrar y hacer clic en el botón de la página deseada
            pagina_destino_locator = selector_paginado.locator(
                f"li:has-text('{numero_pagina_a_navegar}') a" # Ajusta este selector si es necesario
            ).first

            expect(pagina_destino_locator).to_be_visible(timeout=timeout)
            expect(pagina_destino_locator).to_be_enabled(timeout=timeout)
            print(f"\nElemento de la página '{numero_pagina_a_navegar}' encontrado y habilitado.")

            pagina_destino_locator.highlight()
            self.tomar_captura(f"{nombre_base}_pagina_a_navegar_encontrada", directorio)
            
            print(f"\nHaciendo clic en la página '{numero_pagina_a_navegar}'...")
            pagina_destino_locator.click()
            time.sleep(tiempo) # Pausa para permitir la carga de la página y la aplicación de estilos
            
            self.tomar_captura(f"{nombre_base}_pagina_{numero_pagina_a_navegar}_clic", directorio)

            # 2. Verificar que la página de destino se resalte
            print(f"\nVerificando si la página '{numero_pagina_a_navegar}' tiene la clase de resaltado '{clase_resaltado}'...")
            
            pagina_destino_locator.highlight() # Resaltar el elemento para la captura final

            current_classes = pagina_destino_locator.get_attribute("class")
            
            if current_classes and clase_resaltado in current_classes.split():
                print(f"\n  ✅ ÉXITO: La página '{numero_pagina_a_navegar}' está seleccionada y resaltada con la clase '{clase_resaltado}'.")
                self.tomar_captura(f"{nombre_base}_pagina_{numero_pagina_a_navegar}_seleccionada_ok", directorio)
                return True
            else:
                print(f"\n  ❌ FALLO: La página '{numero_pagina_a_navegar}' no tiene la clase de resaltado esperada '{clase_resaltado}'.")
                print(f"  Clases actuales del elemento: '{current_classes}'")
                self.tomar_captura(f"{nombre_base}_pagina_{numero_pagina_a_navegar}_no_resaltada", directorio)
                return False

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): El contenedor de paginación '{selector_paginado}' "
                f"o la página '{numero_pagina_a_navegar}' no estuvieron visibles/interactuables a tiempo "
                f"(timeout de {timeout}ms).\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_timeout_navegacion", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error al interactuar con el componente de paginación durante la navegación.\n"
                f"Posibles causas: Locator inválido, problemas de interacción con el DOM, elemento no clickable.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al navegar y verificar la paginación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
    
    # --- Manejadores y funciones para Alertas y Confirmaciones ---

    # Handler para alertas simples (usado con page.once)
    def _get_simple_alert_handler_for_on(self):
        def handler(dialog: Dialog):
            self._alerta_detectada = True
            self._alerta_mensaje_capturado = dialog.message
            self._alerta_tipo_capturado = dialog.type
            print(f"\n  --> [LISTENER ON - Simple Alert] Alerta detectada: Tipo='{dialog.type}', Mensaje='{dialog.message}'")
            dialog.accept() # Siempre acepta alertas simples
            print("  --> [LISTENER ON - Simple Alert] Alerta ACEPTADA.")
        return handler

    # Handler para diálogos de confirmación (usado con page.once)
    def _get_confirmation_dialog_handler_for_on(self, accion: str):
        def handler(dialog: Dialog):
            self._alerta_detectada = True
            self._alerta_mensaje_capturado = dialog.message
            self._alerta_tipo_capturado = dialog.type
            print(f"\n  --> [LISTENER ON - Dinámico] Confirmación detectada: Tipo='{dialog.type}', Mensaje='{dialog.message}'")
            if accion == 'accept':
                dialog.accept()
                print("  --> [LISTENER ON - Dinámico] Confirmación ACEPTADA.")
            elif accion == 'dismiss':
                dialog.dismiss()
                print("  --> [LISTENER ON - Dinámico] Confirmación CANCELADA.")
            else:
                print(f"  --> [LISTENER ON - Dinámico] Acción desconocida '{accion}'. Aceptando por defecto.")
                dialog.accept()
        return handler    
    
    # Handler para diálogos de pregunta (prompt) (usado con page.once)
    def _get_prompt_dialog_handler_for_on(self, input_text: str, accion: str):
        def handler(dialog: Dialog):
            self._alerta_detectada = True
            self._alerta_mensaje_capturado = dialog.message
            self._alerta_tipo_capturado = dialog.type
            self._alerta_input_capturado = input_text # Guarda el texto que se intentó introducir
            print(f"\n  --> [LISTENER ON - Prompt Dinámico] Diálogo detectado: Tipo='{dialog.type}', Mensaje='{dialog.message}'")

            if accion == 'accept':
                if dialog.type == "prompt":
                    # --- CORRECCIÓN AQUÍ ---
                    dialog.accept(input_text) # Pasa el texto directamente a accept()
                    print(f"  --> [LISTENER ON - Prompt Dinámico] Texto '{input_text}' introducido y prompt ACEPTADO.")
                else:
                    dialog.accept() # Para otros tipos de diálogo, solo aceptar sin texto
                    print("  --> [LISTENER ON - Prompt Dinámico] Diálogo ACEPTADO (sin texto, no es prompt).")
            elif accion == 'dismiss':
                dialog.dismiss()
                print("  --> [LISTENER ON - Prompt Dinámico] Diálogo CANCELADO.")
            else:
                print(f"  --> [LISTENER ON - Prompt Dinámico] Acción desconocida '{accion}'. Cancelando por defecto.")
                dialog.dismiss() # Por seguridad, cancelar si la acción es desconocida
        return handler

    # Handler de eventos para cuando se abre una nueva página.
    def _on_new_page(self, new_page: Page):
        print(f"\n✨ Nueva página detectada: URL = {new_page.url}, Título = {new_page.title()}")
        self._all_new_pages_opened_by_click.append(new_page)
        # Opcional: Si solo te interesa la primera popup o una específica, podrías manejarlo aquí.
        # Por ahora, solo la añadimos a la lista.
    
    #40- Función para verifica una alerta simple utilizando page.expect_event().
    def verificar_alerta_simple_con_expect_event(self, selector, mensaje_esperado: str, nombre_base, directorio, tiempo_espera= 5) -> bool:
        print(f"\n--- Ejecutando con expect_event (Alerta Simple): {nombre_base} ---")
        print(f"Verificando alerta al hacer clic en '{selector}'")
        print(f"  --> Mensaje de alerta esperado: '{mensaje_esperado}'")

        try:
            print(f"  --> Validando visibilidad y habilitación del botón '{selector}'...")
            expect(selector).to_be_visible(timeout=tiempo_espera * 1000)
            expect(selector).to_be_enabled(timeout=tiempo_espera * 1000)
            selector.highlight()
            time.sleep(0.5)

            print("  --> Preparando expect_event para la alerta y haciendo clic...")
            with self.page.expect_event("dialog", timeout=(tiempo_espera + 5) * 1000) as info_dialogo:
                print(f"  --> Haciendo clic en el botón '{selector}'...")
                selector.click(timeout=tiempo_espera * 1000) # Añadir timeout explícito al click

            dialogo = info_dialogo.value
            print(f"\n  --> Alerta detectada. Tipo: '{dialogo.type}', Mensaje: '{dialogo.message}'")

            if dialogo.type != "alert":
                dialogo.accept() # Aceptar para no bloquear si es un tipo inesperado
                raise ValueError(f"\n⚠️Tipo de diálogo inesperado: '{dialogo.type}'. Se esperaba 'alert'.")

            if mensaje_esperado not in dialogo.message:
                self.tomar_captura(f"{nombre_base}_alerta_mensaje_incorrecto", directorio)
                error_msg = (
                    f"\n❌ FALLO: Mensaje de alerta incorrecto.\n"
                    f"  --> Esperado: '{mensaje_esperado}'\n"
                    f"  --> Obtenido: '{dialogo.message}'"
                )
                print(error_msg)
                dialogo.accept() # Aceptar para no bloquear antes de fallar
                return False

            dialogo.accept()
            print("  ✅  --> Alerta ACEPTADA.")

            # Opcional: Verificar el resultado en la página después de la interacción
            # Si tu página muestra un mensaje después de aceptar la alerta, verifícalo aquí.
            # Por ejemplo: expect(self.page.locator("#some_result_element")).to_have_text("Alerta cerrada", timeout=2000)

            self.tomar_captura(f"{nombre_base}_alerta_exitosa", directorio)
            print(f"\n✅  --> ÉXITO: La alerta se mostró, mensaje verificado y aceptada correctamente.")
            time.sleep(0.5)
            return True

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Tiempo de espera excedido): La alerta no apareció después de {tiempo_espera} segundos "
                f"al hacer clic en '{selector}', o la verificación del resultado falló.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_alerta_NO_aparece_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al interactuar con el botón o la alerta.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Validación): Error en la validación de la alerta.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_validacion_alerta", directorio)
            return False

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar la alerta.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
    
    #41- Función para verifica una alerta simple utilizando page.on("dialog") con page.once().
    def verificar_alerta_simple_con_on(self, selector, mensaje_alerta_esperado: str, nombre_base, directorio, tiempo_espera= 5) -> bool:
        print(f"\n--- Ejecutando con page.on (Alerta Simple): {nombre_base} ---")
        print(f"Verificando alerta simple al hacer clic en el botón '{selector}'")
        print(f"  --> Mensaje de alerta esperado: '{mensaje_alerta_esperado}'")

        # Resetear el estado para cada ejecución del test
        self._alerta_detectada = False
        self._alerta_mensaje_capturado = ""
        self._alerta_tipo_capturado = ""

        try:
            # Validar que el botón es visible y habilitado antes de hacer clic
            print(f"  --> Validando visibilidad y habilitación del botón '{selector}'...")
            expect(selector).to_be_visible(timeout=tiempo_espera * 1000)
            expect(selector).to_be_enabled(timeout=tiempo_espera * 1000)
            selector.highlight()
            time.sleep(0.5)

            # === Registrar el listener ANTES de la acción ===
            print("  --> Registrando listener para la alerta con page.once()...")
            # Usa page.once para que el listener se desregistre automáticamente después de una vez.
            self.page.once("dialog", self._get_simple_alert_handler_for_on())

            # Hacer clic en el botón que dispara la alerta
            print(f"  --> Haciendo clic en el botón '{selector}'...")
            # Añadir un timeout explícito para el click
            selector.click(timeout=tiempo_espera * 1000)


            # Esperar a que el listener haya detectado y manejado la alerta
            print("  --> Esperando a que la alerta sea detectada y manejada por el listener...")
            start_time = time.time()
            while not self._alerta_detectada and (time.time() - start_time) * 1000 < (tiempo_espera * 1000 + 2000): # Añadir un poco más de margen
                time.sleep(0.1)

            if not self._alerta_detectada:
                raise TimeoutError(f"La alerta no fue detectada por el listener después de {tiempo_espera} segundos.")

            # Validaciones después de que el listener ha actuado
            if self._alerta_tipo_capturado != "alert":
                raise ValueError(f"\n⚠️Tipo de diálogo inesperado: '{self._alerta_tipo_capturado}'. Se esperaba 'alert'.")

            if mensaje_alerta_esperado not in self._alerta_mensaje_capturado:
                self.tomar_captura(f"{nombre_base}_alerta_mensaje_incorrecto", directorio)
                print(f"\n❌ FALLO: Mensaje de alerta incorrecto.\n  --> Esperado: '{mensaje_alerta_esperado}'\n  --> Obtenido: '{self._alerta_mensaje_capturado}'")
                return False

            # Opcional: Verificar que el elemento afectado por la alerta ha cambiado o desaparecido
            # En el caso de una alerta simple, a menudo no hay un cambio visible directo en la página,
            # pero si tu aplicación lo hace, deberías añadir una verificación aquí.
            # Por ejemplo, si un div muestra "Alerta cerrada":
            # expect(self.page.locator("#resultado_alerta")).to_have_text("Alerta cerrada", timeout=2000)

            self.tomar_captura(f"{nombre_base}_alerta_exitosa", directorio)
            print(f"\n✅  --> ÉXITO: La alerta se mostró, mensaje verificado y aceptada correctamente.")
            time.sleep(0.5)
            return True

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Tiempo de espera excedido): La alerta no apareció o no fue manejada después de {tiempo_espera} segundos "
                f"al hacer clic en '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_alerta_NO_aparece_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al interactuar con el botón o la alerta.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Validación): Error en la validación de la alerta.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_validacion_alerta", directorio)
            return False

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar la alerta.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #42- Función para verifica una alerta de confirmación utilizando page.expect_event(). Este método maneja el diálogo exclusivamente con expect_event.
    def verificar_confirmacion_expect_event(self, selector, mensaje_esperado: str, accion_confirmacion: str, nombre_base, directorio, tiempo_espera= 5) -> bool:
        print(f"\n--- Ejecutando con expect_event (Confirmación): {nombre_base} ---")
        print(f"Verificando confirmación al hacer clic en '{selector}' para '{accion_confirmacion}'")
        print(f"  --> Mensaje de confirmación esperado: '{mensaje_esperado}'")

        try:
            # Validar que el botón es visible y habilitado antes de hacer clic
            print(f"  --> Validando visibilidad y habilitación del botón '{selector}'...")
            expect(selector).to_be_visible(timeout=tiempo_espera * 1000)
            expect(selector).to_be_enabled(timeout=tiempo_espera * 1000)
            selector.highlight()
            time.sleep(0.5)

            # Usar 'with page.expect_event' para sincronizar el clic con la aparición del diálogo
            print("  --> Preparando expect_event para la confirmación y haciendo clic...")
            # Aumentar el timeout aquí para el evento de diálogo y el click
            with self.page.expect_event("dialog", timeout=(tiempo_espera + 10) * 1000) as info_dialogo: # Aumentado a 15 segundos (5+10)
                print(f"  --> Haciendo clic en el botón '{selector}'...")
                selector.click(timeout=(tiempo_espera + 5) * 1000) # Añadir timeout explícito al click (10s si tiempo_espera es 5)

            # Obtener el objeto Dialog una vez que el evento ocurre
            dialogo = info_dialogo.value
            print(f"\n  --> Confirmación detectada. Tipo: '{dialogo.type}', Mensaje: '{dialogo.message}'")

            # Verificar el tipo de diálogo
            if dialogo.type != "confirm":
                if accion_confirmacion == 'accept':
                    dialogo.accept()
                else:
                    dialogo.dismiss()
                raise ValueError(f"\n⚠️Tipo de diálogo inesperado: '{dialogo.type}'. Se esperaba 'confirm'.")

            # Verificar el mensaje de la alerta
            if mensaje_esperado not in dialogo.message:
                self.tomar_captura(f"{nombre_base}_confirmacion_mensaje_incorrecto", directorio)
                error_msg = (
                    f"\n❌ FALLO: Mensaje de confirmación incorrecto.\n"
                    f"  --> Esperado: '{mensaje_esperado}'\n"
                    f"  --> Obtenido: '{dialogo.message}'"
                )
                print(error_msg)
                if accion_confirmacion == 'accept':
                    dialogo.accept()
                else:
                    dialogo.dismiss()
                return False

            # Realizar la acción solicitada (Aceptar o Cancelar)
            if accion_confirmacion == 'accept':
                dialogo.accept()
                print("  ✅  --> Confirmación ACEPTADA.")
            elif accion_confirmacion == 'dismiss':
                dialogo.dismiss()
                print("  ✅  --> Confirmación CANCELADA.")
            else:
                raise ValueError(f"Acción de confirmación no válida: '{accion_confirmacion}'. Use 'accept' o 'dismiss'.")

            # Opcional: Verificar el resultado en la página después de la interacción
            if accion_confirmacion == 'accept':
                expect(self.page.locator("#demo")).to_have_text("You pressed OK!", timeout=5000) # Aumentar timeout para la verificación de texto
                print("  ✅  --> Resultado en página: 'You pressed OK!' verificado.")
            elif accion_confirmacion == 'dismiss':
                expect(self.page.locator("#demo")).to_have_text("You pressed Cancel!", timeout=5000) # Aumentar timeout para la verificación de texto
                print("  ✅  --> Resultado en página: 'You pressed Cancel!' verificado.")

            self.tomar_captura(f"{nombre_base}_confirmacion_exitosa_{accion_confirmacion}", directorio)
            print(f"\n✅  --> ÉXITO: La confirmación se mostró, mensaje verificado y '{accion_confirmacion}' correctamente.")
            time.sleep(0.5)
            return True

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Tiempo de espera excedido): La confirmación no apareció después de {tiempo_espera} segundos "
                f"al hacer clic en '{selector}', o la verificación del resultado falló.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_confirmacion_NO_aparece_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al interactuar con el botón o la confirmación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Validación): Error en la validación de la confirmación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_validacion_confirmacion", directorio)
            return False

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar la confirmación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #43- Función para verifica una alerta de confirmación utilizando page.on("dialog") con page.once().
    def verificar_confirmacion_on_dialog(self, selector, mensaje_esperado: str, accion_confirmacion: str, nombre_base, directorio, tiempo_espera= 5) -> bool:
        print(f"\n--- Ejecutando con page.on (Confirmación): {nombre_base} ---")
        print(f"Verificando confirmación al hacer clic en '{selector}' para '{accion_confirmacion}'")
        print(f"  --> Mensaje de confirmación esperado: '{mensaje_esperado}'")

        # Resetear el estado para cada ejecución del test
        self._alerta_detectada = False
        self._alerta_mensaje_capturado = ""
        self._alerta_tipo_capturado = ""

        try:
            # Validar que el botón es visible y habilitado antes de hacer clic
            print(f"  --> Validando visibilidad y habilitación del botón '{selector}'...")
            expect(selector).to_be_visible(timeout=tiempo_espera * 1000)
            expect(selector).to_be_enabled(timeout=tiempo_espera * 1000)
            selector.highlight()
            time.sleep(0.5)

            # Registrar el listener para la confirmación.
            print("  --> Registrando listener para la confirmación con page.once()...")
            self.page.once("dialog", self._get_confirmation_dialog_handler_for_on(accion_confirmacion))

            # Hacer clic en el botón
            print(f"  --> Haciendo clic en el botón '{selector}'...")
            selector.click(timeout=(tiempo_espera + 5) * 1000) # Añadir timeout explícito al click

            # Esperar a que el listener haya detectado y manejado la confirmación
            print("  --> Esperando a que la confirmación sea detectada y manejada por el listener...")
            start_time = time.time()
            # Aumentar el timeout de espera del loop para asegurar que el handler se dispara
            while not self._alerta_detectada and (time.time() - start_time) * 1000 < (tiempo_espera * 1000 + 5000):
                time.sleep(0.1)

            if not self._alerta_detectada:
                raise TimeoutError(f"La confirmación no fue detectada por el listener después de {tiempo_espera} segundos.")

            # Validaciones después de que el listener ha actuado
            if self._alerta_tipo_capturado != "confirm":
                raise ValueError(f"\n⚠️Tipo de diálogo inesperado: '{self._alerta_tipo_capturado}'. Se esperaba 'confirm'.")

            if mensaje_esperado not in self._alerta_mensaje_capturado:
                self.tomar_captura(f"{nombre_base}_confirmacion_mensaje_incorrecto", directorio)
                print(f"\n❌ FALLO: Mensaje de confirmación incorrecto.\n  --> Esperado: '{mensaje_esperado}'\n  --> Obtenido: '{self._alerta_mensaje_capturado}'")
                return False

            # Opcional: Verificar el resultado en la página después de la interacción
            if accion_confirmacion == 'accept':
                expect(self.page.locator("#demo")).to_have_text("You pressed OK!", timeout=5000)
                print("  ✅  --> Resultado en página: 'You pressed OK!' verificado.")
            elif accion_confirmacion == 'dismiss':
                expect(self.page.locator("#demo")).to_have_text("You pressed Cancel!", timeout=5000)
                print("  ✅  --> Resultado en página: 'You pressed Cancel!' verificado.")

            self.tomar_captura(f"{nombre_base}_confirmacion_exitosa_{accion_confirmacion}", directorio)
            print(f"\n✅  --> ÉXITO: La confirmación se mostró, mensaje verificado y '{accion_confirmacion}' correctamente.")
            time.sleep(0.5)
            return True

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Tiempo de espera excedido): La confirmación no apareció después de {tiempo_espera} segundos "
                f"al hacer clic en '{selector}', o la verificación del resultado falló.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_confirmacion_NO_aparece_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al interactuar con el botón o la confirmación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Validación): Error en la validación de la confirmación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_validacion_confirmacion", directorio)
            return False

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar la confirmación.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #44- Funció para verificar_prompt_expect_event (Implementación para Prompt Alert con expect_event)
    def verificar_prompt_expect_event(self, selector, mensaje_prompt_esperado: str, input_text: str, accion_prompt: str, nombre_base, directorio, tiempo_espera= 5) -> bool:
        print(f"\n--- Ejecutando con expect_event (Prompt Alert): {nombre_base} ---")
        print(f"Verificando prompt al hacer clic en '{selector}' para '{accion_prompt}'")
        print(f"  --> Mensaje del prompt esperado: '{mensaje_prompt_esperado}'")
        if accion_prompt == 'accept':
            print(f"  --> Texto a introducir: '{input_text}'")

        try:
            print(f"  --> Validando visibilidad y habilitación del botón '{selector}'...")
            expect(selector).to_be_visible(timeout=tiempo_espera * 1000)
            expect(selector).to_be_enabled(timeout=tiempo_espera * 1000)
            selector.highlight()
            time.sleep(0.5)

            print("  --> Preparando expect_event para el prompt y haciendo clic...")
            with self.page.expect_event("dialog", timeout=(tiempo_espera + 10) * 1000) as info_dialogo:
                print(f"  --> Haciendo clic en el botón '{selector}'...")
                selector.click(timeout=(tiempo_espera + 5) * 1000)

            dialogo = info_dialogo.value
            print(f"\n  --> Prompt detectado. Tipo: '{dialogo.type}', Mensaje: '{dialogo.message}'")

            # Verificar el tipo de diálogo
            if dialogo.type != "prompt":
                # Si el tipo es inesperado, intenta cerrarlo para no bloquear el test
                if accion_prompt == 'accept':
                    dialogo.accept()
                else:
                    dialogo.dismiss()
                raise ValueError(f"\n⚠️Tipo de diálogo inesperado: '{dialogo.type}'. Se esperaba 'prompt'.")

            # Verificar el mensaje del prompt
            if mensaje_prompt_esperado not in dialogo.message:
                self.tomar_captura(f"{nombre_base}_prompt_mensaje_incorrecto", directorio)
                error_msg = (
                    f"\n❌ FALLO: Mensaje del prompt incorrecto.\n"
                    f"  --> Esperado: '{mensaje_prompt_esperado}'\n"
                    f"  --> Obtenido: '{dialogo.message}'"
                )
                print(error_msg)
                # Intenta cerrar el diálogo antes de fallar
                if accion_prompt == 'accept':
                    dialogo.accept()
                else:
                    dialogo.dismiss()
                return False

            # Realizar la acción solicitada (Introducir texto y Aceptar, o Cancelar)
            if accion_prompt == 'accept':
                # --- CORRECCIÓN AQUÍ ---
                dialogo.accept(input_text) # Pasa el texto directamente a accept()
                print(f"  --> Texto '{input_text}' introducido en el prompt y aceptado.")
            elif accion_prompt == 'dismiss':
                dialogo.dismiss()
                print("  ✅  --> Prompt CANCELADO.")
            else:
                raise ValueError(f"Acción de prompt no válida: '{accion_prompt}'. Use 'accept' o 'dismiss'.")

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Tiempo de espera excedido): El prompt no apareció después de {tiempo_espera} segundos "
                f"al hacer clic en '{selector}', o la verificación del resultado falló.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_prompt_NO_aparece_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al interactuar con el botón o el prompt.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Validación): Error en la validación del prompt.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_validacion_prompt", directorio)
            return False

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar el prompt.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #45- Función para verifica una alerta de tipo 'prompt' utilizando page.on("dialog") con page.once().
    def verificar_prompt_on_dialog(self, selector, mensaje_prompt_esperado: str, input_text: str, accion_prompt: str, nombre_base, directorio, tiempo_espera= 5) -> bool:
        print(f"\n--- Ejecutando con page.on (Prompt Alert): {nombre_base} ---")
        print(f"Verificando prompt al hacer clic en '{selector}' para '{accion_prompt}'")
        print(f"  --> Mensaje del prompt esperado: '{mensaje_prompt_esperado}'")
        if accion_prompt == 'accept':
            print(f"  --> Texto a introducir: '{input_text}'")

        # Resetear el estado para cada ejecución del test
        self._alerta_detectada = False
        self._alerta_mensaje_capturado = ""
        self._alerta_tipo_capturado = ""
        self._alerta_input_capturado = "" # Resetear también el input capturado

        try:
            print(f"  --> Validando visibilidad y habilitación del botón '{selector}'...")
            expect(selector).to_be_visible(timeout=tiempo_espera * 1000)
            expect(selector).to_be_enabled(timeout=tiempo_espera * 1000)
            selector.highlight()
            time.sleep(0.5)

            # === Registrar el listener ANTES de la acción ===
            print("  --> Registrando listener para el prompt con page.once()...")
            # Usamos el handler corregido que pasa el input_text a dialog.accept()
            self.page.once("dialog", self._get_prompt_dialog_handler_for_on(input_text, accion_prompt))

            # Hacer clic en el botón que dispara el prompt
            print(f"  --> Haciendo clic en el botón '{selector}'...")
            selector.click(timeout=(tiempo_espera + 5) * 1000)

            # Esperar a que el listener haya detectado y manejado el prompt
            print("  --> Esperando a que el prompt sea detectado y manejado por el listener...")
            start_time = time.time()
            while not self._alerta_detectada and (time.time() - start_time) * 1000 < (tiempo_espera * 1000 + 5000):
                time.sleep(0.1)

            if not self._alerta_detectada:
                raise TimeoutError(f"El prompt no fue detectado por el listener después de {tiempo_espera} segundos.")

            # Validaciones después de que el listener ha actuado
            if self._alerta_tipo_capturado != "prompt":
                raise ValueError(f"\n⚠️Tipo de diálogo inesperado: '{self._alerta_tipo_capturado}'. Se esperaba 'prompt'.")

            if mensaje_prompt_esperado not in self._alerta_mensaje_capturado:
                self.tomar_captura(f"{nombre_base}_prompt_mensaje_incorrecto", directorio)
                print(f"\n❌ FALLO: Mensaje del prompt incorrecto.\n  --> Esperado: '{mensaje_prompt_esperado}'\n  --> Obtenido: '{self._alerta_mensaje_capturado}'")
                return False

            # Verificar que el texto introducido (si es el caso) se ha guardado correctamente
            if accion_prompt == 'accept' and self._alerta_input_capturado != input_text:
                self.tomar_captura(f"{nombre_base}_prompt_input_incorrecto", directorio)
                print(f"\n❌ FALLO: Texto introducido en el prompt incorrecto.\n  --> Esperado: '{input_text}'\n  --> Obtenido (capturado): '{self._alerta_input_capturado}'")
                return False

            # >>> Lógica para verificar el resultado en la página ELIMINADA de esta función <<<

            self.tomar_captura(f"{nombre_base}_prompt_exitosa_{accion_prompt}", directorio)
            print(f"\n✅  --> ÉXITO: El prompt se mostró, mensaje verificado y acción '{accion_prompt}' completada.")
            time.sleep(0.5)
            return True

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Tiempo de espera excedido): El prompt no apareció o no fue manejado después de {tiempo_espera} segundos "
                f"al hacer clic en '{selector}'.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_prompt_NO_aparece_timeout", directorio)
            return False

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright): Error de Playwright al interactuar con el botón o el prompt.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_playwright", directorio)
            raise

        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Validación): Error en la validación del prompt.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_validacion_prompt", directorio)
            return False

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al verificar el prompt.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado", directorio)
            raise
        
    #46- Función para espera por una nueva pestaña/página (popup) que se haya abierto y cambia el foco de la instancia 'page' actual a esa nueva pestaña.
    def abrir_y_cambiar_a_nueva_pestana(self, selector_boton_apertura, nombre_base, directorio, tiempo_espera=15) -> Page | None:
        print(f"\n🔄 Preparando para hacer clic y esperar nueva pestaña/popup. Esperando hasta {tiempo_espera} segundos...")

        nueva_pagina = None
        try:
            # Usar page.context.expect_event("page") para esperar la nueva página
            # y realizar la acción de click DENTRO de este contexto.
            # Esto asegura que la página capturada es la que se abre DESPUÉS del click.
            with self.page.context.expect_event("page", timeout=tiempo_espera * 1000) as event_info:
                # Realizar el clic en el botón que abre la nueva pestaña
                self.hacer_click_en_elemento(selector_boton_apertura, f"{nombre_base}_click_para_nueva_pestana", directorio, None)
            
            nueva_pagina = event_info.value # El objeto 'Page' de la nueva pestaña
            
            # Esperar a que la nueva página cargue completamente y el body sea visible
            nueva_pagina.wait_for_load_state()
            nueva_pagina.wait_for_selector("body", timeout=tiempo_espera * 1000)

            print(f"✅ Nueva pestaña abierta y detectada: URL = {nueva_pagina.url}, Título = {nueva_pagina.title}")
            
            # Actualizar self.page para que las subsiguientes operaciones usen la nueva página
            self.page = nueva_pagina 
            self.tomar_captura(f"{nombre_base}_nueva_pestana_abierta", directorio)
            
            return nueva_pagina

        except TimeoutError as e:
            error_msg = (
                f"\n❌ FALLO (Timeout): No se detectó ninguna nueva pestaña/página después de {tiempo_espera} segundos "
                f"al intentar hacer clic en el botón de apertura. Asegúrate de que el clic abre una nueva pestaña.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_no_se_detecto_popup_timeout", directorio)
            return None
        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error inesperado al intentar abrir y cambiar a la nueva pestaña.\\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado_abrir_pestana", directorio)
            raise

    #47- Función que cierra la pestaña actual y, si hay otras pestañas abiertas en el mismo contexto, cambia el foco a la primera pestaña disponible.
    def cerrar_pestana_actual(self, nombre_base, directorio, tiempo= 1):
        print(f"\n🚪 Cerrando la pestaña actual: URL = {self.page.url}")
        try:
            current_page_url = self.page.url # Guardar la URL antes de cerrar para el log
            
            # ¡IMPORTANTE! Tomar la captura *antes* de cerrar la página.
            # Cambié el sufijo para indicar que es antes del cierre.
            self.tomar_captura(f"{nombre_base}_antes_de_cerrar", directorio) 
            
            self.page.close()
            print(f"\n✅ Pestaña con URL '{current_page_url}' cerrada exitosamente.")
            
            time.sleep(tiempo) # Pequeña espera después de cerrar

            # Si hay otras páginas abiertas en el contexto, intenta cambiar a la primera disponible
            if self.page.context.pages:
                self.page = self.page.context.pages[0]
                print(f"\n🔄 Foco cambiado automáticamente a la primera pestaña disponible: URL = {self.page.url}")
                # Opcional: Podrías tomar otra captura aquí si quieres mostrar el estado de la nueva pestaña activa.
                # self.tomar_captura(f"{nombre_base}_foco_cambiado", directorio)
            else:
                print("\n⚠️ No hay más pestañas abiertas en el contexto del navegador. La instancia 'page' no apunta a ninguna página activa.")
                self.page = None # No hay página activa

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado): Ocurrió un error al intentar cerrar la pestaña actual.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            # NOTA: Si el error ya es 'Target page, context or browser has been closed',
            # intentar tomar otra captura con self.page.screenshot() aquí también fallará.
            # Por lo tanto, se recomienda NO intentar tomar una captura en el bloque de error
            # si el problema es que la página ya está cerrada.
            # self.tomar_captura(f"{nombre_base}_error_cerrar_pestana", directorio) # Eliminar o comentar esta línea si está aquí
            raise # Re-lanzar la excepción para que el test falle correctamente
        
    #48- Función para hacer clic en un selector y espera que se abran nuevas ventanas/pestañas.
    # Retorna una lista de objetos Page para las nuevas ventanas.
    def hacer_clic_y_abrir_nueva_ventana(self, selector, nombre_base, directorio, nombre_paso="", timeout=30000) -> List[Page]:
        print(f"\n{nombre_paso}: Haciendo clic en '{selector}' para abrir nuevas ventanas.")
        self.tomar_captura(f"{nombre_base}_antes_clic_nueva_ventana", directorio)
        
        # Limpiar la lista de páginas antes de la interacción para evitar acumulación
        self._all_new_pages_opened_by_click = []

        try:
            # Crea una tarea que espera por la nueva página antes de hacer el click.
            # Esto es crucial para Playwright: el "listener" debe estar activo ANTES de la acción.
            with self.page.context.expect_event("page", timeout=timeout) as page_info:
                selector.click() # Realiza el click que debería abrir una nueva ventana
            
            # La nueva página se añadió a _all_new_pages_opened_by_click por el _on_new_page handler.
            # Esperar a que la nueva(s) página(s) cargue(n) completamente
            for new_page in self._all_new_pages_opened_by_click:
                new_page.wait_for_load_state("load")
                new_page.wait_for_load_state("domcontentloaded")
                new_page.wait_for_load_state("networkidle")
                print(f"  --> Nueva página cargada: URL = {new_page.url}")
            
            self.tomar_captura(f"{nombre_base}_despues_clic_nueva_ventana", directorio)
            print(f"  ✅ Se han detectado y cargado {len(self._all_new_pages_opened_by_click)} nueva(s) ventana(s).")
            return self._all_new_pages_opened_by_click

        except TimeoutError:
            print(f"\n❌ FALLO: No se detectó ninguna nueva ventana después de hacer clic en '{selector}' dentro del tiempo de espera de {timeout/1000} segundos.")
            self.tomar_captura(f"{nombre_base}_no_nueva_ventana", directorio)
            return [] # Retorna una lista vacía si no se abre ninguna ventana

        except Exception as e:
            error_msg = f"\n❌ FALLO (Inesperado) - {nombre_paso}: Ocurrió un error al intentar abrir nueva ventana.\nDetalles: {e}"
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_abrir_nueva_ventana", directorio)
            raise # Re-lanzar la excepción para que el test falle correctamente

    #49- Función para cambia el foco del navegador a una ventana/pestaña específica,
    #ya sea por su índice (int) o por una parte de su URL o título (str).
    def cambiar_foco_entre_ventanas(self, nombre_base, directorio, opcion_ventana: Union[int, str], nombre_paso=""):
        print(f"\n{nombre_paso}: Intentando cambiar el foco a la ventana/pestaña: '{opcion_ventana}'")
        
        target_page_to_focus: Page = None
        
        try:
            # Obtener todas las páginas actuales en el contexto del navegador
            all_pages_in_context = self.page.context.pages
            print(f"Ventanas/pestañas abiertas actualmente: {len(all_pages_in_context)}")
            for i, p in enumerate(all_pages_in_context):
                print(f"  [{i}] URL: {p.url} | Título: {p.title()}")

            if isinstance(opcion_ventana, int):
                if 0 <= opcion_ventana < len(all_pages_in_context):
                    target_page_to_focus = all_pages_in_context[opcion_ventana]
                    print(f"  --> Seleccionada por índice: {opcion_ventana}")
                else:
                    error_msg = f"\n❌ FALLO: El índice '{opcion_ventana}' está fuera del rango de pestañas abiertas (0-{len(all_pages_in_context)-1})."
                    print(error_msg)
                    self.tomar_captura(f"{nombre_base}_error_indice_invalido", directorio)
                    raise IndexError(error_msg)
            elif isinstance(opcion_ventana, str):
                # Intentar encontrar por URL o título
                for p in all_pages_in_context:
                    if opcion_ventana in p.url or opcion_ventana in p.title():
                        target_page_to_focus = p
                        print(f"  --> Seleccionada por coincidencia de URL/Título: '{opcion_ventana}'")
                        break
                if not target_page_to_focus:
                    error_msg = f"\n❌ FALLO: No se encontró ninguna pestaña con la URL o título que contenga '{opcion_ventana}'."
                    print(error_msg)
                    self.tomar_captura(f"{nombre_base}_error_no_coincidencia_foco", directorio)
                    raise ValueError(error_msg)
            else:
                error_msg = f"\n❌ FALLO: El tipo de 'opcion_ventana' no es válido. Debe ser int o str."
                print(error_msg)
                self.tomar_captura(f"{nombre_base}_error_tipo_opcion_foco", directorio)
                raise TypeError(error_msg)

            # Si la página objetivo ya es la página actual, no es necesario cambiar
            if target_page_to_focus == self.page:
                print(f"\n✅ El foco ya está en la ventana seleccionada. No es necesario cambiar.")
            else:
                self.page = target_page_to_focus
                print(f"\n✅ Foco cambiado exitosamente a la ventana/pestaña seleccionada.")
            
            print(f"\n   URL de la pestaña actual: {self.page.url}")
            print(f"\n   Título de la pestaña actual: {self.page.title()}")
            self.tomar_captura(f"{nombre_base}_foco_cambiado", directorio)

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado) - {nombre_paso}: Ocurrió un error al intentar cambiar el foco de ventana.\\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_cambiar_foco_ventana", directorio)
            raise

    #50- Función que cierra una Page object específica.
    #Intenta cambiar el foco a la primera página disponible si la página cerrada era la actual.
    def cerrar_pestana_especifica(self, page_to_close: Page, nombre_base, directorio, nombre_paso=""):
        print(f"\n{nombre_paso}: Intentando cerrar la pestaña con URL: {page_to_close.url}")
        try:
            if not page_to_close.is_closed():
                is_current_page = (self.page == page_to_close)
                closed_url = page_to_close.url
                page_to_close.close()
                print(f"✅ Pestaña '{closed_url}' cerrada exitosamente.")
                self.tomar_captura(f"{nombre_base}_pestana_cerrada", directorio)
                
                # Si la página cerrada era la página actual (self.page), cambiar el foco
                if is_current_page:
                    print("\nDetectado: La pestaña cerrada era la pestaña activa.")
                    # Buscar la primera página disponible en el contexto
                    if self.page.context.pages:
                        self.page = self.page.context.pages[0]
                        print(f"🔄 Foco cambiado automáticamente a la primera pestaña disponible: URL = {self.page.url}")
                        self.tomar_captura(f"{nombre_base}_foco_cambiado_despues_cerrar", directorio)
                    else:
                        print("⚠️ No hay más pestañas abiertas en el contexto del navegador. La instancia 'page' no apunta a ninguna página activa.")
                        self.page = None # No hay página activa
            else:
                print(f"ℹ️ La pestaña con URL '{page_to_close.url}' ya estaba cerrada.")

        except Error as e: # Playwright-specific error
            # Esto puede ocurrir si la página ya se cerró por alguna razón externa.
            if "Target page, context or browser has been closed" in str(e):
                print(f"\n⚠️ Advertencia: La pestaña ya estaba cerrada o el contexto ya no es válido. Detalles: {e}")
            else:
                error_msg = (
                    f"\n❌ FALLO (Playwright Error) - {nombre_paso}: Ocurrió un error de Playwright al intentar cerrar la pestaña.\\n"
                    f"Detalles: {e}"
                )
                print(error_msg)
                self.tomar_captura(f"{nombre_base}_error_cerrar_pestana_playwright", directorio)
                raise
        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado) - {nombre_paso}: Ocurrió un error al intentar cerrar la pestaña.\\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_cerrar_pestana", directorio)
            raise
        
    #51- Función para realizar una operación de "Drag and Drop" de un elemento a otro.
    def realizar_drag_and_drop(self, elemento_origen, elemento_destino, nombre_base, directorio, nombre_paso: str = ""):
        print(f"\n{nombre_paso}: Intentando realizar 'Drag and Drop' de '{elemento_origen}' a '{elemento_destino}'")
        
        # Opcional: imprimir tipos para depuración (puedes eliminarlos en producción)
        # print(f"Tipo de elemento_origen: {type(elemento_origen)}")
        # print(f"Tipo de elemento_destino: {type(elemento_destino)}")

        # 1. Verificar que ambos elementos estén visibles y habilitados antes de interactuar (pre-verificación)
        try:
            if not elemento_origen.is_visible():
                raise ValueError(f"\n❌El elemento de origen '{elemento_origen}' no está visible.")
            if not elemento_origen.is_enabled():
                raise ValueError(f"\n❌El elemento de origen '{elemento_origen}' no está habilitado.")
            if not elemento_destino.is_visible():
                raise ValueError(f"\n❌El elemento de destino '{elemento_destino}' no está visible.")
            if not elemento_destino.is_enabled():
                raise ValueError(f"\n❌El elemento de destino '{elemento_destino}' no está habilitado.")
        except ValueError as e:
            error_msg = (
                f"\n❌ FALLO (Pre-validación) - {nombre_paso}: {e}\n"
                f"Asegúrese de que los elementos de origen y destino sean interactuables antes de intentar Drag and Drop."
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_pre_validacion_drag_and_drop", directorio)
            raise # Re-lanza la excepción si falla la validación inicial

        # --- Intento 1: Usar el método .drag_and_drop() ---
        try:
            print(f"\n🔄 Intentando 'Drag and Drop' con el método estándar de Playwright...")
            elemento_origen.drag_and_drop(elemento_destino)
            print(f"\n✅ 'Drag and Drop' realizado exitosamente con el método estándar.")
            self.tomar_captura(f"{nombre_base}_drag_and_drop_exitoso", directorio)
            return # Si funciona, salimos de la función

        except AttributeError as e:
            # Captura específicamente el AttributeError para intentar el método manual
            print(f"\n⚠️ Advertencia: El método directo '.drag_and_drop()' falló con AttributeError: {e}")
            print("\n🔄 Intentando 'Drag and Drop' con método manual de Playwright (mouse.hover, mouse.down, mouse.up)...")
            self.tomar_captura(f"{nombre_base}_fallo_directo_intentando_manual", directorio)
            self._realizar_drag_and_drop_manual(elemento_origen, elemento_destino, nombre_base, directorio, nombre_paso)
            print(f"\n✅ 'Drag and Drop' realizado exitosamente con el método manual.")

        except Error as e: # Otros errores específicos de Playwright para el método directo
            print(f"\n⚠️ Advertencia: El método directo '.drag_and_drop()' falló con error de Playwright: {e}")
            print("\n🔄 Intentando 'Drag and Drop' con método manual de Playwright (mouse.hover, mouse.down, mouse.up)...")
            self.tomar_captura(f"{nombre_base}_fallo_directo_intentando_manual", directorio)
            self._realizar_drag_and_drop_manual(elemento_origen, elemento_destino, nombre_base, directorio, nombre_paso)
            print(f"\n✅ 'Drag and Drop' realizado exitosamente con el método manual.")

        except Exception as e: # Cualquier otro error inesperado en el primer intento
            error_msg = (
                f"\n❌ FALLO (Inesperado - Intento 1) - {nombre_paso}: Ocurrió un error inesperado al intentar realizar 'Drag and Drop' con el método estándar.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado_intento1_drag_and_drop", directorio)
            raise # Si falla aquí, y no es el AttributeError, es un error más serio, lo re-lanzamos.

    def _realizar_drag_and_drop_manual(self, elemento_origen, elemento_destino, nombre_base, directorio, nombre_paso):
        """
        Método privado para realizar Drag and Drop usando las acciones de ratón de bajo nivel.
        Se llama como fallback si el método drag_and_drop() falla.
        """
        try:
            elemento_origen.hover() # Mueve el ratón sobre el elemento de origen
            self.page.mouse.down() # Presiona el botón izquierdo del ratón
            time.sleep(0.5) # Pequeña pausa para simular el arrastre visual
            elemento_destino.hover() # Mueve el ratón sobre el elemento de destino
            time.sleep(0.5) # Pequeña pausa antes de soltar
            self.page.mouse.up() # Suelta el botón izquierdo del ratón
            # No se necesita toma de captura aquí, ya se hizo al inicio del fallback
            # o se hará al final si todo el proceso es exitoso.

        except Error as e:
            error_msg = (
                f"\n❌ FALLO (Playwright Error - Manual) - {nombre_paso}: Ocurrió un error de Playwright al intentar realizar 'Drag and Drop' manualmente.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_manual_drag_and_drop_playwright", directorio)
            raise

        except Exception as e:
            error_msg = (
                f"\n❌ FALLO (Inesperado - Manual) - {nombre_paso}: Ocurrió un error inesperado al intentar realizar 'Drag and Drop' manualmente.\n"
                f"Detalles: {e}"
            )
            print(error_msg)
            self.tomar_captura(f"{nombre_base}_error_inesperado_manual_drag_and_drop", directorio)
            raise
        
    #52- Función para mover sliders de rango (con dos pulgares)
    def mover_slider_rango(self, pulgar_izquierdo_locator, pulgar_derecho_locator, barra_slider_locator,
                           porcentaje_destino_izquierdo: float, porcentaje_destino_derecho: float,
                           nombre_base, directorio, nombre_paso= ""):
        print(f"\n{nombre_paso}: Intentando mover el slider de rango. Pulgar Izquierdo a {porcentaje_destino_izquierdo*100:.0f}%, Pulgar Derecho a {porcentaje_destino_derecho*100:.0f}%")

        # Margen de error para la comparación de posiciones, en píxeles.
        # Un valor pequeño como 2 o 3 píxeles es razonable.
        TOLERANCIA_PIXELES = 3

        # 1. Validaciones iniciales de porcentajes
        if not (0.0 <= porcentaje_destino_izquierdo <= 1.0) or not (0.0 <= porcentaje_destino_derecho <= 1.0):
            raise ValueError("\n❌ Los porcentajes de destino para ambos pulgares deben ser valores flotantes entre 0.0 (0%) y 1.0 (100%).")
        
        # Validación de negocio: el porcentaje izquierdo no puede ser mayor que el derecho
        if porcentaje_destino_izquierdo > porcentaje_destino_derecho:
            raise ValueError("\n❌ El porcentaje del pulgar izquierdo no puede ser mayor que el del pulgar derecho.")

        localizadores = {
            "pulgar izquierdo": pulgar_izquierdo_locator,
            "pulgar derecho": pulgar_derecho_locator,
            "barra del slider": barra_slider_locator
        }

        try:
            barra_slider_locator.highlight() # Esto es para visualización en el navegador durante la ejecución
            
            # 2. Verificar visibilidad y habilitación de todos los elementos
            for nombre_elemento, localizador_elemento in localizadores.items():
                if not localizador_elemento.is_visible():
                    raise ValueError(f"\n❌ El elemento '{nombre_elemento}' ('{localizador_elemento.selector}') no está visible.")
                if not localizador_elemento.is_enabled():
                    raise ValueError(f"\n❌El elemento '{nombre_elemento}' ('{localizador_elemento.selector}') no está habilitado.")
            
            # Obtener el bounding box de la barra del slider (esencial para el cálculo)
            caja_barra = barra_slider_locator.bounding_box()
            if not caja_barra:
                raise RuntimeError(f"\n❌ No se pudo obtener el bounding box de la barra del slider '{barra_slider_locator.selector}'.")

            inicio_x_barra = caja_barra['x']
            ancho_barra = caja_barra['width']
            
            # --- Mover Pulgar Izquierdo (Mínimo) ---
            caja_pulgar_izquierdo = pulgar_izquierdo_locator.bounding_box()
            if not caja_pulgar_izquierdo:
                raise RuntimeError(f"\n❌ No se pudo obtener el bounding box del pulgar izquierdo '{pulgar_izquierdo_locator.selector}'.")

            posicion_x_destino_izquierdo = inicio_x_barra + (ancho_barra * porcentaje_destino_izquierdo)
            posicion_y_destino = caja_pulgar_izquierdo['y'] + (caja_pulgar_izquierdo['height'] / 2) # Y central del pulgar

            # Calcular la posición X central actual del pulgar izquierdo
            posicion_x_actual_izquierdo = caja_pulgar_izquierdo['x'] + (caja_pulgar_izquierdo['width'] / 2)

            # Verificar si el pulgar izquierdo ya está en la posición deseada
            if abs(posicion_x_actual_izquierdo - posicion_x_destino_izquierdo) < TOLERANCIA_PIXELES:
                print(f"\n  > Pulgar izquierdo ya se encuentra en la posición deseada ({porcentaje_destino_izquierdo*100:.0f}%). No se requiere movimiento.")
            else:
                print(f"\n  > Moviendo pulgar izquierdo de X={posicion_x_actual_izquierdo:.0f} a X={posicion_x_destino_izquierdo:.0f} ({porcentaje_destino_izquierdo*100:.0f}%)...")
                self.page.mouse.move(posicion_x_actual_izquierdo, posicion_y_destino) # Mover al centro del pulgar actual
                self.page.mouse.down() # Presionar
                time.sleep(0.2)
                self.page.mouse.move(posicion_x_destino_izquierdo, posicion_y_destino, steps=10) # Arrastrar
                time.sleep(0.2)
                self.page.mouse.up() # Soltar
                print(f"\n  > Pulgar izquierdo movido a X={posicion_x_destino_izquierdo:.0f}.")
            time.sleep(0.5) # Pausa adicional después de procesar el primer pulgar

            # --- Mover Pulgar Derecho (Máximo) ---
            caja_pulgar_derecho = pulgar_derecho_locator.bounding_box()
            if not caja_pulgar_derecho:
                raise RuntimeError(f"\n❌ No se pudo obtener el bounding box del pulgar derecho '{pulgar_derecho_locator.selector}'.")

            posicion_x_destino_derecho = inicio_x_barra + (ancho_barra * porcentaje_destino_derecho)
            posicion_y_destino_derecho = caja_pulgar_derecho['y'] + (caja_pulgar_derecho['height'] / 2) # Y central del pulgar

            # Calcular la posición X central actual del pulgar derecho
            posicion_x_actual_derecho = caja_pulgar_derecho['x'] + (caja_pulgar_derecho['width'] / 2)

            # Verificar si el pulgar derecho ya está en la posición deseada
            if abs(posicion_x_actual_derecho - posicion_x_destino_derecho) < TOLERANCIA_PIXELES:
                print(f"\n  > Pulgar derecho ya se encuentra en la posición deseada ({porcentaje_destino_derecho*100:.0f}%). No se requiere movimiento.")
            else:
                print(f"\n  > Moviendo pulgar derecho de X={posicion_x_actual_derecho:.0f} a X={posicion_x_destino_derecho:.0f} ({porcentaje_destino_derecho*100:.0f}%)...")
                # Siempre movemos el ratón a la posición actual del pulgar antes de "down" para asegurar el arrastre correcto
                self.page.mouse.move(posicion_x_actual_derecho, posicion_y_destino_derecho)
                self.page.mouse.down() # Presionar
                time.sleep(0.2)
                self.page.mouse.move(posicion_x_destino_derecho, posicion_y_destino_derecho, steps=10) # Arrastrar
                time.sleep(0.2)
                self.page.mouse.up() # Soltar
                print(f"\n  > Pulgar derecho movido a X={posicion_x_destino_derecho:.0f}.")

            print(f"\n✅ Slider de rango procesado exitosamente. Izquierdo a {porcentaje_destino_izquierdo*100:.0f}%, Derecho a {porcentaje_destino_derecho*100:.0f}%.")
            self.tomar_captura(f"{nombre_base}_slider_rango_procesado_{porcentaje_destino_izquierdo*100:.0f}_{porcentaje_destino_derecho*100:.0f}pc", directorio)

        except ValueError as e:
            mensaje_error = (
                f"\n❌ FALLO (Validación) - {nombre_paso}: {e}\n"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_error_validacion_slider_rango", directorio)
            raise

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright) - {nombre_paso}: Ocurrió un error de Playwright al intentar mover el slider de rango.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_error_playwright_slider_rango", directorio)
            raise

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Inesperado) - {nombre_paso}: Ocurrió un error inesperado al intentar mover el slider de rango.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_error_inesperado_slider_rango", directorio)
            raise
        
    #53- Función para seleccionar una opción en un ComboBox (elemento <select>) por su atributo 'value'.
    def seleccionar_opcion_por_valor(self, combobox_locator, valor_a_seleccionar, nombre_base, directorio):
        print (f"Seleccionando '{valor_a_seleccionar}' en ComboBox '{combobox_locator}'")

        try:
            # 1. Asegurarse de que el ComboBox esté visible y habilitado
            expect(combobox_locator).to_be_visible(timeout=5000) # Espera 5 segundos
            combobox_locator.highlight() # Para visualización durante la ejecución
            expect(combobox_locator).to_be_enabled(timeout=5000) # Espera 5 segundos
            
            # 2. Tomar captura antes de la selección
            self.tomar_captura(f"{nombre_base}_antes_de_seleccionar_combo", directorio)

            # 3. Seleccionar la opción por su valor
            # El método select_option() espera automáticamente a que el elemento
            # sea visible, habilitado y con la opción disponible.
            combobox_locator.select_option(valor_a_seleccionar)
            print(f"\n✅ Opción '{valor_a_seleccionar}' seleccionada exitosamente en '{combobox_locator}'.")

            # 4. Verificar que la opción fue seleccionada correctamente
            # Usamos to_have_value() para asegurar que el valor del select cambió al esperado
            expect(combobox_locator).to_have_value(valor_a_seleccionar, timeout=5000)
            print(f"\n✅ ComboBox '{combobox_locator}' verificado con valor '{valor_a_seleccionar}'.")

            # 5. Tomar captura después de la selección exitosa
            self.tomar_captura(f"{nombre_base}_despues_de_seleccionar_combo_exito", directorio)

        except TimeoutError as e:
            mensaje_error = (
                f"\n❌ FALLO (Timeout): El ComboBox '{combobox_locator}' "
                f"no se volvió visible/habilitado o la opción '{valor_a_seleccionar}' no se pudo seleccionar a tiempo.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_timeout_combo", directorio)
            raise AssertionError(f"\n❌ No se pudo seleccionar opción '{valor_a_seleccionar}' en ComboBox: {combobox_locator}") from e

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright): Ocurrió un error al intentar seleccionar la opción '{valor_a_seleccionar}' en '{combobox_locator}'.\n"
                f"Posibles causas: Selector inválido, elemento no es un <select>, opción no existe.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_playwright_error_combo", directorio)
            raise AssertionError(f"\n❌ Error de Playwright al seleccionar ComboBox: {combobox_locator}") from e

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al manejar el ComboBox '{combobox_locator}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_inesperado_combo", directorio)
            raise AssertionError(f"\n❌ Error inesperado con ComboBox: {combobox_locator}") from e
        
    #54- Función para seleccionar una opción en un ComboBox (elemento <select>) por su texto visible (label).
    def seleccionar_opcion_por_label(self, combobox_locator, label_a_seleccionar, nombre_base, directorio, tiempo= 1):
        # Si nombre_paso no se proporciona, usa el selector del locator para mayor claridad en el log
        print(f"Seleccionando '{label_a_seleccionar}' en ComboBox '{combobox_locator}' por label")

        try:
            # 1. Asegurarse de que el ComboBox esté visible y habilitado
            expect(combobox_locator).to_be_visible(timeout=5000) # Espera 5 segundos
            combobox_locator.highlight() # Para visualización durante la ejecución
            expect(combobox_locator).to_be_enabled(timeout=5000) # Espera 5 segundos
            
            # 2. Tomar captura antes de la selección
            self.tomar_captura(f"{nombre_base}_antes_de_seleccionar_combo_label", directorio)

            # 3. Seleccionar la opción por su texto visible (label)
            # El método select_option() espera automáticamente a que el elemento
            # sea visible, habilitado y con la opción disponible.
            combobox_locator.select_option(label_a_seleccionar)
            print(f"\n✅ Opción '{label_a_seleccionar}' seleccionada exitosamente en '{combobox_locator}' por label.")

            # 4. Verificar que la opción fue seleccionada correctamente
            # Usamos to_have_text() para asegurar que el texto visible del select cambió al esperado.
            # Ojo: to_have_text() verifica el texto del elemento <select> en sí, que a menudo
            # es el texto de la opción seleccionada. Si el ComboBox es complejo (no un <select> nativo),
            # podrías necesitar verificar el texto de un elemento adyacente que muestra la selección.
            expect(combobox_locator).to_have_text(label_a_seleccionar, timeout=5000)
            print(f"\n✅ ComboBox '{combobox_locator}' verificado con texto seleccionado '{label_a_seleccionar}'.")

            # 5. Tomar captura después de la selección exitosa
            self.tomar_captura(f"{nombre_base}_despues_de_seleccionar_combo_label_exito", directorio)

        except TimeoutError as e:
            mensaje_error = (
                f"\n❌ FALLO (Timeout): El ComboBox '{combobox_locator}' "
                f"no se volvió visible/habilitado o la opción '{label_a_seleccionar}' no se pudo seleccionar a tiempo.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_timeout_combo_label", directorio)
            raise AssertionError(f"\n❌ No se pudo seleccionar opción '{label_a_seleccionar}' en ComboBox por label: {combobox_locator}") from e

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright): Ocurrió un error al intentar seleccionar la opción '{label_a_seleccionar}' en '{combobox_locator}'.\n"
                f"Posibles causas: Selector inválido, elemento no es un <select>, opción con ese label no existe.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_playwright_error_combo_label", directorio)
            raise AssertionError(f"\n❌ Error de Playwright al seleccionar ComboBox por label: {combobox_locator}") from e

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al manejar el ComboBox '{combobox_locator}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_inesperado_combo_label", directorio)
            raise AssertionError(f"\n❌ Error inesperado con ComboBox por label: {combobox_locator}") from e
        
    #55- Función para presionar la tecla TAB en el teclado
    def Tab_Pess(self, tiempo= 0.5):
        self.page.keyboard.press("Tab")
        time.sleep(tiempo)
        
    #56- Función optimizada para seleccionar múltiples opciones en un ComboBox múltiple.
    def seleccionar_multiples_opciones_combo(self, combobox_multiple_locator, valores_a_seleccionar: list[str], nombre_base, directorio):
        print(f"\nSeleccionando múltiples opciones {valores_a_seleccionar} en ComboBox '{combobox_multiple_locator.selector}'")

        try:
            # 1. Asegurarse de que el ComboBox esté visible y habilitado
            expect(combobox_multiple_locator).to_be_visible(timeout=5000) # Espera 5 segundos
            combobox_multiple_locator.highlight() # Para visualización durante la ejecución
            expect(combobox_multiple_locator).to_be_enabled(timeout=5000) # Espera 5 segundos
            
            # Verificar que sea un select múltiple, si es crítico
            # Opcional: Esto puede no ser necesario si tu locator ya apunta específicamente a un 'select[multiple]'
            # expect(combobox_multiple_locator).to_have_attribute("multiple", "") 
            # print("  > ComboBox verificado como select múltiple.")

            # 2. Tomar captura antes de la selección
            self.tomar_captura(f"{nombre_base}_antes_de_seleccionar_multi_combo", directorio)

            # 3. Seleccionar las opciones
            # Playwright's select_option() para listas maneja tanto valores como labels.
            # Pasando una lista de strings seleccionará las opciones correspondientes.
            combobox_multiple_locator.select_option(valores_a_seleccionar)
            print(f"\n✅ Opciones '{valores_a_seleccionar}' seleccionadas exitosamente en '{combobox_multiple_locator}'.")

            # 4. Verificar que las opciones fueron seleccionadas correctamente
            # input_value() para un select múltiple retorna una lista de los valores seleccionados.
            expect(combobox_multiple_locator).to_have_values(valores_a_seleccionar, timeout=5000)
            print(f"\n✅ ComboBox '{combobox_multiple_locator}' verificado con valores seleccionados: {valores_a_seleccionar}.")

            # 5. Tomar captura después de la selección exitosa
            self.tomar_captura(f"{nombre_base}_despues_de_seleccionar_multi_combo_exito", directorio)

        except TimeoutError as e:
            mensaje_error = (
                f"\n❌ FALLO (Timeout): El ComboBox múltiple '{combobox_multiple_locator}' "
                f"no se volvió visible/habilitado o las opciones '{valores_a_seleccionar}' no se pudieron seleccionar a tiempo.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_timeout_multi_combo", directorio)
            raise AssertionError(f"\nNo se pudieron seleccionar opciones '{valores_a_seleccionar}' en ComboBox múltiple: {combobox_multiple_locator}") from e

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright): Ocurrió un error al intentar seleccionar las opciones '{valores_a_seleccionar}' en '{combobox_multiple_locator}'.\n"
                f"Posibles causas: Selector inválido, elemento no es un <select multiple>, alguna opción no existe.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_playwright_error_multi_combo", directorio)
            raise AssertionError(f"\n ❌Error de Playwright al seleccionar ComboBox múltiple: {combobox_multiple_locator}") from e

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al manejar el ComboBox múltiple '{combobox_multiple_locator}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_fallo_inesperado_multi_combo", directorio)
            raise AssertionError(f"\n❌ Error inesperado con ComboBox múltiple: {combobox_multiple_locator}") from e
        
    #57 Función que obtiene y imprime los valores y el texto de todas las opciones en un dropdown list.
    def obtener_valores_dropdown(self, selector_dropdown, nombre_base, directorio, timeout_ms: int = 5000) -> List[Dict[str, str]] | None:
        print(f"\n--- Extrayendo valores del dropdown '{selector_dropdown}' ---")
        valores_opciones: List[Dict[str, str]] = []

        try:
            # 1. Asegurar que el dropdown es visible y habilitado
            selector_dropdown.highlight()
            self.tomar_captura(f"{nombre_base}_dropdown_antes_extraccion", directorio)

            print(f"\n⏳ Esperando que el dropdown '{selector_dropdown}' sea visible y habilitado...")
            expect(selector_dropdown).to_be_visible(timeout=timeout_ms)
            expect(selector_dropdown).to_be_enabled(timeout=timeout_ms)
            print(f"\n✅ Dropdown '{selector_dropdown}' es visible y habilitado.")

            # 2. Obtener todas las opciones dentro del dropdown
            # Usamos `all()` para obtener una lista de locators para cada opción
            option_locators = selector_dropdown.locator("option").all()

            if not option_locators:
                print(f"\n⚠️ No se encontraron opciones dentro del dropdown '{selector_dropdown}'.")
                self.tomar_captura(f"{nombre_base}_dropdown_sin_opciones", directorio)
                return None

            print(f"\nEncontradas {len(option_locators)} opciones para '{selector_dropdown}':")

            # 3. Iterar sobre cada opción y extraer su 'value' y 'text_content'
            for i, option_locator in enumerate(option_locators):
                value = option_locator.get_attribute("value")
                text = option_locator.text_content()

                # Limpieza de espacios en blanco
                clean_value = value.strip() if value else ""
                clean_text = text.strip() if text else ""

                valores_opciones.append({'value': clean_value, 'text': clean_text})
                print(f"  Option {i+1}: Value='{clean_value}', Text='{clean_text}'")

            print(f"\n✅ Valores obtenidos exitosamente del dropdown '{selector_dropdown}'.")
            self.tomar_captura(f"{nombre_base}_dropdown_valores_extraidos", directorio)
            return valores_opciones

        except TimeoutError as e:
            mensaje_error = (
                f"\n❌ FALLO (Timeout): El dropdown '{selector_dropdown}' "
                f"no se volvió visible/habilitado o sus opciones no cargaron a tiempo.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_dropdown_fallo_timeout", directorio)
            raise AssertionError(f"\nDropdown no disponible: {selector_dropdown}") from e

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright): Ocurrió un error de Playwright al intentar obtener los valores del dropdown '{selector_dropdown}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_dropdown_fallo_playwright_error", directorio)
            raise AssertionError(f"\nError de Playwright al extraer valores del dropdown: {selector_dropdown}") from e

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al intentar obtener los valores del dropdown '{selector_dropdown}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_dropdown_fallo_inesperado", directorio)
            raise AssertionError(f"\nError inesperado al extraer valores del dropdown: {selector_dropdown}") from e
        
    #58- Función que obtiene y imprime los valores y el texto de todas las opciones en un dropdown list.
    #Opcionalmente, compara las opciones obtenidas con una lista de opciones esperadas.
    def obtener_y_comparar_valores_dropdown(self, dropdown_locator, nombre_base, directorio, expected_options: List[Union[str, Dict[str, str]]] = None, compare_by_text: bool = True, compare_by_value: bool = False, timeout_ms: int = 5000) -> List[Dict[str, str]] | None:
        """
        Args:
            dropdown_locator (Locator): El objeto Locator de Playwright para el elemento <select> del dropdown.
            nombre_base (str): Nombre base para las capturas de pantalla.
            directorio (str): Directorio donde se guardarán las capturas de pantalla.
            expected_options (List[Union[str, Dict[str, str]]], optional):
                Lista de opciones esperadas para la comparación. Puede ser:
                - List[str]: Si solo quieres comparar por el texto visible de las opciones.
                - List[Dict[str, str]]: Si quieres comparar por 'value' y 'text'.
                  Ej: [{'value': 'usa', 'text': 'Estados Unidos'}].
                Por defecto es None (no se realiza comparación).
            compare_by_text (bool): Si es True, compara el texto visible de las opciones.
                                    Usado si expected_options es List[str] o List[Dict].
            compare_by_value (bool): Si es True, compara el atributo 'value' de las opciones.
                                     Usado si expected_options es List[Dict].
            timeout_ms (int): Tiempo máximo de espera en milisegundos.

        Returns:
            List[Dict[str, str]] | None: Una lista de diccionarios con las opciones reales.
            Retorna None si ocurre un error o no se encuentran opciones.
            La función generará una AssertionError si la comparación falla.
        """
        print(f"\n--- Extrayendo y comparando valores del dropdown '{dropdown_locator}' ---")
        valores_opciones_reales: List[Dict[str, str]] = []

        try:
            # 1. Asegurar que el dropdown es visible y habilitado
            dropdown_locator.highlight()
            self.tomar_captura(f"{nombre_base}_dropdown_antes_extraccion_y_comparacion", directorio)

            print(f"\n⏳ Esperando que el dropdown '{dropdown_locator}' sea visible y habilitado...")
            expect(dropdown_locator).to_be_visible(timeout=timeout_ms)
            expect(dropdown_locator).to_be_enabled(timeout=timeout_ms)
            print(f"\n✅ Dropdown '{dropdown_locator}' es visible y habilitado.")

            # 2. Obtener todas las opciones dentro del dropdown
            option_locators = dropdown_locator.locator("option").all()

            if not option_locators:
                print(f"\n⚠️ No se encontraron opciones dentro del dropdown '{dropdown_locator}'.")
                self.tomar_captura(f"{nombre_base}_dropdown_sin_opciones", directorio)
                # Si se esperaban opciones y no hay ninguna, esto es un fallo
                if expected_options:
                    raise AssertionError(f"FALLO: No se encontraron opciones en el dropdown '{dropdown_locator}', pero se esperaban {len(expected_options)}.")
                return None

            print(f"Encontradas {len(option_locators)} opciones reales para '{dropdown_locator}':")

            # 3. Iterar sobre cada opción y extraer su 'value' y 'text_content'
            for i, option_locator in enumerate(option_locators):
                value = option_locator.get_attribute("value")
                text = option_locator.text_content()

                clean_value = value.strip() if value else ""
                clean_text = text.strip() if text else ""

                valores_opciones_reales.append({'value': clean_value, 'text': clean_text})
                print(f"  Opción Real {i+1}: Value='{clean_value}', Text='{clean_text}'")

            print(f"\n✅ Valores obtenidos exitosamente del dropdown '{dropdown_locator}'.")
            self.tomar_captura(f"{nombre_base}_dropdown_valores_extraidos", directorio)

            # 4. Comparar con las opciones esperadas (si se proporcionan)
            if expected_options is not None:
                print("\n--- Realizando comparación de opciones ---")
                try:
                    expected_set = set()
                    real_set = set()

                    # Preparar los conjuntos para la comparación
                    for opt in expected_options:
                        if isinstance(opt, str):
                            if compare_by_text:
                                expected_set.add(opt.strip().lower()) # Normalizar para comparación
                        elif isinstance(opt, dict):
                            if compare_by_text and 'text' in opt:
                                expected_set.add(opt['text'].strip().lower())
                            if compare_by_value and 'value' in opt:
                                expected_set.add(opt['value'].strip().lower())
                        else:
                            print(f"⚠️ Advertencia: Formato de opción esperada no reconocido: {opt}. Ignorando.")

                    for opt_real in valores_opciones_reales:
                        if compare_by_text:
                            real_set.add(opt_real['text'].strip().lower())
                        if compare_by_value:
                            real_set.add(opt_real['value'].strip().lower())

                    # Comprobar si los conjuntos son idénticos
                    if expected_set == real_set:
                        print("\n✅ ÉXITO: Las opciones del dropdown coinciden con las opciones esperadas.")
                        self.tomar_captura(f"{nombre_base}_dropdown_comparacion_exitosa", directorio)
                    else:
                        missing_in_real = list(expected_set - real_set)
                        missing_in_expected = list(real_set - expected_set)
                        error_msg = f"❌ FALLO: Las opciones del dropdown NO coinciden con las esperadas.\n"
                        if missing_in_real:
                            error_msg += f"  - Opciones esperadas no encontradas en el dropdown: {missing_in_real}\n"
                        if missing_in_expected:
                            error_msg += f"  - Opciones encontradas en el dropdown que no estaban esperadas: {missing_in_expected}\n"
                        print(error_msg)
                        self.tomar_captura(f"{nombre_base}_dropdown_comparacion_fallida", directorio)
                        raise AssertionError(f"Comparación de opciones del dropdown fallida para '{dropdown_locator}'. {error_msg.strip()}")

                except Exception as e:
                    print(f"❌ FALLO: Ocurrió un error durante la comparación de opciones: {e}")
                    self.tomar_captura(f"{nombre_base}_dropdown_error_comparacion", directorio)
                    raise AssertionError(f"Error al comparar opciones del dropdown '{dropdown_locator}': {e}") from e

            return valores_opciones_reales

        except TimeoutError as e:
            mensaje_error = (
                f"\n❌ FALLO (Timeout): El dropdown '{dropdown_locator}' " # Usar dropdown_locator directamente
                f"no se volvió visible/habilitado o sus opciones no cargaron a tiempo.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_dropdown_fallo_timeout", directorio)
            raise AssertionError(f"\nDropdown no disponible: {dropdown_locator}") from e

        except Error as e:
            mensaje_error = (
                f"\n❌ FALLO (Error de Playwright): Ocurrió un error de Playwright al intentar obtener los valores del dropdown '{dropdown_locator}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_dropdown_fallo_playwright_error", directorio)
            raise AssertionError(f"\nError de Playwright al extraer valores del dropdown: {dropdown_locator}") from e

        except Exception as e:
            mensaje_error = (
                f"\n❌ FALLO (Error Inesperado): Ocurrió un error desconocido al intentar obtener los valores del dropdown '{dropdown_locator}'.\n"
                f"Detalles: {e}"
            )
            print(mensaje_error)
            self.tomar_captura(f"{nombre_base}_dropdown_fallo_inesperado", directorio)
            raise AssertionError(f"\nError inesperado al extraer valores del dropdown: {dropdown_locator}") from e