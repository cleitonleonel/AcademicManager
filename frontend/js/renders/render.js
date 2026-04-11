
// render.js
import { appData } from "./data.js";
import { getStatusText } from "./utils.js";

export function renderStats() {
  const statsGrid = document.getElementById('stats-grid');
  const stats = appData.stats;
  statsGrid.innerHTML = `
    <div class="card"><h3>${stats.activeProjects}</h3><p>Projetos Ativos</p></div>
    <div class="card"><h3>${stats.generatedPDFs}</h3><p>PDFs Gerados</p></div>
    <div class="card"><h3>${stats.inProgress}</h3><p>Em Progresso</p></div>
    <div class="card"><h3>${stats.uploadedFiles}</h3><p>Arquivos Enviados</p></div>`;
}

export function renderRecentActivity() {
  const el = document.getElementById('recent-activity');
  el.innerHTML = appData.recentActivity.map(a => `
    <div><i class="${a.icon}" style="color:${a.color}"></i>
      <strong>${a.title}</strong> - ${a.message}<div>${a.time}</div></div>`).join('');
}

export function renderProjects() {
  const el = document.getElementById('projects-grid');
  el.innerHTML = appData.projects.map(p => `
    <div class="project-card">
      <h3>${p.title}</h3><p>${p.description}</p>
      <span>${getStatusText(p.status)}</span>
    </div>`).join('');
}

export function renderFiles() {
  const el = document.getElementById('files-list');
  el.innerHTML = appData.files.map(f => `
    <div><i class="${f.icon}" style="color:${f.color}"></i> ${f.name} (${f.size})</div>`).join('');
}

export function renderTemplates() {
  const el = document.getElementById('templates-grid');
  el.innerHTML = appData.templates.map(t => `
    <div class="card"><h3>${t.name}</h3><p>${t.description}</p></div>`).join('');
}

export function renderSystemInfo() {
  const el = document.getElementById('system-info');
  const c = appData.config.system;
  el.innerHTML = `<div>Versão: ${c.version}</div><div>Python: ${c.pythonVersion}</div>`;
}
