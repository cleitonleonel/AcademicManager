/* jshint esversion: 9 */
'use strict';


export function showNotification(message, type = 'success') {
	const notification = document.getElementById('notification');
	notification.textContent = message;
	notification.className = `notification ${type}`;
	notification.classList.add('show');
	setTimeout(() => notification.classList.remove('show'), 3000);
}

export function editProject(projectId) {
	showNotification('Abrindo editor do projeto...', 'success');
	console.log('Editing project:', projectId);
}

export function generatePDF(projectId) {
	showLoading(true);
	showNotification('Gerando PDF...', 'success');
	
	setTimeout(() => {
		showLoading(false);
		showNotification('PDF gerado com sucesso!', 'success');
		
		console.log('Generating PDF for:', projectId);
	}, 3000);
}

export function showLoading(show) {
	const loading = document.getElementById('loadingModal');
	if (show) {
		loading.style.display = 'block';
		document.body.style.overflow = 'hidden';
	} else {
		loading.style.display = 'none';
		document.body.style.overflow = 'auto';
	}
}

export function setLoadingText(text) {
	document.getElementById('loadingText').textContent = text;
}

export function formatFileSize(bytes) {
	const sizes = ['Bytes', 'KB', 'MB', 'GB'];
	if (bytes === 0) return '0 Bytes';
	const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
	return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

export function getFileType(filename) {
	const extension = filename.split('.').pop().toLowerCase();
	const map = {
		pdf: 'pdf', doc: 'document', docx: 'document', txt: 'text', bib: 'bibliography',
		png: 'image', jpg: 'image', jpeg: 'image', gif: 'image'
	};
	return map[extension] || 'file';
}

export function getFileIcon(filename) {
	const extension = filename.split('.').pop().toLowerCase();
	const map = {
		pdf: 'fas fa-file-pdf', doc: 'fas fa-file-word', docx: 'fas fa-file-word',
		txt: 'fas fa-file-alt', bib: 'fas fa-file-code', png: 'fas fa-image',
		jpg: 'fas fa-image', jpeg: 'fas fa-image', gif: 'fas fa-image'
	};
	return map[extension] || 'fas fa-file';
}

export function getFileColor(filename) {
	const extension = filename.split('.').pop().toLowerCase();
	const map = {
		pdf: '#dc3545', doc: '#0078d4', docx: '#0078d4', txt: '#6c757d',
		bib: '#17a2b8', png: '#28a745', jpg: '#28a745', jpeg: '#28a745', gif: '#28a745'
	};
	return map[extension] || '#6c757d';
}

export function getStatusText(status) {
	return {draft: 'Rascunho', progress: 'Em Progresso', completed: 'Concluído'}[status] || status;
}
