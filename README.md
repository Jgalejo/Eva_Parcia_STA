# EVA_Parcia_STA

**Proyecto Django** orientado al desarrollo y la demostración. Incluye una aplicación sencilla implementada con Arquitectura de 3 Capas, organizada en la siguiente estructura principal: `business/`, `config/`, `core/`, `presentation/`.

---

## 🔧 Requisitos

- Python 3.10+ (recomendado)
- pip

Instalar dependencias:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

## 🚀 Instalación y ejecución

1. Aplicar migraciones:

```bash
python manage.py migrate
```

2. Crear usuario administrador (opcional):

```bash
python manage.py createsuperuser
```

3. Ejecutar servidor de desarrollo:

```bash
python manage.py runserver
```

Abre `http://127.0.0.1:8000/` en tu navegador.

> Nota: el proyecto usa una base de datos SQLite por defecto (`db.sqlite3`).


## 📁 Estructura del proyecto

- `business/` — lógica de negocio y validaciones
- `config/` — configuración de Django
- `core/` — modelos y repositorios
- `presentation/` — vistas, serializadores y plantillas
- `manage.py` — utilidad de gestión de Django



## 📝 Licencia

 **MIT**

