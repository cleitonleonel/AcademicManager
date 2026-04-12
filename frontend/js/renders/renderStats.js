/* jshint esversion: 9 */
'use strict';


import {appData} from "../data.js";

export function renderStats() {
	const statsGrid = document.getElementById("stats-grid");
	const stats = appData.stats || { 
    activeProjects: 0, 
    generatedPDFs: 0, 
    completedProjects: 0, 
    inProgress: 0, 
    draftProjects: 0, 
    uploadedFiles: 0 
  };
	const projects = appData.projects || [];
  
  // Transformando os gráficos em dados REAIS e dinâmicos de Proporção:
  const total = stats.activeProjects > 0 ? stats.activeProjects : 1;
  
  // Usar contagem de PROJETOS para as porcentagens (mais preciso que contagem de arquivos)
  const pCom = Math.round((stats.completedProjects / total) * 100);
  const pPro = Math.round((stats.inProgress / total) * 100);
  const pDra = Math.max(0, 100 - pCom - pPro);
  
  const progPct = `${pPro}%`;

  const pTotal1 = pCom;
  const pTotal2 = pCom + pPro;
  const donutGradient = `conic-gradient(var(--success-color) 0% ${pTotal1}%, var(--warning-color) ${pTotal1}% ${pTotal2}%, var(--info-color) ${pTotal2}% 100%)`;

  // === ALGORITMO CRONOLÓGICO REAL ===
  // Agrupar arquivos gerados/atualizados em 6 períodos temporais no passado
  let buckets = [0, 0, 0, 0, 0, 0];
  const today = new Date();
  
  projects.forEach(p => {
    let dateStr = p.updated_date || p.created_date;
    if (dateStr) {
      let d = new Date(dateStr);
      let diffDays = Math.floor(Math.abs(today - d) / (1000 * 60 * 60 * 24));
      let bucketIdx = Math.floor(diffDays / 7); // Agrupando blocos de Semanas
      
      if (bucketIdx < 6) {
        // Peso do projeto: 1 (criação base) + quantidade de vezes que você salvou alterações nele (edit_count)
        let weight = p.edit_count ? 1 + p.edit_count : 1;
        buckets[5 - bucketIdx] += weight; // Soma a "Temperatura de Atividade" da semana
      }
    }
  });

  // Alteramos o teto máximo: O gráfico agora reage mais rápido
  // Com 5 edições ele já chega perto do topo (antes precisava de 10)
  const maxB = Math.max(...buckets, 5);
  // O +5 é só para a barra nunca sumir do piso visual, e limitamos a 100
  const heights = buckets.map(v => Math.min(100, Math.round((v / maxB) * 100) + 5));
  const [b1, b2, b3, b4, b5, b6] = heights;

  // Calculando vetor SVG Flexível Baseado nas mesmas datas:
  const pts = buckets.map((v, i) => {
    let x = i * 20; // 0, 20, 40, 60, 80, 100
    // O eixo Y começa no topo (0) e vai até baixo (40).
    // Pontos escalam num range de até 30px, com 5px de margem superior (35 a 5 base)
    let y = 35 - Math.round((v / maxB) * 30);
    return `${x},${y}`;
  });
  const linePath = `M0,${pts[0].split(',')[1]} L${pts.join(' L')}`;
  const areaPath = `M0,40 L0,${pts[0].split(',')[1]} L${pts.join(' L')} L100,40 Z`;
  // ==================================

  statsGrid.innerHTML = `
    <div class="card stat-card-modern" style="padding: 1.5rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h3 style="margin-bottom:0; font-size:1rem; color:var(--text-secondary);">Projetos Ativos</h3>
          <div style="padding: 6px; border-radius: 8px; background: rgba(99, 102, 241, 0.15); color: var(--primary-color);"><i class="fas fa-layer-group"></i></div>
        </div>
        <h3 class="stat-value" style="font-size: 2.2rem; margin: 0.5rem 0;">${stats.activeProjects}</h3>
        <p class="stat-label" style="color: var(--success-color); font-size: 0.8rem; text-transform:none;"><i class="fas fa-history"></i> Histórico: 6 Semanas</p>
      </div>
      <!-- Bar Chart Dinâmico de volume -->
      <div style="display:flex; gap: 6px; align-items:flex-end; height: 35px; margin-top: 1rem;">
        <div style="width: 15%; height: ${b1}%; background: var(--primary-color); border-radius: 3px;" title="Há 5 semanas"></div>
        <div style="width: 15%; height: ${b2}%; background: var(--accent-color); border-radius: 3px;" title="Há 4 semanas"></div>
        <div style="width: 15%; height: ${b3}%; background: var(--primary-color); border-radius: 3px;" title="Há 3 semanas"></div>
        <div style="width: 15%; height: ${b4}%; background: var(--accent-color); border-radius: 3px;" title="Há 2 semanas"></div>
        <div style="width: 15%; height: ${b5}%; background: var(--primary-color); border-radius: 3px;" title="Há 1 semana"></div>
        <div style="width: 15%; height: ${b6}%; background: var(--accent-color); border-radius: 3px;" title="Esta semana"></div>
      </div>
    </div>

    <div class="card stat-card-modern" style="padding: 1.5rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h3 style="margin-bottom:0; font-size:1rem; color:var(--text-secondary);">Em Progresso</h3>
          <div style="padding: 6px; border-radius: 8px; background: rgba(217, 119, 6, 0.15); color: var(--warning-color);"><i class="fas fa-spinner"></i></div>
        </div>
        <h3 class="stat-value" style="font-size: 2.2rem; margin: 0.5rem 0;">${stats.inProgress}</h3>
        <p class="stat-label" style="color: var(--warning-color); font-size: 0.8rem; text-transform:none;">${pPro}% do Total</p>
      </div>
      <!-- Barra Progresso Real Matemática -->
      <div style="margin-top: 1rem;">
        <div style="width: 100%; height: 8px; background: rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden;">
          <div style="width: ${progPct}; height: 100%; background: linear-gradient(90deg, var(--warning-color), #fcd34d); border-radius: 6px; transition: width 1s ease;"></div>
        </div>
      </div>
    </div>

    <div class="card stat-card-modern" style="padding: 1.5rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h3 style="margin-bottom:0; font-size:1rem; color:var(--text-secondary);">Rascunhos</h3>
          <div style="padding: 6px; border-radius: 8px; background: rgba(37, 99, 235, 0.15); color: var(--info-color);"><i class="fas fa-pencil-alt"></i></div>
        </div>
        <h3 class="stat-value" style="font-size: 2.2rem; margin: 0.5rem 0;">${stats.draftProjects}</h3>
        <p class="stat-label" style="color: var(--info-color); font-size: 0.8rem; text-transform:none;">${pDra}% do Total</p>
      </div>
      <div style="margin-top: 1rem;">
        <div style="width: 100%; height: 8px; background: rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden;">
          <div style="width: ${pDra}%; height: 100%; background: linear-gradient(90deg, var(--info-color), #60a5fa); border-radius: 6px; transition: width 1s ease;"></div>
        </div>
      </div>
    </div>

    <div class="card stat-card-modern" style="padding: 1.5rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h3 style="margin-bottom:0; font-size:1rem; color:var(--text-secondary);">PDFs Gerados</h3>
          <div style="padding: 6px; border-radius: 8px; background: rgba(16, 185, 129, 0.15); color: var(--success-color);"><i class="fas fa-file-pdf"></i></div>
        </div>
        <h3 class="stat-value" style="font-size: 2.2rem; margin: 0.5rem 0;">${stats.generatedPDFs}</h3>
        <p class="stat-label" style="color: var(--success-color); font-size: 0.8rem; text-transform:none;">Curva de Movimentação</p>
      </div>
      <!-- SVG Vetorial (Linha de ritmo ilustrativa) -->
      <div style="margin-top: 1rem; height: 40px; width: 100%; opacity: 0.8;">
        <svg viewBox="0 0 100 40" width="100%" height="100%" preserveAspectRatio="none">
          <path d="${areaPath}" fill="rgba(16, 185, 129, 0.2)" stroke="none" />
          <path d="${linePath}" fill="none" stroke="var(--success-color)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
    </div>

    <div class="card stat-card-modern" style="padding: 1.5rem; display:flex; flex-direction:column; justify-content:space-between;">
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h3 style="margin-bottom:0; font-size:1rem; color:var(--text-secondary);">Status dos Projetos</h3>
          <div style="padding: 6px; border-radius: 8px; background: rgba(37, 99, 235, 0.15); color: var(--info-color);"><i class="fas fa-chart-pie"></i></div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 0.5rem;">
          <div>
            <h3 class="stat-value" style="font-size: 2.2rem; margin: 0;">${stats.uploadedFiles}</h3>
            <p class="stat-label" style="color: var(--text-secondary); font-size: 0.8rem; text-transform:none;">Total de Arquivos</p>
          </div>
          <!-- Real CSS Donut Chart Matemático -->
          <div style="margin-bottom: 0.2rem;">
            <div style="width: 52px; height: 52px; border-radius: 50%; background: ${donutGradient}; display:flex; align-items:center; justify-content:center; box-shadow: 0 0 8px rgba(0,0,0,0.1);">
              <div style="width: 28px; height: 28px; border-radius:50%; background: var(--surface-bg);"></div>
            </div>
          </div>
        </div>
        <!-- Legenda do Gráfico -->
        <div style="margin-top: 1.2rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.75rem; color: var(--text-secondary);">
          <div style="display:flex; align-items:center; gap: 5px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--success-color);"></span>
            <span>Concluídos: ${pCom}%</span>
          </div>
          <div style="display:flex; align-items:center; gap: 5px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--warning-color);"></span>
            <span>Em Progresso: ${pPro}%</span>
          </div>
          <div style="display:flex; align-items:center; gap: 5px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--info-color);"></span>
            <span>Rascunhos: ${pDra}%</span>
          </div>
        </div>
      </div>
    </div>
  `;
}

