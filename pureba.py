import psycopg2

# 🔹 URL de la base de datos en Render
DATABASE_URL = "postgresql://backup_aldaba_user:vcSsT1eWkj76ZBQTxNPvh0ehbSiKAzX5@dpg-cumn5maj1k6c73b0jofg-a.oregon-postgres.render.com/backup_aldaba"

def obtener_conexion():
    """Conecta a PostgreSQL y devuelve la conexión."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def imprimir_tablas_y_contenido():
    """Imprime todas las tablas y su contenido en PostgreSQL."""
    conn = obtener_conexion()
    if not conn:
        return

    cursor = conn.cursor()

    try:
        # 🔹 Obtener todas las tablas en la base de datos
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
        tablas = cursor.fetchall()

        print("\n📌 **Tablas en la base de datos:**")
        for tabla in tablas:
            nombre_tabla = tabla[0]
            print(f"🔹 Tabla: {nombre_tabla}")

            # 🔍 Obtener contenido de cada tabla
            cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 10;")  # Solo 10 filas para no saturar
            filas = cursor.fetchall()

            if filas:
                print(f"📌 **Contenido de {nombre_tabla} (10 filas):**")
                for fila in filas:
                    print(fila)
            else:
                print(f"⚠ La tabla {nombre_tabla} está vacía.")

            print("-" * 50)  # Separador visual entre tablas

    except Exception as e:
        print(f"❌ Error al consultar la base de datos: {e}")

    finally:
        cursor.close()
        conn.close()

# 🔥 Ejecutar la función
imprimir_tablas_y_contenido()
