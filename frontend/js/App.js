/* jshint esversion: 8 */
'use strict';

const DATA = {
	stats: {
		activeProjects: 3,
		generatedPDFs: 7,
		inProgress: 2,
		uploadedFiles: 15
	},
	projects: [
		{
			id: 'dissertacao',
			title: 'Dissertação de Mestrado',
			description: 'Análise de Machine Learning em Sistemas Distribuídos',
			status: 'progress',
			author: 'João Silva',
			type: 'dissertacao',
			created_at: '2024-01-15',
			updated_at: '2024-02-20'
		},
		{
			id: 'artigo',
			title: 'Artigo Científico',
			description: 'Blockchain aplicado à Educação Digital',
			status: 'completed',
			author: 'Maria Santos',
			type: 'artigo',
			created_at: '2024-01-10',
			updated_at: '2024-02-15'
		},
		{
			id: 'tcc',
			title: 'TCC - Graduação',
			description: 'Sistema de Gestão Acadêmica com IA',
			status: 'draft',
			author: 'Pedro Costa',
			type: 'tcc',
			created_at: '2024-02-01',
			updated_at: '2024-02-18'
		}
	],
	recentActivity: [
		{
			id: 1,
			type: 'pdf_generated',
			icon: 'fas fa-file-pdf',
			color: '#dc3545',
			title: 'Dissertação de Mestrado',
			message: 'PDF gerado com sucesso',
			time: 'Há 2 horas'
		},
		{
			id: 2,
			type: 'project_created',
			icon: 'fas fa-folder-plus',
			color: '#28a745',
			title: 'Projeto TCC',
			message: 'Novo projeto criado',
			time: 'Ontem'
		},
		{
			id: 3,
			type: 'file_uploaded',
			icon: 'fas fa-upload',
			color: '#667eea',
			title: 'Referencias.bib',
			message: 'Arquivo enviado',
			time: 'Há 3 dias'
		}
	],
	files: [
		{
			id: 1,
			name: 'referencias.bib',
			size: '234 KB',
			type: 'bib',
			icon: 'fas fa-file-pdf',
			color: '#dc3545',
			uploaded_at: 'Há 2 horas'
		},
		{
			id: 2,
			name: 'diagrama_arquitetura.png',
			size: '1.2 MB',
			type: 'image',
			icon: 'fas fa-image',
			color: '#28a745',
			uploaded_at: 'Ontem'
		},
		{
			id: 3,
			name: 'capitulo1_rascunho.docx',
			size: '856 KB',
			type: 'document',
			icon: 'fas fa-file-word',
			color: '#0078d4',
			uploaded_at: 'Há 3 dias'
		}
	],
	templates: [
		{
			id: 'abnt',
			name: 'ABNT',
			icon: 'fas fa-graduation-cap',
			description: 'Template padrão brasileiro para trabalhos acadêmicos seguindo as normas ABNT.',
			available: true
		},
		{
			id: 'ieee',
			name: 'IEEE',
			icon: 'fas fa-globe',
			description: 'Template internacional IEEE para artigos científicos e conferências.',
			available: true
		},
		{
			id: 'apa',
			name: 'APA',
			icon: 'fas fa-brain',
			description: 'Template APA para trabalhos em psicologia e ciências sociais.',
			available: true
		},
		{
			id: 'vancouver',
			name: 'Vancouver',
			icon: 'fas fa-heartbeat',
			description: 'Template Vancouver para trabalhos na área de ciências da saúde.',
			available: false
		}
	],
	config: {
		api: {
			url: 'http://localhost:8000/api',
			key: '',
			timeout: 5000
		},
		general: {
			language: 'pt-BR',
			dateFormat: 'dd/mm/yyyy',
			autoSave: 5
		},
		system: {
			version: 'v1.2.0',
			pythonVersion: '3.10+',
			apiStatus: 'Desconectado',
			totalProjects: 3
		}
	}
};

// Estado global da aplicação
let currentSection = 'dashboard';
let appData = JSON.parse(JSON.stringify(DATA)); // Deep copy dos dados

// Configuração da API
let apiConfig = {
	baseUrl: 'http://localhost:8000/api',
	apiKey: '',
	timeout: 5000
};


