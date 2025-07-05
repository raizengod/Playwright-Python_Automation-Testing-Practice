from playwright.sync_api import Page

class MouseActionsLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector de titulo Mouse Hover
    @property
    def tituloMouseHover(self):
        return self.page.locator("#HTML3").get_by_role("heading", name="Mouse Hover")
    
    #Selector de descripción
    @property
    def descripcionMouseHover(self):
        return self.page.locator("#HTML3").get_by_text("Move the mouse over")
    
    #Selector de botón hover
    @property
    def botonHover(self):
        return self.page.locator("#HTML3").get_by_role("button", name="Point Me")
    
    #Selector de opción Movile
    @property
    def opcionMobil(self):
        return self.page.locator("#HTML3").get_by_role("link", name="Mobiles")
    
    #Selector de opción Laptop
    @property
    def opcionLaptop(self):
        return self.page.locator("#HTML3").get_by_role("link", name="Laptops")
    
    #Selector titulo doble click
    @property
    def tituloDobleClick(self):
        return self.page.locator("//*[@id='HTML10']").get_by_role("heading", name="Double Click")
    
    #Selector campo 1 doble click
    @property
    def campoUnoDobleClick(self):
        return self.page.locator("#field1")
    
    #Selector campo 2 doble click
    @property
    def campoDosDobleClick(self):
        return self.page.locator("#field2")
    
    #Selector botón doble click
    @property
    def botonDobleClick(self):
        return self.page.locator("//*[@id='HTML10']").get_by_role("button", name="Copy Text")
    
    #Selector descripción doble click
    @property
    def descripcionDobleClick(self):
        return self.page.locator("//*[@id='HTML10']").get_by_text("Double click on button, the")