from playwright.sync_api import Page

class TablaDinamicaLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector de tabla dinamica
    @property
    def tablaDinamica(self):
        return self.page.locator("#taskTable")
    
    #Selector de contenedor de texto con valores
    @property
    def listaValores(self):
        return self.page.locator("//*[@id='displayValues']")
    
    #Selector de despliegue de valores de CPU
    @property
    def textoCPU(self):
        return self.page.locator("#displayValues > p:nth-child(1) > strong")
    
    #Selector de despliegue de valores de Memoria
    @property
    def textoMemoria(self):
        return self.page.locator("#displayValues > p:nth-child(2) > strong")
    
    #Selector de despliegue de valores de Red
    @property
    def textoRed(self):
        return self.page.locator("#displayValues > p:nth-child(3) > strong")
    
    #Selector de despliegue de valores de Disco
    @property
    def textoDisco(self):
        return self.page.locator("#displayValues > p:nth-child(4) > strong")