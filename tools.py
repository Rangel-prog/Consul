import sqlite3
import json
from typing import Dict, Any

DB_NAME="consultorio_django.db"

def get_database_schema(db_path: str = DB_NAME)-> str:

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT name, sql
        from sqlite_master
        where type = 'table' and name not like 'sqlite_%';
        """)
        tables= cursor.fetchall()
        conn.close()

        if not tables:
            return "No se encontraron tablas en la base de datos."

        schema_description=[]
        for table_name, create_sql in tables:
            schema_description.append(f"---Tabla:{table_name}---")
            schema_description.append(create_sql.strip())
            schema_description.append("")

        return "\n".join(schema_description)
    except sqlite3.Error as e:
        return f"Error al leer el esquema de la base de datos: {str(e)}"

def execute_sql_query(query: str, db_path: str =DB_NAME)-> str:

    cleaned_query= query.strip()

    first_word = cleaned_query.split()[0].upper() if cleaned_query else""
    if first_word not in ("SELECT","WITH"):
        return(
            "Error de Seguridad: Operacion no permitida."
            "El usuario solo tiene permisos de lectura('Select')."
            "Operaciones como Insert,Update,DELET o Drop estan bloqueadas."
        )

    palabras_prohibidas=["DROP","DELETE","TRUNCATE","ALTER","INSERT","UPDATE","PRAGMA","ATTACH","CREATE","REPLACE"]
    cleaned_query = cleaned_query.replace(";"," ")
    tokens = [token.strip(";").upper() for token in cleaned_query.split()]
    for palabra in palabras_prohibidas:
        if palabra in tokens:
         return f"Error de Seguridad: la consulta contiene la instruccion prohibida '{palabra}'."

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(cleaned_query)
        rows = cursor.fetchall()
        conn.close()

        resultados =[dict(row) for row in rows]

        if not resultados:
            return "La consulta no arrojo registros."
        return json.dumps(resultados, ensure_ascii=False, indent=2)
    except sqlite3.Error as e:
        return f"Error de sintaxis en SQLite:{str(e)}"

if __name__ =="__main__":
    print("=== 1.PRUEBA DE ESQUEMA ===")
    print(get_database_schema())

    print("\n=== 2. PRUEBA DE CONSULTA VALIDA ===")
    test_query = "SELECT nombre,apellido, tarifa from Terapeutas where tarifa>700;"
    print(execute_sql_query(test_query))

    print("\n=== 3. PRUEBA DE BLOQUEO DE SEGURIDAD ===")
    malicious_query = "DELETE FROM Terapeutas WHERE id = 1;"
    print(execute_sql_query(malicious_query))

