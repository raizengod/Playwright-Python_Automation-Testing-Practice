from playwright.sync_api import Page

class TextLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector del contenedor
    """Si el elemento no tiene un texto único o un nombre accesible, se busca un elemento padre o un elemento cercano que sí lo tenga, y luego se encadena a un locator.
    en este caso utilizamos el xpath"""
    @property
    def contenedorByText(self):
        return self.page.locator("//*[@id='text-locators']")
    
    #Selector de titulo de sección
    @property
    def tituloDos(self):
        return self.page.locator("#text-locators").get_by_text("getByText()")
    
    #Selector de descripción de la sección
    @property
    def descripcionByText(self):
        return self.page.get_by_text("by their text content.")
    
    #Selector de explicación 1 la sección
    @property
    def textExplicacion1(self):
        return self.page.locator("//*[@id='text-locators']/div[1]").get_by_text("important")
    
    #Selector de explicación 2 la sección
    @property
    def textExplicacion2(self):
        return self.page.locator("//*[@id='text-locators']/div[1]").get_by_text("colored text")
    
    #Selector de item 1
    @property
    def item1(self):
        return self.page.locator("#text-locators > ul").get_by_text("1")
    
    #Selector de item 2
    @property
    def item2(self):
        return self.page.locator("#text-locators > ul").get_by_text("link")
    
    #Selector de item 3
    @property
    def item3(self):
        return self.page.locator("#text-locators > ul").get_by_text("Special:")
    
    #Selector de botón
    @property
    def botonSubmit(self):
        return self.page.locator("#text-locators > div:nth-child(5)").get_by_text("Submit Form")
    
    #Selector de explicación de botón
    @property
    def explicacionBoton(self):
        return self.page.get_by_text("button above to submit")
    
    