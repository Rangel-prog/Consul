# Consul - Asistente Administrativo con IA


Sistema inteligente de consulta de base de datos para la gestión administrativa de un consultorio psicológico. Este proyecto utiliza agentes de Inteligencia Artificial para traducir preguntas en lenguaje natural a consultas SQL, permitiendo a los administradores extraer información sin necesidad de conocimientos técnicos.
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://consul-dyoq3djxeysrm8dzmhgjek.streamlit.app)

## 🚀 Características Principales

* **Consultas en Lenguaje Natural:** Integración con Google Gemini API para interpretar intenciones y consultar la base de datos de manera dinámica.
* **Seguridad por Diseño (Read-Only):** El agente está restringido estrictamente a operaciones SELECT en la base de datos SQLite para garantizar la integridad de los registros.
* **Frontera de Responsabilidad Médica:** Arquitectura con "system prompts" estrictos que bloquean cualquier intento de generar diagnósticos médicos o psicológicos, limitando la IA a tareas puramente administrativas.
* **Interfaz Profesional:** Construido con Streamlit para ofrecer un entorno de chat limpio, responsivo y fácil de usar.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14+
* **Frontend:** Streamlit
* **Base de Datos:** SQLite3
* **Inteligencia Artificial:** Google GenAI SDK (Gemini 1.5 Flash)

## 💻 Ejecución Local

Si deseas correr este proyecto en tu propia máquina, sigue estos pasos:

1. **Clona el repositorio:**
    git clone https://github.com/Rangel-prog/Consul.git
    cd Consul

2. **Instala las dependencias:**
    pip install -r requirements.txt

3. **Configura tus credenciales:**
    Crea una carpeta .streamlit en la raíz del proyecto y dentro un archivo secrets.toml con tu API Key de Google:
    GEMINI_API_KEY="AIzaSy_TU_CLAVE_AQUI"

4. **Inicia la aplicación:**
    streamlit run app.py

## ⚠️ Consideraciones de Despliegue (Rate Limits)

El asistente de este proyecto utiliza un agente inteligente que realiza múltiples llamadas iterativas (Tool Calling) a la base de datos SQLite para inspeccionar el esquema, razonar la consulta y generar una respuesta precisa.

Debido a esta arquitectura, si se utiliza una API Key de la capa gratuita (Free Tier) de Google Gemini, es probable alcanzar el límite estricto de **5 peticiones por minuto**, lo que resultará en un error temporal 429 RESOURCE_EXHAUSTED en la interfaz.

**Para evaluadores:** Si experimentas este límite durante las pruebas en el despliegue público, por favor permite que transcurra 1 minuto entre cada consulta. Para un uso fluido y sin restricciones, se requiere ejecutar el proyecto localmente inyectando una API Key vinculada a una cuenta con facturación habilitada (ej. Google AI Plus).
