from playwright.sync_api import Page

class RoleLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selector del contenedor
    """Si el elemento no tiene un texto único o un nombre accesible, se busca un elemento padre o un elemento cercano que sí lo tenga, y luego se encadena a un locator.
    en este caso utilizamos el xpath y el role"""
    @property
    def contenedorByRole(self):
        return self.page.locator("//*[@id='role-locators']").get_by_role("generic")
        
    #Selector del titulo 1. getByRole() Locators
    @property
    def tituloUno(self):
        return self.page.get_by_role("heading", name="1. getByRole() Locators")
    
    #Selector label de explicación.
    """Si el párrafo no tiene un texto único o un nombre accesible, se busca un elemento padre o un elemento cercano que sí lo tenga, y luego se encadena a un locator.
    en este caso usamos el locator CSS y el role"""
    @property
    def labelDescripcion(self):
        return self.page.locator("#role-locators > p")
    
    #Selector label button
    @property
    def labelBoton(self):
        return self.page.get_by_role("heading", name="Buttons")
    
    #Selector botón primario
    @property
    def botonPrimario(self):
        return self.page.get_by_role("button", name="Primary Action")
    
    #Selector botón Toggle
    @property
    def botonToggle(self):
        return self.page.get_by_role("button", name="Toggle Button")
    
    #Selector botón con div
    @property
    def botonRoleEnDive(self):
        return self.page.get_by_role("button", name="Div with button role")
    
    #Selector label fomulario
    @property
    def labelFormulario(self):
        return self.page.get_by_role("heading", name="Form Elements")
    
    #Selector label usuario
    @property
    def labelUsuario(self):
        return self.page.locator("//*[@id='role-locators']/div/div[2]/label[1]")
    
    #Selecot campo de texto username
    @property
    def campoTextoUsername(self):
        return self.page.get_by_role("textbox", name="Username:")
    
    #Selector checkBox aceptar términos y condiciones
    @property
    def checkTerminosYCondiciones(self):
        return self.page.get_by_role("checkbox", name=" Accept terms")
    
    #Selector label navegación
    @property
    def labelNavegacion(self):
        return self.page.get_by_role("heading", name= "Navigation")
    
    #Selector link home
    @property
    def linkHome(self):
        return self.page.locator("#role-locators > div > div:nth-child(3)").get_by_role("link", name="Home")
    
    #Selector link productos
    @property
    def linkProductos(self):
        return self.page.locator("#role-locators > div > div:nth-child(3)").get_by_role("link", name="Products")
    
    #Selector link contactar
    @property
    def linkContactar(self):
        return self.page.locator("#role-locators > div > div:nth-child(3)").get_by_role("link", name="Contact")
    
    #Selector mensaje de alerta
    """Si el elemento no tiene un texto único o un nombre accesible, se busca un elemento padre o un elemento cercano que sí lo tenga, y luego se encadena a un locator.
    en este caso utilizamos el xpath y el role"""
    @property
    def mensajeAlerta(self):
        return self.page.locator("#role-locators > div > div:nth-child(3)").get_by_role("alert")
    
    #Selector de botón dinamico START
    @property
    def botonDinamicoStart(self):
        return self.page.locator("#HTML5").get_by_role("button", name= "START")
    
    #Selector de botón dinamico STOP
    @property
    def botonDinamicoStop(self):
        return self.page.locator("#HTML5").get_by_role("button", name= "STOP")