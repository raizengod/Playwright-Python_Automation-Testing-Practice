import re
import time
import random
import pytest
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_uploadFiles import UploadLocatorsPage
from practice.utils import config

def test_cargar_un_archivo(set_up_cargarArchivo):
    page= set_up_cargarArchivo
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    ul= UploadLocatorsPage(page)
    
    #Validar que no se tiene archivos precarcados la primera vez
    fg.verificar_valor_campo(ul.buscarUnArchivo, "", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    
    #Verificando que no se muestre el mensaje post-carga de archivo todavía
    fg.validar_elemento_no_visible(ul.estatusUnArchivo, "validar_elemento_no_visible_estatus_un_archivo", config.SCREENSHOT_DIR)
    
    #Subiendo un archivo .txt
    fg.cargar_archivo(ul.buscarUnArchivo, "cargar_archivo_buscar_Un_Archivo", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, "Documento de texto (vacio).txt")
    fg.verificar_valor_campo(ul.buscarUnArchivo, r"C:\fakepath\Documento de texto (vacio).txt", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirUnArchivo, "verificar_texto_contenido_subir_un_archivo", config.SCREENSHOT_DIR, "Upload Single File")
    fg.verificar_texto_contenido(ul.estatusUnArchivo, "Documento de texto (vacio).txt", "verificar_texto_contenido_estatus_Un_Archivo", config.SCREENSHOT_DIR)
    #Subiendo un archivo .xlsx
    fg.cargar_archivo(ul.buscarUnArchivo, "cargar_archivo_buscar_Un_Archivo", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, "Excel (vacio).xlsx")
    fg.verificar_valor_campo(ul.buscarUnArchivo, r"C:\fakepath\Excel (vacio).xlsx", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirUnArchivo, "verificar_texto_contenido_subir_un_archivo", config.SCREENSHOT_DIR, "Upload Single File")
    fg.verificar_texto_contenido(ul.estatusUnArchivo, "Excel", "verificar_texto_contenido_estatus_Un_Archivo", config.SCREENSHOT_DIR)
    #Subiendo un archivo .pptx
    fg.cargar_archivo(ul.buscarUnArchivo, "cargar_archivo_buscar_Un_Archivo", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, "PowerPoint (vacio).pptx")
    fg.verificar_valor_campo(ul.buscarUnArchivo, r"C:\fakepath\PowerPoint (vacio).pptx", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirUnArchivo, "verificar_texto_contenido_subir_un_archivo", config.SCREENSHOT_DIR, "Upload Single File")
    fg.verificar_texto_contenido(ul.estatusUnArchivo, "PowerPoint (vacio)", "verificar_texto_contenido_estatus_Un_Archivo", config.SCREENSHOT_DIR)
    #Subiendo un archivo .docx
    fg.cargar_archivo(ul.buscarUnArchivo, "cargar_archivo_buscar_Un_Archivo", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, "PowerPoint (vacio).pptx")
    fg.verificar_valor_campo(ul.buscarUnArchivo, r"C:\fakepath\PowerPoint (vacio).pptx", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirUnArchivo, "verificar_texto_contenido_subir_un_archivo", config.SCREENSHOT_DIR, "Upload Single File")
    fg.verificar_texto_contenido(ul.estatusUnArchivo, "PowerPoint (vacio)", "verificar_texto_contenido_estatus_Un_Archivo", config.SCREENSHOT_DIR)
    
def test_cargar_multi_archivo(set_up_cargarArchivo):
    page= set_up_cargarArchivo
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    ul= UploadLocatorsPage(page)
    
    #Validar que no se tiene archivos precarcados la primera vez
    fg.verificar_valor_campo(ul.buscarMultiArchivo, "", "verificar_valor_campo_buscar_multi_Archivo", config.SCREENSHOT_DIR)
    
    #Verificando que no se muestre el mensaje post-carga de archivo todavía
    fg.validar_elemento_no_visible(ul.estatusMultiArchivo, "validar_elemento_no_visible_estatus_un_archivo", config.SCREENSHOT_DIR)
    
    #Subiendo 2 archivos
    fg.cargar_archivo(ul.buscarMultiArchivo, "cargar_archivo_buscar_multi_Archivos", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, ["Documento de texto (vacio).txt", "Excel (vacio).xlsx"])
    fg.verificar_valor_campo(ul.buscarMultiArchivo, "C:\\fakepath\\Documento de texto (vacio).txt", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirMultiArchivo, "verificar_texto_contenido_subir_multi_archivos", config.SCREENSHOT_DIR, "Upload Multiple Files")
    fg.verificar_texto_contenido(ul.subirMultiArchivo, "Upload Multiple Files", "verificar_texto_contenido_estatus_multi_Archivo", config.SCREENSHOT_DIR)
    
    #Subiendo 3 archivos
    fg.cargar_archivo(ul.buscarMultiArchivo, "cargar_archivo_buscar_multi_Archivos", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, ["PowerPoint (vacio).pptx","Documento de texto (vacio).txt", "Excel (vacio).xlsx"])
    fg.verificar_valor_campo(ul.buscarMultiArchivo, "C:\\fakepath\\PowerPoint (vacio).pptx", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirMultiArchivo, "verificar_texto_contenido_subir_multi_archivos", config.SCREENSHOT_DIR, "Upload Multiple Files")
    fg.verificar_texto_contenido(ul.subirMultiArchivo, "Upload Multiple Files", "verificar_texto_contenido_estatus_multi_Archivo", config.SCREENSHOT_DIR)
    
    #Subiendo 4 archivos
    fg.cargar_archivo(ul.buscarMultiArchivo, "cargar_archivo_buscar_multi_Archivos", config.SCREENSHOT_DIR, config.SOURCE_FILES_DIR, ["Word (vacio).docx","Documento de texto (vacio).txt", "Excel (vacio).xlsx", "PowerPoint (vacio).pptx"])
    fg.verificar_valor_campo(ul.buscarMultiArchivo, "C:\\fakepath\\Word (vacio).docx", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    fg.hacer_click_en_elemento(ul.subirMultiArchivo, "verificar_texto_contenido_subir_multi_archivos", config.SCREENSHOT_DIR, "Upload Multiple Files")
    fg.verificar_texto_contenido(ul.subirMultiArchivo, "Upload Multiple Files", "verificar_texto_contenido_estatus_multi_Archivo", config.SCREENSHOT_DIR)
    
    
def test_remover_carga(set_up_cargarArchivo):
    page= set_up_cargarArchivo
    
    #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
    fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
    #IMPORTANTE: Creamos un objeto de tipo función 'getByRolgetAltText'
    ul= UploadLocatorsPage(page)
    
    fg.remover_carga_de_archivo(ul.buscarMultiArchivo, "remover_carga_de_archivo_multi_archivo", config.SCREENSHOT_DIR, 1)
    fg.remover_carga_de_archivo(ul.buscarUnArchivo, "remover_carga_de_archivo_un_archivo", config.SCREENSHOT_DIR, 1)
    
    #Validar que no se tiene archivos precarcados la primera vez
    fg.verificar_valor_campo(ul.buscarUnArchivo, "", "verificar_valor_campo_buscar_Un_Archivo", config.SCREENSHOT_DIR)
    
    #Validar que no se tiene archivos precarcados la primera vez
    fg.verificar_valor_campo(ul.buscarMultiArchivo, "", "verificar_valor_campo_buscar_multi_Archivo", config.SCREENSHOT_DIR)