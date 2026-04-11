/* jshint esversion: 9 */
'use strict';

import { showSection } from "./navigation.js";
import { apiRequest, apiConfig } from "./api.js";
import { appData } from "./data.js";
import { renderStats } from "./renders/renderStats.js";
import { loadAndRenderProjects, renderProjects } from "./renders/renderProjects.js";
import { renderFiles } from "./renders/renderFiles.js";
import { renderTemplates } from "./renders/renderTemplates.js";
import { renderRecentActivity } from "./renders/renderRecentActivity.js";
import { renderSystemInfo } from "./renders/renderSystemInfo.js";

// ---------------------------------------------------------------------------
// Bootstrap
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', async () => {

  // 1. Render local mock data immediately (instant paint)
  renderStats();
  renderRecentActivity();
  renderProjects();
  renderFiles();
  renderTemplates();
  renderSystemInfo();

  // 2. Wire navigation
  document.querySelectorAll('.nav-item[data-section]').forEach(item => {
    item.addEventListener('click', e => {
      const sectionId = item.getAttribute('data-section');
      showSection(sectionId, e);
    });
  });

  // 3. Fetch real data from API in background
  await Promise.all([
    loadRealData(),
    fetchSystemDefaults()
  ]);

  // 4. Wire the project creation / editing form
  wireProjectForm();

  // 4.b Populate dashboard flat header date
  const dateEl = document.getElementById('dashboard-date');
  if (dateEl) {
    const opts = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateEl.textContent = new Date().toLocaleDateString('pt-BR', opts);
  }

  // 5. Theme Toggle Logic
    const savedTheme = localStorage.getItem('am_theme') || 'dark';
    document.body.setAttribute('data-theme', savedTheme);
  
    // 6. Wire Backup & Restore system
    wireBackupSystem();

    // 7. Load Settings from Session/LocalStorage
    loadSettingsUI();
  
    const themeToggleBtn = document.getElementById('themeToggleBtn');
  if (themeToggleBtn) {
    const themeIcon = themeToggleBtn.querySelector('i');
    const themeText = themeToggleBtn.querySelector('span');

    const updateThemeUI = (theme) => {
      if (!themeIcon) return;
      if (theme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        if (themeText) themeText.textContent = 'Modo Claro';
      } else {
        themeIcon.className = 'fas fa-moon';
        if (themeText) themeText.textContent = 'Modo Escuro';
      }
    };
    
    updateThemeUI(savedTheme);

    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.body.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', newTheme);
      localStorage.setItem('am_theme', newTheme);
      updateThemeUI(newTheme);
    });
  }

  console.log("Academic Manager — modular + API integrado");
});

// ---------------------------------------------------------------------------
// Real data loader
// ---------------------------------------------------------------------------

async function loadRealData() {
  try {
    // Health check — update system info
    const health = await apiRequest('/health');
    if (health.status === 'ok') {
      appData.config.system.apiStatus = 'Conectado';
      appData.config.system.totalProjects = health.projects_count ?? 0;
    }
  } catch (_) {
    appData.config.system.apiStatus = 'Desconectado';
  }

  try {
    // Stats
    const stats = await apiRequest('/stats');
    if (stats) {
      appData.stats.activeProjects = stats.active_projects ?? appData.stats.activeProjects;
      appData.stats.generatedPDFs  = stats.generated_pdfs  ?? appData.stats.generatedPDFs;
      appData.stats.inProgress     = stats.in_progress      ?? appData.stats.inProgress;
      appData.stats.uploadedFiles  = stats.total_files      ?? appData.stats.uploadedFiles;
    }
  } catch (_) {}

  // Projects (also re-renders the grid)
  await loadAndRenderProjects();

  // Final re-render integrating real API data into UI modules
  renderRecentActivity();
  renderStats();
  renderSystemInfo();
}

// ---------------------------------------------------------------------------
// Project form wiring
// ---------------------------------------------------------------------------

