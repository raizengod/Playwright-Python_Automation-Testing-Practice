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