
import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# Clase PDF para generar el informe
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Informe Esotérico Personalizado", ln=True, align="C")
        self.ln(5)

    def add_section(self, title, content):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 8, content)
        self.ln()

# Funciones del sistema esotérico
class Persona:
    def __init__(self, nombre, fecha_nacimiento, hora_nacimiento, lugar_nacimiento, genero):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.hora_nacimiento = hora_nacimiento
        self.lugar_nacimiento = lugar_nacimiento
        self.genero = genero
        self.datos_bazi = None
        self.datos_astrologia = None
        self.resultado_final = None

class AnalisisEsoterico:
    def __init__(self, persona):
        self.persona = persona

    def generar_bazi(self):
        # Simulación de análisis BaZi básico
        self.persona.datos_bazi = {
            "dia_maestro": "Yi (Madera Yin)",
            "pilares": "Año: Ren Xu, Mes: Ji Chou, Día: Yi Wei, Hora: Ren Shen",
            "elementos": ["Agua", "Tierra", "Madera", "Metal"],
            "estructura": "Día Maestro: Yi (Madera Yin), personalidad adaptable, sensible, creativa."
        }

    def generar_astrologia_occidental(self):
        self.persona.datos_astrologia = {
            "signo_solar": "Acuario",
            "signo_lunar": "Tauro",
            "ascendente": "Leo",
            "perfil": "Visionario, emocionalmente estable, carismático",
        }

    def fusionar_resultados(self):
        self.persona.resultado_final = {
            "personalidad": f"{self.persona.datos_bazi['estructura']}. Internamente, {self.persona.datos_astrologia['perfil']}",
            "poder_personal": "Alta intuición, buena visión estratégica, equilibrio entre lo mental y lo emocional.",
            "recomendaciones": [
                "Buscar profesiones con propósito espiritual o social",
                "Evitar rutinas excesivas o entornos sin inspiración",
                "Cultivar la expresión emocional y creativa",
            ]
        }

    def analizar(self):
        self.generar_bazi()
        self.generar_astrologia_occidental()
        self.fusionar_resultados()
        return self.persona.resultado_final

# Interfaz Streamlit
st.title("Asistente Esotérico con BaZi y Astrología")
st.write("Completa tus datos para recibir un análisis personalizado y descargar tu informe PDF.")

with st.form("formulario"):
    nombre = st.text_input("Nombre completo")
    fecha_nacimiento = st.date_input("Fecha de nacimiento", min_value=datetime(1900, 1, 1), max_value=datetime.today())
    hora_nacimiento = st.text_input("Hora de nacimiento (HH:MM)")
    lugar_nacimiento = st.text_input("Lugar de nacimiento")
    genero = st.selectbox("Género", ["masculino", "femenino"])
    enviar = st.form_submit_button("Analizar")

if enviar:
    persona = Persona(nombre, str(fecha_nacimiento), hora_nacimiento, lugar_nacimiento, genero)
    analisis = AnalisisEsoterico(persona)
    resultado = analisis.analizar()

    st.subheader("Resultado del Análisis")
    st.write(f"**Personalidad:** {resultado['personalidad']}")
    st.write(f"**Poder Personal:** {resultado['poder_personal']}")
    st.write("**Recomendaciones:**")
    for rec in resultado['recomendaciones']:
        st.write(f"- {rec}")

    # Generar PDF en memoria
    pdf = PDF()
    pdf.add_page()
    pdf.add_section("Nombre", nombre)
    pdf.add_section("Fecha de nacimiento", str(fecha_nacimiento))
    pdf.add_section("Hora y lugar", f"{hora_nacimiento}, {lugar_nacimiento}")
    pdf.add_section("Personalidad", resultado['personalidad'])
    pdf.add_section("Poder Personal", resultado['poder_personal'])
    pdf.add_section("Recomendaciones", "\n".join(resultado['recomendaciones']))

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.success("Informe PDF generado correctamente.")
    st.download_button("Descargar PDF", data=pdf_buffer, file_name=f"Informe_Esoterico_{nombre}.pdf", mime="application/pdf")
