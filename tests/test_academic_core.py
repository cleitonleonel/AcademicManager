import pytest
import json
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from datetime import datetime

# Imports dos módulos a serem testados
from academic_manager.builder import AcademicWork, ContentBuilder, paragraph, subtitle, img
from academic_manager.core.file_manager import FileManager
from academic_manager.core.project_manager import ProjectManager
from academic_manager.core.template_generator import TemplateGenerator
from academic_manager.core.pdf_generator import PDFGenerator
from academic_manager.services.aistudio_chat import get_template_json
from academic_manager.services.bing_images import get_image_url, download_image, process_json
from academic_manager.ui.interface import UserInterface
from academic_manager.config.settings import Config


class TestBuilderFunctions:
    """Testes para as funções auxiliares do builder"""
    
    def test_paragraph_creation(self):
        """Testa a criação de parágrafos"""
        result = paragraph("Texto de teste", align="C", custom_attr="value")
        
        expected = {
            "type": "paragraph",
            "text": "Texto de teste",
            "align": "C",
            "custom_attr": "value"
        }
        
        assert result == expected
    
    def test_subtitle_creation(self):
        """Testa a criação de subtítulos"""
        result = subtitle("Título", size=16, style="I")
        
        assert result["type"] == "subtitle"
        assert result["text"] == "Título"
        assert result["font"]["size"] == 16
        assert result["font"]["style"] == "I"
    
    def test_img_creation(self):
        """Testa a criação de imagens"""
        result = img("path/to/image.jpg", position="left", width=50, height=40, text="Legenda")
        
        assert result["type"] == "image"
        assert result["path"] == "path/to/image.jpg"
        assert result["position"] == "left"
        assert result["width"] == 50
        assert result["height"] == 40
        assert result["text"] == "Legenda"


class TestContentBuilder:
    """Testes para a classe ContentBuilder"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.builder = ContentBuilder()
    
    def test_initialization(self):
        """Testa a inicialização do ContentBuilder"""
        assert self.builder.content == []
    
    def test_add_paragraph(self):
        """Testa a adição de parágrafos"""
        result = self.builder.paragraph("Texto teste", align="J", font_size=14)
        
        assert result is self.builder  # Testa method chaining
        assert len(self.builder.content) == 1
        assert self.builder.content[0]["type"] == "paragraph"
        assert self.builder.content[0]["text"] == "Texto teste"
        assert self.builder.content[0]["font"]["size"] == 14
    
    def test_add_subtitle(self):
        """Testa a adição de subtítulos"""
        self.builder.subtitle("Subtítulo", font_style="I", color=(255, 0, 0))
        
        assert len(self.builder.content) == 1
        assert self.builder.content[0]["type"] == "subtitle"
        assert self.builder.content[0]["color"] == (255, 0, 0)
    
    def test_add_image(self):
        """Testa a adição de imagens"""
        self.builder.image("test.jpg", position="right", width=100, text="Imagem teste")
        
        assert len(self.builder.content) == 1
        assert self.builder.content[0]["type"] == "image"
        assert self.builder.content[0]["position"] == "right"
    
    def test_method_chaining(self):
        """Testa o encadeamento de métodos"""
        result = (self.builder
                 .paragraph("Parágrafo 1")
                 .subtitle("Título")
                 .paragraph("Parágrafo 2")
                 .image("test.jpg"))
        
        assert result is self.builder
        assert len(self.builder.content) == 4
    
    def test_get_content(self):
        """Testa a recuperação do conteúdo"""
        self.builder.paragraph("Teste")
        content = self.builder.get_content()
        
        assert isinstance(content, list)
        assert len(content) == 1
    
    def test_clear_content(self):
        """Testa a limpeza do conteúdo"""
        self.builder.paragraph("Teste").clear()
        
        assert self.builder.content == []


class TestAcademicWork:
    """Testes para a classe AcademicWork"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.test_data = {
            "instituicao": "FAESA",
            "unidade": "Centro Universitário",
            "tipo": "GRADUAÇÃO",
            "curso": "Engenharia de Software",
            "aluno": "João Silva",
            "titulo": "Teste de Sistema",
            "subtitulo": "",
            "local": "São Paulo",
            "ano": 2024,
            "disciplina": "Testes de Software",
            "orientador": "Prof. Maria"
        }
        self.academic_work = AcademicWork(self.test_data, "logo.png")
    
    def test_initialization(self):
        """Testa a inicialização da classe AcademicWork"""
        assert self.academic_work.data == self.test_data
        assert self.academic_work.logo_path == "logo.png"
        assert self.academic_work.sections == []
        assert self.academic_work.anchors == {}
    
    @patch('fpdf.FPDF.image')
    def test_add_cover(self, mock_image):
        """Testa a adição da capa"""
        self.academic_work.add_cover()
        
        # Verifica se tentou adicionar a imagem do logo
        mock_image.assert_called()
        
        # Verifica se há pelo menos uma página
        assert self.academic_work.page_no() >= 1
    
    def test_add_section_with_string_content(self):
        """Testa a adição de seção com conteúdo string"""
        self.academic_work.add_section("Introdução", "Conteúdo da introdução")
        
        assert len(self.academic_work.sections) == 1
        assert self.academic_work.sections[0][0] == "Introdução"
    
    def test_add_section_with_list_content(self):
        """Testa a adição de seção com conteúdo em lista"""
        content = [
            {"type": "paragraph", "text": "Parágrafo teste"},
            {"type": "subtitle", "text": "Subtítulo teste"}
        ]
        
        self.academic_work.add_section("Desenvolvimento", content)
        
        assert len(self.academic_work.sections) == 1
        assert self.academic_work.sections[0][0] == "Desenvolvimento"

    def test_unicode_content_is_supported(self):
        """Gera PDF com caracteres tipográficos comuns em respostas da IA."""
        self.academic_work.add_section(
            "Seção — teste",
            [{"type": "paragraph", "text": "“Aspas curvas”, ação, não, … e ≤."}],
        )
        output_path = Path(tempfile.mkdtemp()) / "unicode.pdf"
        try:
            self.academic_work.output(str(output_path))
            assert output_path.exists()
            assert output_path.stat().st_size > 0
        finally:
            shutil.rmtree(output_path.parent, ignore_errors=True)


