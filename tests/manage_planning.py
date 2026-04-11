from fpdf import FPDF
import os

# Caminhos das fontes Arial (normal e negrito)
ARIAL_REGULAR = "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"
ARIAL_BOLD = "/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf"

instituicao = "FUNDAÇÃO DE ASSISTÊNCIA E EDUCAÇÃO"
centro = "CENTRO UNIVERSITÁRIO ESPÍRITO-SANTENSE"
disciplina = "PROJETO INTEGRADOR – Módulo 04"
componentes = (
    "Cleiton Leonel Creton, Beatryz Rodrigues Coelho, \n"
    "Maria Eduarda Moreira de Araújo, Kleyton Martinelli Santos, \n"
    "Eduardo de Oliveira Liria, Kenedy Anderson Souza de Castro, \n"
    "Guilherme Deorce Ribeiro \n")
acao_escolhida = "Projeto Aumigo de Livros"

titulo_acao = (
    'Bot Informativo "Aumigos de Livros" no Telegram: '
    'Conectando Leitores e Protetores de Animais'
)

objetivo = (
    "Desenvolver e integrar um bot no aplicativo Telegram com a finalidade de divulgar "
    "informações sobre o Instituto Aumigo de Livros, incentivando a doação de livros, "
    "a adoção responsável de animais, o voluntariado e o apoio financeiro à causa. "
    "O projeto visa ampliar a visibilidade da instituição e facilitar o acesso do público "
    "a dados relevantes por meio de uma interface automatizada, acessível e de fácil interação."
)

publico_alvo = (
    "Pessoas engajadas em causas sociais e ambientais;\n"
    "Amantes e defensores da causa animal, comprometidos com a adoção responsável;\n"
    "Leitores, educadores e doadores de livros, que veem na leitura um meio de inclusão e "
    "conhecimento;\n"
    "Filantropos e voluntários do Espírito Santo;\n"
    "Usuários de redes sociais, especialmente no Instagram e Telegram."
)

descricao = (
    "O projeto consiste na criação de um bot interativo voltado à disseminação de informações "
    "sobre o Instituto Aumigo de Livros, uma organização sem fins lucrativos que transforma "
    "doações de livros em recursos para o cuidado e resgate de animais abandonados.\n"
    "O bot atua como um canal de comunicação automatizado, oferecendo respostas sobre a história "
    "do instituto, seus objetivos, formas de doação, eventos e resultados alcançados.\n"
    "Com base em linguagem natural, o sistema busca facilitar o acesso às informações e ampliar "
    "a visibilidade da causa, integrando tecnologia, educação e responsabilidade social em um "
    "mesmo ambiente digital."
)

pdf = FPDF(format="A4")
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_left_margin(20)
pdf.set_right_margin(20)

# Adicionar fontes sem o parâmetro "uni" (deprecated)
if os.path.exists(ARIAL_REGULAR):
    pdf.add_font("Arial", "", ARIAL_REGULAR)
else:
    print("⚠️ Fonte Arial regular não encontrada, usando fonte padrão")

if os.path.exists(ARIAL_BOLD):
    pdf.add_font("Arial", "B", ARIAL_BOLD)
else:
    print("⚠️ Fonte Arial Bold não encontrada, usando estilo padrão")

pdf.set_font("Arial", "B", 12)
line_height = pdf.font_size * 1.5
usable_width = pdf.w - 2 * pdf.l_margin

# Cabeçalho com espaçamento ajustado
pdf.multi_cell(usable_width, line_height, instituicao, align="C")
pdf.ln(1)
pdf.multi_cell(usable_width, line_height, centro, align="C")
pdf.ln(1)
pdf.multi_cell(usable_width, line_height, f"Disciplina: {disciplina}", align="C")
pdf.ln(8)  # Espaçamento maior após disciplina

pdf.multi_cell(usable_width, line_height, f"COMPONENTES DO GRUPO: \n{componentes}", align="L")
pdf.ln(8)  # Espaçamento maior após componentes

# Ação extensionista em negrito
pdf.set_font("Arial", "B", 12)
pdf.multi_cell(
    usable_width,
    line_height,
    f"AÇÃO EXTENSIONISTA: {acao_escolhida}",
    align="L"
)
pdf.ln(line_height)


def add_section(title, content):
    # Título em NEGRITO
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(usable_width, line_height, title, align="L")
    pdf.ln(line_height / 3)

    # Conteúdo em fonte normal
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(usable_width, line_height, content, align="J")
    pdf.ln(line_height / 2)


add_section("1. TÍTULO DA AÇÃO", titulo_acao)
add_section("2. OBJETIVO DA AÇÃO", objetivo)
add_section("3. PÚBLICO-ALVO", publico_alvo)
add_section("4. DESCRIÇÃO DA AÇÃO", descricao)

pdf.output("planejamento_acao_extensionista.pdf")
print("✅ PDF gerado com sucesso: planejamento_acao_extensionista.pdf")