// Função para fazer requisições à API (com fallback para dados locais)
async function apiRequest(endpoint, options = {}) {
	try {
		const url = `${apiConfig.baseUrl}${endpoint}`;
		const config = {
			timeout: apiConfig.timeout,
			headers: {
				'Content-Type': 'application/json',
				...(apiConfig.apiKey && {'Authorization': `Bearer ${apiConfig.apiKey}`}),
				...options.headers
			},
			...options
		};
		
		const response = await fetch(url, config);
		
		if (!response.ok) {
			throw new Error(`HTTP ${response.status}: ${response.statusText}`);
		}
		
		return await response.json();
	} catch (error) {
		console.warn('API indisponível, usando dados locais:', error.message);
		// Fallback para dados locais
		return handleLocalData(endpoint, options.method);
	}
}

// Simula resposta da API usando dados locais
function handleLocalData(endpoint, method = 'GET') {
	const paths = endpoint.split('/').filter(p => p);
	
	switch (paths[0]) {
		case 'stats':
			return {stats: appData.stats};
		case 'projects':
			if (method === 'POST') {
				return {success: true, id: Date.now()};
			}
			return {projects: appData.projects};
		case 'files':
			if (paths[1] === 'upload' && method === 'POST') {
				return {success: true, uploaded: []};
			}
			return {files: appData.files};
		case 'activity':
			return {activity: appData.recentActivity};
		case 'templates':
			return {templates: appData.templates};
		case 'config':
			return {config: appData.config};
		default:
			return {success: true};
	}
}

// Funções de renderização
function renderStats() {
	const statsGrid = document.getElementById('stats-grid');
	const stats = appData.stats;
	
	statsGrid.innerHTML = `
                <div class="card" style="text-align: center;">
                    <h3 style="color: #667eea; font-size: 2rem; margin-bottom: 0.5rem;">${stats.activeProjects}</h3>
                    <p>Projetos Ativos</p>
                </div>
                <div class="card" style="text-align: center;">
                    <h3 style="color: #28a745; font-size: 2rem; margin-bottom: 0.5rem;">${stats.generatedPDFs}</h3>
                    <p>PDFs Gerados</p>
                </div>
                <div class="card" style="text-align: center;">
                    <h3 style="color: #dc3545; font-size: 2rem; margin-bottom: 0.5rem;">${stats.inProgress}</h3>
                    <p>Em Progresso</p>
                </div>
                <div class="card" style="text-align: center;">
                    <h3 style="color: #6c757d; font-size: 2rem; margin-bottom: 0.5rem;">${stats.uploadedFiles}</h3>
                    <p>Arquivos Enviados</p>
                </div>
            `;
}

function renderRecentActivity() {
	const activityContainer = document.getElementById('recent-activity');
	const activities = appData.recentActivity;
	
	activityContainer.innerHTML = activities.map(activity => `
                <div style="display: flex; align-items: center; padding: 1rem; border-bottom: 1px solid #eee;">
                    <i class="${activity.icon}" style="color: ${activity.color}; margin-right: 1rem;"></i>
                    <div>
                        <strong>${activity.title}</strong> - ${activity.message}
                        <div style="color: #666; font-size: 0.9rem;">${activity.time}</div>
                    </div>
                </div>
            `).join('');
}

function renderProjects() {
	const projectsGrid = document.getElementById('projects-grid');
	const projects = appData.projects;
	
	projectsGrid.innerHTML = projects.map(project => `
                <div class="project-card">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <div style="margin-bottom: 1rem;">
                        <span class="status-badge status-${project.status}">
                            ${getStatusText(project.status)}
                        </span>
                    </div>
                    <div class="project-actions">
                        <button class="btn" style="font-size: 0.9rem; padding: 8px 16px;" onclick="editProject('${project.id}')">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-success" style="font-size: 0.9rem; padding: 8px 16px;" onclick="generatePDF('${project.id}')">
                            <i class="fas fa-file-pdf"></i> PDF
                        </button>
                    </div>
                </div>
            `).join('');
}

