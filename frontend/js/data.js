/* jshint esversion: 9 */
'use strict';


export const DATA = {
  stats: { activeProjects: 3, generatedPDFs: 7, inProgress: 2, uploadedFiles: 15 },
  projects: [
    { id: 1, title: 'Dissertação de Mestrado', description: 'Análise de Machine Learning em Sistemas Distribuídos', status: 'progress', author: 'João Silva', type: 'dissertacao', created_at: '2024-01-15', updated_at: '2024-02-20' },
    { id: 2, title: 'Artigo Científico', description: 'Blockchain aplicado à Educação Digital', status: 'completed', author: 'Maria Santos', type: 'artigo', created_at: '2024-01-10', updated_at: '2024-02-15' },
    { id: 3, title: 'TCC - Graduação', description: 'Sistema de Gestão Acadêmica com IA', status: 'draft', author: 'Pedro Costa', type: 'tcc', created_at: '2024-02-01', updated_at: '2024-02-18' }
  ],
  recentActivity: [
    { id: 1, type: 'pdf_generated', icon: 'fas fa-file-pdf', color: '#dc3545', title: 'Dissertação de Mestrado', message: 'PDF gerado com sucesso', time: 'Há 2 horas' },
    { id: 2, type: 'project_created', icon: 'fas fa-folder-plus', color: '#28a745', title: 'Projeto TCC', message: 'Novo projeto criado', time: 'Ontem' },
    { id: 3, type: 'file_uploaded', icon: 'fas fa-upload', color: '#667eea', title: 'Referencias.bib', message: 'Arquivo enviado', time: 'Há 3 dias' }
  ],
  files: [
    { id: 1, name: 'referencias.bib', size: '234 KB', type: 'bib', icon: 'fas fa-file-pdf', color: '#dc3545', uploaded_at: 'Há 2 horas' },
    { id: 2, name: 'diagrama_arquitetura.png', size: '1.2 MB', type: 'image', icon: 'fas fa-image', color: '#28a745', uploaded_at: 'Ontem' },
    { id: 3, name: 'capitulo1_rascunho.docx', size: '856 KB', type: 'document', icon: 'fas fa-file-word', color: '#0078d4', uploaded_at: 'Há 3 dias' }
  ],
  templates: [
    { id: 1, name: 'ABNT', icon: 'fas fa-graduation-cap', description: 'Template padrão brasileiro ABNT.', available: true },
    { id: 2, name: 'IEEE', icon: 'fas fa-globe', description: 'Template internacional IEEE.', available: true },
    { id: 3, name: 'APA', icon: 'fas fa-brain', description: 'Template APA.', available: true },
    { id: 4, name: 'Vancouver', icon: 'fas fa-heartbeat', description: 'Template Vancouver.', available: false }
  ],
  config: {
    api: { url: 'http://localhost:8000/api', key: '', timeout: 5000 },
    general: { language: 'pt-BR', dateFormat: 'dd/mm/yyyy', autoSave: 5 },
    system: { version: 'v1.2.0', pythonVersion: '3.10+', apiStatus: 'Desconectado', totalProjects: 3 }
  }
};

export let appData = JSON.parse(JSON.stringify(DATA));
export let currentSection = 'dashboard';
export let editingProject = null;

export function setEditingProject(project) {
  editingProject = project;
}
export function getEditingProject() {
  return editingProject;
}
