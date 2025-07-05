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
    
    #selector de botón de abrir nueva pestaña
    @property
    def botonNewTab(self):
        return self.page.get_by_role("button", name="New Tab")
    
    #Selector de titulo enbezado nueva pestañ
    @property
    def tituloEncabezadoNuevatab1(self):
        return self.page.locator("#header-inner > div.titlewrapper > h1")
    
    #Selector de titulo enbezado nueva pestañ
    @property
    def tituloEncabezadoNuevatab2(self):
        return self.page.locator("//*[@id='header-inner']/div[2]/p")
    
    #Selector de botón de abrir nueva ventana
    @property
    def botonNuevaVentana(self):
        return self.page.get_by_role("button", name= "Popup Windows")
    
    #Selector de titulo de nueva ventana
    @property
    def tituloNuevaVenatana(self):
        return self.page.get_by_role("heading", name="Selenium automates browsers.")
    
    #Selector de titulo de nueva ventana 2
    @property
    def tituloNuevaVenatana2(self):
        return self.page.get_by_role("heading", name="Playwright enables reliable")
    