class TestFileManager:
    """Testes para a classe FileManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_base_dir = Config.BASE_DIR
        Config.BASE_DIR = Path(self.temp_dir) / "test_projects"
        Config.ASSIGNMENTS_DIR = Config.BASE_DIR / "assignments"
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        Config.BASE_DIR = self.original_base_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ensure_directories_exist(self):
        """Testa a criação de diretórios necessários"""
        FileManager.ensure_directories_exist()
        
        assert Config.BASE_DIR.exists()
        assert Config.ASSIGNMENTS_DIR.exists()
    
    def test_list_projects_empty(self):
        """Testa listagem de projetos quando não há nenhum"""
        projects = FileManager.list_projects()
        assert projects == []
    
    def test_list_projects_with_data(self):
        """Testa listagem de projetos com dados"""
        Config.BASE_DIR.mkdir(parents=True, exist_ok=True)
        (Config.BASE_DIR / "project_001").mkdir()
        (Config.BASE_DIR / "project_002").mkdir()
        (Config.BASE_DIR / "assignments").mkdir()  # Deve ser ignorado
        
        projects = FileManager.list_projects()
        
        assert len(projects) == 2
        assert "project_001" in projects
        assert "project_002" in projects
        assert "assignments" not in projects
    
    def test_list_assignments(self):
        """Testa listagem de assignments"""
        Config.ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)
        (Config.ASSIGNMENTS_DIR / "assignment1.md").touch()
        (Config.ASSIGNMENTS_DIR / "assignment2.md").touch()
        
        assignments = FileManager.list_assignments()
        
        assert len(assignments) == 2
        assert "assignment1.md" in assignments
        assert "assignment2.md" in assignments
    
    def test_list_attachments(self):
        """Testa listagem de anexos de um projeto"""
        project_dir = Config.BASE_DIR / "test_project" / "attachments"
        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "image1.jpg").touch()
        (project_dir / "image2.png").touch()
        
        attachments = FileManager.list_attachments("test_project")
        
        assert len(attachments) == 2
        assert "image1.jpg" in attachments
        assert "image2.png" in attachments


class TestProjectManager:
    """Testes para a classe ProjectManager"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_base_dir = Config.BASE_DIR
        Config.BASE_DIR = Path(self.temp_dir) / "test_projects"
        Config.ASSIGNMENTS_DIR = Config.BASE_DIR / "assignments"
        
        self.project_manager = ProjectManager()
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        Config.BASE_DIR = self.original_base_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_get_next_project_number_empty(self):
        """Testa número do próximo projeto quando não há nenhum"""
        number = self.project_manager._get_next_project_number()
        assert number == 1
    
    def test_get_next_project_number_with_existing(self):
        """Testa número do próximo projeto com projetos existentes"""
        Config.BASE_DIR.mkdir(parents=True, exist_ok=True)
        (Config.BASE_DIR / "project_001").mkdir()
        (Config.BASE_DIR / "project_003").mkdir()
        
        number = self.project_manager._get_next_project_number()
        assert number == 4
    
    def test_create_project_structure(self):
        """Testa criação da estrutura de projeto"""
        project_path = Config.BASE_DIR / "test_project"
        
        self.project_manager._create_project_structure(project_path)
        
        assert project_path.exists()
        assert (project_path / "sources").exists()
        assert (project_path / "attachments").exists()
    
    @patch('builtins.input', side_effect=[
        'FAESA',                           # instituicao
        'Centro Universitário',            # unidade
        'GRADUAÇÃO',                       # tipo
        'Engenharia de Software',          # curso
        'João Silva',                      # aluno
        'Título Teste',                    # titulo
        '',                                # subtitulo
        'SP',                              # local
        'Computação Distribuída',          # disciplina
        'Prof. Silva',                     # orientador
    ])
    def test_collect_metadata(self, mock_input):
        """Testa coleta de metadados"""
        metadata = self.project_manager._collect_metadata()

        assert metadata['curso'] == 'Engenharia de Software'
        assert metadata['aluno'] == 'João Silva'
        assert metadata['titulo'] == 'Título Teste'
        assert metadata['ano'] == datetime.now().year


