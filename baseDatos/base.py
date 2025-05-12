import sqlite3

def conectar_db():
    return sqlite3.connect("biblioteca.db")

def crear_tablas(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS libros (
        id_libro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        genero TEXT,
        anio_publicacion INTEGER
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prestamos (
        id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        id_libro INTEGER,
        fecha_prestamo TEXT,
        fecha_devolucion TEXT,
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario),
        FOREIGN KEY(id_libro) REFERENCES libros(id_libro)
    )""")
    conn.commit()

def agregar_usuario(conn):
    nombre = input("Nombre: ")
    email = input("Email: ")
    conn.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
    conn.commit()
    print("✅ Usuario agregado.\n")

def agregar_libro(conn):
    titulo = input("Título: ")
    autor = input("Autor: ")
    genero = input("Género: ")
    anio = int(input("Año de publicación: "))
    conn.execute("INSERT INTO libros (titulo, autor, genero, anio_publicacion) VALUES (?, ?, ?, ?)",
                 (titulo, autor, genero, anio))
    conn.commit()
    print("✅ Libro agregado.\n")

def prestar_libro(conn):
    id_usuario = int(input("ID del usuario: "))
    id_libro = int(input("ID del libro: "))
    fecha_prestamo = input("Fecha de préstamo (YYYY-MM-DD): ")
    fecha_devolucion = input("Fecha de devolución (YYYY-MM-DD): ")
    conn.execute("INSERT INTO prestamos (id_usuario, id_libro, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?)",
                 (id_usuario, id_libro, fecha_prestamo, fecha_devolucion))
    conn.commit()
    print("✅ Préstamo registrado.\n")

def ver_tablas(conn):
    print("\n📚 Libros:")
    for fila in conn.execute("SELECT * FROM libros"):
        print(fila)
    
    print("\n👤 Usuarios:")
    for fila in conn.execute("SELECT * FROM usuarios"):
        print(fila)

    print("\n📦 Préstamos:")
    for fila in conn.execute("""
        SELECT u.nombre, l.titulo, p.fecha_prestamo, p.fecha_devolucion
        FROM prestamos p
        JOIN usuarios u ON p.id_usuario = u.id_usuario
        JOIN libros l ON p.id_libro = l.id_libro
    """):
        print(fila)
    print()

def menu():
    conn = conectar_db()
    crear_tablas(conn)

    while True:
        print("=== MENÚ BIBLIOTECA ===")
        print("1. Agregar usuario")
        print("2. Agregar libro")
        print("3. Registrar préstamo")
        print("4. Ver datos")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_usuario(conn)
        elif opcion == "2":
            agregar_libro(conn)
        elif opcion == "3":
            prestar_libro(conn)
        elif opcion == "4":
            ver_tablas(conn)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida.\n")

    conn.close()

# Ejecutar el menú
menu()
