/* jshint esversion: 9 */
'use strict';

import { appData } from "../data.js";

// Variable to hold the notification timeout ID to prevent race conditions
let notifyTimeout;

function notify(msg, type = 'success') {
  const el = document.getElementById('notification');
  if (!el) return;
  el.textContent = msg;
  // Reset classes fully to apply the new type and show state
  el.className = `notification ${type} show`;
  
  if (notifyTimeout) clearTimeout(notifyTimeout);
  notifyTimeout = setTimeout(() => {
    el.classList.remove('show');
  }, 4000);
}

export function renderTemplates() {
  const container = document.getElementById("templates-grid");
  if (!container) return;

  container.innerHTML = appData.templates.map(t => `
    <div class="card template-card">
      <h3>${t.name}</h3>
      <p>${t.description}</p>
      <div style="margin-top: 1rem;">
        <button class="btn btn-view-template" data-name="${t.name}" style="margin-right: 0.5rem;">
          <i class="fas fa-eye"></i> Exibir
        </button>
        <button class="btn btn-success btn-use-template" data-name="${t.name}">
          <i class="fas fa-download"></i> Usar
        </button>
      </div>
    </div>
  `).join('');

  container.querySelectorAll('.btn-view-template').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const name = e.currentTarget.getAttribute('data-name');
      notify(`O template ${name} aplica estilos automáticos de fonte e margem na geração do PDF.`, 'info');
    });
  });

  container.querySelectorAll('.btn-use-template').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const name = e.currentTarget.getAttribute('data-name');
      
      // Auto-fill form fields
      const typeSelect = document.getElementById('projectType');
      if (typeSelect) {
        // Try mapping known templates to typical graduation types or just log it
        // ABNT -> Graduação, APA -> Mestrado etc, or just leave it.
      }
      const titleInput = document.getElementById('projectTitle');
      if (titleInput) {
        titleInput.value = `Novo Trabalho - Formato ${name}`;
      }
      
      notify(`Template ${name} ativado. Preencha os detalhes do projeto.`, 'success');
      document.querySelector('.nav-item[data-section="new-project"]')?.click();
    });
  });
}
