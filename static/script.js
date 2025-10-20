// Stato dell'applicazione
let allResources = [];
let isCompactView = false;

// Icone per tipo di risorsa
const RESOURCE_ICONS = {
    'file': '📄',
    'pdf': '📕',
    'url': '🔗',
    'folder': '📁',
    'page': '📃',
    'video': '🎥',
    'default': '📌'
};

// Inizializzazione
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎓 MyAriel Resource Manager inizializzato');
    
    // Event listeners
    document.getElementById('refreshBtn').addEventListener('click', loadResources);
    document.getElementById('toggleViewBtn').addEventListener('click', toggleView);
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // Carica risorse automaticamente
    loadResources();
});

// Gestione login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const domain = document.getElementById('domain').value;
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, domain })
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('loginSection').style.display = 'none';
            document.getElementById('cookieSection').style.display = 'none';
            showNotification('✓ Login effettuato!', 'success');
            loadResources();
        } else {
            showNotification('✗ ' + data.message, 'error');
        }
    } catch (error) {
        showNotification('✗ Errore di connessione', 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}
// Carica risorse
async function loadResources(refresh = false) {
    showLoading(true);
    hideEmpty();
    
    try {
        const url = '/api/resources' + (refresh ? '?refresh=true' : '');
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            allResources = data.data;
            
            // Mostra info cache
            if (data.cached) {
                showCacheInfo(data.timestamp);
            } else {
                hideCacheInfo();
            }
            
            displayResources(allResources);
            
            if (allResources.length === 0) {
                showEmpty();
            }
        } else {
            // Se fallisce, mostra form di login
            if (data.message.includes('Credenziali') || data.message.includes('login')) {
                document.getElementById('loginSection').style.display = 'block';
            }
            showNotification('✗ ' + data.message, 'error');
        }
    } catch (error) {
        showNotification('✗ Errore di connessione al server', 'error');
        console.error(error);
        showEmpty();
    } finally {
        showLoading(false);
    }
}

// Visualizza risorse
function displayResources(resources) {
    const container = document.getElementById('resourcesContainer');
    container.innerHTML = '';
    
    if (!resources || resources.length === 0) {
        showEmpty();
        return;
    }
    
    // Filtra corsi che hanno almeno una sezione con risorse
    const coursesWithResources = resources.filter(courseData => 
        courseData.sections && courseData.sections.length > 0
    );
    
    if (coursesWithResources.length === 0) {
        showEmpty();
        return;
    }
    
    coursesWithResources.forEach((courseData, index) => {
        const courseCard = createCourseCard(courseData, index);
        container.appendChild(courseCard);
    });
}

// Crea card per corso
function createCourseCard(courseData, index) {
    const { course, sections } = courseData;
    
    const card = document.createElement('div');
    card.className = 'course-card';
    card.dataset.courseId = course.id;
    
    // Header
    const header = document.createElement('div');
    header.className = 'course-header';
    header.innerHTML = `
        <h3>${escapeHtml(course.name)}</h3>
        <span class="course-toggle">▼</span>
    `;
    header.addEventListener('click', () => toggleCourse(card));
    
    // Content
    const content = document.createElement('div');
    content.className = 'course-content';
    
    // Aggiungi solo sezioni con risorse (i corsi senza sezioni sono già filtrati in displayResources)
    sections.forEach(section => {
        const sectionDiv = createSectionElement(section);
        content.appendChild(sectionDiv);
    });
    
    card.appendChild(header);
    card.appendChild(content);
    
    return card;
}

// Crea elemento sezione
function createSectionElement(section) {
    const div = document.createElement('div');
    div.className = 'section';
    
    const title = document.createElement('h4');
    title.innerHTML = `📚 ${escapeHtml(section.section)}`;
    div.appendChild(title);
    
    if (section.resources && section.resources.length > 0) {
        const list = document.createElement('ul');
        list.className = 'resource-list';
        
        section.resources.forEach(resource => {
            const item = createResourceItem(resource);
            list.appendChild(item);
        });
        
        div.appendChild(list);
    }
    
    return div;
}

