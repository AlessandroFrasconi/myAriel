// Course Page JavaScript

let courseData = null;

// Carica i dettagli del corso all'avvio
document.addEventListener('DOMContentLoaded', () => {
    loadCourseDetails();
    setupModalHandlers();
});

// Carica i dettagli del corso
async function loadCourseDetails() {
    showLoading(true);
    
    try {
        const response = await fetch(`/api/course/${COURSE_ID}/details`);
        const data = await response.json();
        
        if (data.success) {
            courseData = data.data;
            displayCourseDetails(courseData);
            showLoading(false);
        } else {
            showError(data.message);
        }
    } catch (error) {
        console.error('Errore caricamento corso:', error);
        showError('Errore di connessione al server');
    }
}

// Mostra i dettagli del corso
function displayCourseDetails(data) {
    // Titolo e breadcrumb
    document.getElementById('courseTitle').textContent = data.name;
    document.getElementById('courseName').textContent = data.name;
    
    // Annunci
    displayAnnouncements(data.annunci || []);
    
    // Programma
    displayProgramma(data.programma || '');
    
    // Videolezioni
    displayVideolezioni(data.videolezioni || []);
    
    // Risorse
    displayResources(data.risorse || []);
    
    // Mostra il contenuto
    document.getElementById('courseContent').style.display = 'block';
}

// Mostra gli annunci (primi 5)
function displayAnnouncements(annunci) {
    const container = document.getElementById('announcementsList');
    const showAllBtn = document.getElementById('showAllAnnouncements');
    
    if (annunci.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📭</div><p>Nessun annuncio disponibile</p></div>';
        return;
    }
    
    // Mostra solo i primi 5
    const displayedAnnunci = annunci.slice(0, 5);
    
    container.innerHTML = displayedAnnunci.map(ann => `
        <div class="announcement-card">
            <h3>${escapeHtml(ann.title)}</h3>
            ${ann.date ? `<div class="announcement-date">${escapeHtml(ann.date)}</div>` : ''}
            <div class="announcement-content">${escapeHtml(ann.content)}</div>
        </div>
    `).join('');
    
    // Mostra il pulsante "Mostra tutti" se ci sono più di 5 annunci
    if (annunci.length > 5) {
        showAllBtn.style.display = 'block';
    }
}

// Mostra il programma del corso
function displayProgramma(programmaHtml) {
    const container = document.getElementById('programmaContent');
    
    if (!programmaHtml || programmaHtml.trim() === '') {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📄</div><p>Programma non disponibile</p></div>';
        return;
    }
    
    // Inserisci l'HTML del programma (già ripulito dal backend)
    container.innerHTML = programmaHtml;
}

// Mostra le videolezioni
function displayVideolezioni(videolezioni) {
    const container = document.getElementById('videolezioniList');
    
    if (videolezioni.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🎬</div><p>Nessuna videolezione disponibile</p></div>';
        return;
    }
    
    container.innerHTML = videolezioni.map(video => `
        <a href="${video.url}" target="_blank" rel="noopener noreferrer" class="video-link">
            <div>
                <div>${escapeHtml(video.name)}</div>
                <small class="video-section-label">${escapeHtml(video.section)}</small>
            </div>
        </a>
    `).join('');
}

// Mostra le risorse organizzate per sezione
function displayResources(risorse) {
    const container = document.getElementById('resourcesList');
    
    if (risorse.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📦</div><p>Nessuna risorsa disponibile</p></div>';
        return;
    }
    
    container.innerHTML = risorse.map(section => createSectionCard(section)).join('');
    
    // Aggiungi event listeners per le sezioni
    document.querySelectorAll('.section-card').forEach(card => {
        const header = card.querySelector('.section-header');
        header.addEventListener('click', () => toggleSection(card));
    });
    
    // Aggiungi event listeners per le cartelle
    document.querySelectorAll('.folder-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            toggleFolder(item);
        });
    });
}