function wireProjectForm() {
  const form = document.getElementById('newProjectForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const editingId = document.getElementById('projectId')?.value?.trim();

    const payload = {
      titulo:      document.getElementById('projectTitle')?.value?.trim()       || '',
      tipo:        document.getElementById('projectType')?.value                 || 'GRADUAÇÃO',
      aluno:       document.getElementById('projectAuthor')?.value?.trim()      || '',
      orientador:  document.getElementById('projectAdvisor')?.value?.trim()     || '',
      instituicao: document.getElementById('projectInstitution')?.value?.trim() || '',
      unidade:     document.getElementById('projectUnit')?.value?.trim()        || '',
      curso:       document.getElementById('projectCourse')?.value?.trim()      || '',
      disciplina:  document.getElementById('projectDiscipline')?.value?.trim()  || '',
      local:       document.getElementById('projectCity')?.value?.trim()        || '',
      ano:         parseInt(document.getElementById('projectYear')?.value)      || new Date().getFullYear(),
      subtitulo:   document.getElementById('projectSubtitle')?.value?.trim()    || '',
      assignment:  document.getElementById('projectAssignment')?.value?.trim()  || null,
    };

    const modal  = document.getElementById('loadingModal');
    const label  = document.getElementById('loadingText');
    const notify = (msg, type) => {
      const el = document.getElementById('notification');
      if (!el) return;
      el.textContent = msg; el.className = `notification ${type}`; el.classList.add('show');
      setTimeout(() => el.classList.remove('show'), 4000);
    };

    if (label) label.textContent = editingId ? 'Salvando alterações…' : 'Criando projeto…';
    if (modal) modal.style.display = 'block';

    try {
      if (editingId) {
        await apiRequest(`/projects/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(payload),
        });
        notify('Projeto atualizado com sucesso!', 'success');
      } else {
        await apiRequest('/projects', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
        notify('Projeto criado com sucesso!', 'success');
      }

      form.reset();
      if (document.getElementById('projectId')) document.getElementById('projectId').value = '';
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.innerHTML = '<i class="fas fa-save"></i> Criar Projeto';
      const deleteBtn = document.getElementById('deleteProjectBtn');
      if (deleteBtn) deleteBtn.style.display = 'none';

      await loadAndRenderProjects();
      await loadRealData();

      document.querySelector('.nav-item[data-section="projects"]')?.click();
    } catch (err) {
      notify(`Erro: ${err.message}`, 'error');
    } finally {
      if (modal) modal.style.display = 'none';
    }
  });
}
// ---------------------------------------------------------------------------
// Backup & Restore system wiring
// ---------------------------------------------------------------------------

function wireBackupSystem() {
  const doBackupBtn = document.getElementById('doBackupBtn');
  const doRestoreBtn = document.getElementById('doRestoreBtn');
  const fileInput = document.getElementById('restoreFileInput');

  if (doBackupBtn) {
    doBackupBtn.addEventListener('click', () => {
      notify('Iniciando geração do backup...', 'info');
      window.location.href = '/api/system/backup';
    });
  }

  if (doRestoreBtn && fileInput) {
    doRestoreBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', async () => {
      if (!fileInput.files || fileInput.files.length === 0) return;
      
      const file = fileInput.files[0];
      if (!confirm(`Deseja restaurar o backup "${file.name}"? Isso pode sobrescrever dados atuais.`)) {
        fileInput.value = '';
        return;
      }

      const formData = new FormData();
      formData.append('file', file);

      const modal = document.getElementById('loadingModal');
      const label = document.getElementById('loadingText');
      if (label) label.textContent = 'Restaurando backup...';
      if (modal) modal.style.display = 'block';

      try {
        const response = await fetch('/api/system/restore', {
          method: 'POST',
          body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
          notify('Backup restaurado com sucesso!', 'success');
          // Reload everything to see restored projects
          await loadRealData();
        } else {
          throw new Error(result.detail || 'Falha ao restaurar');
        }
      } catch (err) {
        notify(`Erro: ${err.message}`, 'error');
      } finally {
        if (modal) modal.style.display = 'none';
        fileInput.value = '';
      }
    });
  }
}
// ---------------------------------------------------------------------------
// Settings Management (Session-based)
// ---------------------------------------------------------------------------

function notify(msg, type) {
  const el = document.getElementById('notification');
  if (!el) return;
  el.textContent = msg; 
  el.className = `notification ${type}`; 
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 4000);
}

async function fetchSystemDefaults() {
  try {
    const data = await apiRequest('/system/defaults');
    if (data.status === 'success') {
      // Preenche caminhos do sistema que o usuário não altera via UI
      if (document.getElementById('projectsDirectory')) {
        document.getElementById('projectsDirectory').value = data.base_dir || './academic_projects/';
      }
    }
  } catch (err) {
    console.warn('Não foi possível carregar padrões do servidor:', err.message);
  }
}

function loadSettingsUI() {
  // Configurações de API
  document.getElementById('apiUrl').value = apiConfig.baseUrl;
  document.getElementById('apiKey').value = apiConfig.apiKey;
  document.getElementById('apiTimeout').value = apiConfig.timeout;

  // Configurações de PDF
  if (apiConfig.pdfOptions) {
    document.getElementById('defaultFont').value = apiConfig.pdfOptions.font || 'Arial';
    document.getElementById('imageQuality').value = apiConfig.pdfOptions.quality || 'high';
    document.getElementById('pdfCompression').value = apiConfig.pdfOptions.compression || 'none';
  }

  // Preferências Gerais (LocalStorage direto)
  const general = JSON.parse(localStorage.getItem('academic_general_config') || '{}');
  if (general.language) document.getElementById('defaultLanguage').value = general.language;
  if (general.dateFormat) document.getElementById('dateFormat').value = general.dateFormat;
}

window.saveApiConfig = function() {
  apiConfig.baseUrl = document.getElementById('apiUrl').value;
  apiConfig.apiKey = document.getElementById('apiKey').value;
  apiConfig.timeout = parseInt(document.getElementById('apiTimeout').value) || 10000;
  
  localStorage.setItem('academic_api_config', JSON.stringify(apiConfig));
  notify('Configurações de API salvas para esta sessão!', 'success');
};

window.savePdfConfig = function() {
  apiConfig.pdfOptions = {
    font: document.getElementById('defaultFont').value,
    quality: document.getElementById('imageQuality').value,
    compression: document.getElementById('pdfCompression').value
  };
  
  localStorage.setItem('academic_api_config', JSON.stringify(apiConfig));
  notify('Preferências de PDF atualizadas!', 'success');
};

window.saveGeneralConfig = function() {
  const config = {
    language: document.getElementById('defaultLanguage').value,
    dateFormat: document.getElementById('dateFormat').value
  };
  localStorage.setItem('academic_general_config', JSON.stringify(config));
  notify('Preferências gerais salvas!', 'success');
};

window.testApiConnection = async function() {
  try {
    const data = await apiRequest('/health');
    if (data.status === 'ok') {
      notify('Conexão com a API estabelecida com sucesso!', 'success');
    }
  } catch (err) {
    notify('Falha ao conectar com a API: ' + err.message, 'error');
  }
};
