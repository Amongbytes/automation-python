import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importar funciones auxiliares desde el módulo utils
from utils.helpers import (
    crear_driver,
    hacer_login,
    esperar_elemento,
    tomar_captura,
    agregar_primer_producto,
)


# ─── Ciclo del driver ──────────────────

@pytest.fixture
def driver():
    controlador = crear_driver()
    yield controlador
    controlador.quit() 

# TEST 1 — Login exitoso

def test_login_exitoso(driver):
    try:
        # login con credenciales válidas
        hacer_login(driver)

        # Esperar a que la URL cambie a la página de inventario
        WebDriverWait(driver, 10).until(
            EC.url_contains("inventory.html")
        )

        # URL con la ruta esperada
        url_actual = driver.current_url
        assert "inventory.html" in url_actual, (
            f"Se esperaba /inventory.html pero se obtuvo: {url_actual}"
        )

        # Encabezado de la página muestre Products o Swag Labs
        # Título del app bar Swag Labs
        titulo_app = esperar_elemento(driver, By.CLASS_NAME, "app_logo")
        assert "Swag Labs" in titulo_app.text, (
            f"Título inesperado: {titulo_app.text}"
        )

        print(f"\n✅ Login exitoso. URL: {url_actual}")

    except Exception as error:
        # Si el test falla, tomamos captura
        tomar_captura(driver, "fallo_test_login")
        raise error  # enviamos el error



# TEST 1 — Verificación del catálogo de productos


def test_catalogo_productos(driver):
    try:
        # hacemos login para llegar al catálogo
        hacer_login(driver)

        # Esperar a que cargue la página de inventario
        esperar_elemento(driver, By.CLASS_NAME, "inventory_list")

        # ── Validar título de la sección ───────────────────────────────────
        titulo_seccion = esperar_elemento(driver, By.CLASS_NAME, "title")
        assert titulo_seccion.text == "Products", (
            f"Título incorrecto: '{titulo_seccion.text}'"
        )

        # ── Validar que haya al menos un producto ──────────────────────────
        productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(productos) > 0, "No se encontraron productos en el catálogo"

        # ── Imprimir nombre y precio del primer producto ───────────────────
        primer_nombre = driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text
        primer_precio = driver.find_elements(By.CLASS_NAME, "inventory_item_price")[0].text
        print(f"\n Primer producto: {primer_nombre} — {primer_precio}")

        # ── Validar presencia del menú (botón hamburguesa) ─────────────────
        menu_boton = driver.find_element(By.ID, "react-burger-menu-btn")
        assert menu_boton.is_displayed(), "El menú hamburguesa no está visible"

        # ── Validar presencia del filtro de ordenamiento ───────────────────
        filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
        assert filtro.is_displayed(), "El selector de filtro no está visible"

        print(f"Catálogo verificado con {len(productos)} productos.")

    except Exception as error:
        tomar_captura(driver, "fallo_test_catalogo")
        raise error


# TEST 3 — Interacción con el carrito de compras

def test_agregar_producto_al_carrito(driver):
    try:
        # Hacer login
        hacer_login(driver)
        esperar_elemento(driver, By.CLASS_NAME, "inventory_list")

        # ── Agregar primer producto y guardar su nombre ────────────────────
        nombre_producto = agregar_primer_producto(driver)
        print(f"\n🛒 Producto agregado: {nombre_producto}")

        # ── Verificar que el carrito muestre "1" ─────────────────
        badge_carrito = esperar_elemento(
            driver, By.CLASS_NAME, "shopping_cart_badge"
        )
        assert badge_carrito.text == "1", (
            f"Contador del carrito esperado: '1', obtenido: '{badge_carrito.text}'"
        )

        # ── Navegar al carrito haciendo clic en el ícono ───────────────────
        icono_carrito = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        icono_carrito.click()

        # ── Esperar que cargue la página del carrito ───────────────────────
        esperar_elemento(driver, By.CLASS_NAME, "cart_list")

        # Verificar que la URL corresponda al carrito
        assert "cart.html" in driver.current_url, (
            f"No se navegó al carrito. URL actual: {driver.current_url}"
        )

        # ── Verificar que el producto aparece en el carrito ────────────────
        items_en_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(items_en_carrito) == 1, (
            f"Se esperaba 1 item en el carrito, hay: {len(items_en_carrito)}"
        )

        # Verificar que el nombre del producto en el carrito coincide
        nombre_en_carrito = driver.find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).text
        assert nombre_en_carrito == nombre_producto, (
            f"Producto incorrecto en carrito. Esperado: '{nombre_producto}', "
            f"obtenido: '{nombre_en_carrito}'"
        )

        print(f" Carrito verificado. Producto '{nombre_en_carrito}' esta presente.")

    except Exception as error:
        tomar_captura(driver, "fallo_test_carrito")
        raise error