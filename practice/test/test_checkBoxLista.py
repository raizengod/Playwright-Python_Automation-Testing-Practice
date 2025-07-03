import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_checkBoxLista import CheckBoxListaLocatorsPage
from practice.utils import config

def test_verificar_encabezado_tabla(set_up_checkBoxLista):
    page= set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.verificar_encabezados_tabla(cbl.tablaCheck,["ID", "Name", "Price", "Select"], "verificar_encabezados_tabla_check", config.SCREENSHOT_DIR)
    
def test_verificar_datos_de_tabla(set_up_checkBoxLista):
    page= set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    datos_esperados = [
        {"ID": "1", "Name": "Smartphone", "Price": "$10.99", "Select": False}, # Asumiendo checkbox desmarcado
        {"ID": "2", "Name": "Laptop", "Price": "$19.99", "Select": False},  
        {"ID": "3", "Name": "Tablet ", "Price": "$5.99", "Select": False},
        {"ID": "4", "Name": "Smartwatch", "Price": "$7.99", "Select": False},
        {"ID": "5", "Name": "Wireless Earbuds", "Price": "$8.99", "Select": False}
    ]
    
    fg.verificar_datos_filas_tabla(cbl.tablaCheck, datos_esperados, "verificar_datos_filas_tabla_check", config.SCREENSHOT_DIR)
    
def test_interactuar_con_check_aleatorio_tabla(set_up_checkBoxLista):
    page= set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.seleccionar_y_verificar_checkboxes_aleatorios(cbl.tablaCheck, 2, "seleccionar_y_verificar_checkboxes_aleatorios_tabla_check", config.SCREENSHOT_DIR)
    
def test_desmarcar_checkbox_seleccionados(set_up_checkBoxLista):
    page= set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.deseleccionar_y_verificar_checkbox_marcado_aleatorio(cbl.tablaCheck, "deseleccionar_y_verificar_checkbox_marcado_aleatorio_tabla_check", config.SCREENSHOT_DIR)
    
def test_interactuar_con_check_consecutivos_tabla(set_up_checkBoxLista):
    page = set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    #Definiendo el índice de inicio y cuántos checkboxes consecutivos interactuar
    indice_inicio = 1 # Por ejemplo, empezar desde la segunda fila (índice 1)
    cantidad_a_seleccionar = 3 # Seleccionar 2 checkboxes consecutivos (Producto 2 y Producto 3 si existen)

    fg.seleccionar_y_verificar_checkboxes_consecutivos(cbl.tablaCheck, indice_inicio, cantidad_a_seleccionar, "seleccionar_y_verificar_checkboxes_consecutivos_tabla_Check", config.SCREENSHOT_DIR)
    fg.deseleccionar_y_verificar_checkbox_marcado_aleatorio(cbl.tablaCheck, "deseleccionar_y_verificar_checkbox_marcado_aleatorio_tabla_check", config.SCREENSHOT_DIR)
    
def test_buscar_dato_y_marcar_checkBox(set_up_checkBoxLista):
    page= set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.seleccionar_checkbox_por_contenido_celda(cbl.tablaCheck, "s", "seleccionar_checkbox_por_contenido_celda_tabla_check", config.SCREENSHOT_DIR)
    fg.deseleccionar_y_verificar_checkbox_marcado_aleatorio(cbl.tablaCheck, "deseleccionar_y_verificar_checkbox_marcado_aleatorio_tabla_check", config.SCREENSHOT_DIR)
    
def test_verificar_paginado_inicial_y_resaltado(set_up_checkBoxLista):
    page = set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.verificar_pagina_inicial_seleccionada(cbl.contenedorPaginado, "1", "verificar_pagina_inicial_seleccionada_contenedor_paginado", config.SCREENSHOT_DIR)
    
def test_cambio_de_pagina(set_up_checkBoxLista):
    page = set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "3", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "3", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "5", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "4", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "2", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "1", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    
