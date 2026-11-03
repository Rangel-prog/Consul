Asistente de Consultorio Médico (AI Agent)

Este proyecto es un asistente virtual basado en Inteligencia Artificial diseñado para un entorno clínico. Utiliza Streamlit para la interfaz de usuario y el modelo Gemini 3.6 Flash a través del SDK google-genai como motor del agente conversacional.

El sistema está diseñado con un enfoque estricto en la seguridad de los datos y la ética médica, permitiendo interactuar en lenguaje natural con la agenda del consultorio sin emitir diagnósticos médicos automatizados.

🚀 Características Principales

Interfaz Conversacional: Construida con Streamlit, permite al personal interactuar fácilmente mediante un chat, incluyendo preguntas sugeridas y un modo de depuración (verbose) para ver el razonamiento del modelo.

Agente de IA Seguro: Configurado con instrucciones estrictas para manejar únicamente datos administrativos (agenda, precios, disponibilidad, contacto). Nunca asume ni inventa información clínica.

Acceso de Solo Lectura y Auto-reparación: Las operaciones en la base de datos están restringidas a sentencias SELECT. Si el agente comete un error de sintaxis SQL, es capaz de leer el error y corregir su propia consulta automáticamente.

Base de Datos Relacional: Utiliza SQLite (consultorio_django.db) con un esquema robusto para gestionar Pacientes, Terapeutas, Consultorios y Citas.

📂 Estructura del Proyecto

app.py: Archivo principal que ejecuta la interfaz gráfica con Streamlit y maneja el estado de la conversación.

agent.py: Contiene la lógica del agente de IA, la configuración del cliente genai, el prompt del sistema y la lógica de invocación de herramientas (Function Calling) con reintentos automáticos.

database.py: Define el esquema de la base de datos SQLite y contiene scripts para inicializar (init_db) y poblar (seed_db) las tablas con datos de prueba.

tools.py: (Módulo de soporte) Contiene las funciones get_database_schema y execute_sql_query que el agente de IA utiliza para interactuar con la base de datos.

.env: Archivo de configuración local para las variables de entorno.

🛠️ Instalación y Uso

Clonar el repositorio y navegar a la carpeta del proyecto.

Crear y activar un entorno virtual:

En Windows: python -m venv env y luego env\Scripts\activate

En macOS/Linux: python3 -m venv env y luego source env/bin/activate

Instalar las dependencias:
Asegúrate de instalar los paquetes necesarios que utiliza el proyecto:

pip install streamlit python-dotenv google-genai


Configurar las variables de entorno:
Crea un archivo llamado .env en la raíz del proyecto y agrega tu clave de la API de Google Gemini:

GEMINI_API_KEY=tu_clave_api_aqui


Inicializar la base de datos (Opcional, se hace automático):
La aplicación está configurada para crear y poblar la base de datos automáticamente al iniciar si no existe. También puedes hacerlo manualmente:

python database.py


Ejecutar la aplicación:

streamlit run app.py


⚠️ Notas de Seguridad y Limitaciones

Este software es una herramienta administrativa. No debe utilizarse para autodiagnóstico ni como reemplazo del criterio médico profesional.

La base de datos actual (SQLite) está configurada para demostración/uso local.

Las sentencias de escritura (INSERT, UPDATE, DELETE, DROP) están estrictamente bloqueadas a nivel de prompt y se recomienda reforzarlas a nivel de la herramienta execute_sql_query en producción.
