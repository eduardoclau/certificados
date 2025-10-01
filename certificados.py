import io
from datetime import datetime

import streamlit as st
from reportlab.lib.colors import green
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

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
    if isinstance(data, str):
        data = datetime.strptime(data, "%d/%m/%Y")
    mes_ingles = data.strftime('%B')  # Nome do mês em inglês
    mes_portugues = meses_pt.get(mes_ingles, mes_ingles)  # Traduz para português
    return data.strftime(f'%d de {mes_portugues} de %Y')

# Conteúdos programáticos COMPLETOS
conteudos_programaticos = {
    "NR-01": [
        "Informações sobre as Condições e Meio Ambiente de Trabalho",
        "Introdução a Segurança no Trabalho",
        "Uso adequado dos Equipamentos de Proteção Individual - EPI",
        "Informações sobre os Equipamentos de Proteção Coletiva – EPC",
        "Acidente do trabalho",
        "Responsabilidades e Competências, e Riscos inerentes à sua função",
        "Certificado de Aprovação – CA",
        "Conservação, Higienização e Guarda dos EPI'S",
        "EPI para Proteção da Cabeça",
        "EPI para Proteção dos Olhos e Face",
        "EPI para Proteção Auditiva",
        "EPI para Proteção Respiratória",
        "EPI para Proteção do Tronco",
        "EPI para Proteção dos Membros Superiores e Membros Inferiores",
        "EPI para Proteção do Corpo Inteiro",
        "EPI para Proteção Contra Quedas com Diferença de Nível"
    ],
    "NR-06": [
        "Informações sobre as Condições e Meio Ambiente de Trabalho",
        "Introdução a Segurança no Trabalho",
        "Uso adequado dos Equipamentos de Proteção Individual - EPI",
        "Informações sobre os Equipamentos de Proteção Coletiva – EPC",
        "Acidente do trabalho",
        "Responsabilidades e Competências, e Riscos inerentes à sua função",
        "Certificado de Aprovação – CA",
        "Conservação, Higienização e Guarda dos EPI'S",
        "EPI para Proteção da Cabeça",
        "EPI para Proteção dos Olhos e Face",
        "EPI para Proteção Auditiva",
        "EPI para Proteção Respiratória",
        "EPI para Proteção do Tronco",
        "EPI para Proteção dos Membros Superiores e Membros Inferiores",
        "EPI para Proteção do Corpo Inteiro",
        "EPI para Proteção Contra Quedas com Diferença de Nível"
    ],
    "NR-01 e NR-06": [
        "Informações sobre as Condições e Meio Ambiente de Trabalho",
        "Introdução a Segurança no Trabalho",
        "Uso adequado dos Equipamentos de Proteção Individual - EPI",
        "Informações sobre os Equipamentos de Proteção Coletiva – EPC",
        "Acidente do trabalho",
        "Responsabilidades e Competências, e Riscos inerentes à sua função",
        "Certificado de Aprovação – CA",
        "Conservação, Higienização e Guarda dos EPI'S",
        "EPI para Proteção da Cabeça",
        "EPI para Proteção dos Olhos e Face",
        "EPI para Proteção Auditiva",
        "EPI para Proteção Respiratória",
        "EPI para Proteção do Tronco",
        "EPI para Proteção dos Membros Superiores e Membros Inferiores",
        "EPI para Proteção do Corpo Inteiro",
        "EPI para Proteção Contra Quedas com Diferença de Nível"
    ],
    "NR-35 (Trabalho em Altura)": [
        "Normas e regulamentos aplicáveis ao trabalho em altura",
        "Análise de Risco e condições impeditivas",
        "Riscos potenciais e medidas de prevenção e controle",
        "Sistemas, equipamentos e procedimentos de proteção coletiva",
        "Equipamentos de Proteção Individual para trabalho em altura: seleção, inspeção, conservação e limitação de uso",
        "Acidentes típicos em trabalhos em altura",
        "Equipamentos de guindar para elevação de pessoas e de materiais",
        "Noções de técnicas de resgate e primeiros socorros"
    ],
    "NR-33 (Trabalho em Espaço Confinado)": [
        "Definições e reconhecimento de espaços confinados",
        "Critérios de identificação e avaliação de riscos",
        "Funcionamento de equipamentos de medição de atmosferas",
        "Técnicas de trabalho seguro em espaços confinados",
        "Noções de resgate e primeiros socorros específicos",
        "Uso adequado de EPIs e EPCs para espaços confinados",
        "Procedimentos de entrada e trabalho em espaços confinados",
        "Monitoramento contínuo da atmosfera",
        "Comunicação e atuação da equipe"
    ],
    "Treinamento Ergonômico NR-17": [
        "Conceitos básicos de ergonomia",
        "Análise ergonômica do trabalho",
        "Riscos ergonômicos no ambiente laboral",
        "Mobiliário e equipamentos adequados",
        "Técnicas de levantamento e transporte de cargas",
        "Organização do tempo de trabalho",
        "Pausas para descanso e alongamento",
        "Adaptação das condições de trabalho às características psicofisiológicas"
    ],
    "NR-07 - Primeiros Socorros": [
        "Noções básicas de primeiros socorros",
        "Avaliação primária e secundária da vítima",
        "Procedimentos para parada cardiorrespiratória",
        "Controle de hemorragias e curativos",
        "Imobilização de fraturas e luxações",
        "Atendimento a queimaduras",
        "Manuseio de equipamentos de primeiros socorros",
        "Acionamento do serviço médico de emergência"
    ],
    "NR-05 - Designado CIPA": [
        "Estudo do ambiente, das condições de trabalho e riscos originados do processo produtivo",
        "Noções sobre acidentes e doenças do trabalho decorrentes de exposição aos riscos existentes na empresa",
        "Noções sobre a Síndrome da Imunodeficiência Adquirida - AIDS, e medidas de prevenção",
        "Noções sobre as legislações trabalhista e previdenciária relativas à segurança e saúde no trabalho",
        "Princípios gerais de higiene do trabalho e de medidas de controle dos riscos",
        "Organização da CIPA e outros assuntos necessários ao exercício das atribuições da Comissão",
        "Metodologia de investigação e análise de acidentes do trabalho"
    ],
    "NR-05 - CIPA": [
        "Estudo do ambiente, das condições de trabalho e riscos originados do processo produtivo",
        "Noções sobre acidentes e doenças do trabalho decorrentes de exposição aos riscos existentes na empresa",
        "Noções sobre a Síndrome da Imunodeficiência Adquirida - AIDS, e medidas de prevenção",
        "Noções sobre as legislações trabalhista e previdenciária relativas à segurança e saúde no trabalho",
        "Princípios gerais de higiene do trabalho e de medidas de controle dos riscos",
        "Organização da CIPA e outros assuntos necessários ao exercício das atribuições da Comissão",
        "Metodologia de investigação e análise de acidentes do trabalho"
    ],
    "NR-11 - Operador de Empilhadeira": [
        "Legislação e normas técnicas aplicáveis",
        "Componentes e sistemas da empilhadeira",
        "Inspeção diária e preventiva do equipamento",
        "Técnicas de operação segura",
        "Sinalização e comunicação no ambiente de trabalho",
        "Estabilidade de cargas e noções de centro de gravidade",
        "Manutenção básica e corretiva",
        "Procedimentos de emergência"
    ],
    "NR-11 - Operador de Munck": [
        "Legislação específica para operação de munck",
        "Características técnicas do equipamento",
        "Inspeção e manutenção preventiva",
        "Técnicas de içamento e movimentação de cargas",
        "Sinais manuais e comunicação por rádio",
        "Cálculo de capacidade de carga e raio de operação",
        "Procedimentos de segurança em áreas urbanas",
        "Emergências e situações de risco"
    ],
    "NR-11 - Operador de Retroescavadeira": [
        "Normas regulamentadoras aplicáveis",
        "Componentes e sistemas hidráulicos",
        "Inspeção diária do equipamento",
        "Técnicas de escavação e aterramento",
        "Estabilidade do equipamento em diferentes terrenos",
        "Sinalização de área de trabalho",
        "Manutenção básica e preventiva",
        "Procedimentos de segurança específicos"
    ],
    "NR-11 - Operador de Pá Carregadeira": [
        "Legislação e normas técnicas",
        "Características técnicas da pá carregadeira",
        "Inspeção e manutenção diária",
        "Técnicas de carregamento e descarregamento",
        "Movimentação em diferentes superfícies",
        "Controle de estabilidade e centro de gravidade",
        "Comunicação e sinalização no canteiro de obras",
        "Procedimentos de emergência"
    ],
    "NR-20 - Inflamáveis Classe I": [
        "Características dos inflamáveis classe I",
        "Identificação e avaliação de riscos",
        "Procedimentos de segurança em áreas classificadas",
        "Equipamentos de proteção específicos",
        "Prevenção e combate a incêndios",
        "Armazenamento e manuseio seguro",
        "Plano de resposta a emergências",
        "Legislação específica da NR-20"
    ],
    "NR-20 - Inflamáveis Classe II": [
        "Propriedades dos inflamáveis classe II",
        "Técnicas de controle de fontes de ignição",
        "Procedimentos operacionais padronizados",
        "Sistemas de proteção contra incêndio",
        "Inspeção de equipamentos e instalações",
        "Gestão de mudanças em atividades com inflamáveis",
        "Análise preliminar de risco",
        "Treinamento de equipes de emergência"
    ],
    "NR-20 - Inflamáveis Classe III": [
        "Características dos produtos classe III",
        "Gestão de segurança em processos contínuos",
        "Procedimentos para manutenção em áreas críticas",
        "Sistemas de detecção e alarme",
        "Plano de atendimento a emergências",
        "Auditoria do sistema de gestão de segurança",
        "Análise de acidentes e incidentes",
        "Atualização tecnológica e melhores práticas"
    ],
    "IN-28 - Brigadista Orgânico": [
        "Organização e atribuições da brigada de incêndio",
        "Teoria do fogo e métodos de extinção",
        "Classes de incêndio e agentes extintores",
        "Operação de equipamentos de combate a incêndio",
        "Técnicas de evacuação e abandono de área",
        "Primeiros socorros em emergências",
        "Plano de emergência contra incêndio",
        "Simulados e exercícios práticos"
    ]
}

