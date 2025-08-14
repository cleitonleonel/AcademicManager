# Academic Manager

<p align="center">
  <a href="https://github.com/cleitonleonel/SmartBot">
    <img src="static/img/academic_manager.png" alt="AcademicManager" width="45%" height="auto">
  </a>
</p>

<p align="center">
  <i>Ferramenta Python com foco na geração de trabalhos acadêmicos em PDF.
</i>
</p>

<p align="center">
<a href="https://github.com/cleitonleonel/AcademicManager" target="_blank">
  <img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-green" alt="Supported Python Versions"/>
</a>
</p>

---

![academic_manager.gif](static/img/academic_manager.gif)

## 🚀 Características

- **Geração de PDFs**: Criação de documentos acadêmicos usando `fpdf2`.
- **Integração HTTP**: Comunicação com APIs externas via `requests`.
- **Arquitetura Modular**: Estrutura organizada em módulos (`core`, `services`, `ui`, `utils`) para escalabilidade.
- **Gestão de Projetos Acadêmicos**: Organização de trabalhos, instruções e arquivos de fontes e anexos.
- **Python Moderno**: Compatível com Python 3.12+.

---

## 📦 Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Poetry (para gerenciamento de dependências)

### Instalação via Poetry

```bash
# Clone o repositório
git clone https://github.com/cleitonleonel/AcademicManager.git
cd academic_manager

# Instale as dependências
poetry install

# Ative o ambiente virtual
poetry shell
```

### Obtendo a chave de api do google studio
 - Acesse o link https://aistudio.google.com e obtenha sua chave de api
 - Renomeie o arquivo `config-dev.ini` para `config.ini`
 - Adicione a chave de api no arquivo `config.ini` na chave `api_key`
 - Salve o arquivo
 - Reinicie o projeto

---

## 🏃‍♂️ Uso

Execute a aplicação usando o ponto de entrada principal:

```bash
python main.py
```

Ou através do Poetry:

```bash
poetry run python main.py
```

---

## 🏗️ Estrutura do Projeto

```
academic_manager/
├── academic_manager/
│   ├── builder.py             # Criação e montagem de projetos acadêmicos
│   ├── constants.py           # Constantes globais do sistema
│   ├── config/                # Configurações do projeto
│   │   └── settings.py
│   ├── core/                  # Núcleo da aplicação
│   │   ├── file_manager.py
│   │   ├── pdf_generator.py
│   │   ├── project_manager.py
│   │   └── template_generator.py
│   ├── models/                # Modelos de dados
│   │   └── project.py
│   ├── services/              # Integrações externas e APIs
│   │   ├── aistudio_chat.py
│   │   └── bing_images.py
│   ├── ui/                    # Interfaces e interações com o usuário
│   │   └── interface.py
│   └── utils/                 # Funções auxiliares
│       └── helpers.py
├── academic_projects/         # Projetos e trabalhos acadêmicos organizados
├── tests/                     # Testes unitários e de performance
├── main.py                    # Ponto de entrada
├── pyproject.toml             # Configuração do Poetry
└── README.md                  # Este arquivo
```

---

## 🧪 Testes

Execute os testes usando pytest:

```bash
# Executar todos os testes
poetry run pytest

# Executar com verbose
poetry run pytest -v

# Executar testes específicos
poetry run pytest tests/academic_tests.py
```

Cobertura de testes inclui:

- Execução normal da aplicação
- Tratamento de interrupção por teclado
- Propagação adequada de exceções
- Isolamento usando mocks

---

## 🛠️ Desenvolvimento

### Dependências

Produção:

- `fpdf2`: Geração de documentos PDF
- `requests`: Cliente HTTP para APIs

Desenvolvimento:

- `pytest`: Framework de testes
- `pytest-mock`: Mocking para testes

### Comandos úteis

```bash
# Instalar dependências de desenvolvimento
poetry install --with dev

# Executar testes
poetry run pytest

# Adicionar nova dependência
poetry add <package>

# Adicionar dependência de desenvolvimento
poetry add --group dev <package>
```

---

## 📋 Requisitos

- Python >= 3.10
- Bibliotecas: fpdf2, requests, pytest, pytest-mock
- Sistema operacional: Linux, macOS, Windows

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

## 👨‍💻 Autor

Cleiton Leonel Creton - [@cleitonleonel](https://github.com/cleitonleonel)

---

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto  
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)  
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)  
4. Push para a branch (`git push origin feature/nova-feature`)  
5. Abra um Pull Request

---

## 📈 Status do Projeto

Este projeto está em desenvolvimento ativo. Para relatórios de bugs ou solicitações de features, abra uma issue no GitHub.