class TestTemplateGenerator:
    """Testes para a classe TemplateGenerator"""
    
    @patch('academic_manager.core.template_generator.get_template_json')
    @patch('academic_manager.core.template_generator.process_json')
    def test_generate_ai_template_success(self, mock_process_json, mock_get_template):
        """Testa geração bem-sucedida de template via IA"""
        # Mock responses
        mock_get_template.return_value = '{"title": "Test", "sections": []}'
        mock_process_json.return_value = {}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = Path(f.name)
        
        try:
            result = TemplateGenerator.generate_ai_template(
                "Assignment content",
                {},
                output_path,
                "test_project"
            )
            
            assert result is not None
            assert result["title"] == "Test"
            mock_get_template.assert_called_once()
        
        finally:
            output_path.unlink(missing_ok=True)
    
    @patch('academic_manager.core.template_generator.FileManager.list_assignments')
    @patch('academic_manager.core.template_generator.UserInterface.select_from_list')
    @patch('builtins.open', new_callable=mock_open, read_data="Assignment content")
    def test_select_assignment_success(self, mock_file, mock_select, mock_list):
        """Testa seleção bem-sucedida de assignment"""
        mock_list.return_value = ["assignment1.md", "assignment2.md"]
        mock_select.return_value = "assignment1.md"
        
        result = TemplateGenerator.select_assignment()
        
        assert result == "Assignment content"
        mock_list.assert_called_once()
        mock_select.assert_called_once()


class TestPDFGenerator:
    """Testes para a classe PDFGenerator"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_base_dir = Config.BASE_DIR
        Config.BASE_DIR = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        Config.BASE_DIR = self.original_base_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('academic_manager.core.pdf_generator.AcademicWork')
    def test_generate_pdf_success(self, mock_academic_work):
        """Testa geração bem-sucedida de PDF"""
        # Setup
        project_name = "test_project"
        project_path = Config.BASE_DIR / project_name
        project_path.mkdir(parents=True)
        (project_path / "sources").mkdir()

        metadata = {
            "titulo": "Test Title",
            "curso": "Engineering",
            "aluno": "John Doe"
        }

        template = {
            "sections": [
                {"name": "Introduction", "blocks": [{"type": "paragraph", "text": "Test"}]}
            ]
        }

        # Mock do AcademicWork
        mock_pdf = Mock()
        mock_academic_work.return_value = mock_pdf
        mock_pdf.page_no.return_value = 1

        generator = PDFGenerator()
        result = generator.generate_pdf(project_name, metadata, template)

        assert result is True
        mock_academic_work.assert_called_once()
        mock_pdf.add_cover.assert_called_once()
        mock_pdf.add_back_cover.assert_called_once()


class TestAIStudioChat:
    """Testes para o módulo aistudio_chat"""

    def setup_method(self):
        """Cria a estrutura de diretórios necessária para salvar o prompt.md."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_base_dir = Config.BASE_DIR
        Config.BASE_DIR = Path(self.temp_dir)
        project_dir = Config.BASE_DIR / "test_project"
        project_dir.mkdir(parents=True, exist_ok=True)

    def teardown_method(self):
        Config.BASE_DIR = self.original_base_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('requests.post')
    def test_get_template_json_success(self, mock_post):
        """Testa chamada bem-sucedida para API do Gemini"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": '{"title": "Test Template"}'}]
                }
            }]
        }
        mock_post.return_value = mock_response

        result = get_template_json("Test assignment", False, "test_project")

        assert result == '{"title": "Test Template"}'
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_get_template_json_error(self, mock_post):
        """Testa tratamento de erro na API"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        result = get_template_json("Test assignment", False, "test_project")

        assert result is None