# Caminho para o logo da empresa (ajuste conforme necessário)
LOGO_PATH = "Fortneer-Horizontal - Escuro 2.png"  # Coloque o caminho correto para o logo da empresa

# Função para gerar a página de verso com conteúdo programático
def generate_back_page(c, training_name, width, height, margin):
    # Desenhar a moldura verde colada nas extremidades
    c.setStrokeColor(green)
    c.setLineWidth(10)
    c.rect(0, 0, width, height)
    
    # Título do conteúdo programático
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - margin - 50, "CONTEÚDO PROGRAMÁTICO")
    
    # Nome do treinamento
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height - margin - 80, training_name)
    
    # Conteúdo programático
    c.setFont("Helvetica", 12)
    y_position = height - margin - 120
    
    # Verifica se existe conteúdo programático para o treinamento
    if training_name in conteudos_programaticos:
        conteudos = conteudos_programaticos[training_name]
        for i, conteudo in enumerate(conteudos):
            if y_position < margin + 50:
                c.showPage()
                # Desenhar a moldura verde na nova página
                c.setStrokeColor(green)
                c.setLineWidth(10)
                c.rect(0, 0, width, height)
                y_position = height - margin - 50
                
            c.drawString(margin + 20, y_position, f"{i+1}. {conteudo}")
            y_position -= 20
    else:
        c.drawString(margin + 20, y_position, "Conteúdo programático não disponível para este treinamento.")

