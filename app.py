import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Berries Lean Logic - Tec Morelia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilo visual básico
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍓 Mentor IA: Especialidad Lean Logistics")
st.subheader("Entorno BANI - Caso: Berries del Sol Michoacano")

# --- 2. CONFIGURACIÓN DE LA API ---
# Nota: AI, Data Science y Vibecoding requieren precisión en las llaves
GOOGLE_API_KEY = "AIzaSyAuKzzCt3Lmn1Kw78xKxT9uUTkeiJQWNX0" 

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "PEGA_AQUÍ_TU_LLAVE":
    st.error("🔑 Error: API Key no configurada.")
    st.stop()
else:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Selección automática del modelo disponible
        models_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if 'models/gemini-1.5-flash' in models_list:
            selected_model = 'models/gemini-1.5-flash'
        elif 'models/gemini-1.5-pro' in models_list:
            selected_model = 'models/gemini-1.5-pro'
        else:
            selected_model = models_list[0]
            
        st.sidebar.success(f"Conectado a: {selected_model}")
        
    except Exception as e:
        st.sidebar.error(f"Error de conexión: {e}")
        st.stop()

# --- 3. BARRA LATERAL ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Logo_TecNM.svg/1200px-Logo_TecNM.svg.png", width=100)
    st.markdown("### Contexto del Caso")
    st.info("""
    **Región:** Los Reyes / Zamora.
    **BANI:** Ruptura de frío y huelga.
    """)

# --- 4. CONFIGURACIÓN DEL PROMPT ---
system_prompt = """
Eres un Mentor Senior en Lean Logistics para el Tec de Morelia. 
Tu valor central es ser un agente de cambio e impulsar el pensamiento crítico.
Guía a los alumnos sin dar soluciones directas. Exige precisión en KPIs (OEE, Takt Time).
"""

model = genai.GenerativeModel(
    model_name=selected_model,
    system_instruction=system_prompt
)

# --- 5. INTERFAZ DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Atención Equipo! Reportan falla en frío en Los Reyes. ¿Qué herramientas Lean proponen?"}
    ]

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto del alumno
if prompt := st.chat_input("Escribe tu análisis técnico aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        try:
            # Aquí es donde estaba el error de sintaxis anterior
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error al generar respuesta: {e}")
                
    except Exception as e:
        st.error(f"Hubo un error con el modelo de IA: {e}")
        st.info("Sugerencia: Verifica que la API Key tenga acceso a Gemini 1.5 Flash en Google AI Studio.")
