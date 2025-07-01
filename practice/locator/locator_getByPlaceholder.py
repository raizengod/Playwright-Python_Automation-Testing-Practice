from playwright.sync_api import Page

class PlaceholderLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector del campo email por placeholder
    @property
    def campoPlaceholderEmail(self):
        return self.page.get_by_placeholder("Enter your full name")
    
    #Selector del campo número de teléfono por placeholder
    @property
    def campoPlaceholderTelefono(self):
        return self.page.get_by_placeholder("Phone number (xxx-xxx-xxxx)")
    
    #Selector del campo mensaje por placeholder
    @property
    def campoPlaceholderMensaje(self):
        return self.page.get_by_placeholder("Type your message here...")
    
    #Selector del campo bucar por placeholder
    @property
    def campoPlaceholderBuscar(self):
        return self.page.get_by_placeholder("Search products...")
    
    #Selector del botón buscar por role
    @property
    def botonBuscar(self):
        return self.page.get_by_role("button", name="Search")