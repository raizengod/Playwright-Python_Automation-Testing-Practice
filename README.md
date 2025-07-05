# Proyecto de Automatización de Pruebas UI con Playwright y Python

## 🚀 Descripción General

Este proyecto demuestra mis habilidades en **automatización de pruebas de interfaz de usuario (UI)** utilizando **Playwright** con **Python** y el framework **Pytest**. El objetivo es validar las funcionalidades clave de la página web de práctica: https://testautomationpractice.blogspot.com/.

Este repositorio forma parte de mi portafolio personal, mostrando mi capacidad para diseñar, desarrollar y ejecutar pruebas automatizadas robustas.

## ✨ Características Principales

* **Tecnología Moderna:** Implementado con Playwright, un framework de automatización rápido y confiable.
* **Lenguaje de Programación:** Desarrollado en **Python 3.13.5**.
* **Gestión de Pruebas:** Organización de casos de prueba con **Pytest**.
* **Generación de Informes:** Utilización de para visualización clara y detallada de los resultados de las pruebas.
* **Cobertura Funcional:** Validación de formularios, tablas web, interacción con checkBox individuales, varios checkBox, carga de archivos, varios tipos de localizadores de elementos, acciones con el mouse, interacción con alertas, pop-up, nuevas ventanas y pestañas

## 🛠️ Tecnologías Utilizadas

* **Playwright**: Framework de automatización de navegadores para pruebas end-to-end.
* **Python**: Lenguaje de programación utilizado para escribir los scripts de prueba.
* **Pytest**: Framework de pruebas para Python, utilizado para organizar y ejecutar los tests.
* **GitHub Actions**: Para la integración continua (CI) y la ejecución automatizada de pruebas.

## 🚀 Ejecución de las Pruebas
Sigue estos pasos para configurar y ejecutar las pruebas en tu entorno local:

**Prerrequisitos**
1. **Instalar Python 3.13.5** (si no lo tienes instalado).

Para ejecutar las pruebas localmente, sigue los siguientes pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/raizengod/Playwright-Python_Automation-Testing-Practice.git
    cd ATP
    ```

2.  **Crear y activar un entorno virtual (recomendado):**
    ```bash
    python -m venv mv_ATP
    # En Windows:
    .\venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    playwright install  # Instala los navegadores necesarios (Chromium, Firefox, WebKit)
    ```
**Ejecución de Pruebas**

1.  **Ejecuta las pruebas y genera los resultados de reporte:**
    ```bash
    pytest practce\test\test_alertsAndPopups.py -s -v --template=html1/index.html --report=reportes/html1/playwright_reporte.html
    ```

2.  **Ejecutar todas las pruebas con Pytest:**
    ```bash
    pytest practce\test\test_getByRole.py practce\test\test_getByText.py practce\test\test_getByLabel.py practce\test\test_getByPlaceholder.py practce\test\test_getByAltText.py practce\test\test_getByTitle.py practce\test\test_getByTestId.py practce\test\test_cargarArchivo.py practce\test\test_tablaEstatica.py practce\test\test_tablaDinamica.py practce\test\test_checkBoxLista.py practce\test\test_alertsAndPopups.py practce\test\test_mouseAction.py
    ```

3.  **Ejecutar pruebas específicas (ejemplo):**
    ```bash
    pytest practce\test\test_tablaDinamica.py
    ```

4.  **Ejecutar todas las pruebas con reporte detallado y genera los resultados en reporte HTML:**:**
    ```bash
    pytest practce\test\test_getByRole.py practce\test\test_getByText.py practce\test\test_getByLabel.py practce\test\test_getByPlaceholder.py practce\test\test_getByAltText.py practce\test\test_getByTitle.py practce\test\test_getByTestId.py practce\test\test_cargarArchivo.py practce\test\test_tablaEstatica.py practce\test\test_tablaDinamica.py practce\test\test_checkBoxLista.py practce\test\test_alertsAndPopups.py practce\test\test_mouseAction.py -s -v --template=html1/index.html --report=reportes/html1/playwright_reporte.html
    ```

## 📂 Estructura del Proyecto (Ejemplo)

```
ATP/
├── .github/
│   └── workflows/
│       └── playwright.yml         # Configuración de GitHub Actions para CI
├── mv_ATP/
├── preactice/                 # Contenedor principal del código fuente
│   ├── __init__.py
│   ├── pages/                 # Implementación del Page Object Model (POM)
│   │   ├── __init__.py
│   │   └── base_page.py       # Clase base con funciones globales
│   ├── locator/            # Centralización de selectores de elementos web
│   │   ├── __init__.py
│   │   ├── locator_AlertsAndPopups.py
│   │   ├── locator_barraMenu.py
│   │   ├── locator_cheBoxLista.py
│   │   ├── locator_getByAltText.py
│   │   ├── locator_getByLabel.py
│   │   ├── locator_getByPlaceholdr.py
│   │   ├── locator_getByRole.py
│   │   ├── locator_getByTestId.py
│   │   ├── locator_getByText.py
│   │   ├── locator_getByTitle.py
│   │   ├── locator_mouseAction
│   │   ├── locator_tablaDinamica.py
│   │   ├── locator_tablaEstatica.py
│   │   └── locator_uploadFiles.py
│   ├── tests/
│   │   ├── archivos_fuentes/  # Archivos para probar upload
│   │   ├── reporte/
│   │   │   ├── html/          # Directorio donde se genera el informe HTML
│   │   │   ├── video/         
│   │   │   ├── traceview/     # Directorio donde se genera registro traceview de la prueba  
│   │   │   └── imagen/  
│   │   ├── test_alertsAndPopups.py
│   │   ├── test_cargarArchivo.py
│   │   ├── test_checkBoxLista.py
│   │   ├── test_getByAltText.py
│   │   ├── test_getByLabel.py
│   │   ├── test_getByPlaceholder.py
│   │   ├── test_getByRole.py
│   │   ├── test_getByTestId.py
│   │   ├── test_getByText.py
│   │   ├── test_getByTitle.py
│   │   ├── test_mouseAction.py
│   │   ├── test_tablaDinamica.py
│   │   └── test_tablaEstatica.py
│   └── util/
│       ├── __init__.py
│       └── config.py
├── .gitignore
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Este archivo
```