from playwright.sync_api import Page

class IdTestLocatorsPage:
    
    def __init__(self, page: Page):
        self.page = page
        
    #Selectoe de texto nombre Jone Doe
    #Este elemento usa 'data-pw="profile-name"'
    @property
    def nombreDoe(self):
        # Usamos un selector CSS para el atributo data-pw
        return self.page.locator('[data-pw="profile-name"]')
    
    #Selectoe de correo Jone Doe
    #Este elemento usa 'data-pw="profile-email"'
    @property
    def correoJone(self):
        # Usamos un selector CSS para el atributo data-pw
        return self.page.locator('[data-pw="profile-email"]')
    
    #Selector de boton editar perfil
    @property
    def botonEditarPerfil(self):
        return self.page.get_by_test_id("edit-profile-btn")
    
    #Selector nombre producto A por test id
    @property
    def productoANombre(self):
        return self.page.locator("#testid-locators > div.grid > div:nth-child(1)").get_by_test_id("product-name")
    
    #Selector precio producto A por test id
    @property
    def productoAPrecio(self):
        return self.page.locator("//*[@id='testid-locators']/div[2]/div[1]").get_by_test_id("product-price")
    
    #Selector nombre producto B por test id
    @property
    def productoBNombre(self):
        return self.page.locator("#testid-locators > div.grid > div:nth-child(2)").get_by_test_id("product-name")
    
    #Selector precio producto A por test id
    @property
    def productoBPrecio(self):
        return self.page.locator("//*[@id='testid-locators']/div[2]/div[2]").get_by_test_id("product-price")
    
    #Selector nombre producto B por test id
    @property
    def productoCNombre(self):
        return self.page.locator("#testid-locators > div.grid > div:nth-child(3)").get_by_test_id("product-name")
    
    #Selector precio producto A por test id
    @property
    def productoCPrecio(self):
        return self.page.locator("//*[@id='testid-locators']/div[2]/div[3]").get_by_test_id("product-price")
    
    #Selector link home
    @property
    def linkHombe(self):
        return self.page.locator("#testid-locators").get_by_test_id("nav-home")
    
    #Selector link products
    @property
    def linkProducts(self):
        return self.page.locator("//*[@id='testid-locators']").get_by_test_id("nav-products")
    
    #Selector link contact
    @property
    def linkContact(self):
        return self.page.locator("#testid-locators").get_by_test_id("nav-contact")