/**
 * Paper Analysis Frontend Application
 * Main application logic
 */

// =============================================================================
// Configuration
// =============================================================================

const API_BASE_URL = 'http://127.0.0.1:8000';
const API_ANALYZE_ENDPOINT = `${API_BASE_URL}/api/v1/analyze`;
const MAX_FILE_SIZE_MB = 50;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

// =============================================================================
// DOM Elements
// =============================================================================

const elements = {
    pdfInput: document.getElementById('pdfInput'),
    fileInfo: document.getElementById('fileInfo'),
    templateSelect: document.getElementById('templateSelect'),
    analyzeButton: document.getElementById('analyzeButton'),

    uploadSection: document.getElementById('uploadSection'),
    progressSection: document.getElementById('progressSection'),
    resultSection: document.getElementById('resultSection'),
    errorSection: document.getElementById('errorSection'),

    resultMeta: document.getElementById('resultMeta'),
    resultContent: document.getElementById('resultContent'),
    errorMessage: document.getElementById('errorMessage'),

    copyButton: document.getElementById('copyButton'),
    downloadButton: document.getElementById('downloadButton'),
    newAnalysisButton: document.getElementById('newAnalysisButton'),
    retryButton: document.getElementById('retryButton')
};

// =============================================================================
// State
// =============================================================================

let state = {
    selectedFile: null,
    analysisResult: null
};

// =============================================================================
// Initialization
// =============================================================================

function initialize() {
    attachEventListeners();
    validateForm();
}

function attachEventListeners() {
    elements.pdfInput.addEventListener('change', handleFileSelect);
    elements.analyzeButton.addEventListener('click', handleAnalyze);
    elements.copyButton.addEventListener('click', handleCopy);
    elements.downloadButton.addEventListener('click', handleDownload);
    elements.newAnalysisButton.addEventListener('click', handleNewAnalysis);
    elements.retryButton.addEventListener('click', handleRetry);
}

// =============================================================================
// File Handling
// =============================================================================

function handleFileSelect(event) {
    const file = event.target.files[0];

    if (!file) {
        clearFileSelection();
        return;
    }

    const validation = validateFile(file);
    if (!validation.valid) {
        showError(validation.message);
        clearFileSelection();
        return;
    }

    state.selectedFile = file;
    displayFileInfo(file);
    validateForm();
}

function validateFile(file) {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        return {
            valid: false,
            message: 'PDF 파일만 업로드 가능합니다.'
        };
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
        return {
            valid: false,
            message: `파일 크기는 ${MAX_FILE_SIZE_MB}MB를 초과할 수 없습니다.`
        };
    }

    return { valid: true };
}

function displayFileInfo(file) {
    const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
    elements.fileInfo.textContent = `선택된 파일: ${file.name} (${sizeInMB} MB)`;
    elements.fileInfo.classList.remove('hidden');
}

function clearFileSelection() {
    state.selectedFile = null;
    elements.pdfInput.value = '';
    elements.fileInfo.classList.add('hidden');
    validateForm();
}

// =============================================================================
// Form Validation
// =============================================================================

function validateForm() {
    const isValid = state.selectedFile !== null;
    elements.analyzeButton.disabled = !isValid;
}

// =============================================================================
// Analysis
// =============================================================================

async function handleAnalyze() {
    if (!state.selectedFile) {
        return;
    }

    showProgressSection();

    try {
        const result = await analyzeDocument();
        state.analysisResult = result;
        showResultSection(result);
    } catch (error) {
        showErrorSection(error.message);
    }
}

async function analyzeDocument() {
    const formData = createFormData();

    const response = await fetch(API_ANALYZE_ENDPOINT, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
            errorData.detail || `분석 실패: ${response.statusText}`
        );
    }

    return await response.json();
}

function createFormData() {
    const formData = new FormData();
    formData.append('file', state.selectedFile);
    return formData;
}

// =============================================================================
// UI State Management
// =============================================================================

function showProgressSection() {
    hideAllSections();
    elements.progressSection.classList.remove('hidden');
}

function showResultSection(result) {
    hideAllSections();
    displayAnalysisResult(result);
    elements.resultSection.classList.remove('hidden');
}

function showErrorSection(message) {
    hideAllSections();
    elements.errorMessage.textContent = message;
    elements.errorSection.classList.remove('hidden');
}

function hideAllSections() {
    elements.uploadSection.classList.add('hidden');
    elements.progressSection.classList.add('hidden');
    elements.resultSection.classList.add('hidden');
    elements.errorSection.classList.add('hidden');
}

// =============================================================================
// Result Display
// =============================================================================

function displayAnalysisResult(result) {
    displayMetadata(result);
    displayMarkdownContent(result.markdown_content);
}

function displayMetadata(result) {
    const metadata = [
        `PDF: ${result.pdf_filename}`,
        `분석 페이지: ${result.total_pages}`,
        `모델: ${result.model_used}`,
        `생성 시각: ${result.analysis_timestamp}`
    ];

    elements.resultMeta.innerHTML = metadata.join(' | ');
}

function displayMarkdownContent(markdown) {
    const html = MarkdownRenderer.render(markdown);
    elements.resultContent.innerHTML = html;
}

// =============================================================================
// Actions
// =============================================================================

function handleCopy() {
    if (!state.analysisResult) {
        return;
    }

    copyToClipboard(state.analysisResult.markdown_content);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            showTemporaryMessage(elements.copyButton, '복사됨!');
        })
        .catch(() => {
            alert('복사 실패. 다시 시도해주세요.');
        });
}

function showTemporaryMessage(button, message) {
    const originalText = button.textContent;
    button.textContent = message;
    setTimeout(() => {
        button.textContent = originalText;
    }, 2000);
}

function handleDownload() {
    if (!state.analysisResult) {
        return;
    }

    downloadMarkdown(
        state.analysisResult.markdown_content,
        state.analysisResult.pdf_filename
    );
}

function downloadMarkdown(content, pdfFilename) {
    const filename = generateDownloadFilename(pdfFilename);
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();

    URL.revokeObjectURL(url);
}

function generateDownloadFilename(pdfFilename) {
    const baseName = pdfFilename.replace('.pdf', '');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    return `${baseName}_analysis_${timestamp}.md`;
}

function handleNewAnalysis() {
    state.selectedFile = null;
    state.analysisResult = null;

    clearFileSelection();
    hideAllSections();
    elements.uploadSection.classList.remove('hidden');
}

function handleRetry() {
    hideAllSections();
    elements.uploadSection.classList.remove('hidden');
}

function showError(message) {
    alert(message);
}

// =============================================================================
// Initialize on DOM Load
// =============================================================================

document.addEventListener('DOMContentLoaded', initialize);
