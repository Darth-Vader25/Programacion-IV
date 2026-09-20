# 📚 Sistema de Gestión de Biblioteca Personal

Aplicación de línea de comandos (CLI) desarrollada en Python y SQLite para administrar la colección de libros de una biblioteca personal de forma sencilla y eficiente.

## 📌 Características principales
- **Agregar libros**: Registrar nuevo libro definiendo título, autor, género y estado (`Leído` / `No leído`).
- **Listar colección**: Visualizar la lista completa de libros con su respectivo ID único.
- **Búsqueda flexible**: Búsqueda mediante palabras clave por *Título*, *Autor* o *Género*.
- **Actualizar datos**: Modificar campos específicos o cambiar el estado de lectura de un libro seleccionado.
- **Eliminar libros**: Quitar registros obsoletos con confirmación de seguridad.
- **Persistencia de datos**: Todos los datos se guardan de forma permanente en SQLite (`biblioteca.db`).

## 🛠️ Requisitos e Instalación

### Requisitos previos
- **Python 3.x** instalado en el sistema.
- La biblioteca estándar `sqlite3` viene preinstalada con Python (no requiere instalaciones de dependencias de terceros).

### Ejecución del programa

1. Clona o descarga este repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/biblioteca-personal.git](https://github.com/tu-usuario/biblioteca-personal.git)
   cd biblioteca-personal
