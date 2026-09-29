import sqlite3

def conectar_db():
    conexion = sqlite3.connect('gremio_python.db')
    cursor = conexion.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Crear tablas si no existen (omito el DDL completo para brevedad, pero incluye lo básico)
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, clase TEXT NOT NULL, nivel_experiencia INTEGER NOT NULL CHECK (nivel_experiencia > 0)
    );
    CREATE TABLE IF NOT EXISTS misiones (
        id INTEGER PRIMARY KEY, descripcion TEXT NOT NULL, nivel_dificultad INTEGER NOT NULL CHECK (nivel_dificultad BETWEEN 1 AND 10), localizacion TEXT NOT NULL, recompensa_oro INTEGER NOT NULL CHECK (recompensa_oro >= 0)
    );
    CREATE TABLE IF NOT EXISTS monstruos (
        id INTEGER PRIMARY KEY, nombre TEXT NOT NULL, tipo TEXT NOT NULL, nivel_amenaza INTEGER NOT NULL CHECK (nivel_amenaza > 0)
    );
    CREATE TABLE IF NOT EXISTS misiones_heroes (
        mision_id INTEGER, heroe_id INTEGER, PRIMARY KEY (mision_id, heroe_id), FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE, FOREIGN KEY (heroe_id) REFERENCES heroes(id) ON DELETE CASCADE
    );
    CREATE TABLE IF NOT EXISTS misiones_monstruos (
        mision_id INTEGER, monstruo_id INTEGER, PRIMARY KEY (mision_id, monstruo_id), FOREIGN KEY (mision_id) REFERENCES misiones(id) ON DELETE CASCADE, FOREIGN KEY (monstruo_id) REFERENCES monstruos(id) ON DELETE CASCADE
    );
    """)
    return conexion, cursor

def mostrar_menu():
    print("\n--- ⚔️ GREMIO DE AVENTUREROS ---")
    print("1. Ver todos los Héroes")
    print("2. Agregar un nuevo Héroe")
    print("3. Ver todas las Misiones")
    print("4. Agregar una nueva Misión")
    print("5. Ver Monstruos")
    print("6. Ver Reporte Completo (Misiones + Héroes + Monstruos)")
    print("7. Salir")
    return input("Elige una opción (1-7): ")

def ver_heroes(cursor):
    cursor.execute("SELECT id, nombre, clase, nivel_experiencia FROM heroes")
    resultados = cursor.fetchall()
    print("\n--- Lista de Héroes ---")
    for r in resultados:
        print(f"ID: {r[0]} | Nombre: {r[1]} | Clase: {r[2]} | Nivel: {r[3]}")

def agregar_heroe(cursor, conexion):
    print("\n--- Nuevo Héroe ---")
    nombre = input("Nombre: ")
    clase = input("Clase (ej. Guerrero, Mago): ")
    nivel = int(input("Nivel de experiencia (mayor a 0): "))
    try:
        cursor.execute("INSERT INTO heroes (nombre, clase, nivel_experiencia) VALUES (?, ?, ?)", (nombre, clase, nivel))
        conexion.commit()
        print(f"✅ Héroe '{nombre}' agregado exitosamente.")
    except sqlite3.IntegrityError as e:
        print(f"❌ Error al agregar héroe (verifica las restricciones): {e}")

def ver_misiones(cursor):
    cursor.execute("SELECT id, descripcion, nivel_dificultad, localizacion, recompensa_oro FROM misiones")
    resultados = cursor.fetchall()
    print("\n--- Lista de Misiones ---")
    for r in resultados:
        print(f"ID: {r[0]} | {r[1]} | Dificultad: {r[2]} | Lugar: {r[3]} | Oro: {r[4]}")

def agregar_mision(cursor, conexion):
    print("\n--- Nueva Misión ---")
    descripcion = input("Descripción: ")
    dificultad = int(input("Nivel de dificultad (1-10): "))
    localizacion = input("Localización: ")
    recompensa = int(input("Recompensa en oro: "))
    try:
        cursor.execute("INSERT INTO misiones (descripcion, nivel_dificultad, localizacion, recompensa_oro) VALUES (?, ?, ?, ?)", 
                       (descripcion, dificultad, localizacion, recompensa))
        conexion.commit()
        print("✅ Misión agregada exitosamente.")
    except sqlite3.IntegrityError as e:
        print(f"❌ Error al agregar misión: {e}")

def ver_monstruos(cursor):
    cursor.execute("SELECT id, nombre, tipo, nivel_amenaza FROM monstruos")
    resultados = cursor.fetchall()
    print("\n--- Lista de Monstruos ---")
    for r in resultados:
        print(f"ID: {r[0]} | Nombre: {r[1]} | Tipo: {r[2]} | Amenaza: {r[3]}")

def reporte_completo(cursor):
    cursor.execute("""
        SELECT m.descripcion, h.nombre, mon.nombre 
        FROM misiones m
        LEFT JOIN misiones_heroes mh ON m.id = mh.mision_id
        LEFT JOIN heroes h ON mh.heroe_id = h.id
        LEFT JOIN misiones_monstruos mm ON m.id = mm.mision_id
        LEFT JOIN monstruos mon ON mm.monstruo_id = mon.id
        ORDER BY m.id;
    """)
    resultados = cursor.fetchall()
    print("\n--- Reporte de Asignaciones ---")
    for r in resultados:
        heroe = r[1] if r[1] else "Sin héroe"
        monstruo = r[2] if r[2] else "Sin monstruo"
        print(f"Misión: {r[0]} ➜ Héroe: {heroe} | Monstruo: {monstruo}")

def main():
    conexion, cursor = conectar_db()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            ver_heroes(cursor)
        elif opcion == '2':
            agregar_heroe(cursor, conexion)
        elif opcion == '3':
            ver_misiones(cursor)
        elif opcion == '4':
            agregar_mision(cursor, conexion)
        elif opcion == '5':
            ver_monstruos(cursor)
        elif opcion == '6':
            reporte_completo(cursor)
        elif opcion == '7':
            print("Saliendo del sistema del Gremio...")
            conexion.close()
            break
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()