class TestBingImages:
    """Testes para o módulo bing_images"""
    
    @patch('requests.get')
    def test_get_image_url_success(self, mock_get):
        """Testa busca bem-sucedida de URL de imagem"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
            <a class="iusc" m='{"murl":"https://example.com/image.jpg"}'></a>
        '''
        mock_get.return_value = mock_response
        
        result = get_image_url("test query")
        
        assert result == "https://example.com/image.jpg"
    
    @patch('requests.get')
    def test_get_image_url_no_results(self, mock_get):
        """Testa busca sem resultados"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>No images</body></html>'
        mock_get.return_value = mock_response
        
        result = get_image_url("test query")
        
        assert result is None
    
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_download_image_success(self, mock_file, mock_get):
        """Testa download bem-sucedido de imagem"""
        mock_response = Mock()
        mock_response.content = b'fake image data'
        mock_get.return_value = mock_response
        
        download_image("https://example.com/image.jpg", "test_image.jpg")
        
        mock_get.assert_called_once()
        mock_file.assert_called_once_with("test_image.jpg", "wb")
    
    @patch('academic_manager.services.bing_images.get_image_url')
    @patch('academic_manager.services.bing_images.download_image')
    def test_process_json(self, mock_download, mock_get_url):
        """Testa processamento de JSON para baixar imagens"""
        # Note: bing_images.process_json reads block['query'], not block['text']
        json_data = {
            "sections": [{
                "blocks": [
                    {
                        "type": "image",
                        "query": "A beautiful landscape",
                        "text": "Caption text"
                    },
                    {
                        "type": "paragraph",
                        "text": "Some text"
                    }
                ]
            }]
        }

        mock_get_url.return_value = "https://example.com/image.jpg"

        result = process_json(json_data, "test_project")

        assert "imagem_1" in result
        mock_get_url.assert_called_with("A beautiful landscape")
        mock_download.assert_called_once()


class TestUserInterface:
    """Testes para a classe UserInterface"""
    
    @patch('builtins.input', return_value='user input')
    def test_input_with_default_user_input(self, mock_input):
        """Testa entrada com input do usuário"""
        result = UserInterface.input_with_default("Enter value", "default")
        assert result == "user input"
    
    @patch('builtins.input', return_value='')
    def test_input_with_default_default_value(self, mock_input):
        """Testa entrada com valor padrão"""
        result = UserInterface.input_with_default("Enter value", "default")
        assert result == "default"
    
    @patch('builtins.input', return_value='2')
    def test_select_from_list_valid_choice(self, mock_input):
        """Testa seleção válida de lista"""
        items = ["Option 1", "Option 2", "Option 3"]
        result = UserInterface.select_from_list(items, "Choose option")
        assert result == "Option 2"
    
    @patch('builtins.input', return_value='5')
    def test_select_from_list_invalid_choice(self, mock_input):
        """Testa seleção inválida de lista"""
        items = ["Option 1", "Option 2"]
        result = UserInterface.select_from_list(items, "Choose option")
        assert result is None
    
    def test_select_from_list_empty_list(self):
        """Testa seleção com lista vazia"""
        result = UserInterface.select_from_list([], "Choose option")
        assert result is None
    
    @patch('builtins.input', return_value='a')
    def test_get_user_choice_valid(self, mock_input):
        """Testa escolha válida do usuário"""
        result = UserInterface.get_user_choice("Choose", ['a', 'b', 'c'])
        assert result == 'a'
    
    @patch('builtins.input', return_value='q')
    def test_get_user_choice_quit(self, mock_input):
        """Testa comando de saída"""
        result = UserInterface.get_user_choice("Choose", ['a', 'b', 'c'])
        assert result == 'q'
    
    @patch('builtins.input', return_value='x')
    def test_get_user_choice_invalid(self, mock_input):
        """Testa escolha inválida"""
        result = UserInterface.get_user_choice("Choose", ['a', 'b', 'c'])
        assert result is None


