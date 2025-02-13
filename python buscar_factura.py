import psycopg2

# ✅ URL de la base de datos PostgreSQL en Render
DATABASE_URL = "postgresql://backup_aldaba_user:vcSsT1eWkj76ZBQTxNPvh0ehbSiKAzX5@dpg-cumn5maj1k6c73b0jofg-a.oregon-postgres.render.com/backup_aldaba"

def conectar_db():
    """Establece conexión con la base de datos PostgreSQL en Render."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")
        return None

def buscar_factura(factura_no):
    """Busca una factura en la tabla 'ventas' y devuelve los detalles."""
    conn = conectar_db()
    if not conn:
        return None
    
    cursor = conn.cursor()

    try:
        print(f"📌 Buscando factura {factura_no} en la tabla 'ventas'...")

        # 🔍 Consultar la tabla 'ventas' para traer los datos correctos
        cursor.execute("""
            SELECT factura_no, nombre, estado, total, saldo
            FROM ventas
            WHERE factura_no = %s;
        """, (factura_no,))

        resultado = cursor.fetchone()

        if resultado:
            print(f"✅ Factura encontrada: {resultado}")
            return {
                "success": True,
                "factura": resultado[0],
                "cliente": resultado[1],
                "estado": resultado[2],
                "total": resultado[3],
                "saldo": resultado[4]
            }
        else:
            print(f"❌ No se encontró la factura {factura_no} en la base de datos.")
            return {"success": False, "message": f"No se encontró la factura {factura_no} en la base de datos."}

    except Exception as e:
        print(f"❌ Error en la consulta SQL: {e}")
        return {"success": False, "message": "Error en la consulta SQL."}

    finally:
        cursor.close()
        conn.close()