# nombra el archivo: Ve a la ubicación de tu archivo y colcoar el nombre a conftest.py
# La convención de conftest.py le indica a Pytest que este archivo contiene fixtures que deben estar disponibles 
# para los tests en ese directorio y sus subdirectorios.
import pytest
import time
from playwright.sync_api import Page, expect, Playwright, sync_playwright
from datetime import datetime
import os
from typing import Generator
from practice.utils import config

from practice.pages.base_page import Funciones_Globales
from practice.locator.locator_getByRole import RoleLocatorsPage
from practice.locator.locator_barraMenu import MenuLocatorsPage

# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="function", # Cambiado a 'function' como en tu ejemplo más reciente
    params=[
        # Resoluciones de escritorio
        #{"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()

        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page) # Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        
        # Ahora puedes usar fg, lr, ml sin el error de 'NoneType'
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
            
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session", # Se mantiene 'session' como en tu código original para esta fixture
    params=[
        # Resoluciones de escritorio
        #{"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_ir_a(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # Importaciones de tus clases POM (Page Object Model)
        # Se importan aquí para asegurar que estén disponibles en el fixture (aunque también pueden ir arriba)
        # from practice.pages.base_page import Funciones_Globales # Ya están arriba
        # from practice.locator.locator_getByRole import RoleLocatorsPage # Ya están arriba
        # from practice.locator.locator_barraMenu import MenuLocatorsPage # Ya están arriba

        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
            
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session", # Se mantiene 'session' como en tu código original para esta fixture
    params=[
        # Resoluciones de escritorio
        #{"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_byText(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 500)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                    
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session", # Se mantiene 'session' como en tu código original para esta fixture
    params=[
        # Resoluciones de escritorio
        #{"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        {"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_byLabel(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 1200)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                    
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session", # Se mantiene 'session' como en tu código original para esta fixture
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_byPlaceholder(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 1800)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session", # Se mantiene 'session' como en tu código original para esta fixture
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_byAltText(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 2100)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                    
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_byTitle(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 2550)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                    
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_byTestId(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 3000)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                    
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_cargarArchivo(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 3800)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                    
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_manejodDeTabla(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        lr = RoleLocatorsPage(page)
        ml = MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 4400)
        
        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%MM%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")
                
# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_checkBoxLista(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None

    try:
        from practice.pages.base_page import Funciones_Globales
        from practice.locator.locator_getByRole import RoleLocatorsPage
        from practice.locator.locator_barraMenu import MenuLocatorsPage
        #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
        fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
        #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
        lr= RoleLocatorsPage(page)
        #IMPORTANTE: Creamos un objeto de tipo función 'barraMenu'
        ml= MenuLocatorsPage(page)
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        page = context.new_page()
        
        #IMPORTANTE: Creamos un objeto de tipo función 'Funciones_Globales'
        fg= Funciones_Globales(page) #Este page va ser enviado a la función __init__ en el archivo FuncionesPOM
        #IMPORTANTE: Creamos un objeto de tipo función 'getByRole'
        lr= RoleLocatorsPage(page)
        #IMPORTANTE: Creamos un objeto de tipo función 'barraMenu'
        ml= MenuLocatorsPage(page)

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(5000)
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        #Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 5000)
        

        yield page

    finally:
        if context:
            context.tracing.stop(path=trace_path)
            
            context.close()
            
            if browser_instance:
                browser_instance.close()
            
            # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
            if page and page.video:
                video_path = page.video.path()
                
                new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
                new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
                try:
                    os.rename(video_path, new_video_path)
                    print(f"\nVideo guardado como: {new_video_path}")
                except Exception as e:
                    print(f"\nError al renombrar el video: {e}")

# Usaremos un fixture parametrizado para la emulación de navegadores y dispositivos
@pytest.fixture(
    scope="session",
    params=[
        # Resoluciones de escritorio
        {"browser": "chromium", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Puedes descomentar las siguientes líneas si deseas probar con Firefox, WebKit o dispositivos móviles
        #{"browser": "firefox", "resolution": {"width": 1920, "height": 1080}, "device": None},
        #{"browser": "webkit", "resolution": {"width": 1920, "height": 1080}, "device": None},
        # Emulación de dispositivos móviles
        #{"browser": "chromium", "device": "iPhone 12", "resolution": None},
        #{"browser": "firefox", "device": "Pixel 5", "resolution": None},
        #{"browser": "webkit", "device": "iPad Air", "resolution": None},
    ]
)
def set_up_mouseAction(playwright: Playwright, request) -> Generator[Page, None, None]:
    param = request.param
    browser_type = param["browser"]
    resolution = param["resolution"]
    device_name = param["device"]

    browser_instance = None
    context = None
    page = None # Inicialmente None, se le asignará el objeto Page real más adelante

    try:
        # --- Lanza el navegador según el tipo especificado ---
        if browser_type == "chromium":
            browser_instance = playwright.chromium.launch(headless=False, slow_mo=500)
        elif browser_type == "firefox":
            browser_instance = playwright.firefox.launch(headless=False, slow_mo=500)
        elif browser_type == "webkit":
            browser_instance = playwright.webkit.launch(headless=False, slow_mo=500)
        else:
            raise ValueError(f"\nEl tipo de navegador '{browser_type}' no es compatible.")

        # Prepara las opciones de contexto para la grabación de video y la emulación de dispositivos
        context_options = {
            "record_video_dir": config.VIDEO_DIR, # Usamos la ruta de config.py
            "record_video_size": {"width": 1920, "height": 1080}
        }

        # --- Crea un nuevo contexto del navegador con las opciones y/o emulación de dispositivo ---
        if device_name:
            device = playwright.devices[device_name]
            context = browser_instance.new_context(**device, **context_options)
        elif resolution:
            context = browser_instance.new_context(viewport=resolution, **context_options)
        else:
            context = browser_instance.new_context(**context_options)

        # --- Crea una nueva página dentro del contexto ---
        # ¡Aquí es donde 'page' se convierte en un objeto Page válido!
        page = context.new_page()
        
        # --- IMPORTANTE: Creamos objetos de tus clases POM *después* de que 'page' sea válido ---
        # Este 'page' ahora es un objeto Page real de Playwright.
        fg = Funciones_Globales(page)
        ml = MenuLocatorsPage(page)   

        # Inicializa Trace Viewer con un nombre dinámico
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name_suffix = ""
        if device_name:
            trace_name_suffix = device_name.replace(" ", "_").replace("(", "").replace(")", "")
        elif resolution:
            trace_name_suffix = f"{resolution['width']}x{resolution['height']}"

        trace_file_name = f"traceview_{current_time}_{browser_type}_{trace_name_suffix}.zip"
        trace_path = os.path.join(config.TRACEVIEW_DIR, trace_file_name) # Usamos la ruta de config.py

        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        # Navegación inicial y configuraciones de página
        page.goto(config.BASE_URL) # Usamos la URL de config.py
        page.set_default_timeout(800) # Un timeout de 5 segundos es más común que 800ms
        
        fg.hacer_click_en_elemento(ml.irAPlaywright, "PlaywrightPractice", config.SCREENSHOT_DIR, "PlaywrightPractice")
        # Luego del paso anterior, ahora si podemos llamar a nuestras funciones creadas en el archivo POM
        fg.esperar_fijo(1)
        fg.scroll_pagina(0, 1100)
        
        # Este 'yield' es lo que pasa el objeto 'page' a tus funciones de test
        yield page

    finally:
        # Bloque finally para asegurar que los recursos se cierren correctamente
        if context:
            context.tracing.stop(path=trace_path)
            context.close()
            
        if browser_instance:
            browser_instance.close()
            
        # Renombra el archivo de video con el formato AAAAMMDD-HHMMSS
        # Verifica si 'page' no es None y tiene un objeto de video antes de intentar acceder a .video
        if page and page.video:
            video_path = page.video.path()
            
            new_video_name = datetime.now().strftime("%Y%m%d-%H%M%S") + ".webm"
            new_video_path = os.path.join(config.VIDEO_DIR, new_video_name)
            try:
                os.rename(video_path, new_video_path)
                print(f"\nVideo guardado como: {new_video_path}")
            except Exception as e:
                print(f"\nError al renombrar el video: {e}")