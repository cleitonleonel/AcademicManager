# Suíte de Testes - Academic Manager

## Visão Geral

Este projeto é um **sistema automatizado para geração de trabalhos acadêmicos em PDF**. O sistema integra:

- **IA (Google Gemini)** para geração de conteúdo estruturado
- **Web scraping (Bing Images)** para busca automática de imagens
- **Geração de PDF** com formatação acadêmica padrão
- **Interface de linha de comando** para interação com o usuário

## Estrutura dos Testes

### 1. Testes Unitários

#### `TestBuilderFunctions`
- Testa funções auxiliares para criação de elementos (parágrafo, subtítulo, imagem)
- Verifica estrutura correta dos dicionários retornados

#### `TestContentBuilder`
- Testa a classe que constrói conteúdo de forma fluente
- Verifica method chaining e gerenciamento de estado
- Testa adição e limpeza de conteúdo

#### `TestAcademicWork`
- Testa a classe principal para geração de PDF
- Verifica criação de capa, contracapa e seções
- Testa diferentes tipos de conteúdo (texto, imagem, lista)

#### `TestFileManager`
- Testa operações de sistema de arquivos
- Verifica criação de diretórios e listagem de arquivos
- Testa gerenciamento de projetos e anexos

#### `TestProjectManager`
- Testa criação e atualização de projetos
- Verifica estrutura de diretórios e metadados
- Testa numeração automática de projetos

#### `TestTemplateGenerator`
- Testa geração de templates via IA
- Verifica seleção e leitura de assignments
- Testa integração com APIs externas

#### `TestPDFGenerator`
- Testa geração final do PDF
- Verifica integração entre metadados e templates
- Testa criação de arquivos de saída

### 2. Testes de Serviços Externos

#### `TestAIStudioChat`
- Testa integração com Google Gemini API
- Verifica formatação de requests e parsing de responses
- Testa tratamento de erros da API

#### `TestBingImages`
- Testa busca e download de imagens
- Verifica parsing de HTML do Bing
- Testa processamento de JSON para extração de descrições

### 3. Testes de Interface

#### `TestUserInterface`
- Testa métodos de interação com usuário
- Verifica validação de entrada e seleção de opções
- Testa comportamento com entradas inválidas

### 4. Testes de Integração

#### `TestIntegration`
- Testa workflows completos do sistema
- Verifica integração entre componentes
- Testa cenários end-to-end

### 5. Testes Parametrizados

#### `TestParametrized`
- Testa múltiplos valores para parâmetros
- Verifica diferentes configurações de alinhamento, posição e estilos

## Configuração dos Testes

### Dependências Necessárias

```bash
pip install pytest pytest-cov pytest-mock beautifulsoup4 requests fpdf2
```

### Estrutura de Arquivos

```
tests/
├── conftest.py                 # Configurações globais do pytest
├── test_academic_manager.py    # Suíte principal de testes
├── fixtures/                   # Dados de teste
│   ├── sample_assignment.txt
│   ├── sample_template.json
│   └── test_images/
└── reports/                    # Relatórios de cobertura
    ├── htmlcov/
    └── coverage.xml
```

### Arquivo conftest.py

```python
import pytest
import tempfile
import shutil
from pathlib import Path
from academic_manager.config.settings import Config

@pytest.fixture(scope="session")
def temp_workspace():
    """Cria workspace temporário para todos os testes"""
    temp_dir = tempfile.mkdtemp()
    original_base_dir = Config.BASE_DIR
    Config.BASE_DIR = Path(temp_dir) / "test_projects"
    Config.ASSIGNMENTS_DIR = Config.BASE_DIR / "assignments"
    
    yield temp_dir
    
    Config.BASE_DIR = original_base_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock para API key"""
    monkeypatch.setenv("API_KEY", "test_api_key_123")

@pytest.fixture
def sample_assignment_content():
    """Conteúdo de exemplo para assignment"""
    return """
    Desenvolva um trabalho sobre Inteligência Artificial aplicada à educação.
    O trabalho deve conter:
    - Introdução ao tema
    - Desenvolvimento com exemplos práticos
    - Conclusão com reflexões
    - Referências bibliográficas
    """
```

### Executando os Testes

#### Executar todos os testes:
```bash
pytest tests/ -v
```

#### Executar com cobertura:
```bash
pytest tests/ --cov=academic_manager --cov-report=html --cov-report=term-missing
```

#### Executar testes específicos:
```bash
pytest tests/test_academic_manager.py::TestContentBuilder -v
```

#### Executar com profiling:
```bash
pytest tests/ --profile --profile-svg
```

## Casos de Teste Detalhados

### Testes de Robustez

#### Tratamento de Erros
- **Arquivos inexistentes**: Testa comportamento quando arquivos não existem
- **Permissões negadas**: Simula erros de permissão de escrita
- **API indisponível**: Testa fallback quando serviços externos falham
- **JSON malformado**: Verifica parsing de dados corrompidos

#### Casos Extremos
- **Textos muito longos**: Testa formatação com conteúdo extenso
- **Caracteres especiais**: Verifica encoding UTF-8 e caracteres acentuados
- **Imagens grandes**: Testa redimensionamento automático
- **Memória limitada**: Simula condições de baixa memória