function renderFiles() {
	const filesList = document.getElementById('files-list');
	const files = appData.files;
	
	filesList.innerHTML = files.map(file => `
                <div style="display: flex; align-items: center; justify-content: space-between; padding: 1rem; border-bottom: 1px solid #eee;">
                    <div style="display: flex; align-items: center;">
                        <i class="${file.icon}" style="color: ${file.color}; margin-right: 1rem; font-size: 1.2rem;"></i>
                        <div>
                            <strong>${file.name}</strong>
                            <div style="color: #666; font-size: 0.9rem;">${file.size} - ${file.uploaded_at}</div>
                        </div>
                    </div>
                    <div>
                        <button class="btn" style="padding: 6px 12px; font-size: 0.8rem;" onclick="downloadFile('${file.id}')">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="btn btn-danger" style="padding: 6px 12px; font-size: 0.8rem; margin-left: 0.5rem;" onclick="deleteFile('${file.id}')">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
}

function renderTemplates() {
	const templatesGrid = document.getElementById('templates-grid');
	const templates = appData.templates;
	
	templatesGrid.innerHTML = templates.map(template => `
                <div class="card">
                    <h3><i class="${template.icon}"></i> ${template.name}</h3>
                    <p>${template.description}</p>
                    <div style="margin-top: 1rem;">
                        <button class="btn" style="margin-right: 0.5rem;" onclick="previewTemplate('${template.id}')" ${!template.available ? 'disabled' : ''}>
                            <i class="fas fa-eye"></i> Exibir
                        </button>
                        <button class="btn btn-success" onclick="useTemplate('${template.id}')" ${!template.available ? 'disabled' : ''}>
                            <i class="fas fa-download"></i> Usar
                        </button>
                    </div>
                </div>
            `).join('');
}

function renderSystemInfo() {
	const systemInfo = document.getElementById('system-info');
	const config = appData.config.system;
	
	systemInfo.innerHTML = `
                <div><strong>Versão:</strong> ${config.version}</div>
                <div><strong>Python:</strong> ${config.pythonVersion}</div>
                <div><strong>Status API:</strong> <span style="color: ${config.apiStatus === 'Conectado' ? '#28a745' : '#dc3545'};">${config.apiStatus}</span></div>
                <div><strong>Projetos:</strong> ${config.totalProjects} ativos</div>
            `;
}

// Funções utilitárias
function getStatusText(status) {
	const statusMap = {
		'draft': 'Rascunho',
		'progress': 'Em Progresso',
		'completed': 'Concluído'
	};
	return statusMap[status] || status;
}

// Funções de ações
async function loadData() {
	try {
		setLoadingText('Carregando dados...');
		showLoading(true);
		
		// Carregar todos os dados em paralelo
		const [statsResponse, projectsResponse, filesResponse, activityResponse] = await Promise.all([
			apiRequest('/stats'),
			apiRequest('/projects'),
			apiRequest('/files'),
			apiRequest('/activity')
		]);
		
		// Atualizar dados locais
		if (statsResponse.stats) appData.stats = statsResponse.stats;
		if (projectsResponse.projects) appData.projects = projectsResponse.projects;
		if (filesResponse.files) appData.files = filesResponse.files;
		if (activityResponse.activity) appData.recentActivity = activityResponse.activity;
		
		// Re-renderizar todas as seções
		renderStats();
		renderRecentActivity();
		renderProjects();
		renderFiles();
		renderTemplates();
		renderSystemInfo();
		
		showNotification('Dados carregados com sucesso!', 'success');
	} catch (error) {
		console.error('Erro ao carregar dados:', error);
		showNotification('Erro ao carregar dados da API', 'error');
	} finally {
		showLoading(false);
	}
}

// Navigation
function showSection(sectionId) {
	// Hide all sections
	document.querySelectorAll('.content-section').forEach(section => {
		section.classList.remove('active');
	});
	// Remove active class from nav items
	document.querySelectorAll('.nav-item').forEach(item => {
		item.classList.remove('active');
	});
	// Show selected section
	document.getElementById(sectionId).classList.add('active');
	// Add active class to clicked nav item
	event.target.classList.add('active');
	currentSection = sectionId;
}

// Project Management
function editProject(projectId) {
	showNotification('Abrindo editor do projeto...', 'success');
	console.log('Editing project:', projectId);
}

async function generatePDF(projectId) {
	try {
		setLoadingText('Gerando PDF...');
		showLoading(true);
		
		const response = await apiRequest(`/projects/${projectId}/pdf`, {
			method: 'POST'
		});
		
		showNotification('PDF gerado com sucesso!', 'success');
		
		// Simular download do PDF
		if (response.pdf_url) {
			const link = document.createElement('a');
			link.href = response.pdf_url;
			link.download = `projeto_${projectId}.pdf`;
			link.click();
		}
		
		// Recarregar atividade recente
		await loadRecentActivity();
	} catch (error) {
		showNotification('Erro ao gerar PDF', 'error');
	} finally {
		showLoading(false);
	}
}

async function loadRecentActivity() {
	try {
		const response = await apiRequest('/activity');
		if (response.activity) {
			appData.recentActivity = response.activity;
			renderRecentActivity();
		}
	} catch (error) {
		console.error('Erro ao carregar atividade recente:', error);
	}
}

// Form Handling
document.getElementById('newProjectForm').addEventListener('submit', async function (e) {
	e.preventDefault();
	
	const formData = {
		title: document.getElementById('projectTitle').value,
		type: document.getElementById('projectType').value,
		description: document.getElementById('projectDescription').value,
		author: document.getElementById('projectAuthor').value,
		advisor: document.getElementById('projectAdvisor').value,
		institution: document.getElementById('projectInstitution').value,
		course: document.getElementById('projectCourse').value,
		template: document.getElementById('projectTemplate').value
	};
	
	try {
		if (editingProject) {
			// Modo de edição
			setLoadingText('Salvando alterações...');
			showLoading(true);
			
			const response = await apiRequest(`/projects/${editingProject.id}`, {
				method: 'PUT',
				body: JSON.stringify(formData)
			});
			
			// Atualizar projeto nos dados locais
			const projectIndex = appData.projects.findIndex(p => p.id === editingProject.id);
			if (projectIndex !== -1) {
				appData.projects[projectIndex] = {
					...appData.projects[projectIndex],
					...formData,
					updated_at: new Date().toISOString().split('T')[0]
				};
			}
			
			showNotification('Projeto atualizado com sucesso!', 'success');
			
			// Sair do modo de edição
			cancelEdit();
		} else {
			// Modo de criação
			setLoadingText('Criando projeto...');
			showLoading(true);
			
			const response = await apiRequest('/projects', {
				method: 'POST',
				body: JSON.stringify(formData)
			});
			
			showNotification('Projeto criado com sucesso!', 'success');
			
			// Adicionar projeto aos dados locais
			const newProject = {
				id: response.id || Date.now().toString(),
				title: formData.title,
				description: formData.description,
				status: 'draft',
				author: formData.author,
				type: formData.type,
				advisor: formData.advisor,
				institution: formData.institution,
				course: formData.course,
				template: formData.template,
				created_at: new Date().toISOString().split('T')[0]
			};
			
			appData.projects.push(newProject);
			appData.stats.activeProjects++;
			
			// Limpar formulário e ir para projetos
			clearForm();
			showSection('projects');
		}
		
		// Re-renderizar projetos e stats
		renderProjects();
		renderStats();
		
	} catch (error) {
		const errorMsg = editingProject ? 'Erro ao salvar alterações' : 'Erro ao criar projeto';
		showNotification(errorMsg, 'error');
	} finally {
		showLoading(false);
	}
});

function clearForm() {
	document.getElementById('newProjectForm').reset();
	document.getElementById('projectId').value = '';
	
	// Se estiver em modo de edição, cancelar
	if (editingProject) {
		cancelEdit();
	}
}

// File Management
document.getElementById('fileInput').addEventListener('change', function (e) {
	const files = Array.from(e.target.files);
	if (files.length > 0) {
		uploadFiles(files);
	}
});

async function uploadFiles(files) {
	try {
		setLoadingText(`Enviando ${files.length} arquivo(s)...`);
		showLoading(true);
		
		const formData = new FormData();
		files.forEach(file => {
			formData.append('files', file);
		});
		
		const response = await apiRequest('/files/upload', {
			method: 'POST',
			headers: {}, // Remove Content-Type para FormData
			body: formData
		});
		
		showNotification('Arquivos enviados com sucesso!', 'success');
		
		// Simular adição de arquivos aos dados locais
		files.forEach((file, index) => {
			const newFile = {
				id: Date.now() + index,
				name: file.name,
				size: formatFileSize(file.size),
				type: getFileType(file.name),
				icon: getFileIcon(file.name),
				color: getFileColor(file.name),
				uploaded_at: 'Agora'
			};
			appData.files.unshift(newFile);
		});
		
		appData.stats.uploadedFiles = appData.files.length;
		
		renderFiles();
		renderStats();
	} catch (error) {
		showNotification('Erro ao enviar arquivos', 'error');
	} finally {
		showLoading(false);
	}
}

async function downloadFile(fileId) {
	try {
		const response = await apiRequest(`/files/${fileId}/download`);
		showNotification('Download iniciado!', 'success');
	} catch (error) {
		showNotification('Erro ao baixar arquivo', 'error');
	}
}

async function deleteFile(fileId) {
	if (!confirm('Tem certeza que deseja excluir este arquivo?')) return;
	
	try {
		await apiRequest(`/files/${fileId}`, {
			method: 'DELETE'
		});
		
		// Remover dos dados locais
		appData.files = appData.files.filter(file => file.id != fileId);
		appData.stats.uploadedFiles = appData.files.length;
		
		renderFiles();
		renderStats();
		showNotification('Arquivo excluído com sucesso!', 'success');
	} catch (error) {
		showNotification('Erro ao excluir arquivo', 'error');
	}
}

// Template functions
function previewTemplate(templateId) {
	showNotification(`Abrindo preview do template ${templateId}...`, 'success');
}

function useTemplate(templateId) {
	showNotification(`Usando template ${templateId}...`, 'success');
}

// Configuration functions
async function testApiConnection() {
	try {
		setLoadingText('Testando conexão...');
		showLoading(true);
		
		const url = document.getElementById('apiUrl').value;
		const key = document.getElementById('apiKey').value;
		const timeout = document.getElementById('apiTimeout').value;
		
		// Atualizar configuração temporariamente para teste
		const oldConfig = {...apiConfig};
		apiConfig = {
			baseUrl: url,
			apiKey: key,
			timeout: parseInt(timeout)
		};
		
		const response = await apiRequest('/health');
		
		appData.config.system.apiStatus = 'Conectado';
		renderSystemInfo();
		showNotification('Conexão com a API estabelecida!', 'success');
	} catch (error) {
		appData.config.system.apiStatus = 'Desconectado';
		renderSystemInfo();
		showNotification('Falha na conexão com a API', 'error');
	} finally {
		showLoading(false);
	}
}

async function saveApiConfig() {
	try {
		apiConfig = {
			baseUrl: document.getElementById('apiUrl').value,
			apiKey: document.getElementById('apiKey').value,
			timeout: parseInt(document.getElementById('apiTimeout').value)
		};
		
		// Salvar na API se disponível
		await apiRequest('/config/api', {
			method: 'POST',
			body: JSON.stringify(apiConfig)
		});
		
		appData.config.api = {...apiConfig};
		showNotification('Configurações de API salvas!', 'success');
	} catch (error) {
		showNotification('Erro ao salvar configurações', 'error');
	}
}

async function saveGeneralConfig() {
	try {
		const config = {
			language: document.getElementById('defaultLanguage').value,
			dateFormat: document.getElementById('dateFormat').value,
			autoSave: parseInt(document.getElementById('autoSaveInterval').value)
		};
		
		await apiRequest('/config/general', {
			method: 'POST',
			body: JSON.stringify(config)
		});
		
		appData.config.general = {...config};
		showNotification('Preferências salvas!', 'success');
	} catch (error) {
		showNotification('Erro ao salvar preferências', 'error');
	}
}

// Drag and Drop for file upload
function setupFileUpload() {
	const fileUpload = document.querySelector('.file-upload');
	
	fileUpload.addEventListener('dragover', function (e) {
		e.preventDefault();
		this.style.background = 'rgba(102, 126, 234, 0.15)';
	});
	
	fileUpload.addEventListener('dragleave', function (e) {
		e.preventDefault();
		this.style.background = 'rgba(102, 126, 234, 0.05)';
	});
	
	fileUpload.addEventListener('drop', function (e) {
		e.preventDefault();
		this.style.background = 'rgba(102, 126, 234, 0.05)';
		const files = Array.from(e.dataTransfer.files);
		if (files.length > 0) {
			uploadFiles(files);
		}
	});
}

// Utility Functions
function showLoading(show) {
	const loading = document.getElementById('loadingModal');
	if (show) {
		loading.style.display = 'block';
		document.body.style.overflow = 'hidden';
	} else {
		loading.style.display = 'none';
		document.body.style.overflow = 'auto';
	}
}

function setLoadingText(text) {
	document.getElementById('loadingText').textContent = text;
}

function showNotification(message, type = 'success') {
	const notification = document.getElementById('notification');
	notification.textContent = message;
	notification.className = `notification ${type}`;
	notification.classList.add('show');
	setTimeout(() => {
		notification.classList.remove('show');
	}, 3000);
}

function formatFileSize(bytes) {
	const sizes = ['Bytes', 'KB', 'MB', 'GB'];
	if (bytes === 0) return '0 Bytes';
	const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
	return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

function getFileType(filename) {
	const extension = filename.split('.').pop().toLowerCase();
	const typeMap = {
		'pdf': 'pdf',
		'doc': 'document', 'docx': 'document',
		'txt': 'text',
		'bib': 'bibliography',
		'png': 'image', 'jpg': 'image', 'jpeg': 'image', 'gif': 'image'
	};
	return typeMap[extension] || 'file';
}

function getFileIcon(filename) {
	const extension = filename.split('.').pop().toLowerCase();
	const iconMap = {
		'pdf': 'fas fa-file-pdf',
		'doc': 'fas fa-file-word', 'docx': 'fas fa-file-word',
		'txt': 'fas fa-file-alt',
		'bib': 'fas fa-file-code',
		'png': 'fas fa-image', 'jpg': 'fas fa-image', 'jpeg': 'fas fa-image', 'gif': 'fas fa-image'
	};
	return iconMap[extension] || 'fas fa-file';
}

function getFileColor(filename) {
	const extension = filename.split('.').pop().toLowerCase();
	const colorMap = {
		'pdf': '#dc3545',
		'doc': '#0078d4', 'docx': '#0078d4',
		'txt': '#6c757d',
		'bib': '#17a2b8',
		'png': '#28a745', 'jpg': '#28a745', 'jpeg': '#28a745', 'gif': '#28a745'
	};
	return colorMap[extension] || '#6c757d';
}

// Função para atualizar dados externamente (simula integração com API)
function updateData(newData) {
	if (newData.stats) {
		appData.stats = {...appData.stats, ...newData.stats};
		renderStats();
	}
	if (newData.projects) {
		appData.projects = newData.projects;
		renderProjects();
	}
	if (newData.files) {
		appData.files = newData.files;
		renderFiles();
	}
	if (newData.activity) {
		appData.recentActivity = newData.activity;
		renderRecentActivity();
	}
	if (newData.templates) {
		appData.templates = newData.templates;
		renderTemplates();
	}
}

// Função para obter dados atuais (para uso externo)
function getCurrentData() {
	return JSON.parse(JSON.stringify(appData));
}

// Auto-refresh dos dados (opcional)
let autoRefreshInterval;

function startAutoRefresh(intervalMs = 30000) {
	if (autoRefreshInterval) {
		clearInterval(autoRefreshInterval);
	}
	
	autoRefreshInterval = setInterval(() => {
		if (apiConfig.baseUrl) {
			console.log('Auto-refreshing data...');
			loadData();
		}
	}, intervalMs);
}

function stopAutoRefresh() {
	if (autoRefreshInterval) {
		clearInterval(autoRefreshInterval);
		autoRefreshInterval = null;
	}
}

// Initialize
document.addEventListener('DOMContentLoaded', function () {
	// Carregar configurações salvas
	const savedApiUrl = localStorage.getItem('apiUrl');
	if (savedApiUrl) {
		document.getElementById('apiUrl').value = savedApiUrl;
		apiConfig.baseUrl = savedApiUrl;
	}
	
	// Renderizar dados iniciais
	renderStats();
	renderRecentActivity();
	renderProjects();
	renderFiles();
	renderTemplates();
	renderSystemInfo();
	
	// Configurar upload de arquivos
	setupFileUpload();
	
	// Tentar carregar dados da API
	loadData();
	
	console.log('Academic Manager Frontend initialized');
	console.log('Use updateData(newData) para atualizar dados externamente');
	console.log('Use getCurrentData() para obter dados atuais');
});

// Expor funções globais para uso externo
window.AcademicManager = {
	updateData,
	getCurrentData,
	loadData,
	startAutoRefresh,
	stopAutoRefresh,
	showNotification
};