# Academic Manager 🎓

<p align="center">
  <img src="static/img/academic_manager.png" alt="AcademicManager" width="45%" height="auto">
</p>

<p align="center">
  <i>Transforme enunciados em trabalhos acadêmicos profissionais com o poder da IA.</i>
</p>

<p align="center">
<a href="https://github.com/cleitonleonel/AcademicManager" target="_blank">
  <img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-green" alt="Supported Python Versions"/>
</a>
<img src="https://img.shields.io/badge/docker-ready-blue" alt="Docker Ready"/>
<img src="https://img.shields.io/badge/status-modernized-orange" alt="Status Modernized"/>
</p>

---

O **AcademicManager** é uma ferramenta robusta para automação de trabalhos acadêmicos. Ele utiliza inteligência artificial (Gemini) para processar enunciados, gerar templates estruturados e exportar documentos PDF formatados seguindo padrões acadêmicos.

## ✨ Novidades da Versão Modernizada

Recentemente o projeto passou por uma grande evolução, ganhando uma interface web de última geração e ferramentas de BI:

- **Dashboard Administrativo**: Visualize seu progresso com gráficos de atividade em tempo real.
- **Configurações Dinâmicas**: Altere chaves de API, fontes de PDF e preferências gerais diretamente na UI, com persistência por sessão (LocalStorage).
- **Sistema de Backup & Restore**: Proteja seus projetos exportando e importando pacotes compactados (.zip) de forma integrada.
- **Híbrido por Design**: Escolha entre o modo terminal (CLI) clássico ou a nova experiência Web.

---

## 🚀 Como Rodar

### 1. Usando Docker (Recomendado)

A maneira mais rápida e limpa de subir o projeto em qualquer ambiente.

```bash
# Clone e entre na pasta
git clone https://github.com/cleitonleonel/AcademicManager.git
cd AcademicManager

# Suba o ambiente com um comando
docker compose up -d
```

O sistema estará disponível em:
- 🌐 Interface de Usuário: [http://localhost:8000/](http://localhost:8000/)
- 📚 Documentação da API: [http://localhost:8000/docs](http://localhost:8000/docs)

> [!TIP]
> Os projetos criados serão salvos na pasta `academic_projects/` do seu computador, graças aos volumes do Docker.

### 2. Instalação Local (Poetry)

```bash
# Instale as dependências
poetry install

# Modo Web
poetry run python main.py --web

# Modo Terminal (CLI)
poetry run python main.py
```

---

## 🛠️ Configuração da API Key

Para utilizar as funcionalidades de IA (Gemini):
1. Obtenha sua chave em [aistudio.google.com](https://aistudio.google.com).
2. Você pode configurá-la de duas formas:
   - **Fixa**: Renomeie `config-dev.ini` para `config.ini` e insira a chave.
   - **Dinâmica**: Insira a chave diretamente na tela de *Configurações* do Dashboard (válido para a sessão atual).

---

## 🏗️ Estrutura do Projeto

- `academic_manager/`: Motor central (Core, PDF, Services).
- `api/`: Backend FastAPI, rotas e lógica assíncrona.
- `frontend/`: Dashboard moderno (HTML/CSS/JS).
- `academic_projects/`: Diretorio onde seus trabalhos são armazenados.

---

## 🧪 Qualidade e Testes

O projeto utiliza o `pytest` para garantir a estabilidade das funcionalidades centrais e da API.

### Como rodar os testes

Você pode executar os testes de três formas diferentes:

#### 1. Via Poetry (Desenvolvimento Local)
```bash
# Executa todos os testes e mostra a cobertura no terminal
poetry run pytest

# Gera um relatório HTML detalhado de cobertura
poetry run pytest --cov-report=html
```

#### 2. Via Docker (Consistência Total)
Execute os testes dentro do container para garantir que o ambiente seja idêntico ao de produção:
```bash
docker compose run --rm academic-manager pytest
```

#### 3. Via Pip (Manual)
```bash
python -m pytest
```

### O que é testado?
- **Core**: Validação da geração de PDF, lógica de templates e manipulação de arquivos.
- **API**: Testes de integração de todos os endpoints HTTP usando `TestClient`.
- **Stress**: Testes de performance para garantir estabilidade sob carga.
- **Cobertura**: Relatórios automáticos que mostram exatamente quais partes do código foram testadas.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

## 👨‍💻 Autor

Cleiton Leonel Creton - [@cleitonleonel](https://github.com/cleitonleonel)

---

> [!IMPORTANT]
> Este projeto é uma ferramenta de auxílio acadêmico. Lembre-se sempre de revisar o conteúdo gerado pela IA para garantir a precisão e a qualidade do seu trabalho.
