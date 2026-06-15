// Main JavaScript for UniBot

// Utility function for console logging
function log(message, type = 'info') {
    const prefix = '🤖 [UniBot]';
    if (type === 'error') {
        console.error(prefix, message);
    } else if (type === 'warn') {
        console.warn(prefix, message);
    } else {
        console.log(prefix, message);
    }
}

// Debounce utility
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Format timestamp
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
}