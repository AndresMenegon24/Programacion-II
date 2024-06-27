## ALUMNOS: ANDRES MENEGON Y CLAUDIO MAZA

## Archivos y Directorios Principales

- **`app.py`**: Configuración principal de la aplicación Flask.
- **`config.py`**: Configuración de la base de datos y otros parámetros.
- **`models.py`**: Definición de los modelos de la base de datos.
- **`forms.py`**: Definición de los formularios de la aplicación.
- **`run.py`**: Script para iniciar la aplicación.
- **`routes.py`**: Definición de las rutas y lógica de la aplicación.
- **`/templates`**: Directorio que contiene los archivos HTML.
- **`/static`**: Directorio que contiene archivos estáticos como CSS e imágenes.

## Uso

1. **Iniciar la aplicación:**

    ```bash
    python run.py
    ```

2. **Acceder a la aplicación:**

    Abre tu navegador web y navega a `http://127.0.0.1:5000`.

3. **Iniciar sesión:**

    - Navega a `http://127.0.0.1:5000/login`.
    - Utiliza las credenciales:
        - **Usuario**: `admin`
        - **Contraseña**: `1234`

4. **Cerrar sesión:**

    - Haz clic en `Cerrar Sesión` en el menú de navegación.

5. **Registrar un nuevo caso:**

    - Navega a `Registrar Caso` en el menú de navegación.
    - Completa el formulario y haz clic en `Registrar`.

6. **Ver casos registrados:**

    - Navega a `Ver Casos` en el menú de navegación.
    - Visualiza los casos registrados y los gráficos generados.

## Personalización

- **Estilos CSS**: Puedes personalizar el estilo de la aplicación editando el archivo `static/css/styles.css`.
- **Plantillas HTML**: Puedes modificar las plantillas HTML en el directorio `templates` para cambiar el diseño de las páginas.

## Gráficos

La aplicación utiliza Chart.js para generar gráficos que ayudan a visualizar los datos epidemiológicos de manera clara y efectiva. Los gráficos incluyen:
- Zonas con mayor riesgo epidemiológico.
- Agrupación por grupos.
- Agrupación por género.
- Agrupación por rangos etarios.
- Estado de ingreso por barrio.
- Relación entre grupo y barrio.
- Relación entre edad, grupo y barrio.

## Autenticación

Se ha añadido una funcionalidad de autenticación básica que requiere que los usuarios inicien sesión antes de acceder a ciertas partes de la aplicación. Las credenciales por defecto son:
- **Usuario**: `admin`
- **Contraseña**: `1234`

Para cerrar sesión, simplemente haz clic en `Cerrar Sesión` en el menú de navegación.
