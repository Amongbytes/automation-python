import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ─── Constantes del sitio ───────────────────────────────────────────────────

BASE_URL       = "https://www.saucedemo.com"
USUARIO_VALIDO = "standard_user"
CLAVE_VALIDA   = "secret_sauce"
CARPETA_CAPTURAS = "reports"


# ─── Configuración del navegador ────────────────────────────────────────────

def crear_driver():
    opciones = webdriver.ChromeOptions()

    # Ejecutar en modo headles:
    opciones.add_argument("--no-sandbox")           
    opciones.add_argument("--disable-dev-shm-usage") 
    opciones.add_argument("--window-size=1280,800") #tamalo de ventana 

    # ChromeDriverManager
    servicio = Service(ChromeDriverManager().install())
    driver   = webdriver.Chrome(service=servicio, options=opciones)

    return driver


# ─── Función de login ────────────────────────────────────────────────────────

def hacer_login(driver, usuario=USUARIO_VALIDO, clave=CLAVE_VALIDA):
    # Navega al link  de la web sauvedemo 
    driver.get(BASE_URL)

    # Esperar a que el campo de usuario esté visible (10 secundos)
    espera = WebDriverWait(driver, 10)
    campo_usuario = espera.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    # Escribir el  usuario
    campo_usuario.clear()
    campo_usuario.send_keys(usuario)

    # Localiza el campo de contraseña y escribir la clave
    campo_clave = driver.find_element(By.ID, "password")
    campo_clave.clear()
    campo_clave.send_keys(clave)

    # Hacer click en el botón de login
    boton_login = driver.find_element(By.ID, "login-button")
    boton_login.click()


# ─── Función de espera explícita ────────────────────────────────────────────

def esperar_elemento(driver, by, valor, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, valor))
    )


# ─── Función de captura de pantalla ─────────────────────────────────────────

def tomar_captura(driver, nombre_archivo):
    # Crear la carpeta si no existe
    os.makedirs(CARPETA_CAPTURAS, exist_ok=True)

    # Ruta completa del archivo
    ruta = os.path.join(CARPETA_CAPTURAS, f"{nombre_archivo}.png")
    driver.save_screenshot(ruta)
    print(f"[Captura guardada] → {ruta}")


# ─── Función para agregar producto al carrito ─────────────────────────────────

def agregar_primer_producto(driver):
    # Obtener el nombre del primer producto de la lista
    nombre_producto = driver.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    # Hacer clic en el primer botón "Add to cart" que aparezca
    boton_agregar = driver.find_element(
        By.CSS_SELECTOR, ".btn_primary.btn_inventory"
    )
    boton_agregar.click()

    return nombre_producto