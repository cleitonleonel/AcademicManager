import pytest
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch
from academic_manager.config.settings import Config


# Configuração de escopo de sessão
@pytest.fixture(scope="session")
def temp_workspace():
    """Cria workspace temporário para todos os testes da sessão"""
    temp_dir = tempfile.mkdtemp()
    original_base_dir = Config.BASE_DIR
    original_assignments_dir = Config.ASSIGNMENTS_DIR

    # Configura diretórios temporários
    Config.BASE_DIR = Path(temp_dir) / "test_projects"
    Config.ASSIGNMENTS_DIR = Config.BASE_DIR / "assignments"

    yield temp_dir

    # Cleanup
    Config.BASE_DIR = original_base_dir
    Config.ASSIGNMENTS_DIR = original_assignments_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def mock_api_key():
    """Mock global para API key"""
    with patch.dict('os.environ', {'API_KEY': 'test_api_key_12345'}):
        yield 'test_api_key_12345'


# Fixtures de dados
@pytest.fixture
def sample_academic_metadata():
    """Metadados de exemplo para trabalho acadêmico"""
    return {
        "curso": "Engenharia de Software",
        "aluno": "João Silva Santos",
        "titulo": "Sistema de Testes Automatizados para Aplicações Web",
        "local": "São Paulo",
        "ano": 2024,
        "disciplina": "Engenharia de Software II",
        "orientador": "Prof. Dra. Maria dos Santos"
    }


