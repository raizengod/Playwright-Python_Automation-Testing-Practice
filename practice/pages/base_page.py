import re
import time
from playwright.sync_api import Page, expect, Error , TimeoutError, sync_playwright, Response 
from datetime import datetime
import os

class Funciones_Globales:
    
    #1- Creamos una función incial 'Constructor'-----ES IMPORTANTE TENER ESTE INICIADOR-----
    def __init__(self, page):
        self.page= page
        
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

            # 3. Verificar que el checkbox está marcado después de la acción
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
        
    #30- Función para Extrae y retorna el valor de un elemento dado su selector.
    def obtener_valor_elemento(self, selector, nombre_base, directorio, tiempo= 0.5) -> str | None:
        print(f"\nExtrayendo valor del elemento '{selector}'")
        try:
            selector.highlight()
            self.tomar_captura(f"{nombre_base}_antes_extraccion_valor", directorio)

            valor_extraido = None

            # Intentar obtener el valor de diferentes maneras
            try:
                # 1. Intentar obtener el 'value' si es un campo de entrada
                valor_extraido = selector.input_value(timeout=1000)
                print(f"\n✅ Valor extraído (input_value) de '{selector}': '{valor_extraido}'")
            except Exception:
                # 2. Si no es un campo de entrada, intentar obtener el 'textContent'
                try:
                    valor_extraido = selector.text_content(timeout=1000)
                    print(f"\n✅ Valor extraído (text_content) de '{selector}': '{valor_extraido}'")
                except Exception:
                    # 3. Si text_content falla, intentar obtener el 'innerText'
                    try:
                        valor_extraido = selector.inner_text(timeout=1000)
                        print(f"\n✅ Valor extraído (inner_text) de '{selector}': '{valor_extraido}'")
                    except Exception:
                        # 4. Finalmente, intentar obtener un atributo común como 'title' o 'alt'
                        # Esto es más general y puede requerir especificar el atributo.
                        # Para esta función, nos centraremos en texto o valor de input.
                        print(f"\n⚠️ No se pudo obtener el valor como input_value, text_content o inner_text para '{selector}'.")

            if valor_extraido is not None:
                print(f"\n✅ Se obtuvo el valor del elemento '{selector}': '{valor_extraido}'")
                time.sleep(tiempo)
                return valor_extraido.strip() if isinstance(valor_extraido, str) else valor_extraido
            else:
                print(f"\n❌ No se pudo extraer ningún valor significativo del elemento '{selector}'.")
                self.tomar_captura(f"{nombre_base}_fallo_extraccion_valor_no_encontrado", directorio)
                time.sleep(tiempo)
                return None

        except Exception as e:
            print(f"\n❌ Error al intentar extraer el valor del elemento '{selector}': {e}")
            self.tomar_captura(f"{nombre_base}_error_extraccion_valor", directorio)
            # Dependiendo de la política de tu framework, puedes relanzar la excepción
            # o retornar None para indicar que la operación falló.
            # raise # Descomentar para relanzar la excepción
            return None