def test_cambiar_pagina_y_activar_checkBox(set_up_checkBoxLista):
    page = set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    fg.verificar_pagina_inicial_seleccionada(cbl.contenedorPaginado, "1", "verificar_pagina_inicial_seleccionada_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.seleccionar_checkbox_por_contenido_celda(cbl.tablaCheck, "u", "seleccionar_checkbox_por_contenido_celda_tabla_check", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "2", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.seleccionar_checkbox_por_contenido_celda(cbl.tablaCheck, "u", "seleccionar_checkbox_por_contenido_celda_tabla_check", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "3", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.seleccionar_checkbox_por_contenido_celda(cbl.tablaCheck, "u", "seleccionar_checkbox_por_contenido_celda_tabla_check", config.SCREENSHOT_DIR)
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "4", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.seleccionar_checkbox_por_contenido_celda(cbl.tablaCheck, "u", "seleccionar_checkbox_por_contenido_celda_tabla_check", config.SCREENSHOT_DIR)

@pytest.mark.xfail(reason= "Los checkBox no mantienen el estado marcado previamente cuando se cambia entre número de páginas")    
def test_cambiar_pagina_y_ver_checkBox_activos_previamente(set_up_checkBoxLista):
    page = set_up_checkBoxLista
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo base_page
    #IMPORTANTE: Creamos un objeto de tipo función 'CheckBoxListaLocatorsPage'
    cbl= CheckBoxListaLocatorsPage(page)
    
    # Navegar y verificar página 1
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "1", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.verificar_pagina_inicial_seleccionada(cbl.contenedorPaginado, "1", "verificar_pagina_inicial_seleccionada_contenedor_paginado", config.SCREENSHOT_DIR)
    datos_esperados1 = [
        {"ID": "1", "Name": "Smartphone", "Price": "$10.99", "Select": False}, # Asumiendo checkbox desmarcado
        {"ID": "2", "Name": "Laptop", "Price": "$19.99", "Select": False},  
        {"ID": "3", "Name": "Tablet ", "Price": "$5.99", "Select": False},
        {"ID": "4", "Name": "Smartwatch", "Price": "$7.99", "Select": False},
        {"ID": "5", "Name": "Wireless Earbuds", "Price": "$8.99", "Select": True}
    ]
    datos_ok_1 = fg.verificar_datos_filas_tabla(cbl.tablaCheck, datos_esperados1, "verificar_datos_filas_tabla_check_pagina1", config.SCREENSHOT_DIR)
    assert datos_ok_1 is True, "Los datos de la tabla en la Página 1 no coinciden con los esperados."
    
    # Navegar y verificar página 2
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "2", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.verificar_pagina_inicial_seleccionada(cbl.contenedorPaginado, "2", "verificar_pagina_inicial_seleccionada_contenedor_paginado", config.SCREENSHOT_DIR)
    datos_esperados2 = [
        {"ID": "6", "Name": "Bluetooth Speaker", "Price": "$9.99", "Select": True},
        {"ID": "7", "Name": "Television", "Price": "2$0.99", "Select": False},
        {"ID": "8", "Name": "Action Camera", "Price": "$15.99", "Select": False},
        {"ID": "9", "Name": "Gaming Console", "Price": "$5.99", "Select": False},
        {"ID": "10", "Name": "Digital Camera", "Price": "$16.99", "Select": False}
    ]
    datos_ok_2 = fg.verificar_datos_filas_tabla(cbl.tablaCheck, datos_esperados2, "verificar_datos_filas_tabla_check_pagina2", config.SCREENSHOT_DIR)
    assert datos_ok_2 is True, "Los datos de la tabla en la Página 2 no coinciden con los esperados."
    
    # Navegar y verificar página 3
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "3", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.verificar_pagina_inicial_seleccionada(cbl.contenedorPaginado, "3", "verificar_pagina_inicial_seleccionada_contenedor_paginado", config.SCREENSHOT_DIR)
    datos_esperados3 = [
        {"ID": "11", "Name": "Smart Home Hub", "Price": "$20.99", "Select": True},
        {"ID": "12", "Name": "Router", "Price": "$24.99", "Select": True},
        {"ID": "13", "Name": "Portable Charger", "Price": "$30.99", "Select": False},
        {"ID": "14", "Name": "Fitness Tracker", "Price": "$19.99", "Select": False},
        {"ID": "15", "Name": "Desktop Computer", "Price": "$2.99", "Select": True}
    ]
    datos_ok_3 = fg.verificar_datos_filas_tabla(cbl.tablaCheck, datos_esperados3, "verificar_datos_filas_tabla_check_pagina3", config.SCREENSHOT_DIR)
    assert datos_ok_3 is True, "Los datos de la tabla en la Página 3 no coinciden con los esperados."
    
    # Navegar y verificar página 4
    fg.navegar_y_verificar_pagina(cbl.contenedorPaginado, "4", "navegar_y_verificar_pagina_contenedor_paginado", config.SCREENSHOT_DIR)
    fg.verificar_pagina_inicial_seleccionada(cbl.contenedorPaginado, "4", "verificar_pagina_inicial_seleccionada_contenedor_paginado", config.SCREENSHOT_DIR)
    datos_esperados4 = [
        {"ID": "16", "Name": "E-Reader", "Price": "$10.99", "Select": False},
        {"ID": "17", "Name": "VR Headset", "Price": "$11.99", "Select": False},
        {"ID": "18", "Name": "Streaming Device", "Price": "$13.99", "Select": False},
        {"ID": "19", "Name": "Soundbar", "Price": "$16.99", "Select": True},
        {"ID": "20", "Name": "Wireless Mouse 20", "Price": "$17.99", "Select": True}
    ]
    datos_ok_4 = fg.verificar_datos_filas_tabla(cbl.tablaCheck, datos_esperados4, "verificar_datos_filas_tabla_check_pagina4", config.SCREENSHOT_DIR)
    assert datos_ok_4 is True, "Los datos de la tabla en la Página 4 no coinciden con los esperados."