@pytest.fixture
def sample_template_data():
    """Template de exemplo com conteúdo estruturado"""
    return {
        "title": "Sistema de Testes Automatizados",
        "sections": [
            {
                "name": "INTRODUÇÃO",
                "blocks": [
                    {
                        "type": "paragraph",
                        "text": "Este trabalho apresenta uma análise abrangente sobre sistemas de testes automatizados para aplicações web modernas. Com o crescimento da complexidade das aplicações web, a necessidade de processos de teste eficientes e confiáveis tornou-se fundamental para garantir a qualidade do software."
                    },
                    {
                        "type": "paragraph",
                        "text": "Os testes automatizados representam uma evolução natural dos processos manuais de verificação, oferecendo maior velocidade, consistência e cobertura na detecção de defeitos."
                    }
                ]
            },
            {
                "name": "DESENVOLVIMENTO",
                "blocks": [
                    {
                        "type": "subtitle",
                        "text": "Metodologias de Teste",
                        "align": "L",
                        "font": {"style": "B", "size": 14}
                    },
                    {
                        "type": "paragraph",
                        "text": "As metodologias de teste modernas incluem Test-Driven Development (TDD), Behavior-Driven Development (BDD) e práticas de integração contínua."
                    },
                    {
                        "type": "image",
                        "position": "right",
                        "path": "%(imagem_1)s",
                        "width": 80,
                        "height": 60,
                        "text": "Arquitetura de testes em pirâmide mostrando a distribuição ideal entre testes unitários, de integração e end-to-end."
                    },
                    {
                        "type": "subtitle",
                        "text": "Ferramentas e Frameworks",
                        "align": "L",
                        "font": {"style": "B", "size": 14}
                    },
                    {
                        "type": "paragraph",
                        "text": "Entre as principais ferramentas utilizadas no mercado, destacam-se Selenium para testes de interface, Jest para JavaScript, PyTest para Python e Cypress para testes end-to-end modernos."
                    },
                    {
                        "type": "list",
                        "items": [
                            "Selenium WebDriver - Automação de navegadores web",
                            "Jest - Framework de testes para JavaScript/TypeScript",
                            "PyTest - Framework de testes para Python",
                            "Cypress - Testes end-to-end modernos",
                            "JUnit - Testes unitários para Java"
                        ]
                    }
                ]
            },
            {
                "name": "CONCLUSÃO",
                "blocks": [
                    {
                        "type": "paragraph",
                        "text": "A implementação de sistemas de testes automatizados demonstrou ser essencial para o desenvolvimento de software moderno. Os benefícios observados incluem redução significativa no tempo de detecção de bugs, melhoria na qualidade do código e maior confiança nas entregas."
                    },
                    {
                        "type": "image",
                        "position": "below",
                        "path": "%(imagem_2)s",
                        "width": 120,
                        "height": 80,
                        "text": "Gráfico comparativo mostrando redução de 70% no tempo de detecção de bugs com implementação de testes automatizados."
                    },
                    {
                        "type": "paragraph",
                        "text": "Recomenda-se a adoção gradual dessas práticas, começando pelos testes unitários e expandindo progressivamente para testes de integração e end-to-end, sempre mantendo o foco na qualidade e manutenibilidade do código de teste."
                    }
                ]
            },
            {
                "name": "REFERÊNCIAS",
                "blocks": [
                    {
                        "type": "list",
                        "items": [
                            "BECK, Kent. Test Driven Development: By Example. Boston: Addison-Wesley Professional, 2022.",
                            "FOWLER, Martin. Refactoring: Improving the Design of Existing Code. 2nd ed. Boston: Addison-Wesley Professional, 2019.",
                            "GREGORY, Janet; CRISPIN, Lisa. Agile Testing: A Practical Guide for Testers and Agile Teams. Boston: Addison-Wesley Professional, 2021.",
                            "HUMBLE, Jez; FARLEY, David. Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation. Boston: Addison-Wesley Professional, 2020."
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def sample_assignment_content():
    """Conteúdo de exemplo para assignment/enunciado"""
    return """
    TRABALHO AVALIATIVO - ENGENHARIA DE SOFTWARE II
    
    Tema: Sistema de Testes Automatizados para Aplicações Web
    
    Objetivo:
    Desenvolver um trabalho acadêmico que explore os conceitos, metodologias e ferramentas
    relacionadas aos sistemas de testes automatizados, com foco em aplicações web.
    
    Requisitos:
    1. Introdução ao tema (contextualização e importância)
    2. Revisão bibliográfica sobre metodologias de teste (TDD, BDD, etc.)
    3. Análise comparativa de ferramentas populares (Selenium, Cypress, Jest, etc.)
    4. Estudo de caso prático ou exemplo de implementação
    5. Conclusões e recomendações
    6. Referências bibliográficas (mínimo 5 fontes)
    
    Formatação:
    - Mínimo 15 páginas
    - Fonte Times New Roman, tamanho 12
    - Espaçamento 1,5
    - Margens: 3cm (esquerda), 2cm (demais)
    - Incluir figuras e diagramas ilustrativos
    
    Prazo de entrega: 30 dias
    Valor: 30% da nota final
    """


# Fixtures para mocking de serviços externos
@pytest.fixture
def mock_gemini_api_success():
    """Mock para API do Gemini retornando sucesso"""
    with patch('academic_manager.services.aistudio_chat.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "title": "Sistema de Testes Automatizados",
                            "sections": [
                                {
                                    "name": "INTRODUÇÃO",
                                    "blocks": [
                                        {
                                            "type": "paragraph",
                                            "text": "Introdução sobre testes automatizados..."
                                        }
                                    ]
                                }
                            ]
                        })
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def mock_gemini_api_error():
    """Mock para API do Gemini retornando erro"""
    with patch('academic_manager.services.aistudio_chat.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 429  # Rate limit
        mock_response.text = "Rate limit exceeded"
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def mock_bing_images_success():
    """Mock para busca de imagens no Bing retornando sucesso"""
    with patch('academic_manager.services.bing_images.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <div class="imgres">
            <a class="iusc" m='{"murl":"https://example.com/test_pyramid.jpg","rurl":"https://example.com"}'>
                <img src="thumb.jpg" alt="Test Pyramid">
            </a>
        </div>
        '''
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_bing_images_no_results():
    """Mock para busca de imagens sem resultados"""
    with patch('academic_manager.services.bing_images.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><p>No images found</p></body></html>'
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_image_download_success():
    """Mock para download de imagem bem-sucedido"""
    with patch('academic_manager.services.bing_images.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.content = b'fake_image_data_jpeg_header\xFF\xD8\xFF\xE0'
        mock_get.return_value = mock_response
        yield mock_get


# Fixtures para sistema de arquivos
@pytest.fixture
def temp_project_structure(temp_workspace):
    """Cria estrutura completa de projeto para testes"""
    project_name = "test_project_001"
    project_path = Config.BASE_DIR / project_name

    # Cria estrutura de diretórios
    project_path.mkdir(parents=True, exist_ok=True)
    (project_path / "sources").mkdir(exist_ok=True)
    (project_path / "attachments").mkdir(exist_ok=True)

    # Cria arquivos de exemplo
    settings_data = {
        "curso": "Engenharia de Software",
        "aluno": "Teste User",
        "titulo": "Projeto de Teste",
        "local": "São Paulo",
        "ano": 2024,
        "disciplina": "Teste",
        "orientador": "Prof. Teste"
    }

    with open(project_path / "settings.json", "w", encoding="utf-8") as f:
        json.dump(settings_data, f, ensure_ascii=False, indent=4)

    with open(project_path / "instructions.md", "w", encoding="utf-8") as f:
        f.write("# Instruções do Projeto\nDescrição das instruções...")

    # Cria arquivos de origem (logo, máscara)
    (project_path / "sources" / "logo.png").write_bytes(b'fake_png_data')
    (project_path / "sources" / "mask.png").write_bytes(b'fake_png_mask')

    return project_path


@pytest.fixture
def sample_assignments_dir(temp_workspace):
    """Cria diretório de assignments com exemplos"""
    Config.ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)

    assignments = {
        "trabalho_ia.txt": """
        Desenvolva um trabalho sobre Inteligência Artificial na Educação.
        Deve conter introdução, desenvolvimento e conclusão.
        """,
        "projeto_web.txt": """
        Crie um projeto sobre desenvolvimento web moderno.
        Inclua frameworks, ferramentas e boas práticas.
        """,
        "estudo_banco_dados.txt": """
        Realize um estudo sobre sistemas de banco de dados NoSQL.
        Compare diferentes tecnologias e casos de uso.
        """
    }

    for filename, content in assignments.items():
        with open(Config.ASSIGNMENTS_DIR / filename, "w", encoding="utf-8") as f:
            f.write(content.strip())

    return Config.ASSIGNMENTS_DIR


# Fixtures para input de usuário
@pytest.fixture
def mock_user_input_create_project():
    """Mock para entrada do usuário ao criar projeto"""
    inputs = [
        "Projeto Teste",  # Nome do projeto
        "Ciência da Computação",  # Curso
        "Maria Silva",  # Aluno
        "IA na Educação",  # Título
        "Rio de Janeiro",  # Local
        "Inteligência Artificial",  # Disciplina  
        "Prof. Dr. João Santos"  # Orientador
    ]
    with patch('builtins.input', side_effect=inputs):
        yield inputs


@pytest.fixture
def mock_user_input_select_options():
    """Mock para seleção de opções pelo usuário"""
    with patch('builtins.input', return_value='1'):  # Seleciona primeira opção
        yield '1'


# Fixtures para validação de PDF
@pytest.fixture
def pdf_validator():
    """Validador para arquivos PDF gerados"""

    def validate_pdf(pdf_path: Path):
        """Valida estrutura básica de um PDF"""
        if not pdf_path.exists():
            return False, "PDF file does not exist"

        if pdf_path.stat().st_size < 100:
            return False, "PDF file is too small"

        with open(pdf_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                return False, "Invalid PDF header"

        return True, "PDF is valid"

    return validate_pdf


# Configurações de marcadores
def pytest_configure(config):
    """Configuração customizada do pytest"""
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as requiring API access"
    )


def pytest_collection_modifyitems(config, items):
    """Modifica coleção de testes baseado em marcadores"""
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return

    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


def pytest_addoption(parser):
    """Adiciona opções customizadas ao pytest"""
    parser.addoption(
        "--runslow", action="store_true", default=False,
        help="run slow tests"
    )
    parser.addoption(
        "--runapi", action="store_true", default=False,
        help="run tests that require API access"
    )
