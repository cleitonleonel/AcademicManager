/* jshint esversion: 9 */
'use strict';

import { appData } from "./data.js";

// Load from localStorage if available (session/dynamic overrides)
const savedConfig = JSON.parse(localStorage.getItem('academic_api_config') || '{}');

export let apiConfig = {
  baseUrl: savedConfig.baseUrl || 'http://localhost:8000/api',
  apiKey: savedConfig.apiKey || '',
  timeout: savedConfig.timeout || 10000,
  pdfOptions: savedConfig.pdfOptions || { font: 'Arial', quality: 'high' }
};

/**
 * Make an authenticated request to the real API.
 * Falls back to local mock data if the server is unreachable.
 */
export async function apiRequest(endpoint, options = {}) {
  try {
    const url = `${apiConfig.baseUrl}${endpoint}`;
    const isFormData = options.body instanceof FormData;
    const config = {
      headers: {
        ...(!isFormData && { 'Content-Type': 'application/json' }),
        ...(apiConfig.apiKey && { 'Authorization': `Bearer ${apiConfig.apiKey}` }),
        ...(apiConfig.pdfOptions && { 'X-PDF-Options': JSON.stringify(apiConfig.pdfOptions) }),
        ...options.headers
      },
      ...options
    };
    const response = await fetch(url, config);
    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw new Error(errorBody.detail || `HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.warn('API indisponível, fallback local:', error.message);
    return handleLocalData(endpoint, options.method || 'GET');
  }
}

/**
 * Download a binary file from the API (e.g. a generated PDF).
 * Returns a Blob URL that can be assigned to an anchor's href.
 */
export async function downloadFile(endpoint) {
  const url = `${apiConfig.baseUrl}${endpoint}`;
  const response = await fetch(url, {
    headers: apiConfig.apiKey
      ? { 'Authorization': `Bearer ${apiConfig.apiKey}` }
      : {}
  });
  if (!response.ok) throw new Error(`Download failed: HTTP ${response.status}`);
  const blob = await response.blob();
  return URL.createObjectURL(blob);
}

/** Local fallback data when the server is not running. */
function handleLocalData(endpoint, method = 'GET') {
  const paths = endpoint.split('/').filter(Boolean);
  switch (paths[0]) {
    case 'stats':    return { active_projects: 0, generated_pdfs: 0, in_progress: 0, total_files: 0 };
    case 'projects': return method === 'POST' ? { status: 'success', project_folder: 'local' } : { projects: appData.projects };
    case 'assignments': return { assignments: [] };
    case 'health':   return { status: 'ok', message: 'local', projects_count: 0 };
    default:         return { status: 'success' };
  }
}
