import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE SEGURIDAD (SECRETS) ---
# Intentamos obtener la llave de los Secrets de Streamlit Cloud
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # Si pruebas localmente, busca en un archivo local o muestra advertencia
    api_key = None

# --- 2. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Berries Lean Logic - Tec Morelia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.title("🍓 Mentor IA: Especialidad Lean Logistics")
st.subheader("Entorno BANI - Caso: Berries del Sol Michoacano")

# --- 3. VALIDACIÓN E INICIALIZACIÓN ---
if not api_key:
    st.error("🔑 Error: API Key no detectada. Configúrala en 'Settings > Secrets' de Streamlit Cloud.")
    st.stop()
else:
    try:
        genai.configure(api_key=api_key)
        
        # Selección dinámica de modelo para evitar errores 404
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if 'models/gemini-1.5-flash' in available_models:
            model_name = 'models/gemini-1.5-flash'
        elif 'models/gemini-1.5-pro' in available_models:
            model_name = 'models/gemini-1.5-pro'
        else:
            model_name = available_models[0]
            
        st.sidebar.success(f"✅ Conectado a: {model_name}")
        
    except Exception as e:
        st.sidebar.error(f"❌ Error de conexión: {e}")
        st.stop()

# --- 4. BARRA LATERAL (CASO BANI) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_TecNM.svg/1200px-Logo_TecNM.svg.png", width=100)
    st.markdown("### Contexto del Semestre")
    st.info("""
    **Región:** Los Reyes / Zamora.
    **BANI:** Frágil y No-lineal.
    **Meta:** Ser agente de cambio.
    """)

# --- 5. CONFIGURACIÓN DEL PROMPT DEL MENTOR ---
system_prompt = """
Eres un Mentor Senior en Lean Logistics para el Tec de Morelia.
Tu objetivo es ayudar a estudiantes de Industrial a desarrollar pensamiento no lineal y crítico.

REGLAS:
1. No des respuestas directas.
2. Exige precisión técnica: OEE, Takt Time, Lead Time, Muda.
3. Si la solicitud es vaga, responde: 'Solicitud imprecisa. Indica el KPI y el área afectada.'
4. Dirige a los estudiantes con su profesor para teoría profunda de las materias.
"""

model = genai.GenerativeModel(
    model_name=model_name,
    system_instruction=system_prompt
)

# --- 6. INTERFAZ DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Atención Equipo! El entorno BANI ha afectado la logística en Los Reyes. ¿Cómo planean reducir el desperdicio hoy?"}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del alumno
if prompt := st.chat_input("Ingresa tu análisis técnico..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generación de respuesta
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error en generación: {e}")
