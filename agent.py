import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()
from google import genai
from google.genai import types
from google.genai.errors import ServerError

from tools import get_database_schema,execute_sql_query

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: No se encontro la variable de entorno 'GEMINI_API_KEY'.")
    print("Verefica tu archivo .env o variable de sistema")
    sys.exit(1)

client = genai.Client(api_key=api_key)

MODELO_ACTIVO = "gemini-3.6-flash"

SYSTEM_INSTRUCTION="""
Eres un asistente administrativo especializado en la gestion de un consultorio de psicologia/terapia,con base de datos SQLite.
Tu objetivo es responder con precision a preguntas administrativas formuladas por usuarios, utilizando las herraminetas a tu disposicion.

Sigue rigurosamnete estas reglas de operacion:
1.Siempre invoca primero 'get_database_schema' si no conoces o necesitas validar los nombres exactos de tablas y columnas.
2.Recuerda que el campo 'estado' de la tabla citas solo puede tener estos valores:
  -'pendiente'
  -'confirmada'
  -'cancelada'
3. Las relaciones entre tablas son:Terapeutas.id_consultorio -> Consultorios.id_consultorio, y Citas.id_consultorio/id_terapeuta/id_paciente -> Consultorios/Terapeutas/Pacientes respectivamente
4. Construye consultas SQL compatibles con la sintaxis de SQLite.
5. NUNCA intentes ejecutar sentencias de escritura (INSERT, UPDATE, DELETE, DROP). Solo tienes permisos SELECT.
6. Si 'execute_sql_query' devuelve un error de sintaxis o columna, lee con atencion el mensaje de error, corrige tu consulta y vuelve a intentar (autorreparacion).
7. Presenta tu respuesta final en espanol, de forma clara, profesional y estructurada (usa vinetas o tablas de texto si es util).
8. Nunca inventes ni asumas informacion clinica o de diagnostico; solo maneja datos administrativos (agenda, precios, disponibilidad, contacto).
"""

def _enviar_mensaje_con_reintento(chat, mensaje_o_parte, max_intentos: int =4):
    demora=2
    for intento in range(max_intentos):
        try:
            return chat.send_message(mensaje_o_parte)
        except ServerError as e:
            if "503" in str(e) and intento < max_intentos -1:
                print(f"[Aviso] Servidor con alta demanda. Reintentaloen {demora} segundos...")
                time.sleep(demora)
                demora *=2
            else:
                raise e

def preguntar_al_agente(pregunta:str, verbose: bool = True) ->str:
    herramientas_disponibles={
        "get_database_schema": get_database_schema,
        "execute_sql_query": execute_sql_query, 
    }

    chat = client.chats.create(
        model=MODELO_ACTIVO,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.1,
            tools=[get_database_schema, execute_sql_query],
        ),
    )

    if verbose:
        print(f"\n[Usuario]:{pregunta}")
        print("-" *60)

    response =_enviar_mensaje_con_reintento(chat,pregunta)

    while response.function_calls:
        for function_call in response.function_calls:
            func_name = function_call.name
            func_args = function_call.args

            if verbose:
                print(f"[Agente de accion]Invocando herramientas:'{func_name}'")
                if func_args:
                    print(f"Argumentos:{dict(func_args)}")

            if func_name in herramientas_disponibles:
                tool_output = herramientas_disponibles[func_name](**func_args)
            else:
                tool_output =f"Error Herramienta'{func_name}' no reconocida."

            if verbose:
                vista_previa= str(tool_output).strip().replace("\n","")
                if len(vista_previa) >120:
                    vista_previa = vista_previa[:120] +"..."
                print(f"[Observacion]:{vista_previa}\n")

            response = _enviar_mensaje_con_reintento(
                chat,
                types.Part.from_function_response(
                    name=func_name,
                    response={"result": tool_output},    
                ),
            )

    return response.text

if __name__ == "__main__":
    print(f"Iniciando prueba del agente DBA con modelo:{MODELO_ACTIVO}...\n")

    consulta_prueba=(
    "¿Cual es la tarifa mas alta y cuales son las direcciones de los consultorios?"
    )

    respuesta= preguntar_al_agente(consulta_prueba, verbose=True)

    print("\n" + "=" * 60)
    print("[RESPUESTA FINAL DEL AGENTE]:")
    print("=" * 60)
    print(respuesta)