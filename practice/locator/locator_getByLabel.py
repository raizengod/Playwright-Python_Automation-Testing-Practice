from playwright.sync_api import Page

class LabelLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector del contenedor
    """Si el elemento no tiene un texto único o un nombre accesible, se busca un elemento padre o un elemento cercano que sí lo tenga, y luego se encadena a un locator.
    en este caso utilizamos el xpath"""
    @property
    def contenedorByLabel(self):
        return self.page.locator("#label-locators")
    
    #Selector del campo email
    @property
    def campoEmail(self):
        return self.page.get_by_label("Email Address:")
    
    #Selector del campo clave
    @property
    def campoClave(self):
        return self.page.get_by_label("Password:")
    
    #selector del campo numérico edad
    @property
    def campoEdad(self):
        return self.page.get_by_label("Your Age:")
    
    #Selector de radio button Standar
    @property
    def optionStandar(self):
        return self.page.locator("#label-locators > fieldset").get_by_label("Standard")
    
    #Selector de radio button Express
    @property
    def optionExpress(self):
        return self.page.locator("#label-locators > fieldset").get_by_label("Express")