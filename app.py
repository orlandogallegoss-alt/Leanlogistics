import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Berries Lean Logic - Tec Morelia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilo personalizado para el Tec de Morelia
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stChatFloatingInputContainer { background-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍓 Mentor IA: Especialidad Lean Logistics")
st.subheader("Entorno BANI - Caso: Berries del Sol Michoacano")

# --- 2. CONFIGURACIÓN DE LA API ---
# Nota: Para mayor seguridad en Streamlit Cloud, usa st.secrets["GOOGLE_API_KEY"]
GOOGLE_API_KEY = "AIzaSyAuKzzCt3Lmn1Kw78xKxT9uUTkeiJQWNX0" 

# --- 3. BARRA LATERAL (INFORMACIÓN Y DIAGNÓSTICO) ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_TecNM.svg/1200px-Logo_TecNM.svg.png", width=100)
    st.markdown("### Contexto Industrial")
    st.info("""
    **Región:** Los Reyes / Zamora, Michoacán.
    **Problema BANI:** Fluctuaciones térmicas y huelga de transporte.
    **Objetivo:** Reducir Muda y optimizar el Lead Time.
    """)
    st.divider()
    st.write("🔍 **Estatus del Sistema:**")

# Validar API Key y seleccionar modelo automáticamente
if not GOOGLE_API_KEY or GOOGLE_API_KEY == "PEGA_AQUÍ_TU_LLAVE":
    st.error("🔑 Error: API Key no configurada en el código.")
    st.stop()
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Detector automático de modelos disponibles para evitar el error 404
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Prioridad de selección
        if 'models/gemini-1.5-flash' in available_models:
            selected_model = 'gemini-1.5-flash'
        elif 'models/gemini-1.5-pro' in available_models:
            selected_model = 'gemini-1.5-pro'
        else:
            selected_model = available_models[0].replace('models/', '')
        
        st.sidebar.success(f"Conectado a: {selected_model}")
        
    except Exception as e:
        st.sidebar.error("Error de conexión con Google AI Studio.")
        st.stop()

# --- 4. CONFIGURACIÓN DEL MENTOR (PROMPT) ---
system_prompt = """
Eres un Mentor Senior en Lean Logistics para la carrera de Ingeniería Industrial del Tec de Morelia.
Tu misión es guiar a equipos de 3 a 5 personas en la resolución del caso 'Berries del Sol'.

REGLAS DE OPERACIÓN:
1. ENTORNO BANI: Michoacán está en crisis logística. Los alumnos deben proponer soluciones ágiles.
2. LEY DE LA PRECISIÓN: Si el alumno es vago (ej. "¿Qué hago?"), responde: "Solicitud imprecisa. Indica el KPI (OEE, Takt Time, Fill Rate) y el área de impacto."
3. DATOS TÉCNICOS: Solo entrega históricos de mermas o costos si usan términos como 'Muda', 'Kaizen' o 'Lead Time'.
4. DERIVACIÓN: Si preguntan teoría básica, diles: "Consulta este concepto con tu profesor de la materia para profundizar en la base académica."
"""

# Inicializar el modelo
model = genai.GenerativeModel(
    model_name=selected_model,
    system_instruction=system_prompt
)

# --- 5. INTERFAZ DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Atención Equipo de Industrial! El reporte de hoy en la zona de Los Reyes indica una ruptura en la cadena de frío del 15% en el SKU Zarzamora Fresh. ¿Cuál es su análisis técnico inicial?"}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del alumno
if prompt := st.chat_input("Escribe tu análisis o solicitud de datos técnicos..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Fallo en la comunicación: {e}")
                
    except Exception as e:
        st.error(f"Hubo un error con el modelo de IA: {e}")
        st.info("Sugerencia: Verifica que la API Key tenga acceso a Gemini 1.5 Flash en Google AI Studio.")
