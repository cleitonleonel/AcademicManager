/* jshint esversion: 9 */
'use strict';


import { appData } from "../data.js";

export function renderFiles() {
  const container = document.getElementById("files-list");
  if (!container) return;

  container.innerHTML = appData.files.map(f => `
    <div class="file-item">
      <i class="${f.icon}" style="color:${f.color}"></i>
      <span>${f.name} (${f.size})</span>
    </div>
  `).join('');
}
