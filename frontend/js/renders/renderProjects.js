/* jshint esversion: 9 */
'use strict';

import { appData } from "../data.js";
import { apiRequest, downloadFile } from "../api.js";
import { getStatusText } from "../utils.js";
import { showSection } from "../navigation.js";

/** Notification helper (duplicated minimally to avoid circular imports) */
function notify(msg, type = 'success') {
  const el = document.getElementById('notification');
  if (!el) return;
  el.textContent = msg;
  el.className = `notification ${type}`;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 4000);
}

function setLoading(show, text = 'Processando...') {
  const modal = document.getElementById('loadingModal');
  const label = document.getElementById('loadingText');
  if (!modal) return;
  if (label) label.textContent = text;
  modal.style.display = show ? 'block' : 'none';
  document.body.style.overflow = show ? 'hidden' : 'auto';
}

/** Generate and download a PDF for the given project. */
export async function generatePDF(projectId) {
  try {
    setLoading(true, 'Gerando PDF…');
    // 1. Trigger generation
    await apiRequest(`/projects/${projectId}/pdf`, { method: 'POST' });
    // 2. Download the resulting file
    const blobUrl = await downloadFile(`/projects/${projectId}/pdf/download`);
    const anchor = document.createElement('a');
    anchor.href = blobUrl;
    anchor.download = `${projectId}.pdf`;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(blobUrl), 10_000);
    notify('PDF gerado e download iniciado!', 'success');
  } catch (err) {
    notify(`Erro ao gerar PDF: ${err.message}`, 'error');
  } finally {
    setLoading(false);
  }
}

/** Generate and download a PPTX for the given project. */
export async function generatePPTX(projectId) {
  try {
    setLoading(true, 'Gerando Slides PPTX…');
    // 1. Trigger generation
    await apiRequest(`/projects/${projectId}/pptx`, { method: 'POST' });
    // 2. Download the resulting file
    const blobUrl = await downloadFile(`/projects/${projectId}/pptx/download`);
    const anchor = document.createElement('a');
    anchor.href = blobUrl;
    anchor.download = `${projectId}.pptx`;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(blobUrl), 10_000);
    notify('Slides PPTX gerados e download iniciado!', 'success');
  } catch (err) {
    notify(`Erro ao gerar PPTX: ${err.message}`, 'error');
  } finally {
    setLoading(false);
  }
}

/** Navigate to the edit form for the given project. */
export async function editProject(projectId) {
  setLoading(true, 'Carregando dados do projeto...');
  try {
    const res = await apiRequest(`/projects/${projectId}`);
    if (!res || !res.project) throw new Error("Projeto não encontrado");
    const project = res.project;

    // Fill the "new project" form with existing data from the API
    const set = (id, val) => { const el = document.getElementById(id); if (el) el.value = val ?? ''; };
    set('projectTitle',       project.titulo);
    set('projectType',        project.tipo);
    set('projectAuthor',      project.aluno);
    set('projectAdvisor',     project.orientador);
    set('projectInstitution', project.instituicao);
    set('projectCourse',      project.curso);
    set('projectUnit',        project.unidade);
    set('projectCity',        project.local);
    set('projectYear',        project.ano);
    set('projectSubtitle',    project.subtitulo);
    set('projectDiscipline',  project.disciplina);

    // Store editing state
    const hiddenId = document.getElementById('projectId');
    if (hiddenId) hiddenId.value = projectId;

    // Change button label
    const submitBtn = document.querySelector('#newProjectForm button[type="submit"]');
    if (submitBtn) submitBtn.innerHTML = '<i class="fas fa-save"></i> Salvar Alterações';

    // Show delete button
    const deleteBtn = document.getElementById('deleteProjectBtn');
    if (deleteBtn) {
      deleteBtn.style.display = 'inline-flex';
      deleteBtn.onclick = () => deleteProject(projectId);
    }

    // Navigate to form
    const newProjectNav = document.querySelector('.nav-item[data-section="new-project"]');
    if (newProjectNav) newProjectNav.click();
  } catch (err) {
    notify(`Erro ao carregar projeto: ${err.message}`, 'error');
  } finally {
    setLoading(false);
  }
}

