from playwright.sync_api import Page

class UploadLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector del opción cargar un solo archivo
    @property
    def tituloCargarArchivo(self):
        return self.page.locator("//*[@id='HTML15']").get_by_title("title")
    
    #Selector seleccionar archivo unico
    @property
    def buscarUnArchivo(self):
        return self.page.locator("//*[@id='singleFileInput']")
    
    #Selector seleccionar archivo unico
    @property
    def subirUnArchivo(self):
        return self.page.get_by_role("button", name="Upload Single File")
    
    #Selector estatus de cargar de un archivo
    @property
    def estatusUnArchivo(self):
        return self.page.locator("#singleFileStatus")
    
    #Selector seleccionar archivo unico
    @property
    def buscarMultiArchivo(self):
        return self.page.locator("#multipleFilesInput")
    
    #Selector seleccionar archivo unico
    @property
    def subirMultiArchivo(self):
        return self.page.get_by_role("button", name="Upload Multiple Files")
    
    #Selector estatus de cargar de multiples archivo
    @property
    def estatusMultiArchivo(self):
        return self.page.locator("#multipleFilesStatus")