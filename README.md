# 🤖 Pre-entrega Automation Testing — Saucedemo

Automatización de pruebas sobre [saucedemo.com](https://www.saucedemo.com) usando Python, Selenium WebDriver y Pytest.

## Propósito

Validar de forma automatizada los flujos de login, navegación del catálogo e interacción con el carrito de compras.

## Tecnologías

- Python 3.10+
- Selenium WebDriver
- Pytest + pytest-html
- webdriver-manager (descarga automática del driver)
- Git / GitHub

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
# Correr todos los tests con reporte HTML
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

## Estructura

```
├── tests/          → Casos de prueba
├── utils/          → Funciones auxiliares (helpers)
├── reports/        → Reporte HTML y capturas de fallos
├── requirements.txt
└── README.md
```

## Tests incluidos

| Test | Descripción |
|------|-------------|
| `test_login_exitoso` | Login con credenciales válidas y validación de /inventory.html |
| `test_catalogo_productos` | Verifica título, productos, menú y filtros |
| `test_agregar_producto_al_carrito` | Agrega producto, verifica badge y contenido del carrito |