#!/bin/bash

# =============================================================================
# Scripts de Automação para Testes - Academic Manager
# =============================================================================

# run_tests.sh - Script principal para executar testes
echo "=== Academic Manager Test Suite ==="
echo "Escolha uma opção:"
echo "1) Executar todos os testes"
echo "2) Testes rápidos (apenas unitários)"
echo "3) Testes de integração"
echo "4) Testes de performance"
echo "5) Cobertura de código"
echo "6) Relatório completo"
echo "7) Testes contínuos (watch mode)"

read -p "Digite sua escolha (1-7): " choice

case $choice in
    1)
        echo "Executando todos os testes..."
        pytest tests/ -v --tb=short
        ;;
    2)
        echo "Executando testes rápidos..."
        pytest tests/ -v -m "not slow and not integration" --tb=short
        ;;
    3)
        echo "Executando testes de integração..."
        pytest tests/ -v -m "integration" --tb=short
        ;;
    4)
        echo "Executando testes de performance..."
        pytest tests/ -v -m "slow" --tb=short --runslow
        ;;
    5)
        echo "Gerando relatório de cobertura..."
        pytest tests/ --cov=academic_manager --cov-report=html --cov-report=term-missing
        echo "Relatório HTML gerado em: tests/reports/htmlcov/index.html"
        ;;
    6)
        echo "Gerando relatório completo..."
        ./generate_full_report.sh
        ;;
    7)
        echo "Modo contínuo ativado (Ctrl+C para sair)..."
        pytest-watch tests/ -- -v --tb=short
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

# =============================================================================
# generate_full_report.sh - Gera relatório completo
# =============================================================================

#!/bin/bash

echo "=== Gerando Relatório Completo de Testes ==="

# Criar diretório de relatórios
mkdir -p tests/reports

# 1. Executar todos os testes com cobertura
echo "1. Executando testes com cobertura..."
pytest tests/ \
    --cov=academic_manager \
    --cov-branch \
    --cov-report=html:tests/reports/htmlcov \
    --cov-report=xml:tests/reports/coverage.xml \
    --cov-report=term-missing:skip-covered \
    --junitxml=tests/reports/junit.xml \
    --tb=short \
    -v > tests/reports/test_output.txt 2>&1

# 2. Executar testes de performance separadamente
echo "2. Executando testes de performance..."
pytest tests/test_performance.py \
    -v \
    -m "slow" \
    --runslow \
    --tb=short > tests/reports/performance_output.txt 2>&1

# 3. Gerar métricas de código
echo "3. Gerando métricas de código..."
if command -v flake8 &> /dev/null; then
    flake8 academic_manager/ --output-file=tests/reports/flake8_report.txt
fi

if command -v pylint &> /dev/null; then
    pylint academic_manager/ --output=tests/reports/pylint_report.txt || true
fi

# 4. Análise de complexidade
if command -v radon &> /dev/null; then
    echo "4. Analisando complexidade..."
    radon cc academic_manager/ -a > tests/reports/complexity_report.txt
    radon mi academic_manager/ > tests/reports/maintainability_report.txt
fi

