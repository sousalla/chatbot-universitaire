// Chat functionality for UniBot

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const welcomeMessage = document.getElementById('welcomeMessage');
const statusBanner = document.getElementById('statusBanner');
const statusText = document.getElementById('statusText');
const modelStatus = document.getElementById('modelStatus');

// State
let isWaiting = false;
let currentSessionId = null;

// Initialize chat
document.addEventListener('DOMContentLoaded', () => {
    log('Chat initialized');
    setupEventListeners();
    checkServerStatus();
    loadHistory();
    userInput?.focus();
});

// Setup event listeners
function setupEventListeners() {
    sendBtn?.addEventListener('click', sendMessage);
    clearBtn?.addEventListener('click', clearHistory);
    userInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // Quick questions
    document.querySelectorAll('.quick-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const question = btn.getAttribute('data-question');
            if (question) {
                userInput.value = question;
                sendMessage();
            }
        });
    });
}

// Check server status
async function checkServerStatus() {
    try {
        const isHealthy = await API.healthCheck();
        if (isHealthy) {
            const status = await API.getStatus();
            updateStatusBanner(status);
            updateModelStatus(status);
        } else {
            statusBanner.className = 'alert alert-danger alert-dismissible fade show mb-3';
            statusText.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Serveur indisponible';
            modelStatus.innerHTML = '<i class="fas fa-times-circle me-1"></i> Hors ligne';
        }
    } catch (error) {
        log('Server check failed', 'error');
        statusBanner.className = 'alert alert-danger alert-dismissible fade show mb-3';
        statusText.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Connexion au serveur impossible';
        modelStatus.innerHTML = '<i class="fas fa-times-circle me-1"></i> Hors ligne';
    }
}

// Update status banner
function updateStatusBanner(status) {
    if (status && status.llm_loaded && status.vector_store_ready) {
        statusBanner.className = 'alert alert-success alert-dismissible fade show mb-3';
        statusText.innerHTML = '<i class="fas fa-check-circle me-2"></i>Système opérationnel - Modèle actif + Base vectorielle prête';
    } else if (status && status.vector_store_ready) {
        statusBanner.className = 'alert alert-warning alert-dismissible fade show mb-3';
        statusText.innerHTML = '<i class="fas fa-database me-2"></i>Base vectorielle prête (recherche uniquement)';
    } else {
        statusBanner.className = 'alert alert-info alert-dismissible fade show mb-3';
        statusText.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Initialisation en cours...';
    }
}

// Update model status
function updateModelStatus(status) {
    if (status && status.llm_loaded) {
        modelStatus.innerHTML = '<i class="fas fa-microchip text-success me-1"></i> Gemma actif';
    } else {
        modelStatus.innerHTML = '<i class="fas fa-microchip text-warning me-1"></i> Mode recherche';
    }
}

// Add a message to the chat
function addMessage(text, isUser) {
    if (welcomeMessage) welcomeMessage.style.display = 'none';
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = formatMessage(text);
    
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Format message (links, line breaks, code blocks)
function formatMessage(text) {
    if (!text) return '';
    
    // Convert URLs to clickable links
    let formatted = text.replace(/(https?:\/\/[^\s]+)/g, (url) => {
        const displayUrl = url.length > 50 ? url.substring(0, 47) + '...' : url;
        return `<a href="${url}" target="_blank" rel="noopener noreferrer">🔗 ${displayUrl}</a>`;
    });
    
    // Convert line breaks to <br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Highlight bold text
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    return formatted;
}

// Show typing indicator
let typingDiv = null;

function showTyping() {
    removeTyping();
    
    typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `<div class="typing-indicator">
        <i class="fas fa-microchip me-2"></i>
        Gemma génère une réponse<span class="typing-dots"></span>
    </div>`;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

function removeTyping() {
    if (typingDiv && typingDiv.parentNode) {
        typingDiv.remove();
        typingDiv = null;
    }
}

// Scroll to bottom
function scrollToBottom() {
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Send message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message || isWaiting) return;
    
    log(`Sending: ${message.substring(0, 50)}...`);
    
    // Hide welcome message
    if (welcomeMessage) welcomeMessage.style.display = 'none';
    
    // Add user message
    addMessage(message, true);
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;
    
    // Show typing
    showTyping();
    isWaiting = true;
    
    try {
        const response = await API.sendMessage(message);
        removeTyping();
        
        if (response.success && response.response) {
            addMessage(response.response, false);
        } else {
            addMessage("Une erreur s'est produite. Veuillez réessayer.", false);
        }
    } catch (error) {
        log(`Error: ${error.message}`, 'error');
        removeTyping();
        addMessage("❌ Erreur de connexion au serveur. Vérifiez que le serveur est en cours d'exécution.", false);
    } finally {
        isWaiting = false;
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Load history
async function loadHistory() {
    try {
        const history = await API.getHistory();
        
        if (history && history.length > 0) {
            if (welcomeMessage) welcomeMessage.style.display = 'none';
            
            for (const item of history) {
                addMessage(item.user, true);
                addMessage(item.bot, false);
            }
            scrollToBottom();
        }
        
        log(`Loaded ${history.length} messages from history`);
    } catch (error) {
        log('Error loading history', 'error');
    }
}

// Clear history
async function clearHistory() {
    if (!confirm('Êtes-vous sûr de vouloir effacer l\'historique de la conversation ?')) {
        return;
    }
    
    try {
        await API.clearHistory();
        chatMessages.innerHTML = '';
        if (welcomeMessage) welcomeMessage.style.display = 'block';
        log('History cleared');
    } catch (error) {
        log('Error clearing history', 'error');
    }
}