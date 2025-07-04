from playwright.sync_api import Page

class AlertsPopupsLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector de botón Simple Alert
    @property
    def botonSimpleAlert(self):
        return self.page.locator("#HTML9").get_by_text("Simple Alert")
    
    #Selector de botón Confirmation Alert
    @property
    def botonConfirmationAlert(self):
        return self.page.locator("#HTML9").get_by_text("Confirmation Alert")
    
    #Selector de mensaje de acción confirmada
    @property
    def mensajeConfirmacionDeAccion(self):
        return self.page.locator("//*[@id='demo']")
    
    #selector de botón de ingresar prompt
    @property
    def botonPromptAlert(self):
        return self.page.locator("#HTML9").get_by_text("Prompt Alert")