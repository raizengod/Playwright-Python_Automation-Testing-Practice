from playwright.sync_api import Page

class MenuLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector del opción Playwright
    @property
    def irAPlaywright(self):
        return self.page.locator("//*[@id='PageList2']/div/ul/li[5]/a")