from playwright.sync_api import Page

class TitleLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selectoe de texto explicativo a hacer
    @property
    def explicacionText(self):
        return self.page.locator("//*[@id='title-locators']/div").get_by_text("Hover over these elements")
        
    #Selector de link en sección getByTitle
    @property
    def homeLink(self):
        return self.page.locator("#title-locators > div").get_by_title("Home page link")
    
    #Selector de HTML en sección getByTitle
    @property
    def htmlText(self):
        return self.page.locator("//*[@id='title-locators']/div").get_by_title("HyperText Markup Language")
    
    #Selector de texto en sección getByTitle
    @property
    def textTooltip(self):
        return self.page.locator("#title-locators > div").get_by_title("Tooltip text")
    
    #Selector de botón SAVE en sección getByTitle
    @property
    def saveBoton(self):
        return self.page.locator("//*[@id='title-locators']").get_by_title("Click to save your changes")