/** Delete a project after confirmation. */
async function deleteProject(projectId) {
  if (!confirm(`Remover o projeto "${projectId}" permanentemente?`)) return;
  try {
    setLoading(true, 'Removendo projeto…');
    await apiRequest(`/projects/${projectId}`, { method: 'DELETE' });
    appData.projects = appData.projects.filter(p => p.id !== projectId);
    renderProjects();
    notify('Projeto removido com sucesso.', 'success');
    document.querySelector('.nav-item[data-section="projects"]')?.click();
  } catch (err) {
    notify(`Erro ao remover: ${err.message}`, 'error');
  } finally {
    setLoading(false);
  }
}

/** Load projects from the real API and refresh the grid. */
export async function loadAndRenderProjects() {
  try {
    const res = await apiRequest('/projects');
    if (res.projects) {
      appData.projects = res.projects;
    }
  } catch (err) {
    console.warn('Could not load projects from API:', err.message);
  }
  renderProjects();
}

/** Render the projects grid from appData (may be local or API-sourced). */
export function renderProjects() {
  const container = document.getElementById('projects-grid');
  if (!container) return;

  if (!appData.projects.length) {
    container.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:3rem; color:#999;">
        <i class="fas fa-folder-open" style="font-size:3rem; margin-bottom:1rem; display:block;"></i>
        Nenhum projeto encontrado. <a href="#" id="goCreate">Crie o primeiro!</a>
      </div>`;
    container.querySelector('#goCreate')?.addEventListener('click', e => {
      e.preventDefault();
      document.querySelector('.nav-item[data-section="new-project"]')?.click();
    });
    return;
  }

  container.innerHTML = appData.projects.map(p => {
    const statusClass = p.status === 'completed'
      ? 'completed'
      : p.status === 'progress' ? 'progress' : 'draft';

    return `
      <div class="card project-card" data-id="${p.id}">
        <h3>${p.title}</h3>
        <p>${p.description}</p>
        <div style="margin-bottom:1rem;">
          <span class="badge ${statusClass}">${getStatusText(p.status)}</span>
        </div>
        <small style="color:var(--text-secondary); display:block; margin-bottom:1.5rem; font-weight: 500;">
          <i class="fas fa-user" style="color:var(--primary-color);"></i> ${p.author || '—'}
        </small>
        <div class="project-actions">
          <button class="btn btn-edit" data-action="edit" title="Editar projeto">
            <i class="fas fa-edit"></i> Editar
          </button>
          <button class="btn btn-success btn-file" data-action="pdf" title="Gerar e baixar PDF">
            <i class="fas fa-file-pdf"></i> PDF
          </button>
          <button class="btn btn-pptx" data-action="pptx" title="Gerar e baixar PPTX (Slides)"
                  style="background-color:#D24726; border-color:#D24726; color:white;">
            <i class="fas fa-file-powerpoint"></i> PPTX
          </button>
          <button class="btn btn-danger btn-delete" data-action="delete" title="Remover projeto"
                  style="padding:8px 12px;">
            <i class="fas fa-trash"></i>
          </button>
        </div>
      </div>`;
  }).join('');

  // Wire up events
  container.querySelectorAll('.btn-edit').forEach(btn =>
    btn.addEventListener('click', () => editProject(btn.closest('.project-card').dataset.id))
  );
  container.querySelectorAll('.btn-file').forEach(btn =>
    btn.addEventListener('click', () => generatePDF(btn.closest('.project-card').dataset.id))
  );
  container.querySelectorAll('.btn-pptx').forEach(btn =>
    btn.addEventListener('click', () => generatePPTX(btn.closest('.project-card').dataset.id))
  );
  container.querySelectorAll('.btn-delete').forEach(btn =>
    btn.addEventListener('click', () => deleteProject(btn.closest('.project-card').dataset.id))
  );
}
