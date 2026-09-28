# Droguería Flask

Este proyecto es una aplicación web para gestionar productos de una droguería con Flask, SQLite y plantillas HTML.

## Requisitos

- Python 3.10 o superior
- Git
- Cuenta de GitHub

## 1) Crear entorno virtual

En la carpeta del proyecto ejecuta:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2) Instalar dependencias

```bash
pip install flask
```

## 3) Ejecutar la aplicación

```bash
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:5001
```

## 4) Iniciar sesión

El proyecto ya incluye un usuario por defecto:

- Correo: `admin@drogueria.com`
- Contraseña: `admin123`

## 5) Subir el proyecto a GitHub

Si el repositorio es de otra persona y tú quieres subirlo desde tu cuenta, la forma correcta es hacer un fork o que esa persona haga push desde su cuenta.

### Opción recomendada: subir desde la cuenta de la persona dueña del repositorio

```bash
git init
git branch -M main
git checkout -b feature/login-y-estilos
git add .
git commit -m "Agregar login y estilos de la app"
git remote add origin https://github.com/mapasariza09-collab/DrogueriaFlask.git
git push -u origin feature/login-y-estilos
```

Después, en GitHub aparece la opción de hacer Pull Request para unir la rama con `main`.

### Si no tienes permisos para hacer push directo

Haz fork del repositorio original a tu cuenta y luego cambia el remote:

```bash
git remote set-url origin https://github.com/TU_USUARIO/DrogueriaFlask.git
git push -u origin feature/login-y-estilos
```

Luego se puede abrir un Pull Request desde tu fork hacia el repositorio original.

## 6) Ignorar archivos locales

Se recomienda ignorar la carpeta `.venv` y la base de datos local para no subir información local del desarrollo.

Archivo `.gitignore` recomendado:

```gitignore
.venv/
__pycache__/
*.pyc
*.db
```

## 7) Estructura del proyecto

```text
Drogueria/
├── app.py
├── requirements.txt
├── .gitignore
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── form_producto.html
│   ├── layout.html
│   ├── login.html
│   ├── productos.html
│   └── registro.html
└── README.md
```

## 8) Funcionalidades actuales

- Login con usuario y contraseña
- Registro de usuarios
- Protección de rutas con sesión
- Listado de productos
- Agregar, editar y eliminar productos
- Diseño adaptado y mensajes de alerta con cierre

## 9) Nota importante

La base de datos SQLite se crea automáticamente al ejecutar la aplicación si no existe. Por eso no se recomienda subir el archivo `drogueria.db` al repositorio.