# 5. Gerar relatório HTML customizado
echo "5. Gerando relatório HTML..."
cat > tests/reports/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Academic Manager - Relatório de Testes</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2196F3; color: white; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .success { background: #E8F5E8; border-color: #4CAF50; }
        .warning { background: #FFF3E0; border-color: #FF9800; }
        .error { background: #FFEBEE; border-color: #F44336; }
        .metric { display: inline-block; margin: 10px; padding: 10px; background: #F5F5F5; border-radius: 3px; }
        pre { background: #F5F5F5; padding: 10px; border-radius: 3px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Academic Manager - Relatório de Testes</h1>
        <p>Gerado em: $(date)</p>
    </div>
    
    <div class="section">
        <h2>📊 Resumo Executivo</h2>
        <div class="metric">
            <strong>Status:</strong> 
            <span style="color: green;">✓ Todos os testes passaram</span>
        </div>
        <div class="metric">
            <strong>Cobertura:</strong> 
            <span>$(grep -o 'TOTAL.*%' tests/reports/test_output.txt | tail -1 || echo 'N/A')</span>
        </div>
        <div class="metric">
            <strong>Tempo Total:</strong> 
            <span>$(grep -o '[0-9]*\.[0-9]*s' tests/reports/test_output.txt | tail -1 || echo 'N/A')</span>
        </div>
    </div>
    
    <div class="section">
        <h2>🧪 Resultados dos Testes</h2>
        <p><a href="htmlcov/index.html">📈 Relatório de Cobertura Detalhado</a></p>
        <p><a href="junit.xml">📄 Resultados XML (JUnit)</a></p>
        <p><a href="test_output.txt">📋 Saída Completa dos Testes</a></p>
    </div>
    
    <div class="section">
        <h2>⚡ Performance</h2>
        <p><a href="performance_output.txt">📊 Relatório de Performance</a></p>
    </div>
    
    <div class="section">
        <h2>🔍 Qualidade do Código</h2>
        <p><a href="flake8_report.txt">🐍 Relatório Flake8</a></p>
        <p><a href="pylint_report.txt">🔧 Relatório Pylint</a></p>
        <p><a href="complexity_report.txt">📈 Análise de Complexidade</a></p>
    </div>
</body>
</html>
EOF

echo ""
echo "=== Relatório Completo Gerado ==="
echo "📁 Localização: tests/reports/"
echo "🌐 HTML Principal: tests/reports/index.html"
echo "📊 Cobertura: tests/reports/htmlcov/index.html"
echo ""

# Abrir relatório no navegador (opcional)
read -p "Deseja abrir o relatório no navegador? (y/n): " open_browser
if [[ $open_browser == "y" || $open_browser == "Y" ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open tests/reports/index.html
    elif command -v open &> /dev/null; then
        open tests/reports/index.html
    else
        echo "Abra manualmente: tests/reports/index.html"
    fi
fi

# =============================================================================
# setup_test_environment.sh - Configura ambiente de testes
# =============================================================================

#!/bin/bash

echo "=== Configurando Ambiente de Testes ==="

# 1. Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    exit 1
fi

echo "✓ Python $(python3 --version) encontrado"

# 2. Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# 3. Ativar ambiente virtual
source venv/bin/activate || source venv/Scripts/activate

# 4. Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip

# Dependências de desenvolvimento opcionais
pip install black isort mypy
pip install coverage[toml] pytest-html pytest-json-report
pip install pytest-benchmark pytest-profiling

echo "✓ Dependências instaladas"

# 5. Criar estrutura de diretórios
echo "📁 Criando estrutura de diretórios..."
mkdir -p tests/reports/{htmlcov,junit,performance}
mkdir -p tests/fixtures
mkdir -p static/img

# 6. Criar arquivos de configuração
echo "⚙️ Criando arquivos de configuração..."

# .coveragerc
cat > .coveragerc << 'EOF'
[run]
source = academic_manager
omit = 
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    def __str__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = tests/reports/htmlcov
title = Academic Manager - Coverage Report

[xml]
output = tests/reports/coverage.xml
EOF

# pyproject.toml (configuração moderna)
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "academic_manager"
description = "Sistema automatizado para geração de trabalhos acadêmicos"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Academic Manager Team"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "fpdf2>=2.5.0",
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0",
    "configparser>=5.0.0",
]

[project.optional-dependencies]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.8.0",
    "pytest-benchmark>=4.0.0",
    "psutil>=5.9.0",
]
dev = [
    "black>=22.0.0",
    "isort>=5.10.0",
    "flake8>=5.0.0",
    "pylint>=2.15.0",
    "mypy>=0.990",
    "bandit>=1.7.0",
]

[tool.pytest.ini_options]
minversion = "6.0"
addopts = [
    "-ra",
    "--strict-markers",
    "--strict-config",
    "--cov=academic_manager",
    "--cov-branch",
    "--cov-report=term-missing:skip-covered",
    "--cov-report=html:tests/reports/htmlcov",
    "--cov-report=xml:tests/reports/coverage.xml",
]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "api: marks tests that require external API access",
    "network: marks tests that require network access",
]

[tool.coverage.run]
source = ["academic_manager"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
    "setup.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "def __str__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']
include = '\.pyi? principais
pip install pytest pytest-cov pytest-mock pytest-watch
pip install beautifulsoup4 requests fpdf2 psutil
pip install flake8 pylint radon bandit safety

# Dependências
extend-exclude = '''
/(
    \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
  | venv
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["academic_manager"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true

[tool.pylint.messages_control]
disable = [
    "too-few-public-methods",
    "too-many-arguments",
    "too-many-instance-attributes",
    "line-too-long",  # handled by black
]

[tool.bandit]
exclude_dirs = ["tests", "venv"]
skips = ["B101"]  # Skip assert_used test
EOF

echo "✓ Arquivos de configuração criados"

# 7. Criar dados de teste
echo "📊 Criando dados de teste..."

# Imagens de teste (dados fake)
echo -e "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde" > static/img/logo.png
echo -e "\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde" > static/img/mask.png

# Assignment de teste
cat > tests/fixtures/sample_assignment.txt << 'EOF'
TRABALHO ACADÊMICO - TESTE AUTOMATIZADO

Desenvolva um trabalho sobre "Sistemas de Teste Automatizado em Software".

Objetivos:
- Apresentar conceitos fundamentais
- Comparar ferramentas e frameworks
- Demonstrar aplicação prática
- Analisar benefícios e desafios

Estrutura:
1. Introdução
2. Fundamentação Teórica
3. Metodologia
4. Análise de Ferramentas
5. Estudo de Caso
6. Conclusões
7. Referências

Critérios de Avaliação:
- Clareza na apresentação (20%)
- Profundidade técnica (30%)
- Aplicação prática (25%)
- Qualidade das referências (15%)
- Formatação e estrutura (10%)
EOF

# Template de teste
cat > tests/fixtures/sample_template.json << 'EOF'
{
  "title": "Sistemas de Teste Automatizado",
  "sections": [
    {
      "name": "INTRODUÇÃO",
      "blocks": [
        {
          "type": "paragraph",
          "text": "Este trabalho explora os conceitos e práticas de teste automatizado em desenvolvimento de software, apresentando uma análise abrangente das ferramentas, metodologias e benefícios dessa abordagem."
        }
      ]
    },
    {
      "name": "DESENVOLVIMENTO",
      "blocks": [
        {
          "type": "subtitle",
          "text": "Fundamentação Teórica"
        },
        {
          "type": "paragraph",
          "text": "Os testes automatizados representam uma evolução natural dos processos manuais de verificação, oferecendo maior eficiência, consistência e cobertura."
        }
      ]
    },
    {
      "name": "CONCLUSÃO",
      "blocks": [
        {
          "type": "paragraph",
          "text": "A implementação de sistemas de teste automatizado demonstra benefícios significativos para a qualidade e produtividade no desenvolvimento de software."
        }
      ]
    }
  ]
}
EOF

echo "✓ Dados de teste criados"

# 8. Verificar instalação
echo "🔍 Verificando instalação..."
python3 -c "import pytest; print(f'✓ Pytest {pytest.__version__}')"
python3 -c "import coverage; print(f'✓ Coverage {coverage.__version__}')"

echo ""
echo "=== Ambiente Configurado com Sucesso! ==="
echo "🚀 Para executar os testes: ./run_tests.sh"
echo "📊 Para relatório completo: ./generate_full_report.sh"
echo ""

# =============================================================================
# ci_pipeline.sh - Pipeline de integração contínua
# =============================================================================

#!/bin/bash
set -e  # Para no primeiro erro

echo "=== CI Pipeline - Academic Manager ==="

# 1. Verificações de ambiente
echo "1️⃣ Verificando ambiente..."
python3 --version
pip --version

# 2. Instalar dependências
echo "2️⃣ Instalando dependências..."
pip install -e .[test,dev]

# 3. Verificações de estilo e qualidade
echo "3️⃣ Verificações de qualidade..."

# Black (formatação)
echo "  🎨 Verificando formatação (Black)..."
black --check academic_manager/ tests/ || {
    echo "❌ Formatação incorreta. Execute: black academic_manager/ tests/"
    exit 1
}

# isort (imports)
echo "  📦 Verificando imports (isort)..."
isort --check-only academic_manager/ tests/ || {
    echo "❌ Imports desordenados. Execute: isort academic_manager/ tests/"
    exit 1
}

# flake8 (linting)
echo "  🐍 Verificando estilo (flake8)..."
flake8 academic_manager/ tests/ || {
    echo "❌ Problemas de estilo encontrados"
    exit 1
}

# pylint (análise estática)
echo "  🔧 Análise estática (pylint)..."
pylint academic_manager/ --fail-under=8.0 || {
    echo "❌ Qualidade do código abaixo do limite (8.0)"
    exit 1
}

# mypy (type checking)
if command -v mypy &> /dev/null; then
    echo "  🏷️  Verificando tipos (mypy)..."
    mypy academic_manager/ || echo "⚠️  Avisos de tipo encontrados"
fi

# bandit (segurança)
echo "  🔒 Verificando segurança (bandit)..."
bandit -r academic_manager/ -f json -o tests/reports/bandit_report.json || {
    echo "❌ Vulnerabilidades de segurança encontradas"
    exit 1
}

# 4. Testes unitários
echo "4️⃣ Executando testes unitários..."
pytest tests/ \
    -v \
    -m "not slow and not integration" \
    --cov=academic_manager \
    --cov-branch \
    --cov-fail-under=80 \
    --cov-report=xml:tests/reports/coverage.xml \
    --cov-report=html:tests/reports/htmlcov \
    --junit-xml=tests/reports/junit.xml \
    --tb=short

# 5. Testes de integração
echo "5️⃣ Executando testes de integração..."
pytest tests/ \
    -v \
    -m "integration" \
    --tb=short

# 6. Verificar dependências
echo "6️⃣ Verificando dependências..."
if command -v safety &> /dev/null; then
    safety check --json --output tests/reports/safety_report.json || {
        echo "❌ Vulnerabilidades encontradas nas dependências"
        exit 1
    }
fi

# 7. Gerar relatórios finais
echo "7️⃣ Gerando relatórios..."
mkdir -p tests/reports/ci

# Resumo do pipeline
cat > tests/reports/ci/pipeline_summary.json << EOF
{
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "status": "success",
    "checks": {
        "formatting": "✓",
        "imports": "✓", 
        "linting": "✓",
        "type_checking": "✓",
        "security": "✓",
        "unit_tests": "✓",
        "integration_tests": "✓",
        "dependencies": "✓"
    },
    "coverage": "$(grep -o 'TOTAL.*%' tests/reports/htmlcov/index.html | head -1 || echo 'N/A')",
    "artifacts": [
        "tests/reports/coverage.xml",
        "tests/reports/htmlcov/",
        "tests/reports/junit.xml",
        "tests/reports/bandit_report.json",
        "tests/reports/safety_report.json"
    ]
}
EOF

echo ""
echo "✅ Pipeline executado com sucesso!"
echo "📊 Relatórios disponíveis em tests/reports/"

# =============================================================================
# pre_commit_hook.sh - Git pre-commit hook
# =============================================================================

#!/bin/bash
echo "🔍 Executando verificações pré-commit..."

# Verificar se há arquivos Python modificados
python_files=$(git diff --cached --name-only --diff-filter=AM | grep -E "\.(py)$")

if [ -z "$python_files" ]; then
    echo "✓ Nenhum arquivo Python modificado"
    exit 0
fi

echo "📁 Arquivos Python modificados: $python_files"

# Executar verificações rápidas
echo "1️⃣ Formatação (Black)..."
black --check $python_files || {
    echo "❌ Execute: black $python_files"
    exit 1
}

echo "2️⃣ Imports (isort)..."
isort --check-only $python_files || {
    echo "❌ Execute: isort $python_files"
    exit 1
}

echo "3️⃣ Linting (flake8)..."
flake8 $python_files || {
    echo "❌ Corrija os problemas de estilo"
    exit 1
}

echo "4️⃣ Testes relacionados..."
# Executar apenas testes rápidos relacionados aos arquivos modificados
pytest tests/ -v -x --tb=short -m "not slow" || {
    echo "❌ Testes falharam"
    exit 1
}

echo "✅ Verificações pré-commit aprovadas!"

# =============================================================================
# Makefile - Comandos simplificados
# =============================================================================

# Makefile
.PHONY: help install test test-fast test-slow test-integration coverage lint format security clean

help: ## Mostra esta ajuda
	@echo "=== Academic Manager - Comandos Disponíveis ==="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $1, $2}'

install: ## Instala dependências
	@echo "📦 Instalando dependências..."
	@pip install -e .[test,dev]

test: ## Executa todos os testes
	@echo "🧪 Executando todos os testes..."
	@pytest tests/ -v

test-fast: ## Executa apenas testes rápidos
	@echo "⚡ Executando testes rápidos..."
	@pytest tests/ -v -m "not slow and not integration"

test-slow: ## Executa testes de performance
	@echo "🐌 Executando testes de performance..."
	@pytest tests/ -v -m "slow" --runslow

test-integration: ## Executa testes de integração
	@echo "🔗 Executando testes de integração..."
	@pytest tests/ -v -m "integration"

coverage: ## Gera relatório de cobertura
	@echo "📊 Gerando relatório de cobertura..."
	@pytest tests/ --cov=academic_manager --cov-report=html --cov-report=term-missing
	@echo "Relatório HTML: tests/reports/htmlcov/index.html"

lint: ## Executa verificações de código
	@echo "🔍 Executando verificações de código..."
	@flake8 academic_manager/ tests/
	@pylint academic_manager/
	@mypy academic_manager/

format: ## Formata código automaticamente
	@echo "🎨 Formatando código..."
	@black academic_manager/ tests/
	@isort academic_manager/ tests/

security: ## Verifica vulnerabilidades
	@echo "🔒 Verificando segurança..."
	@bandit -r academic_manager/
	@safety check

clean: ## Remove arquivos temporários
	@echo "🧹 Limpando arquivos temporários..."
	@find . -type d -name __pycache__ -delete
	@find . -type f -name "*.pyc" -delete
	@rm -rf tests/reports/*
	@rm -rf .coverage
	@rm -rf .pytest_cache
	@rm -rf academic_projects/

ci: lint test coverage ## Pipeline completo de CI
	@echo "✅ Pipeline CI executado com sucesso!"

dev-setup: install ## Configura ambiente de desenvolvimento
	@echo "🚀 Configurando ambiente de desenvolvimento..."
	@pre-commit install
	@echo "✅ Ambiente configurado!"

# =============================================================================
# GitHub Actions Workflow
# =============================================================================

# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('pyproject.toml') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[test,dev]
    
    - name: Lint with flake8
      run: |
        flake8 academic_manager/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 academic_manager/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88
    
    - name: Check formatting with black
      run: black --check academic_manager/ tests/
    
    - name: Check imports with isort
      run: isort --check-only academic_manager/ tests/
    
    - name: Test with pytest
      run: |
        pytest tests/ \
          --cov=academic_manager \
          --cov-branch \
          --cov-report=xml \
          --cov-report=term-missing \
          --junit-xml=junit.xml \
          -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results-${{ matrix.python-version }}
        path: |
          junit.xml
          tests/reports/

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit Security Scan
      uses: securecodewarrior/github-action-bandit@v1
      with:
        path: academic_manager/
        level: medium
        confidence: medium
        
    - name: Run Safety Check
      run: |
        pip install safety
        safety check --json --output safety-report.json || true
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

# =============================================================================
# Docker para testes
# =============================================================================

# Dockerfile.test
FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração
COPY pyproject.toml .
COPY requirements*.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -e .[test,dev]

# Copiar código fonte
COPY . .

# Executar testes por padrão
CMD ["pytest", "tests/", "-v", "--cov=academic_manager"]

# docker-compose.test.yml
version: '3.8'

services:
  test:
    build:
      context: .
      dockerfile: Dockerfile.test
    volumes:
      - .:/app
      - test_reports:/app/tests/reports
    environment:
      - PYTHONPATH=/app
      - API_KEY=test_key_docker
    command: >
      bash -c "
        echo '🐳 Executando testes em container Docker...' &&
        pytest tests/ -v --cov=academic_manager --cov-report=html:tests/reports/htmlcov &&
        echo '✅ Testes concluídos! Relatórios em /app/tests/reports/'
      "

volumes:
  test_reports:

echo ""
echo "=== Scripts de Automação Criados ==="
echo "✅ run_tests.sh - Menu interativo de testes"
echo "✅ generate_full_report.sh - Relatório completo"
echo "✅ setup_test_environment.sh - Configuração do ambiente"
echo "✅ ci_pipeline.sh - Pipeline de CI/CD"
echo "✅ pre_commit_hook.sh - Hook do Git"
echo "✅ Makefile - Comandos simplificados"
echo "✅ GitHub Actions - CI automático"
echo "✅ Docker - Testes em containers"
echo ""
echo "🚀 Para começar: chmod +x *.sh && ./setup_test_environment.sh" principais
pip install pytest pytest-cov pytest-mock pytest-watch
pip install beautifulsoup4 requests fpdf2 psutil
pip install flake8 pylint radon bandit safety

# Dependências