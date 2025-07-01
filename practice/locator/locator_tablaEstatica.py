from playwright.sync_api import Page

class TablaEstaticaLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector de tabla estatica
    @property
    def tabla(self):
        return self.page.locator("#HTML1 > div.widget-content")