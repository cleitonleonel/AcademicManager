/* jshint esversion: 9 */
'use strict';


import { appData } from "../data.js";

export function renderSystemInfo() {
  const container = document.getElementById("system-info");
  if (!container) return;

  const sys = appData.config.system;
  container.innerHTML = `
    <div>Versão: ${sys.version}</div>
    <div>Python: ${sys.pythonVersion}</div>
    <div>Status: ${sys.apiStatus}</div>
    <div>Projetos: ${sys.totalProjects}</div>
  `;
}
