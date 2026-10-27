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

https://github.com/user-attachments/assets/74552b2f-a0b9-49fb-b8e7-628796b093cf

O **AcademicManager** é uma ferramenta para automação de trabalhos acadêmicos. Ele utiliza inteligência artificial (Gemini) para processar enunciados, gerar templates estruturados e exportar documentos PDF e PPTX formatados.

## ✨ Novidades da Versão Modernizada

O projeto possui uma interface web baseada em FastAPI e um modo de terminal:

- **Dashboard Administrativo**: Visualize seu progresso com gráficos de atividade em tempo real.
- **Configurações Dinâmicas**: Informe a chave de API e preferências pela interface web, com persistência por sessão (LocalStorage).
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

# Crie a configuração local (não versionada)
cp config-dev.ini config.ini
# Edite config.ini e informe sua chave da API

# Suba o ambiente com um comando
docker compose up -d
```

O sistema estará disponível em:
- 🌐 Interface de Usuário: [http://localhost:8000/](http://localhost:8000/)
- 📚 Documentação da API: [http://localhost:8000/docs](http://localhost:8000/docs)

> [!TIP]
> Os projetos criados serão salvos na pasta `academic_projects/` do seu computador, graças ao volume do Docker. Essa pasta contém dados gerados/localmente armazenados e não deve ser enviada ao Git.

Para encerrar o ambiente:

```bash
docker compose down
```

### 2. Instalação Local (Poetry)

Requisitos: Python 3.10 ou superior, Poetry e, para a exportação de PDF, as fontes Liberation Sans instaladas no sistema.

```bash
# Crie a configuração local (não versionada)
cp config-dev.ini config.ini
# Edite config.ini e informe sua chave da API

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
2. Copie `config-dev.ini` para `config.ini` e insira a chave em `api_key`.
3. Como alternativa, informe a chave diretamente na tela de *Configurações* do Dashboard; nesse caso, ela vale apenas para a sessão atual.

`config.ini` é ignorado pelo Git para evitar o envio de credenciais. Nunca publique uma chave de API no repositório; se ela for exposta, revogue-a e gere outra.

---

## 🏗️ Estrutura do Projeto

- `academic_manager/`: Motor central (Core, PDF, Services).
- `api/`: Backend FastAPI, rotas e lógica assíncrona.
- `frontend/`: Dashboard moderno (HTML/CSS/JS).
- `academic_projects/`: Diretório onde seus trabalhos são armazenados localmente (ignorado pelo Git).
- `config-dev.ini`: Modelo de configuração sem credenciais.
- `config.ini`: Configuração local com credenciais (não versionada).

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
- **API**: Testes de integração dos endpoints HTTP usando `TestClient`.
- **Exportação**: Geração de arquivos PDF e PPTX.
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