# Testes de integração
class TestIntegration:
    """Testes de integração entre componentes"""

    def setup_method(self):
        """Setup para testes de integração"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_base_dir = Config.BASE_DIR
        self.original_assignments_dir = Config.ASSIGNMENTS_DIR
        Config.BASE_DIR = Path(self.temp_dir)
        Config.ASSIGNMENTS_DIR = Config.BASE_DIR / "assignments"
        # Ensure directories exist so ProjectManager.__init__ doesn't fail
        Config.BASE_DIR.mkdir(parents=True, exist_ok=True)
        Config.ASSIGNMENTS_DIR.mkdir(parents=True, exist_ok=True)

    def teardown_method(self):
        """Cleanup após testes"""
        Config.BASE_DIR = self.original_base_dir
        Config.ASSIGNMENTS_DIR = self.original_assignments_dir
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('builtins.input', side_effect=[
        'test_project',             # Nome do projeto
        'FIM',                      # assignment multiline terminator
        'FAESA',                    # instituicao
        'Centro Universitário',     # unidade
        'GRADUAÇÃO',                # tipo
        'Engenharia',               # curso
        'João',                     # aluno
        'Título',                   # titulo
        '',                         # subtitulo
        'SP',                       # local
        'Disciplina',               # disciplina
        'Prof',                     # orientador
    ])
    def test_full_project_creation_workflow(self, mock_input):
        """Testa o workflow completo de criação de projeto"""
        project_manager = ProjectManager()

        result = project_manager.create_new_project()
        
        assert result is not None
        project_name, metadata = result
        
        # Verifica se o projeto foi criado
        project_path = Config.BASE_DIR / project_name
        assert project_path.exists()
        assert (project_path / "sources").exists()
        assert (project_path / "attachments").exists()
        assert (project_path / "settings.json").exists()
        
        # Verifica os metadados
        assert metadata['aluno'] == 'João'
        assert metadata['curso'] == 'Engenharia'


# Fixtures para testes
@pytest.fixture
def sample_academic_data():
    """Dados de exemplo para trabalho acadêmico"""
    return {
        "curso": "Engenharia de Software",
        "aluno": "João Silva",
        "titulo": "Sistema de Testes Automatizados",
        "local": "São Paulo",
        "ano": 2024,
        "disciplina": "Engenharia de Software",
        "orientador": "Prof. Maria Santos"
    }


@pytest.fixture
def sample_template():
    """Template de exemplo"""
    return {
        "title": "Sistema de Testes",
        "sections": [
            {
                "name": "Introdução",
                "blocks": [
                    {
                        "type": "paragraph",
                        "text": "Este trabalho apresenta um sistema de testes automatizados."
                    }
                ]
            },
            {
                "name": "Desenvolvimento",
                "blocks": [
                    {
                        "type": "subtitle",
                        "text": "Metodologia"
                    },
                    {
                        "type": "paragraph",
                        "text": "A metodologia utilizada foi baseada em TDD."
                    }
                ]
            }
        ]
    }


# Testes parametrizados
class TestParametrized:
    """Testes parametrizados para diferentes cenários"""
    
    @pytest.mark.parametrize("align,expected", [
        ("L", "L"),
        ("C", "C"),
        ("R", "R"),
        ("J", "J")
    ])
    def test_paragraph_alignments(self, align, expected):
        """Testa diferentes alinhamentos de parágrafo"""
        result = paragraph("Teste", align=align)
        assert result["align"] == expected
    
    @pytest.mark.parametrize("position,expected", [
        ("left", "left"),
        ("right", "right"),
        ("center", "center"),
        ("above", "above"),
        ("below", "below")
    ])
    def test_image_positions(self, position, expected):
        """Testa diferentes posições de imagem"""
        result = img("test.jpg", position=position)
        assert result["position"] == expected
    
    @pytest.mark.parametrize("font_style,expected", [
        ("B", "B"),
        ("I", "I"),
        ("U", "U"),
        ("BI", "BI")
    ])
    def test_subtitle_font_styles(self, font_style, expected):
        """Testa diferentes estilos de fonte para subtítulo"""
        result = subtitle("Teste", style=font_style)
        assert result["font"]["style"] == expected


# Configuração de pytest
if __name__ == "__main__":
    # Configurações para executar os testes
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--cov=academic_manager",
        "--cov-report=html",
        "--cov-report=term-missing"
    ])
