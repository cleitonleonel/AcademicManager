/* jshint esversion: 9 */
'use strict';


export function showSection(sectionId, event = null) {
	// esconder todas as seções
	document.querySelectorAll('.content-section').forEach(s =>
		s.classList.remove('active')
	);
	
	// remover destaque dos itens do menu
	document.querySelectorAll('.nav-item').forEach(i =>
		i.classList.remove('active')
	);
	
	// ativar a seção escolhida
	const section = document.getElementById(sectionId);
	if (section) section.classList.add('active');
	
	// marcar item ativo
	if (event) event.currentTarget.classList.add('active');
}
