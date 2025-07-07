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
    
    #Selector titulo Drag and Drop
    @property
    def tituloDragAndDrop(self):
        return self.page.locator("#HTML2").get_by_text("Drag and Drop")
    
    #Selector elemento Drag me
    @property
    def objetoDragMe(self):
        return self.page.locator("//*[@id='draggable']")
    
    #Selector elemento Drop
    @property
    def objetoDropHere(self):
        return self.page.locator("//*[@id='droppable']")
    
    #Selector titulo slider
    @property
    def tituloSlider(self):
        return self.page.locator("#HTML7").get_by_role("heading", name="Slider")
    
    #Selector barra slider
    @property
    def barraSlider(self):
        return self.page.locator("#slider-range")
    
    #Selector punto inicio
    @property
    def puntoInicioSlider(self):
        return self.page.locator("#slider-range span").first
    
    #Selector punto final
    @property
    def puntoFinalSlider(self):
        return self.page.locator("#slider-range span").nth(1)
    
    #Selector subtitulo slider price
    @property
    def subTituloPriceSlider(self):
        return self.page.locator("#HTML7").get_by_text("Price range:")
    
    #Selector de rango de precio
    @property
    def rangoPrecio(self):
        return self.page.locator("#HTML7").get_by_role("textbox", name="Price range:")
    
    #Selector de titulo comboBox
    @property
    def tituloComboBox(self):
        return self.page.locator("#HTML17").get_by_role("heading", name="Scrolling DropDown")
    
    #Selector de comboBox
    @property
    def comboBox(self):
        return self.page.locator("//*[@id='HTML17']").get_by_role("textbox", name="Select an item")