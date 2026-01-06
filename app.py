import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Berries Lean Logic - Tec Morelia", layout="wide")
st.title("🍓 Sistema de Respuesta BANI: Logística de Berries")
st.sidebar.markdown("### Caso: Berries del Sol Michoacano")
st.sidebar.info("Ubicación: Los Reyes / Zamora. Mercado: Exportación Global.")

# --- CONFIGURACIÓN DE LA API ---
GOOGLE_API_KEY = "AIzaSyAuKzzCt3Lmn1Kw78xKxT9uUTkeiJQWNX0" # Tu llave configurada

if not GOOGLE_API_KEY or GOOGLE_API_KEY == "PEGA_AQUÍ_TU_LLAVE":
    st.error("Configura tu API Key.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

    # --- PROMPT CON CONTEXTO DE BERRIES ---
    system_prompt = """
    Eres un Mentor Senior en Lean Logistics especializado en la agroindustria de Michoacán.
    
    CONTEXTO DE LA EMPRESA:
    - Manejas 3 SKUs: Zarzamora Fresh, Fresa Frozen, Arándano Premium.
    - El Lead Time promedio de cosecha a empaque es de 4 horas.
    - El costo por palé perdido por ruptura de cadena de frío es de $4,500 USD.

    ESCENARIO BANI (Enero 2026): 
    - Incomprensible: Las temperaturas en la región de Los Reyes han subido 5 grados por encima del promedio histórico, afectando la maduración acelerada.
    - Frágil: El principal proveedor de cajas refrigeradas tiene huelga de transportistas.

    REGLAS PARA EL ALUMNO:
    1. Si piden ayuda sin datos técnicos, responde: 'Análisis insuficiente. Indica el SKU afectado y el impacto en el Takt Time de la línea de empaque.'
    2. Si proponen soluciones de inventario sin considerar la vida útil (shelf-life), critícalos por generar desperdicio (Muda).
    3. Dirígelos con su profesor de 'Administración de Almacenes' o 'Logística de Transporte' si no saben calcular el stock de seguridad para productos perecederos.
    """

    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Equipo, el reporte de hoy indica fluctuaciones térmicas en las cámaras. ¿Cuál es su plan de contingencia aplicando Lean?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ingresa tu análisis o solicitud de datos..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})