// Crea una card di sezione
function createSectionCard(section) {
    const resources = section.resources || [];
    
    return `
        <div class="section-card">
            <div class="section-header">
                <span>📚 ${escapeHtml(section.section)}</span>
                <span class="section-toggle">▼</span>
            </div>
            <div class="section-content">
                <ul class="resource-list">
                    ${resources.map(res => createResourceItem(res)).join('')}
                </ul>
            </div>
        </div>
    `;
}

// Crea un elemento risorsa
function createResourceItem(resource) {
    const icon = getResourceIcon(resource.type);
    
    if (resource.type === 'folder') {
        return `
            <li class="resource-item folder-item" data-url="${resource.url}">
                <span class="resource-icon">${icon}</span>
                <span class="resource-link">${escapeHtml(resource.name)}</span>
            </li>
        `;
    } else {
        return `
            <li class="resource-item">
                <span class="resource-icon">${icon}</span>
                <a href="${resource.url}" target="_blank" rel="noopener noreferrer" class="resource-link">
                    ${escapeHtml(resource.name)}
                </a>
            </li>
        `;
    }
}

// Ottieni icona per tipo risorsa
function getResourceIcon(type) {
    const icons = {
        'file': '📄',
        'pdf': '📕',
        'url': '🔗',
        'folder': '📁',
        'page': '📃',
        'assignment': '📝',
        'quiz': '❓',
        'forum': '💬',
        'video': '🎥'
    };
    return icons[type] || '📌';
}

// Toggle sezione
function toggleSection(card) {
    card.classList.toggle('expanded');
}

// Toggle cartella (carica contenuto se non già caricato)
async function toggleFolder(folderItem) {
    const folderUrl = folderItem.dataset.url;
    const existingContents = folderItem.querySelector('.folder-contents');
    
    // Se già espansa, comprimi
    if (existingContents) {
        existingContents.remove();
        return;
    }
    
    // Mostra loading
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'folder-contents folder-loading';
    loadingDiv.textContent = 'Caricamento...';
    folderItem.appendChild(loadingDiv);
    
    try {
        const response = await fetch('/api/folder/contents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: folderUrl })
        });
        
        const data = await response.json();
        
        if (data.success && data.files.length > 0) {
            loadingDiv.remove();
            
            const contentsDiv = document.createElement('div');
            contentsDiv.className = 'folder-contents';
            contentsDiv.innerHTML = `
                <ul class="resource-list">
                    ${data.files.map(file => createResourceItem(file)).join('')}
                </ul>
            `;
            folderItem.appendChild(contentsDiv);
            
            // Aggiungi event listener per sotto-cartelle (ricorsivo)
            contentsDiv.querySelectorAll('.folder-item').forEach(subFolder => {
                subFolder.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    toggleFolder(subFolder);
                });
            });
        } else {
            loadingDiv.textContent = 'Cartella vuota';
        }
    } catch (error) {
        console.error('Errore caricamento cartella:', error);
        loadingDiv.textContent = 'Errore caricamento';
    }
}

// Setup modal handlers
function setupModalHandlers() {
    const modal = document.getElementById('announcementsModal');
    const btn = document.getElementById('showAllAnnouncements');
    const span = document.querySelector('.close');
    
    btn.addEventListener('click', () => {
        showAllAnnouncementsModal();
    });
    
    span.addEventListener('click', () => {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
}

// Mostra tutti gli annunci nel modal
function showAllAnnouncementsModal() {
    const modal = document.getElementById('announcementsModal');
    const container = document.getElementById('allAnnouncementsList');
    
    if (!courseData || !courseData.annunci) return;
    
    container.innerHTML = courseData.annunci.map(ann => `
        <div class="announcement-card">
            <h3>${escapeHtml(ann.title)}</h3>
            ${ann.date ? `<div class="announcement-date">${escapeHtml(ann.date)}</div>` : ''}
            <div class="announcement-content">${escapeHtml(ann.content)}</div>
        </div>
    `).join('');
    
    modal.style.display = 'block';
}

// Mostra/nascondi loading
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('courseContent').style.display = show ? 'none' : 'block';
}

// Mostra errore
function showError(message) {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('errorState').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

// Utility: escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