### Testes de Performance

```python
import pytest
import time

class TestPerformance:
    """Testes de performance do sistema"""
    
    def test_pdf_generation_time(self):
        """Verifica se PDF é gerado em tempo aceitável"""
        start_time = time.time()
        # ... gerar PDF ...
        end_time = time.time()
        
        assert (end_time - start_time) < 30  # Máximo 30 segundos
    
    def test_image_download_timeout(self):
        """Testa timeout em downloads de imagem"""
        with patch('requests.get', side_effect=requests.exceptions.Timeout):
            result = download_image("http://example.com/image.jpg", "test.jpg")
            assert result is None
```

### Mocks e Fixtures Avançados

```python
@pytest.fixture
def mock_gemini_api():
    """Mock completo da API do Gemini"""
    with patch('academic_manager.services.aistudio_chat.requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "title": "IA na Educação",
                            "sections": [
                                {
                                    "name": "Introdução",
                                    "blocks": [
                                        {
                                            "type": "paragraph",
                                            "text": "A inteligência artificial revoluciona a educação..."
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
def mock_bing_search():
    """Mock para busca de imagens no Bing"""
    with patch('academic_manager.services.bing_images.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '''
        <div class="imgres">
            <a class="iusc" m='{"murl":"https://example.com/ai_education.jpg"}'>
            </a>
        </div>
        '''
        mock_get.return_value = mock_response
        yield mock_get
```

## Testes de Segurança

### Validação de Entrada

```python
class TestSecurity:
    """Testes de segurança"""
    
    def test_path_traversal_prevention(self):
        """Testa prevenção de path traversal"""
        malicious_path = "../../../etc/passwd"
        with pytest.raises(SecurityError):
            FileManager.read_file(malicious_path)
    
    def test_xss_prevention_in_content(self):
        """Testa prevenção de XSS em conteúdo"""
        malicious_content = "<script>alert('xss')</script>"
        result = paragraph(malicious_content)
        assert "<script>" not in result["text"]
    
    def test_api_key_not_logged(self):
        """Verifica que API key não aparece em logs"""
        with patch('builtins.print') as mock_print:
            get_template_json("test", False, "project")
            
            # Verifica que nenhum print contém a API key
            for call in mock_print.call_args_list:
                assert "test_api_key_123" not in str(call)
```

## Testes de Regressão

```python
class TestRegression:
    """Testes para prevenir regressões"""
    
    def test_pdf_output_consistency(self):
        """Verifica consistência do PDF gerado"""
        # Gera PDF com dados conhecidos
        metadata = {...}
        template = {...}
        
        pdf_path = generate_pdf("test_project", metadata, template)
        
        # Verifica características do PDF
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 1000  # Tamanho mínimo
        
        # Verifica conteúdo específico
        with open(pdf_path, 'rb') as f:
            content = f.read()
            assert b"SUMARIO" in content  # Sumário em português
            assert metadata["aluno"].encode() in content
    
    def test_json_template_structure(self):
        """Verifica estrutura consistente do template JSON"""
        template = generate_template("Assignment content")
        
        required_keys = ["title", "sections"]
        assert all(key in template for key in required_keys)
        
        for section in template["sections"]:
            assert "name" in section
            assert "blocks" in section
            
            for block in section["blocks"]:
                assert "type" in block
                assert block["type"] in ["paragraph", "subtitle", "image", "list"]
```

## Relatórios e Métricas

### Configuração do Coverage

```ini
# .coveragerc
[run]
source = academic_manager
omit = 
    */tests/*
    */venv/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError

[html]
directory = tests/reports/htmlcov
```

### Métricas Esperadas

- **Cobertura de código**: Mínimo 85%
- **Tempo de execução**: Todos os testes em < 2 minutos
- **Taxa de sucesso**: 100% em ambiente controlado
- **Testes por componente**: Mínimo 5 testes por classe principal

## Integração Contínua

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-mock
    
    - name: Run tests
      run: |
        pytest tests/ --cov=academic_manager --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

## Troubleshooting

### Problemas Comuns

1. **ImportError**: Verifique PYTHONPATH e instalação de dependências
2. **FileNotFoundError**: Confirme criação de diretórios temporários
3. **API Timeout**: Use mocks para testes offline
4. **Encoding Issues**: Force UTF-8 em todas as operações de arquivo

### Debug de Testes

```python
# Para debug detalhado
pytest tests/ -v -s --tb=long --pdb

# Para executar um teste específico com debug
pytest tests/test_academic_manager.py::TestContentBuilder::test_add_paragraph -v -s
```

## Conclusão

Esta suíte de testes garante a qualidade e confiabilidade do Academic Manager, cobrindo:

- ✅ **Funcionalidade completa** - Todos os componentes testados
- ✅ **Integração robusta** - Workflows end-to-end validados  
- ✅ **Tratamento de erros** - Cenários de falha cobertos
- ✅ **Performance adequada** - Tempos de execução monitorados
- ✅ **Segurança básica** - Validações de entrada implementadas
- ✅ **Manutenibilidade** - Testes organizados e documentados

Os testes servem como documentação viva do sistema e garantem que mudanças futuras não quebrem funcionalidades existentes.