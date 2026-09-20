import sqlite3
import sys

# Name of the database file
DB_NAME = "biblioteca.db"

def conectar_bd():
    """Crea la conexión a la base de datos y genera la tabla si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT NOT NULL CHECK(estado IN ('Leído', 'No leído'))
        )
    """
    )
    conn.commit()
    return conn


def agregar_libro(conn):
    """Agrega un nuevo libro a la base de datos."""
    print("\n--- Agregar Nuevo Libro ---")
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    genero = input("Género: ").strip()

    if not titulo or not autor or not genero:
        print("❌ Error: Todos los campos son obligatorios.")
        return

    print("Estado de lectura:")
    print("1. Leído")
    print("2. No leído")
    opcion_estado = input("Selecciona una opción (1/2): ").strip()

    estado = "Leído" if opcion_estado == "1" else "No leído"

    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO libros (titulo, autor, genero, estado)
        VALUES (?, ?, ?, ?)
    """,
        (titulo, autor, genero, estado),
    )
    conn.commit()
    print(f"✅ ¡Libro '{titulo}' agregado con éxito!")


def ver_libros(conn):
    """Muestra todos los libros registrados."""
    print("\n--- Listado de Libros ---")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, titulo, autor, genero, estado FROM libros ORDER BY id ASC"
    )
    libros = cursor.fetchall()

    if not libros:
        print("📖 No hay libros registrados en la biblioteca.")
        return

    print("-" * 70)
    print(
        f"{'ID':<4} | {'Título':<25} | {'Autor':<20} | {'Género':<10} | {'Estado':<10}"
    )
    print("-" * 70)
    for libro in libros:
        print(
            f"{libro[0]:<4} | {libro[1]:<25} | {libro[2]:<20} | {libro[3]:<10} | {libro[4]:<10}"
        )
    print("-" * 70)


def buscar_libros(conn):
    """Busca libros por título, autor o género."""
    print("\n--- Buscar Libros ---")
    criterio = input("Ingresa término de búsqueda (Título, Autor o Género): ").strip()

    if not criterio:
        print("❌ El término de búsqueda no puede estar vacío.")
        return

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, titulo, autor, genero, estado 
        FROM libros 
        WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ?
    """,
        (f"%{criterio}%", f"%{criterio}%", f"%{criterio}%"),
    )

    libros = cursor.fetchall()

    if not libros:
        print(f"🔍 No se encontraron coincidencias para '{criterio}'.")
        return

    print("\nResultados encontrados:")
    print("-" * 70)
    print(
        f"{'ID':<4} | {'Título':<25} | {'Autor':<20} | {'Género':<10} | {'Estado':<10}"
    )
    print("-" * 70)
    for libro in libros:
        print(
            f"{libro[0]:<4} | {libro[1]:<25} | {libro[2]:<20} | {libro[3]:<10} | {libro[4]:<10}"
        )
    print("-" * 70)


def actualizar_libro(conn):
    """Modifica la información o estado de un libro existente."""
    ver_libros(conn)
    print("\n--- Actualizar Libro ---")
    try:
        libro_id = int(
            input("Ingresa el ID del libro que deseas actualizar: ").strip()
        )
    except ValueError:
        print("❌ Error: Debes ingresar un ID numérico válido.")
        return

    cursor = conn.cursor()
    cursor.execute(
        "SELECT titulo, autor, genero, estado FROM libros WHERE id = ?",
        (libro_id,),
    )
    libro = cursor.fetchone()

    if not libro:
        print(f"❌ No existe ningún libro con el ID {libro_id}.")
        return

    print("\nDeja el campo en blanco si no deseas modificarlo.")
    nuevo_titulo = input(f"Nuevo Título [{libro[0]}]: ").strip() or libro[0]
    nuevo_autor = input(f"Nuevo Autor [{libro[1]}]: ").strip() or libro[1]
    nuevo_genero = input(f"Nuevo Género [{libro[2]}]: ").strip() or libro[2]

    print(f"Estado actual: {libro[3]}")
    print("1. Leído")
    print("2. No leído")
    print("3. Mantener actual")
    opc_estado = input("Selecciona opción de estado (1/2/3): ").strip()

    if opc_estado == "1":
        nuevo_estado = "Leído"
    elif opc_estado == "2":
        nuevo_estado = "No leído"
    else:
        nuevo_estado = libro[3]

    cursor.execute(
        """
        UPDATE libros 
        SET titulo = ?, autor = ?, genero = ?, estado = ?
        WHERE id = ?
    """,
        (nuevo_titulo, nuevo_autor, nuevo_genero, nuevo_estado, libro_id),
    )

    conn.commit()
    print(f"✅ ¡El libro con ID {libro_id} ha sido actualizado correctamente!")


def eliminar_libro(conn):
    """Elimina un libro de la base de datos por su ID."""
    ver_libros(conn)
    print("\n--- Eliminar Libro ---")
    try:
        libro_id = int(
            input("Ingresa el ID del libro que deseas eliminar: ").strip()
        )
    except ValueError:
        print("❌ Error: Debes ingresar un ID numérico válido.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT titulo FROM libros WHERE id = ?", (libro_id,))
    libro = cursor.fetchone()

    if not libro:
        print(f"❌ No existe ningún libro con el ID {libro_id}.")
        return

    confirmacion = (
        input(
            f"⚠️ ¿Estás seguro de que deseas eliminar '{libro[0]}'? (s/n): "
        )
        .strip()
        .lower()
    )
    if confirmacion == "s":
        cursor.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
        conn.commit()
        print(f"🗑️ Libro '{libro[0]}' eliminado con éxito.")
    else:
        print("Cancelado. El libro no ha sido eliminado.")


def mostrar_menu():
    """Despliega las opciones del menú principal."""
    print("\n" + "=" * 35)
    print(" 📚 GESTOR DE BIBLIOTECA PERSONAL ")
    print("=" * 35)
    print("1. Agregar nuevo libro")
    print("2. Ver todos los libros")
    print("3. Buscar libros")
    print("4. Actualizar libro")
    print("5. Eliminar libro")
    print("6. Salir")
    print("=" * 35)


def main():
    """Función principal que controla el flujo del programa."""
    conn = conectar_bd()

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción (1-6): ").strip()

        if opcion == "1":
            agregar_libro(conn)
        elif opcion == "2":
            ver_libros(conn)
        elif opcion == "3":
            buscar_libros(conn)
        elif opcion == "4":
            actualizar_libro(conn)
        elif opcion == "5":
            eliminar_libro(conn)
        elif opcion == "6":
            print("\n👋 ¡Gracias por usar la biblioteca personal! Hasta luego.")
            conn.close()
            sys.exit()
        else:
            print("❌ Opción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    main()