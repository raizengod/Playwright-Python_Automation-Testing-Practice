from playwright.sync_api import Page

class AltLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector de logo playwrigh
    @property
    def logoPlaywright(self):
        return self.page.get_by_alt_text("logo image")
    
    #Selector de subdescripción de imagen
    @property
    def subDescripcionImagen(self):
        return self.page.locator("//*[@id='alttext-locators']/div").get_by_text("Playwright Logo")