# Função para gerar o PDF
def generate_pdf(participants, training_name, company, date, hours, instructor, observations):
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

        # Adicionar observações se fornecidas
        if observations:
            obs_y_position = height - margin - 250 - logo_height
            obs_text = f"<b>Observações:</b> {observations}"
            obs_paragraph = Paragraph(obs_text, body_style)
            obs_paragraph.wrapOn(c, width - 2 * margin, height)
            obs_paragraph.drawOn(c, margin, obs_y_position)

        # Local e data (usando a data do treinamento, não a data atual)
        location_date = f"<b>{city}, {formatar_data_pt(date)}.</b>"
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
        
        # Nova página para o conteúdo programático (verso)
        c.showPage()
        generate_back_page(c, training_name, width, height, margin)
        
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
    },
    {
        "name": "José Vilmar Krutli",
        "role": "Técnico em Segurança do Trabalho",
        "registration": "MTE/SC.00019615"
    }
]

# Entrada de dados
st.header("Informações do Treinamento")
training_name = st.selectbox("Qual Treinamento?", options=training_options)  # Selectbox para escolher o treinamento
company = st.text_input("Nome da empresa?")
date = st.date_input("Data de realização", datetime.now())
hours = st.number_input("Carga horária (horas)", min_value=1, step=1)
city = st.text_input("Cidade de realização do Treinamento")

# NOVO CAMPO: Observações
st.header("Observações")
observations = st.text_area("Observações (opcional)", 
                           placeholder="Digite aqui qualquer observação adicional que deva constar no certificado...",
                           height=100)

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
        pdf_buffer = generate_pdf(participants, training_name, company, date.strftime("%d/%m/%Y"), hours, instructor, observations)
        st.success("Certificados gerados com sucesso!")
        st.download_button(
            label="Baixar Certificados",
            data=pdf_buffer,
            file_name="certificados.pdf",
            mime="application/pdf",
        )