// Crea elemento risorsa
function createResourceItem(resource) {
    const li = document.createElement('li');
    li.className = 'resource-item';
    
    const icon = getResourceIcon(resource);
    const iconSpan = document.createElement('span');
    iconSpan.className = 'resource-icon';
    iconSpan.textContent = icon;
    
    const link = document.createElement('a');
    link.className = 'resource-link';
    link.href = resource.url;
    link.textContent = resource.name;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    
    const type = document.createElement('span');
    type.className = 'resource-type';
    type.textContent = getResourceTypeLabel(resource.type);
    
    li.appendChild(iconSpan);
    li.appendChild(link);
    li.appendChild(type);
    
    return li;
}

// Ottieni icona per risorsa
function getResourceIcon(resource) {
    if (resource.name.toLowerCase().includes('.pdf')) return RESOURCE_ICONS.pdf;
    if (resource.type === 'url') return RESOURCE_ICONS.url;
    if (resource.type === 'folder') return RESOURCE_ICONS.folder;
    if (resource.type === 'page') return RESOURCE_ICONS.page;
    if (resource.name.toLowerCase().match(/\.(mp4|avi|mov|wmv)/)) return RESOURCE_ICONS.video;
    if (resource.type === 'file') return RESOURCE_ICONS.file;
    return RESOURCE_ICONS.default;
}

// Ottieni etichetta tipo risorsa
function getResourceTypeLabel(type) {
    const labels = {
        'file': 'File',
        'url': 'Link',
        'folder': 'Cartella',
        'page': 'Pagina',
        'video': 'Video'
    };
    return labels[type] || 'Risorsa';
}

// Toggle corso (espandi/comprimi)
function toggleCourse(card) {
    card.classList.toggle('expanded');
}

// Toggle vista compatta
function toggleView() {
    isCompactView = !isCompactView;
    const container = document.getElementById('resourcesContainer');
    const btn = document.getElementById('toggleViewBtn');
    
    if (isCompactView) {
        container.classList.add('compact-view');
        btn.textContent = '📋 Vista Normale';
    } else {
        container.classList.remove('compact-view');
        btn.textContent = '📋 Vista Compatta';
    }
}

// Gestione ricerca
function handleSearch(e) {
    const query = e.target.value.toLowerCase().trim();
    
    if (!query) {
        displayResources(allResources);
        return;
    }
    
    const filtered = allResources.map(courseData => {
        // Filtra per nome corso
        const courseMatch = courseData.course.name.toLowerCase().includes(query);
        
        // Filtra sezioni e risorse
        const filteredSections = courseData.sections
            .map(section => {
                const sectionMatch = section.section.toLowerCase().includes(query);
                const filteredResources = section.resources.filter(resource =>
                    resource.name.toLowerCase().includes(query)
                );
                
                if (sectionMatch || filteredResources.length > 0) {
                    return {
                        ...section,
                        resources: sectionMatch ? section.resources : filteredResources
                    };
                }
                return null;
            })
            .filter(s => s !== null);
        
        if (courseMatch || filteredSections.length > 0) {
            return {
                course: courseData.course,
                sections: courseMatch ? courseData.sections : filteredSections
            };
        }
        return null;
    }).filter(c => c !== null);
    
    displayResources(filtered);
    
    // Espandi automaticamente i risultati
    if (query) {
        setTimeout(() => {
            document.querySelectorAll('.course-card').forEach(card => {
                card.classList.add('expanded');
            });
        }, 100);
    }
}

// Mostra/nascondi loading
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// Mostra/nascondi empty state
function showEmpty() {
    document.getElementById('emptyState').style.display = 'block';
    document.getElementById('resourcesContainer').style.display = 'none';
}

function hideEmpty() {
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('resourcesContainer').style.display = 'block';
}

// Info cache
function showCacheInfo(timestamp) {
    const info = document.getElementById('cacheInfo');
    const date = new Date(timestamp);
    const timeStr = date.toLocaleString('it-IT');
    info.innerHTML = `ℹ️ Dati dalla cache (ultimo aggiornamento: ${timeStr}). <a href="#" onclick="loadResources(true); return false;" style="color: #0066cc; text-decoration: underline;">Aggiorna ora</a>`;
    info.style.display = 'block';
}

function hideCacheInfo() {
    document.getElementById('cacheInfo').style.display = 'none';
}

// Notifiche
function showNotification(message, type = 'info') {
    // Implementazione semplice con alert (può essere migliorata)
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Crea notifica visiva
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#e74c3c' : type === 'success' ? '#27ae60' : '#3498db'};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Utility: escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Aggiungi animazioni CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
