import sqlite3 
from datetime import datetime

def get_connection(db_path: str = "consultorio_django.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn 

def init_db(db_path: str = "consultorio_django.db") -> None:
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Terapeutas; ")
    cursor.execute("DROP TABLE IF EXISTS Consultorios;")
    cursor.execute("DROP TABLE IF EXISTS PACIENTES;")
    cursor.execute("DROP TABLE IF EXISTS CITAS;")

    cursor.execute("""
    Create table Terapeutas(
        id_terapeuta integer primary key autoincrement,
        nombre varchar(100) not null,
        apellido varchar(100) not null,
        especialidad varchar(100)not null,
        tarifa decimal(10,2)not null,
        estado boolean not null default 1,
        id_consultorio integer not null,
        FOREIGN KEY (id_consultorio) REFERENCES Consultorios(id_consultorio)
        )
        """)

    cursor.execute("""
    CREATE TABLE Consultorios(
        id_consultorio integer primary key autoincrement,
        direccion varchar(100)not null,
        numero_consultorio integer not null,
        estado boolean not null default 1);
        """
    )

    cursor.execute("""
    CREATE TABLE PACIENTES(
    id_paciente integer primary key autoincrement,
    nombre varchar(100) not null,
    apellido varchar(100) not null,
    direccion varchar(100) not null,
    telefono varchar(15) not null,
    email varchar(100) not null,
    estatus boolean not null default 1
    );
    """)

    cursor.execute("""
    CREATE TABLE CITAS(
    id_cita integer primary key autoincrement,
    fecha_cita datetime not null default current_timestamp,
    precio decimal(10,2)not null,
    estado varchar(20) not null check (estado in ('pendiente','confirmada','cancelada')) default'pendiente',
    id_consultorio integer not null,
    id_terapeuta integer not null,
    id_paciente integer not null,
    FOREIGN KEY (id_consultorio) REFERENCES Consultorios(id_consultorio),
    FOREIGN KEY (id_terapeuta) REFERENCES Terapeutas(id_terapeuta),
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente)
    );
    """)

    conn.commit()
    conn.close()
    print("TABLAS CREADAS CON EXITO")

def seed_db(db_path: str = "consultorio_django.db")-> None:
    conn = get_connection(db_path)
    cursor = conn.cursor()

    consultorios=[
            ("Av. Insurgentes Sur 1234",1,1),
            ("Calle Reforma 5678",2,1),
            ("Av. Juarez 91011",3,1),
            ("Calle Hidalgo 1213",4,1),
            ("Av. Revolucion 1415",5,1),
    ]
    cursor.executemany("""
    INSERT INTO Consultorios(direccion,numero_consultorio,estado)
    VALUES(?,?,?);
    """, consultorios)
    

    Terapeutas=[
                ("Cristal","Vargas","Psicologia clinica",1,800.00,1),
                ("Juan","Perez","Terapia ocupacional",2,600.00,1),
                ("Maria","Gonzalez","Psicologia del desarrollo",3,700.00,1),
                ("Aketzalli","Rangel","Psicologa infaltil",4,1000.00,1),
                ("Esmeralda","Lopez","Psicologa cognitiva",5,700.00,1),
    ]
    cursor.executemany("""
    INSERT INTO Terapeutas(nombre,apellido,especialidad,id_consultorio,tarifa,estado)
    VALUES(?,?,?,?,?,?);
    """, Terapeutas)


    pacientes=[
        ("Luis","Martinez","Calle veracruz 123","477-111-2222","luis.martinez@gmail.com",1),
        ("Fernando","Ramirez","San Juan Bosco 456","477-510-7813","fernando.ramirez@gmail.com",1),
        ("Emiliano","Zapata","Calle Hidalgo 789","477-111-2222","emiliano.zapata@gmail.com",1),
    ]

    cursor.executemany("""
    INSERT INTO Pacientes(nombre,apellido,direccion,telefono,email,estatus)
    VALUES(?,?,?,?,?,?);
    """, pacientes)

    citas=[
        ("2026-09-29 10:00:00",800.00,"pendiente",1,1,1),
        ("2026-09-30 15:00:00",600.00,"confirmada",2,2,2),
        ("2026-10-03 19:00:00",700.00,"cancelada",3,3,3),
    ]

    cursor.executemany("""
    INSERT INTO Citas(fecha_cita, precio, estado, id_consultorio, id_terapeuta, id_paciente)
    VALUES(?,?,?,?,?,?);
    """, citas)

    conn.commit()
    conn.close()
    print("Datos insertados con exito")

if __name__ == "__main__":
    init_db()
    seed_db()