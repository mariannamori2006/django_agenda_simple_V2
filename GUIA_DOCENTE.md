# Agenda Simple V2 — Guía de instalación y explicación docente

## 1. ¿Qué se conserva?
Se mantiene el proyecto `config`, la aplicación `apps`, las rutas (`apps/urls.py`), las vistas basadas en funciones, el login/logout, la protección CSRF, el CSS y el CRUD de clientes y citas. No se incluye `.venv`: se crea en cada computadora.

## 2. ¿Qué cambió y por qué?
1. **`apps/models/Cliente.py`**: tabla SQL `clientes`, clave primaria `id` de tipo INT, nombre, apellido, correo (150), dni (20), teléfono (30) y fechas automáticas. Se eliminaron edad y peso.
2. **`apps/models/Cita.py`**: tabla SQL `citas`, clave `id`, columna `client_id` como clave foránea, asunto (200), fecha DATE, hora TIME, dirección (255), referencia (255), notas TEXT, estado y fechas automáticas. Se eliminaron tipo de reunión y enlace virtual.
3. **`apps/views.py`**: el CRUD ahora recibe los nuevos nombres de campos, valida fecha/hora por separado y busca por asunto y estado. Se mantiene la regla de no eliminar clientes con citas.
4. **`apps/templates/control/clientes.html` y `citas.html`**: formularios y tablas muestran únicamente los nuevos campos. Se conservan los botones, rutas y CSRF.
5. **`apps/static/control/js/app.js`**: se conserva la confirmación de eliminación; se elimina la lógica de mostrar campos para reuniones virtuales.
6. **`config/settings.py`**: se cambia únicamente el nombre de la base de datos a `agenda_simple_v2_db`. Revisa usuario, contraseña y puerto para tu instalación local.
7. **`apps/migrations/0001_initial.py`**: migración inicial nueva para crear las tablas en una base independiente; no se ejecutan las migraciones antiguas de V1.

## 3. Instalación en otra PC (PowerShell)
Descomprimir en `C:\xampp\htdocs\agenda_simple_v2` (o cualquier carpeta). Abrir esa carpeta en VS Code y ejecutar:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si deseas activar el entorno y PowerShell lo impide, usa `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y luego `.\.venv\Scripts\Activate.ps1`. **No necesitas activarlo** para ejecutar los comandos siguientes.

## 4. Crear la base de datos
En phpMyAdmin o en la consola SQL del servidor MariaDB/MySQL **compatible con Django 6**, ejecutar:

```sql
CREATE DATABASE agenda_simple_v2_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Verificar en `config/settings.py` que HOST, PORT, USER y PASSWORD coincidan con tu servidor. El proyecto original usa `127.0.0.1`, puerto `3307`, usuario `root` y una contraseña configurada en settings; no son necesariamente los datos de la nueva PC.

## 5. Crear tablas y ejecutar

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Abrir `http://127.0.0.1:8000/` e iniciar sesión con el superusuario creado.

## 6. Práctica guiada para alumnos
1. Abrir `models/Cliente.py` y explicar campos, longitudes, clave primaria y `auto_now_add`/`auto_now`.
2. Abrir `models/Cita.py` y explicar relación 1:N: un cliente tiene varias citas y cada cita pertenece a un cliente.
3. Comparar `db_column="client_id"` con el atributo Python `cliente` (en la base SQL la columna se llama `client_id`).
4. Explicar `makemigrations` (prepara migraciones) y `migrate` (crea tablas en MariaDB).
5. Abrir `views.py` y seguir el flujo POST → validación → ORM → mensaje → redirect.
6. Abrir los HTML y señalar `name` de cada input, `{% csrf_token %}`, edición y búsqueda.
7. Probar: crear cliente → crear cita → editar cita → buscar → intentar borrar cliente con citas → borrar cita → borrar cliente.

## 7. Notas de interpretación del diagrama
- `estado ENUM(...)` no muestra los valores en la imagen: se adoptaron **Pendiente, Confirmada, Completada, Cancelada** mediante `choices` de Django. Esto se guarda como VARCHAR en MariaDB, no como un ENUM nativo.
- `referencia VARCHAR(25...)` aparece truncado en la captura: se ha usado VARCHAR(255). Ajusta `max_length` si el diagrama original establece otra longitud.
- La imagen no indica claramente qué columnas permiten NULL; se dejó `telefono`, `referencia` y `notas` como opcionales, y el resto como obligatorias.
- DNI se conserva con validación peruana de 8 dígitos del proyecto original, aunque la columna permite hasta 20 caracteres.
- No se migran datos de V1 a V2: es una instalación nueva con base independiente.
