/* jshint esversion: 9 */
'use strict';

import { appData } from "../data.js";

export function renderRecentActivity() {
  const container = document.getElementById("recent-activity");
  if (!container) return;

  const projects = [...(appData.projects || [])];
  
  // Sort projects by last_activity (fallback to updated_date then created_date)
  projects.sort((a, b) => {
    const ta = a.last_activity || a.updated_date || a.created_date || 0;
    const tb = b.last_activity || b.updated_date || b.created_date || 0;
    const da = ta ? new Date(ta).getTime() : 0;
    const db = tb ? new Date(tb).getTime() : 0;
    return db - da;
  });

  const recent = projects.slice(0, 4);

  if (recent.length === 0) {
    container.innerHTML = '<p style="color: #666; font-style: italic;">Nenhuma atividade recente no sistema.</p>';
    return;
  }

  container.innerHTML = recent.map(p => {
    const activityDate = p.last_activity || p.updated_date || p.created_date;
    let timeStr = activityDate 
      ? new Date(activityDate).toLocaleDateString() 
      : 'Projeto Antigo';
      
    // Tratar informações caso estejam vazias
    const author = p.author ? p.author : "Desconhecido";
    const statusText = p.status ? p.status.toUpperCase() : "N/A";

    // Transformar atividade recente em Card Vertical, simulando a barra de progresso
    const progressPerc = p.status === 'completed' ? '100%' : (p.status === 'progress' ? '50%' : '15%');
    const badgeColor = p.status === 'completed' ? 'var(--success-color)' : (p.status === 'progress' ? 'var(--warning-color)' : 'var(--primary-color)');

    return `
      <div class="card project-card" style="padding: 1.5rem;">
        <div style="display:flex; justify-content:space-between; margin-bottom: 0.5rem; align-items:flex-start;">
          <h3 style="margin-bottom:0; font-size: 1.15rem;">${p.title}</h3>
          <i class="fas fa-ellipsis-v" style="color:var(--text-secondary); cursor:pointer;"></i>
        </div>
        <div style="margin-bottom:1.5rem;">
          <span class="badge" style="background: rgba(99, 102, 241, 0.15); color: ${badgeColor}; padding: 0.2rem 0.6rem; font-size: 0.70rem;">${statusText}</span>
          <span class="badge" style="background: rgba(100, 116, 139, 0.2); color: var(--text-secondary); padding: 0.2rem 0.6rem; font-size: 0.70rem;">${p.type || 'Acadêmico'}</span>
        </div>
        
        <div style="margin-bottom: 1.5rem;">
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 0.4rem; color: var(--text-secondary);">
            <span>Progresso</span>
            <span>${progressPerc}</span>
          </div>
          <div style="width: 100%; height: 6px; background: rgba(0,0,0,0.2); border-radius: 4px; overflow: hidden;">
            <div style="width: ${progressPerc}; height: 100%; background: linear-gradient(90deg, var(--primary-color), var(--accent-color)); border-radius: 4px;"></div>
          </div>
        </div>

        <div style="font-size: 0.85rem; color: var(--text-secondary); flex: 1;">
          <p style="margin-bottom: 0.3rem;"><strong style="color:var(--text-primary);">• Atualização:</strong> Arquivos lidos na pasta</p>
          <p style="margin-bottom: 0.3rem;"><strong style="color:var(--text-primary);">• ID:</strong> ${p.id}</p>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; border-top: 1px solid var(--surface-border); padding-top: 1rem;">
          <div style="display:flex; gap: 5px; align-items:center;">
             <div style="width:24px; height:24px; border-radius:50%; background:var(--primary-color); color:white; display:flex; align-items:center; justify-content:center; font-size:0.6rem;"><i class="fas fa-user-graduate"></i></div>
             <span style="font-size:0.8rem; font-weight:600; color:var(--text-primary); margin-left:4px;">${author}</span>
          </div>
          <div style="font-size: 0.75rem; color: var(--text-secondary);">
            <i class="fas fa-calendar-alt"></i> ${timeStr}
          </div>
        </div>
      </div>
    `;
  }).join('');
}
