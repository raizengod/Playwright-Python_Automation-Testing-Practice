from playwright.sync_api import Page

class CheckBoxListaLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector de tabla con check
    @property
    def tablaCheck(self):
        return self.page.locator("#productTable")
    
    #Selector de encabezado de tabla
    @property
    def encabezadotabla(self):
        return self.page.locator("#productTable > thead")
    
    #Selector paginador
    @property
    def contenedorPaginado(self):
        return self.page.locator("#pagination")