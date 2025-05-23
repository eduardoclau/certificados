import io
from datetime import datetime

import streamlit as st
from reportlab.lib.colors import green
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

# Configuração da página DEVE ser a primeira coisa
st.set_page_config(
    page_title="Gerador de Certificados",
    page_icon="📄",
    layout="centered"
)

# Mapeamento dos meses em português
meses_pt = {
    "January": "Janeiro",
    "February": "Fevereiro",
    "March": "Março",
    "April": "Abril",
    "May": "Maio",
    "June": "Junho",
    "July": "Julho",
    "August": "Agosto",
    "September": "Setembro",
    "October": "Outubro",
    "November": "Novembro",
    "December": "Dezembro"
}

# Função para formatar a data em português
def formatar_data_pt(data):
    mes_ingles = data.strftime('%B')  # Nome do mês em inglês
    mes_portugues = meses_pt.get(mes_ingles, mes_ingles)  # Traduz para português
    return data.strftime(f'%d de {mes_portugues} de %Y')

# Caminho para o logo da empresa (ajuste conforme necessário)
LOGO_PATH = "Fortneer-Horizontal - Escuro 2.png"  # Coloque o caminho correto para o logo da empresa

# Função para gerar o PDF
def generate_pdf(participants, training_name, company, date, hours, instructor):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))  # Modo paisagem
    
    # Definir margens (2 cm em todas as bordas)
    margin = 2 * cm
    width, height = landscape(A4)  # Largura e altura invertidas

    # Estilos de texto
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    body_style = styles["BodyText"]
    signature_style = styles["BodyText"]
    signature_style.fontName = "Helvetica"

    # Adicionar conteúdo do certificado para cada participante
    for participant in participants:
        # Desenhar a moldura verde colada nas extremidades (em cada página)
        c.setStrokeColor(green)  # Define a cor da borda como verde
        c.setLineWidth(10)  # Define a espessura da borda (aumentada para 10 pontos)
        c.rect(0, 0, width, height)  # Desenha o retângulo colado nas extremidades

        # Adicionar logo (se existir)
        try:
            logo = ImageReader(LOGO_PATH)
            # Definir o tamanho da logo
            logo_width = 259  # Largura da logo
            logo_height = 67  # Altura da logo
            # Posicionar a logo no canto esquerdo superior
            logo_x = margin  # Alinhado à esquerda, respeitando a margem
            logo_y = height - margin - logo_height  # Alinhado ao topo, respeitando a margem
            c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height)
        except Exception as e:
            st.warning(f"Não foi possível carregar o logo: {e}")

        # Título do certificado
        title = Paragraph("CERTIFICADO DE PARTICIPAÇÃO", title_style)
        title.wrapOn(c, width - 2 * margin, height)
        title.drawOn(c, margin, height - margin - 100 - logo_height)  # Ajuste para não sobrepor a logo

        # Texto do certificado
        text = f"""
        Certificamos que <b>{participant}</b> participou do <b>Treinamento de {training_name}</b>, 
        realizado pela empresa <b>{company}</b>, na data de <b>{date}</b>, 
        perfazendo um total de <b>{hours} horas de atividades</b>.
        """
        paragraph = Paragraph(text, body_style)
        paragraph.wrapOn(c, width - 2 * margin, height)
        paragraph.drawOn(c, margin, height - margin - 200 - logo_height)  # Ajuste para não sobrepor a logo

        # Local e data
        location_date = f"<b>{city}, {formatar_data_pt(datetime.now())}.</b>"
        location_paragraph = Paragraph(location_date, body_style)
        location_paragraph.wrapOn(c, width - 2 * margin, height)
        location_paragraph.drawOn(c, margin, margin + 100)

        # Assinatura (baseada no instrutor selecionado)
        signature = Paragraph(f"<b>{instructor['name']}</b>", signature_style)
        signature.wrapOn(c, width - 2 * margin, height)
        signature.drawOn(c, margin, margin + 80)

        role = Paragraph(f"<b>{instructor['role']}</b>", body_style)
        role.wrapOn(c, width - 2 * margin, height)
        role.drawOn(c, margin, margin + 60)

        mte = Paragraph(f"<b>{instructor['registration']}</b>", body_style)
        mte.wrapOn(c, width - 2 * margin, height)
        mte.drawOn(c, margin, margin + 40)

        # Nova página para o próximo participante
        c.showPage()
    
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# CSS personalizado para melhorar a interface
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f4f4;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input, .stDateInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stSelectbox>div>div>div {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stTextArea>div>div>textarea {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
    }
    .stMarkdown h1 {
        color: #333;
        font-size: 28px;
        font-weight: bold;
    }
    .stMarkdown h2 {
        color: #555;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Logo da Fortneer no topo da página
st.image("Fortneer-Horizontal - Escuro 2.png", width=300)  # Ajuste o caminho e o tamanho conforme necessário

# Título da aplicação
st.title("Gerador de Certificados de Participação")
st.markdown("Preencha os campos abaixo para gerar certificados de participação.")

# Opções de treinamento
training_options = [
    "NR-01",
    "NR-06",
    "NR-01 e NR-06",
    "NR-35 (Trabalho em Altura)",
    "NR-33 (Trabalho em Espaço Confinado)",
    "Treinamento Ergonômico NR-17",
    "NR-07 - Primeiros Socorros",
    "NR-05 - Designado CIPA",
    "NR-05 - CIPA",
    "NR-11 - Operador de Empilhadeira",
    "NR-11 - Operador de Munck",
    "NR-11 - Operador de Retroescavadeira",
    "NR-11 - Operador de Pá Carregadeira",
    "NR-20 - Inflamáveis Classe I",
    "NR-20 - Inflamáveis Classe II",
    "NR-20 - Inflamáveis Classe III",
    "IN-28 - Brigadista Orgânico"
]

# Opções de instrutores
instructors = [
    {
        "name": "Gian Sehenen Garcia",
        "role": "Técnico em Segurança do Trabalho",
        "registration": "MTE/SC.000785.4"
    },
    {
        "name": "Fabiana Mufatto Saviato Cardoso",
        "role": "Engenheira de Segurança do Trabalho",
        "registration": "CREA/SC.092791-5"
    },
    {
    "name": "Allan Douglas Dos Santos",
        "role": "Técnico em Segurança do Trabalho",
        "registration": "MTE/PR.0016043"
    },
    {
        "name": "Kelvin de Macedo",
        "role": "Técnico em Segurança do Trabalho",
        "registration": "MTE/SC.0039941"
    },
    {
        "name": "Karina Locatelli",
        "role": "Técnico em Segurança do Trabalho",
        "registration": "MTE/SC.0006216"
    }
]

# Entrada de dados
st.header("Informações do Treinamento")
training_name = st.selectbox("Qual Treinamento?", options=training_options)  # Selectbox para escolher o treinamento
company = st.text_input("Nome da empresa?")
date = st.date_input("Data de realização", datetime.now())
hours = st.number_input("Carga horária (horas)", min_value=1, step=1)
city = st.text_input("Cidade de realização do Treinamento")

# Seleção do instrutor
st.header("Informações do Instrutor")
instructor_options = [f"{instructor['name']} - {instructor['role']}" for instructor in instructors]
selected_instructor = st.selectbox("Selecione o Instrutor", options=instructor_options)
instructor = next((i for i in instructors if f"{i['name']} - {i['role']}" == selected_instructor), None)

# Entrada de participantes
st.header("Participantes")
participants = st.text_area("Nomes dos participantes (um por linha)").split("\n")

# Remover linhas vazias (caso o usuário tenha pressionado Enter sem digitar nada)
participants = [p.strip() for p in participants if p.strip()]

# Gerar PDF
st.header("Gerar Certificados")
if st.button("Gerar Certificados"):
    if not training_name or not company or not participants or not instructor:
        st.error("Por favor, preencha todos os campos obrigatórios.")
    else:
        pdf_buffer = generate_pdf(participants, training_name, company, date.strftime("%d/%m/%Y"), hours, instructor)
        st.success("Certificados gerados com sucesso!")
        st.download_button(
            label="Baixar Certificados",
            data=pdf_buffer,
            file_name="certificados.pdf",
            mime="application/pdf",
        )
